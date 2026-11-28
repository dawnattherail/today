#!/usr/bin/env python3
"""Write data/today.json for the self-updating Today box, then commit and push.

Run by the picks thread's scratch job: once at night (phase=night) and after each
track's morning scratch pull (phase=morning).

Usage:
  python3 tools/write_today.py --in selections.json [--push]

selections.json:
{
  "date": "2026-12-12", "date_label": "Saturday, December 12, 2026",
  "phase": "night" | "morning", "updated": "11:40 AM ET",
  "selections": [ {"track": "Belmont", "race": 7, "post": "2:38 PM ET", "horse": "#3 Epitaph",
                   "status": "pre" | "ok" | "new"} ],
  "scratch_notes": ["<b>Fair Grounds</b> Race 7: #12 R T's Gem scratched, so no Blue Ribbon bet in that race."],
  "totals_line": "<b>Birdie's top pick in every race since Oct 25:</b> 552 races, 155 winners (28.1%). Through Nov 26. ",
  "show_url": "https://..."
}

Rules (Chris):
 - One box per Blue Ribbon Selection. A scratched selection is NOT in "selections";
   name it only in scratch_notes.
 - Real picks never go on this public repo before launch day, Dec 11, 2026.
   Before then this script only accepts files marked "sample": true.
"""
import argparse, datetime, json, os, subprocess, sys

LAUNCH = datetime.date(2026, 12, 11)
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REQ = ["date", "date_label", "phase", "selections"]

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="src", required=True)
    ap.add_argument("--push", action="store_true")
    a = ap.parse_args()
    d = json.load(open(a.src))
    for k in REQ:
        if k not in d:
            sys.exit(f"missing field: {k}")
    if d["phase"] not in ("night", "morning"):
        sys.exit("phase must be night or morning")
    for s in d["selections"]:
        for k in ("track", "race", "post", "horse"):
            if k not in s:
                sys.exit(f"selection missing {k}: {s}")
        if s.get("status", "pre") not in ("pre", "ok", "new"):
            sys.exit(f"bad status {s.get('status')} (scratched picks go in scratch_notes only)")
    if datetime.date.today() < LAUNCH and not d.get("sample"):
        sys.exit("Before Dec 11, 2026 only sample data may be published (Chris: samples only until launch).")
    out = os.path.join(REPO, "data", "today.json")
    json.dump(d, open(out, "w"), indent=1, ensure_ascii=False)
    print("wrote", out, len(d["selections"]), "selections")
    if a.push:
        msg = f"Today box: {d['date']} {d['phase']} ({len(d['selections'])} selections)"
        subprocess.run(["git", "-C", REPO, "add", "data/today.json"], check=True)
        r = subprocess.run(["git", "-C", REPO, "commit", "-m", msg], capture_output=True, text=True)
        print(r.stdout.strip() or r.stderr.strip())
        subprocess.run(["git", "-C", REPO, "push", "origin", "HEAD:main"], check=True)
        print("pushed; live within about a minute at https://dawnattherail.github.io/today/data/today.json")

if __name__ == "__main__":
    main()
