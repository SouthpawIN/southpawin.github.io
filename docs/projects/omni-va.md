# Omni VA

**The assistant. The local model server. The OmniStep Evolution Radio.**

[Repo](https://github.com/SouthpawIN/nous-girl-agent) · [Quick start](https://github.com/SouthpawIN/nous-girl-agent#quick-start)

## What it is

A standalone, voice-interactive, ever-evolving desktop assistant that serves as a **curated local-model server manager**. The assistant is the face of the model — voice and music come *from the model itself*, with a graceful fallback to Edge TTS and curated playlists when you swap to a text-only LLM.

The **OmniStep Evolution Radio** lives as a plugin inside the agent. It's a perpetual radio that watches what you engage with, builds playlists reflecting your taste, trains LoRAs on what you like, and feeds the Ohm evolutionary chain for self-improvement. Notes the agent curates are handoff-ready to **Hermes Agent** for execution.

## Quick start

```bash
git clone https://github.com/SouthpawIN/nous-girl-agent
cd nous-girl-agent
./scripts/install.sh
./scripts/dev.sh  # all three: assistant + radio + agent
```

## Architecture

- **Pet:** forked Open-LLM-VTuber, vendored into `vtuber-core/`
- **Agent:** Omni VA curator (headless Hermes profile)
- **Radio:** OmniStep Evolution Radio plugin (sibling process)
- **Models:** hand-curated YAML in `models/curated.yaml`
- **Eikons:** Live2D sprites in `assistant/sprites/`

## Default model

**OmniStep (Qwen2.5-Omni-3B)** — multimodal native. Text + voice from one model, music from the radio plugin. Falls back to Edge TTS Jenny if you swap in a text-only LLM.

See [Models](../models/index.md) for the full catalog.

## Tiers of the agent

```
Omni VA (curation)  →  Senter (prioritization)  →  Hermes main (execution)
            ↑                                                            ↓
            └────────── writes notes to ~/wiki/assistant-curated/ ────────────┘
```

The assistant's curator is **bounded** — web search, web fetch, file write (notes only), social. It can't execute code. That's intentional.

---

## See also

- [Blog: Senter as Hermes Auxiliary](https://southpawin.github.io/blog/senter-as-hermes-auxiliary/)
- [Blog: The 5-Stage Pipeline](https://southpawin.github.io/blog/the-5-stage-pipeline/)
- [Blog: The Notebook Schema](https://southpawin.github.io/blog/the-notebook-schema/)
