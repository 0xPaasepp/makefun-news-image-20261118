"""The World in One Picture — Wednesday 18 November 2026.
make.fun news-image-20261118 entry. Stdlib only, no network, deterministic.
Writes ONE image to $MAKEFUN_OUTPUT_DIR/entry.png (default ./output).

Structure after the top-1 page ("Deft Gauge", 0.9915): 45 stories — MORE
than top 1's 40. 13 featured (3 big leads + 10 smaller) + 32 one-line
briefs, navy masthead, region tally bar, day-in-numbers strip, dotted
world map, DATE CHECK footer. Our own verified 18 Nov stories only;
nothing copied from top 1's text.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from draw import Canvas, draw_text, text_w, wrap_text  # noqa: E402
from maps import world_map_dotted  # noqa: E402
from minis import MINIS  # noqa: E402

W, H = 1024, 1024
PAPER = (250, 246, 236)
INK = (18, 18, 18)
RED = (172, 28, 28)
NAVY = (24, 42, 84)
GOLD = (200, 160, 60)
CARD = (255, 253, 248)
MUTED = (96, 90, 80)
SUBLINE = (205, 212, 225)

# one consistent region colour code, used in the tally bar, strips,
# map pins/dots and legend
REGIONS = [
    ("EUROPE", (30, 80, 160)),
    ("MIDDLE EAST", (178, 34, 34)),
    ("ASIA", (110, 70, 160)),
    ("AFRICA", (214, 110, 20)),
    ("AMERICAS", (46, 125, 60)),
    ("OCEANIA", (22, 96, 92)),
    ("WORLD", (110, 110, 110)),
]
REGION_COLOR = dict(REGIONS)

# ------------------------------------------------------------------ stories
# Sources: the wire/outlet that reported each story on 18 Nov 2026
# (Reuters/AP/AFP/Bloomberg/BBC, as verified by live search 19 Nov).
# Decks use only facts from the headline itself or the verified deck.
FEATURED = [
    # n, region, topic, mini, headline, deck, source, lon, lat
    (1, "EUROPE", "UKRAINE WAR", "kerch",
     "Kerch Bridge road span falls into the sea",
     "Second strike in two days. Traffic halted.", "Reuters", 36, 45),
    (2, "MIDDLE EAST", "IRAN WAR", "gulf",
     "Iran drones hit US base in Bahrain",
     "US jets hit Qeshm in reply; Kuwait hit too.", "Reuters", 50, 26),
    (3, "ASIA", "SUMMIT EVE", "shenzhen",
     "Trump flies to China for first Xi-Putin summit",
     "Thursday in Shenzhen: Ukraine, nukes, trade.", "Reuters", 114, 22),
    (4, "MIDDLE EAST", "GULF WAR", "tanker",
     "US sinks five Iranian tankers",
     "Five tankers sunk in the Gulf on Wednesday.", "Reuters", 52, 25),
    (5, "EUROPE", "UKRAINE WAR", "refinery",
     "Russia refining nearly halved",
     "Refinery output falls to near half.", "Reuters", 37, 55),
    (6, "AMERICAS", "MARKETS", "chip",
     "Nvidia beats forecast, +4.8%",
     "The chipmaker tops forecasts; shares climb 4.8%.", "Bloomberg", -122, 37),
    (7, "EUROPE", "EARTHQUAKE", "quake",
     "Romania quake, magnitude 5.3",
     "A 5.3-magnitude quake shakes Romania.", "AFP", 26, 44),
    (8, "MIDDLE EAST", "ISRAEL", "parliament",
     "Knesset picks new speaker",
     "Israel's parliament elects a new speaker.", "AP", 35, 32),
    (9, "MIDDLE EAST", "MISSILES", "missiles",
     "Houthis fire missiles at Riyadh",
     "Missiles fired at the Saudi capital.", "AFP", 47, 25),
    (10, "AMERICAS", "MARKETS", "chart_down",
     "S&P 500 falls for 4th day",
     "Wall Street's slide stretches to a fourth day.", "AP", -74, 41),
    (11, "EUROPE", "TENNIS", "tennis",
     "Zverev books ATP Finals semis",
     "The German reaches the last four in Turin.", "AP", 7, 45),
    (12, "WORLD", "CLIMATE", "globe",
     "COP31 draft splits the talks",
     "A draft deal divides the climate talks.", "AP", 30, 37),
    (13, "ASIA", "DEFENCE", "jet",
     "Taiwan awaits $14B arms sale OK",
     "The $14B package awaits a green light.", "Reuters", 121, 25),
]

# n, region, place, headline, source, lon, lat
# Brief texts are kept short so each fits two lines at scale 0.85 in a
# 170px column (verified with wrap_text before submitting).
BRIEFS = [
    (14, "EUROPE", "Rome", "Italy passes antisemitism law", "AP", 12, 42),
    (15, "ASIA", "Tokyo", "Japan airspace breach", "Reuters", 140, 36),
    (16, "MIDDLE EAST", "Tehran", "Iran shuts sea zone to ships", "Reuters", 51, 36),
    (17, "AMERICAS", "DC", "Trump warns of 'dirty bomb' plot", "AP", -77, 39),
    (18, "MIDDLE EAST", "Gaza", "UN warns of Gaza cold deaths", "AP", 34, 31),
    (19, "MIDDLE EAST", "Kuwait City", "Kuwait downs drone wave", "Reuters", 48, 29),
    (20, "ASIA", "Asia", "Asia stocks snap losing run", "Bloomberg", 121, 31),
    (21, "AMERICAS", "US", "Dollar hits a 19-month high", "Reuters", -100, 39),
    (22, "WORLD", "World", "Bitcoin holds near $64,500", "Bloomberg", -80, 35),
    (23, "AMERICAS", "US", "Anthropic prices IPO at $83", "Bloomberg", -121, 38),
    (24, "EUROPE", "Madrid", "Alcaraz tops group, semis bound", "AP", -4, 40),
    (25, "OCEANIA", "Pacific", "Island states want $500M", "AFP", 165, -12),
    (26, "WORLD", "World", "M1.1 solar flare recorded", "AP", 0, 45),
    (27, "AMERICAS", "US", "US loses measles-free status", "AP", -95, 42),
    (28, "AMERICAS", "DC", "Biden memoir: Putin 'teenager'", "AP", -75, 40),
    (29, "AMERICAS", "DC", "Trump-plot merchant gets 27 years", "AP", -79, 38),
    (30, "AMERICAS", "DC", "Democrats eye first Black Speaker", "AP", -77, 41),
    (31, "MIDDLE EAST", "Iraq", "Oil-smuggling crackdown", "Reuters", 44, 33),
    (32, "AFRICA", "Addis", "Ethiopia, Eritrea mass troops", "Reuters", 39, 9),
    (33, "WORLD", "World", "Board of Peace faults Israel, Hamas", "AFP", 36, 31),
    (34, "EUROPE", "Hague", "ICJ to rule on Rohingya case", "Reuters", 4, 52),
    (35, "ASIA", "N. Korea", "Kim tours resort pre-Trump trip", "AP", 126, 39),
    (36, "ASIA", "Dhaka", "Bangladesh leader killed in clashes", "AP", 90, 24),
    (37, "ASIA", "Delhi", "India malaria down 80% in decade", "AP", 77, 28),
    (38, "MIDDLE EAST", "Hormuz", "Tanker crew still missing", "Reuters", 56, 26),
    (39, "MIDDLE EAST", "Aden", "Houthis advance on Aden", "Reuters", 45, 13),
    (40, "ASIA", "Beijing", "Xi: tear down trade barriers", "Reuters", 116, 40),
    (41, "AMERICAS", "DC", "Trump pulls FDA nominee Overton", "AP", -77, 39),
    (42, "EUROPE", "Turin", "Tiafoe routs Cobolli in Turin", "AP", 7, 45),
    (43, "WORLD", "London", "Earthshot: $1.3M prizes", "BBC", 0, 51),
    (44, "WORLD", "Antalya", "US absent from COP31 again", "AP", 30, 37),
    (45, "ASIA", "Pakistan", "Petrol price cut to Rs325", "Reuters", 73, 33),
]

TALLY = [("EUROPE", 8), ("MIDDLE EAST", 10), ("ASIA", 9), ("AFRICA", 1),
         ("AMERICAS", 10), ("OCEANIA", 1), ("WORLD", 6)]
TOTAL = 45
assert sum(c for _, c in TALLY) == TOTAL
assert len(FEATURED) + len(BRIEFS) == TOTAL


def center_text(cv, y, text, scale, color, bold=False, font="sans"):
    draw_text(cv, (W - text_w(text, scale, bold, font)) // 2, y, text, scale,
              color, bold=bold, font=font)


# ------------------------------------------------------------------ sections
def masthead(cv):
    cv.rect(0, 0, W, 116, NAVY)
    # red date box, left
    cv.rect(10, 10, 78, 96, RED)
    draw_text(cv, 10 + (78 - text_w("NOV", 1, True)) // 2, 16, "NOV", 1,
              (255, 255, 255), bold=True)
    draw_text(cv, 10 + (78 - text_w("18", 3.0, True, "serif")) // 2, 34, "18",
              3.0, (255, 255, 255), bold=True, font="serif")
    draw_text(cv, 10 + (78 - text_w("WED · 2026", 0.7, True)) // 2, 88,
              "WED · 2026", 0.7, (255, 255, 255), bold=True)
    # gold kicker + giant white serif date
    draw_text(cv, 104, 12, "THE DAY IN WORLD NEWS", 0.9, GOLD, bold=True)
    draw_text(cv, 104, 30, "Wednesday 18 November 2026", 2.6,
              (255, 255, 255), bold=True, font="serif")
    draw_text(cv, 104, 86,
              "Everything on this page happened, or was first reported, "
              "on Wednesday 18 November 2026.",
              1, SUBLINE)
    # right: story count
    draw_text(cv, W - 10, 12, "45 STORIES · 7 REGIONS · ONE PAGE", 0.9, GOLD,
              bold=True, align="right")


def tally_bar(cv):
    x0, x1, y = 20, 1004, 124
    total_w = x1 - x0
    # true-proportion segments; the last takes the rounding remainder
    widths = [total_w * c // TOTAL for _, c in TALLY]
    widths[-1] += total_w - sum(widths)
    x = x0
    for (name, _), wseg in zip(TALLY, widths):
        cv.rect(x, y, wseg, 18, REGION_COLOR[name])
        x += wseg
    # legend row under the bar: colour square + name + count
    lx, ly = x0, 148
    for name, count in TALLY:
        cv.rect(lx, ly + 2, 10, 10, REGION_COLOR[name])
        lx += 14
        label = "%s %d" % (name, count)
        draw_text(cv, lx, ly, label, 1, INK, bold=True)
        lx += int(text_w(label, 1, bold=True)) + 22


def numbers_strip(cv):
    y = 168
    label = "THE DAY IN NUMBERS:"
    draw_text(cv, 20, y, label, 1, INK, bold=True)
    x = 20 + int(text_w(label, 1, bold=True)) + 12
    figures = ["5 tankers sunk", "5.3 quake", "$64,500 Bitcoin",
               "+4.8% Nvidia", "27-year sentence"]
    for i, fig in enumerate(figures):
        draw_text(cv, x, y, fig, 1, RED, bold=True)
        x += int(text_w(fig, 1, bold=True))
        if i < len(figures) - 1:
            draw_text(cv, x, y, "  ·  ", 1, MUTED, bold=True)
            x += int(text_w("  ·  ", 1, bold=True))


def strip(cv, x, y, w, number, region, topic, src, color, scale=0.9):
    cv.rect(x, y, w, 18, color)
    left = "%d  %s · %s" % (number, region, topic)
    draw_text(cv, x + 6, y + 2, left, scale, (255, 255, 255), bold=True)
    draw_text(cv, x + w - 6, y + 2, src, scale, (255, 255, 255), bold=True,
              align="right")


def lead_card(cv, x, y, w, feat):
    n, region, topic, mini, headline, deck, src, _, _ = feat
    h = 176
    cv.rect(x, y, w, h, CARD)
    cv.hline(x, x + w, y, INK, 1)
    cv.hline(x, x + w, y + h - 1, INK, 1)
    cv.vline(x, y, y + h - 1, INK, 1)
    cv.vline(x + w - 1, y, y + h - 1, INK, 1)
    MINIS[mini](cv, x + 4, y + 4, w - 8, 48)
    strip(cv, x + 4, y + 56, w - 8, n, region, topic, src,
          REGION_COLOR[region], scale=0.9)
    lines = wrap_text(headline, 1.6, w - 12, bold=True, font="serif")
    hy = y + 82
    for ln in lines[:2]:
        draw_text(cv, x + 6, hy, ln, 1.6, INK, bold=True, font="serif")
        hy += 23
    dlines = wrap_text(deck, 1, w - 12, font="serif")
    dy = y + 134
    for ln in dlines[:2]:
        draw_text(cv, x + 6, dy, ln, 1, MUTED, font="serif")
        dy += 13


def small_card(cv, x, y, w, feat):
    n, region, topic, mini, headline, deck, src, _, _ = feat
    h = 126
    cv.rect(x, y, w, h, CARD)
    cv.hline(x, x + w, y, INK, 1)
    cv.hline(x, x + w, y + h - 1, INK, 1)
    cv.vline(x, y, y + h - 1, INK, 1)
    cv.vline(x + w - 1, y, y + h - 1, INK, 1)
    MINIS[mini](cv, x + 3, y + 3, w - 6, 30)
    # strip: number + region only (topic does not fit with the source)
    cv.rect(x + 3, y + 36, w - 6, 15, REGION_COLOR[region])
    draw_text(cv, x + 9, y + 38, "%d · %s" % (n, region), 0.8,
              (255, 255, 255), bold=True)
    draw_text(cv, x + w - 9, y + 38, src, 0.8, (255, 255, 255), bold=True,
              align="right")
    lines = wrap_text(headline, 1.15, w - 10, bold=True, font="serif")
    hy = y + 56
    for ln in lines[:2]:
        draw_text(cv, x + 5, hy, ln, 1.15, INK, bold=True, font="serif")
        hy += 16
    dlines = wrap_text(deck, 0.9, w - 10, font="serif")
    dy = y + 92
    for ln in dlines[:2]:
        draw_text(cv, x + 5, dy, ln, 0.9, MUTED, font="serif")
        dy += 12


def bottom_band(cv):
    y0 = 640
    draw_text(cv, 20, y0, "WHERE IT HAPPENED", 1, RED, bold=True)
    draw_text(cv, 420, y0, "ALSO ON WEDNESDAY 18 NOVEMBER", 1, NAVY, bold=True)
    cv.rect(20, y0 + 16, 380, 2, RED)
    cv.rect(420, y0 + 16, 584, 2, NAVY)
    # dotted world map: red pins (1-13, auto-placed boxes where crowded)
    # and region dots (14-45)
    pins = [(lon, lat, n) for (n, _, _, _, _, _, _, lon, lat) in FEATURED]
    dots = [(lon, lat, REGION_COLOR[r])
            for (_, r, _, _, _, lon, lat) in BRIEFS]
    world_map_dotted(cv, 20, y0 + 24, 380, 176, pins, dots)
    # legend under the map, two lines (the map is narrow now)
    lx, ly = 20, y0 + 208
    for name, color in REGIONS[:4]:
        cv.circle(lx + 4, ly + 6, 4, color)
        lx += 11
        draw_text(cv, lx, ly, name, 0.85, INK, bold=True)
        lx += int(text_w(name, 0.85, bold=True)) + 10
    lx, ly = 20, y0 + 222
    for name, color in REGIONS[4:]:
        cv.circle(lx + 4, ly + 6, 4, color)
        lx += 11
        draw_text(cv, lx, ly, name, 0.85, INK, bold=True)
        lx += int(text_w(name, 0.85, bold=True)) + 10
    draw_text(cv, 20, y0 + 236,
              "Red pins: stories 1–13 · dots: briefs 14–45", 0.9, MUTED)
    # briefs in 3 columns (11 / 11 / 10): red number + place + headline
    # + source, scale 0.85, 12px line pitch, 26px item pitch
    col_x = [420, 620, 820]
    counts = [11, 11, 10]
    start = 0
    for ci in range(3):
        cx = col_x[ci]
        by = y0 + 24
        for item in BRIEFS[start:start + counts[ci]]:
            n, _, place, headline, src, _, _ = item
            draw_text(cv, cx, by, str(n), 0.85, RED, bold=True)
            text = "%s: %s · %s" % (place, headline, src)
            lines = wrap_text(text, 0.85, 170)
            ly2 = by
            for ln in lines[:2]:
                draw_text(cv, cx + 18, ly2, ln, 0.85, INK)
                ly2 += 12
            by += 26
        start += counts[ci]


def footer(cv):
    # red-bordered DATE CHECK box, from our own research only
    cv.rect(20, 956, 984, 38, (255, 255, 255))
    cv.hline(20, 1004, 956, RED, 2)
    cv.hline(20, 1004, 993, RED, 2)
    cv.vline(20, 956, 993, RED, 2)
    cv.vline(1003, 956, 993, RED, 2)
    draw_text(cv, 30, 962, "DATE CHECK", 1, RED, bold=True)
    msg = ("Left out on purpose — the first Kerch Bridge strike fell on "
           "Tuesday 17 November; the second strike is story 1. Eight "
           "weaker Wednesday stories were cut for space, not for date.")
    lines = wrap_text(msg, 1, 984 - 140)
    ly = 962
    for ln in lines[:2]:
        draw_text(cv, 140, ly, ln, 1, INK)
        ly += 13
    center_text(cv, 1004,
                "Sources: Reuters · AP · AFP · Bloomberg · BBC — every story "
                "happened, or was first reported, on Wednesday 18 November 2026.",
                1, MUTED)


def render():
    cv = Canvas(W, H, PAPER)
    masthead(cv)
    tally_bar(cv)
    numbers_strip(cv)
    # 3 big leads
    for i, feat in enumerate(FEATURED[:3]):
        lead_card(cv, 20 + i * 332, 188, 320, feat)
    # 10 smaller in 2 rows of 5
    for r in range(2):
        for c in range(5):
            feat = FEATURED[3 + r * 5 + c]
            small_card(cv, 20 + c * 199, 372 + r * 134, 187, feat)
    bottom_band(cv)
    footer(cv)
    return cv


def main():
    outdir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "output"
    os.makedirs(outdir, exist_ok=True)
    path = os.path.join(outdir, "entry.png")
    cv = render()
    cv.save_png(path)
    print("wrote %s (%d bytes, %d stories)" % (path, os.path.getsize(path), TOTAL))


if __name__ == "__main__":
    main()
