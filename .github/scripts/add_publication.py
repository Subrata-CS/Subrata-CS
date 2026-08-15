#!/usr/bin/env python3
"""Append one publication from a GitHub issue form to publications.json.

The issue body arrives on stdin. GitHub issue forms render as:

    ### Type

    conference

    ### Year

    2026

Nothing here needs installing - standard library only.
"""
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA = os.path.join(ROOT, "publications.json")
VALID_TYPES = {"conference", "journal", "preprint", "workshop", "thesis"}


def parse(body):
    """Map every '### Heading' to the text under it."""
    fields, key, buf = {}, None, []
    for line in body.replace("\r\n", "\n").split("\n"):
        head = re.match(r"^###\s+(.+?)\s*$", line)
        if head:
            if key:
                fields[key] = "\n".join(buf).strip()
            key, buf = head.group(1).strip().lower(), []
        elif key:
            buf.append(line)
    if key:
        fields[key] = "\n".join(buf).strip()
    return fields


def main():
    fields = parse(sys.stdin.read())

    kind = fields.get("type", "").strip().lower()
    year = fields.get("year", "").strip()
    title = fields.get("paper name", "").strip()
    link = fields.get("link", "").strip()

    problems = []
    if kind not in VALID_TYPES:
        problems.append(f"Type must be one of: {', '.join(sorted(VALID_TYPES))}.")
    if not re.fullmatch(r"(19|20)\d{2}", year):
        problems.append("Year must be a four-digit year, for example 2026.")
    if not title or title.lower() in {"_no response_", "none"}:
        problems.append("Paper name is empty.")
    if not re.match(r"^https?://\S+$", link):
        problems.append("Link must start with http:// or https://.")
    if problems:
        print("FAILED\n" + "\n".join("- " + p for p in problems), file=sys.stderr)
        sys.exit(1)

    with open(DATA, encoding="utf-8") as f:
        data = json.load(f)
    items = data["publications"] if isinstance(data, dict) else data

    if any(str(i.get("link", "")).strip() == link for i in items):
        print("FAILED\n- That link is already in the table.", file=sys.stderr)
        sys.exit(1)

    items.append({"type": kind, "year": int(year), "title": title, "link": link})
    items.sort(key=lambda i: (-int(i.get("year", 0)), str(i.get("title", "")).lower()))

    with open(DATA, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")

    print(f"Added: {title} ({year}, {kind}) - {len(items)} papers now in the table.")


if __name__ == "__main__":
    main()
