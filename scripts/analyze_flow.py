#!/usr/bin/env python3
"""Tag each assistant turn with a flow step and compare against the prompt's defined order."""
import argparse
import json
import re
from collections import Counter, defaultdict


STEP_KEYWORDS = [
    ("VOICEMAIL", [r"voicemail", r"after the beep", r"नहीं उठाया", r"callback later"]),
    ("LANG_CHECK", [r"शुरू करने से पहले", r"hindi.*english", r"theek rahegi", r"hindi या english"]),
    ("PLATFORM_SILENCE", [r"are you still there", r"सुन रहे हैं", r"आप वहाँ हैं"]),
    ("IDENTITY_CONFIRM", [r"से बात कर सकता हूँ", r"आप .*से हैं", r"speaking with"]),
    ("TRUST_BUILD", [r"priority dealer", r"priority partner", r"field team"]),
    ("PRODUCT_TEASER", [
        r"lithium-ion batteries",
        r"e-rickshaw.*supply",
        r"trontek",
        r"fifty-?one point two",
    ]),
    ("DISCOVERY", [r"अभी .* काम होता", r"current supplier", r"battery type", r"e-rickshaw या lithium"]),
    ("REQUIREMENTS", [r"voltage की ज़रूरत", r"capacity में", r"monthly approximately"]),
    ("PRODUCT_PRESENT", [r"battery की price", r"warranty.*charger", r"soc meter"]),
    ("OBJECTION_HANDLE", [r"price.*depend", r"bulk pricing", r"competitive pricing", r"दस या ज़्यादा"]),
    ("FIELD_VISIT", [r"field representative", r"visit schedule", r"products दिखाय"]),
    ("WHATSAPP_OFFER", [r"whatsapp पे", r"catalogue भेजूँ"]),
    ("CLOSE", [r"अच्छा दिन हो", r"शुक्रिया sir", r"iTarang याद रख"]),
    ("GREETING_ONLY", [r"^नमस्ते", r"^हेलो", r"^hello"]),
]

DEFINED_ORDER = [
    "GREETING_ONLY",
    "LANG_CHECK",
    "IDENTITY_CONFIRM",
    "TRUST_BUILD",
    "PRODUCT_TEASER",
    "DISCOVERY",
    "REQUIREMENTS",
    "PRODUCT_PRESENT",
    "OBJECTION_HANDLE",
    "FIELD_VISIT",
    "WHATSAPP_OFFER",
    "CLOSE",
]


def split_turns(transcript: str) -> list[tuple[str, str]]:
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
            current_role = "assistant" if role in ("assistant", "agent", "bot", "ai") else "user"
            current_text = [line[m.end():]]
        else:
            current_text.append(line)
    if current_role is not None:
        turns.append((current_role, " ".join(current_text).strip()))
    return turns


def tag_turn(text: str) -> str:
    low = text.lower()
    for label, patterns in STEP_KEYWORDS:
        for p in patterns:
            if re.search(p, low, re.IGNORECASE):
                return label
    return "OTHER"


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--transcripts", required=True)
    p.add_argument("--prompt", required=True)
    p.add_argument("--output", required=True)
    args = p.parse_args()

    records = json.load(open(args.transcripts))

    flow_violations = defaultdict(list)
    step_counts = Counter()
    skipped_steps = Counter()
    sequences = []

    for rec in records:
        ts = rec.get("timestamp", "")
        turns = split_turns(rec.get("transcript", ""))
        assistant_steps = []
        for role, t in turns:
            if role == "assistant" and t:
                step = tag_turn(t)
                assistant_steps.append(step)
                step_counts[step] += 1

        seq = list(dict.fromkeys(assistant_steps))
        sequences.append({"ts": ts, "seq": seq})

        # Check missing key steps when call was substantive (>=4 assistant turns)
        if len(assistant_steps) >= 4:
            for required in ["IDENTITY_CONFIRM", "PRODUCT_TEASER", "DISCOVERY"]:
                if required not in assistant_steps:
                    skipped_steps[required] += 1
                    flow_violations[required].append(ts)

        # Out-of-order: PRODUCT_PRESENT before DISCOVERY
        if "PRODUCT_PRESENT" in assistant_steps and "DISCOVERY" in assistant_steps:
            if assistant_steps.index("PRODUCT_PRESENT") < assistant_steps.index("DISCOVERY"):
                flow_violations["PRESENT_BEFORE_DISCOVERY"].append(ts)

    out = {
        "step_counts": step_counts.most_common(),
        "skipped_required_steps": dict(skipped_steps),
        "flow_violations": {k: len(v) for k, v in flow_violations.items()},
        "violation_examples": {k: v[:5] for k, v in flow_violations.items()},
        "sample_sequences": sequences[:10],
    }
    json.dump(out, open(args.output, "w"), ensure_ascii=False, indent=2)
    print(json.dumps({"output": args.output, "total": len(records)}))


if __name__ == "__main__":
    main()
