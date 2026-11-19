"""Map and pictogram drawings for the news-image entry. All hand-authored.
Stdlib only. Written fresh for news-image-20261118.
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
            cv.circle(x + 3 + c * 6, y + 3 + r * 5, 1, (255, 255, 255))


def _flag_cn(cv, x, y, w, h):
    cv.rect(x, y, w, h, (200, 30, 30))
    _star(cv, x + 7, y + 7, 4, (255, 220, 60), 5)
    for dx, dy in ((16, 3), (19, 7), (19, 11), (16, 14)):
        _star(cv, x + dx, y + dy, 2, (255, 220, 60), 5)


def _flag_ru(cv, x, y, w, h):
    cv.rect(x, y, w, h // 3 + 1, (255, 255, 255))
    cv.rect(x, y + h // 3, w, h // 3 + 1, (30, 80, 180))
    cv.rect(x, y + 2 * h // 3, w, h // 3 + 1, (200, 30, 30))


def map_kerch(cv, x, y, w, h):
    cv.rect(x, y, w, h, SEA)
    # Crimea (west): diamond peninsula, Kerch tip pointing east to the strait
    cv.poly([(x + 8, y + 22), (x + 55, y + 8), (x + 105, y + 12),
             (x + 135, y + 24), (x + 162, y + 42), (x + 156, y + 54),
             (x + 138, y + 50), (x + 120, y + 58), (x + 104, y + 70),
             (x + 88, y + 86), (x + 68, y + 100), (x + 44, y + 108),
             (x + 20, y + 102), (x + 4, y + 88), (x, y + 60),
             (x, y + 32)], LAND2)
    # Taman / Russia (east): peninsula pointing west to the strait
    cv.poly([(x + 186, y), (x + w, y), (x + w, y + h), (x + 205, y + h),
             (x + 192, y + 82), (x + 184, y + 56), (x + 190, y + 30),
             (x + 182, y + 12)], LAND)
    # bridge: horizontal across the strait, destroyed gap in the middle
    by = y + 50
    cv.line(x + 150, by, x + 164, by, INK, 4)
    cv.line(x + 182, by, x + 196, by, INK, 4)
    _star(cv, x + 173, by, 12, (255, 90, 20))
    _star(cv, x + 173, by, 6, RED)
    cv.circle(x + 163, y + 42, 6, (120, 120, 120))
    cv.circle(x + 183, y + 58, 5, (120, 120, 120))
    # boats in the Black Sea
    for bx2, by2 in ((x + 108, y + 94), (x + 150, y + 100)):
        cv.poly([(bx2, by2), (bx2 + 30, by2), (bx2 + 25, by2 + 7),
                 (bx2 + 5, by2 + 7)], INK)
    draw_text(cv, x + 232, y + 8, "RUSSIA", 1, INK, bold=True)
    draw_text(cv, x + 10, y + 86, "CRIMEA", 1, INK, bold=True)
    draw_text(cv, x + 92, y + 4, "KERCH STRAIT", 1, (20, 60, 110), bold=True)
    draw_text(cv, x + 104, y + 80, "BLACK SEA", 1, (20, 60, 110), bold=True)


def map_gulf(cv, x, y, w, h):
    cv.rect(x, y, w, h, SEA)
    # Iran (top): coast dips south toward the Strait of Hormuz
    cv.poly([(x, y), (x + w, y), (x + w, y + 42), (x + 285, y + 38),
             (x + 270, y + 36), (x + 262, y + 44), (x + 258, y + 52),
             (x + 250, y + 44), (x + 235, y + 32), (x + 210, y + 26),
             (x + 170, y + 20), (x + 120, y + 18), (x + 60, y + 22),
             (x, y + 28)], LAND)
    # Arabia (bottom): Qatar peninsula juts north, Musandam spikes up
    # to pinch the Strait of Hormuz
    cv.poly([(x, y + h), (x + w, y + h), (x + w, y + 102),
             (x + 290, y + 96), (x + 274, y + 90), (x + 268, y + 84),
             (x + 262, y + 66), (x + 254, y + 86), (x + 235, y + 88),
             (x + 210, y + 86), (x + 180, y + 82), (x + 165, y + 78),
             (x + 160, y + 60), (x + 148, y + 58), (x + 142, y + 72),
             (x + 130, y + 76), (x + 100, y + 78), (x + 70, y + 80),
             (x + 40, y + 84), (x, y + 88)], LAND2)
    # Qeshm island, hugging the Iranian coast by Hormuz
    cv.poly([(x + 234, y + 56), (x + 258, y + 54), (x + 264, y + 60),
             (x + 240, y + 63)], LAND2)
    # Bahrain island, off the Saudi coast west of Qatar
    cv.poly([(x + 136, y + 66), (x + 146, y + 64), (x + 150, y + 70),
             (x + 140, y + 73)], LAND2)
    # Bahrain dot + Kuwait marker
    cv.circle(x + 143, y + 68, 5, RED)
    cv.circle(x + 143, y + 68, 2, (255, 255, 255))
    cv.rect(x + 10, y + 82, 7, 7, RED)
    # drones flying Iran -> Bahrain
    for dx, dy in ((0.60, 30), (0.66, 40), (0.58, 46)):
        px, py = x + int(w * dx), y + dy
        cv.poly([(px, py), (px - 9, py + 4), (px - 2, py + 2)], INK)
    _star(cv, x + 143, y + 68, 9, (255, 90, 20))
    _star(cv, x + 250, y + 58, 9, (255, 90, 20))
    draw_text(cv, x + int(w * 0.78), y + 10, "IRAN", 1, INK, bold=True)
    draw_text(cv, x + 8, y + 96, "ARABIA", 1, INK, bold=True)
    draw_text(cv, x + int(w * 0.46), y + 80, "BAHRAIN", 1, RED, bold=True)
    draw_text(cv, x + int(w * 0.74), y + 78, "QESHM", 1, (20, 60, 110), bold=True)
    draw_text(cv, x + int(w * 0.18), y + 84, "KUWAIT", 1, RED, bold=True)


def map_china(cv, x, y, w, h):
    cv.rect(x, y, w, h, SEA)
    # real China outline: Manchuria in the north-east, Shandong
    # peninsula, Fujian coast, Guangdong south coast
    cv.poly([(x + 28, y + 22), (x + 60, y + 10), (x + 110, y + 4),
             (x + 160, y + 4), (x + 205, y + 8), (x + 238, y + 4),
             (x + 252, y + 14), (x + 244, y + 28), (x + 228, y + 36),
             (x + 238, y + 42), (x + 222, y + 46), (x + 210, y + 52),
             (x + 212, y + 64), (x + 204, y + 74), (x + 196, y + 84),
             (x + 182, y + 90), (x + 168, y + 94), (x + 150, y + 100),
             (x + 130, y + 102), (x + 110, y + 100), (x + 90, y + 94),
             (x + 68, y + 88), (x + 48, y + 80), (x + 32, y + 68),
             (x + 20, y + 54), (x + 14, y + 38), (x + 18, y + 28)], LAND)
    # Hainan island, just off the south coast
    cv.poly([(x + 148, y + 104), (x + 160, y + 102), (x + 163, y + 108),
             (x + 152, y + 109)], LAND)
    # Taiwan, east of Fujian
    cv.poly([(x + 222, y + 78), (x + 228, y + 76), (x + 230, y + 84),
             (x + 224, y + 86)], LAND)
    # Shenzhen dot on the south coast
    sx, sy = x + 176, y + 88
    cv.circle(sx, sy, 7, RED)
    cv.circle(sx, sy, 3, (255, 255, 255))
    draw_text(cv, sx - 40, sy - 20, "SHENZHEN", 1, RED, bold=True)
    draw_text(cv, x + 90, y + 40, "CHINA", 1, INK, bold=True)
    # three flags top-right
    _flag_us(cv, x + w - 150, y + 6, 44, 26)
    _flag_cn(cv, x + w - 100, y + 6, 44, 26)
    _flag_ru(cv, x + w - 50, y + 6, 44, 26)
    draw_text(cv, x + 8, y + h - 14, "TRUMP - XI - PUTIN", 1, INK, bold=True)
    draw_text(cv, x + w - 150, y + 36, "THU 19 NOV", 1, BLUE, bold=True)


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
            cv.line(px, py, tx + nw // 2, ty + 5, INK, 1)
            cv.circle(px, py, 5, RED)
            cv.rect(tx - 2, ty - 2, nw + 4, 14, (255, 255, 255))
            draw_text(cv, tx, ty, num_s, 1, RED, bold=True)


# ---------------------------------------------------------------- pictograms
def icon(cv, kind, x, y, s, color):
    """Small pictogram in a s x s box at (x, y)."""
    c = color
    if kind == "blast":
        _star(cv, x + s // 2, y + s // 2, s // 2 - 1, c)
    elif kind == "chart":
        for i, hh in enumerate((0.35, 0.6, 1.0)):
            bh = int(s * hh)
            cv.rect(x + i * (s // 3) + 1, y + s - bh, s // 4, bh, c)
    elif kind == "coin":
        cv.circle(x + s // 2, y + s // 2, s // 2 - 1, c)
        cv.circle(x + s // 2, y + s // 2, s // 2 - 4, (247, 242, 231))
        draw_text(cv, x + s // 2 - 4, y + s // 2 - 7, "$", 1, c, bold=True)
    elif kind == "trophy":
        cv.rect(x + 4, y + 2, s - 8, s // 2, c)
        cv.rect(x + s // 2 - 2, y + s // 2 + 2, 4, s // 3, c)
        cv.rect(x + 2, y + s - 4, s - 4, 3, c)
        cv.rect(x, y + 4, 4, 8, c)
        cv.rect(x + s - 4, y + 4, 4, 8, c)
    elif kind == "ball":
        cv.circle(x + s // 2, y + s // 2, s // 2 - 1, c)
        cv.circle(x + s // 2, y + s // 2, 3, (247, 242, 231))
        for a in (30, 150, 270):
            px = x + s // 2 + int(8 * math.cos(math.radians(a)))
            py = y + s // 2 + int(8 * math.sin(math.radians(a)))
            cv.circle(px, py, 2, (247, 242, 231))
    elif kind == "flask":
        cv.poly([(x + s // 2 - 3, y + 2), (x + s // 2 + 3, y + 2),
                 (x + s // 2 + 3, y + s // 2), (x + s - 2, y + s - 2),
                 (x + 2, y + s - 2), (x + s // 2 - 3, y + s // 2)], c)
    elif kind == "globe":
        cv.circle(x + s // 2, y + s // 2, s // 2 - 1, c)
        cv.line(x + s // 2, y + 1, x + s // 2, y + s - 1, (247, 242, 231), 1)
        cv.line(x + 1, y + s // 2, x + s - 1, y + s // 2, (247, 242, 231), 1)
    elif kind == "flag":
        cv.vline(x + 3, y + 2, y + s - 2, c, 2)
        cv.poly([(x + 5, y + 2), (x + s - 2, y + 6), (x + 5, y + 10)], c)
    elif kind == "quake":
        for yy in (6, 14, 22):
            cv.line(x + 2, y + yy, x + s // 3, y + yy - 4, c, 2)
            cv.line(x + s // 3, y + yy - 4, x + 2 * s // 3, y + yy + 3, c, 2)
            cv.line(x + 2 * s // 3, y + yy + 3, x + s - 2, y + yy - 2, c, 2)
    elif kind == "sun":
        cv.circle(x + s // 2, y + s // 2, s // 4, c)
        for a in range(0, 360, 45):
            x2 = x + s // 2 + int((s // 2 - 1) * math.cos(math.radians(a)))
            y2 = y + s // 2 + int((s // 2 - 1) * math.sin(math.radians(a)))
            x1 = x + s // 2 + int((s // 4 + 1) * math.cos(math.radians(a)))
            y1 = y + s // 2 + int((s // 4 + 1) * math.sin(math.radians(a)))
            cv.line(x1, y1, x2, y2, c, 2)
    elif kind == "leaf":
        cv.circle(x + s // 2, y + s // 2 - 2, s // 3, c)
        cv.line(x + s // 2, y + s // 2 + 4, x + s // 2, y + s - 2, c, 2)
    elif kind == "ship":
        cv.poly([(x + 2, y + s // 2 + 4), (x + s - 2, y + s // 2 + 4),
                 (x + s - 6, y + s - 2), (x + 6, y + s - 2)], c)
        cv.vline(x + s // 2, y + 2, y + s // 2 + 4, c, 2)
        cv.poly([(x + s // 2 + 2, y + 4), (x + s - 4, y + s // 2),
                 (x + s // 2 + 2, y + s // 2)], c)
    elif kind == "plane":
        cv.poly([(x + 2, y + s // 2), (x + s - 2, y + 2), (x + s - 6, y + s // 2),
                 (x + s - 2, y + s - 2)], c)
    elif kind == "bolt":
        cv.poly([(x + s // 2 + 3, y + 1), (x + s // 2 - 5, y + s // 2 + 2),
                 (x + s // 2 - 1, y + s // 2 + 2), (x + s // 2 - 4, y + s - 1),
                 (x + s // 2 + 5, y + s // 2 - 1), (x + s // 2 + 1, y + s // 2 - 1)], c)
    elif kind == "vote":
        cv.rect(x + 2, y + s // 2, s - 4, s // 2 - 2, c)
        cv.line(x + 4, y + 4, x + s // 2, y + s // 2 - 2, c, 2)
        cv.line(x + s // 2, y + s // 2 - 2, x + s - 3, y + 2, c, 2)
    elif kind == "bank":
        cv.poly([(x + 1, y + 8), (x + s // 2, y + 1), (x + s - 1, y + 8)], c)
        for i in range(3):
            cv.vline(x + 5 + i * (s // 3), y + 10, y + s - 4, c, 2)
        cv.rect(x + 2, y + s - 3, s - 4, 3, c)
    elif kind == "mask":
        cv.circle(x + s // 3, y + s // 2, s // 5, c)
        cv.circle(x + 2 * s // 3, y + s // 2, s // 5, c)
    elif kind == "alert":
        cv.poly([(x + s // 2, y + 1), (x + s - 2, y + s - 3), (x + 2, y + s - 3)], c)
        draw_text(cv, x + s // 2 - 4, y + s // 2 - 2, "!", 1, (247, 242, 231), bold=True)
    elif kind == "rocket":
        cv.poly([(x + s // 2, y + 1), (x + s // 2 + 6, y + s // 2),
                 (x + s // 2, y + s - 6), (x + s // 2 - 6, y + s // 2)], c)
        cv.circle(x + s // 2, y + s // 3, 3, (247, 242, 231))
    else:  # dot
        cv.circle(x + s // 2, y + s // 2, s // 3, c)
