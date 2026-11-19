"""The World in One Picture — Wednesday 18 November 2026.
make.fun news-image-20261118 entry. Stdlib only, no network, deterministic.
Writes ONE image to $MAKEFUN_OUTPUT_DIR/entry.png (default ./output).
Written fresh for news-image-20261118.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from draw import Canvas, draw_text, text_w, wrap_text  # noqa: E402
from icons import map_kerch, map_gulf, map_china, world_map, icon  # noqa: E402

W, H = 1024, 1024
PAPER = (247, 242, 231)
INK = (20, 20, 20)
RED = (178, 34, 34)
BLUE = (30, 80, 160)
NAVY = (25, 45, 90)
GREEN = (46, 125, 60)
ORANGE = (214, 110, 20)
GOLD = (214, 158, 32)
CARD = (255, 253, 248)
MUTED = (90, 85, 75)

# ------------------------------------------------------------------ stories
TOP = [
    {
        "map": map_kerch,
        "tag": "EUROPE  -  UKRAINE WAR",
        "tag_color": RED,
        "headline": "Kerch Bridge road span falls into the sea",
        "deck": "Second strike in two days. Traffic halted.",
    },
    {
        "map": map_gulf,
        "tag": "MIDDLE EAST  -  GULF WAR",
        "tag_color": RED,
        "headline": "Iran drones hit US base in Bahrain",
        "deck": "US jets hit Qeshm in reply; Kuwait hit too.",
    },
    {
        "map": map_china,
        "tag": "ASIA  -  SUMMIT EVE",
        "tag_color": BLUE,
        "headline": "Trump flies to China for first Xi-Putin summit",
        "deck": "Thursday in Shenzhen: Ukraine, nukes, trade.",
    },
]

MIDDLE = [
    ("EUROPE", BLUE, [
        ("vote", "Italy passes antisemitism law"),
        ("quake", "Romania quake, magnitude 5.3"),
        ("bank", "Knesset picks new speaker"),
        ("plane", "Japan protests airspace breach"),
        ("sun", "Earthshot: $1.3M prizes"),
        ("chart", "Russian oil refining nearly halved"),
    ]),
    ("MIDDLE EAST", RED, [
        ("ship", "US sinks five Iranian tankers"),
        ("flag", "Iran shuts sea zone to ships"),
        ("blast", "Houthis fire missiles at Riyadh"),
        ("blast", "Trump warns of 'dirty bomb' plot"),
        ("globe", "UN warns of Gaza cold deaths"),
        ("plane", "Kuwait downs drone wave"),
    ]),
    ("MARKETS & TECH", GREEN, [
        ("chart", "Nvidia beats forecast, +4.8%"),
        ("chart", "Asia stocks snap losing streak"),
        ("chart", "S&P 500 falls for 4th day"),
        ("coin", "Dollar hits 19-month high"),
        ("coin", "Bitcoin holds near $64,500"),
        ("flask", "Anthropic prices IPO at $83"),
    ]),
    ("SPORT & CLIMATE", ORANGE, [
        ("trophy", "Zverev books ATP Finals semis"),
        ("ball", "Alcaraz tops group, semis bound"),
        ("leaf", "COP31 draft splits the talks"),
        ("globe", "Island states want $500M"),
        ("flask", "Antalya AI Pledge backed"),
        ("sun", "M1.1 solar flare recorded"),
    ]),
]

ALSO = [
    "US loses measles-free status",
    "Biden memoir: Putin 'teenager'",
    "Trump pulls FDA nominee Overton",
    "Rubio: no sign outages are sabotage",
    "Navy chief grilled on Iran war",
    "Merchant gets 27 years for Trump plot",
    "Democrats eye first Black Speaker",
    "Iraq cracks down on oil smuggling",
    "Fed's Williams: no dramatic move",
    "Ethiopia, Eritrea mass troops at border",
    "Board of Peace faults Israel, Hamas",
    "ICJ to rule on Rohingya case",
    "Taiwan awaits $14B arms sale OK",
    "Kim tours resort before Trump trip",
    "Pakistan cuts petrol to Rs325",
    "Pakistan condemns Israel at UN",
    "Bangladesh leader killed in clashes",
    "India malaria down 80% in decade",
    "Tanker crew missing in Hormuz",
    "Houthis advance on Aden",
    "Xi: tear down trade barriers",
    "Tiafoe routs Cobolli in Turin",
    "Nvidia forms export-control panel",
    "Apple joins parade of tech glitches",
    "FAA halts new router installs",
    "US absent from COP31 again",
]

DOTS = [
    (36, 45, 1, 10, -16),     # Kerch
    (30, 50, 2, -26, -16),    # Kyiv
    (50, 26, 3, -34, 2),      # Bahrain
    (56, 27, 4, 8, -18),      # Qeshm
    (48, 29, 5, 4, 12),       # Kuwait
    (114, 22, 6, -4, -16),    # Shenzhen
    (121, 15, 7, 8, 8),       # Manila
    (30, 37, 8, 8, 12),       # Antalya
    (7, 45, 9, -4, 10),       # Turin
    (2, 49, 10, -28, -12),    # Paris
    (-77, 39, 11),            # Washington
    (77, 28, 12, 10, 10),     # Delhi
]

TOTAL_STORIES = len(TOP) + sum(len(s) for _, _, s in MIDDLE) + len(ALSO)


def center(cv, y, text, scale, color, bold=False, font="sans"):
    draw_text(cv, (W - text_w(text, scale, bold, font)) // 2, y, text, scale,
              color, bold=bold, font=font)


# ------------------------------------------------------------------ sections
def masthead(cv):
    center(cv, 14, "THE WORLD'S NEWS IN ONE PICTURE", 1, INK, bold=True)
    center(cv, 32, "WEDNESDAY 18 NOVEMBER 2026", 3, RED, bold=True, font="serif")
    center(cv, 88, "%d STORIES  -  6 CONTINENTS  -  ALL FROM WEDNESDAY" % TOTAL_STORIES,
           1, BLUE, bold=True)
    center(cv, 104, "KERCH BRIDGE FALLS  -  GULF STRIKES SPREAD  -  TRUMP FLIES TO SHENZHEN",
           1, INK, bold=True)
    cv.hline(20, 120, W - 20, INK, 2)


def top_card(cv, x, y, w, story):
    cv.rect(x, y, w, 204, CARD)
    # outline
    cv.hline(x, y, x + w, INK, 2)
    cv.hline(x, y + 203, x + w, INK, 2)
    cv.vline(x, y, y + 203, INK, 2)
    cv.vline(x + w - 1, y, y + 203, INK, 2)
    story["map"](cv, x + 4, y + 4, w - 8, 110)
    # tag
    tag = story["tag"]
    tw = text_w(tag, 1, bold=True) + 16
    cv.rect(x + 4, y + 120, tw, 18, story["tag_color"])
    draw_text(cv, x + 12, y + 123, tag, 1, (255, 255, 255), bold=True)
    # headline (2 lines max)
    lines = wrap_text(story["headline"], 1, w - 12, bold=True)
    hy = y + 144
    for ln in lines[:2]:
        draw_text(cv, x + 6, hy, ln, 1, INK, bold=True)
        hy += 14
    # deck (2 lines max)
    dlines = wrap_text(story["deck"], 1, w - 12)
    dy = y + 174
    for ln in dlines[:2]:
        draw_text(cv, x + 6, dy, ln, 1, MUTED)
        dy += 13


def middle_column(cv, x, y, w, header, color, stories):
    draw_text(cv, x, y, header, 1, color, bold=True)
    cv.rect(x, y + 15, w, 2, color)
    ry = y + 22
    for kind, headline in stories:
        cv.rect(x, ry, 30, 30, (232, 226, 214))
        icon(cv, kind, x + 1, ry + 1, 28, color)
        lines = wrap_text(headline, 1, w - 36, bold=True)
        ly = ry + 2
        for ln in lines[:2]:
            draw_text(cv, x + 36, ly, ln, 1, INK, bold=True)
            ly += 13
        ry += 46


def bottom_band(cv):
    y0 = 648
    draw_text(cv, 20, y0, "WHERE IT HAPPENED", 1, RED, bold=True)
    draw_text(cv, 510, y0, "ALSO ON WEDNESDAY 18 NOVEMBER", 1, BLUE, bold=True)
    cv.rect(20, y0 + 15, 470, 2, RED)
    cv.rect(510, y0 + 15, 494, 2, BLUE)
    # world map + caption
    world_map(cv, 20, y0 + 22, 470, 230, DOTS)
    draw_text(cv, 20, y0 + 258, "1 KERCH  2 KYIV  3 BAHRAIN  4 QESHM", 1, INK, bold=True)
    draw_text(cv, 20, y0 + 272, "5 KUWAIT  6 SHENZHEN  7 MANILA", 1, INK, bold=True)
    draw_text(cv, 20, y0 + 286, "8 ANTALYA  9 TURIN  10 PARIS", 1, INK, bold=True)
    draw_text(cv, 20, y0 + 300, "11 WASHINGTON  12 DELHI", 1, INK, bold=True)
    # ALSO list: 26 lines at 12px pitch, bulleted (no numbers).
    ay = y0 + 20
    for item in ALSO:
        draw_text(cv, 510, ay, "\u2022 %s" % item, 1, INK)
        ay += 12


def footer(cv):
    cv.rect(20, 984, W - 40, 2, RED)
    center(cv, 992, "EVERY STORY HAPPENED OR WAS FIRST REPORTED ON WEDNESDAY 18 NOVEMBER 2026",
           1, INK, bold=True)


def render():
    cv = Canvas(W, H, PAPER)
    # outer frame
    cv.hline(4, 4, W - 4, INK, 3)
    cv.hline(4, H - 5, W - 4, INK, 3)
    cv.vline(4, 4, H - 4, INK, 3)
    cv.vline(W - 5, 4, H - 4, INK, 3)
    masthead(cv)
    # top row: 3 cards
    for i, story in enumerate(TOP):
        top_card(cv, 20 + i * 332, 126, 320, story)
    cv.hline(20, 336, W - 20, INK, 2)
    # middle: 4 columns
    for i, (header, color, stories) in enumerate(MIDDLE):
        middle_column(cv, 20 + i * 252, 344, 228, header, color, stories)
    cv.hline(20, 642, W - 20, INK, 2)
    bottom_band(cv)
    footer(cv)
    return cv


def main():
    outdir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "output"
    os.makedirs(outdir, exist_ok=True)
    path = os.path.join(outdir, "entry.png")
    cv = render()
    cv.save_png(path)
    print("wrote %s (%d bytes, %d stories)" % (path, os.path.getsize(path), TOTAL_STORIES))


if __name__ == "__main__":
    main()
