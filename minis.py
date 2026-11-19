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
    """Dusk sky in three BRIGHT bands, bridge silhouette over the
    strait with a WIDE broken gap and a span drooping into the sea,
    big explosion, bright sea with shimmer, two boats, distant coast.
    The gap must read at a glance: the span has fallen, not intact."""
    cv.rect(x, y, w, h // 3, (178, 122, 150))
    cv.rect(x, y + h // 3, w, h // 3, (216, 150, 110))
    cv.rect(x, y + 2 * h // 3, w, h - 2 * h // 3, (240, 180, 134))
    # sun with a soft glow ring, bigger
    cv.circle(x + w - 34, y + 14, 15, (255, 224, 150))
    _sun(cv, x + w - 34, y + 14, 10, (255, 212, 112))
    # distant coast silhouette along the horizon, left
    sea_y = y + int(h * 0.62)
    cv.poly([(x, sea_y), (x + int(w * 0.30), sea_y - 10),
             (x + int(w * 0.42), sea_y - 4), (x + int(w * 0.42), sea_y),
             (x, sea_y)], (115, 80, 90))
    cv.rect(x, sea_y + 2, w, y + h - sea_y - 2, (72, 132, 176))
    # shimmer on the water, clear of the boats
    for sx, sy, sw in ((0.55, 0.72, 0.16), (0.72, 0.80, 0.12),
                       (0.58, 0.88, 0.14)):
        cv.line(x + int(w * sx), y + int(h * sy),
                x + int(w * (sx + sw)), y + int(h * sy), (185, 220, 245), 2)
    by = sea_y
    gap = 26
    # bridge deck: two thick segments with a wide gap in the middle
    cv.line(x + 6, by, x + w // 2 - gap, by, INK, 5)
    cv.line(x + w // 2 + gap, by, x + w - 6, by, INK, 5)
    # pylons at the broken ends, taller
    cv.line(x + w // 2 - gap, by, x + w // 2 - gap, by - 15, INK, 4)
    cv.line(x + w // 2 + gap, by, x + w // 2 + gap, by - 15, INK, 4)
    # fallen span: the right segment's broken end droops into the sea
    cv.line(x + w // 2 + gap, by, x + w // 2 + gap + 20, by + 12, INK, 4)
    # big explosion in the gap, brighter
    _star(cv, x + w // 2, by - 6, 12, (255, 140, 60))
    _star(cv, x + w // 2, by - 6, 6, RED)
    # two boats in the strait, clear of the blast
    bx, by2 = x + w - 66, y + h - 10
    cv.poly([(bx, by2), (bx + 26, by2), (bx + 21, by2 + 6), (bx + 5, by2 + 6)],
            INK)
    cv.rect(bx + 8, by2 - 5, 8, 5, INK)
    bx2, by3 = x + 14, y + h - 8
    cv.poly([(bx2, by3), (bx2 + 18, by3), (bx2 + 15, by3 + 5),
             (bx2 + 3, by3 + 5)], INK)
    cv.rect(bx2 + 5, by3 - 4, 6, 4, INK)


def mini_gulf(cv, x, y, w, h):
    """Night sea, tanker, second ship, drones on a clear flight path,
    waves, stars, moon, a distant platform on the horizon. The drone
    dots descend in a diagonal line toward the burst — a flight path,
    not scattered confetti."""
    cv.rect(x, y, w, h, (26, 44, 78))
    # stars, clear of the drone path and the moon
    for sx, sy in ((0.12, 0.30), (0.24, 0.10), (0.72, 0.08), (0.82, 0.22),
                   (0.92, 0.12), (0.06, 0.55)):
        cv.circle(x + int(w * sx), y + int(h * sy), 2, (230, 230, 210))
    # moon, top-left, with a faint halo
    cv.circle(x + 22, y + 12, 8, (200, 200, 180))
    cv.circle(x + 22, y + 12, 5, (240, 240, 220))
    cv.rect(x, y + h - 16, w, 16, (50, 102, 148))
    cv.line(x + 8, y + h - 10, x + w - 8, y + h - 10, (150, 195, 230), 2)
    cv.line(x + 20, y + h - 5, x + w - 20, y + h - 5, (150, 195, 230), 2)
    cv.line(x + int(w * 0.55), y + h - 13, x + int(w * 0.85), y + h - 13,
            (150, 195, 230), 2)
    cv.rect(x + 14, y + h - 26, w - 60, 10, INK)
    cv.rect(x + w - 62, y + max(2, h - 34), 18, 8, INK)
    # distant oil platform on the horizon, far right, clear of the ships
    cv.rect(x + w - 26, y + h - 36, 18, 6, (50, 60, 80))
    cv.line(x + w - 22, y + h - 30, x + w - 22, y + h - 16, (50, 60, 80), 2)
    cv.line(x + w - 12, y + h - 30, x + w - 12, y + h - 16, (50, 60, 80), 2)
    cv.circle(x + w - 17, y + h - 38, 2, (255, 150, 60))
    # second, smaller ship at the left
    cv.rect(x + 16, y + h - 22, 30, 7, INK)
    cv.rect(x + 26, y + h - 28, 8, 6, INK)
    # drones on a flight path: a faint trail line, then four dots
    # descending toward the burst at lower right, growing as they near
    path = [(0.28, 0.14, 2), (0.42, 0.28, 3), (0.56, 0.42, 3),
            (0.70, 0.56, 4)]
    px0 = x + int(w * path[0][0])
    py0 = y + int(h * path[0][1])
    px1 = x + int(w * path[-1][0])
    py1 = y + int(h * path[-1][1])
    cv.line(px0, py0, px1, py1, (140, 140, 150), 1)
    for dx, dy, dr in path:
        cv.circle(x + int(w * dx), y + int(h * dy), dr, (255, 90, 60))
    _star(cv, x + w - 36, y + h - 20, 9, (255, 120, 40))


def mini_shenzhen(cv, x, y, w, h):
    """Sunset skyline that reads as a city, never a bar chart: sky in
    two bands, six buildings of VARIED widths with stepped tops, one
    antenna tower, lit windows, a dark street band, three small flags
    on poles at the top-left, sun with a glow at the top-right."""
    cv.rect(x, y, w, h, (240, 190, 110))
    cv.rect(x, y + int(h * 0.62), w, h - int(h * 0.62), (250, 222, 150))
    # sun with glow, top-right
    glow_r = max(8, h // 5)
    cv.circle(x + w - 30, y + 12, glow_r + 4, (255, 232, 150))
    _sun(cv, x + w - 30, y + 12, max(6, glow_r - 4), (255, 220, 120))
    # three small flags on poles, top-left
    for i, col in enumerate(((200, 30, 30), (30, 60, 140), (255, 255, 255))):
        fx = x + 12 + i * 28
        cv.line(fx, y + 5, fx, y + 18, INK, 2)
        cv.rect(fx + 2, y + 5, 16, 9, col)
    # street band along the bottom
    gh = max(6, h // 8)
    cv.rect(x, y + h - gh, w, gh, (70, 60, 75))
    # buildings: varied widths, heights, two stepped tops, one antenna
    sky_h = max(14, int(h * 0.40))
    zone_top = y + sky_h
    zone_bot = y + h - gh
    zone_h = zone_bot - zone_top
    fracs = [(0.11, 0.55, False), (0.15, 0.75, True), (0.10, 0.45, False),
             (0.17, 0.95, False), (0.13, 0.65, True), (0.12, 0.50, False)]
    bx = x + 4
    gap = max(3, w // 80)
    for bw_f, bh_f, stepped in fracs:
        bw = int(w * bw_f)
        bh = int(zone_h * bh_f)
        top = zone_bot - bh
        cv.rect(bx, top, bw, bh, (60, 50, 70))
        if stepped:
            sh = max(3, h // 16)
            sw = int(bw * 0.55)
            cv.rect(bx + (bw - sw) // 2, top - sh, sw, sh, (60, 50, 70))
        if bh_f >= 0.95:
            # antenna tower: mast + red beacon
            cv.line(bx + bw // 2, top, bx + bw // 2, top - max(6, h // 8),
                    INK, 2)
            cv.circle(bx + bw // 2, top - max(6, h // 8), 2, RED)
        if h >= 48 and bh_f >= 0.65:
            # lit windows, sparse checkerboard, on the taller buildings
            for row in range((bh - 8) // 8):
                wy = top + 6 + row * 8
                for col_i in range((bw - 6) // 7):
                    if (row + col_i) % 2 == 0:
                        cv.rect(bx + 4 + col_i * 7, wy, 2, 3,
                                (255, 220, 120))
        bx += bw + gap


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
    """A refinery, not a bar chart: one wide process stack, one thin
    flare chimney with a small flame at its tip, a round storage
    tank, a ground line and a connecting pipe. The flame sits on the
    chimney tip — it never overlaps any bar."""
    cv.rect(x, y, w, h, (235, 228, 215))
    ground = y + h - 6
    # wide process stack, left
    s1 = max(9, int(h * 0.38))
    cv.rect(x + 14, ground - s1, 18, s1, NAVY)
    # thin flare chimney with a flame at its tip
    cv.rect(x + 42, y + 8, 7, ground - (y + 8), NAVY)
    _star(cv, x + 45, y + 6, 5, (255, 120, 40))
    _star(cv, x + 45, y + 6, 2, RED)
    # pipe between the units, and the ground line
    cv.line(x + 14, ground - 4, x + 60, ground - 4, NAVY, 2)
    cv.rect(x + 12, ground, 52, 4, NAVY)
    # round storage tank at the right
    cv.circle(x + w - 34, ground - 8, 9, NAVY)
    cv.circle(x + w - 34, ground - 8, 4, (235, 228, 215))


def mini_chip(cv, x, y, w, h):
    """Chip square + rising arrow."""
    cv.rect(x, y, w, h, (225, 235, 225))
    cx, cy = x + w // 3, y + h // 2
    cv.rect(cx - 12, cy - 12, 24, 24, NAVY)
    cv.rect(cx - 6, cy - 6, 12, 12, GOLD)
    for dx in (-18, -6, 6, 18):
        cv.line(cx + dx, cy - 16, cx + dx, cy - 12, INK, 2)
        cv.line(cx + dx, cy + 12, cx + dx, cy + 16, INK, 2)
    for dy in (-12, 0, 12):
        cv.line(cx - 16, cy + dy, cx - 12, cy + dy, INK, 2)
        cv.line(cx + 12, cy + dy, cx + 16, cy + dy, INK, 2)
    cv.line(x + w - 46, y + h - 10, x + w - 14, y + 10, (46, 125, 60), 3)
    cv.line(x + w - 14, y + 10, x + w - 26, y + 10, (46, 125, 60), 3)
    cv.line(x + w - 14, y + 10, x + w - 14, y + 22, (46, 125, 60), 3)


def mini_quake(cv, x, y, w, h):
    """Seismograph trace, BIG: tall spikes filling the box height,
    thick line — the quake symbol, no empty space around it."""
    cv.rect(x, y, w, h, (235, 228, 215))
    mid = y + h // 2
    amp = max(6, h // 2 - 3)
    cv.line(x + 6, mid + 8, x + w - 6, mid + 8, (120, 110, 95), 3)
    pts = [(x + 8, mid), (x + int(w * 0.24), mid),
           (x + int(w * 0.32), mid - amp), (x + int(w * 0.40), mid + amp),
           (x + int(w * 0.48), mid - amp), (x + int(w * 0.56), mid + amp),
           (x + int(w * 0.64), mid - amp // 2), (x + int(w * 0.76), mid),
           (x + w - 8, mid)]
    for i in range(len(pts) - 1):
        cv.line(pts[i][0], pts[i][1], pts[i + 1][0], pts[i + 1][1], RED, 4)


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
    """Night sky, one big missile climbing with a smoke trail + burst."""
    cv.rect(x, y, w, h, NIGHT)
    sx, sy = x + 18, y + h - 6
    ex, ey = x + w - 44, y + 8
    # smoke trail behind the missile, offset below its path
    cv.line(sx + 6, sy + 2, ex - 8, ey + 12, (200, 200, 200), 2)
    # missile body + cone head
    cv.line(sx, sy, ex, ey, (255, 120, 60), 5)
    cv.poly([(ex, ey), (ex - 16, ey + 2), (ex - 6, ey + 12)], (255, 200, 90))
    _star(cv, ex + 6, ey - 2, 8, (255, 200, 90))
    _star(cv, ex + 6, ey - 2, 4, (255, 120, 60))
    # second, smaller trail lower right
    cv.line(x + int(w * 0.55), y + h - 4, x + w - 12, y + h - 18,
            (255, 120, 60), 3)
    cv.circle(x + w - 12, y + h - 18, 4, (255, 200, 90))


def mini_chart_down(cv, x, y, w, h):
    """Three falling bars + a true diagonal down-trend arrow that
    runs ABOVE the bars and never crosses one, with a down-right
    arrowhead at its tip."""
    cv.rect(x, y, w, h, (235, 228, 215))
    for i, bh in enumerate((14, 10, 6)):
        cv.rect(x + 16 + i * 20, y + h - 8 - bh, 14, bh, RED)
    # trend line: shallow diagonal from top-left to lower-right,
    # staying above every bar top
    tx0, ty0 = x + 12, y + 5
    tx1, ty1 = x + w - 14, y + h - 14
    cv.line(tx0, ty0, tx1, ty1, RED, 4)
    # arrowhead at the tip: back along the line and straight up
    cv.line(tx1, ty1, tx1 - 14, ty1, RED, 4)
    cv.line(tx1, ty1, tx1, ty1 - 14, RED, 4)


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
    """Globe + a leaf (diamond with a vein and a stem) — clearly a
    leaf, never a play button."""
    cv.rect(x, y, w, h, (225, 235, 225))
    cx, cy = x + w // 2 - 6, y + h // 2
    r = min(18, h // 2 - 3)
    cv.circle(cx, cy, r, (40, 90, 130))
    cv.line(cx, cy - r, cx, cy + r, (255, 255, 255), 2)
    cv.line(cx - r, cy, cx + r, cy, (255, 255, 255), 2)
    # leaf: pointed diamond with a vein, on a short stem
    lx, ly = x + w - 22, y + h - 18
    cv.line(lx, ly + 8, lx, ly + 2, (46, 125, 60), 2)
    cv.poly([(lx, ly + 2), (lx - 11, ly - 4), (lx, ly - 12),
             (lx + 11, ly - 4)], (46, 125, 60))
    cv.line(lx, ly - 10, lx, ly + 1, (225, 235, 225), 1)


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
