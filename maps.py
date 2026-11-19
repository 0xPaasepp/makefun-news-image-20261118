"""Map drawings for the news-image entry: real-coastline regional maps
(Kerch, Gulf, China) and the world map. All hand-authored, stdlib only.
Regional maps are drawn in their native 312x110 geometry and stretched
vertically (KY) to fill the taller 312x140 card map box.
"""
import math
from draw import draw_text

SEA = (168, 205, 228)
LAND = (224, 198, 152)
LAND2 = (210, 182, 132)
INK = (20, 20, 20)
RED = (178, 34, 34)
BLUE = (30, 80, 160)
GREEN = (46, 125, 60)
GOLD = (214, 158, 32)

# vertical stretch: native map height 110 -> card map height 140
KY = 140.0 / 110.0


def _S(pts):
    """Scale a native (x, y) point list vertically for the taller box."""
    return [(px, py * KY) for px, py in pts]


def _star(cv, cx, cy, r, color, points=8):
    for k in range(points):
        a = math.radians(k * 360 / points)
        x2 = int(cx + r * math.cos(a))
        y2 = int(cy + r * math.sin(a))
        cv.line(cx, cy, x2, y2, color, 2)
    cv.circle(cx, cy, max(2, r // 3), color)


def _flag_us(cv, x, y, w, h):
    cv.rect(x, y, w, h, (255, 255, 255))
    for i in range(0, 7, 2):
        cv.rect(x, y + i * h // 7, w, h // 7 + 1, (178, 34, 34))
    cv.rect(x, y, w // 2, h // 2 + 1, (30, 60, 140))
    for r in range(2):
        for c in range(3):
            cv.circle(x + 4 + c * 7, y + 4 + r * 6, 2, (255, 255, 255))


def _flag_cn(cv, x, y, w, h):
    cv.rect(x, y, w, h, (200, 30, 30))
    _star(cv, x + 8, y + 8, 5, (255, 220, 60), 5)
    for dx, dy in ((19, 3), (22, 7), (22, 12), (19, 15)):
        _star(cv, x + dx, y + dy, 2, (255, 220, 60), 5)


def _flag_ru(cv, x, y, w, h):
    cv.rect(x, y, w, h // 3 + 1, (255, 255, 255))
    cv.rect(x, y + h // 3, w, h // 3 + 1, (30, 80, 180))
    cv.rect(x, y + 2 * h // 3, w, h // 3 + 1, (200, 30, 30))


def map_kerch(cv, x, y, w, h):
    cv.rect(x, y, w, h, SEA)
    # Crimea (west): diamond peninsula, Kerch tip pointing east to the strait
    cv.poly([(x + px, y + py) for px, py in _S([(8, 22), (55, 8), (105, 12),
             (135, 24), (162, 42), (156, 54), (138, 50), (120, 58), (104, 70),
             (88, 86), (68, 100), (44, 108), (20, 102), (4, 88), (0, 60),
             (0, 32)])], LAND2)
    # Taman / Russia (east): peninsula pointing west to the strait
    cv.poly([(x + px, y + py) for px, py in _S([(186, 0), (312, 0), (312, 110),
             (205, 110), (192, 82), (184, 56), (190, 30), (182, 12)])], LAND)
    # bridge: horizontal across the strait, destroyed gap in the middle
    by = y + 50 * KY
    cv.line(x + 150, by, x + 164, by, INK, 4)
    cv.line(x + 182, by, x + 196, by, INK, 4)
    _star(cv, x + 173, by, 12, (255, 90, 20))
    _star(cv, x + 173, by, 6, RED)
    # boats in the Black Sea: hull + cabin, bold, clear of the label above
    for bx2, by2 in ((x + 108, y + 100 * KY), (x + 178, y + 102 * KY)):
        cv.poly([(bx2, by2), (bx2 + 32, by2), (bx2 + 26, by2 + 8),
                 (bx2 + 6, by2 + 8)], INK)
        cv.rect(bx2 + 10, by2 - 6, 10, 6, INK)
    draw_text(cv, x + 232, y + 10, "RUSSIA", 1, INK, bold=True)
    draw_text(cv, x + 10, y + 110, "CRIMEA", 1, INK, bold=True)
    draw_text(cv, x + 92, y + 5, "KERCH STRAIT", 1, (20, 60, 110), bold=True)
    draw_text(cv, x + 104, y + 102, "BLACK SEA", 1, (20, 60, 110), bold=True)


def map_gulf(cv, x, y, w, h):
    cv.rect(x, y, w, h, SEA)
    # Iran (top): coast dips south toward the Strait of Hormuz
    cv.poly([(x + px, y + py) for px, py in _S([(0, 0), (312, 0), (312, 42),
             (285, 38), (270, 36), (262, 44), (258, 52), (250, 44), (235, 32),
             (210, 26), (170, 20), (120, 18), (60, 22), (0, 28)])], LAND)
    # Arabia (bottom): Qatar peninsula juts north, Musandam spikes up
    # to pinch the Strait of Hormuz
    cv.poly([(x + px, y + py) for px, py in _S([(0, 110), (312, 110), (312, 102),
             (290, 96), (274, 90), (268, 84), (262, 66), (254, 86), (235, 88),
             (210, 86), (180, 82), (165, 78), (160, 60), (148, 58), (142, 72),
             (130, 76), (100, 78), (70, 80), (40, 84), (0, 88)])], LAND2)
    # Qeshm island, hugging the Iranian coast by Hormuz
    cv.poly([(x + px, y + py) for px, py in _S([(234, 56), (258, 54), (264, 60),
             (240, 63)])], LAND2)
    # Bahrain island, off the Saudi coast west of Qatar
    cv.poly([(x + px, y + py) for px, py in _S([(136, 66), (146, 64), (150, 70),
             (140, 73)])], LAND2)
    # Bahrain dot + Kuwait marker
    cv.circle(x + 143, y + 68 * KY, 5, RED)
    cv.circle(x + 143, y + 68 * KY, 2, (255, 255, 255))
    cv.rect(x + 10, y + 82 * KY, 7, 7, RED)
    # drones flying Iran -> Bahrain: bold triangles
    for dx, dy in ((0.60, 30), (0.66, 40), (0.58, 46)):
        px, py = x + int(w * dx), y + dy * KY
        cv.poly([(px, py), (px - 11, py + 5), (px - 2, py + 2)], INK)
    _star(cv, x + 143, y + 68 * KY, 9, (255, 90, 20))
    _star(cv, x + 250, y + 58 * KY, 9, (255, 90, 20))
    draw_text(cv, x + int(w * 0.78), y + 13, "IRAN", 1, INK, bold=True)
    draw_text(cv, x + 8, y + 122, "ARABIA", 1, INK, bold=True)
    draw_text(cv, x + int(w * 0.46), y + 102, "BAHRAIN", 1, RED, bold=True)
    draw_text(cv, x + int(w * 0.74), y + 99, "QESHM", 1, (20, 60, 110), bold=True)
    draw_text(cv, x + int(w * 0.18), y + 107, "KUWAIT", 1, RED, bold=True)


def map_china(cv, x, y, w, h):
    cv.rect(x, y, w, h, SEA)
    # real China outline: Manchuria in the north-east, Shandong
    # peninsula, Fujian coast, Guangdong south coast
    cv.poly([(x + px, y + py) for px, py in _S([(28, 22), (60, 10), (110, 4),
             (160, 4), (205, 8), (238, 4), (252, 14), (244, 28), (228, 36),
             (238, 42), (222, 46), (210, 52), (212, 64), (204, 74), (196, 84),
             (182, 90), (168, 94), (150, 100), (130, 102), (110, 100),
             (90, 94), (68, 88), (48, 80), (32, 68), (20, 54), (14, 38),
             (18, 28)])], LAND)
    # Hainan island, just off the south coast
    cv.poly([(x + px, y + py) for px, py in _S([(148, 104), (160, 102),
             (163, 108), (152, 109)])], LAND)
    # Taiwan, east of Fujian
    cv.poly([(x + px, y + py) for px, py in _S([(222, 78), (228, 76), (230, 84),
             (224, 86)])], LAND)
    # Shenzhen dot on the south coast
    sx, sy = x + 176, y + 88 * KY
    cv.circle(sx, sy, 7, RED)
    cv.circle(sx, sy, 3, (255, 255, 255))
    draw_text(cv, sx - 40, sy - 26, "SHENZHEN", 1, RED, bold=True)
    draw_text(cv, x + 90, y + 51, "CHINA", 1, INK, bold=True)
    # three flags top-right
    _flag_us(cv, x + w - 162, y + 8, 48, 30)
    _flag_cn(cv, x + w - 108, y + 8, 48, 30)
    _flag_ru(cv, x + w - 54, y + 8, 48, 30)
    draw_text(cv, x + 8, y + h - 14, "TRUMP - XI - PUTIN", 1, INK, bold=True)
    draw_text(cv, x + w - 150, y + 46, "THU 19 NOV", 1, BLUE, bold=True)


# ---------------------------------------------------------------- world map
# continent outlines as (lon, lat) pairs; projected into the given box
_NA = [(-168, 66), (-165, 60), (-158, 58), (-155, 55), (-150, 59),
       (-145, 60), (-138, 59), (-132, 56), (-128, 51), (-125, 49),
       (-124, 43), (-121, 37), (-117, 33), (-112, 29), (-110, 24),
       (-105, 20), (-100, 17), (-95, 16), (-90, 14), (-87, 13),
       (-83, 9), (-80, 9), (-77, 8), (-76, 10), (-73, 11), (-69, 12),
       (-66, 11), (-63, 10), (-61, 10), (-64, 17), (-68, 18), (-71, 19),
       (-74, 20), (-77, 21), (-80, 23), (-81, 25), (-80, 27), (-81, 30),
       (-79, 32), (-76, 35), (-74, 38), (-71, 41), (-69, 44), (-66, 45),
       (-64, 44), (-60, 46), (-59, 47), (-55, 47), (-53, 48), (-55, 50),
       (-58, 52), (-60, 55), (-65, 58), (-70, 60), (-75, 62), (-78, 60),
       (-80, 56), (-82, 52), (-84, 55), (-87, 57), (-90, 58), (-93, 59),
       (-94, 62), (-92, 64), (-88, 64), (-85, 66), (-82, 66), (-80, 67),
       (-82, 68), (-88, 68), (-92, 68), (-95, 69), (-100, 68),
       (-110, 68), (-120, 69), (-130, 70), (-140, 70), (-150, 71),
       (-160, 70), (-165, 68)]
_GL = [(-58, 64), (-45, 60), (-30, 68), (-22, 70), (-30, 76), (-45, 76),
       (-58, 74), (-60, 70)]
_SA = [(-79, 9), (-77, 4), (-80, -2), (-81, -5), (-78, -9), (-76, -13),
       (-72, -18), (-70, -22), (-70, -30), (-71, -33), (-72, -37),
       (-73, -42), (-73, -48), (-71, -52), (-68, -54), (-66, -55),
       (-65, -50), (-65, -45), (-62, -41), (-58, -36), (-54, -34),
       (-50, -30), (-48, -26), (-43, -23), (-40, -21), (-38, -16),
       (-35, -9), (-35, -6), (-38, -4), (-42, -3), (-46, -1), (-50, 0),
       (-52, 4), (-55, 6), (-58, 8), (-61, 9), (-65, 10), (-69, 11),
       (-72, 12), (-75, 11), (-77, 9)]
_AF = [(-17, 15), (-17, 20), (-15, 25), (-10, 30), (-6, 33), (-2, 35),
       (3, 37), (10, 37), (12, 34), (19, 32), (23, 33), (30, 31),
       (32, 31), (34, 28), (36, 24), (38, 20), (40, 15), (43, 12),
       (46, 11), (51, 12), (51, 10), (48, 5), (46, 2), (43, -1),
       (41, -3), (40, -8), (39, -13), (36, -18), (35, -22), (33, -26),
       (30, -30), (28, -33), (25, -34), (19, -35), (17, -32), (15, -27),
       (13, -22), (12, -18), (13, -13), (12, -8), (9, -1), (9, 4),
       (6, 4), (2, 6), (-2, 5), (-7, 4), (-12, 7), (-15, 11), (-17, 14)]
_EU = [(-9, 37), (-6, 36), (-2, 37), (0, 38), (3, 39), (6, 39),
       (8, 42), (10, 44), (12, 44), (15, 45), (18, 44), (19, 42),
       (21, 41), (23, 40), (25, 39), (27, 38), (29, 37), (30, 36),
       (30, 40), (29, 43), (27, 44), (25, 45), (24, 47), (23, 49),
       (22, 51), (21, 54), (19, 55), (18, 57), (19, 58), (21, 59),
       (23, 60), (25, 60), (27, 61), (29, 63), (30, 65), (28, 68),
       (25, 70), (21, 70), (17, 69), (13, 68), (10, 65), (7, 62),
       (5, 60), (5, 58), (8, 57), (9, 55), (7, 54), (4, 53), (2, 51),
       (0, 50), (-2, 48), (-2, 46), (-1, 44), (-4, 44), (-8, 43),
       (-9, 41), (-9, 38)]
_IT = [(10, 44), (13, 44), (15, 42), (16, 40), (18, 40), (16, 38),
       (14, 39), (12, 41), (10, 43)]
_GR = [(22, 40), (23, 38), (24, 37), (26, 38), (24, 39), (22, 39)]
_AS = [(30, 62), (32, 66), (40, 68), (50, 69), (60, 70), (70, 72),
       (80, 73), (90, 75), (100, 77), (110, 76), (120, 73), (130, 72),
       (140, 72), (150, 70), (160, 70), (170, 66), (178, 65), (170, 60),
       (162, 58), (158, 52), (156, 51), (150, 55), (142, 55), (140, 50),
       (137, 46), (135, 43), (131, 42), (128, 40), (126, 39), (122, 38),
       (120, 34), (122, 30), (120, 27), (118, 25), (114, 22), (110, 20),
       (108, 17), (109, 12), (106, 10), (104, 8), (101, 7), (100, 9),
       (98, 11), (96, 15), (94, 17), (92, 21), (90, 22), (88, 22),
       (86, 20), (83, 18), (80, 15), (78, 10), (76, 8), (75, 11),
       (73, 16), (72, 20), (70, 22), (68, 23), (66, 25), (62, 25),
       (58, 25), (56, 26), (54, 27), (52, 28), (50, 29), (48, 30),
       (48, 29), (50, 26), (51, 25), (54, 24), (56, 24), (58, 23),
       (59, 22), (58, 20), (55, 17), (52, 15), (48, 14), (45, 13),
       (43, 12), (42, 15), (40, 18), (39, 21), (38, 24), (36, 28),
       (35, 29), (34, 31), (36, 36), (34, 36), (32, 36), (30, 36),
       (30, 42), (30, 48), (30, 55)]
_AU = [(113, -22), (114, -28), (115, -32), (118, -35), (124, -33),
       (129, -32), (132, -32), (135, -35), (138, -35), (140, -38),
       (145, -38), (150, -37), (153, -32), (153, -27), (150, -22),
       (146, -19), (142, -11), (141, -13), (136, -12), (132, -11),
       (128, -14), (124, -14), (120, -14), (116, -16), (113, -20)]
_TAS = [(145, -41), (148, -41), (148, -43), (146, -44), (145, -42)]
_UK = [(-5, 50), (-3, 53), (-5, 56), (-3, 58), (-1, 57), (0, 53),
       (-2, 51), (-4, 50)]
_JP = [(130, 31), (132, 33), (135, 34), (137, 35), (139, 36), (140, 38),
       (141, 40), (141, 42), (143, 43), (145, 44), (143, 45), (141, 44),
       (140, 42), (139, 38), (137, 37), (135, 35), (133, 34), (131, 33)]
_PH = [(120, 18), (122, 18), (122, 14), (121, 13), (120, 14)]

_CONTINENTS = [_NA, _GL, _SA, _AF, _EU, _IT, _GR, _AS, _AU, _TAS, _UK,
               _JP, _PH]


# ---------------------------------------------------------------- dotted map
def _point_in_poly(px, py, poly):
    """Ray-casting point-in-polygon for a list of (x, y) points."""
    inside = False
    n = len(poly)
    j = n - 1
    for i in range(n):
        xi, yi = poly[i]
        xj, yj = poly[j]
        if (yi > py) != (yj > py):
            xint = xi + (py - yi) * (xj - xi) / (yj - yi)
            if px < xint:
                inside = not inside
        j = i
    return inside


def world_map_dotted(cv, x, y, w, h, pins, dots):
    """Dotted world map: grey dots form the continents on a pale
    blue-grey field. pins: (lon, lat, number) red numbered pins.
    dots: (lon, lat, colour) small region-coloured dots."""
    cv.rect(x, y, w, h, (232, 236, 240))
    # project continent outlines once, with bounding boxes
    projected = []
    for cont in _CONTINENTS:
        pts = []
        for lon, lat in cont:
            px = x + int((lon + 170) / 360.0 * w)
            py = y + int((75 - lat) / 130.0 * h)
            pts.append((px, py))
        xs = [p[0] for p in pts]
        ys = [p[1] for p in pts]
        projected.append((pts, min(xs), max(xs), min(ys), max(ys)))
    step = 7
    for gy in range(y + 4, y + h - 2, step):
        for gx in range(x + 4, x + w - 2, step):
            on_land = False
            for pts, bx0, bx1, by0, by1 in projected:
                if bx0 <= gx <= bx1 and by0 <= gy <= by1:
                    if _point_in_poly(gx, gy, pts):
                        on_land = True
                        break
            if on_land:
                cv.circle(gx, gy, 2, (140, 145, 150))
    for lon, lat, color in dots:
        px = x + int((lon + 170) / 360.0 * w)
        py = y + int((75 - lat) / 130.0 * h)
        cv.circle(px, py, 3, color)
    from draw import text_w as _tw
    from draw import text_w as _tw
    # --- pin placement: cluster rows -------------------------------------
    # Pins closer than 26px to another pin form a cluster. Big clusters
    # split into an upper half (row of boxes ABOVE the pins) and a lower
    # half (row BELOW), each row x-ordered to match its pins, so the
    # thin leader lines are short and can never cross. Small clusters
    # (<=3 pins) get a single row, above or below, whichever hits fewer
    # dots. Row y is chosen from two candidates by fewest collisions.
    proj = []
    for lon, lat, num in pins:
        px = x + int((lon + 170) / 360.0 * w)
        py = y + int((75 - lat) / 130.0 * h)
        proj.append((px, py, num))
    dot_pts = []
    for lon, lat, _color in dots:
        dot_pts.append((x + int((lon + 170) / 360.0 * w),
                        y + int((75 - lat) / 130.0 * h)))
    n = len(proj)
    parent = list(range(n))

    def _find(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a

    for i in range(n):
        for j in range(i + 1, n):
            if ((proj[i][0] - proj[j][0]) ** 2
                    + (proj[i][1] - proj[j][1]) ** 2) < 26 * 26:
                ri, rj = _find(i), _find(j)
                if ri != rj:
                    parent[ri] = rj
    clusters = {}
    for i in range(n):
        clusters.setdefault(_find(i), []).append(i)
    placed = []  # (x0, y0, x1, y1) boxes already on the map

    def _row_hits(bx0, by0, bx1, by1, own):
        if bx0 < x + 2 or by0 < y + 2 or bx1 > x + w - 2 or by1 > y + h - 2:
            return 999
        hits = 0
        for (ox0, oy0, ox1, oy1) in placed:
            if bx0 < ox1 + 2 and bx1 > ox0 - 2 and by0 < oy1 + 2 and by1 > oy0 - 2:
                hits += 1
        for (dx, dy) in dot_pts:
            if bx0 - 3 <= dx <= bx1 + 3 and by0 - 3 <= dy <= by1 + 3:
                hits += 1
        for k, (ox, oy, _num) in enumerate(proj):
            if k in own:
                continue
            if bx0 - 4 <= ox <= bx1 + 4 and by0 - 4 <= oy <= by1 + 4:
                hits += 1
        return hits

    def _place_row(half, above):
        """One row of number boxes for the given pin indices."""
        half = sorted(half, key=lambda i: proj[i][0])
        widths = [_tw(str(proj[i][2]), 1, bold=True) + 8 for i in half]
        total = sum(widths) + 4 * (len(half) - 1)
        cx = sum(proj[i][0] for i in half) / len(half)
        min_py = min(proj[i][1] for i in half)
        max_py = max(proj[i][1] for i in half)
        if above:
            cands = [max(y + 2, min_py - 20), max(y + 2, min_py - 36)]
        else:
            cands = [min(y + h - 16, max_py + 6), min(y + h - 16, max_py + 24)]
        own = set(half)
        best = None
        for ry in cands:
            sx = int(min(max(cx - total / 2, x + 2), x + w - 2 - total))
            hits = 0
            bx = sx
            for wd in widths:
                hits += _row_hits(bx, ry, bx + wd, ry + 14, own)
                bx += wd + 4
            if best is None or hits < best[0]:
                best = (hits, ry, sx)
        _hits, ry, sx = best
        bx = sx
        for i, wd in zip(half, widths):
            px, py, num = proj[i]
            num_s = str(num)
            if above:
                cv.line(px, py, bx + wd // 2, ry + 14, INK, 1)
            else:
                cv.line(px, py, bx + wd // 2, ry, INK, 1)
            cv.circle(px, py, 4, RED)
            cv.rect(bx, ry, wd, 14, (255, 255, 255))
            cv.hline(bx, bx + wd - 1, ry, RED, 1)
            cv.hline(bx, bx + wd - 1, ry + 13, RED, 1)
            draw_text(cv, bx + 4, ry + 1, num_s, 1, RED, bold=True)
            placed.append((bx, ry, bx + wd, ry + 14))
            bx += wd + 4

    for members in clusters.values():
        if len(members) == 1:
            px, py, num = proj[members[0]]
            r = 9 if len(str(num)) > 1 else 8
            cv.circle(px, py, r, RED)
            nw = _tw(str(num), 1, bold=True)
            draw_text(cv, px - nw // 2, py - 6, str(num), 1,
                      (255, 255, 255), bold=True)
            placed.append((px - r, py - r, px + r, py + r))
            continue
        if len(members) >= 4:
            # split by height: upper half gets a row above, lower half below
            by_py = sorted(members, key=lambda i: proj[i][1])
            half_n = len(by_py) // 2
            _place_row(by_py[:half_n], above=True)
            _place_row(by_py[half_n:], above=False)
        else:
            # single row: score above vs below, place the better one
            min_py = min(proj[i][1] for i in members)
            max_py = max(proj[i][1] for i in members)
            above_y = max(y + 2, min_py - 20)
            below_y = min(y + h - 16, max_py + 6)

            def _score(ry):
                half = sorted(members, key=lambda i: proj[i][0])
                widths = [_tw(str(proj[i][2]), 1, bold=True) + 8
                          for i in half]
                total = sum(widths) + 4 * (len(half) - 1)
                cx = sum(proj[i][0] for i in half) / len(half)
                sx = int(min(max(cx - total / 2, x + 2), x + w - 2 - total))
                hits = 0
                bx = sx
                for wd in widths:
                    hits += _row_hits(bx, ry, bx + wd, ry + 14, set(members))
                    bx += wd + 4
                return hits

            if _score(below_y) < _score(above_y):
                _place_row(members, above=False)
            else:
                _place_row(members, above=True)


def world_map(cv, x, y, w, h, dots):
    """dots: list of (lon, lat, number) or (lon, lat, number, label_dx, label_dy).
    With a label offset, the number is drawn in a white box with a leader line
    instead of inside the dot (for crowded areas)."""
    from draw import text_w as _tw
    cv.rect(x, y, w, h, SEA)
    for cont in _CONTINENTS:
        pts = []
        for lon, lat in cont:
            px = x + int((lon + 170) / 360.0 * w)
            py = y + int((75 - lat) / 130.0 * h)
            pts.append((px, py))
        cv.poly(pts, LAND)
    # muted continent labels: on land where they fit, else in empty ocean
    # beside the continent (never touching a dot or the key below)
    for text, lx, ly in (("N. AMERICA", 30, 24), ("S. AMERICA", 20, 155),
                         ("AFRICA", 220, 104), ("AUSTRALIA", 360, 176)):
        from draw import draw_text as _dt2
        _dt2(cv, x + lx, y + ly, text, 1, (120, 112, 98), bold=True)
    for entry in dots:
        lon, lat, num = entry[0], entry[1], entry[2]
        lx = entry[3] if len(entry) > 3 else None
        ly = entry[4] if len(entry) > 4 else None
        px = x + int((lon + 170) / 360.0 * w)
        py = y + int((75 - lat) / 130.0 * h)
        num_s = str(num)
        if lx is None:
            r = 9 if len(num_s) > 1 else 7
            cv.circle(px, py, r, RED)
            nw = _tw(num_s, 1, bold=True)
            draw_text(cv, px - nw // 2, py - 6, num_s, 1, (255, 255, 255), bold=True)
        else:
            tx, ty = px + lx, py + ly
            nw = _tw(num_s, 1, bold=True)
            cv.line(px, py, tx + nw // 2, ty + 5, INK, 2)
            cv.circle(px, py, 5, RED)
            cv.rect(tx - 2, ty - 2, nw + 4, 14, (255, 255, 255))
            cv.hline(tx - 2, tx + nw + 1, ty - 2, RED, 1)
            cv.hline(tx - 2, tx + nw + 1, ty + 11, RED, 1)
            draw_text(cv, tx, ty, num_s, 1, RED, bold=True)


