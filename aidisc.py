#!/usr/bin/env python3
"""aidisc - write one AI-use disclosure record per video as Markdown.

A CHECKLIST, not legal advice and not a compliance verdict. It never claims a
video is compliant. Stdlib only. Never overwrites an existing record.

Usage:
  python aidisc.py --out records --video-id ep-001 --title "Night Rain" \
      --tool "SDXL 1.0 (local)" --ai-used --altered --realistic --disclosure-applied

Flags (all optional except --video-id, --title):
  --ai-used              AI generated or meaningfully AI-altered some content
  --altered              AI altered existing footage/audio (vs generated fresh)
  --realistic            the AI content could be mistaken for real people, places or events
  --disclosure-applied   you set the AI-use disclosure in the upload form
Output: <out>/<video-id>.md
"""
import argparse
import datetime as _dt
import os
import re
import sys

DISCLAIMER = (
    "This record is a checklist for the creator's own files. It is not legal advice "
    "and does not state that the video complies with any platform policy."
)


def slugify(text: str) -> str:
    s = re.sub(r"[^A-Za-z0-9._-]+", "-", text.strip()).strip("-.")
    if not s:
        raise ValueError("video-id produces an empty file name")
    return s


def required_disclosure(ai_used: bool, realistic: bool) -> str:
    """Rule of thumb from YouTube's GenAI disclosure help page: disclosure is
    expected for realistic-looking AI content; minor/aesthetic edits and clearly
    non-realistic animation generally need none. Result is a prompt to check, not a verdict."""
    if not ai_used:
        return "no (no AI content recorded)"
    if realistic:
        return "YES - realistic AI content: check the Studio 'AI use' setting"
    return "probably no - non-realistic AI content; re-check the live YouTube help page"


def build_record(video_id, title, tools, ai_used, altered, realistic, applied, today):
    lines = [
        f"# AI disclosure record: {title}",
        "",
        f"- Video ID: `{video_id}`",
        f"- Record date: {today}",
        f"- AI used: {'yes' if ai_used else 'no'}",
        f"- AI altered existing footage or audio: {'yes' if altered else 'no'}",
        f"- Could be mistaken for real people, places or events: {'yes' if realistic else 'no'}",
        f"- Tools / models: {', '.join(tools) if tools else 'none recorded'}",
        f"- Disclosure required (checklist): {required_disclosure(ai_used, realistic)}",
        f"- Disclosure applied in upload form: {'yes' if applied else 'no'}",
    ]
    if ai_used and realistic and not applied:
        lines.append("- ACTION: required disclosure not yet marked as applied; fix before publishing.")
    lines += ["", f"> {DISCLAIMER}", ""]
    return "\n".join(lines)


def write_record(out_dir, video_id, text) -> str:
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, slugify(video_id) + ".md")
    if os.path.exists(path):
        raise FileExistsError(f"refusing to overwrite existing record: {path}")
    with open(path, "x", encoding="utf-8", newline="\n") as f:
        f.write(text)
    return path


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--out", default="records")
    p.add_argument("--video-id", required=True)
    p.add_argument("--title", required=True)
    p.add_argument("--tool", action="append", default=[], help="repeatable")
    p.add_argument("--ai-used", action="store_true")
    p.add_argument("--altered", action="store_true")
    p.add_argument("--realistic", action="store_true")
    p.add_argument("--disclosure-applied", action="store_true")
    a = p.parse_args(argv)
    if a.altered and not a.ai_used:
        p.error("--altered requires --ai-used")
    if a.realistic and not a.ai_used:
        p.error("--realistic requires --ai-used")
    today = _dt.date.today().isoformat()
    text = build_record(a.video_id, a.title, a.tool, a.ai_used, a.altered, a.realistic,
                        a.disclosure_applied, today)
    try:
        path = write_record(a.out, a.video_id, text)
    except FileExistsError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 2
    print(path)
    return 0


if __name__ == "__main__":
    sys.exit(main())
