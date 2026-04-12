#!/usr/bin/env python3
"""Scan Bolna transcripts for known prompt-violation patterns."""
import argparse
import json
import re
from collections import defaultdict


ROMANIZED_HINDI_TERMS = [
    r"\bbol raha\b",
    r"\btheek\b",
    r"\brahegi\b",
    r"\bkarein\b",
    r"\bmein baat\b",
    r"\bkaam hota\b",
    r"\bbaare mein\b",
    r"\bhoon\b",
    r"\bnamaste\b",
    r"\babhi\b",
    r"\bsahi\b",
    r"\bkya\b",
    r"\bbataiye\b",
    r"\bzaroor\b",
]

ENGLISH_SILENCE = re.compile(r"hey,?\s*are you still there", re.IGNORECASE)
WRONG_COMPANY = re.compile(r"\bTarang Batteries\b", re.IGNORECASE)
DIGITS_RE = re.compile(r"\b\d{2,}\b")
LANG_QUESTION_RE = re.compile(r"शुरू करने से पहले")
HALLUCINATED_FINANCING = re.compile(
    r"\b(HDFC|ICICI|SBI|Axis|Kotak|Bajaj Finance|interest rate|EMI of|percent interest|p\.a\.)\b",
    re.IGNORECASE,
)
VOICEMAIL_HINTS = [
    "voicemail",
    "leave a message",
    "after the beep",
    "नहीं उठाया",
    "callback later",
]

ROMAN_RE = re.compile("|".join(ROMANIZED_HINDI_TERMS), re.IGNORECASE)
DEVANAGARI_RE = re.compile(r"[\u0900-\u097F]")


def split_turns(transcript: str) -> list[tuple[str, str]]:
    """Return list of (role, text) tuples. Handles assistant:/user: and Agent:/User: prefixes."""
    if not transcript:
        return []
    lines = transcript.splitlines()
    turns = []
    current_role = None
    current_text = []
    role_re = re.compile(r"^(assistant|user|agent|customer|bot|caller|ai)\s*:\s*", re.IGNORECASE)
    for raw in lines:
        line = raw.strip()
        if not line:
            continue
        m = role_re.match(line)
        if m:
            if current_role is not None:
                turns.append((current_role, " ".join(current_text).strip()))
            role = m.group(1).lower()
            if role in ("assistant", "agent", "bot", "ai"):
                current_role = "assistant"
            else:
                current_role = "user"
            current_text = [line[m.end():]]
        else:
            current_text.append(line)
    if current_role is not None:
        turns.append((current_role, " ".join(current_text).strip()))
    return turns


def detect_prompt_version(transcript: str) -> str:
    if re.search(r"^assistant\s*:", transcript, re.MULTILINE | re.IGNORECASE):
        return "current"
    if re.search(r"^Agent\s*:", transcript, re.MULTILINE):
        return "older"
    return "unknown"


def make_excerpt(text: str, n: int = 160) -> str:
    text = re.sub(r"\s+", " ", text).strip()
    return text if len(text) <= n else text[: n - 1] + "…"


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--transcripts", required=True)
    p.add_argument("--prompt", required=True)
    p.add_argument("--output", required=True)
    args = p.parse_args()

    records = json.load(open(args.transcripts))

    findings = defaultdict(lambda: {"count": 0, "timestamps": [], "evidence": []})
    versions = {"current": 0, "older": 0, "unknown": 0}

    for rec in records:
        ts = rec.get("timestamp", "")
        transcript = rec.get("transcript", "")
        version = detect_prompt_version(transcript)
        versions[version] += 1
        rec["_version"] = version

        turns = split_turns(transcript)
        assistant_turns = [t for r, t in turns if r == "assistant"]

        # 1. Romanized Hindi
        for t in assistant_turns:
            if ROMAN_RE.search(t) and not DEVANAGARI_RE.search(t):
                f = findings["romanized_hindi"]
                f["count"] += 1
                if ts not in f["timestamps"]:
                    f["timestamps"].append(ts)
                if len(f["evidence"]) < 5:
                    f["evidence"].append({"ts": ts, "v": version, "text": make_excerpt(t)})
                break
            elif ROMAN_RE.search(t):
                # mixed: still flag if romanized fragment present
                f = findings["romanized_hindi_mixed"]
                f["count"] += 1
                if ts not in f["timestamps"]:
                    f["timestamps"].append(ts)
                if len(f["evidence"]) < 5:
                    f["evidence"].append({"ts": ts, "v": version, "text": make_excerpt(t)})
                break

        # 2. English silence prompt
        for t in assistant_turns:
            if ENGLISH_SILENCE.search(t):
                f = findings["english_silence_prompt"]
                f["count"] += 1
                f["timestamps"].append(ts)
                if len(f["evidence"]) < 5:
                    f["evidence"].append({"ts": ts, "v": version, "text": make_excerpt(t)})
                break

        # 3. Wrong company name
        for t in assistant_turns:
            if WRONG_COMPANY.search(t):
                f = findings["wrong_company_name"]
                f["count"] += 1
                f["timestamps"].append(ts)
                if len(f["evidence"]) < 5:
                    f["evidence"].append({"ts": ts, "v": version, "text": make_excerpt(t)})
                break

        # 4. Digits in responses
        for t in assistant_turns:
            digits = DIGITS_RE.findall(t)
            if digits:
                f = findings["digits_in_response"]
                f["count"] += 1
                if ts not in f["timestamps"]:
                    f["timestamps"].append(ts)
                if len(f["evidence"]) < 5:
                    f["evidence"].append({
                        "ts": ts, "v": version,
                        "digits": digits[:5], "text": make_excerpt(t)
                    })
                break

        # 5. Long responses
        for t in assistant_turns:
            words = t.split()
            if len(words) > 60:
                f = findings["long_response"]
                f["count"] += 1
                if ts not in f["timestamps"]:
                    f["timestamps"].append(ts)
                if len(f["evidence"]) < 5:
                    f["evidence"].append({
                        "ts": ts, "v": version,
                        "words": len(words), "text": make_excerpt(t, 220)
                    })
                break

        # 6. Empty/truncated responses
        for t in assistant_turns:
            if 0 < len(t.strip()) <= 3:
                f = findings["empty_response"]
                f["count"] += 1
                if ts not in f["timestamps"]:
                    f["timestamps"].append(ts)
                if len(f["evidence"]) < 5:
                    f["evidence"].append({"ts": ts, "v": version, "text": repr(t)})
                break

        # 7. Repeated questions (consecutive identical assistant turns)
        for i in range(1, len(assistant_turns)):
            a, b = assistant_turns[i - 1], assistant_turns[i]
            if len(a) > 20 and a == b:
                f = findings["repeated_question"]
                f["count"] += 1
                if ts not in f["timestamps"]:
                    f["timestamps"].append(ts)
                if len(f["evidence"]) < 5:
                    f["evidence"].append({"ts": ts, "v": version, "text": make_excerpt(a)})
                break

        # 8. Blank name handling — double space before जी
        for t in assistant_turns:
            if "  जी" in t or t.startswith(" जी"):
                f = findings["blank_owner_name"]
                f["count"] += 1
                if ts not in f["timestamps"]:
                    f["timestamps"].append(ts)
                if len(f["evidence"]) < 5:
                    f["evidence"].append({"ts": ts, "v": version, "text": make_excerpt(t)})
                break

        # 9. Post-voicemail continuation
        post_vm_assist = 0
        seen_vm = False
        for role, t in turns:
            if any(h in t.lower() for h in VOICEMAIL_HINTS):
                seen_vm = True
                continue
            if seen_vm and role == "assistant":
                post_vm_assist += 1
        if seen_vm and post_vm_assist > 1:
            f = findings["post_voicemail_continuation"]
            f["count"] += 1
            if ts not in f["timestamps"]:
                f["timestamps"].append(ts)
            if len(f["evidence"]) < 5:
                f["evidence"].append({
                    "ts": ts, "v": version,
                    "post_vm_assistant_turns": post_vm_assist,
                })

        # 10. Hallucinated financing
        for t in assistant_turns:
            if HALLUCINATED_FINANCING.search(t):
                f = findings["hallucinated_financing"]
                f["count"] += 1
                if ts not in f["timestamps"]:
                    f["timestamps"].append(ts)
                if len(f["evidence"]) < 5:
                    f["evidence"].append({"ts": ts, "v": version, "text": make_excerpt(t)})
                break

        # 11. Language question repeated
        full_assistant = "\n".join(assistant_turns)
        if len(LANG_QUESTION_RE.findall(full_assistant)) >= 2:
            f = findings["language_question_repeated"]
            f["count"] += 1
            if ts not in f["timestamps"]:
                f["timestamps"].append(ts)
            if len(f["evidence"]) < 5:
                f["evidence"].append({"ts": ts, "v": version, "text": "asked language ≥2x"})

    out = {
        "total_transcripts": len(records),
        "version_split": versions,
        "patterns": dict(findings),
    }
    json.dump(out, open(args.output, "w"), ensure_ascii=False, indent=2)
    print(json.dumps({"output": args.output, "total": len(records), "versions": versions}))


if __name__ == "__main__":
    main()
