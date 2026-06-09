<p align="center">
  <h1 align="center">🗣️ Indian TTS Models — Benchmarking Standards</h1>
  <p align="center">
    <strong>Establishing benchmarking standards for Indian Language Speech Models,<br>focusing on Text-to-Speech (TTS) Synthesis</strong>
  </p>
  <p align="center">
    <a href="#models-tested">Models Tested</a> •
    <a href="#benchmarking-criteria">Benchmarking Criteria</a> •
    <a href="#results">Results</a> •
    <a href="#getting-started">Getting Started</a> •
    <a href="#repository-structure">Repository Structure</a>
  </p>
</p>

---

## 📋 Project Overview

This project benchmarks open-source and API-based **Text-to-Speech (TTS)** models for **Indian languages**, with an initial focus on **Hindi**. The goal is to establish a standardized evaluation framework for comparing Indian language speech synthesis models across key quality dimensions — naturalness, intelligibility, prosody, and voice cloning fidelity.

This work is carried out as part of an internship at **[Kaliber.AI](https://kaliber.ai) / Bay Area Advanced Analytics**.

### 🎯 Objectives

- Survey and catalog available TTS models supporting Indian languages
- Define a reproducible benchmarking methodology for Indian language TTS
- Compare models across naturalness, intelligibility, accent accuracy, and multi-speaker support
- Produce sample audio outputs for side-by-side subjective evaluation
- Provide ready-to-run notebooks for testing each model on Google Colab

---

## 🧠 Models Tested

We evaluated **7 TTS models** spanning open-source research models, community models, and commercial API services:

| # | Model | Source | Type | Languages | Voice Cloning |
|:-:|-------|--------|------|-----------|:-------------:|
| 1 | **XTTS v2** | [Coqui TTS](https://github.com/coqui-ai/TTS) | Open-source | Multi-lingual (incl. Hindi) | ✅ |
| 2 | **Meta MMS** | [Meta Research](https://huggingface.co/facebook/mms-tts) | Open-source | 1,100+ languages | ❌ |
| 3 | **VITS Rasa 13** | [AI4Bharat](https://huggingface.co/ai4bharat/vits_rasa_13) | Open-source | 13 Indian languages | ❌ |
| 4 | **Indic Parler-TTS** | [AI4Bharat](https://huggingface.co/ai4bharat/indic-parler-tts) | Open-source | Indian languages | ❌ |
| 5 | **Kokoro** | [Kokoro-82M](https://huggingface.co/hexgrad/Kokoro-82M) | Open-source | Multi-lingual (incl. Hindi) | ❌ |
| 6 | **Suno Bark** | [Suno AI](https://github.com/suno-ai/bark) | Open-source | Multi-lingual | ✅ |

---

## 📊 Benchmarking Criteria

Each model is evaluated against the following criteria:

### Quantitative Metrics *(planned)*
| Metric | Description |
|--------|-------------|
| **MOS (Mean Opinion Score)** | Subjective 1-5 scale rating of naturalness |
| **Intelligibility** | Word-level accuracy via ASR round-trip evaluation |
| **Inference Latency** | Time to generate speech (seconds/utterance) |
| **RTF (Real-Time Factor)** | Processing time relative to audio duration |

### Qualitative Assessment
| Dimension | What We Evaluate |
|-----------|------------------|
| **Naturalness** | Does the speech sound human-like? |
| **Prosody** | Are stress, intonation, and rhythm appropriate? |
| **Accent Fidelity** | Does the model sound like a native speaker? |
| **Multi-Speaker** | Are male/female voices distinguishable and natural? |
| **Code-Mixing** | How well does it handle Hindi-English mixed text? |
| **Voice Cloning** | Can it replicate a target speaker's voice? |

---

## 📈 Evaluation Results

We evaluated the top performing models (VITS Rasa 13, Meta MMS, and Kokoro) against the **AI4Bharat IndicVoices-R** dataset. Detailed results and scoring can be found in our comprehensive spreadsheet and CSV files:
- [`docs/Indian_TTS_Models_Overview.xlsx`](docs/Indian_TTS_Models_Overview.xlsx)
- [`docs/IndicVoices_VITS_Evaluation.csv`](docs/IndicVoices_VITS_Evaluation.csv)
- [`docs/Kokoro_Evaluation_Results.csv`](docs/Kokoro_Evaluation_Results.csv)

The [`notebooks/Evaluating_TTS_models.ipynb`](notebooks/Evaluating_TTS_models.ipynb) notebook contains the full pipeline used to process and score these datasets automatically. Note that commercial freemium APIs (such as TTSMaker) were excluded from bulk evaluation due to API cost limits.

---

## 🔍 Model Details

### 1. XTTS v2 (Coqui TTS)
- **Architecture:** Auto-regressive transformer-based TTS with voice cloning
- **Key Feature:** Zero-shot voice cloning from a short audio reference (~6 seconds)
- **Indian Language Support:** Hindi (with cross-lingual transfer)
- **Hardware:** Requires GPU (T4 or better recommended)
- **Notebook:** [`notebooks/xtts_v2.ipynb`](notebooks/xtts_v2.ipynb)

<details>
<summary>📝 Code Example</summary>

```python
import torch
import os
from TTS.api import TTS

os.environ["COQUI_TOS_AGREED"] = "1"
device = "cuda" if torch.cuda.is_available() else "cpu"

tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)

tts.tts_to_file(
    text="हैलो, मेरा नाम जय है।",
    speaker_wav="reference_audio.wav",
    language="hi",
    file_path="xtts_output.wav"
)
```
</details>

### 2. Meta MMS (Massively Multilingual Speech)
- **Architecture:** VITS-based model trained on 1,100+ languages
- **Key Feature:** Broadest language coverage of any TTS model
- **Indian Language Support:** Hindi, Tamil, Bengali, Telugu, Marathi, and many more
- **Hardware:** Can run on CPU
- **Notebook:** [`notebooks/meta_mms.ipynb`](notebooks/meta_mms.ipynb)

### 3. VITS Rasa 13 (AI4Bharat)
- **Architecture:** VITS (Variational Inference with adversarial learning for end-to-end TTS)
- **Key Feature:** Native support for 13 Indian languages with multiple speaker IDs & emotion styles
- **Indian Language Support:** Hindi, Bengali, Tamil, Telugu, Kannada, Malayalam, Marathi, Gujarati, Assamese, Odia, Punjabi, Manipuri, Bodo
- **Hardware:** Can run on CPU (fast inference)
- **Model ID:** `ai4bharat/vits_rasa_13`
- **Notebook:** [`notebooks/vits_rasa_13.ipynb`](notebooks/vits_rasa_13.ipynb)

<details>
<summary>📝 Code Example</summary>

```python
import torch
from transformers import AutoModel, AutoTokenizer

device = "cuda" if torch.cuda.is_available() else "cpu"

model_id = "ai4bharat/vits_rasa_13"
tokenizer = AutoTokenizer.from_pretrained(model_id, trust_remote_code=True)
model = AutoModel.from_pretrained(model_id, trust_remote_code=True).to(device)

text = "हैलो, मेरा नाम जय है।"
inputs = tokenizer(text, return_tensors="pt").to(device)

with torch.no_grad():
    output = model(
        inputs['input_ids'],
        speaker_id=0,   # 0 for Female, 1 for Male, etc.
        emotion_id=0     # 0 for ALEXA, 1 for ANGER, etc.
    )

audio = output.waveform.cpu().numpy().squeeze()
```
</details>

### 4. Indic Parler-TTS (AI4Bharat)
- **Architecture:** Encoder-decoder transformer with DAC audio codec
- **Key Feature:** Natural language voice description (e.g., "A female speaker with a calm voice in a quiet room")
- **Indian Language Support:** Multiple Indian languages (Hindi tested)
- **Hardware:** GPU recommended (T4 or better), ~3.5 GB VRAM
- **Model ID:** `ai4bharat/indic-parler-tts`
- **Notebook:** [`notebooks/indic_parler_tts.ipynb`](notebooks/indic_parler_tts.ipynb)

<details>
<summary>📝 Code Example</summary>

```python
import torch
from parler_tts import ParlerTTSForConditionalGeneration
from transformers import AutoTokenizer
import soundfile as sf

device = "cuda" if torch.cuda.is_available() else "cpu"

# Load model & SEPARATE tokenizers for description and text
parler_id = "ai4bharat/indic-parler-tts"
text_tokenizer = AutoTokenizer.from_pretrained(parler_id, use_fast=False)
desc_tokenizer = AutoTokenizer.from_pretrained("google/flan-t5-large")
model = ParlerTTSForConditionalGeneration.from_pretrained(parler_id).to(device)

# Inputs
text = "हैलो, मेरा नाम जय है।"
description = "A male speaker with a clear, natural voice talking at a calm, steady pace in a quiet room."

# IMPORTANT: Description → input_ids, Text → prompt_input_ids
desc_tokens = desc_tokenizer(description, return_tensors="pt")
text_tokens = text_tokenizer(text, return_tensors="pt")

with torch.no_grad():
    generation = model.generate(
        input_ids=desc_tokens.input_ids.to(device),
        attention_mask=desc_tokens.attention_mask.to(device),
        prompt_input_ids=text_tokens.input_ids.to(device),
        prompt_attention_mask=text_tokens.attention_mask.to(device),
    )

audio = generation.cpu().numpy().squeeze()
sf.write("output.wav", audio, model.config.sampling_rate)
```
</details>

### 5. Kokoro (82M)
- **Architecture:** Lightweight TTS model based on StyleTTS architecture (82 million parameters)
- **Key Feature:** Extremely fast generation, high quality, and supports multiple voices and languages natively
- **Indian Language Support:** Hindi (via `lang_code='h'`)
- **Hardware:** Can run efficiently on CPU, blazingly fast on GPU
- **Notebook / Script:** Evaluated in [`notebooks/VITS_rasa_finetune.ipynb`](notebooks/VITS_rasa_finetune.ipynb)
- **Samples:** [`samples/kokoro/`](samples/kokoro/)

<details>
<summary>📝 Code Example</summary>

```python
import numpy as np
import soundfile as sf
from kokoro import KPipeline

pipeline = KPipeline(lang_code='h') # 'h' for Hindi
prompt_text = "हैलो, मेरा नाम जय है।"
voice_id = "hm_omega" # Male voice

generator = pipeline(prompt_text, voice=voice_id, speed=1.0)
audio_pieces = [audio for _, _, audio in generator]

if audio_pieces:
    final_audio = np.concatenate(audio_pieces)
    sf.write("kokoro_output.wav", final_audio, 24000)
```
</details>

### 6. Suno Bark
- **Architecture:** Transformer-based text-to-audio model
- **Key Feature:** Can generate speech, music, and sound effects; supports multilingual synthesis
- **Indian Language Support:** Hindi (via multilingual capability)
- **Hardware:** GPU recommended (T4 or better)
- **Notebook:** [`notebooks/suno_bark.ipynb`](notebooks/suno_bark.ipynb)

---

## 🎧 Sample Audio Outputs

All generated audio samples are stored in the [`samples/`](samples/) directory, organized by model:

```
samples/
├── indic-parler/
│   ├── indic_parler_female.wav
│   └── indic_parler_male.wav
├── vits-rasa/
│   ├── vits_rasa_female.wav
│   └── vits_rasa_male.wav
├── suno-bark/
│   ├── bark_hindi_female.wav
│   └── bark_hindi_male.wav
├── kokoro/
│   ├── kokoro_female.wav
│   └── kokoro_male.wav
├── xtts-v2/
│   └── xtts_v2_male_hindi.wav
├── meta-mms/
│   └── mms_male_hindi.wav
```

**Test Sentence (Hindi):**
> हैलो, मेरा नाम जय है।  
> *(Hello, my name is Jay.)*

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- Google Colab (recommended for GPU access) or a local machine with NVIDIA GPU
- Hugging Face account with API token (for gated models)

### Installation

```bash
# Clone the repository
git clone https://github.com/JayGang07/Indian-TTS-models.git
cd Indian-TTS-models

# Install dependencies
pip install -r requirements.txt
```

### Running on Google Colab

Each model has a dedicated notebook in the [`notebooks/`](notebooks/) directory. Click the "Open in Colab" badge at the top of each notebook to run directly.

> **⚠️ Important:** Some models (Indic Parler-TTS, XTTS v2, Suno Bark) require a **GPU runtime**.  
> In Colab: `Runtime → Change runtime type → T4 GPU`

### Hugging Face Authentication

For models hosted on Hugging Face (VITS Rasa, Indic Parler-TTS), you'll need to authenticate:

```python
from huggingface_hub import login
login(token="your_hf_token_here")
```

> **🔒 Never commit your token to the repository.** Use environment variables or Colab secrets.

---

## 📁 Repository Structure

```
Indian-TTS-models/
│
├── README.md                        # This file
├── requirements.txt                 # Python dependencies
├── .gitignore                       # Git ignore rules
│
├── docs/                            # Documentation, datasets & evaluation results
│   ├── Indian_TTS_Models_Overview.xlsx
│   ├── IndicVoices_VITS_Evaluation.csv
│   ├── Kokoro_Evaluation_Results.csv
│   └── IndicVoices_Audio.zip
│
├── notebooks/                       # Jupyter notebooks
│   ├── Evaluating_TTS_models.ipynb  # Bulk evaluation pipeline
│   ├── VITS_rasa_finetune.ipynb     # VITS & Kokoro testing script
│   ├── indic_parler_tts.ipynb
│   ├── vits_rasa_13.ipynb
│   ├── suno_bark.ipynb
│   ├── xtts_v2.ipynb
│   └── meta_mms.ipynb
│
├── samples/                         # Generated audio samples
│   ├── indic-parler/
│   ├── vits-rasa/
│   ├── suno-bark/
│   ├── kokoro/
│   ├── xtts-v2/
│   └── meta-mms/
│
└── assets/                          # Images, diagrams for README
```

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| **Language** | Python 3.12 |
| **Runtime** | Google Colab (T4 GPU) |
| **ML Frameworks** | PyTorch, Hugging Face Transformers |
| **Audio** | SoundFile, SciPy, TorchAudio |
| **Key Libraries** | `parler-tts`, `coqui-tts`, `transformers` |

---

## 📌 Key Findings *(Preliminary)*

| Model | Naturalness | Speed | Hindi Quality | Ease of Use |
|-------|:-----------:|:-----:|:-------------:|:-----------:|
| **XTTS v2** | ⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ |
| **Meta MMS** | ⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐ |
| **VITS Rasa 13** | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| **Indic Parler-TTS** | ⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐ |
| **Kokoro** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Suno Bark** | ⭐⭐⭐ | ⭐⭐ | ⭐⭐ | ⭐⭐⭐ |

> **Note:** These are preliminary subjective ratings based on initial testing. A formal MOS study is planned.

---

## 🤝 Team & Acknowledgements

This project is part of an internship at **[Kaliber.AI](https://kaliber.ai) / Bay Area Advanced Analytics**.

### Acknowledgements
- [AI4Bharat](https://ai4bharat.org/) for Indic Parler-TTS and VITS Rasa models
- [Hugging Face](https://huggingface.co/) for model hosting and the Transformers library
- [Meta Research](https://ai.meta.com/) for MMS
- [Suno AI](https://www.suno.ai/) for Bark

---

## 📄 License

This project is for **research and educational purposes** only. Individual model licenses apply:

| Model | License |
|-------|---------|
| XTTS v2 | Coqui Public Model License |
| Meta MMS | CC BY-NC 4.0 |
| VITS Rasa 13 | MIT |
| Indic Parler-TTS | Apache 2.0 |
| Suno Bark | MIT |
| Kokoro | Apache 2.0 |

---

<p align="center">
  <strong>⭐ If you find this useful, please star the repository!</strong>
  <br><br>
  <em>Last updated: June 2026</em>
</p>
