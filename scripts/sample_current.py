#!/usr/bin/env python3
"""Dump full transcripts that match current-prompt format (assistant:/user:) for LLM review."""
import json
import re
import sys

records = json.load(open(sys.argv[1]))
out = []
for rec in records:
    t = rec.get("transcript", "")
    if re.search(r"^assistant\s*:", t, re.MULTILINE | re.IGNORECASE):
        out.append(rec)
print(f"# {len(out)} current-prompt transcripts\n")
for i, rec in enumerate(out, 1):
    print(f"=== [{i}] {rec.get('timestamp')} ===")
    print(rec.get("transcript", "")[:2500])
    print()
