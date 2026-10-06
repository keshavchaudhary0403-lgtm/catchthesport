#!/usr/bin/env python3
"""Check data.json before committing. Prints OK or the problems found (exit code 1)."""
import json
import re
import sys
from datetime import datetime

errors = []
try:
    d = json.load(open("data.json", encoding="utf-8"))
except Exception as e:  # noqa: BLE001
    print("data.json is not valid JSON:", e)
    sys.exit(1)

def need(obj, key, typ, where):
    if key not in obj:
        errors.append(f"{where}: missing '{key}'")
        return False
    if not isinstance(obj[key], typ):
        errors.append(f"{where}: '{key}' should be {typ.__name__ if isinstance(typ, type) else typ}")
        return False
    return True

ISO = re.compile(r"^\d{4}-\d{2}-\d{2}(T\d{2}:\d{2}(:\d{2})?\+05:30)?$")

need(d, "lastUpdated", str, "root")
try:
    datetime.fromisoformat(d.get("lastUpdated", ""))
    from datetime import timezone, timedelta
    lu = datetime.fromisoformat(d.get("lastUpdated", ""))
    if lu > datetime.now(timezone.utc) + timedelta(minutes=2):
        errors.append("root: lastUpdated is in the future — use the real current IST time: TZ=Asia/Kolkata date +%Y-%m-%dT%H:%M:%S+05:30")
except ValueError:
    errors.append("root: lastUpdated must look like 2026-10-02T15:45:00+05:30")
for k in ("matches", "feed", "schedule"):
    need(d, k, list, "root")

ids = set()
for i, m in enumerate(d.get("matches", [])):
    w = f"matches[{i}] ({m.get('id', '?')})"
    for k in ("id", "sport", "st"):
        need(m, k, str, w)
    if m.get("id") in ids:
        errors.append(f"{w}: duplicate id")
    ids.add(m.get("id"))
    if m.get("st") not in ("upcoming", "live", "result"):
        errors.append(f"{w}: st must be upcoming, live or result")
    for side in ("a", "b"):
        t = m.get(side)
        if not (isinstance(t, list) and 2 <= len(t) <= 4 and all(isinstance(x, str) for x in t)):
            errors.append(f"{w}: '{side}' must be [code, name, score(, colour)] strings")
    if m.get("when") and not ISO.match(m["when"]):
        errors.append(f"{w}: when must be 2026-10-03 or 2026-10-03T14:00:00+05:30")
    if m.get("st") == "upcoming" and not m.get("when"):
        errors.append(f"{w}: upcoming match needs 'when'")
    w_ = m.get("watch")
    if w_ is not None and not (isinstance(w_, str) or (isinstance(w_, list) and all(isinstance(x, str) or (isinstance(x, dict) and isinstance(x.get("n"), str)) for x in w_))):
        errors.append(f"{w}: watch must be a list like [\"Star Sports 1\", \"JioHotstar\"] or [{{'n': 'YouTube', 'u': 'https://…'}}]")
    if m.get("st") == "live" and not ((len(m.get("a", [])) > 2 and m["a"][2]) or (len(m.get("b", [])) > 2 and m["b"][2])):
        print(f"warning: {w} is live but has no score — add the current score (and scoreAt)")
    if m.get("st") in ("live", "upcoming") and m.get("india") and not m.get("watch"):
        print(f"warning: {w} has no 'watch' (TV channel / streaming app in India) — add it once confirmed")
    if m.get("win") not in (None, "a", "b"):
        errors.append(f"{w}: win must be 'a' or 'b'")

if d.get("featured") and d["featured"] not in ids:
    errors.append("root: featured id not found in matches")

for i, f in enumerate(d.get("feed", [])):
    for k in ("t", "tag", "c", "m", "text"):
        need(f, k, str, f"feed[{i}]")
for i, s in enumerate(d.get("schedule", [])):
    for k in ("d", "mo", "title", "meta", "time"):
        need(s, k, str, f"schedule[{i}]")

def check_src(obj, where):
    for s in obj.get("src", []) or []:
        if not (isinstance(s, dict) and isinstance(s.get("u"), str) and s["u"].startswith("http")):
            errors.append(f"{where}: src entries need {{'t': title, 'u': 'https://…'}}")

for i, m in enumerate(d.get("matches", [])):
    check_src(m, f"matches[{i}]")
for i, f in enumerate(d.get("feed", [])):
    check_src(f, f"feed[{i}]")
    if f.get("match") and f["match"] not in ids:
        errors.append(f"feed[{i}]: match id '{f['match']}' not found")
for i, s in enumerate(d.get("schedule", [])):
    if s.get("match") and s["match"] not in ids:
        errors.append(f"schedule[{i}]: match id '{s['match']}' not found")
for i, c in enumerate(d.get("competitions", [])):
    check_src(c, f"competitions[{i}]")

ev = d.get("event")
if ev is not None:
    need(ev, "name", str, "event")
    if need(ev, "medalTable", list, "event"):
        for i, r in enumerate(ev["medalTable"]):
            for k in ("g", "s", "b"):
                if not isinstance(r.get(k), int):
                    errors.append(f"event.medalTable[{i}]: '{k}' must be a whole number")
    if ev.get("medalChecked"):
        try:
            from datetime import timezone, timedelta
            if datetime.fromisoformat(ev["medalChecked"]) > datetime.now(timezone.utc) + timedelta(minutes=2):
                errors.append("event.medalChecked is in the future — use the real IST time")
        except ValueError:
            errors.append("event.medalChecked must look like 2026-10-02T15:45:00+05:30")
    meds = ev.get("indiaMedals")
    ind = next((r for r in ev.get("medalTable", []) if r.get("code") == "IND"), None)
    if isinstance(meds, list) and ind:
        for i, x in enumerate(meds):
            if x.get("medal") not in ("gold", "silver", "bronze"):
                errors.append(f"event.indiaMedals[{i}]: medal must be gold, silver or bronze")
            check_src(x, f"event.indiaMedals[{i}]")
        for col, k in (("gold", "g"), ("silver", "s"), ("bronze", "b")):
            n = sum(1 for x in meds if x.get("medal") == col)
            if n != ind[k]:
                print(f"warning: indiaMedals has {n} {col} but India's table row says {ind[k]} — add the missing medal(s)")

if errors:
    print("\n".join(errors))
    sys.exit(1)
print(f"OK — {len(d['matches'])} matches, {len(d['feed'])} feed items, {len(d['schedule'])} schedule rows")
