#!/usr/bin/env python3
"""Fetch Saptarshi's real GitHub contribution calendar and derive profile stats."""
import datetime as dt
import json
import os
import re
import sys
from pathlib import Path

import requests
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
PROFILE = json.loads((ROOT / "config/profile.json").read_text())
USERNAME = os.getenv("GH_PROFILE_USER", PROFILE["github_username"])
OUT_PATH = ROOT / "data/contributions.json"
URL = f"https://github.com/users/{USERNAME}/contributions"


def fetch_days():
    response = requests.get(URL, headers={"User-Agent": "saptarshi-profile-readme/1.0"}, timeout=30)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    cells = soup.select("td.ContributionCalendar-day")
    if not cells:
        raise RuntimeError("GitHub contribution calendar markup was not found.")
    days = []
    for td in cells:
        date = td.get("data-date")
        if not date:
            continue
        tooltip = soup.find("tool-tip", attrs={"for": td.get("id")})
        text = tooltip.get_text(" ", strip=True) if tooltip else ""
        if re.search(r"no contributions", text, re.I):
            count = 0
        else:
            match = re.match(r"(\d+)", text)
            count = int(match.group(1)) if match else 0
        days.append({"date": date, "count": count, "level": int(td.get("data-level") or 0)})
    return sorted(days, key=lambda x: x["date"])


def streak(days):
    idx = len(days) - 1
    if idx >= 0 and days[idx]["count"] == 0:
        idx -= 1
    length = 0
    while idx >= 0 and days[idx]["count"] > 0:
        length += 1
        idx -= 1
    if not length:
        return {"length": 0, "start": None, "end": None}
    return {"length": length, "start": days[idx + 1]["date"], "end": days[idx + length]["date"]}


def longest(days):
    best = run = 0
    best_start = best_end = None
    start = None
    for i, day in enumerate(days):
        if day["count"]:
            if run == 0:
                start = i
            run += 1
            if run > best:
                best = run
                best_start, best_end = days[start]["date"], day["date"]
        else:
            run = 0
    return {"length": best, "start": best_start, "end": best_end}


def build(days):
    total = sum(d["count"] for d in days)
    active = sum(d["count"] > 0 for d in days)
    best = max(days, key=lambda d: d["count"]) if days else {"date": None, "count": 0}
    monthly = {}
    for d in days:
        key = d["date"][:7]
        monthly[key] = monthly.get(key, 0) + d["count"]
    return {
        "username": USERNAME,
        "generated_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "range": {"start": days[0]["date"], "end": days[-1]["date"]},
        "total_contributions": total,
        "active_days": active,
        "avg_per_active_day": round(total / active, 1) if active else 0,
        "current_streak": streak(days),
        "longest_streak": longest(days),
        "best_day": best,
        "monthly": [{"month": k, "total": v} for k, v in sorted(monthly.items())],
        "days": days,
    }


if __name__ == "__main__":
    days = fetch_days()
    data = build(days)
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(json.dumps(data, indent=2))
    print(f"Updated {OUT_PATH}: {data['total_contributions']} contributions")
