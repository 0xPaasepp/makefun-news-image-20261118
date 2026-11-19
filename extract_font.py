"""Extract real glyph outlines from Liberation TTFs into fontdata.py.

Stdlib + fontTools (build-time only; the entry itself is stdlib-only).
Run: python3 extract_font.py   (writes fontdata.py next to this script)

Liberation fonts are metrically Times New Roman / Arial (SIL Open Font
License). UPM is 2048, same as the DejaVu data this replaces.

Output format matches the old fontdata.py: one glyph per line,
'c': (advance, [contour, ...]), contours are lists of (x, y) points
in font units, y-up from the baseline. Quadratic curves are flattened
to polylines (12 subdivisions per curve — deterministic).
"""
import os
import sys

from fontTools.ttLib import TTFont

HERE = os.path.dirname(os.path.abspath(__file__))
LIB = "/usr/share/fonts/truetype/liberation"

FACES = {
    "sans": "LiberationSans-Regular.ttf",
    "sans-bold": "LiberationSans-Bold.ttf",
    "serif": "LiberationSerif-Regular.ttf",
    "serif-bold": "LiberationSerif-Bold.ttf",
}

# ASCII printable (32-126) + middle dot, en dash, em dash, bullet —
# the exact charset the entry's text uses.
CHARSET = ([chr(c) for c in range(32, 127)]
           + ["\u00b7", "\u2013", "\u2014", "\u2022"])

STEPS = 12


def _flatten_quad(p0, p1, p2):
    """Subdivide a quadratic Bezier into STEPS line segments (excl. p0)."""
    pts = []
    for i in range(1, STEPS + 1):
        t = i / STEPS
        u = 1 - t
        x = u * u * p0[0] + 2 * u * t * p1[0] + t * t * p2[0]
        y = u * u * p0[1] + 2 * u * t * p1[1] + t * t * p2[1]
        pts.append((int(round(x)), int(round(y))))
    return pts


def _flatten_contour(coords, flags):
    """coords/flags for one contour -> polyline points (no duplicate close)."""
    n = len(coords)
    if n == 0:
        return []
    if n == 1:
        return [coords[0]]
    # Build the point walk: start at an on-curve point if there is one,
    # else at the implied midpoint of the last/first off-curve pair.
    pts = []  # list of (x, y, on_curve)
    start = 0
    if not flags[0]:
        # implied on-curve start point between last and first points
        mid = ((coords[-1][0] + coords[0][0]) // 2,
               (coords[-1][1] + coords[0][1]) // 2)
        pts.append((mid[0], mid[1], True))
    else:
        start = 0
    for i in range(start, n):
        pts.append((coords[i][0], coords[i][1], bool(flags[i])))
    if not flags[0]:
        # the walk ends at the implied start point again — drop the dup
        pass
    # rotate so the walk starts at the first on-curve point
    first_on = next((i for i, p in enumerate(pts) if p[2]), 0)
    pts = pts[first_on:] + pts[:first_on]
    out = [pts[0][:2]]
    i = 1
    m = len(pts)
    while i < m:
        p = pts[i]
        if p[2]:
            out.append(p[:2])
            i += 1
        else:
            # quadratic: p is control, next point (or implied start) is end
            q = pts[(i + 1) % m]
            if q[2]:
                end = q[:2]
                i += 2
            else:
                end = ((p[0] + q[0]) // 2, (p[1] + q[1]) // 2)
                i += 1
            out.extend(_flatten_quad(out[-1], p[:2], end))
            if q[2]:
                pass
            else:
                # q is the next control point; loop continues from it
                # (it is already the next item in pts after i advanced)
                pass
    # drop a duplicate closing point if the last equals the first
    if len(out) > 1 and out[-1] == out[0]:
        out.pop()
    return out


def extract(path):
    font = TTFont(path)
    upm = font["head"].unitsPerEm
    assert upm == 2048, "unexpected UPM %d in %s" % (upm, path)
    cmap = font.getBestCmap()
    glyf = font["glyf"]
    hmtx = font["hmtx"]
    glyphs = {}
    for ch in CHARSET:
        code = ord(ch)
        if code not in cmap:
            raise SystemExit("missing glyph for %r in %s" % (ch, path))
        name = cmap[code]
        glyph = glyf[name]
        adv = hmtx[name][0]
        contours = []
        if glyph.numberOfContours > 0:
            coords, ends, flags = glyph.getCoordinates(glyf)
            start = 0
            for end in ends:
                c = _flatten_contour(coords[start:end + 1],
                                     flags[start:end + 1])
                if len(c) >= 3:
                    contours.append(c)
                start = end + 1
        glyphs[ch] = (adv, contours)
    return glyphs


def main():
    all_faces = {}
    for face, fname in FACES.items():
        path = os.path.join(LIB, fname)
        all_faces[face] = extract(path)
        print("extracted %s: %d glyphs from %s"
              % (face, len(all_faces[face]), fname))
    out = []
    out.append('"""Real font glyph outlines, extracted from the Liberation fonts.')
    out.append('')
    out.append('Liberation fonts are metrically Times New Roman / Arial')
    out.append('(SIL Open Font License). See /usr/share/fonts/truetype/liberation/.')
    out.append('Data: one glyph per line, \'A\': (advance, [contour, ...]), contours are')
    out.append('lists of (x, y) points in font units, y-up from the baseline.')
    out.append('Generated by the build-time extractor (extract_font.py, in this repo).')
    out.append('"""')
    out.append('UPM = 2048')
    out.append('')
    out.append('FONTS = {')
    for face in ("sans", "sans-bold", "serif", "serif-bold"):
        glyphs = all_faces[face]
        out.append('    %r: {' % face)
        for ch in CHARSET:
            adv, contours = glyphs[ch]
            out.append('        %r: (%d, %r),'
                       % (ch, adv, contours))
        out.append('    },')
    out.append('}')
    dest = os.path.join(HERE, "fontdata.py")
    with open(dest, "w", encoding="utf-8") as f:
        f.write("\n".join(out) + "\n")
    print("wrote %s (%d bytes)" % (dest, os.path.getsize(dest)))


if __name__ == "__main__":
    main()
