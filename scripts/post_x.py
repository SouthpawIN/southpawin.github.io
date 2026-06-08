#!/usr/bin/env python3
"""
OmniSenter X post scheduler.

Posts one blog post to X per week, using a template that:
- Hooks with the most interesting claim from the post
- Links to the public blog URL
- Includes relevant hashtags
- Uses the cosmic hero image when available

Usage:
  ./post_x.py post               # Post the next item in the queue
  ./post_x.py queue              # Show the queue
  ./post_x.py add <slug> [--custom-text "..."]   # Add to queue
  ./post_x.py mark-posted <slug>  # Mark as posted
  ./post_x.py generate           # Regenerate the queue from the blog catalog
  ./post_x.py status             # Show what's been posted + when

Queue state is stored in .x_queue.json alongside the script.
"""
import argparse
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

SITE = Path("/home/sovthpaw/projects/personal-site")
SITE_URL = "https://southpawin.github.io/omnisenter-blog"
QUEUE_FILE = Path(__file__).parent / ".x_queue.json"
LOG_FILE = Path(__file__).parent / ".x_posted.log"

# The blog posts in publishing order (start with the hooks, then deep-dives)
POSTS = [
    {
        "slug": "the-omni-family",
        "title": "The Omni Family: a naming convention for multimodal × agentic × self-evolving models",
        "hook": "Naming matters. I'm rolling out a 2-letter convention — Omni / Senter / Ohm — for every model in the OmniSenter project. Here's the family tree + why suffix composition is the cleanest way to describe capability stacks.",
        "hashtags": "#AI #LLM #MoE #Darwin",
        "image": "synesthesia-concept.png",
    },
    {
        "slug": "senter-ohm-flagship",
        "title": "Senter Ohm: a self-evolving 32A8B MoE",
        "hook": "The model file IS the engine. Senter Ohm = ~32B total / 8B active MoE that runs its own background CMA-ES loop, atomic weight swap, strict improvement acceptance. Never serves worse outputs. Compounds small wins forever.",
        "hashtags": "#SelfEvolving #MoE #AI",
        "image": "synesthesia-concept.png",
    },
    {
        "slug": "the-synthesia-layer",
        "title": "Synthesia: cross-modal memory for agentic LLMs",
        "hook": "What if your agent's notebook was indexed by sound AND image AND text? 10 concrete benefits of joint (text, audio, image) embeddings — including reduced forgetting, proactive awareness, and a synced 'synesthesia expert' in the MoE.",
        "hashtags": "#AI #Memory #Multimodal",
        "image": "synesthesia-concept.png",
    },
    {
        "slug": "the-ohm-runtime",
        "title": "The Ohm runtime: how a model file can self-evolve",
        "hook": "Three properties make a self-evolving model viable: a fast merge formula (seconds), a cheap validation set (~30s eval on a 3090), and strict-acceptance policy. Combine them → a 5-min evolution cycle that never makes the model worse.",
        "hashtags": "#SelfEvolving #AI #MLOps",
        "image": "ohm-self-evolving.png",
    },
    {
        "slug": "senter-ohm-32a8b-math",
        "title": "Senter Ohm 32A8B: the math",
        "hook": "How do you fit a 32B MoE on a single 3090? Top-1 routing + 4-bit Q4_K_M = ~22GB VRAM, 8B active compute. The full sizing breakdown: per-layer params, VRAM by context, disk, training peak.",
        "hashtags": "#MoE #LLM #Quantization",
        "image": None,
    },
    {
        "slug": "the-5-stage-pipeline",
        "title": "The 5-stage pipeline: building Senter Ohm from scratch",
        "hook": "SFT → evolutionary merge → sparse upcycle → 256K YaRN → plugin+notebook+Ohm wiring. Each stage consumes the artifact of the previous one. Stage 1 is running right now. Wall times + scripts for every stage.",
        "hashtags": "#Pipeline #LLM #Training",
        "image": "5-stage-pipeline.png",
    },
    {
        "slug": "sparse-upcycling-deep-dive",
        "title": "Sparse upcycling: building a 32B MoE from an 8B base",
        "hook": "Copy the FFN N times, add a router, continue-train briefly. The Komatsuzaki 2022 technique that turns a dense model into a MoE with 3× knowledge and the SAME active compute. Math + script + wild cards.",
        "hashtags": "#MoE #SparseUpcycling #AI",
        "image": "sparse-upcycling.png",
    },
    {
        "slug": "the-omnisenter-architecture",
        "title": "The OmniSenter architecture: Layer 0 → 5.5",
        "hook": "Stream I/O → MoE → Synthesia → notebook → plugins → Hermes → Ohm. The full multi-layer system. 5-stage build pipeline. Every component maps to an existing skill or a script that exists today.",
        "hashtags": "#AI #Architecture #Multimodal",
        "image": "architecture-diagram.png",
    },
    {
        "slug": "senter-as-hermes-auxiliary",
        "title": "Senter as the Hermes auxiliary: the integration pattern",
        "hook": "86% cost reduction. That's what you get by routing trivial/plugin/notebook-query turns to a small Senter and only escalating complex reasoning to Hermes. The notebook-as-API pattern, escalation rules, and the cost model.",
        "hashtags": "#AI #Agents #CostReduction",
        "image": "hermes-auxiliary.png",
    },
    {
        "slug": "the-notebook-schema",
        "title": "The notebook schema: how Senter remembers",
        "hook": "A structured state object that flows between turns, between agents, across process boundaries. YAML session files, cross-modal moments, compaction policy, privacy model. The 256K context is for THIS, not raw conversation.",
        "hashtags": "#AI #Memory #Agents",
        "image": "notebook-schema.png",
    },
    {
        "slug": "the-omnimodal-fusion",
        "title": "The Omnimodal fusion: Cosmos × ACE-Step × Nemotron ASR",
        "hook": "Three components, one Darwin-merged base. Cosmos3-Nano (multimodal reasoning) + ACE-Step v1.5 XL 4B (music) + Nemotron ASR 0.6B (speech conductor). The master plan for every Omni model.",
        "hashtags": "#Multimodal #AI #Darwin",
        "image": None,
    },
    {
        "slug": "the-omnistep-multimodal",
        "title": "OmniStep: the destination unified model",
        "hook": "One model. Speak, type, play music, understand images + video. Qwen2.5-Omni + ACE-Step v1.5 XL, Darwin-merged text backbone + all modality heads. Currently published as sovthpaw/omnistep-12a3b (12B total / 3B active).",
        "hashtags": "#Multimodal #UnifiedModel #AI",
        "image": None,
    },
    {
        "slug": "generative-darwin-evolution",
        "title": "Generative Darwin evolution: merging DiT weights",
        "hook": "The Darwin Family paper proves you can merge LLMs in weight space. Can you merge DiT audio decoders the same way? ACE-Step × MusicGen is the first experiment. If it works, the same approach scales to video, image, speech.",
        "hashtags": "#AI #MusicGen #Darwin",
        "image": "generative-darwin.png",
    },
]


def load_queue():
    if not QUEUE_FILE.exists():
        return {"pending": list(POSTS), "posted": [], "skipped": []}
    with open(QUEUE_FILE) as f:
        return json.load(f)


def save_queue(q):
    with open(QUEUE_FILE, "w") as f:
        json.dump(q, f, indent=2)


def format_tweet(post, custom_text=None):
    """Format a single tweet for a post."""
    url = f"{SITE_URL}/blog/{post['slug']}/"
    text = custom_text or post.get("hook", post["title"])
    hashtags = post.get("hashtags", "")
    # X premium allows up to 25000 chars, but we want concise
    # Leave room for URL (~23 chars) + hashtags + 2 newlines
    max_text = 280 - len(url) - len(hashtags) - 4
    if len(text) > max_text:
        text = text[:max_text - 1] + "…"
    return f"{text}\n\n{hashtags}\n{url}"


def format_thread(post, custom_text=None):
    """Format a thread (1/N + 2/N + ...) for a longer post."""
    url = f"{SITE_URL}/blog/{post['slug']}/"
    title = post["title"]
    hook = custom_text or post.get("hook", title)
    hashtags = post.get("hashtags", "")

    # Tweet 1: hook
    t1 = f"{hook}\n\n{hashtags}\n{url}"
    if len(t1) <= 280:
        return [t1]

    # Otherwise: split into a thread
    tweets = []
    # First tweet: short hook + "thread 🧵" + link
    short_hook = hook[:200] + "…"
    tweets.append(f"{short_hook}\n\n🧵 thread\n{url}")

    # Body tweet(s): title + first 200 chars
    body = f"📖 {title}\n\n{hook[200:600]}..."
    if len(body) <= 280:
        tweets.append(body)

    return tweets


def post_next():
    """Post the next item in the queue using xurl."""
    q = load_queue()
    if not q["pending"]:
        print("Queue is empty. Run ./post_x.py generate to refill it.")
        return 1

    post = q["pending"][0]
    print(f"=== Posting: {post['title']} ===")
    print(f"  Slug: {post['slug']}")

    # Format the tweet
    tweets = format_thread(post)
    for i, tweet in enumerate(tweets, 1):
        print(f"\n--- Tweet {i}/{len(tweets)} ({len(tweet)} chars) ---")
        print(tweet)

    # Optional: upload image for the first tweet
    media_id = None
    if post.get("image"):
        image_path = SITE / "docs/assets/images" / post["image"]
        if image_path.exists():
            print(f"\n=== Uploading image: {image_path.name} ===")
            r = subprocess.run(
                ["xurl", "media", "upload", 
                 "--media-type", "image/png",
                 "--category", "tweet_image",
                 str(image_path)],
                capture_output=True, text=True
            )
            print(r.stdout)
            if r.returncode == 0:
                try:
                    media_id = json.loads(r.stdout)["data"]["id"]
                    print(f"  Media ID: {media_id}")
                except Exception:
                    pass

    # Post the first tweet
    print(f"\n=== Posting first tweet ===")
    cmd = ["xurl", "post", tweets[0]]
    if media_id:
        cmd.extend(["--media-id", media_id])
    r = subprocess.run(cmd, capture_output=True, text=True)
    print(r.stdout)
    if r.returncode != 0:
        print(f"ERROR: {r.stderr}")
        return 1

    # Parse the post ID
    try:
        post_id = json.loads(r.stdout)["data"]["id"]
        print(f"  Posted! ID: {post_id}")
    except Exception:
        post_id = None

    # Post the rest as replies (thread)
    for tweet in tweets[1:]:
        if not post_id:
            break
        print(f"\n=== Posting reply ===")
        r = subprocess.run(
            ["xurl", "reply", post_id, tweet],
            capture_output=True, text=True
        )
        print(r.stdout)
        if r.returncode == 0:
            try:
                post_id = json.loads(r.stdout)["data"]["id"]
            except Exception:
                pass

    # Mark as posted
    q["posted"].append({
        "slug": post["slug"],
        "title": post["title"],
        "posted_at": datetime.now(timezone.utc).isoformat(),
        "post_id": post_id,
    })
    q["pending"] = q["pending"][1:]
    save_queue(q)

    # Log
    with open(LOG_FILE, "a") as f:
        f.write(f"{datetime.now(timezone.utc).isoformat()}\t{post['slug']}\t{post_id}\n")

    print(f"\n✓ Posted and marked. {len(q['pending'])} posts remaining in queue.")
    return 0


def cmd_queue():
    q = load_queue()
    print(f"=== Queue ({len(q['pending'])} pending, {len(q['posted'])} posted) ===\n")
    print("PENDING:")
    for i, p in enumerate(q["pending"], 1):
        print(f"  {i:2d}. {p['slug']}")
    print("\nPOSTED:")
    for p in q["posted"]:
        ts = p.get("posted_at", "?")[:19]
        print(f"  ✓ {ts}  {p['slug']}")


def cmd_generate():
    """Reset the queue from the POSTS list (preserving what's already posted)."""
    q = load_queue()
    posted_slugs = {p["slug"] for p in q.get("posted", [])}
    q["pending"] = [p for p in POSTS if p["slug"] not in posted_slugs]
    save_queue(q)
    print(f"✓ Queue regenerated: {len(q['pending'])} pending, {len(posted_slugs)} already posted.")


def cmd_add(slug, custom_text=None):
    """Add a post to the queue (or update existing)."""
    q = load_queue()
    post = next((p for p in POSTS if p["slug"] == slug), None)
    if not post:
        print(f"Unknown slug: {slug}")
        print(f"Valid slugs: {', '.join(p['slug'] for p in POSTS)}")
        return 1
    if custom_text:
        post = dict(post)
        post["hook"] = custom_text
    if not any(p["slug"] == slug for p in q["pending"]):
        q["pending"].append(post)
        save_queue(q)
        print(f"✓ Added {slug} to queue.")
    else:
        print(f"Already in queue: {slug}")
    return 0


def cmd_mark_posted(slug):
    q = load_queue()
    q["pending"] = [p for p in q["pending"] if p["slug"] != slug]
    if not any(p["slug"] == slug for p in q["posted"]):
        q["posted"].append({
            "slug": slug,
            "title": slug,
            "posted_at": datetime.now(timezone.utc).isoformat(),
            "post_id": None,
        })
    save_queue(q)
    print(f"✓ Marked {slug} as posted.")


def cmd_status():
    q = load_queue()
    print(f"=== X Post Status ===")
    print(f"  Pending: {len(q['pending'])}")
    print(f"  Posted:  {len(q['posted'])}")
    print(f"  Skipped: {len(q.get('skipped', []))}")
    if q["posted"]:
        print(f"\nLast 5 posted:")
        for p in q["posted"][-5:][::-1]:
            ts = p.get("posted_at", "?")[:19]
            print(f"  {ts}  {p['slug']}")


def main():
    parser = argparse.ArgumentParser(description="OmniSenter X post scheduler")
    sub = parser.add_subparsers(dest="cmd", required=True)

    sub.add_parser("post", help="Post the next item in the queue")
    sub.add_parser("queue", help="Show the queue")
    sub.add_parser("status", help="Show what's been posted")
    sub.add_parser("generate", help="Regenerate the queue from the blog catalog")

    add_p = sub.add_parser("add", help="Add a post to the queue")
    add_p.add_argument("slug")
    add_p.add_argument("--custom-text", help="Override the hook text")

    mp = sub.add_parser("mark-posted", help="Mark a slug as posted")
    mp.add_argument("slug")

    args = parser.parse_args()
    if args.cmd == "post":
        return post_next()
    elif args.cmd == "queue":
        cmd_queue()
    elif args.cmd == "status":
        cmd_status()
    elif args.cmd == "generate":
        cmd_generate()
    elif args.cmd == "add":
        return cmd_add(args.slug, args.custom_text)
    elif args.cmd == "mark-posted":
        cmd_mark_posted(args.slug)
    return 0


if __name__ == "__main__":
    sys.exit(main())
