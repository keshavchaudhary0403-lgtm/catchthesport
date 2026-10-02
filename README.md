# Catch The Sport — live sports hub

Homepage for the Catch The Sport YouTube channel: live scores, results and upcoming matches across every sport Indian fans follow. Live at https://catchthesport.vercel.app

| File | What it does |
|---|---|
| `index.html` | The website (design, layout, scripts). Rarely changes. |
| `data.json` | **All content** — matches, featured event (e.g. Asian Games), tournaments, live feed, India schedule, players, videos. |
| `UPDATING.md` | Rules and field reference for updating `data.json`. Scheduled Claude tasks follow it. |
| `scripts/validate.py` | Run before committing: `python3 scripts/validate.py` must print `OK`. |
| `flags/` | Country flags (flag-icons, MIT licence). |
| `vercel.json` | Tells Vercel never to cache `data.json`. |

Updates: commit a change to `data.json` on `main` → Vercel redeploys in ~30 s → open pages refresh within 20 s.

Still to fill in: your YouTube channel link (search `https://www.youtube.com/` in `index.html`), footer social links, and real video entries in `data.json`.
