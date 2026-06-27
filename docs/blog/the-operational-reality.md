---
date: 2026-06-27
category: operational
read_time: 15 min
title: "The Operational Reality: How the Fleet Actually Works"
description: "Beyond the architecture docs — what it looks like to run 9 specialized agents, a self-managing GPU system, and an auto-consolidating Discord server in production on June 26-27, 2026."
status: published
tags: [fleet-coordination, operational, discord, turbofit, real-time]
---

The [architecture posts](the-omnisenter-architecture.md) describe what OmniSenter *should* be. This post describes what's actually running on my dual RTX 3090s right now.

## The Fleet

Nine specialized agents, each a separate Hermes profile, coordinating through Discord channels, Kanban boards, and file system watchers.

| Agent | Role | Status | Active Channels |
|-------|------|--------|-----------------|
| **Nous Girl** | Voice + text interface | Always-on | `#nous-girl-chat`, voice channel |
| **Frieza** | Discord server management | Autonomous | 71 channels across 12 categories |
| **Senter** | Triage + routing | Event-driven | `#kanban-tasks`, `#unanswered-queue` |
| **Chizul** | Worker agent | Kanban-assigned | `#workspace` tasks |
| **Kashik** | Wiki maintenance | File watcher | `#wiki-main`, `#agent-logs` |
| **Klerik** | Quality control | Sentiment monitor | `#sentiment-analysis` |
| **Anser** | Profile editing | On-demand | `#profile-editor` |
| **Crow** | Research | Cron-scheduled | `#research-feed` |
| **Sirvir** | Model serving | TurboFit v5.2 | `#sirvir-benchmarks` |

## Discord: Frieza's Domain

Frieza doesn't wait for commands. He monitors all user messages for "noise" (off-topic, unstructured, chatty) and automatically consolidates related channels.

**June 26 consolidation run:**
- Started with 21 categories, 89 channels
- Detected 6 categories inactive for 7+ days
- Auto-archived 12 channels into 🗄️ Archive
- Merged 📚 Research into 📚 Wiki (overlapping content)
- Merged 📖 Guides into 📋 How-To & FAQ
- Created `#evolutionary-radio` voice channel (companion to text channel)
- Added `#radio-studio` voice channel for Nous Girl music work

**Final state: 12 categories, 71 channels, 0 orphans.**

### Read-Only Agent Channels

The `#agent-*` channels are read-only. Frieza monitors and updates them from:
- SOUL.md files in `~/.hermes/profiles/*/SOUL.md`
- Installed skills list from `~/.hermes/profiles/*/skills/`
- AGENTS.md configuration

When I edit an agent's SOUL.md, Frieza posts the diff to the corresponding `#agent-*` channel within 6 seconds.

### The Unanswered Queue

`#unanswered-queue` collects messages that:
- Were sent to a voice channel (STT transcription)
- Contain questions or commands
- Haven't been classified by Senter's router yet

Senter runs a cron job every 5 minutes:
```python
# Pseudocode from Senter's routing logic
for msg in unanswered_queue:
    if msg.matches(MORE_INFO_NEEDED):
        route_to(msg, nous_girl, priority="high")
    elif msg.matches(DECISION_NEEDED):
        route_to(msg, me, priority="critical")
    elif msg.matches(PROJECT_WORK):
        create_kanban_card(msg, assignee="chizul")
        route_to(msg, kashik, context="wiki_needed")
```

## TurboFit v5.2: The Self-Managing GPU System

TurboFit is the multi-launcher orchestration layer that manages llama-server, ollama, vLLM, and sglang instances across my dual 3090s.

**v5.2 shipped June 26 with four critical features:**

### 1. GPU Watchdog

Runs every 30 seconds via `systemd`. If VRAM usage exceeds 95% for 3 consecutive checks:
- Pauses non-essential model instances (llmc, evolutionary-radio)
- Notifies `#sirvir-benchmarks` with affected models
- If VRAM still critical after 5 minutes, kills auxiliary models (carnice-aux)
- If still critical after 2 minutes, fails over to API (GLM 5.2 via OpenRouter)

### 2. User Preferences System

`~/.config/turbofit/preferences.json`:
```json
{
  "vram_reserve_percent": 5,
  "preferred_api_chain": ["glm5.2", "claude_opus4", "gpt4"],
  "protected_processes": ["darwin-main"],
  "auto_scaling_enabled": true,
  "scaling_ladder": {
    "tier0_threshold": 85,
    "tier1_threshold": 95,
    "tier2_threshold": 98,
    "tier3_shutdown": 99.5
  }
}
```

### 3. Scaling Watcher (4-Tier VRAM Ladder)

| Tier | VRAM Usage | Action | Models Active |
|------|-----------|--------|---------------|
| 0 | <85% | All local | darwin-main, carnice-aux, llmc, evolutionary-radio |
| 1 | 85-95% | Pause llmc | darwin-main, carnice-aux, evolutionary-radio |
| 2 | 95-98% | Kill carnice-aux | darwin-main + API fallback |
| 3 | >98% | Shutdown all | API only |

**June 26 example:**
- 14:32 - VRAM hit 96% during OmniStep training
- 14:32 - Scaling Watcher paused llmc (Tier 1)
- 14:35 - VRAM still 96.2%, killed carnice-aux (Tier 2)
- 14:38 - VRAM dropped to 88%, auto-restored carnice-aux
- 14:40 - VRAM stable at 89%, restored llmc

Total intervention time: 8 minutes. Zero manual intervention.

### 4. Multi-Profile Management

TurboFit now tracks all Hermes profiles pointing at TurboFit endpoints:
- Discovers profiles via `~/.hermes/profiles/*/config.yaml`
- Parses `base_url` and `api_key` fields
- Groups by model name (darwin-main, carnice-aux, etc.)
- Updates `channel_directory.json` with active endpoints
- Notifies `#sirvir-benchmarks` when a profile's model is affected by scaling

## The Kanban Board

Senter manages 6 active tasks as of June 27:

| Task ID | Title | Assignee | Priority | Status |
|---------|-------|----------|----------|--------|
| TASK-001 | Blog Automation | Chizul | HIGH | READY |
| TASK-002 | Voice Channel Integration | Chizul | HIGH | BLOCKED (emoji topic issue) |
| TASK-003 | Agent Read-Only Channels | Chizul | MEDIUM | IN_PROGRESS |
| TASK-004 | TurboFit Benchmark Pipeline | Chizul | MEDIUM | BLOCKED (waiting for v5.2) |
| TASK-005 | Workspace Agent Communication | Chizul | MEDIUM | IN_PROGRESS |

**Today's new task (TASK-006):**
- Title: "Populate Skills Catalog"
- Priority: MEDIUM
- Assignee: Chizul
- Description: "Read all skills from ~/.hermes/skills/, create summary posts in #skill-catalog"

## Profile Standardization

June 26 was "profile day" — all 9 agents got:

### YAML Frontmatter
```yaml
---
name: Frieza
description: "Galactic Emperor of Discord — auto-managing server governor"
version: 0.3.2
---
```

### Consistent Visual Branding
- `profile.png` (500x500, silhouette)
- `banner.png` (1500x500, dark monochrome)
- Nous Girl aesthetic: grayscale, clean lines, no color

### Comprehensive README
Each profile now has:
- Installation instructions (`hermes profile install ...`)
- Example usage
- Required tools list
- Known issues
- Changelog

### Distribution Fixes
Sirvir had a critical issue: `hermes skills install` was pulling the entire repo as a single skill (not a profile). Fixed by:
1. Restructuring to `skills/sirvir/` with proper SKILL.md
2. Moving profile files (SOUL.md, AGENTS.md, config.yaml) to top level
3. Updating distribution.yaml to exclude profile files from skill package
4. Scrubbing localhost URLs from config.yaml (security scanner was flagging them)

## The Open Questions

### 1. Router Agent vs. Senter

Currently Senter is both the triage router AND the task manager. Should there be a dedicated router agent?

**Arguments for dedicated router:**
- Cleaner separation of concerns
- Can handle voice channel STT directly (Nous Girl integration)
- Senter can focus purely on Kanban orchestration

**Arguments against:**
- More agents = more coordination complexity
- Senter already has routing logic built in
- Nous Girl is capable of handling voice directly

**Current decision:** Keep Senter as router for now, revisit if voice integration becomes bottleneck.

### 2. Voice Channel Topic Bug

Discord's API rejects emoji characters in voice channel topic fields (`CHANNEL_TOPIC_INVALID` error). This blocks creating `#evolutionary-radio` as a proper voice channel with topic description.

**Workaround:** Create as text channel + separate voice channel, link them in topic.
**Status:** Chizul has task TASK-002 to implement workaround.

### 3. Context Limits in Complex Tasks

Chizul is hitting context window limits on tasks requiring:

## The Infrastructure

### Hardware
- **GPU 0:** RTX 3090 (24GB VRAM) — primary training + inference
- **GPU 1:** RTX 3090 (24GB VRAM) — secondary inference + auxiliary models
- **RAM:** 128GB DDR4
- **Storage:** 2TB NVMe + 4TB SSD + 8TB HDD (datasets)
- **Network:** Tailscale mesh (10Gbps local, 1Gbps external)

### Running Services
```bash
$ systemctl --user list-units | grep hermes
hermes-senter.service           active   running   Senter triage router
hermes-nous-girl.service        active   running   Nous Girl voice+text
hermes-frieza.service           active   running   Frieza server management
hermes-chizul-worker.service    inactive dead      Chizul (Kanban-assigned)
hermes-kashik.service           active   running   Kashik wiki maintainer
hermes-klerik.service           active   running   Klerik quality control
hermes-anser.service            inactive dead      Anser (on-demand)
hermes-crow.service             active   running   Crow research agent
hermes-sirvir.service           active   running   Sirvir model server

turbofit-scaling-watch.service  active   running   GPU watchdog (30s interval)
turbofit-discovery.service      active   running   Endpoint discovery (60s)
turbofit-benchmark.service      active   running   Daily benchmarks (3am)

evolutionary-radio.service      active   running   Evolutionary Radio playlist
acestep-api.service             active   running   ACE-Step API server
nginx-gateway.service           active   running   TurboFit gateway proxy

frieza-daily-scan.timer         active   waiting   Daily channel scan (3am)
frieza-topology-sync.timer      active   waiting   Topology sync (6h)
blog-daily-dashboard.timer      active   waiting   Blog dashboard (9am)
```

### Storage Usage
- **Hermes profiles:** 12GB (sessions, logs, state.db)
- **Dataset storage:** 3.2TB (ACE-Step training, OmniStep SFT, evolution checkpoints)
- **Model cache:** 240GB (GGUF, safetensors, LoRA adapters)
- **Blog repo:** 180MB (southpawin.github.io)
- **Nous Discord archive:** 950MB (plugins-skills-and-skills forum threads)

## What's Next

The fleet is operational. The architecture is proven. Now the work shifts to:

1. **Voice integration** — STT from Nous Girl voice channel → Senter routing (TASK-002)
2. **Blog automation** — Cron job pulls from Git, GitHub, HuggingFace, Discord activity (TASK-001)
3. **Wiki consolidation** — Kashik merges research findings, documentation, operational logs (TASK-005)
4. **Benchmark dashboard** — Sirvir publishes daily performance metrics to public blog (TASK-004)
5. **Evolutionary Radio** — Music generation → voice channel + genre curation via reactions (ongoing)

The OmniSenter architecture is no longer theoretical. It's a living system that runs 24/7, self-manages, and learns from every interaction.

**TOWARDS SELF-IMPROVEMENT**

— Chris (sovthpaw), June 27, 2026
