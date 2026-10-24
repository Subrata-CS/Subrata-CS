#!/usr/bin/env python3
"""Keeps the profile README in sync with publications.json.

    python .github/scripts/profile.py build            rewrite README tables
    python .github/scripts/profile.py add-paper < body add one paper from an issue form
    python .github/scripts/profile.py add-news  < body add one news line from an issue form

publications.json is the single source of truth. The website
(subrata-cs.github.io) reads the same file, so one update changes both.
Standard library only.
"""
import json
import os
import re
import sys
from datetime import date

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA = os.path.join(ROOT, "publications.json")
README = os.path.join(ROOT, "README.md")
ME = "Subrata Pramanik"          # bolded automatically in every author list
NEWS_SHOWN = 3                   # newest N news lines on the README
MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
          "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
EMPTY = {"", "_no response_", "none", "-", "n/a"}


# ───────────────────────────────────────────────────────────── helpers ──
def load():
    with open(DATA, encoding="utf-8") as f:
        data = json.load(f)
    data.setdefault("publications", [])
    data.setdefault("news", [])
    data.setdefault("awards", [])
    data.setdefault("service", [])
    return data


def save(data):
    data["publications"].sort(key=lambda p: (-int(p.get("year", 0)), p.get("title", "").lower()))
    data["news"].sort(key=lambda n: n.get("date", ""), reverse=True)
    data["awards"].sort(key=lambda a: str(a.get("year", "")), reverse=True)
    with open(DATA, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")


def cell(s):
    """Make text safe inside a Markdown table cell."""
    return str(s).replace("|", "\\|").replace("\n", " ").strip()


def bold_me(authors):
    return authors.replace(ME, f"**{ME}**") if authors else ""


def pretty_date(d):
    m = re.fullmatch(r"(\d{4})-(\d{2})", d or "")
    return f"{MONTHS[int(m.group(2)) - 1]} {m.group(1)}" if m else d


def replace_block(doc, name, body):
    start, end = f"<!-- {name}:START -->", f"<!-- {name}:END -->"
    if start not in doc or end not in doc:
        print(f"README has no {name} markers; skipped")
        return doc
    pre, rest = doc.split(start, 1)
    _, post = rest.split(end, 1)
    return f"{pre}{start}\n{body}\n{end}{post}"


# ─────────────────────────────────────────────────────────────── build ──
def render_publications(pubs):
    if not pubs:
        return "\nPapers under review, coming soon.\n"
    rows = ["", "| Year | Paper | Venue | Links |", "|:---:|:---|:---:|:---:|"]
    for p in pubs:
        title = cell(p["title"])
        paper = f"**[{title}]({p['link']})**" if p.get("link") else f"**{title}**"
        if p.get("authors"):
            paper += f"<br/><sub>{cell(bold_me(p['authors']))}</sub>"
        venue = cell(p.get("venue", ""))
        if p.get("note"):
            venue += f"<br/><sub>{cell(p['note'])}</sub>"
        links = []
        if p.get("link"):
            links.append(f"[Paper]({p['link']})")
        if p.get("code"):
            links.append(f"[Code]({p['code']})")
        rows.append(f"| {p.get('year', '')} | {paper} | {venue} | {' · '.join(links)} |")
    return "\n".join(rows) + "\n"


def render_news(news):
    if not news:
        return ""
    lines = ["", "### News", ""]
    for n in news[:NEWS_SHOWN]:
        lines.append(f"- **{pretty_date(n['date'])}:** {n['text'].strip()}")
    return "\n".join(lines) + "\n"


def build():
    data = load()
    save(data)  # keeps the JSON sorted for the website too
    with open(README, encoding="utf-8") as f:
        doc = f.read()
    doc = replace_block(doc, "PUBLICATIONS", render_publications(data["publications"]))
    doc = replace_block(doc, "NEWS", render_news(data["news"]))
    today = date.today()
    doc = replace_block(doc, "UPDATED", f"<sub>Last updated: {today.day} {today.strftime('%B %Y')}</sub>")
    with open(README, "w", encoding="utf-8") as f:
        f.write(doc)
    print(f"README rebuilt: {len(data['publications'])} papers, {len(data['news'])} news items.")


# ───────────────────────────────────────────────────────── issue forms ──
def parse(body):
    """GitHub issue forms arrive as '### Label' followed by the answer."""
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
    return {k: ("" if v.strip().lower() in EMPTY else v.strip()) for k, v in fields.items()}


def fail(problems):
    print("FAILED\n" + "\n".join("- " + p for p in problems), file=sys.stderr)
    sys.exit(1)


def is_url(s):
    return bool(re.match(r"^https?://\S+$", s))


def add_paper():
    f = parse(sys.stdin.read())
    title, year, venue = f.get("paper title", ""), f.get("year", ""), f.get("venue", "")
    link, code = f.get("paper link", ""), f.get("code link", "")
    image = f.get("teaser image link", "")
    authors, note = f.get("authors", ""), f.get("note", "")

    problems = []
    if not title:
        problems.append("Paper title is empty.")
    if not re.fullmatch(r"(19|20)\d{2}", year):
        problems.append("Year must be four digits, e.g. 2027.")
    if not venue:
        problems.append("Venue is empty (e.g. ICDAR 2027).")
    if not is_url(link):
        problems.append("Paper link must start with https://")
    if code and not is_url(code):
        problems.append("Code link must start with https:// (or leave it empty).")
    if image and not (is_url(image) or re.fullmatch(r"[\w./-]+\.(png|jpe?g|gif|webp|svg)", image, re.I)):
        problems.append("Teaser image must be an https:// link or a path like assets/papers/fig.png.")
    if problems:
        fail(problems)

    data = load()
    if any(p.get("link", "").strip() == link for p in data["publications"]):
        fail(["That paper link is already in the list."])
    entry = {"title": title, "year": int(year), "venue": venue, "link": link}
    if authors:
        entry["authors"] = authors
    if code:
        entry["code"] = code
    if note:
        entry["note"] = note
    if image:
        entry["image"] = image
    data["publications"].append(entry)
    save(data)
    print(f"Added paper: {title} ({venue}, {year}).")


def add_news():
    f = parse(sys.stdin.read())
    when, text = f.get("month", ""), f.get("news", "")
    if not when:
        when = date.today().strftime("%Y-%m")
    problems = []
    if not re.fullmatch(r"(19|20)\d{2}-(0[1-9]|1[0-2])", when):
        problems.append("Month must look like 2026-10 (or be left empty for this month).")
    if not text:
        problems.append("News text is empty.")
    if problems:
        fail(problems)
    data = load()
    data["news"].append({"date": when, "text": text.replace("\n", " ")})
    save(data)
    print(f"Added news for {pretty_date(when)}.")


def add_award():
    f = parse(sys.stdin.read())
    year, text = f.get("year", ""), f.get("award", "")
    problems = []
    if not re.fullmatch(r"(19|20)\d{2}", year):
        problems.append("Year must be four digits, e.g. 2027.")
    if not text:
        problems.append("Award text is empty.")
    if problems:
        fail(problems)
    data = load()
    data["awards"].append({"year": int(year), "text": text.replace("\n", " ")})
    save(data)
    print(f"Added award ({year}).")


def add_service():
    f = parse(sys.stdin.read())
    text = f.get("service", "")
    if not text:
        fail(["Service text is empty."])
    data = load()
    if text in data["service"]:
        fail(["That line is already in the list."])
    data["service"].append(text.replace("\n", " "))
    save(data)
    print("Added service line.")


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "build"
    {"build": build, "add-paper": add_paper, "add-news": add_news,
     "add-award": add_award, "add-service": add_service}[cmd]()
