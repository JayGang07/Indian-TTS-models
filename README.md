<p align="center">
 <h1 align="center"> Indian TTS Models — Benchmarking Standards</h1>
 <p align="center">
 <strong>Establishing benchmarking standards for Indian Language Speech Models,<br>focusing on Text-to-Speech (TTS) Synthesis</strong>
 
---

## Project Overview

This project benchmarks open-source and API-based **Text-to-Speech (TTS)** models for **Indian languages**, with an initial focus on **Hindi**. The goal is to establish a standardized evaluation framework for comparing Indian language speech synthesis models across key quality dimensions — naturalness, intelligibility, prosody, and voice cloning fidelity.

This work is carried out as part of an internship at **[Kaliber.AI](https://kaliber.ai) / Bay Area Advanced Analytics**.

### Objectives

- Survey and catalog available TTS models supporting Indian languages
- Define a reproducible benchmarking methodology for Indian language TTS
- Compare models across naturalness, intelligibility, accent accuracy, and multi-speaker support
- Produce sample audio outputs for side-by-side subjective evaluation
- Provide ready-to-run notebooks for testing each model on Google Colab

---

## Models Tested

We evaluated **8 TTS models** spanning open-source research models, community models, and commercial API services:

| # | Model | Source | Architecture Type | Year | Parameters | Voice Cloning |
|:-:|-------|--------|-------------------|:----:|:----------:|:-------------:|
| 1 | **XTTS v2** | [Coqui TTS](https://github.com/coqui-ai/TTS) | Auto-regressive Transformer | 2023 | 518M | Yes |
| 2 | **Meta MMS** | [Meta Research](https://huggingface.co/facebook/mms-tts) | VITS-based | 2023 | 300M | No |
| 3 | **Suno Bark** | [Suno AI](https://github.com/suno-ai/bark) | Transformer-based Text-to-Audio | 2023 | 550M | No |
| 4 | **VITS Rasa 13** | [AI4Bharat](https://huggingface.co/ai4bharat/vits_rasa_13) | VITS (Adversarial learning) | 2024 | 40.2M | No |
| 5 | **Indic Parler-TTS** | [AI4Bharat](https://huggingface.co/ai4bharat/indic-parler-tts) | Encoder-Decoder Transformer | 2024 | 938M | No |
| 6 | **Kokoro** | [Kokoro-82M](https://huggingface.co/hexgrad/Kokoro-82M) | StyleTTS-based | 2024 | 82M | No |
| 7 | **Kokoclone** | Community Model | StyleTTS-based | 2025 | 82M | Yes |
| 8 | **Spark-TTS** | [Spark-TTS](https://github.com/QwenLM/Spark-TTS) | Qwen2.5 LLM + BiCodec | 2025 | 500M | Yes |

---

## Training & Evaluation Datasets

The models we evaluated were trained and tested against a variety of large-scale, high-quality speech datasets:

| Dataset | Hours | Languages | Speakers / Accents |
|---------|-------|-----------|--------------------|
| **Rasa** | 400 | 13 | 20 |
| **IndicVoices** | 7,200 | 22 | 16,237 |
| **GLOBE** | 535 | English | 164 global accents |
| **IndicVoices_r** | 1,700 | 22 | 10,496 |
| **IndicTTS** | 40 (20 Native, 20 English) | 13 | - |

---

## Phonetically Balanced Dataset Breakdown

### What is a Phonetically Balanced Dataset?
A **phonetically balanced dataset** is a collection of text or audio data that contains all the distinct sounds (phonemes) of a language in the same proportion that they naturally occur in everyday conversation. Rather than just using random sentences, these datasets are carefully constructed to ensure TTS models learn how to pronounce both common sounds and rare edge-case letters accurately.

**Example:** Instead of a simple sentence like "Hello, my name is Jay," a phonetically dense Hindi sentence might be deliberately written to include loan words, nasal sounds, and aspirated consonants (e.g., "ज़ुबैर ने फ़र्ज़ निभाते हुए क़िले के पास से गुज़रते हुए एक ख़त पढ़ा।") to force the model to render rare phonemes like 'ज़', 'फ़', 'क़', and 'ख़'.

To rigorously test the intelligibility and pronunciation of each model, we generated a **Custom Phonetically Balanced Hindi Dataset** (`datasets/hindi_evaluation_set.json`). This dataset targets challenging Indian language phonemes, including Velars, Gutturals, Retroflexes, Palatals, and Nasals.

### Hindi Phoneme Frequencies
- Phoneme अ (Schwa): 250
- Phoneme ् (Vowel Length Modifier): 170
- Phoneme क्: 90
- Phoneme र्: 86
- Phoneme आ: 84
- Phoneme ए: 75
- Phoneme इ / ई: 67
- Phoneme त्: 57
- Phoneme न्: 51
- Phoneme म्: 47
- Phoneme श्: 36
- Phoneme द्: 34
- Phoneme उ / ऊ: 32
- Phoneme ल्: 30
- Phoneme ् (Aspiration Modifier / महाप्राण): 30
- Phoneme ह् (Voiced): 28
- Phoneme प्: 27
- Phoneme स्: 27
- Phoneme ऑ (English Loan): 24
- Phoneme य्: 24
- Phoneme ग्: 23
- Phoneme ट्: 21
- Phoneme ब्: 19
- Phoneme व्: 19
- Phoneme झ़् (Nukta/Loan): 17
- Phoneme ओ: 15
- Phoneme ड़् (Flap): 12
- Phoneme ऐ: 11
- Phoneme ड्: 7
- Phoneme ज़् (Nukta): 7
- Phoneme फ़् (Nukta): 6
- Phoneme आँ (Nasalized): 6
- Phoneme ञ्: 5
- Phoneme ष्: 3
- Phoneme ण्: 3
- Phoneme ङ्: 3
- Phoneme क़् (Nukta): 3
- Phoneme ऊँ (Nasalized): 3
- Phoneme ख़् (Nukta): 2
- Phoneme ह्: 2
- Phoneme ग़् (Nukta): 1

### Summary of Dataset Design

**1. The Natural Dominance of the Schwa (अ)**
The phoneme 'अ' (schwa) is the absolute backbone of the Hindi language. Every standard consonant in Devanagari inherently carries a schwa unless heavily modified. If a dataset forced an artificially low number of 'अ' sounds just to match rare consonants, the sentences would sound robotic, entirely unnatural, and grammatically impossible.

**2. Representative Vowel Lengths (Long Vowels / मात्राएँ)**
The high frequency of long vowel modifiers (170 occurrences) represents vowel lengthening (like आ, ई, ऊ, ए). Hindi is a syllable-timed language where vowel length changes the entire meaning of a word (e.g., kam vs. kaam). A high number of length modifiers ensures the model gets enough sustained vowel data to learn proper pitch and tone.

**3. Inclusion of the "Long Tail" (The Rare Sounds)**
This is where the true "balance" of this dataset shines. In a random selection of 20 conversational Hindi sentences, you would likely find zero instances of sounds like 'क़', 'ख़', 'ग़', or the aspirated flap 'ढ़'.
By deliberately writing sentences like the loan_words_nukta and perso_arabic_nukta ones, the dataset forces these rare edge cases to appear:
- 'ज़' (7 times)
- 'फ़' (6 times)
- 'क़' (3 times)
- 'ख़' (2 times)
- 'ग़' (1 time)

Even though they only appear a few times, their guaranteed presence means an acoustic model is forced to process them, preventing the system from collapsing them into standard sounds (like turning 'ज़' into 'ज' or 'फ़' into 'फ').

**4. Broad Consonant Class Coverage**
If you group the mid-frequency numbers, you can see the articulatory balancing act at play:
- Velars/Throat: 'क' (90), 'ग' (23)
- Dentals/Alveolars: 'त' (57), 'द' (34), 'न' (51)
- Labials/Lips: 'प' (27), 'ब' (19), 'म' (47)
- Retroflexes (Curled Tongue): 'ट' (21), 'ड' (7), 'ड़' (12)

---

## Evaluation Metrics

To thoroughly compare these models, we relied on a combination of human-centric and automated evaluation metrics:

### Subjective Metrics (Human Evaluation)
- **MOS (Mean Opinion Score):** Rates the overall naturalness and quality of the generated speech on a 1-5 scale.
- **Comparative MOS (CMOS):** Directly compares two audio samples side-by-side to determine which sounds better.
- **ABX Testing:** A listener is presented with two samples (A and B) and must identify which one matches a reference sample (X) most closely, heavily used for testing voice cloning fidelity.

### Objective Metrics (Automated Evaluation)
- **WER (Word Error Rate):** Measures how many words were transcribed incorrectly.
- **CER (Character Error Rate):** Measures character-level spelling and phonetic mistakes.
- **STOI (Short-Time Objective Intelligibility):** Computes the intelligibility of synthesized speech based on acoustic features.
- **PESQ (Perceptual Evaluation of Speech Quality):** An objective method for predicting subjective quality scores of speech.

---

## Quantitative Evaluation Results

We processed the generated audio through an automated **Whisper ASR pipeline** to compute the Word Error Rate (WER) and Character Error Rate (CER).

### Model Leaderboard (Hindi Phonetics)

| Rank | Model | Word Error Rate (WER) | Character Error Rate (CER) |
|:----:|-------|:---------------------:|:--------------------------:|
| 1 | **Kokoro** | **0.359** | **0.129** |
| 2 | **XTTS v2** | 0.525 | 0.217 |
| 3 | **Meta MMS** | 0.566 | 0.209 |
| 4 | **VITS Rasa 13** | 0.573 | 0.232 |
| 5 | **Suno Bark** | 0.616 | 0.292 |
| 6 | **Indic Parler-TTS** | 0.892 | 0.645 |

*(Note: Lower is better. TTSMaker was excluded from bulk automated evaluation due to API constraints.)*

---

## Evaluation Pipeline Architecture

```mermaid
graph TD
 A[Phonetically Balanced Text Dataset] --> B(TTS Model Inference)
 B --> C[Generated Audio .wav]
 C --> D(Whisper ASR Transcription)
 D --> E{Error Calculation}
 E --> F[Word Error Rate]
 E --> G[Character Error Rate]
```

### Whisper ASR Transcription Engine

The pipeline utilizes OpenAI's Whisper model for robust ASR transcription. Whisper is available in multiple model sizes depending on the hardware and accuracy requirements:

1. **Tiny (39M parameters)**: The fastest and most lightweight model. Excellent for fast note-taking or low-power devices, but prone to higher error rates on complex audio.
2. **Base (74M parameters)**: A great balance of speed and size. Requires very little memory and transcribes quickly on almost any hardware.
3. **Small (244M parameters)**: Highly recommended for a mix of good transcription accuracy and reasonable processing time on modern computers.
4. **Medium (769M parameters)**: Offers high accuracy and handles background noise well, but requires a dedicated GPU or more powerful processors to run smoothly.
5. **Large (1.55B parameters)**: The most accurate and robust model, perfect for professional transcriptions. It features three iterations:
   - **large-v1 & large-v2**: Previous iterations of the large model.
   - **large-v3**: The latest standard large release, trained on more diverse datasets for superior multilingual accuracy.

#### Whisper Models Hardware & Performance Breakdown

| Model | Params | English-Only | VRAM (GPU) | GGML Disk | RAM (whisper.cpp) | Speed | English WER | Multilingual WER |
|---|---|---|---|---|---|---|---|---|
| **tiny** | 39 M | `tiny.en` | ~1 GB | 75 MiB | ~273 MB | ~10x | ~7.6% | ~12% |
| **base** | 74 M | `base.en` | ~1 GB | 142 MiB | ~388 MB | ~7x | ~5.0% | ~10% |
| **small** | 244 M | `small.en` | ~2 GB | 466 MiB | ~852 MB | ~4x | ~3.4% | ~7% |
| **medium** | 769 M | `medium.en` | ~5 GB | 1.5 GiB | ~2.1 GB | ~2x | ~2.9% | ~5% |
| **large-v2** | 1,550 M | N/A | ~10 GB | 2.9 GiB | ~3.9 GB | 1x | ~2.7% | ~4% |
| **large-v3** | 1,550 M | N/A | ~10 GB | 2.9 GiB | ~3.9 GB | 1x | ~2.4% | ~3.5% |


### Understanding Error Metrics (WER & CER)

#### Word Error Rate (WER)
When WER is calculated, the errors are further broken down into:
1. **Substitutions (S)**: The TTS engine mispronounces a word, causing the ASR to hear a completely different word (e.g., saying “cataracts” instead of “Cadillac”).
2. **Deletions (D)**: The TTS cuts off early or skips a word completely.
3. **Insertions (I)**: The TTS model hallucinates or adds extra words, filler syllables, or stammers.

$$WER = \frac{S + I + D}{N} \times 100$$

> **Note:** In modern TTS development, a low WER indicates the audio is highly intelligible. However, WER does not measure voice naturalness, emotion, or prosody—a robotic-sounding voice can still be highly intelligible with a 0% WER.

#### Character Error Rate (CER)
The CER formula is a metric used to evaluate the accuracy of AI text models, speech-to-text, and OCR software by measuring character-level differences.

$$CER = \frac{S + D + I}{N}$$

**Where:**
- **S** = Substitutions (wrong characters in place of correct ones)
- **D** = Deletions (characters missing from the AI output)
- **I** = Insertions (extra characters incorrectly added to the output)
- **N** = Total number of characters in the original, correct reference text

**How to Calculate It:**
1. Align the AI's output with the correct, human-verified reference text.
2. Count the minimum number of single-character edits (S + D + I) needed to change the output into the reference text.
3. Divide this sum by the total length of the reference text (N).
4. Multiply by 100 to get a percentage.

---

## Detailed Model Breakdowns

### 1. Kokoro (82M)
- **Architecture:** Lightweight TTS model based on StyleTTS architecture (82 million parameters).
- **Key Feature:** Extremely fast generation, high quality, and supports multiple voices natively.
- **Results:** Achieved the absolute best performance on our phonetically balanced Hindi tests with a WER of 0.359.
- **Workspace:** [`models/kokoro/`](models/kokoro/)

### 2. XTTS v2 (Coqui TTS)
- **Architecture:** Auto-regressive transformer-based TTS with voice cloning.
- **Key Feature:** Zero-shot voice cloning from a short audio reference (~6 seconds).
- **Results:** Extremely natural voice cloning capabilities, ranking second in overall intelligibility.
- **Workspace:** [`models/voice_cloning/xtts-v2/`](models/voice_cloning/xtts-v2/)

### 3. Meta MMS (Massively Multilingual Speech)
- **Architecture:** VITS-based model trained on 1,100+ languages.
- **Key Feature:** Broadest language coverage of any TTS model.
- **Results:** Consistent performance across diverse phonemes, slightly edging out VITS Rasa.
- **Workspace:** [`models/meta-mms/`](models/meta-mms/)

### 4. VITS Rasa 13 (AI4Bharat)
- **Architecture:** VITS (Variational Inference with adversarial learning for end-to-end TTS).
- **Key Feature:** Native support for 13 Indian languages with multiple speaker IDs & emotion styles.
- **Workspace:** [`models/vits-rasa/`](models/vits-rasa/)

### 5. Indic Parler-TTS (AI4Bharat)
- **Architecture:** Encoder-decoder transformer with DAC audio codec.
- **Key Feature:** Natural language voice description prompting (e.g., "A female speaker with a calm voice").
- **Workspace:** [`models/indic-parler/`](models/indic-parler/)

### 6. Suno Bark
- **Architecture:** Transformer-based text-to-audio model (1.2B parameters).
- **Key Feature:** Can generate speech, music, and sound effects; supports multilingual synthesis.
- **Workspace:** [`models/suno-bark/`](models/suno-bark/)

### 7. KokoClone (Kokoro + Voice Cloning)
- **Architecture:** Kokoro-82M extended with voice cloning capabilities using speaker embeddings.
- **Key Feature:** Combines Kokoro's fast, high-quality synthesis with zero-shot voice cloning.
- **Indian Language Support:** Hindi (via `lang_code='h'`).
- **Workspace:** [`models/voice_cloning/kokoclone/`](models/voice_cloning/kokoclone/)

### 8. Spark-TTS
- **Architecture:** Qwen2.5 LLM + BiCodec-based TTS with voice cloning via audio prompts (~1.1B parameters).
- **Key Feature:** High-fidelity voice cloning and controllable speech generation with natural prosody.
- **Indian Language Support:** Hindi (via multi-lingual capability).
- **Workspace:** [`models/voice_cloning/spark-tts/`](models/voice_cloning/spark-tts/)


## Repository Structure

The repository is organized functionally by **model**:

```text
Indian-TTS-models/
├── README.md                          # This presentation document
├── requirements.txt                   # Python dependencies
├── .gitignore                         # Git ignore rules
│
├── datasets/                          # Large testing datasets
│   ├── dataset_48.5_41.5.zip
│   └── hindi_evaluation_set.json      # Custom phonetically balanced Hindi dataset
│
├── docs/                              # Project-level documentation
│   └── Indian_TTS_Models_Overview.xlsx
│
├── models/                            # The Core Model Workspaces
│   ├── indic-parler/
│   │   ├── notebooks/                 # indic_parler_tts.ipynb, indic_parler_phonetic_eval.ipynb
│   │   ├── samples/                   # Male & female Hindi audio samples
│   │   └── phonetic_evaluation/       # Whisper ASR evaluation CSV + audio ZIP
│   │
│   ├── kokoro/
│   │   ├── notebooks/                 # kokoro.ipynb
│   │   ├── samples/                   # Male & female Hindi audio samples
│   │   ├── phonetic_evaluation/       # Phonetic + IndicVoices evaluation results
│   │   └── assets/                    # Visual dashboards (PNG)
│   │
│   ├── meta-mms/
│   │   ├── notebooks/                 # Meta_MMS.ipynb, mms_phonetic_eval.ipynb
│   │   ├── samples/                   # Hindi audio sample
│   │   └── phonetic_evaluation/       # Phonetic + IndicVoices evaluation results
│   │
│   ├── suno-bark/
│   │   ├── notebooks/                 # suno_bark_phonetic_eval.ipynb
│   │   ├── samples/                   # Male & female Hindi audio samples
│   │   └── phonetic_evaluation/       # Whisper ASR evaluation CSV + audio ZIP
│   │
│   ├── tts-maker/
│   │   └── samples/                   # Male & female Hindi audio samples (MP3)
│   │
│   ├── vits-rasa/
│   │   ├── notebooks/                 # vits_rasa_13.ipynb, vits_rasa_phonetic_eval.ipynb
│   │   ├── samples/                   # Male & female Hindi audio samples
│   │   └── phonetic_evaluation/       # Phonetic + IndicVoices evaluation results
│   │
│   └── voice_cloning/                 # Voice Cloning Models
│       ├── xtts-v2/
│       │   ├── notebooks/             # xtts.ipynb, xtts_v2.ipynb, xtts_phonetic_eval.ipynb
│       │   ├── samples/               # Hindi audio samples
│       │   └── phonetic_evaluation/   # Whisper ASR evaluation CSV + audio ZIP
│       │
│       ├── kokoclone/
│       │   ├── notebooks/             # kokoclone.ipynb
│       │   └── outputs/               # Evaluation output ZIP
│       │
│       └── spark-tts/
│           ├── notebooks/             # spark_tts.ipynb
│           └── outputs/               # TTS output ZIP
│
└── utility_notebooks/                 # Bulk testing and evaluation scripts
    ├── Evaluating_TTS_models.ipynb
    ├── Testing_Indian_TTS_models.ipynb
    └── VITS_rasa_finetune.ipynb       # Cross-model evaluation (VITS Rasa + Kokoro)
```

---

## Getting Started

### Prerequisites
- Python 3.10+
- Google Colab (recommended for GPU access) or a local machine with NVIDIA GPU.
- Hugging Face account with API token (for gated models like Parler).

### Installation
```bash
# Clone the repository
git clone https://github.com/JayGang07/Indian-TTS-models.git
cd Indian-TTS-models

# Install dependencies
pip install -r requirements.txt
```

### Running on Google Colab
Navigate to any model's `notebooks/` directory and open the `.ipynb` file.

> **⚠ Important:** Some models (Indic Parler-TTS, XTTS v2, Suno Bark) require a **GPU runtime**. 
> In Colab: `Runtime → Change runtime type → T4 GPU`

### Hugging Face Authentication
For models hosted on Hugging Face, authenticate using:
```python
from huggingface_hub import login
login(token="your_hf_token_here")
```

---

## Acknowledgements

This project is part of an internship at **[Kaliber.AI](https://kaliber.ai) / Bay Area Advanced Analytics**.

- [AI4Bharat](https://ai4bharat.org/) for Indic Parler-TTS and VITS Rasa models
- [Hugging Face](https://huggingface.co/) for model hosting and the Transformers library
- [Meta Research](https://ai.meta.com/) for MMS
- [Suno AI](https://www.suno.ai/) for Bark
- [Hexgrad](https://huggingface.co/hexgrad) for the amazing Kokoro-82M model

---

## References

- [Whisper Speech Recognition Model Capable of Recognizing 99 Languages](https://medium.com/axinc-ai/whisper-speech-recognition-model-capable-of-recognizing-99-languages-5b5cf0197c16)
- [Arxiv Paper 2501.00425](https://arxiv.org/abs/2501.00425)
- [Whisper Model Sizes Explained](https://openwhispr.com/blog/whisper-model-sizes-explained)
- [Whisper Models Directory](https://whisper-api.com/blog/models/)
- [Springer Link Reference](https://link.springer.com/chapter/10.1007/978-981-96-6960-8_6)
