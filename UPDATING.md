# How to update Catch The Sport

This is the rulebook for anyone (person or scheduled Claude task) updating https://catchthesport.vercel.app.

The site is a single static page. **All content lives in `data.json`.** Committing to `main` redeploys on Vercel in about 30 seconds, and open pages pick up the new data within 20 seconds.

- Edit **only `data.json`**. Never edit `index.html`, `vercel.json`, `flags/` or this file during routine updates.
- Before every commit run `python3 scripts/validate.py` — it must print `OK`.
- Always run `git pull --rebase` right before committing (two scheduled tasks share this repo).

## Audience and priorities

**India first.** The site serves Indian fans first (a global version comes later). The page sorts India matches above everything else in every tier, the hero tiles count only India ("India live", "India today", "India next 7 days", "Indian events on"), and India results lead the results line. Keep the data India-heavy:

- At least **3 out of 4 matches** should involve an Indian team/athlete or an Indian league (`"india": true`). Non-India matches only when Indian fans genuinely follow them (ICC events, big cricket series, Premier League top-6 games, Champions League knockouts, F1 race, Grand Slam finals) — at most ~8 at a time.
- `"india": true` also covers Indian domestic leagues and tournaments (ISL, I-League, IPL/WPL, PKL, Ranji/Duleep/Vijay Hazare/SMAT, Durand, IFA Shield, Hockey India League, national championships) and Indian clubs abroad.
- Feed: at least two-thirds of items about India/Indian leagues; put India items first when several happen at the same time.
- Competitions: mark Indian ones `"india": true` (they sort first).
- Players: Indian athletes only.


The site is for **Indian sports fans**. Every update should answer: *what is India playing, what's live, what just happened, what's next?*

Coverage priority (highest first):

1. **India national teams** in any sport — cricket (men & women), football, hockey, kabaddi, plus Indian athletes in finals/medal rounds (badminton, tennis, boxing, wrestling, shooting, athletics, chess, archery, weightlifting, table tennis, golf).
2. **Indian leagues** — IPL, WPL, ISL, PKL, Hockey India League, Ranji/Duleep/Vijay Hazare/Syed Mushtaq Ali (knockouts), Durand Cup, Super Cup, IWL, I-League, UTT, PBL, Prime Volleyball.
3. **Indian clubs abroad** — AFC Champions League 2 / Challenge League ties of ISL clubs.
4. **Global events Indian fans follow** — ICC tournaments, big Test/ODI/T20I series, Premier League (top-6 games), Champions League knockouts, La Liga Clásico, F1, tennis Grand Slams (and Indian players anywhere), BWF Super 750/1000, Olympics / Asian Games / Commonwealth Games, FIFA World Cup.

**Report results neutrally.** The site is built for Indian fans but must not hide who won. Record every finished match with both scores and the correct `win` side, including India losses and matches between other countries (finals, medal matches, big league games). Feed items should state India's defeats as plainly as its wins ("India lose 3–5 to China in the final"). The page shows all results in a "RESULTS" running line, winner first.

**What the page puts first.** The site orders everything as: live matches → matches under way → upcoming matches (soonest first) → tournaments on → just-finished results → older results. Your job is to make that order meaningful:

- Find what is **live right now** across all sports (cricket, football, tennis, badminton, hockey, kabaddi, F1, chess, athletics, golf …) at every run, and add it with `"st": "live"` and a short `status` — this is the most important thing on the page.
- Keep the next **7 days** of fixtures full and varied (India first, then Indian leagues, then global events), with real IST times.
- Keep `competitions` to about **8–12** tournaments: set `"live": true` only for tournaments with matches this week, and put dates in `status` ("Live · till 17 Oct", "Starts 10 Oct"). Finished tournaments get a status containing "Concluded" (they sort to the end) and are removed after 3 days.
- When there is no multi-sport event, there is no `event` key — the match centre is the top section.

Mark anything involving an Indian team or athlete with `"india": true`. Mark headline fixtures with `"big": true`; medal/final matches with `"gold": true`.

## Rolling window

- `matches`: keep roughly **25–45** items: everything live now, all of today, India results from the last **3 days**, major other results from the last **2 days**, and upcoming fixtures for the next **14 days** (India: all; others: the important ones). Remove older items.
- Cap any single non-India competition at about 6 upcoming items so the grid stays varied.

## `data.json` reference

```jsonc
{
  "lastUpdated": "2026-10-02T15:45:00+05:30",   // MUST change on every edit: the REAL current IST time from `TZ=Asia/Kolkata date +%Y-%m-%dT%H:%M:%S+05:30` (never estimate or round up)
  "dayLabel": "Fri 2 Oct · Asian Games Day 13",  // short line shown on the hero card
  "featured": "ag-cricket-final",                // optional: id of the match for the 3D hero card
  "heroFacts": [],                               // optional: [{ "v": "67", "l": "India's Asian Games medals" }] — leave [] for automatic counts
  "matches": [ /* see below */ ],
  "event": { /* optional multi-sport event block, see below */ },
  "competitions": [ { "sport": "Cricket", "name": "India v West Indies", "status": "Live series · till 17 Oct", "live": true, "india": true, "note": "…" } ],
  "feed": [ { "t": "15:42", "tag": "GOLD", "c": "var(--gold)", "m": "Boxing", "text": "…" } ],
  "schedule": [ { "d": "03", "mo": "OCT", "title": "India v West Indies, 3rd ODI", "meta": "Cricket · New Chandigarh", "time": "14:00" } ],
  "players": [ { "i": "SG", "name": "Shubman Gill", "role": "Cricket · ODI captain", "p": "…", "photo": { "u": "https://upload.wikimedia.org/…", "by": "Bollywood Hungama", "lic": "CC BY 3.0", "licUrl": "https://creativecommons.org/licenses/by/3.0", "page": "https://commons.wikimedia.org/wiki/File:…" } } ],
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
  "resultAt": "2026-10-02T10:36:00+05:30", // results only: real IST time you set it to result. Drives "JUST FINISHED" — the site shows it at the top of the ticker/match centre for 6 h and on the hero card for 90 min
  "india": true, "big": true, "gold": false,
  "note": "One factual line: scorers, top performers, context.",
  "venue": "New Chandigarh",
  "watch": ["Star Sports 1", "JioHotstar"], // where to watch LIVE in India: TV channels and streaming apps (see below)
  "scoreAt": "2026-10-06T20:24:00+05:30"     // live only: real IST time the score was last confirmed (shown as "as of 8:24 pm")
}
```

Codes: use 3-letter country codes for national teams (`IND`, `PAK`, `AUS`, `ENG`, `BRA` …) — they show real flags (see the list in `flags/`, mapped in `index.html` `FLAGMAP`). `WI` (West Indies) and all clubs get a coloured badge: give clubs a short code (`MCFC`, `BFC`, `LIV`) and their main colour as the 4th element. Use `TBC` when an opponent is unknown.

Scores are free text: cricket `"406/2"` or `"245/8 (50)"`; football `"2"`; tennis `"6-4 7-5"`; individual events the athlete's result, or `"Won"` if only the outcome is known.

### Where to watch (`watch`) — fill it for every live and upcoming match

- A list of the channels and apps that broadcast/stream the match **in India**, TV first then apps: `["Star Sports 1", "Star Sports 1 Hindi", "JioHotstar"]`, `["Sony Ten 1", "SonyLIV"]`, `["DD Sports", "Waves"]`, `["FanCode"]`, `["Sports18", "JioHotstar"]`.
- A free official stream on YouTube or a federation site: `{"n": "YouTube – AIFF TV", "u": "https://www.youtube.com/@…"}` (only real URLs).
- The page shows each with an icon by type: TV channel, streaming app (JioHotstar, SonyLIV, FanCode, Prime Video, F1 TV, Waves get a tap-through link), YouTube. Any other name shows as a TV channel unless you give a `u` link.
- Check the official broadcaster announcement (league/federation/broadcaster press release, or a news report naming the channel) — rights change between seasons and tournaments, so never assume. If not confirmed, omit `watch` (the page says "not confirmed yet").

### Scores — always show the score

- Every **live** match must carry its current score in `a[2]`/`b[2]` (cricket `"124/3 (14.2)"` for the batting side and `"Yet to bat"` or the first-innings total for the other; football `"1"`; tennis set scores) plus `status` and `scoreAt` (when you confirmed it). Update both on every run while the match is live.
- Every **result** must carry final scores for both sides.
- Keep `status` **short** (under ~40 characters, one idea): `"India need 110 off 84"`, `"72' · rain delay"`, `"2nd set"`. Don't repeat the score or add times in it — the page shows the score and `scoreAt` itself. Longer context goes in `note`.

Status changes: when a match starts set `"st": "live"` with a `status`; when it ends set `"st": "result"`, fill both scores, `win`, `day`, `recent: true` and `resultAt` (current IST time from the shell). Keep `when` on results too. If a match has started but you can't find its score, leave it `upcoming` — the site labels it "UNDER WAY" automatically.

### Player photos (`players[].photo`) — legal rules

- **Only Wikimedia Commons files under a free licence**: CC0 / public domain, CC BY, CC BY-SA, or GODL-India (Indian government photos: PIB, PMO, President's Secretariat). Check the licence on the file's Commons page. Never use photos from news sites, Google Images, team/league sites, agencies (Getty, AP, PTI, BCCI) or social media — even if they look free.
- Fill every field: `u` (the upload.wikimedia.org / thumb.wikimedia.org image URL, ideally a ~250px thumbnail), `by` (author as written on Commons), `lic` (short licence name), `licUrl` (licence link), `page` (the Commons file page). The page shows the credit under the players and in the player panel — that attribution is what the licence requires.
- Easiest way: the player's English Wikipedia infobox photo is usually on Commons; use its file page to read author and licence. If there is no free photo, omit `photo` — the page shows initials.
- Keep a player's `photo` when you edit their note. When you replace a player, drop or replace their photo too.

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
  "medalChecked": "2026-10-02T10:12:00+05:30",   // set EVERY run after you verify the medal table (real IST time from the shell), even if nothing changed
  "othersAsOf": "end of Day 12 (latest published table)",   // how current the non-India rows are; update when you refresh them
  "medalTable": [ { "code": "CHN", "name": "China", "g": 154, "s": 71, "b": 63 } ],   // top 9 + India
  "medalSrc": [ { "t": "Khel Now – medal tally", "u": "https://…" } ],
  "indiaMedals": [   // EVERY India medal — the count per colour must match India's row in medalTable
    { "medal": "silver", "sport": "Archery", "event": "Recurve mixed team", "who": "Kumkum Mohod & Dhiraj Bommadevara — lost the final 3–5 to China",
      "day": "2 Oct",   // only for medals won in the last 2 days (drives the "Latest" tab and date badge); remove after that
      "src": [ { "t": "Outlook India – Day 13 live", "u": "https://…" } ] }
  ]
}
```

After the closing ceremony: set `statusText` to "Concluded — final standings" (the page then moves the block below the live content and renames the menu link to "… results"), update the final table, keep the block for **3 days**, then delete the whole `event` key. Aichi-Nagoya 2026 closed on 4 Oct → delete its `event` block, its matches and its competition entry on **7 Oct**. Event matches use `"comp": "Asian Games"` (or the event's name).

## Sources and links (everything on the site is clickable)

Every item opens a detail panel that shows its source, so **attach sources**:

- `src`: a list of `{ "t": "Publisher – short title", "u": "https://…" }` on every match, competition, feed item (optional, falls back to its match), and every medal. Use the article you actually read. Never invent URLs.
- Feed items: add `"match": "<match id>"` when the update is about a match on the site.
- Schedule rows: add `"match": "<match id>"` when the row is a match on the site (clicking the row opens that match).
- Competitions: give each an `"id"` and, if its fixtures are on the site, `"comp"` equal to the matches' `comp` value, so the panel lists them.
- Players: optional `"q"` = the word to match in match names/notes/medals (usually the surname).
- When a match or medal is updated, update its `src` too.

## Research rules

- Use several sources and search phrasings. Results often appear first in the **opponent's or host's language** — search Korean, Chinese, Japanese, Malay, Arabic, Urdu, Spanish, Portuguese etc. as relevant (e.g. "아시안게임 양궁 결승 인도", "亚运会 决赛 印度").
- If the built-in browser on Keshav's computer is available, **search Google** there (read the AI Overview and Top stories, then confirm in an article). Cloud runs cannot fetch Google — don't retry it.
- Good sources: ESPNcricinfo, Cricbuzz, BCCI, Olympics.com, Khel Now, The Bridge, Sportstar, Indian Express, Hindustan Times, Times of India, NDTV Sports, ANI, PTI, Outlook, Business Standard, AIFF, Hockey India, ISL, PKL, BWF, ATP/WTA, Premier League, UEFA, F1, Wikipedia, plus foreign outlets (Yonhap, Chosun, Xinhua, NHK, Kyodo, Dawn, Malay Mail …).
- **Never invent** scores, names, times or venues. Use `TBC` / leave blank when unknown. When sources disagree, use the most recent timestamped report.
- Times are always **IST**. Get the current time from the shell (`TZ=Asia/Kolkata date`) — never guess it. Feed `t` values are the time the event happened, not the time you are writing.
- Keep notes short, neutral and factual. No betting odds.
