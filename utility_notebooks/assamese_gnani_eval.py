"""
TTS Voice Quality Evaluation via Gnani ASR — Assamese
Transcribes audio from TTS voice directories using Gnani Prisma v2.5,
then computes WER & CER against Assamese reference sentences.

Uses soundfile + numpy for robust audio format handling (supports IEEE float WAV).
"""
import io
import os
import json
import csv
import time
import wave
import struct
import argparse
import requests
import numpy as np
import soundfile as sf
import editdistance
from pathlib import Path
from datetime import datetime
from typing import Optional

# ─── CONFIG ──────────────────────────────────────────────────────────────────

API_URL           = "https://api.vachana.ai/stt/v3"
LANGUAGE_CODE     = "as-IN"
FORMAT            = "transcribe"
REQUEST_DELAY_SEC = 1.2

# ─── METRICS ─────────────────────────────────────────────────────────────────

def normalize(text: str) -> str:
    return " ".join(text.strip().lower().split())

def compute_wer(ref: str, hyp: str) -> float:
    r, h = normalize(ref).split(), normalize(hyp).split()
    return editdistance.eval(r, h) / len(r) if r else 0.0

def compute_cer(ref: str, hyp: str) -> float:
    r = list(normalize(ref).replace(" ", ""))
    h = list(normalize(hyp).replace(" ", ""))
    return editdistance.eval(r, h) / len(r) if r else 0.0

# ─── AUDIO CONVERSION ────────────────────────────────────────────────────────

def read_and_convert_to_16k_wav(audio_path: Path) -> bytes:
    """Read any WAV format (incl. IEEE float) and convert to 16kHz mono 16-bit PCM."""
    data, samplerate = sf.read(str(audio_path), dtype='float32')

    # Downmix to mono if stereo/multi-channel
    if data.ndim > 1:
        data = np.mean(data, axis=1)

    # Simple resampling to 16000 Hz via linear interpolation
    if samplerate != 16000:
        duration = len(data) / samplerate
        new_length = int(duration * 16000)
        old_indices = np.linspace(0, len(data) - 1, new_length)
        data = np.interp(old_indices, np.arange(len(data)), data)

    # Convert float [-1, 1] to int16
    data = np.clip(data * 32767, -32768, 32767).astype(np.int16)

    # Write to in-memory WAV
    buf = io.BytesIO()
    with wave.open(buf, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(16000)
        wf.writeframes(data.tobytes())
    return buf.getvalue()

# ─── GNANI API ────────────────────────────────────────────────────────────────

def transcribe(audio_path: Path, api_key: str) -> Optional[str]:
    headers = {"X-API-Key-ID": api_key}
    data    = {"language_code": LANGUAGE_CODE, "format": FORMAT}

    try:
        wav_bytes = read_and_convert_to_16k_wav(audio_path)
    except Exception as e:
        print(f"  [AUDIO ERROR] {e}")
        return None

    files = {"audio_file": (audio_path.name, io.BytesIO(wav_bytes), "audio/wav")}
    try:
        resp = requests.post(API_URL, headers=headers, data=data, files=files, timeout=60)
        resp.raise_for_status()
        payload = resp.json()
        if not payload.get("success", True):
            print(f"  [API ERROR] {payload}")
            return None
        return payload.get("transcript", "")
    except requests.exceptions.HTTPError as e:
        print(f"  [HTTP ERROR] {e} | {resp.text[:200]}")
        return None
    except Exception as e:
        print(f"  [ERROR] {e}")
        return None

# ─── EVALUATE ONE VOICE DIRECTORY ────────────────────────────────────────────

def evaluate_voice(
    voice_dir: Path,
    references: list[str],
    api_key: str,
    output_dir: Path,
):
    voice_name = voice_dir.name
    print(f"\n{'='*60}")
    print(f"  Voice Dir : {voice_name}")
    print(f"  Language  : Assamese ({LANGUAGE_CODE})")
    print(f"  Samples   : {len(references)}")
    print(f"{'='*60}")

    # Try multiple naming patterns
    wav_files = sorted(voice_dir.glob("eval_*.wav"))
    if not wav_files:
        wav_files = sorted(voice_dir.glob("assamese_benchmark_*.wav"))
    if not wav_files:
        wav_files = sorted(voice_dir.glob("speech_as-IN_*.wav"))
    if not wav_files:
        wav_files = sorted(voice_dir.glob("*.wav"))

    if not wav_files:
        print(f"  [SKIP] No .wav files found in {voice_dir}")
        return None

    if len(wav_files) != len(references):
        print(f"  [WARN] {len(wav_files)} wav files but {len(references)} references — using min of both")

    n = min(len(wav_files), len(references))

    output_dir.mkdir(parents=True, exist_ok=True)
    csv_path = output_dir / f"{voice_name}_predictions.csv"

    # Checkpoint
    checkpoint_path = output_dir / f"{voice_name}_checkpoint.json"
    completed = {}
    if checkpoint_path.exists():
        with open(checkpoint_path) as f:
            completed = json.load(f)
        print(f"  Resuming — {len(completed)} samples already done")

    csv_exists = csv_path.exists()
    csv_file   = open(csv_path, "a", newline="", encoding="utf-8")
    writer     = csv.DictWriter(csv_file, fieldnames=[
        "sample_id", "filename", "reference", "hypothesis", "wer", "cer", "status"
    ])
    if not csv_exists:
        writer.writeheader()

    wer_scores, cer_scores = [], []
    error_count = 0

    for i in range(n):
        wav_path  = wav_files[i]
        reference = references[i].strip()
        sample_id = wav_path.stem

        if sample_id in completed:
            wer_scores.append(completed[sample_id]["wer"])
            cer_scores.append(completed[sample_id]["cer"])
            continue

        if not reference:
            print(f"  [{i+1:>3}/{n}] SKIPPED (empty reference)")
            continue

        print(f"  [{i+1:>3}/{n}] {wav_path.name} ... ", end="", flush=True)

        hypothesis = transcribe(wav_path, api_key)

        if hypothesis is None:
            print("FAILED")
            error_count += 1
            writer.writerow({
                "sample_id": sample_id, "filename": wav_path.name,
                "reference": reference, "hypothesis": "",
                "wer": "", "cer": "", "status": "error"
            })
        else:
            wer = compute_wer(reference, hypothesis)
            cer = compute_cer(reference, hypothesis)
            wer_scores.append(wer)
            cer_scores.append(cer)
            completed[sample_id] = {"wer": wer, "cer": cer}
            print(f"WER={wer:.3f}  CER={cer:.3f}")
            writer.writerow({
                "sample_id": sample_id, "filename": wav_path.name,
                "reference": reference, "hypothesis": hypothesis,
                "wer": round(wer, 4), "cer": round(cer, 4), "status": "ok"
            })

        csv_file.flush()

        if (i + 1) % 5 == 0:
            with open(checkpoint_path, "w", encoding="utf-8") as f:
                json.dump(completed, f, ensure_ascii=False, indent=2)

        time.sleep(REQUEST_DELAY_SEC)

    csv_file.close()
    with open(checkpoint_path, "w", encoding="utf-8") as f:
        json.dump(completed, f, ensure_ascii=False, indent=2)

    success  = len(wer_scores)
    avg_wer  = sum(wer_scores) / success if success else None
    avg_cer  = sum(cer_scores) / success if success else None

    summary = {
        "voice":         voice_name,
        "language_code": LANGUAGE_CODE,
        "total_samples": n,
        "success":       success,
        "errors":        error_count,
        "avg_wer":       round(avg_wer, 4) if avg_wer is not None else None,
        "avg_cer":       round(avg_cer, 4) if avg_cer is not None else None,
        "timestamp":     datetime.now().isoformat(),
    }

    summary_path = output_dir / f"{voice_name}_summary.json"
    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)

    if avg_wer is not None:
        print(f"\n  [OK] Done  |  Avg WER: {avg_wer:.4f}  |  Avg CER: {avg_cer:.4f}")
    else:
        print(f"\n  [FAIL] No successful transcriptions")
    return summary

# ─── REPORT ──────────────────────────────────────────────────────────────────

def write_report(summaries: list[dict], output_dir: Path):
    report_path = output_dir / "tts_evaluation_report.txt"
    lines = [
        "=" * 70,
        "  TTS Voice Quality Report — Gnani ASR (Prisma v2.5)",
        f"  Language  : Assamese (as-IN)",
        f"  Generated : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "=" * 70,
        "",
        f"  {'Voice':<30} {'Samples':>8} {'Success':>8} {'Errors':>7} {'WER':>8} {'CER':>8}",
        "  " + "-" * 71,
    ]
    for s in summaries:
        wer_str = f"{s['avg_wer']:>8.4f}" if s['avg_wer'] is not None else "     N/A"
        cer_str = f"{s['avg_cer']:>8.4f}" if s['avg_cer'] is not None else "     N/A"
        lines.append(
            f"  {s['voice']:<30} {s['total_samples']:>8} {s['success']:>8} "
            f"{s['errors']:>7} {wer_str} {cer_str}"
        )

    valid = [s for s in summaries if s["avg_wer"] is not None]
    if valid:
        best = min(valid, key=lambda s: s["avg_wer"])
        lines += [
            "",
            f"  Best voice (lowest WER): {best['voice']}  "
            f"(WER={best['avg_wer']:.4f}, CER={best['avg_cer']:.4f})",
        ]

    lines += ["", "=" * 70]
    report = "\n".join(lines)
    print("\n" + report)
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report)
    print(f"\n  Report saved → {report_path}")

# ─── CLI ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Evaluate TTS voice quality via Gnani ASR on Assamese benchmark"
    )
    parser.add_argument(
        "--voice_dirs", nargs="+", required=True,
        help="Paths to TTS voice directories (each containing eval_XX.wav or similar)"
    )
    parser.add_argument(
        "--reference_json", required=True,
        help="Path to Assamese reference JSON file"
    )
    parser.add_argument(
        "--api_key", default=os.environ.get("GNANI_API_KEY"),
        help="Gnani API key (or set GNANI_API_KEY env var)"
    )
    parser.add_argument(
        "--output_dir", default="./assamese_eval_results",
        help="Directory to save results (default: ./assamese_eval_results)"
    )
    args = parser.parse_args()

    if not args.api_key:
        raise ValueError("No API key. Pass --api_key or set GNANI_API_KEY env var.")

    with open(args.reference_json, encoding="utf-8") as f:
        ref_data = json.load(f)
    references = [entry["assamese_sentence"] for entry in ref_data]
    print(f"Loaded {len(references)} reference sentences from {args.reference_json}")

    output_dir = Path(args.output_dir)
    summaries  = []

    for voice_dir in args.voice_dirs:
        summary = evaluate_voice(
            voice_dir  = Path(voice_dir),
            references = references,
            api_key    = args.api_key,
            output_dir = output_dir,
        )
        if summary:
            summaries.append(summary)

    if summaries:
        write_report(summaries, output_dir)

if __name__ == "__main__":
    main()
