# Optimize-Prompt Skill Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Create a Claude Code skill (`/optimize-prompt`) that scrapes voice AI best practices, analyzes call transcripts, and proposes prompt improvements for Bolna AI dialer system prompts.

**Architecture:** Single skill file (`SKILL.md`) containing the full workflow as instructions for Claude Code. Firecrawl MCP tools handle web scraping. Python `openpyxl` parses Excel transcripts. Cached best practices stored as markdown files in the skill's `references/` directory.

**Tech Stack:** Claude Code Skill (markdown), Firecrawl MCP, Python (openpyxl for Excel parsing), Git CLI

---

## File Structure

```
~/.claude/skills/optimize-prompt/
  SKILL.md                                          # Skill definition + full workflow
  references/
    best-practices-cache/                           # Created on first run
      (bolna-prompting-guide.md)                    # Cached scrape results
      (elevenlabs-conversational-ai.md)             # Cached scrape results
```

---

### Task 1: Create Skill Directory and SKILL.md Skeleton

**Files:**
- Create: `~/.claude/skills/optimize-prompt/SKILL.md`
- Create: `~/.claude/skills/optimize-prompt/references/best-practices-cache/.gitkeep`

- [ ] **Step 1: Create the skill directory structure**

```bash
mkdir -p ~/.claude/skills/optimize-prompt/references/best-practices-cache
touch ~/.claude/skills/optimize-prompt/references/best-practices-cache/.gitkeep
```

- [ ] **Step 2: Write the SKILL.md frontmatter and overview**

Create `~/.claude/skills/optimize-prompt/SKILL.md` with:

```markdown
---
name: optimize-prompt
description: >
  Optimize Bolna AI dialer system prompts by scraping best practices from ElevenLabs
  and Bolna docs, analyzing call transcripts for issues, and proposing prompt improvements.
  Use when the user runs /optimize-prompt or asks to improve/optimize/fix their AI caller prompt.
  Trigger phrases: "optimize prompt", "improve prompt", "fix prompt", "analyze transcripts",
  "prompt issues", "optimize-prompt".
---

# Bolna Prompt Optimizer

Optimize AI dialer system prompts using best practices from ElevenLabs and Bolna,
combined with transcript analysis from real calls.

## Usage

- `/optimize-prompt` — optimize the default agent (vikram)
- `/optimize-prompt priya` — optimize a specific agent
- `/optimize-prompt --refresh-cache` — force re-scrape of best practices
- `/optimize-prompt vikram --refresh-cache` — combine both

## Workflow

Follow these steps in order. Do not skip steps. Present findings to the user
for approval before making any changes.
```

- [ ] **Step 3: Commit**

```bash
cd ~/.claude/skills/optimize-prompt
git init  # Only if not already in a git-tracked location — skills dir is not a repo, skip this
```

No git commit needed here — skill files live in `~/.claude/skills/`, not in a git repo. We'll commit prompt changes to the `bolna_prompt` repo later.

---

### Task 2: Write Step 1 — Argument Parsing and Prompt Resolution

**Files:**
- Modify: `~/.claude/skills/optimize-prompt/SKILL.md`

- [ ] **Step 1: Add the argument parsing section to SKILL.md**

Append this section to `SKILL.md`:

```markdown
### Step 1: Resolve Target Prompt

Parse the user's command arguments:

1. Extract the agent name from the argument. Default to `vikram` if no argument given.
2. Check for `--refresh-cache` flag. If present, set `REFRESH_CACHE = true`.
3. Resolve the prompt file path: `prompt/{agent_name}_system_prompt.md` (relative to the repo root).
4. **Read the prompt file** using the Read tool.
   - If the file does not exist, tell the user:
     > "Prompt file `prompt/{agent_name}_system_prompt.md` not found. Available prompts:"
     Then run `ls prompt/*_system_prompt.md` to show available files, and stop.
5. Store the full prompt content as `[CURRENT_PROMPT]` for later analysis.

**Example resolution:**
- `/optimize-prompt` → `prompt/vikram_system_prompt.md`
- `/optimize-prompt priya` → `prompt/priya_system_prompt.md`
```

- [ ] **Step 2: Verify the section reads correctly**

Read back the file to confirm formatting is correct:

```bash
cat ~/.claude/skills/optimize-prompt/SKILL.md
```

---

### Task 3: Write Step 2 — Best Practices Scraping and Caching

**Files:**
- Modify: `~/.claude/skills/optimize-prompt/SKILL.md`

- [ ] **Step 1: Add the best practices scraping section to SKILL.md**

Append this section to `SKILL.md`:

```markdown
### Step 2: Load or Scrape Best Practices

Check the cache directory: `~/.claude/skills/optimize-prompt/references/best-practices-cache/`

**If cache has `.md` files AND `REFRESH_CACHE` is not true:**

Read all `.md` files from the cache directory using the Read tool. Store their combined content as `[BEST_PRACTICES]`.

**If cache is empty OR `REFRESH_CACHE` is true:**

Use the Firecrawl MCP tools to scrape best practices. Run these searches:

1. **Bolna prompting guide:**
   ```
   firecrawl_search({
     query: "Bolna AI voice agent system prompt best practices guide",
     limit: 3,
     scrapeOptions: { formats: ["markdown"], onlyMainContent: true }
   })
   ```
   Save the combined results to `~/.claude/skills/optimize-prompt/references/best-practices-cache/bolna-prompting-guide.md` using the Write tool.

2. **Bolna GitHub examples:**
   ```
   firecrawl_search({
     query: "Bolna AI agent prompt examples site:github.com",
     limit: 3,
     scrapeOptions: { formats: ["markdown"], onlyMainContent: true }
   })
   ```
   Save to `~/.claude/skills/optimize-prompt/references/best-practices-cache/bolna-github-examples.md`.

3. **ElevenLabs conversational AI prompting:**
   ```
   firecrawl_search({
     query: "ElevenLabs conversational AI agent prompt design best practices",
     limit: 3,
     scrapeOptions: { formats: ["markdown"], onlyMainContent: true }
   })
   ```
   Save to `~/.claude/skills/optimize-prompt/references/best-practices-cache/elevenlabs-conversational-ai.md`.

4. **ElevenLabs TTS optimization:**
   ```
   firecrawl_search({
     query: "ElevenLabs text to speech optimization pronunciation numbers SSML",
     limit: 3,
     scrapeOptions: { formats: ["markdown"], onlyMainContent: true }
   })
   ```
   Save to `~/.claude/skills/optimize-prompt/references/best-practices-cache/elevenlabs-tts-optimization.md`.

After scraping, read all cached files and store as `[BEST_PRACTICES]`.

**If Firecrawl is unavailable** (MCP server not connected), tell the user:
> "Firecrawl MCP server is not available. Please ensure it's configured, or manually add best practice documents to `~/.claude/skills/optimize-prompt/references/best-practices-cache/`."
Then stop.
```

- [ ] **Step 2: Verify the section reads correctly**

Read back the file to confirm.

---

### Task 4: Write Step 3 — Transcript Loading

**Files:**
- Modify: `~/.claude/skills/optimize-prompt/SKILL.md`

- [ ] **Step 1: Add the transcript loading section to SKILL.md**

Append this section to `SKILL.md`:

```markdown
### Step 3: Load Transcripts

Load call transcripts from the `transcripts/` directory in the repo.

1. **Find transcript files:**
   Use the Glob tool to find all `.xlsx` files in the `transcripts/` directory.
   If no files found, tell the user:
   > "No transcript files found in `transcripts/`. Please add `.xlsx` files with call transcripts."
   Then stop.

2. **Parse Excel files:**
   For each `.xlsx` file, run this Python script via the Bash tool:

   ```bash
   python3 -c "
   import openpyxl, json, sys

   wb = openpyxl.load_workbook('transcripts/FILENAME.xlsx', read_only=True)
   ws = wb.active

   headers = [cell.value for cell in next(ws.iter_rows(min_row=1, max_row=1))]
   transcript_col = headers.index('transcript') if 'transcript' in headers else None
   summary_col = headers.index('summary') if 'summary' in headers else None
   lead_id_col = headers.index('lead_id') if 'lead_id' in headers else None
   direction_col = headers.index('direction') if 'direction' in headers else None

   if transcript_col is None:
       print('ERROR: No transcript column found', file=sys.stderr)
       sys.exit(1)

   calls = []
   for row in ws.iter_rows(min_row=2, values_only=True):
       transcript = row[transcript_col]
       if not transcript:
           continue
       calls.append({
           'lead_id': row[lead_id_col] if lead_id_col is not None else None,
           'direction': row[direction_col] if direction_col is not None else None,
           'transcript': str(transcript),
           'summary': str(row[summary_col]) if summary_col is not None and row[summary_col] else ''
       })

   print(json.dumps(calls[:100]))  # Limit to 100 most recent calls for analysis
   wb.close()
   "
   ```

   Replace `FILENAME.xlsx` with the actual filename.

3. **Store the parsed transcripts** as `[TRANSCRIPTS]` — a list of call objects with transcript text and summary.

4. **Report to user:**
   > "Loaded {N} transcripts from {filename}. Proceeding to analysis."
```

- [ ] **Step 2: Verify the section reads correctly**

Read back the file to confirm.

---

### Task 5: Write Step 4 — Transcript Analysis

**Files:**
- Modify: `~/.claude/skills/optimize-prompt/SKILL.md`

- [ ] **Step 1: Add the transcript analysis section to SKILL.md**

Append this section to `SKILL.md`:

```markdown
### Step 4: Analyze Transcripts Against Prompt and Best Practices

With `[CURRENT_PROMPT]`, `[BEST_PRACTICES]`, and `[TRANSCRIPTS]` loaded, perform the analysis.

#### 4a. Categorize Each Call

Read each transcript and classify the outcome:

- **Successful** — dealer engaged meaningfully: discussed products, scheduled visit, placed order, requested info
- **Failed** — early disconnect, dealer frustrated, agent went off-script, no engagement
- **Partial** — some engagement but dealer lost interest or conversation stalled

#### 4b. Identify Issues

For each transcript, check against these issue categories. Compare agent responses against both the prompt rules and the best practices:

| Category | Detection Rules |
|---|---|
| **Flow violations** | Agent skipped steps defined in SECTION 4 of the prompt (e.g., went straight to product without discovery). Steps are out of order. Language check skipped. Identity confirmation missed. |
| **Style violations** | Any single agent response exceeds 60 words or 2 lines. Agent sounds robotic or overly formal. Agent uses scripted phrases instead of natural conversation. Hindi written in romanized form instead of Devanagari. |
| **TTS issues** | Numbers written as digits instead of spelled out (e.g., "49500" instead of "forty-nine thousand five hundred"). Currency symbols used (₹, Rs.). Abbreviations that TTS would mangle. |
| **Hallucinations** | Agent states specific prices, delivery timelines, or product specs without calling `product_lookup` or `service_coverage` tools. Agent invents benefits not in SECTION 7 or 8 of the prompt. |
| **Tone mismatches** | Agent is pushy with a cold/new lead. Agent is too slow/cautious with a warm/hot lead. Agent continues pitching after dealer clearly said no. |
| **Missing guardrails** | Agent badmouths competitors. Agent promises custom pricing. Agent discusses off-topic subjects. Agent repeats the exact same sentence verbatim. |
| **Conversation stalls** | Agent asks the same question twice with identical wording. Conversation goes in circles with no progress. Agent doesn't advance to the next step after getting an answer. |
| **Best practice violations** | Any patterns from `[BEST_PRACTICES]` that the prompt fails to incorporate — e.g., missing pause markers, lack of confirmation loops, TTS pacing issues, missing error recovery patterns. |

#### 4c. Compile the Analysis Report

Structure your findings as:

**ANALYSIS REPORT**

**Summary:**
- Total calls analyzed: {N}
- Successful: {N} | Failed: {N} | Partial: {N}

**Top Issues (ranked by frequency):**

For each issue:
> **Issue #{N}: {Category} — {Brief description}**
> - Frequency: Found in {N}/{total} calls
> - Evidence: "{excerpt from transcript showing the problem}"
> - Prompt section affected: SECTION {N}, Step {N}
> - Proposed fix: {Specific change to make to the prompt text}
> - Before: "{current prompt text}"
> - After: "{proposed new prompt text}"

**Best Practice Gaps:**
List any best practices from the scraped docs that the current prompt does not incorporate, with specific suggestions for where and how to add them.

Present this full report to the user. Do NOT proceed until the user responds.
```

- [ ] **Step 2: Verify the section reads correctly**

Read back the file to confirm.

---

### Task 6: Write Step 5 — User Approval and Step 6 — Apply Changes

**Files:**
- Modify: `~/.claude/skills/optimize-prompt/SKILL.md`

- [ ] **Step 1: Add the approval and apply sections to SKILL.md**

Append this section to `SKILL.md`:

```markdown
### Step 5: Get User Approval

After presenting the analysis report, ask the user:

> "Which changes would you like me to apply? You can:
> - **Approve all** — I'll apply every proposed edit
> - **Approve specific** — tell me the issue numbers to apply (e.g., 'apply 1, 3, 5')
> - **Reject all** — no changes made
> - **Modify** — tell me what to change about a proposal before applying"

Wait for the user's response. Do NOT proceed without explicit approval.

### Step 6: Apply Changes, Commit, and Push

Once the user approves (all or specific changes):

1. **Apply edits:**
   For each approved change, use the Edit tool to modify the prompt file (`prompt/{agent_name}_system_prompt.md`).
   Apply changes one at a time. Each Edit call should use the exact "Before" text as `old_string` and the exact "After" text as `new_string`.

2. **Show the diff:**
   Run `git diff prompt/{agent_name}_system_prompt.md` and show the user the changes.

3. **Commit:**
   ```bash
   git add prompt/{agent_name}_system_prompt.md
   git commit -m "Optimize {agent_name} prompt: {brief summary of changes applied}"
   ```

4. **Push:**
   Ask the user before pushing:
   > "Changes committed. Push to remote (origin main)?"

   If yes:
   ```bash
   git push origin main
   ```

   If no, tell them they can push later with `git push origin main`.

5. **Summary:**
   > "Done! Applied {N} changes to `prompt/{agent_name}_system_prompt.md`.
   > Commit: {commit hash}
   > {Pushed to origin main / Ready to push when you are}"
```

- [ ] **Step 2: Verify the complete SKILL.md reads correctly end-to-end**

Read the full file to confirm all sections flow correctly and there are no formatting issues.

- [ ] **Step 3: Commit the skill spec and plan to the bolna_prompt repo**

```bash
cd "/Users/apoorvgupta/Desktop/Itarang Files/itarang code/bolna_prompt"
git add docs/
git commit -m "Add optimize-prompt skill design spec and implementation plan"
```

---

### Task 7: Test the Skill End-to-End

**Files:**
- Read: `~/.claude/skills/optimize-prompt/SKILL.md` (verify it loads)
- Read: `prompt/vikram_system_prompt.md` (verify resolution works)
- Read: `transcripts/sample_transcripts.xlsx` (verify parsing works)

- [ ] **Step 1: Verify skill is discoverable**

Run `/optimize-prompt` in Claude Code and confirm:
- The skill loads and begins executing
- Step 1 resolves to `prompt/vikram_system_prompt.md`
- The prompt file is read successfully

- [ ] **Step 2: Verify transcript parsing**

Run the Python openpyxl parsing command from Task 4 against `sample_transcripts.xlsx` and confirm:
- JSON output is produced
- Transcripts are parsed with correct fields
- No errors

```bash
cd "/Users/apoorvgupta/Desktop/Itarang Files/itarang code/bolna_prompt"
python3 -c "
import openpyxl, json, sys
wb = openpyxl.load_workbook('transcripts/sample_transcripts.xlsx', read_only=True)
ws = wb.active
headers = [cell.value for cell in next(ws.iter_rows(min_row=1, max_row=1))]
transcript_col = headers.index('transcript')
print(f'Found {ws.max_row - 1} rows, transcript column at index {transcript_col}')
# Parse first 3
for i, row in enumerate(ws.iter_rows(min_row=2, max_row=4, values_only=True)):
    t = row[transcript_col]
    print(f'Row {i+1}: {len(str(t))} chars')
wb.close()
"
```

Expected: Output showing row count and character counts for first 3 transcripts.

- [ ] **Step 3: Verify Firecrawl availability**

Test that Firecrawl MCP tools are accessible by running a simple search:

```
firecrawl_search({ query: "Bolna AI voice agent", limit: 1, scrapeOptions: { formats: ["markdown"], onlyMainContent: true } })
```

Expected: Search results returned with markdown content.

- [ ] **Step 4: Commit the final skill file**

No git commit for the skill itself (it lives in `~/.claude/skills/`, not the repo). This step confirms the skill is complete and functional.
