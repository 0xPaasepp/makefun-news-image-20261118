# makefun-news-image-20261118

The World in One Picture — Wednesday 18 November 2026.

[![news-image-20261118](https://make.fun/badge/news-image-20261118.svg)](https://make.fun/bounty/news-image-20261118)
[![rank](https://make.fun/badge/news-image-20261118/0xPaasepp/makefun-news-image-20261118/rank.svg)](https://make.fun/bounty/news-image-20261118)
[![reward](https://make.fun/badge/news-image-20261118/0xPaasepp/makefun-news-image-20261118/reward.svg)](https://make.fun/bounty/news-image-20261118)

An entry for [Sum up 18 November's world news in one image](https://make.fun/bounty/news-image-20261118) on make.fun.

A Python 3.13 program (standard library only, no network) that draws a 1024×1024
newspaper front page of Wednesday 18 November 2026: **53 verified stories** — a huge
bold date, three top stories each with a hand-drawn map (the Kerch Bridge, the Gulf,
Shenzhen), four section columns (Europe, Middle East, Markets & Tech, Sport & Climate),
a world map with 12 numbered locations, and an "ALSO ON WEDNESDAY" list.

Every story happened or was first reported on Wednesday 18 November 2026.

## Run

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

Writes `out/entry.png` (1024×1024 PNG, under 1 MiB). Running it twice writes
byte-identical output.

## Files

- `main.py` — the stories and the page layout
- `draw.py` — a tiny canvas, real DejaVu font glyphs, and a PNG encoder
- `fontdata.py` — real DejaVu font glyph outlines extracted at build time
- `icons.py` — the maps (Kerch Strait, the Gulf, China, the world) and pictograms
