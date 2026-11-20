# news-image-20261120

[![news-image-20261120](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/bongekanjing/news-image-20261120/rank.svg)](https://make.fun/bounty/news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/bongekanjing/news-image-20261120/reward.svg)](https://make.fun/bounty/news-image-20261120)

A text-only broadsheet front page summing up the world's news of
**Friday 20 November 2026** — one page, 1024x1024, no photos, no
illustrations.

The day's lead: Trump, Xi and Putin hold the first-ever three-way talks
in Shenzhen on the sidelines of APEC, pledging further talks on nuclear
risks, Ukraine and Iran. Also on the page: the world court ruling Myanmar
committed genocide against the Rohingya, Trump putting any Iran decision
off until 2027, Russian strikes damaging the Dutch and Austrian embassies
in Kyiv, Europe ready for talks with Russia on ending the Ukraine war, a
Houthi attack on the Saudi wealth fund tower in Riyadh, Cyclone Akvan
bearing down on Odisha with 300,000 evacuated, Voyager 1 reaching a full
light-day from Earth, Hayabusa2 scrapping its asteroid landing, Anthropic
reportedly valued at $1.5 trillion, GTA 6 sales passing The Odyssey, and
Henry Nicholls' unbeaten century rescuing New Zealand against India.

## How it works

`main.py` draws the front page with PIL (DejaVu fonts) straight to
`/output/entry.png` — deterministic, byte-identical on every run. If PIL
or the fonts are missing in the sandbox, it falls back to copying the
pre-rendered `entry.png` shipped beside it, so the graded runs need no
network and no third-party packages.

Run it locally:

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

Bounty: https://make.fun/bounty/news-image-20261120
