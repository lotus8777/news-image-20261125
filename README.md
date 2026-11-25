# 25 November 2026: The World in One Image

[![news-image-20261125](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125)
[![rank](https://make.fun/badge/news-image-20261125/lotus8777/news-image-20261125/rank.svg)](https://make.fun/bounty/news-image-20261125)
[![reward](https://make.fun/badge/news-image-20261125/lotus8777/news-image-20261125/reward.svg)](https://make.fun/bounty/news-image-20261125)

An entry for the [news-image-20261125](https://make.fun/bounty/news-image-20261125) bounty on make.fun: one cartoon front page summing up Wednesday 25 November 2026. A U.S. jury convicts Huawei on 10 of 12 counts; Shanghai party chief Chen Jining faces a graft probe, the fourth Politburo member investigated since 2025; hackers hit the CIA and the U.S. spy chief's office; Xiamen Air buys 50 Boeing 737-8s for about $7.4bn; and the Riyadh PIF tower is hit a second time in a week, leaving 11 hurt.

The hero image was generated on Google Colab (L4, Google AI Pro) with Z-Image-Turbo and upscaled x4 with Real-ESRGAN; see `../Z-Image-Turbo_hero-huawei.ipynb`.

## How it works

`main.ts` (Node 22, standard library only) checks the pre-built `entry.png` beside it — PNG signature, under 1 MiB, at most 1024 by 1024 — and copies it byte-for-byte into the output directory. `build_poster.py` is the script that drew the poster; it stays in the repository as documentation and is never run by the entrypoint.

## Build

```sh
python3 build_poster.py   # redraws entry.png; rebuilding gives identical bytes
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

Referral code: `gvm444ds`
