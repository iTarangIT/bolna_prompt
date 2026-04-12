#!/usr/bin/env python3
"""Fetch ElevenLabs call/TTS history and convert to the bolna transcript record schema.

Two data sources are supported:

1. **convai** — ElevenLabs Conversational AI conversations
   GET /v1/convai/conversations           (list, paginated by `next_cursor`)
   GET /v1/convai/conversations/{id}      (per-conversation transcript)
   Requires the `convai_read` permission on the API key.

2. **tts_history** — ElevenLabs TTS generation history
   GET /v1/history                        (list, paginated by `last_history_item_id`)
   Each item is a single TTS synthesis = one assistant turn from a Bolna call.
   Requires the `speech_history_read` permission on the API key.

The script reads the API key from the env var `ELEVENLABS_API_KEY`. If not set,
it tries to read it from a `.env` file in the current working directory
(simple `KEY=VALUE` parser, no shell expansion).

Output: a JSON array of records matching the bolna transcript schema:
    { "timestamp", "lead_id", "direction", "transcript", "summary", "source" }

If the API key is missing or lacks permissions, the script writes an empty
array AND a sibling `<output>.error.json` describing the failure, so the
calling skill can continue gracefully and surface the issue to the user.
"""
import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

API_BASE = "https://api.elevenlabs.io"


def load_api_key() -> str | None:
    key = os.environ.get("ELEVENLABS_API_KEY")
    if key:
        return key.strip()
    env_path = Path.cwd() / ".env"
    if env_path.exists():
        for line in env_path.read_text().splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" in line:
                k, _, v = line.partition("=")
                if k.strip() == "ELEVENLABS_API_KEY":
                    return v.strip().strip('"').strip("'")
    return None


def http_get(url: str, api_key: str, timeout: int = 30) -> tuple[int, dict | None, str]:
    """Returns (status_code, parsed_json_or_none, raw_body)."""
    req = urllib.request.Request(url, headers={"xi-api-key": api_key, "accept": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            body = resp.read().decode("utf-8", errors="replace")
            try:
                return resp.status, json.loads(body), body
            except json.JSONDecodeError:
                return resp.status, None, body
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        try:
            return e.code, json.loads(body), body
        except json.JSONDecodeError:
            return e.code, None, body
    except urllib.error.URLError as e:
        return 0, None, f"network error: {e}"


def epoch_to_iso(epoch: int | float | None) -> str:
    if not epoch:
        return ""
    try:
        return datetime.fromtimestamp(int(epoch), tz=timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    except Exception:
        return ""


def fetch_convai_conversations(api_key: str, limit: int) -> tuple[list[dict], dict | None]:
    records: list[dict] = []
    cursor: str | None = None
    fetched = 0
    while fetched < limit:
        page_size = min(100, limit - fetched)
        params = {"page_size": str(page_size)}
        if cursor:
            params["cursor"] = cursor
        url = f"{API_BASE}/v1/convai/conversations?{urllib.parse.urlencode(params)}"
        status, data, raw = http_get(url, api_key)
        if status != 200 or not isinstance(data, dict):
            return records, {"endpoint": "list_conversations", "status": status, "body": raw[:500]}
        items = data.get("conversations") or data.get("history") or []
        if not items:
            break
        for item in items:
            conv_id = item.get("conversation_id") or item.get("id")
            if not conv_id:
                continue
            detail_url = f"{API_BASE}/v1/convai/conversations/{conv_id}"
            d_status, detail, d_raw = http_get(detail_url, api_key)
            if d_status != 200 or not isinstance(detail, dict):
                # Skip this one but keep going
                continue
            transcript_lines: list[str] = []
            for turn in detail.get("transcript", []) or []:
                role = turn.get("role", "").lower()
                tag = "assistant" if role in ("agent", "assistant", "ai") else "user"
                msg = turn.get("message") or turn.get("text") or ""
                if msg:
                    transcript_lines.append(f"{tag}: {msg}")
            records.append({
                "timestamp": epoch_to_iso(item.get("start_time_unix_secs")),
                "lead_id": item.get("conversation_id", ""),
                "direction": detail.get("metadata", {}).get("call_direction", "outbound"),
                "transcript": "\n".join(transcript_lines),
                "summary": detail.get("analysis", {}).get("transcript_summary", "") if isinstance(detail.get("analysis"), dict) else "",
                "source": "elevenlabs_convai",
            })
            fetched += 1
            if fetched >= limit:
                break
            time.sleep(0.05)  # gentle on rate limits
        cursor = data.get("next_cursor")
        if not cursor or not data.get("has_more", False):
            break
    return records, None


def fetch_tts_history(api_key: str, limit: int) -> tuple[list[dict], dict | None]:
    """TTS history doesn't contain user turns — it's just synthesized audio text.

    We bucket consecutive items from the same voice within a 5-minute window into
    a single 'call' for analysis purposes. This is a heuristic; ElevenLabs doesn't
    natively expose call boundaries via the TTS history API.
    """
    items: list[dict] = []
    last_id: str | None = None
    fetched = 0
    while fetched < limit:
        page_size = min(1000, limit - fetched)
        params = {"page_size": str(page_size)}
        if last_id:
            params["start_after_history_item_id"] = last_id
        url = f"{API_BASE}/v1/history?{urllib.parse.urlencode(params)}"
        status, data, raw = http_get(url, api_key)
        if status != 200 or not isinstance(data, dict):
            return [], {"endpoint": "tts_history", "status": status, "body": raw[:500]}
        history = data.get("history") or []
        if not history:
            break
        items.extend(history)
        fetched += len(history)
        if not data.get("has_more"):
            break
        last_id = data.get("last_history_item_id")
        if not last_id:
            break
        time.sleep(0.05)

    items.sort(key=lambda x: x.get("date_unix") or 0)
    records: list[dict] = []
    current: list[dict] | None = None
    last_voice = None
    last_ts = 0
    BUCKET_GAP_SECS = 5 * 60
    for item in items:
        voice = item.get("voice_id") or item.get("voice_name") or ""
        ts = item.get("date_unix") or 0
        if (
            current is None
            or voice != last_voice
            or (ts - last_ts) > BUCKET_GAP_SECS
        ):
            if current:
                records.append(_bucket_to_record(current))
            current = []
        current.append(item)
        last_voice = voice
        last_ts = ts
    if current:
        records.append(_bucket_to_record(current))
    return records, None


def _bucket_to_record(items: list[dict]) -> dict:
    first = items[0]
    transcript_lines = [f"assistant: {it.get('text', '').strip()}" for it in items if it.get("text")]
    return {
        "timestamp": epoch_to_iso(first.get("date_unix")),
        "lead_id": first.get("history_item_id", ""),
        "direction": "outbound",
        "transcript": "\n".join(transcript_lines),
        "summary": f"TTS-history bucket: {len(items)} synthesis events, voice={first.get('voice_name', '')}",
        "source": "elevenlabs_tts_history",
    }


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--mode", required=True, choices=["convai", "tts_history", "both"])
    p.add_argument("--limit", type=int, default=500, help="Max records to fetch (per source)")
    p.add_argument("--output", required=True)
    args = p.parse_args()

    api_key = load_api_key()
    if not api_key:
        err = {"error": "missing_api_key", "message": "Set ELEVENLABS_API_KEY env var or add it to .env"}
        Path(args.output).write_text(json.dumps([]))
        Path(args.output + ".error.json").write_text(json.dumps(err, indent=2))
        print(json.dumps({"output": args.output, "count": 0, "error": "missing_api_key"}))
        sys.exit(0)

    all_records: list[dict] = []
    errors: list[dict] = []

    if args.mode in ("convai", "both"):
        recs, err = fetch_convai_conversations(api_key, args.limit)
        all_records.extend(recs)
        if err:
            errors.append({"source": "convai", **err})

    if args.mode in ("tts_history", "both"):
        recs, err = fetch_tts_history(api_key, args.limit)
        all_records.extend(recs)
        if err:
            errors.append({"source": "tts_history", **err})

    Path(args.output).write_text(json.dumps(all_records, ensure_ascii=False, indent=2))
    if errors:
        Path(args.output + ".error.json").write_text(json.dumps(errors, indent=2))

    print(json.dumps({
        "output": args.output,
        "count": len(all_records),
        "errors": errors,
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
