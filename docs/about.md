---
title: About
---

# About OmniSenter

<div class="tow-badge">TOWARDS SELF-IMPROVEMENT</div>

---

## What is OmniSenter?

**OmniSenter** is a project to build a **multi-stage agentic MoE with the
Ohm self-evolution engine** — and to make it a useful auxiliary to the
[Hermes Agent](https://github.com/SouthpawIN/hermes-agent).

The model that the project produces is called **Senter Ohm** — a ~32B
total / 8B active sparse-upcycled Mixture-of-Experts with the
self-evolution engine bundled in. The 256K context window is for
**the notebook** — the structured state object that flows between Senter
Ohm and Hermes.

## The three load-bearing ideas

1. **Darwin Family weight-space recombination** (per
   [arXiv:2605.14386](https://arxiv.org/abs/2605.14386)) — a
   training-free way to merge LLMs that outperforms either parent.
2. **Sparse upcycling** (per
   [Komatsuzaki et al. 2022](https://arxiv.org/abs/2212.05055)) — turn
   a dense model into a MoE by copying the FFN as N parallel experts +
   a router. Cheap, fast, and the active compute stays the same.
3. **The Ohm runtime** — the model file *is* the engine. Background
   CMA-ES loop, atomic weight swap, strict-acceptance policy. The model
   gets a tiny bit better every 5 minutes while it serves.

## The naming

- **Omni** = multimodal native (text + vision + audio + video + music)
- **Senter** = Omni with the agentic core wired in (function calling,
  the notebook, plugin routing)
- **Ohm** = the self-evolution engine (the `.ohm` file format)
- **Senter Ohm** = the flagship — all three composited (~32A8B MoE)
- **OmniSenter** = the project itself, and the small Senter
  (`OmniSenter 12B`)

[Read the full naming post →](blog/the-omni-family.md)

## The team

**OmniSenter** is a project by [Chris (SouthpawIN)](https://github.com/SouthpawIN),
built at [Nous Research](https://nousresearch.com). The blog is written
in collaboration with **Nous Girl** (the Senter-side voice).

## The repos

The OmniSenter system spans 9 GitHub repos:

| Repo | Role |
|---|---|
| [`evolutionary-training`](https://github.com/SouthpawIN/evolutionary-training) | Main repo, training scripts, Ohm runtime |
| [`evolutionary-model-merging`](https://github.com/SouthpawIN/evolutionary-model-merging) | Darwin Family (CMA-ES + paper-exact merge) |
| [`multimodal-expansion`](https://github.com/SouthpawIN/multimodal-expansion) | REAP + EvoMoE + sparse_upcycle |
| [`omnistep-fusion`](https://github.com/SouthpawIN/omnistep-fusion) | Cosmos × ACE-Step multimodal merge |
| [`evolutionary-radio`](https://github.com/SouthpawIN/evolutionary-radio) | The OmniStep-brained music radio |
| [`hermes-agent`](https://github.com/SouthpawIN/hermes-agent) | The smart agent Senter is auxiliary to |
| [`senter`](https://github.com/SouthpawIN/senter) | Senter Hermes profile |
| [`nous-girl`](https://github.com/SouthpawIN/nous-girl) | Nous Girl Hermes profile |
| [`chizul`](https://github.com/SouthpawIN/chizul) | Chizul Hermes profile |

## The HuggingFace models

| Model | Size | Status |
|---|---|---|
| [`sovthpaw/omnistep-12a3b`](https://huggingface.co/sovthpaw/omnistep-12a3b) | 12A3B | ✅ published (transitional) |
| [`sovthpaw/Omni-Senter-3B`](https://huggingface.co/sovthpaw/Omni-Senter-3B) | 3B | ✅ published (transitional) |
| [`sovthpaw/OmniSenter-Base-16B`](https://huggingface.co/sovthpaw/OmniSenter-Base-16B) | 16B | ✅ published (transitional) |
| `sovthpaw/omnisenter-12b` | ~12B | ⏳ planned |
| `sovthpaw/omnisenterstep` | TBD | ⏳ planned |
| `sovthpaw/senter-ohm-32a8b` | ~32A8B | ⏳ planned |

## The skill stack

Built on:

- [TRL](https://github.com/huggingface/trl) for SFT
- [PEFT](https://github.com/huggingface/peft) for QLoRA
- [bitsandbytes](https://github.com/TimDettmers/bitsandbytes) for 4-bit
- [llama.cpp](https://github.com/ggerganov/llama.cpp) for inference
- [Xurl](https://github.com/xdevplatform/xurl) for X integration
- [MkDocs Material](https://squidfunk.github.io/mkdocs-material/) for this site

## License

Apache 2.0 (following parent model licenses).

---

<div class="tow-callout">TOWARDS SELF-IMPROVEMENT</div>
