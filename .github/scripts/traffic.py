#!/usr/bin/env python3
"""Build a real visitor count for the profile README.

Why not a hit-counter badge: GitHub proxies every README image through Camo, so
a counter service only ever sees GitHub's proxy, never the visitor. It cannot
tell your refresh apart from a stranger's first visit. The number it shows is
page hits, and yours are in it.

What this does instead: it reads GitHub's own traffic API, which reports unique
visitors per day per repository - real people, counted once a day no matter how
often they reload. Then it drops your own device from any day you were working
in that repository, so checking your own work never moves the number.

The API only keeps 14 days. This script stores every day permanently in
data/traffic.json, so the total keeps growing and nothing is ever lost.

Standard library only. Runs on a schedule from .github/workflows/traffic.yml.
"""
import json
import os
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
STORE = os.path.join(ROOT, "data", "traffic.json")
README = os.path.join(ROOT, "README.md")
API = "https://api.github.com"

TOKEN = os.environ.get("GH_TOKEN", "")
OWNER = os.environ.get("OWNER", "")
HOME_REPO = os.environ.get("HOME_REPO", "")

# ── settings ─────────────────────────────────────────────────────────────────
# How many devices of your own visit a repo on a day you work in it. Laptop
# only: 1. Laptop and phone: 2. Each one is subtracted from that day's count.
OWN_DEVICES = int(os.environ.get("OWN_DEVICES", "1"))

# Subtract your devices every single day, not only days you pushed something.
# Turn this on if you browse your repos far more often than you commit.
DISCOUNT_EVERY_DAY = os.environ.get("DISCOUNT_EVERY_DAY", "false").lower() == "true"

# What the badge says.
BADGE_LABEL = os.environ.get("BADGE_LABEL", "VISITORS")
BADGE_COLOUR = "5A6288"

START, END = "<!-- VISITORS:START -->", "<!-- VISITORS:END -->"


def api(path, token=TOKEN):
    req = urllib.request.Request(API + path, headers={
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": "profile-traffic-counter",
        **({"Authorization": f"Bearer {token}"} if token else {}),
    })
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def repos_to_track():
    """Every public repo we can read traffic for.

    The built-in GITHUB_TOKEN only reaches the repo the workflow runs in. Add a
    personal access token as the INSIGHTS_TOKEN secret and every public repo is
    counted instead. Either way the script works.
    """
    names = [HOME_REPO]
    if os.environ.get("WIDE_TOKEN"):
        try:
            page, found = 1, []
            while True:
                batch = api(f"/users/{OWNER}/repos?per_page=100&type=owner&page={page}")
                if not batch:
                    break
                found += [r["name"] for r in batch if not r.get("fork")]
                page += 1
                if page > 5:
                    break
            names = sorted(set(found) | {HOME_REPO})
        except urllib.error.HTTPError as e:
            print(f"Could not list repos ({e.code}) - tracking {HOME_REPO} only")
    return [n for n in names if n]


def owner_active_days():
    """Days the owner worked in a repo, as {repo: {date, ...}}.

    A push, an issue, a comment - if you touched a repo that day you also looked
    at it. Those are the days your own device is removed from the count.
    """
    active = {}
    try:
        for page in (1, 2, 3):
            events = api(f"/users/{OWNER}/events/public?per_page=100&page={page}")
            if not events:
                break
            for ev in events:
                if ev.get("actor", {}).get("login", "").lower() != OWNER.lower():
                    continue
                repo = ev.get("repo", {}).get("name", "").split("/")[-1]
                day = str(ev.get("created_at", ""))[:10]
                if repo and day:
                    active.setdefault(repo, set()).add(day)
    except urllib.error.HTTPError as e:
        print(f"Could not read owner activity ({e.code}) - keeping every day")
    return active


def load():
    if os.path.exists(STORE):
        with open(STORE, encoding="utf-8") as f:
            return json.load(f)
    return {"days": {}, "totals": {}, "updated": None}


def save(data):
    os.makedirs(os.path.dirname(STORE), exist_ok=True)
    with open(STORE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, sort_keys=True)
        f.write("\n")


def collect(data):
    """Merge the last 14 days from the API into the permanent store."""
    token = os.environ.get("WIDE_TOKEN") or TOKEN
    reached = 0
    for repo in repos_to_track():
        try:
            views = api(f"/repos/{OWNER}/{repo}/traffic/views", token)
        except urllib.error.HTTPError as e:
            # 403 just means this token has no push access to that repo.
            print(f"  {repo}: no traffic access ({e.code})")
            continue
        reached += 1
        bucket = data["days"].setdefault(repo, {})
        for day in views.get("views", []):
            date = str(day.get("timestamp", ""))[:10]
            if date:
                bucket[date] = {"count": int(day.get("count", 0)),
                                "uniques": int(day.get("uniques", 0))}
        print(f"  {repo}: {len(views.get('views', []))} days merged")
    if reached == 0:
        print("No repository traffic could be read - nothing written")
        return False
    return True


def totals(data):
    """Add up every stored day, minus your own device on days you were there."""
    active = owner_active_days()
    visitors = views = mine = 0
    for repo, days in data["days"].items():
        was_here = active.get(repo, set())
        for date, d in days.items():
            u, c = int(d.get("uniques", 0)), int(d.get("count", 0))
            drop = OWN_DEVICES if (DISCOUNT_EVERY_DAY or date in was_here) else 0
            drop = min(drop, u)
            mine += drop
            visitors += u - drop
            views += max(c - drop, 0)
    return {"visitors": visitors, "views": views, "self_excluded": mine,
            "repos": len(data["days"]),
            "since": min((d for days in data["days"].values() for d in days), default="")}


def badge(t):
    label = BADGE_LABEL.replace(" ", "_")
    since = f" since {t['since']}" if t["since"] else ""
    return (f'<img src="https://img.shields.io/badge/{label}-{t["visitors"]}-'
            f'{BADGE_COLOUR}?style=for-the-badge&labelColor=160F3C" '
            f'alt="{t["visitors"]} unique visitors{since}, my own visits not counted" />')


def write_readme(t):
    if not os.path.exists(README):
        return
    doc = open(README, encoding="utf-8").read()
    if START not in doc or END not in doc:
        print("README has no VISITORS markers - badge not updated")
        return
    new = doc[:doc.index(START) + len(START)] + "\n" + badge(t) + "\n" + doc[doc.index(END):]
    open(README, "w", encoding="utf-8").write(new)


def main():
    if not OWNER or not HOME_REPO:
        sys.exit("OWNER and HOME_REPO must be set")
    data = load()
    print(f"Reading traffic for {OWNER}:")
    if not collect(data):
        return
    t = totals(data)
    data["totals"] = t
    data["updated"] = datetime.now(timezone.utc).isoformat(timespec="seconds")
    save(data)
    write_readme(t)
    print(f"\n{t['visitors']} unique visitors across {t['repos']} repo(s), "
          f"{t['views']} views, {t['self_excluded']} of my own visits removed.")


if __name__ == "__main__":
    main()
