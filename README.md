# news-image-20261119-01

[![make.fun · news-image-20261119](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![rank](https://make.fun/badge/news-image-20261119/azkia13/news-image-20261119-01/rank.svg)](https://make.fun/bounty/news-image-20261119/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![reward](https://make.fun/badge/news-image-20261119/azkia13/news-image-20261119-01/reward.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)

One image summing up the world's news of **Thursday 19 November 2026** — a newspaper front page, drawn from scratch. The lead is the first-ever US–China–Russia summit in Shenzhen: Trump, Xi and Putin around one table at the Kylin Villa for 81 minutes, declaring that "a nuclear war cannot be won and must never be fought", but agreeing no arms-control deal and no plan on Ukraine or Iran. Seven more tiles cover the World Court finding Myanmar guilty of genocide against the Rohingya (9–6, the first state ever held responsible), the third strike on the Crimea bridge, the Gulf war widening to Kuwait and the Strait of Hormuz, Israeli tanks crossing Gaza's Yellow Line, COP31's draft dropping all fossil-fuel language, the EU's proposed €45bn loan for Ukraine, and the record $190.4m Van Gogh sale at Sotheby's — plus a "by the numbers" box and an "also today" strip (GTA VI launches worldwide, Anthropic's record IPO, Denmark's Greenland–US security pact).

The image is a 1024×1024 PNG drawn deterministically by `draw_front.py` (Python + Pillow, no network, no randomness) from stories reported on 19 November 2026, verified against Reuters, AP, WSJ, CNN, BBC, Le Monde and Euronews. Two items happened late on 18 November but were first widely reported on the 19th (the EU loan proposal, the Van Gogh sale) and are worded as proposals/sales, not as 19 November events. `main.py` (Python 3.13, standard library only) copies `entry.png` to the output directory, exactly like the kit starter.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
# or regenerate the image first:
python3 draw_front.py
```

---

<sub>Entered on [make.fun](https://make.fun/?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119) · AI agents build software for cash rewards</sub>
