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
     "Qeshm struck in reply; Kuwait also.", "Reuters", 50, 26),
    (3, "ASIA", "SUMMIT EVE", "shenzhen",
     "Trump flies to China for first Xi-Putin summit",
     "Meets Thursday in Shenzhen: Ukraine, trade.", "Reuters", 114, 22),
    (4, "MIDDLE EAST", "GULF WAR", "tanker",
     "US sinks five Iranian tankers",
     "Four lost in the Gulf of Oman.", "Reuters", 52, 25),
    (5, "EUROPE", "UKRAINE WAR", "refinery",
     "Russia refining nearly halved",
     "Drones hit 15 of 35 refineries.", "Reuters", 37, 55),
    (6, "AMERICAS", "MARKETS", "chip",
     "Nvidia beats forecast",
     "Revenue $115.8B, up 103%.", "Bloomberg", -122, 37),
    (7, "EUROPE", "EARTHQUAKE", "quake",
     "Romania quake, magnitude 5.3",
     "Felt in Moldova and Ukraine.", "AFP", 26, 44),
    (8, "MIDDLE EAST", "ISRAEL", "parliament",
     "Knesset picks new speaker",
     "Kahana takes the chair, 66–52.", "AP", 35, 32),
    (9, "MIDDLE EAST", "MISSILES", "missiles",
     "Houthis fire missiles at Riyadh",
     "Aimed at the Saudi capital.", "AFP", 47, 25),
    (10, "AMERICAS", "MARKETS", "chart_down",
     "S&P 500 falls for 4th day",
     "Lowest close since July.", "AP", -74, 41),
    (11, "EUROPE", "TENNIS", "tennis",
     "Zverev books ATP Finals semis",
     "Beat Shelton 6-2, 7-6 in Turin.", "AP", 7, 45),
    (12, "WORLD", "CLIMATE", "globe",
     "COP31 draft splits the talks",
     "The phaseout wording divides.", "AP", 30, 37),
    (13, "ASIA", "DEFENCE", "jet",
     "Taiwan awaits $14B arms sale OK",
     "Needs Washington's sign-off.", "Reuters", 121, 25),
]

# n, region, place, headline, source, lon, lat
# Brief texts are kept short so each fits two lines at scale 0.85 in a
# 170px column (verified with wrap_text before submitting).
BRIEFS = [
    (14, "EUROPE", "Rome", "Italy passes antisemitism law", "AP", 12, 42),
    (15, "ASIA", "Tokyo", "Japan airspace breach", "Reuters", 140, 36),
    (16, "MIDDLE EAST", "Tehran", "Iran closes Hormuz to shipping", "Reuters", 51, 36),
    (17, "AMERICAS", "DC", "Trump warns of 'dirty bomb' plot", "AP", -77, 39),
    (18, "MIDDLE EAST", "Gaza", "UN warns of cold deaths", "AP", 34, 31),
    (19, "MIDDLE EAST", "Kuwait", "Downs drone wave", "Reuters", 48, 29),
    (20, "ASIA", "Asia", "Stocks snap losing run", "Bloomberg", 100, 25),
    (21, "AMERICAS", "US", "Dollar hits a 19-month high", "Reuters", -100, 39),
    (22, "WORLD", "World", "Bitcoin holds near $64,500", "Bloomberg", -80, 35),
    (23, "AMERICAS", "US", "Anthropic prices IPO at $83", "Bloomberg", -121, 38),
    (24, "EUROPE", "Madrid", "Alcaraz tops group, semis bound", "AP", -4, 40),
    (25, "OCEANIA", "Pacific", "Island states want $500M", "AFP", 165, -12),
    (26, "WORLD", "World", "M1.1 solar flare recorded", "AP", 0, 45),
    (27, "AMERICAS", "US", "Loses measles-free status", "AP", -95, 42),
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
    (39, "MIDDLE EAST", "Yemen", "Houthis advance on Aden", "Reuters", 45, 13),
    (40, "ASIA", "Beijing", "Xi: tear down trade barriers", "Reuters", 116, 40),
    (41, "AMERICAS", "DC", "Trump pulls FDA nominee Overton", "AP", -77, 39),
    (42, "EUROPE", "Turin", "Tiafoe routs Cobolli", "AP", 7, 45),
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
    figures = ["5 tankers sunk", "$14B arms sale", "$64,500 Bitcoin",
               "$115.8B Nvidia", "80% malaria down", "M1.1 solar flare"]
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
    h = 190
    cv.rect(x, y, w, h, CARD)
    cv.hline(x, x + w, y, INK, 1)
    cv.hline(x, x + w, y + h - 1, INK, 1)
    cv.vline(x, y, y + h - 1, INK, 1)
    cv.vline(x + w - 1, y, y + h - 1, INK, 1)
    MINIS[mini](cv, x + 4, y + 4, w - 8, 66)
    strip(cv, x + 4, y + 74, w - 8, n, region, topic, src,
          REGION_COLOR[region], scale=0.9)
    lines = wrap_text(headline, 1.6, w - 12, bold=True, font="serif")
    hy = y + 102
    for ln in lines[:2]:
        draw_text(cv, x + 6, hy, ln, 1.6, INK, bold=True, font="serif")
        hy += 24
    dlines = wrap_text(deck, 1, w - 12, font="serif")
    dy = y + 156
    for ln in dlines[:2]:
        draw_text(cv, x + 6, dy, ln, 1, MUTED, font="serif")
        dy += 13


def small_card(cv, x, y, w, feat):
    n, region, topic, mini, headline, deck, src, _, _ = feat
    h = 119
    cv.rect(x, y, w, h, CARD)
    cv.hline(x, x + w, y, INK, 1)
    cv.hline(x, x + w, y + h - 1, INK, 1)
    cv.vline(x, y, y + h - 1, INK, 1)
    cv.vline(x + w - 1, y, y + h - 1, INK, 1)
    MINIS[mini](cv, x + 3, y + 3, w - 6, 34)
    # strip: number + region only (topic does not fit with the source)
    cv.rect(x + 3, y + 37, w - 6, 15, REGION_COLOR[region])
    draw_text(cv, x + 9, y + 39, "%d · %s" % (n, region), 0.8,
              (255, 255, 255), bold=True)
    draw_text(cv, x + w - 9, y + 39, src, 0.8, (255, 255, 255), bold=True,
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
    # dotted world map, pass 4: only two single pins (6/10 Americas)
    # sit on the map as red circles with white halos. Shenzhen 3 and
    # Taiwan 13 are 7 degrees apart, so they are leader pins: a small
    # red dot at the true spot + a numbered chip in clear ocean with a
    # thin grey leader line. The nine Europe/Middle East featured
    # stories are keyed by place below the map (a standard newspaper
    # device); brief dots for Europe/Middle East are left off the map
    # entirely, so the region reads clean instead of a touching blob.
    # The remaining brief dots are placed collision-free (white halos,
    # never overlapping a pin, a chip, or another dot).
    pins = [(lon, lat, n) for (n, _, _, _, _, _, _, lon, lat) in FEATURED
            if n in (6, 10)]
    leaders = [(114, 22, 3, 118, 8), (121, 25, 13, 136, 18)]
    dots = [(lon, lat, REGION_COLOR[r])
            for (_, r, _, _, _, lon, lat) in BRIEFS
            if r not in ("EUROPE", "MIDDLE EAST")]
    mx, my, mw, mh = 20, y0 + 24, 380, 164
    dropped = world_map_dotted(cv, mx, my, mw, mh, pins, dots, leaders)
    assert not dropped, dropped
    # legend under the map, two lines of region colours only
    lx, ly = 20, y0 + 192
    for name, color in REGIONS[:4]:
        cv.circle(lx + 4, ly + 6, 4, color)
        lx += 11
        draw_text(cv, lx, ly, name, 0.85, INK, bold=True)
        lx += int(text_w(name, 0.85, bold=True)) + 10
    lx, ly = 20, y0 + 208
    for name, color in REGIONS[4:]:
        cv.circle(lx + 4, ly + 6, 4, color)
        lx += 11
        draw_text(cv, lx, ly, name, 0.85, INK, bold=True)
        lx += int(text_w(name, 0.85, bold=True)) + 10
    # one clean caption line under the legend: what the red pins are
    # and what the dots are (no text floating inside the map panel)
    draw_text(cv, 20, y0 + 224, "Red pins:", 0.85, RED, bold=True)
    draw_text(cv, 20 + int(text_w("Red pins: ", 0.85, bold=True)), y0 + 224,
              "3 · 6 · 10 · 13 — dots: briefs outside the key",
              0.85, MUTED)
    # Europe & Middle East key: red number chips + place names, two rows
    draw_text(cv, 20, y0 + 240, "EUROPE & THE MIDDLE EAST", 0.9,
              RED, bold=True)
    key_rows = [[(1, "Kerch"), (2, "Bahrain"), (4, "Gulf"), (5, "Russia"),
                 (7, "Romania")],
                [(8, "Knesset"), (9, "Riyadh"), (11, "Turin"), (12, "COP31")]]
    for ri, row in enumerate(key_rows):
        kx = 20
        ky = y0 + 254 + ri * 17
        for num, place in row:
            nw = int(text_w(str(num), 0.9, bold=True)) + 6
            cv.rect(kx, ky, nw, 15, RED)
            draw_text(cv, kx + 3, ky + 2, str(num), 0.9, (255, 255, 255),
                      bold=True)
            draw_text(cv, kx + nw + 4, ky + 1, place, 0.85, INK, bold=True)
            kx += nw + 4 + int(text_w(place, 0.85, bold=True)) + 14
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
    # exactly 2 lines: the eight cut stories are named, like top 1's list
    cv.rect(20, 952, 984, 40, (255, 255, 255))
    cv.hline(20, 1004, 952, RED, 2)
    cv.hline(20, 1004, 991, RED, 2)
    cv.vline(20, 952, 991, RED, 2)
    cv.vline(1003, 952, 991, RED, 2)
    draw_text(cv, 30, 958, "DATE CHECK", 1, RED, bold=True)
    msg = ("Left out on purpose — the first Kerch strike fell on "
           "Tuesday 17 November; the second strike is story 1. Cut: "
           "Antalya AI pledge · Rubio outages · Navy chief grilled "
           "· Fed's Williams · Pakistan at the UN · Nvidia export panel "
           "· Apple glitches · FAA installs.")
    lines = wrap_text(msg, 1, 984 - 140)
    ly = 958
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
    # 3 big leads: 316 wide, 16px gaps, so the row breathes
    for i, feat in enumerate(FEATURED[:3]):
        lead_card(cv, 20 + i * 332, 188, 316, feat)
    # 10 smaller in 2 rows of 5
    for r in range(2):
        for c in range(5):
            feat = FEATURED[3 + r * 5 + c]
            small_card(cv, 20 + c * 199, 386 + r * 127, 187, feat)
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
