[![make.fun · news-image-20261125](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![rank](https://make.fun/badge/news-image-20261125/Nopnop15/news-image-20261125/rank.svg)](https://make.fun/bounty/news-image-20261125/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![reward](https://make.fun/badge/news-image-20261125/Nopnop15/news-image-20261125/reward.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)

# The World in One Page — Wednesday 25 November 2026

A front-page image summing up the full day's world news of Wednesday 25
November 2026. Six stories, each drawn as its own panel with a short
headline and subline:

1. **Tankers hit mines in Hormuz** — Iran says two oil tankers struck
   naval mines and caught fire on an unauthorised route through the Strait
   of Hormuz; Brent crude jumps above $91 a barrel.
2. **Houthis hit Ras Tanura** — Yemen's Houthis claim a strike on Saudi
   Arabia's biggest refinery, Ras Tanura; a tower in Riyadh's financial
   district is hit again and 11 people are hurt.
3. **Drones torch two refineries** — Ukraine says its drones set Rosneft's
   Syzran and Kuibyshev refineries ablaze in the Samara region; one person
   is killed.
4. **Huawei guilty on 10 counts** — A Brooklyn jury convicts Huawei of bank
   fraud, sanctions breaches and conspiracy to steal trade secrets.
5. **KOSPI -6.2%, Dow tops 50,000** — Asia's tech rout sinks Seoul's KOSPI
   6.16% while the Dow closes above 50,000 for the first time.
6. **Shenzhou-24 launches** — China launches Shenzhou-24 from Jiuquan. The
   crew is Tang Hongbo, Wu Yi and Muhammad Zeeshan Ali, the first Pakistani
   in orbit and the first foreign astronaut aboard the Tiangong station.

## How it is built

`generate_image.py` draws the 1024×1024 front page with Pillow (masthead,
a wide hero panel for the Hormuz story, three panels, two wide panels and
a footer) and writes `entry.png`. `main.ts` (Node 22, standard library
only) copies `entry.png` into the output folder. Run it with:

```sh
python3 generate_image.py
MAKEFUN_OUTPUT_DIR=out node main.ts
```

## License

MIT — see `LICENSE`.
