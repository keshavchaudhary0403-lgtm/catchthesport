# How to update Catch The Sport

This is the rulebook for anyone (person or scheduled Claude task) updating https://catchthesport.vercel.app.

The site is a single static page. **All content lives in `data.json`.** Committing to `main` redeploys on Vercel in about 30 seconds, and open pages pick up the new data within 20 seconds.

- Edit **only `data.json`**. Never edit `index.html`, `vercel.json`, `flags/` or this file during routine updates.
- Before every commit run `python3 scripts/validate.py` — it must print `OK`.
- Always run `git pull --rebase` right before committing (two scheduled tasks share this repo).

## Audience and priorities

The site is for **Indian sports fans**. Every update should answer: *what is India playing, what's live, what just happened, what's next?*

Coverage priority (highest first):

1. **India national teams** in any sport — cricket (men & women), football, hockey, kabaddi, plus Indian athletes in finals/medal rounds (badminton, tennis, boxing, wrestling, shooting, athletics, chess, archery, weightlifting, table tennis, golf).
2. **Indian leagues** — IPL, WPL, ISL, PKL, Hockey India League, Ranji/Duleep/Vijay Hazare/Syed Mushtaq Ali (knockouts), Durand Cup, Super Cup, IWL, I-League, UTT, PBL, Prime Volleyball.
3. **Indian clubs abroad** — AFC Champions League 2 / Challenge League ties of ISL clubs.
4. **Global events Indian fans follow** — ICC tournaments, big Test/ODI/T20I series, Premier League (top-6 games), Champions League knockouts, La Liga Clásico, F1, tennis Grand Slams (and Indian players anywhere), BWF Super 750/1000, Olympics / Asian Games / Commonwealth Games, FIFA World Cup.

Mark anything involving an Indian team or athlete with `"india": true`. Mark headline fixtures with `"big": true`; medal/final matches with `"gold": true`.

## Rolling window

- `matches`: keep roughly **25–45** items: everything live now, all of today, India results from the last **3 days**, major other results from the last **2 days**, and upcoming fixtures for the next **14 days** (India: all; others: the important ones). Remove older items.
- Cap any single non-India competition at about 6 upcoming items so the grid stays varied.

## `data.json` reference

```jsonc
{
  "lastUpdated": "2026-10-02T15:45:00+05:30",   // MUST change on every edit (IST, ISO format)
  "dayLabel": "Fri 2 Oct · Asian Games Day 13",  // short line shown on the hero card
  "featured": "ag-cricket-final",                // optional: id of the match for the 3D hero card
  "heroFacts": [],                               // optional: [{ "v": "67", "l": "India's Asian Games medals" }] — leave [] for automatic counts
  "matches": [ /* see below */ ],
  "event": { /* optional multi-sport event block, see below */ },
  "competitions": [ { "sport": "Cricket", "name": "India v West Indies", "status": "Live series · till 17 Oct", "live": true, "india": true, "note": "…" } ],
  "feed": [ { "t": "15:42", "tag": "GOLD", "c": "var(--gold)", "m": "Boxing", "text": "…" } ],
  "schedule": [ { "d": "03", "mo": "OCT", "title": "India v West Indies, 3rd ODI", "meta": "Cricket · New Chandigarh", "time": "14:00" } ],
  "players": [ { "i": "SG", "name": "Shubman Gill", "role": "Cricket · ODI captain", "p": "…" } ],
  "videos": [ { "big": "GILL 222\nRECORD", "title": "…", "meta": "…", "len": "12:04", "bg": "#0F766E", "url": "https://youtube.com/…" } ],
  "sources": "Olympics.com, ESPNcricinfo, …"
}
```

### Match object

```jsonc
{
  "id": "ind-wi-odi3",               // unique, stable, lowercase
  "sport": "Cricket",                // Cricket, Football, Hockey, Kabaddi, Badminton, Tennis, Athletics, Boxing, Wrestling, Shooting, Archery, Chess, Table tennis, Golf, Formula 1, Basketball, …
  "comp": "India v West Indies",     // competition / series name
  "round": "3rd ODI",                // stage, match number, weight class …
  "st": "upcoming",                  // "upcoming" | "live" | "result"
  "a": ["IND", "India", ""],         // [code, display name, score, optional colour]
  "b": ["WI", "West Indies", "", "#7B1E3A"],
  "when": "2026-10-03T14:00:00+05:30", // IST datetime, or just "2026-10-03" if time unknown
  "status": "34.2 ov",               // live only: overs / minute / set score
  "win": "a",                        // results only: "a" or "b" (omit for draws)
  "day": "3 Oct",                    // results only: short date label
  "recent": true,                    // results only: also show under "Live & today"
  "india": true, "big": true, "gold": false,
  "note": "One factual line: scorers, top performers, context.",
  "venue": "New Chandigarh",
  "watch": "JioHotstar"              // broadcaster in India, only if confirmed
}
```

Codes: use 3-letter country codes for national teams (`IND`, `PAK`, `AUS`, `ENG`, `BRA` …) — they show real flags (see the list in `flags/`, mapped in `index.html` `FLAGMAP`). `WI` (West Indies) and all clubs get a coloured badge: give clubs a short code (`MCFC`, `BFC`, `LIV`) and their main colour as the 4th element. Use `TBC` when an opponent is unknown.

Scores are free text: cricket `"406/2"` or `"245/8 (50)"`; football `"2"`; tennis `"6-4 7-5"`; individual events the athlete's result, or `"Won"` if only the outcome is known.

Status changes: when a match starts set `"st": "live"` with a `status`; when it ends set `"st": "result"`, fill both scores, `win`, `day`, `recent: true`. If a match has started but you can't find its score, leave it `upcoming` — the site labels it "UNDER WAY" automatically.

### Feed

Newest first, at most ~15 entries, India first in spirit. `t` is `"HH:MM"` IST for today, or a short date for older items. `tag`: GOLD / SILVER / BRONZE / WIN / LOSS / DRAW / FINAL / LIVE / OUT / NEWS. `c`: `var(--gold)`, `var(--silver)`, `var(--bronze)`, `var(--win)`, `var(--accent)`, `var(--live-text)`.

### Schedule

India's next ~10 events in time order (`time` "HH:MM" IST or "TBC"); drop finished ones.

### Event block (multi-sport games)

Use `event` only while a multi-sport event India competes in is on (Asian Games, Commonwealth Games, Olympics, SAF Games …):

```jsonc
"event": {
  "name": "Aichi-Nagoya 2026 Asian Games", "short": "Asian Games",
  "eyebrow": "Featured event · 20th Asian Games",
  "desc": "…", "statusText": "Live · closes 4 Oct, Nagoya",
  "stats": [ { "v": "45", "l": "Nations" }, { "v": "11 · 23 · 33", "l": "India G · S · B" } ],
  "medalAsOf": "…", "medalNote": "optional note under the table",
  "medalTable": [ { "code": "CHN", "name": "China", "g": 154, "s": 71, "b": 63 } ],   // top 9 + India
  "indiaGolds": [ { "sport": "Archery", "event": "…", "who": "…", "isNew": true } ],
  "indiaToday": [ { "medal": "gold", "sport": "…", "event": "…", "who": "…" } ],
  "indiaYesterday": [ … ]
}
```

After the closing ceremony: set `statusText` to "Concluded — final standings", update the final table, keep the block for **3 days**, then delete the whole `event` key. Event matches use `"comp": "Asian Games"` (or the event's name).

## Research rules

- Use several sources and search phrasings. Results often appear first in the **opponent's or host's language** — search Korean, Chinese, Japanese, Malay, Arabic, Urdu, Spanish, Portuguese etc. as relevant (e.g. "아시안게임 양궁 결승 인도", "亚运会 决赛 印度").
- If the built-in browser on Keshav's computer is available, **search Google** there (read the AI Overview and Top stories, then confirm in an article). Cloud runs cannot fetch Google — don't retry it.
- Good sources: ESPNcricinfo, Cricbuzz, BCCI, Olympics.com, Khel Now, The Bridge, Sportstar, Indian Express, Hindustan Times, Times of India, NDTV Sports, ANI, PTI, Outlook, Business Standard, AIFF, Hockey India, ISL, PKL, BWF, ATP/WTA, Premier League, UEFA, F1, Wikipedia, plus foreign outlets (Yonhap, Chosun, Xinhua, NHK, Kyodo, Dawn, Malay Mail …).
- **Never invent** scores, names, times or venues. Use `TBC` / leave blank when unknown. When sources disagree, use the most recent timestamped report.
- Times are always **IST**.
- Keep notes short, neutral and factual. No betting odds.
