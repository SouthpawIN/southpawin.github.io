# OmniSenter

**The flagship. ~32B total / 8B active. Multimodal native. Self-evolving.**

[Repo](https://github.com/SouthpawIN/evolutionary-training) · [Blog posts](https://southpawin.github.io/blog/)

## What it is

A 32B-A8B multimodal MoE that serves as a notebook-keeping auxiliary to Hermes Agent. It has:
- **Synthesia** — a cross-modal memory indexer (Layer 1.5)
- **Ohm** — a self-evolution engine (background loop, atomic weight swap, CMA-ES)
- **A 256K context window** — for the notebook, the structured state object

The 5-stage training pipeline:

1. **Agentic SFT** — 8B QLoRA on Hermes-3 + Nemotron data
2. **Evolutionary merge** — 3 variants A/B/C, continue-train
3. **Sparse upcycle** — 8B dense → 50B-A8B MoE
4. **YaRN** — 6.25x context extension to 256K
5. **Plugin wiring** — Hermes tool calls, notebook schema, pet integration

## Current status

| Stage | Status | ETA |
|---|---|---|
| 1: Agentic SFT | Running — step 1000/4268, loss 0.3959 | ~57h from now |
| 2: Evo merge | Scripts ready, queued | After stage 1 |
| 3: Sparse upcycle | `sparse_upcycle.py` ready | After stage 2 |
| 4: YaRN | Recipe documented | After stage 3 |
| 5: Wiring | Profiles + plugins built | After stage 4 |

## Naming convention

- **Omni** — multimodal native
- **Senter** — Omni + agentic core
- **Ohm** — self-evolution engine
- **Senter Ohm** — flagship, ~32A8B MoE
- **OmniSenter** — the project as a whole

[Read the naming post →](https://southpawin.github.io/blog/the-omni-family/)

## Models (current / pending)

- `sovthpaw/omnistep-12a3b` — 12B total / 3B active (transitional v1)
- `sovthpaw/Omni-Senter-3B` — 3B (transitional v1)
- `sovthpaw/OmniSenter-Base-16B` — 16B base (transitional v1)
- **Senter Ohm ~32A8B** — pending Stage 4 completion

## See also

- [Blog: Senter Ohm flagship](https://southpawin.github.io/blog/senter-ohm-flagship/)
- [Blog: The 5-stage pipeline](https://southpawin.github.io/blog/the-5-stage-pipeline/)
- [Blog: Sparse upcycling deep dive](https://southpawin.github.io/blog/sparse-upcycling-deep-dive/)
- [Blog: The 32A8B math](https://southpawin.github.io/blog/senter-ohm-32a8b-math/)
- [Wiki: Synthesia](https://southpawin.github.io/wiki/concepts/synthesia/)
- [Wiki: Ohm](https://southpawin.github.io/wiki/concepts/ohm/)
