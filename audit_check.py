"""Pass-4 audit checks for news-image-20261118 (run BEFORE/AFTER fixes).

Programmatic checks over main.py data + font metrics. Run from the repo dir:
    python3 audit_check.py
Exit 0 = all checks pass, 1 = failures listed.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from draw import text_w, wrap_text  # noqa: E402
import main as M  # noqa: E402

fails = []


def check(name, ok, detail=""):
    print(("PASS " if ok else "FAIL ") + name + ((" — " + detail) if detail else ""))
    if not ok:
        fails.append(name)


# 1. tally counts
counts = {}
for feat in M.FEATURED:
    counts[feat[1]] = counts.get(feat[1], 0) + 1
for b in M.BRIEFS:
    counts[b[1]] = counts.get(b[1], 0) + 1
for name, c in M.TALLY:
    check("tally %s == %d" % (name, c), counts.get(name, 0) == c,
          "counted %d" % counts.get(name, 0))
check("tally total 45", sum(c for _, c in M.TALLY) == 45)
check("stories total 45", len(M.FEATURED) + len(M.BRIEFS) == 45)
check("featured 13 / briefs 32", len(M.FEATURED) == 13 and len(M.BRIEFS) == 32)

# 2/3. lead + small card wraps
for feat in M.FEATURED[:3]:
    n = feat[0]
    hl = wrap_text(feat[4], 1.6, 316 - 12, bold=True, font="serif")
    dk = wrap_text(feat[5], 1, 316 - 12, font="serif")
    check("lead %d headline <=2 lines" % n, len(hl) <= 2, "%d lines" % len(hl))
    check("lead %d deck 1 line" % n, len(dk) == 1, "%d lines: %s" % (len(dk), dk))
for feat in M.FEATURED[3:]:
    n = feat[0]
    hl = wrap_text(feat[4], 1.15, 187 - 10, bold=True, font="serif")
    dk = wrap_text(feat[5], 0.9, 187 - 10, font="serif")
    check("card %d headline <=2 lines" % n, len(hl) <= 2, "%d lines" % len(hl))
    check("card %d deck 1 line" % n, len(dk) == 1, "%d lines: %s" % (len(dk), dk))

# 4. briefs
for b in M.BRIEFS:
    n, _, place, headline, src, _, _ = b
    text = "%s: %s · %s" % (place, headline, src)
    lines = wrap_text(text, 0.85, 170)
    check("brief %d <=2 lines" % n, len(lines) <= 2, "%d lines" % len(lines))
    check("brief %d no double space" % n, "  " not in text, text)
    # place word must not repeat at headline start
    first = headline.split()[0].strip("'\"").lower().rstrip(":")
    check("brief %d no place-word repeat" % n,
          first != place.lower().strip("'\""),
          "%s / %s" % (place, headline))

# 5. DATE CHECK
msg = ("Left out on purpose — the first Kerch strike fell on "
       "Tuesday 17 November; the second strike is story 1. Cut: "
       "Antalya AI pledge · Rubio outages · Navy chief grilled "
       "· Fed's Williams · Pakistan at the UN · Nvidia export panel "
       "· Apple glitches · FAA installs.")
lines = wrap_text(msg, 1, 984 - 140)
check("DATE CHECK exactly 2 lines", len(lines) == 2, "%d lines" % len(lines))
cut = msg.split("Cut: ", 1)[1].split(" · ")
check("DATE CHECK names 8 cut stories", len(cut) == 8, str(cut))

# 6. numbers strip width
label = "THE DAY IN NUMBERS:"
x = 20 + int(text_w(label, 1, bold=True)) + 12
figs = ["5 tankers sunk", "$14B arms sale", "$64,500 Bitcoin",
        "$115.8B Nvidia", "80% malaria down", "M1.1 solar flare"]
for i, fig in enumerate(figs):
    x += int(text_w(fig, 1, bold=True))
    if i < len(figs) - 1:
        x += int(text_w("  ·  ", 1, bold=True))
check("numbers strip ends < 1004", x < 1004, "ends x=%d" % x)
# each figure must appear in a story on the page
page_text = " ".join([f[4] + " " + f[5] for f in M.FEATURED] +
                     [b[3] for b in M.BRIEFS])
for fig in figs:
    key = fig.split()[0].strip("$") if "Nvidia" not in fig else "115.8"
    check("strip figure backed on page: %s" % fig,
          key in page_text or fig.split()[0] in page_text, "")

# 7. masthead title width
tw = text_w("Wednesday 18 November 2026", 2.6, True, "serif")
check("masthead title fits", 104 + tw < 1014, "w=%d" % tw)

# 8. key rows width
key_rows = [[(1, "Kerch"), (2, "Bahrain"), (4, "Gulf"), (5, "Russia"),
             (7, "Romania")],
            [(8, "Knesset"), (9, "Riyadh"), (11, "Turin"), (12, "COP31")]]
for ri, row in enumerate(key_rows):
    kx = 20
    for num, place in row:
        nw = int(text_w(str(num), 0.9, bold=True)) + 6
        kx += nw + 4 + int(text_w(place, 0.85, bold=True)) + 14
    check("key row %d width < 400" % (ri + 1), kx - 14 < 400, "w=%d" % (kx - 14))

# 9. caption line width
cap = "Red pins: 3 · 6 · 10 · 13 — dots: briefs outside the key"
check("caption width < 380", text_w(cap, 0.85) < 380, "w=%d" % text_w(cap, 0.85))

# 10. map geometry: use the REAL layout function with the REAL inputs
import math
from maps import layout_world_points
mx, my, mw, mh = 20, 664, 380, 164
pins = [(lon, lat, n) for (n, _, _, _, _, _, _, lon, lat) in M.FEATURED
        if n in (6, 10)]
leaders = [(114, 22, 3, 118, 8), (121, 25, 13, 136, 18)]
dots = [(lon, lat, M.REGION_COLOR[r])
        for (_, r, _, _, _, lon, lat) in M.BRIEFS
        if r not in ("EUROPE", "MIDDLE EAST")]
pin_draws, dot_draws, dropped = layout_world_points(
    mx, my, mw, mh, pins, dots, leaders)
check("map: no dots dropped", not dropped, str(dropped))
print("brief dots on map: %d (of 32; Europe/ME briefs keyed, not dotted)"
      % len(dot_draws))
halos = []  # (cx, cy, radius) circles dots must clear
rects = []  # (x0, y0, x1, y1) chip rects with margin
for pd in pin_draws:
    if pd["kind"] == "pin":
        halos.append((pd["cx"], pd["cy"], pd["r"] + 3))
    else:
        halos.append((pd["dx"], pd["dy"], 6))
        rects.append((pd["cx"] - 3, pd["cy"] - 3,
                      pd["cx"] + pd["cw"] + 3, pd["cy"] + pd["ch"] + 3))
for k, (px, py, _c) in enumerate(dot_draws):
    for (hx, hy, hr) in halos:
        d = math.dist((px, py), (hx, hy))
        check("dot %d clear of pin halo" % k, d >= hr + 4.5, "d=%.1f" % d)
    for (rx0, ry0, rx1, ry1) in rects:
        check("dot %d clear of chip rect" % k,
              not (rx0 <= px <= rx1 and ry0 <= py <= ry1),
              "dot at (%d,%d)" % (px, py))
for i in range(len(dot_draws)):
    for j in range(i + 1, len(dot_draws)):
        d = math.dist(dot_draws[i][:2], dot_draws[j][:2])
        check("dot-dot %d/%d >= 7.5px" % (i, j), d >= 7.5, "d=%.1f" % d)
ld = [pd for pd in pin_draws if pd["kind"] == "leader"]
check("leader dots >= 7px apart",
      math.dist((ld[0]["dx"], ld[0]["dy"]), (ld[1]["dx"], ld[1]["dy"])) >= 7,
      "")
a, b = ld
gap = max(b["cx"] - (a["cx"] + a["cw"]), a["cx"] - (b["cx"] + b["cw"]),
          b["cy"] - (a["cy"] + a["ch"]), a["cy"] - (b["cy"] + b["ch"]))
check("leader chips do not touch", gap >= 2, "gap=%.1f" % gap)

# 11. sources used vs sources line
used = set([f[6] for f in M.FEATURED] + [b[4] for b in M.BRIEFS])
check("sources line covers all used", used <= {"Reuters", "AP", "AFP", "Bloomberg", "BBC"},
      str(sorted(used)))

# 12. deck echo scan: shared content words headline vs deck
STOP = {"the", "a", "an", "of", "in", "on", "at", "to", "for", "and", "vs",
        "is", "are", "was", "its", "it", "as", "by", "with", "from"}
for feat in M.FEATURED:
    n = feat[0]
    hw = set(w.strip(".,'\"").lower() for w in feat[4].split()) - STOP
    dw = set(w.strip(".,'\"").lower() for w in feat[5].split()) - STOP
    shared = hw & dw
    # allow number/place carry-overs only if deck adds new info words
    check("card %d deck no headline echo" % n, not shared,
          "shared: %s" % sorted(shared))

print()
print("FAILURES: %d" % len(fails))
for f in fails:
    print("  - " + f)
sys.exit(1 if fails else 0)
