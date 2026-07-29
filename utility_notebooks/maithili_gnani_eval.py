"""
TTS Voice Quality Evaluation via Gnani ASR — Maithili
Transcribes audio from TTS voice ZIP archives using Gnani Prisma v2.5,
then computes WER & CER against Maithili reference sentences.

Evaluates 3 models:
  1. Meta MMS (VITS) — vits_maithili_audio.zip
  2. Indic Parler-TTS — indic_parler_maithili_audio.zip
  3. Syspin VITS — syspin_maithili_audio.zip

Uses soundfile + numpy for robust audio format handling (supports IEEE float WAV).
"""
import io
import os
import json
import csv
import time
import wave
import struct
import sys
import zipfile
import tempfile
import shutil
import requests
import numpy as np
import soundfile as sf
import editdistance
from pathlib import Path
from datetime import datetime
from typing import Optional

sys.stdout.reconfigure(encoding='utf-8')

# ─── CONFIG ──────────────────────────────────────────────────────────────────

API_URL           = "https://api.vachana.ai/stt/v3"
API_KEY           = os.environ.get("GNANI_API_KEY", "")
LANGUAGE_CODE     = "hi-IN"  # Gnani does not support mai-IN; using hi-IN (Hindi) as Maithili uses Devanagari
FORMAT            = "transcribe"
REQUEST_DELAY_SEC = 1.5

# Paths
REPO_ROOT = Path(r"c:\Users\jayku\Downloads\Kaliber.AI\Indian-TTS-models")
DATASET_PATH = REPO_ROOT / "datasets" / "maithili_balanced_set.json"

MODELS = [
    {
        "name": "Meta MMS (VITS)",
        "zip_path": REPO_ROOT / "models" / "meta-mms" / "phonetic_evaluation" / "vits_maithili_audio.zip",
        "file_pattern": "vits_sent_",
    },
    {
        "name": "Indic Parler-TTS",
        "zip_path": REPO_ROOT / "models" / "indic-parler" / "phonetic_evaluation" / "indic_parler_maithili_audio.zip",
        "file_pattern": "parler_sent_",
    },
    {
        "name": "Syspin VITS",
        "zip_path": REPO_ROOT / "models" / "syspin" / "phonetic_evaluation" / "syspin_maithili_audio.zip",
        "file_pattern": "syspin_sent_",
    },
]

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

def transcribe(audio_path: Path) -> Optional[str]:
    headers = {"X-API-Key-ID": API_KEY}
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
        print(f"  [HTTP ERROR] {e} | {resp.text[:300]}")
        return None
    except Exception as e:
        print(f"  [ERROR] {e}")
        return None

# ─── EVALUATE ONE MODEL ─────────────────────────────────────────────────────

def evaluate_model(model_info: dict, references: list[str]) -> dict:
    name = model_info["name"]
    zip_path = model_info["zip_path"]
    file_pattern = model_info["file_pattern"]

    print(f"\n{'='*60}")
    print(f"  Model   : {name}")
    print(f"  ZIP     : {zip_path.name}")
    print(f"  Language : Maithili ({LANGUAGE_CODE})")
    print(f"  Samples : {len(references)}")
    print(f"{'='*60}")

    # Extract zip to temp directory
    tmp_dir = Path(tempfile.mkdtemp())
    try:
        with zipfile.ZipFile(zip_path) as z:
            z.extractall(tmp_dir)

        # Find audio files in sorted order
        wav_files = sorted(tmp_dir.glob(f"{file_pattern}*.wav"),
                          key=lambda p: int(''.join(filter(str.isdigit, p.stem)) or 0))

        if not wav_files:
            # Try any .wav files
            wav_files = sorted(tmp_dir.glob("*.wav"),
                              key=lambda p: int(''.join(filter(str.isdigit, p.stem)) or 0))

        if not wav_files:
            print(f"  [SKIP] No .wav files found")
            return None

        print(f"  Found {len(wav_files)} audio files")

        n = min(len(wav_files), len(references))
        wer_scores, cer_scores = [], []
        error_count = 0

        for i in range(n):
            wav_path = wav_files[i]
            reference = references[i].strip()

            if not reference:
                print(f"  [{i+1:>3}/{n}] SKIPPED (empty reference)")
                continue

            print(f"  [{i+1:>3}/{n}] {wav_path.name} ... ", end="", flush=True)

            hypothesis = transcribe(wav_path)

            if hypothesis is None:
                print("FAILED")
                error_count += 1
            else:
                w = compute_wer(reference, hypothesis)
                c = compute_cer(reference, hypothesis)
                wer_scores.append(w)
                cer_scores.append(c)
                print(f"WER={w:.3f}  CER={c:.3f}")

            time.sleep(REQUEST_DELAY_SEC)

        success = len(wer_scores)
        avg_wer = sum(wer_scores) / success if success else None
        avg_cer = sum(cer_scores) / success if success else None

        summary = {
            "model": name,
            "language_code": LANGUAGE_CODE,
            "total_samples": n,
            "success": success,
            "errors": error_count,
            "avg_wer": round(avg_wer, 4) if avg_wer is not None else None,
            "avg_cer": round(avg_cer, 4) if avg_cer is not None else None,
            "timestamp": datetime.now().isoformat(),
        }

        if avg_wer is not None:
            print(f"\n  [OK] Done  |  Avg WER: {avg_wer:.4f}  |  Avg CER: {avg_cer:.4f}")
        else:
            print(f"\n  [FAIL] No successful transcriptions")

        return summary

    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)

# ─── MAIN ────────────────────────────────────────────────────────────────────

def main():
    print("=" * 60)
    print("  Maithili TTS Evaluation — Gnani ASR (Prisma v2.5)")
    print(f"  Dataset  : {DATASET_PATH.name}")
    print(f"  Language : {LANGUAGE_CODE}")
    print("=" * 60)

    # Load reference sentences
    with open(DATASET_PATH, encoding='utf-8') as f:
        raw_data = json.load(f)

    if isinstance(raw_data, dict):
        for key, value in raw_data.items():
            if isinstance(value, list):
                raw_data = value
                break

    references = []
    for item in raw_data:
        if isinstance(item, dict):
            for k in ['sentence', 'text', 'transcript']:
                if k in item:
                    references.append(str(item[k]))
                    break
        elif isinstance(item, str):
            references.append(item)

    print(f"Loaded {len(references)} reference sentences\n")

    summaries = []
    for model_info in MODELS:
        summary = evaluate_model(model_info, references)
        if summary:
            summaries.append(summary)

    # ── FINAL REPORT ──
    print("\n" + "=" * 70)
    print("  MAITHILI TTS EVALUATION REPORT — Gnani ASR (Prisma v2.5)")
    print(f"  Generated : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)
    print(f"\n  {'Model':<25} {'Samples':>8} {'WER':>10} {'CER':>10}")
    print("  " + "-" * 55)
    for s in summaries:
        wer_str = f"{s['avg_wer']:>10.4f}" if s['avg_wer'] is not None else "       N/A"
        cer_str = f"{s['avg_cer']:>10.4f}" if s['avg_cer'] is not None else "       N/A"
        print(f"  {s['model']:<25} {s['success']:>8} {wer_str} {cer_str}")

    # Save results JSON
    output_path = REPO_ROOT / "utility_notebooks" / "maithili_gnani_eval_results.json"
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(summaries, f, ensure_ascii=False, indent=2)
    print(f"\n  Results saved → {output_path}")

    print("\n" + "=" * 70)

if __name__ == "__main__":
    main()
