"""Drawing engine for the news-image entry: supersampled canvas, vector font, PNG output.
Stdlib only. Written fresh for news-image-20261118.

Rendering: everything is drawn into a 2x buffer (2048x2048) and downsampled
to 1024x1024 with a 2x2 box average, so every edge gets real anti-aliasing.
All public coordinates are logical 1024x1024 coordinates; the canvas scales
them internally. Deterministic: same input -> byte-identical PNG.

Font: a stroke (vector) font, not a bitmap font. Glyphs are polylines on a
20x28 grid (cap top y=3, baseline y=25), drawn as thick lines with round
joins/caps, so diagonals are true diagonals and curves are smooth arcs.
Lowercase renders as small caps (the entry uses them for body text).
"""
import math
import struct
import zlib

SS = 2  # supersample factor


# ---------------------------------------------------------------- canvas
class Canvas:
    def __init__(self, w, h, bg):
        self.w = w
        self.h = h
        self.bw = w * SS
        self.bh = h * SS
        r, g, b = bg
        self.buf = bytearray(bytes((r, g, b)) * (self.bw * self.bh))

    def set(self, x, y, c):
        bx = int(round(x * SS))
        by = int(round(y * SS))
        if 0 <= bx < self.bw and 0 <= by < self.bh:
            i = (by * self.bw + bx) * 3
            self.buf[i] = c[0]
            self.buf[i + 1] = c[1]
            self.buf[i + 2] = c[2]

    def rect(self, x, y, w, h, c):
        bx0 = max(0, int(round(x * SS)))
        by0 = max(0, int(round(y * SS)))
        bx1 = min(self.bw, int(round((x + w) * SS)))
        by1 = min(self.bh, int(round((y + h) * SS)))
        if bx1 <= bx0 or by1 <= by0:
            return
        buf = self.buf
        bw = self.bw
        row = bytes(c) * (bx1 - bx0)
        n = (bx1 - bx0) * 3
        for yy in range(by0, by1):
            base = (yy * bw + bx0) * 3
            buf[base:base + n] = row

    def hline(self, x0, x1, y, c, thick=1):
        if x1 < x0:
            x0, x1 = x1, x0
        self.rect(x0, y - thick // 2, x1 - x0 + 1, thick, c)

    def vline(self, x, y0, y1, c, thick=1):
        if y1 < y0:
            y0, y1 = y1, y0
        self.rect(x - thick // 2, y0, thick, y1 - y0 + 1, c)

    def line(self, x0, y0, x1, y1, c, thick=1):
        ax = int(round(x0 * SS))
        ay = int(round(y0 * SS))
        bx = int(round(x1 * SS))
        by = int(round(y1 * SS))
        t = max(1, int(round(thick * SS)))
        dx = abs(bx - ax)
        dy = -abs(by - ay)
        sx = 1 if ax < bx else -1
        sy = 1 if ay < by else -1
        err = dx + dy
        buf = self.buf
        bw = self.bw
        bh = self.bh
        half = t // 2
        while True:
            x0b = ax - half
            y0b = ay - half
            cx0 = x0b if x0b > 0 else 0
            cy0 = y0b if y0b > 0 else 0
            cx1 = x0b + t if x0b + t < bw else bw
            cy1 = y0b + t if y0b + t < bh else bh
            if cx1 > cx0 and cy1 > cy0:
                row = bytes(c) * (cx1 - cx0)
                n = (cx1 - cx0) * 3
                for yy in range(cy0, cy1):
                    base = (yy * bw + cx0) * 3
                    buf[base:base + n] = row
            if ax == bx and ay == by:
                break
            e2 = 2 * err
            if e2 >= dy:
                err += dy
                ax += sx
            if e2 <= dx:
                err += dx
                ay += sy

    def circle(self, cx, cy, r, c, fill=True):
        if fill:
            cbx = int(round(cx * SS))
            cby = int(round(cy * SS))
            rb = int(round(r * SS))
            if rb <= 0:
                self.set(cx, cy, c)
                return
            buf = self.buf
            bw = self.bw
            bh = self.bh
            r2 = rb * rb
            for dy in range(-rb, rb + 1):
                half = int((r2 - dy * dy) ** 0.5)
                y = cby + dy
                if 0 <= y < bh:
                    x0 = cbx - half
                    x1 = cbx + half
                    if x0 < 0:
                        x0 = 0
                    if x1 >= bw:
                        x1 = bw - 1
                    if x1 >= x0:
                        base = (y * bw + x0) * 3
                        buf[base:base + (x1 - x0 + 1) * 3] = bytes(c) * (x1 - x0 + 1)
        else:
            for a in range(0, 360, 2):
                x = cx + r * math.cos(math.radians(a))
                y = cy + r * math.sin(math.radians(a))
                self.set(x, y, c)

    def poly(self, pts, c):
        """Filled polygon via scanlines."""
        if len(pts) < 3:
            return
        bpts = [(int(round(px * SS)), int(round(py * SS))) for px, py in pts]
        ys = [p[1] for p in bpts]
        y0 = max(0, min(ys))
        y1 = min(self.bh - 1, max(ys))
        n = len(bpts)
        buf = self.buf
        bw = self.bw
        for y in range(y0, y1 + 1):
            xs = []
            for i in range(n):
                x1, y1p = bpts[i]
                x2, y2p = bpts[(i + 1) % n]
                if (y1p <= y < y2p) or (y2p <= y < y1p):
                    if y2p != y1p:
                        xs.append(x1 + (y - y1p) * (x2 - x1) / (y2p - y1p))
            xs.sort()
            for k in range(0, len(xs) - 1, 2):
                xa = max(0, int(xs[k]))
                xb = min(bw - 1, int(xs[k + 1]))
                if xb >= xa:
                    base = (y * bw + xa) * 3
                    buf[base:base + (xb - xa + 1) * 3] = bytes(c) * (xb - xa + 1)

    def _downsample(self):
        """2x2 box average of the SS buffer -> logical-size RGB bytes."""
        w, h = self.w, self.h
        src = self.buf
        sw = self.bw * 3
        out = bytearray(w * h * 3)
        for oy in range(h):
            r0 = src[(oy * SS) * sw:(oy * SS + 1) * sw]
            r1 = src[(oy * SS + 1) * sw:(oy * SS + 2) * sw]
            obase = oy * w * 3
            for ch in range(3):
                c0 = r0[ch::3]
                c1 = r1[ch::3]
                avg = bytes(((a + b + c + d + 2) // 4)
                            for a, b, c, d in zip(c0[0::2], c0[1::2],
                                                 c1[0::2], c1[1::2]))
                out[obase + ch:obase + w * 3:3] = avg
        return bytes(out)

    def save_png(self, path):
        data = self._downsample()
        raw = bytearray()
        stride = self.w * 3
        for y in range(self.h):
            raw.append(0)
            raw += data[y * stride:(y + 1) * stride]
        comp = zlib.compress(bytes(raw), 6)

        def chunk(typ, data):
            out = struct.pack(">I", len(data)) + typ + data
            out += struct.pack(">I", zlib.crc32(typ + data) & 0xFFFFFFFF)
            return out

        ihdr = struct.pack(">IIBBBBB", self.w, self.h, 8, 2, 0, 0, 0)
        png = b"\x89PNG\r\n\x1a\n"
        png += chunk(b"IHDR", ihdr)
        png += chunk(b"IDAT", comp)
        png += chunk(b"IEND", b"")
        with open(path, "wb") as f:
            f.write(png)
        return len(png)


# ---------------------------------------------------------------- font
# Real font glyphs: outlines extracted from the Liberation fonts (see
# fontdata.py), rendered as FILLED polygons with the even-odd rule on
# the 2x supersampled canvas. This is real printed type (Liberation
# Serif / Liberation Sans — Times/Arial metrics, the classic newspaper
# faces), not a stroke font: lowercase is true lowercase, counters are
# real holes, curves are the font's own curves. No runtime dependency
# on any font file.
from fontdata import FONTS, UPM  # noqa: E402

# Logical metrics: one em = 14 * scale px; the baseline sits 12.5 * scale px
# below the top of the cell (same cell geometry as the font before, so the
# layout code does not move).
_EM = 14.0
_BASELINE = 12.5
_TRACK = 0.5  # extra tracking, logical px per char, times scale


def _face(font, bold):
    if font == "serif":
        return "serif-bold" if bold else "serif"
    return "sans-bold" if bold else "sans"


def _glyph(face, ch):
    g = FONTS[face].get(ch)
    if g is None:
        g = FONTS[face][" "]
    return g


def char_adv(ch, scale, bold=False, font="sans"):
    """Advance width of one char in logical px."""
    adv = _glyph(_face(font, bold), ch)[0]
    return adv / UPM * _EM * scale + _TRACK * scale


def text_w(s, scale, bold=False, font="sans"):
    if not s:
        return 0
    return sum(char_adv(ch, scale, bold, font) for ch in s) - _TRACK * scale


def char_w(scale):
    """Legacy helper: width of an average char."""
    return int(round(0.6 * _EM * scale + _TRACK * scale))


_SPANS = {}


def _spans(face, ch, em_buf):
    """(advance_buf, [(dy, x0, x1), ...]) for one glyph at buffer resolution.

    Spans are relative to the baseline row (dy < 0 above it); x0/x1 are
    buffer columns relative to the glyph origin. Even-odd fill across all
    contours, so counters (O, D, A, ...) stay hollow. Computed once per
    (face, char, size) and cached.
    """
    key = (face, ch, em_buf)
    hit = _SPANS.get(key)
    if hit is not None:
        return hit
    adv_units, contours = _glyph(face, ch)
    s = em_buf / UPM
    adv_buf = adv_units * s
    bcons = []
    for cons in contours:
        bcons.append([(x * s, -y * s) for (x, y) in cons])
    spans = []
    if bcons:
        ys = [p[1] for bc in bcons for p in bc]
        y0 = int(math.floor(min(ys)))
        y1 = int(math.ceil(max(ys)))
        for dy in range(y0, y1 + 1):
            xs = []
            for bc in bcons:
                n = len(bc)
                for i in range(n):
                    x1, y1p = bc[i]
                    x2, y2p = bc[(i + 1) % n]
                    if (y1p <= dy < y2p) or (y2p <= dy < y1p):
                        if y2p != y1p:
                            xs.append(x1 + (dy - y1p) * (x2 - x1) / (y2p - y1p))
            xs.sort()
            for k in range(0, len(xs) - 1, 2):
                xa = int(xs[k])
                xb = int(xs[k + 1])
                if xb >= xa:
                    spans.append((dy, xa, xb))
    res = (adv_buf, spans)
    _SPANS[key] = res
    return res


def draw_char(cv, x, y, ch, scale, color, bold=False, font="sans"):
    """Draw one glyph. (x, y) is the top-left of the 14*scale logical cell."""
    face = _face(font, bold)
    em_buf = int(round(_EM * scale * SS))
    _, spans = _spans(face, ch, em_buf)
    if not spans:
        return
    bx0 = int(round(x * SS))
    by_base = int(round((y + _BASELINE * scale) * SS))
    buf = cv.buf
    bw = cv.bw
    bh = cv.bh
    pix = bytes(color)
    for dy, xa, xb in spans:
        yy = by_base + dy
        if 0 <= yy < bh:
            cx0 = bx0 + xa
            cx1 = bx0 + xb
            if cx0 < 0:
                cx0 = 0
            if cx1 >= bw:
                cx1 = bw - 1
            if cx1 >= cx0:
                base = (yy * bw + cx0) * 3
                buf[base:base + (cx1 - cx0 + 1) * 3] = pix * (cx1 - cx0 + 1)


def draw_text(cv, x, y, s, scale, color, bold=False, align="left", max_x=None,
              font="sans"):
    """Draw text; y is the top of the 14*scale cell. Returns width used."""
    w = text_w(s, scale, bold, font)
    if align == "center":
        x = x - w // 2
    elif align == "right":
        x = x - w
    cx = x
    for ch in s:
        draw_char(cv, cx, y, ch, scale, color, bold, font)
        cx += char_adv(ch, scale, bold, font)
    return w


def wrap_text(s, scale, max_w, bold=False, font="sans"):
    """Greedy word wrap; returns list of lines."""
    words = s.split(" ")
    lines = []
    cur = ""
    for w in words:
        trial = (cur + " " + w).strip()
        if text_w(trial, scale, bold, font) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines
