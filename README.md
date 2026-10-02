# Catch The Sport — Asian Games 2026 Live

Homepage for the Catch The Sport YouTube channel, with live coverage of the Aichi-Nagoya 2026 Asian Games.

## Files

| File | What it does |
|---|---|
| `index.html` | The website (design, layout, scripts). |
| `asian-games-data.json` | All the results, medals, schedule and live updates. **This is the file you edit to update the site.** |
| `vercel.json` | Tells Vercel never to cache the data file, so visitors always get the latest numbers. |
| `favicon.svg` | Browser tab icon. |

## Deploy (one time)

1. Create a new repository on GitHub and upload everything in this folder (including `.gitignore`).
2. In Vercel: **Add New → Project → Import** your GitHub repo.
3. Framework preset: **Other**. Leave build command and output directory empty. Click **Deploy**.

## Updating live results

1. On GitHub, open `asian-games-data.json` and click the pencil (Edit) icon.
2. Change what you need, for example India's medals:
   ```json
   { "code": "IND", "name": "India", "g": 12, "s": 23, "b": 33 }
   ```
3. **Always change `lastUpdated`** to the current time, e.g. `"2026-10-02T15:45:00+05:30"`.
   The page only refreshes when this value changes.
4. Click **Commit changes**. Vercel redeploys in about 30 seconds, and anyone with the
   page open sees the new data within 60 seconds — no reload needed.

### Common edits

- **Match finished:** in `matches`, change `"st": "upcoming"` to `"st": "result"`, fill in the scores
  (third item in `a` and `b`), add `"win": "a"` or `"win": "b"` and `"day": "2 Oct · Day 13"`.
- **New update in the feed:** add a line at the top of `feed`:
  `{ "t": "15:40", "tag": "GOLD", "c": "var(--gold)", "m": "Hockey", "text": "..." }`
  (tag colours: `var(--gold)`, `var(--silver)`, `var(--bronze)`, `var(--accent)`, `var(--live-text)`).
- **New India gold:** add it to the top of `indiaGolds` and to `indiaToday`.
- **Country codes with flags:** CHN, JPN, KOR, UZB, IRI, THA, BRN, IND, KAZ, PAK, SRI, MAS, HKG.
  Any other code shows as a text badge; `TBC` shows a "?".

Before committing, you can paste the file into https://jsonlint.com to check for typos —
if the JSON is broken, the site simply keeps showing the previous data.

## Still to fill in

- Your YouTube channel link (search `https://www.youtube.com/` in `index.html`).
- Instagram / X / Contact links in the footer (`href="#"`).
- Video titles, views and lengths in the `videos` section of the data file.
