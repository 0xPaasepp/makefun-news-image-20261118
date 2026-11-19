"""Small minimal flat pictograms for the 13 featured cards.
Each draws into a small box (w ~300 for leads, ~180 for small cards).
Flat shapes only, 2-4 bold elements per pictogram, nothing smaller
than 3px — the user rejected big crude drawings, so these stay SMALL
and minimal.
"""
import math

INK = (20, 20, 20)
RED = (178, 34, 34)
ORANGE = (214, 110, 20)
GOLD = (214, 158, 32)
NAVY = (24, 42, 84)
NIGHT = (16, 28, 56)
SEA = (40, 90, 130)


def _star(cv, cx, cy, r, color, points=8):
    for k in range(points):
        a = math.radians(k * 360 / points)
        x2 = int(cx + r * math.cos(a))
        y2 = int(cy + r * math.sin(a))
        cv.line(cx, cy, x2, y2, color, 2)
    cv.circle(cx, cy, max(2, r // 3), color)


def _sun(cv, cx, cy, r, color):
    cv.circle(cx, cy, r, color)


def mini_kerch(cv, x, y, w, h):
    """Dusk sky, bridge silhouette, explosion."""
    cv.rect(x, y, w, h, (196, 120, 90))
    cv.rect(x, y, w, h // 2, (150, 90, 130))
    _sun(cv, x + w - 34, y + 14, 9, (255, 210, 110))
    by = y + h - 14
    cv.line(x + 6, by, x + w // 2 - 14, by, INK, 4)
    cv.line(x + w // 2 + 14, by, x + w - 6, by, INK, 4)
    cv.line(x + w // 2 - 14, by, x + w // 2 - 14, by - 12, INK, 3)
    cv.line(x + w // 2 + 14, by, x + w // 2 + 14, by - 12, INK, 3)
    _star(cv, x + w // 2, by - 6, 9, (255, 120, 40))
    _star(cv, x + w // 2, by - 6, 4, RED)


def mini_gulf(cv, x, y, w, h):
    """Night sea, tanker, drone dots."""
    cv.rect(x, y, w, h, NIGHT)
    cv.rect(x, y + h - 16, w, 16, (30, 70, 110))
    cv.rect(x + 14, y + h - 26, w - 60, 10, INK)
    cv.rect(x + w - 62, y + max(2, h - 34), 18, 8, INK)
    for dx, dy in ((0.30, 12), (0.42, 8), (0.52, 16), (0.64, 10)):
        cv.circle(x + int(w * dx), y + dy, 3, (255, 90, 60))
    _star(cv, x + w - 40, y + h - 22, 7, (255, 120, 40))
    cv.circle(x + 22, y + 12, 4, (240, 240, 220))


def mini_shenzhen(cv, x, y, w, h):
    """Sunset skyline, three flags."""
    cv.rect(x, y, w, h, (240, 190, 110))
    _sun(cv, x + w - 30, y + 12, 10, (255, 220, 120))
    bw = w // 7
    for i, bh in enumerate((26, 36, 22, 40, 30, 38, 24)):
        bh = min(bh, h - 12)
        cv.rect(x + 4 + i * bw, y + h - 10 - bh, bw - 4, bh, (60, 50, 70))
    for i, col in enumerate(((200, 30, 30), (30, 60, 140), (255, 255, 255))):
        fx = x + 16 + i * 34
        cv.line(fx, y + 6, fx, y + 22, INK, 2)
        cv.rect(fx + 2, y + 6, 20, 11, col)


def mini_tanker(cv, x, y, w, h):
    """Tanker: red hull, white cabin, mast + flag — reads as a ship."""
    cv.rect(x, y, w, h, (210, 225, 235))
    cv.rect(x, y + h - 12, w, 12, SEA)
    cv.poly([(x + 16, y + h - 24), (x + w - 16, y + h - 24),
             (x + w - 26, y + h - 12), (x + 26, y + h - 12)], RED)
    cv.rect(x + w - 52, y + max(2, h - 34), 16, 10, (255, 255, 255))
    cv.line(x + 26, y + h - 24, x + 26, y + 6, INK, 2)
    cv.rect(x + 28, y + 6, 14, 8, RED)


def mini_refinery(cv, x, y, w, h):
    """Two stacks + a big red flame, sized to the box."""
    cv.rect(x, y, w, h, (235, 228, 215))
    ground = y + h - 6
    s1 = max(10, int(h * 0.55))
    s2 = max(14, int(h * 0.75))
    cv.rect(x + 16, ground - s1, 20, s1, NAVY)
    cv.rect(x + 44, ground - s2, 20, s2, NAVY)
    cv.rect(x + 14, ground, 52, 4, NAVY)
    _star(cv, x + w - 34, y + 12, 9, (255, 120, 40))
    _star(cv, x + w - 34, y + 12, 4, RED)


def mini_chip(cv, x, y, w, h):
    """Chip square + rising arrow."""
    cv.rect(x, y, w, h, (225, 235, 225))
    cx, cy = x + w // 3, y + h // 2
    cv.rect(cx - 12, cy - 12, 24, 24, NAVY)
    cv.rect(cx - 6, cy - 6, 12, 12, GOLD)
    for dx in (-18, -6, 6, 18):
        cv.line(cx + dx, cy - 16, cx + dx, cy - 12, INK, 2)
        cv.line(cx + dx, cy + 12, cx + dx, cy + 16, INK, 2)
    cv.line(x + w - 46, y + h - 10, x + w - 14, y + 10, (46, 125, 60), 3)
    cv.line(x + w - 14, y + 10, x + w - 26, y + 10, (46, 125, 60), 3)
    cv.line(x + w - 14, y + 10, x + w - 14, y + 22, (46, 125, 60), 3)


def mini_quake(cv, x, y, w, h):
    """One building, one bold zigzag crack."""
    cv.rect(x, y, w, h, (235, 228, 215))
    cv.rect(x + 14, y + 8, 40, h - 16, (120, 110, 95))
    pts = [(x + 16, y + 8), (x + 36, y + h // 2), (x + 22, y + h - 10)]
    for i in range(len(pts) - 1):
        cv.line(pts[i][0], pts[i][1], pts[i + 1][0], pts[i + 1][1], RED, 4)
    cv.rect(x + w - 36, y + h - 20, 24, 20, (120, 110, 95))


def mini_parliament(cv, x, y, w, h):
    """Pediment + three thick columns, sized to the box."""
    cv.rect(x, y, w, h, (235, 228, 215))
    ph = max(6, h // 4)
    cv.poly([(x + w // 2 - 40, y + 4), (x + w // 2 + 40, y + 4),
             (x + w // 2, y + 4 + ph)], NAVY)
    top = y + 4 + ph + 2
    bot = y + h - 6
    if bot - top >= 4:
        for i in range(3):
            cx = x + 20 + i * 26
            cv.rect(cx, top, 10, bot - top, NAVY)
    cv.rect(x + 10, bot, w - 20, 5, NAVY)


def mini_missiles(cv, x, y, w, h):
    """Night sky, two bold missile trails."""
    cv.rect(x, y, w, h, NIGHT)
    for (sx, sy) in ((0.15, 0.75), (0.5, 0.8)):
        ex = x + int(w * sx) + 30
        ey = y + int(h * sy) - 16
        cv.line(x + int(w * sx), y + int(h * sy), ex, ey, (255, 120, 60), 4)
        cv.circle(ex, ey, 4, (255, 200, 90))


def mini_chart_down(cv, x, y, w, h):
    """Three falling bars + down arrow."""
    cv.rect(x, y, w, h, (235, 228, 215))
    for i, bh in enumerate((26, 18, 10)):
        bh = min(bh, h - 10)
        cv.rect(x + 16 + i * 20, y + h - 8 - bh, 14, bh, RED)
    cv.line(x + 16, y + 10, x + w - 16, y + h - 24, RED, 4)
    cv.line(x + w - 16, y + h - 24, x + w - 30, y + h - 24, RED, 4)
    cv.line(x + w - 16, y + h - 24, x + w - 16, y + h - 38, RED, 4)


def mini_tennis(cv, x, y, w, h):
    """Tennis ball on a court band."""
    cv.rect(x, y, w, h, (225, 235, 225))
    cv.rect(x, y + h - 14, w, 14, (46, 125, 60))
    r = min(16, h // 2 - 3)
    cv.circle(x + w // 2, y + h // 2 - 2, r, (200, 220, 60))
    cv.line(x + w // 2 - 8, y + h // 2 - 14, x + w // 2 - 8,
            y + h // 2 + 10, (255, 255, 255), 3)
    cv.line(x + w // 2 + 8, y + h // 2 - 14, x + w // 2 + 8,
            y + h // 2 + 10, (255, 255, 255), 3)


def mini_globe(cv, x, y, w, h):
    """Globe + leaf."""
    cv.rect(x, y, w, h, (225, 235, 225))
    cx, cy = x + w // 2 - 6, y + h // 2
    r = min(18, h // 2 - 3)
    cv.circle(cx, cy, r, (40, 90, 130))
    cv.line(cx, cy - r, cx, cy + r, (255, 255, 255), 2)
    cv.line(cx - r, cy, cx + r, cy, (255, 255, 255), 2)
    cv.poly([(x + w - 30, y + h - 12), (x + w - 14, y + h - 26),
             (x + w - 12, y + h - 10)], (46, 125, 60))


def mini_jet(cv, x, y, w, h):
    """Fighter jet silhouette, larger."""
    cv.rect(x, y, w, h, (225, 232, 240))
    cx, cy = x + w // 2, y + h // 2
    ws = min(20, h // 2 - 4)
    cv.poly([(cx - 44, cy + 6), (cx + 34, cy - 4), (cx + 46, cy),
             (cx + 34, cy + 4), (cx - 44, cy + 10)], INK)
    cv.poly([(cx - 10, cy - 4), (cx + 4, cy - ws), (cx + 12, cy - 4)], INK)
    cv.poly([(cx - 10, cy + 8), (cx + 4, cy + ws), (cx + 12, cy + 8)], INK)
    cv.line(cx - 48, cy + 8, cx - 58, cy + 8, (255, 120, 60), 4)


MINIS = {
    "kerch": mini_kerch,
    "gulf": mini_gulf,
    "shenzhen": mini_shenzhen,
    "tanker": mini_tanker,
    "refinery": mini_refinery,
    "chip": mini_chip,
    "quake": mini_quake,
    "parliament": mini_parliament,
    "missiles": mini_missiles,
    "chart_down": mini_chart_down,
    "tennis": mini_tennis,
    "globe": mini_globe,
    "jet": mini_jet,
}
