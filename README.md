[![make.fun · news-image-20261125](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![rank](https://make.fun/badge/news-image-20261125/Nopnop15/news-image-20261125/rank.svg)](https://make.fun/bounty/news-image-20261125/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![reward](https://make.fun/badge/news-image-20261125/Nopnop15/news-image-20261125/reward.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)

# The World in One Page — Wednesday 25 November 2026

A front-page image summing up the world's news of Wednesday 25 November
2026. Six stories, each drawn as its own panel with a short headline and
subline:

1. **Shenzhou-24 launches** — China launches Shenzhou-24 from Jiuquan at
   08:18 Beijing time. The crew is Tang Hongbo, Wu Yi and Muhammad Zeeshan
   Ali, the first Pakistani in orbit and the first foreign astronaut aboard
   the Tiangong station.
2. **EU sanctions Russia** — The European Union proposes a broad new
   sanctions package covering banking, crypto and sports events, plus a visa
   ban for war participants.
3. **CIA and ODNI hacked** — US intelligence agencies the CIA and the
   Office of the Director of National Intelligence are hit by a cyberattack
   affecting unclassified information; officials say classified systems were
   undisrupted.
4. **Australia–Solomons pact** — Australia and Solomon Islands sign a
   security agreement naming Australia the Solomons' primary security
   partner and ruling out foreign military bases.
5. **Sanofi buys Insmed** — French pharma company Sanofi agrees to acquire
   US biotech Insmed in a $41 billion deal.
6. **Rial at record low** — Iran's rial hits a record low of 2.856 million
   per dollar on Tehran's open market after fresh US sanctions target its
   financial network.

## How it is built

`generate_image.py` draws the 1024×1024 front page with Pillow
(masthead, hero rocket panel, five more panels, footer) and writes
`entry.png`. `main.ts` (Node 22, standard library only) copies `entry.png`
into the output folder. Run it with:

```sh
python3 generate_image.py
MAKEFUN_OUTPUT_DIR=out node main.ts
```

## License

MIT — see `LICENSE`.
