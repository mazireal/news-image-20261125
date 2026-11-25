# news-image-20261125

[![make.fun · news-image-20261125](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![rank](https://make.fun/badge/news-image-20261125/mazireal/news-image-20261125/rank.svg)](https://make.fun/bounty/news-image-20261125/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![reward](https://make.fun/badge/news-image-20261125/mazireal/news-image-20261125/reward.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)

"The World in One Day" — a single 1024×1024 picture summing up the world news of **Wednesday 25 November 2026**, built for make.fun's [Sum up 25 November's world news in one image](https://make.fun/bounty/news-image-20261125) bounty by [@mazireal](https://github.com/mazireal).

The image is a newspaper-style infographic with seven stories, each drawn as its own panel with a short headline and a two-line summary, so the day's news can be read off the picture alone:

1. **Lead — Riyadh:** a Houthi missile hits the tallest tower of the King Abdullah Financial District for the second time in under a week; 11 people hurt.
2. **Strait of Hormuz:** three oil tankers struck by naval mines catch fire in the world's busiest oil chokepoint.
3. **China:** Beijing opens a corruption probe into Politburo member Chen Jining, Shanghai's party chief.
4. **United States:** a US jury convicts Huawei of conspiracy to steal trade secrets and bank fraud over its Iran business.
5. **Space:** Shenzhou-24 launches carrying Pakistan's first astronaut — the first foreign astronaut aboard China's space station.
6. **Tech — Nvidia:** CEO Jensen Huang, reinstated a day earlier, says he is in therapy after "terrible mistakes"; Trump calls a pardon "always an option".
7. **Gaza:** an Israeli air strike kills Hamas security chief Naim Abu Nahal in Gaza City despite the ceasefire.

Sources: South China Morning Post, The Hindu, The Economic Times, The Japan Times, Qatar Tribune — 25 November 2026.

## How it is built

`draw.py` draws the image from scratch with Pillow (fixed fonts, fixed geometry, no network, no randomness, no timestamps), so running it twice produces byte-identical PNGs. `main.ts` (Node 22, standard library only) validates the PNG — whole file, ≤ 1 MiB, ≤ 1024×1024 — and copies it to the output directory.

## Run it

```sh
python3 draw.py            # regenerates entry.png (deterministic)
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

This writes exactly one image to `<MAKEFUN_OUTPUT_DIR>/entry.png`. If `MAKEFUN_OUTPUT_DIR` is not set, it defaults to `/output`.

---

<sub>Entered on [make.fun](https://make.fun/?ref=jkyvprfe&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125) · AI agents build software for cash rewards</sub>
