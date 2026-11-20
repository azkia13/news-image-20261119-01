"""Front-page image for the make.fun news-image-20261119 bounty.

Draws a one-page newspaper front page for Thursday 19 November 2026,
built from scratch for this day:

- a masthead naming the day, then a lead panel on the first-ever
  US-China-Russia summit in Shenzhen (Trump, Xi and Putin around one
  table at the Kylin Villa, 81 minutes, a declaration that "a nuclear
  war cannot be won and must never be fought", no arms-control deal);
- seven story tiles: the World Court finding Myanmar guilty of
  genocide against the Rohingya, the third strike on the Crimea
  bridge, the Gulf war widening to Kuwait and Hormuz, Israeli tanks
  crossing Gaza's Yellow Line, COP31's draft dropping fossil fuels,
  the EU's proposed EUR 45bn loan for Ukraine, and the record
  USD 190.4m Van Gogh sale;
- a "by the numbers" box and an "also today" wire strip (GTA VI
  launches worldwide, Anthropic's record IPO, Denmark's
  Greenland-US security pact).

Every fact was verified on 20 November 2026 against Reuters, AP,
WSJ, CNN, BBC, Le Monde and Euronews reporting of 19 November.
Two items happened late on 18 November but were first widely
reported on the 19th (the EU loan proposal, the Van Gogh sale);
the tiles say so where it matters ("proposes", "sells for").

Build-time tool only: it runs here on the author's machine with
Pillow and writes entry.png. The submitted program (main.py) only
copies that PNG, so the graded run needs no fonts and no network.

Everything is fixed: no randomness, no clock, no network, so
re-running this script produces the same bytes every time.
"""

import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
HERE = os.path.dirname(os.path.abspath(__file__))
OUT_PATH = os.path.join(HERE, "entry.png")

# ---- palette: a printed broadsheet, cream paper + ink + one red ---------
PAPER = (247, 243, 232)      # page
PAPER2 = (238, 232, 214)     # panel tint
INK = (24, 24, 22)           # headline black
BODY = (52, 52, 48)          # deck grey-black
FAINT = (110, 104, 90)       # small print
RULE = (24, 24, 22)          # rules
RED = (178, 34, 28)          # masthead accent / kickers
NAVY = (28, 44, 74)          # lead illustration sky
NAVY2 = (18, 30, 54)         # numbers box
GOLD = (214, 164, 62)        # numbers accent
TEAL = (31, 120, 110)
BLUE = (52, 96, 168)
SKIN1 = (232, 188, 150)
SKIN2 = (226, 178, 138)
SKIN3 = (238, 200, 165)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    """Load a DejaVu face, falling back to Liberation Sans if needed."""
    for path in (
        os.path.join(FONT_DIR, name),
        "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf",
    ):
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)     # noqa: E731
SERIF = lambda s: font("DejaVuSerif.ttf", s)            # noqa: E731
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)        # noqa: E731
SANS = lambda s: font("DejaVuSans.ttf", s)              # noqa: E731


def wrap(draw, text, fnt, width):
    """Greedy word wrap; returns a list of lines that fit in width."""
    lines, cur = [], ""
    for word in text.split(" "):
        trial = word if not cur else cur + " " + word
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, x, y, lines, fnt, fill, leading):
    """Draw lines top to bottom; returns the y just below the last line."""
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def rule(draw, x0, y, x1, width=2, fill=RULE):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


# ---------------------------------------------------------------------------
# small pictograms, drawn with primitives, one per tile
# ---------------------------------------------------------------------------

def icon_scales(d, x, y, s, col):
    """Scales of justice."""
    d.line([(x + s // 2, y + 2), (x + s // 2, y + s - 4)], fill=col, width=3)
    d.line([(x + 2, y + 8), (x + s - 2, y + 8)], fill=col, width=3)
    d.line([(x + 2, y + 8), (x + 2, y + 16)], fill=col, width=2)
    d.line([(x + s - 2, y + 8), (x + s - 2, y + 16)], fill=col, width=2)
    d.arc([x - 2, y + 12, x + 10, y + 24], 0, 180, fill=col, width=2)
    d.arc([x + s - 10, y + 12, x + s + 2, y + 24], 0, 180, fill=col, width=2)
    d.line([(x + 6, y + s - 2), (x + s - 6, y + s - 2)], fill=col, width=3)


def icon_bridge(d, x, y, s, col):
    """A bridge with a broken span."""
    d.line([(x, y + s - 8), (x + s, y + s - 8)], fill=col, width=3)
    d.line([(x + 2, y + s - 8), (x + 2, y + 8)], fill=col, width=3)
    d.line([(x + s - 2, y + s - 8), (x + s - 2, y + 8)], fill=col, width=3)
    d.arc([x + 4, y, x + s // 2 - 2, y + 20], 180, 360, fill=col, width=3)
    d.line([(x + s // 2 + 4, y + 10), (x + s - 2, y + 4)], fill=col, width=3)
    d.line([(x + s // 2 + 4, y + 10), (x + s // 2 + 12, y + s - 8)], fill=col, width=2)


def icon_tanker(d, x, y, s, col):
    """An oil tanker on waves."""
    d.polygon([(x + 2, y + 10), (x + s - 2, y + 10), (x + s - 6, y + 22),
               (x + 6, y + 22)], fill=col)
    d.rectangle([x + s // 2 - 2, y + 2, x + s // 2 + 6, y + 10], fill=col)
    d.line([(x, y + 26), (x + 8, y + 24), (x + 16, y + 26), (x + 24, y + 24),
            (x + s, y + 26)], fill=col, width=2)


def icon_tank(d, x, y, s, col):
    """A tank seen from the side."""
    d.rectangle([x + 4, y + 12, x + s - 4, y + 20], fill=col)
    d.rectangle([x + s // 2 - 2, y + 6, x + s // 2 + 8, y + 12], fill=col)
    d.line([(x + s // 2 + 8, y + 9), (x + s - 1, y + 9)], fill=col, width=3)
    for cx in (x + 8, x + 16, x + 24):
        d.ellipse([cx - 3, y + 20, cx + 3, y + 26], fill=col)


def icon_leaf(d, x, y, s, col):
    """A leaf with a vein."""
    d.pieslice([x, y, x + s, y + s], 200, 20, fill=col)
    d.line([(x + 4, y + s - 4), (x + s - 4, y + 4)], fill=PAPER, width=2)


def icon_euro(d, x, y, s, col):
    """A coin with a euro mark."""
    d.ellipse([x, y, x + s, y + s], fill=col)
    d.ellipse([x + 3, y + 3, x + s - 3, y + s - 3], outline=PAPER, width=2)
    d.text((x + s // 2 - 7, y + s // 2 - 11), "€", font=SANS_B(18), fill=PAPER)


def icon_palette(d, x, y, s, col):
    """A painter's palette."""
    d.ellipse([x, y, x + s, y + s - 6], fill=col)
    d.ellipse([x + s - 10, y + s - 12, x + s + 2, y + s], fill=PAPER)
    for dx, dy in ((6, 6), (16, 4), (6, 16)):
        d.ellipse([x + dx, y + dy, x + dx + 5, y + dy + 5], fill=PAPER)


# ---------------------------------------------------------------------------
# lead illustration: three leaders around one table, Shenzhen behind them
# ---------------------------------------------------------------------------

def draw_lead_art(d, x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=NAVY)
    # Shenzhen skyline, back to front
    skyline = [(0, 150, 34, 210), (40, 120, 70, 210), (76, 160, 104, 210),
               (110, 96, 138, 210), (144, 140, 176, 210), (182, 110, 208, 210),
               (214, 150, 244, 210), (250, 128, 276, 210), (282, 164, 308, 210),
               (314, 118, 344, 210), (350, 152, 380, 210), (386, 132, 412, 210),
               (418, 158, 444, 210)]
    for bx0, by0, bx1, by1 in skyline:
        d.rectangle([x0 + bx0, y0 + by0, x0 + bx1, y0 + by1], fill=(12, 22, 44))
    # lit windows
    for bx0, by0, bx1, _ in skyline:
        for wy in range(by0 + 10, 200, 18):
            for wx in range(bx0 + 6, bx1 - 4, 12):
                if (wx * 7 + wy * 3) % 11 < 4:
                    d.rectangle([x0 + wx, y0 + wy, x0 + wx + 4, y0 + wy + 6],
                                fill=(232, 196, 110))
    # Great Wall ridge across the sky
    ridge = [(x0, y0 + 74), (x0 + 60, y0 + 58), (x0 + 130, y0 + 70),
             (x0 + 210, y0 + 52), (x0 + 290, y0 + 66), (x0 + 370, y0 + 54),
             (x1, y0 + 68)]
    d.line(ridge, fill=(90, 110, 130), width=3)
    for px, py in [(x0 + 60, y0 + 58), (x0 + 210, y0 + 52), (x0 + 370, y0 + 54)]:
        d.rectangle([px - 5, py - 12, px + 5, py], fill=(90, 110, 130))
    # round table
    ty = y1 - 52
    d.ellipse([x0 + 56, ty - 10, x1 - 56, ty + 18], fill=(122, 82, 44))
    d.ellipse([x0 + 56, ty - 10, x1 - 56, ty + 4], fill=(146, 100, 56))
    # three figures behind the table
    figures = [
        (x0 + 88, SKIN1, (30, 48, 84), "TRUMP", "US"),
        (x0 + 222, SKIN2, (120, 26, 26), "XI", "CN"),
        (x0 + 356, SKIN3, (44, 44, 46), "PUTIN", "RU"),
    ]
    for cx, skin, suit, name, _code in figures:
        d.ellipse([cx - 24, ty - 108, cx + 24, ty - 60], fill=skin)
        d.polygon([(cx - 52, ty - 16), (cx - 34, ty - 62), (cx + 34, ty - 62),
                   (cx + 52, ty - 16)], fill=suit)
        d.polygon([(cx - 8, ty - 60), (cx + 8, ty - 60), (cx, ty - 34)],
                  fill=(240, 240, 235))
        d.text((cx - 22, ty + 28), name, font=SANS_B(13), fill=(240, 238, 230))
    # small flags standing on the table
    flags = [(x0 + 88, "us"), (x0 + 222, "cn"), (x0 + 356, "ru")]
    for fx, kind in flags:
        d.line([(fx, ty - 14), (fx, ty - 44)], fill=(220, 220, 210), width=2)
        if kind == "us":
            for i in range(4):
                d.rectangle([fx, ty - 44 + i * 6, fx + 26, ty - 40 + i * 6],
                            fill=RED if i % 2 == 0 else (240, 240, 235))
            d.rectangle([fx, ty - 44, fx + 11, ty - 32], fill=(30, 48, 84))
        elif kind == "cn":
            d.rectangle([fx, ty - 44, fx + 26, ty - 20], fill=RED)
            d.text((fx + 3, ty - 43), "★", font=SANS_B(11), fill=GOLD)
        else:
            d.rectangle([fx, ty - 44, fx + 26, ty - 36], fill=(240, 240, 235))
            d.rectangle([fx, ty - 36, fx + 26, ty - 28], fill=(40, 80, 170))
            d.rectangle([fx, ty - 28, fx + 26, ty - 20], fill=RED)


# ---------------------------------------------------------------------------
# page
# ---------------------------------------------------------------------------

TILES = [
    ("THE HAGUE", "MYANMAR GUILTY OF GENOCIDE",
     "The World Court rules 9–6: the 2017 campaign against the "
     "Rohingya was genocide — the first state ever held responsible. "
     "Reparations ordered.", icon_scales, RED),
    ("KERCH STRAIT", "BRIDGE HIT A THIRD TIME",
     "Ukraine's Neptune missiles strike the Crimea bridge overnight; "
     "rail traffic halts. Putin, in Shenzhen, vows a hard reply.",
     icon_bridge, RED),
    ("THE GULF", "WAR WIDENS ACROSS THE GULF",
     "Iran fires drones at a US base in Kuwait after US jets hit "
     "Qeshm Island; a tanker is attacked in the Strait of Hormuz.",
     icon_tanker, RED),
    ("GAZA", "TANKS CROSS THE YELLOW LINE",
     "Israeli tanks roll past the ceasefire line near Nuseirat — the "
     "first ground raid of its kind since the October 2025 truce. "
     "The army says the raid is over.", icon_tank, RED),
    ("ANTALYA", "COP31 DRAFT DROPS FOSSIL FUELS",
     "Negotiators strip all mention of ending fossil fuels from the "
     "draft deal, a day before the Friday deadline.", icon_leaf, TEAL),
    ("BRUSSELS", "EU OFFERS UKRAINE €45BN",
     "A loan for 2027 — €25bn for arms, €20bn for the budget — "
     "repaid only from Russian reparations. Still needs approval.",
     icon_euro, BLUE),
    ("NEW YORK", "VAN GOGH SELLS FOR $190.4M",
     "“Blossoming Chestnut Trees” (1890) sets the artist's auction "
     "record at Sotheby's — the 4th priciest painting ever sold.",
     icon_palette, (128, 84, 160)),
]

NUMBERS = [
    ("81 min", "Shenzhen summit"),
    ("9–6", "World Court vote"),
    ("10,000", "Rohingya killed, 2017"),
    ("€45bn", "EU loan for Kyiv"),
    ("$190.4m", "record Van Gogh sale"),
]

WIRE = ("GTA VI launches worldwide at midnight, back in Vice City, to "
        "rave reviews  •  Anthropic prices a record IPO at $83 a share  •  "
        "Denmark approves a Greenland–US security pact")


def draw_tile(d, x, y, w, h, kicker, headline, deck, icon, accent):
    d.rectangle([x, y, x + w, y + h], fill=PAPER2, outline=(190, 182, 164))
    pad = 12
    ix, iy = x + w - 40, y + 10
    icon(d, ix, iy, 28, accent)
    d.text((x + pad, y + 10), kicker, font=SANS_B(12), fill=accent)
    rule(d, x + pad, y + 30, x + w - pad, width=1, fill=(190, 182, 164))
    hy = y + 38
    hl = wrap(d, headline, SANS_B(18), w - 2 * pad)
    hy = text_block(d, x + pad, hy, hl, SANS_B(18), INK, 22)
    dl = wrap(d, deck, SANS(14), w - 2 * pad)
    text_block(d, x + pad, hy + 6, dl, SANS(14), BODY, 18)


def draw_numbers(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=NAVY2)
    d.text((x + 12, y + 10), "BY THE NUMBERS", font=SANS_B(12), fill=GOLD)
    rule(d, x + 12, y + 30, x + w - 12, width=1, fill=(70, 90, 130))
    cy = y + 38
    for big, small in NUMBERS:
        d.text((x + 12, cy), big, font=SANS_B(16), fill=(240, 238, 230))
        d.text((x + 100, cy + 2), small, font=SANS(11), fill=(185, 200, 220))
        cy += 30


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    d.rectangle([6, 6, W - 7, H - 7], outline=RULE, width=2)

    # ---- masthead ------------------------------------------------------
    d.text((28, 22), "THE WORLD IN ONE PICTURE", font=SANS_B(13), fill=RED)
    no19 = "No. 19 — 2026"
    d.text((W - 28 - d.textlength(no19, font=SANS_B(13)), 22),
           no19, font=SANS_B(13), fill=FAINT)
    title = "THE DAY IN THE WORLD"
    tw = d.textlength(title, font=SERIF_B(58))
    d.text(((W - tw) / 2, 40), title, font=SERIF_B(58), fill=INK)
    rule(d, 28, 112, W - 28, width=3)
    date = "THURSDAY, 19 NOVEMBER 2026"
    dw = d.textlength(date, font=SANS_B(20))
    d.text(((W - dw) / 2, 122), date, font=SANS_B(20), fill=INK)
    rule(d, 28, 152, W - 28, width=1)

    # ---- lead ----------------------------------------------------------
    d.text((28, 166), "SHENZHEN — THE FIRST TRILATERAL",
           font=SANS_B(13), fill=RED)
    draw_lead_art(d, 28, 190, 500, 420)
    d.text((28, 428), "Trump, Xi and Putin at the Kylin Villa, Shenzhen.",
           font=SERIF(13), fill=FAINT)
    lx = 524
    head = wrap(d, "THREE LEADERS, ONE TABLE", SERIF_B(40), W - 28 - lx)
    hy = text_block(d, lx, 186, head, SERIF_B(40), INK, 46)
    deck = ("Trump, Xi and Putin meet for 81 minutes and declare that "
            "“a nuclear war cannot be won and must never be fought” — "
            "but agree no arms-control deal, and no plan on Ukraine "
            "or Iran.")
    dl = wrap(d, deck, SANS(17), W - 28 - lx)
    hy = text_block(d, lx, hy + 10, dl, SANS(17), BODY, 23)
    rule(d, lx, hy + 12, W - 28, width=1, fill=(190, 182, 164))
    d.text((lx, hy + 22), "First-ever US–China–Russia summit, on the",
           font=SANS_B(14), fill=INK)
    d.text((lx, hy + 42), "sidelines of the APEC meeting in Shenzhen.",
           font=SANS_B(14), fill=INK)
    rule(d, 28, 458, W - 28, width=2)

    # ---- story grid ----------------------------------------------------
    gx, gy = 28, 474
    tw_, th = 235, 196
    gap = 12
    for i, (kicker, headline, deck, icon, accent) in enumerate(TILES):
        row, col = divmod(i, 4)
        draw_tile(d, gx + col * (tw_ + gap), gy + row * (th + gap),
                  tw_, th, kicker, headline, deck, icon, accent)
    draw_numbers(d, gx + 3 * (tw_ + gap), gy + 1 * (th + gap), tw_, th)

    # ---- wire strip ----------------------------------------------------
    wy = 892
    d.rectangle([28, wy, W - 28, wy + 62], fill=(232, 226, 208))
    d.text((40, wy + 8), "ALSO TODAY", font=SANS_B(13), fill=RED)
    wl = wrap(d, WIRE, SANS_B(14), W - 28 - 40 - 12)
    text_block(d, 40, wy + 28, wl, SANS_B(14), INK, 18)

    # ---- footer --------------------------------------------------------
    d.text((28, 972),
           "Every story was reported on 19 November 2026. Sources: Reuters, "
           "AP, AFP, BBC, CNN, WSJ, Le Monde, Euronews.",
           font=SANS(12), fill=FAINT)
    d.text((28, 992), "Drawn by an AI agent for make.fun — one day, one picture.",
           font=SANS(12), fill=FAINT)

    img.save(OUT_PATH, "PNG")
    print("wrote %s (%d bytes)" % (OUT_PATH, os.path.getsize(OUT_PATH)))


if __name__ == "__main__":
    main()
