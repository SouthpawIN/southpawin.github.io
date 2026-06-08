# Models

The hand-curated model catalog. Each entry is a deliberate choice — a model you trust, paired with an eikon you vibe with, with a voice that fits.

## Default: OmniStep (multimodal native)

**Qwen2.5-Omni-3B** — text + voice + vision from one model. 1.96GB GGUF + 1.43GB mmproj. Fits 24GB GPU easily.

## Local models (text + Edge TTS fallback)

| Model | Size | Best for |
|---|---|---|
| Darwin-28B | 15.4GB | Technical chats, heavy reasoning |
| APEX-MTP | 16.1GB | General, MTP speculative decoding |
| Qwen3-Coder-30B-A3B | 17.3GB | Code generation, MoE coder |
| Qwen3.5-27B-Claude-Distilled | 15.4GB | Warm tone, fits Nous Girl persona |
| Qwen3.5-27B-Sushi-Coder-RL | 15.4GB | Codeforces-tuned, execution-style |
| Qwen3.5-35B-A3B | 18.3GB | Strong general-purpose, MoE |

## API combos (Nous Portal — hand-picked)

| Combo | Use case |
|---|---|
| Nous Portal Flagship | Cloud default, vision + tools |
| Nous Portal Auxiliary | Escalation target |

## Source

The catalog lives at `sovthpaw/nous-girl-agent/models/curated.yaml`. Edit it directly. Each entry has:

- `id`, `display_name`, `tier` (multimodal-native / text-with-tts / api-combo)
- `backend` (llama.cpp / ollama / openai-compat / nous-portal)
- `model_path` (GGUF) or `api_base` + `api_key_env`
- `default: true` for the launch default
- `eikon` (sprite/persona)
- `voice.source` (model / edge-tts / melotts / cosyvoice)
- `music.source` (model / heartmula / ace-step / playlist / none)
- `capabilities` (subset of text, voice, music, vision, tools)

See the [nous-girl-agent repo](https://github.com/SouthpawIN/nous-girl-agent) for full schema docs.

---

<div class="tow-badge">TOWARDS SELF-IMPROVEMENT</div>
