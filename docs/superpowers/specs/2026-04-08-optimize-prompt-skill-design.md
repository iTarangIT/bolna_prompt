# Design Spec: Bolna Prompt Optimizer Skill (`/optimize-prompt`)

**Date:** 2026-04-08
**Status:** Draft

---

## Overview

A Claude Code skill that optimizes Bolna AI dialer system prompts by:
1. Scraping best practices from ElevenLabs and Bolna docs (cached)
2. Analyzing call transcripts to identify prompt-related issues
3. Proposing specific prompt edits for user approval
4. Committing and pushing approved changes to the git repo

## Trigger

- **Manual only** via `/optimize-prompt [agent_name]`
- Default agent: `vikram` (resolves to `prompt/vikram_system_prompt.md`)
- Pattern: `prompt/{agent_name}_system_prompt.md`
- Flag: `--refresh-cache` to force re-scrape of best practices

## Skill Location

```
~/.claude/skills/optimize-prompt/
  SKILL.md                              # Skill definition
  references/
    best-practices-cache/               # Cached scraping results (created on first run)
      bolna-prompting-guide.md
      elevenlabs-conversational-ai.md
      ...
```

**Expects to be run from inside the `bolna_prompt` repo directory.**

---

## Workflow

### Step 1 — Resolve Target Prompt

- Parse argument (default: `vikram`)
- Map to `prompt/{name}_system_prompt.md`
- Error with clear message if file doesn't exist

### Step 2 — Load or Scrape Best Practices

Check if `~/.claude/skills/optimize-prompt/references/best-practices-cache/` has cached files.

**If cache is empty (first run or after `--refresh-cache`):**
- Use Firecrawl to search and scrape Bolna docs (prompting guide, best practices, GitHub examples)
- Use Firecrawl to search and scrape ElevenLabs docs (TTS-optimized prompting, conversational AI guidelines)
- Save each scraped source as a separate markdown file in the cache directory

**If cache exists:**
- Skip scraping, load cached files directly

**URL discovery:** The skill uses Firecrawl search (not hardcoded URLs) to find the most relevant pages by searching for terms like "Bolna prompt engineering guide" and "ElevenLabs conversational AI prompting".

### Step 3 — Load Transcripts

- Read from `transcripts/` directory
- Support `.xlsx` files (parsed via Python `openpyxl`)
- Expected columns: `lead_id`, `timestamp`, `direction`, `to number`, `from number`, `transcript`, `summary`, `conv_id`
- Parse into structured format: transcript text + summary per call
- **Future:** Google Sheet URL support (user provides link, skill pulls via Sheets API or export URL)

### Step 4 — Analyze Transcripts

Categorize each call by outcome:
- **Successful** — dealer engaged, visit scheduled, order discussed, info shared
- **Failed** — early hangup, repeated confusion, agent off-script, dealer frustrated
- **Partial** — some engagement but lost interest midway

Detect issues by comparing transcripts against the prompt rules and scraped best practices:

| Category | What to Look For |
|---|---|
| Flow violations | Steps skipped, out-of-order, discovery questions missed |
| Style violations | Responses too long (>60 words), overly formal, robotic phrasing |
| TTS issues | Numbers not spelled out, symbols instead of words, TTS-unfriendly formatting |
| Hallucinations | Product info, pricing, or delivery promises not sourced from tools |
| Tone mismatches | Cold leads getting aggressive pitch, warm leads getting slow discovery |
| Missing guardrails | Agent badmouthing competitors, making unauthorized promises, repeating verbatim |
| Conversation stalls | Agent repeating itself, circular dialogue, no forward progress |

### Step 5 — Present Findings + Proposed Edits

Show a structured report to the user:

1. **Summary stats** — total calls analyzed, success/fail/partial counts
2. **Top issues** — ranked by frequency
3. **Per-issue detail:**
   - Issue description
   - Evidence (transcript excerpts)
   - Specific prompt section affected
   - Proposed edit (before/after)

**Wait for user approval before proceeding.** User may approve all, reject all, or selectively approve individual changes. Only approved edits are applied.

### Step 6 — Apply, Commit, Push

On approval:
- Edit the prompt file with approved changes
- Commit with descriptive message (e.g., "Optimize vikram prompt: fix flow violations, improve TTS formatting")
- Push to remote (`origin main`)

---

## Transcript Source Roadmap

| Phase | Source | How |
|---|---|---|
| Now | Local `.xlsx` file in `transcripts/` | `openpyxl` parsing |
| Later | Google Sheet | User provides link; skill pulls via export URL or Sheets API |

---

## Constraints

- Skill must be run from inside the `bolna_prompt` repo
- Never modify prompt without user approval
- Firecrawl must be available for first-run scraping
- Python with `openpyxl` must be available for Excel parsing
- Git remote must be configured for push step
