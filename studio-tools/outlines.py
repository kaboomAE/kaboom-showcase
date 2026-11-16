"""Flat outlines in millimetres, for parts that raise or cut text and artwork: shared by the projects.

    text_regions(lines, font_file, em_mm)  shaped with HarfBuzz (kerning, ligatures, Arabic joining
                                           and right-to-left), outlines from the font with fontTools
    svg_regions(svg_file, height_mm)       an SVG's filled shapes, transforms applied
    thin_share(geom, nozzle_mm)            how much of an outline is narrower than two lines of the nozzle

Regions are {"outer": [[x, y], ...], "holes": [[[x, y], ...], ...]} with y up, the same shape as
brand/kaboom_logo.json, so a cadgen model can extrude them without these libraries.
Needs: fonttools, uharfbuzz, shapely, svgelements.
"""

from __future__ import annotations

from pathlib import Path

import shapely
import uharfbuzz as hb
from fontTools.pens.basePen import BasePen
from fontTools.ttLib import TTFont
from shapely.geometry import MultiPolygon, Polygon
from shapely.ops import unary_union

CURVE_STEPS = 10          # straight runs per curve segment: well under 0.05 mm off on 30 mm letters


class _Flatten(BasePen):
    """Collects a glyph's contours as point rings, curves sampled into short straight runs."""

    def __init__(self, glyphset):
        super().__init__(glyphset)
        self.rings: list[list[tuple[float, float]]] = []
        self._ring: list[tuple[float, float]] = []

    def _moveTo(self, p):
        self._ring = [p]

    def _lineTo(self, p):
        self._ring.append(p)

    def _curveToOne(self, p1, p2, p3):
        p0 = self._ring[-1]
        for i in range(1, CURVE_STEPS + 1):
            t = i / CURVE_STEPS
            a, b, c, d = (1 - t) ** 3, 3 * t * (1 - t) ** 2, 3 * t * t * (1 - t), t ** 3
            self._ring.append((a * p0[0] + b * p1[0] + c * p2[0] + d * p3[0], a * p0[1] + b * p1[1] + c * p2[1] + d * p3[1]))

    def _qCurveToOne(self, p1, p2):
        p0 = self._ring[-1]
        for i in range(1, CURVE_STEPS + 1):
            t = i / CURVE_STEPS
            a, b, c = (1 - t) ** 2, 2 * t * (1 - t), t * t
            self._ring.append((a * p0[0] + b * p1[0] + c * p2[0], a * p0[1] + b * p1[1] + c * p2[1]))

    def _closePath(self):
        if len(self._ring) >= 3:
            self.rings.append(self._ring)
        self._ring = []

    _endPath = _closePath


def _fill_nonzero(rings: list[list[tuple[float, float]]]):
    """Rings filled by the non-zero rule: biggest first, each added or cut by its turning direction."""
    polys = []
    for r in rings:
        p = Polygon(r)
        if not p.is_valid:
            p = p.buffer(0)
        if p.area > 1e-9:
            polys.append((abs(Polygon(r).area), Polygon(r).exterior.is_ccw, p))
    if not polys:
        return Polygon()
    polys.sort(key=lambda t: -t[0])
    solid_dir = polys[0][1]
    out = Polygon()
    for _, ccw, p in polys:
        out = out.union(p) if ccw == solid_dir else out.difference(p)
    return out


def _visual_runs(line: str) -> list[tuple[str, bool]]:
    """A line split into runs of one direction, in the order they read left to right on the sign.

    A simple form of the Unicode bidi rules, enough for names and addresses: Arabic letters run right
    to left, Latin letters and numbers (Arabic-Indic digits too) left to right; spaces and marks go
    with the run before them. In a line that starts with Arabic, the runs are laid right to left,
    so "فيلا ١٢" keeps its number the right way round.
    """
    import unicodedata

    def kind(ch: str) -> str | None:
        b = unicodedata.bidirectional(ch)
        return "R" if b in ("R", "AL") else "L" if b == "L" else "N" if b in ("EN", "AN") else None

    runs: list[list] = []
    for ch in line:
        k = kind(ch)
        if runs and (k is None or k == runs[-1][1] or (k == "N" and runs[-1][1] == "L")):
            runs[-1][0] += ch
        else:
            runs.append([ch, k])
    for r in runs:                      # a run of only spaces or marks at the start takes the next run's kind
        if r[1] is None:
            r[1] = next((q[1] for q in runs if q[1]), "L")
    first_strong = next((r[1] for r in runs if r[1] in ("R", "L")), "L")
    if first_strong == "R":
        # Laid right to left: a left-to-right run's space after it (logically) shows on its left
        for r in runs:
            if r[1] != "R" and r[0] != r[0].rstrip():
                r[0] = " " + r[0].rstrip()
        runs = runs[::-1]
    # A run keeps its trailing space: shaped in its own direction, it lands between it and the next run
    return [(text, k == "R") for text, k in runs if text.strip()] or [(line, False)]


def text_regions(lines: list[str], font_file: str | Path, em_mm: float, line_height: float = 1.16):
    """Lines of text centred on each other, the block centred on (0, 0). Returns a shapely geometry."""
    font_file = Path(font_file)
    tt = TTFont(font_file)
    upm = tt["head"].unitsPerEm
    order = tt.getGlyphOrder()
    glyphs = tt.getGlyphSet()
    face = hb.Face(hb.Blob.from_file_path(str(font_file)))
    font = hb.Font(face)
    scale = em_mm / upm
    shaped_lines = []
    for n, line in enumerate(lines):
        x, parts = 0.0, []
        for run, rtl in _visual_runs(line):
            buf = hb.Buffer()
            buf.add_str(run)
            buf.guess_segment_properties()      # the script: Arabic letters join
            buf.direction = "rtl" if rtl else "ltr"
            hb.shape(font, buf, {"kern": True, "liga": True})
            for info, pos in zip(buf.glyph_infos, buf.glyph_positions):   # visual order, left to right
                pen = _Flatten(glyphs)
                glyphs[order[info.codepoint]].draw(pen)
                if pen.rings:
                    ox, oy = (x + pos.x_offset) * scale, pos.y_offset * scale - n * line_height * em_mm
                    rings = [[(ox + u * scale, oy + v * scale) for u, v in r] for r in pen.rings]
                    parts.append(_fill_nonzero(rings))
                x += pos.x_advance
        geom = unary_union(parts) if parts else Polygon()
        if not geom.is_empty:
            minx, _, maxx, _ = geom.bounds
            geom = shapely.affinity.translate(geom, -(minx + maxx) / 2, 0)
        shaped_lines.append(geom)
    block = unary_union(shaped_lines)
    if block.is_empty:
        return block
    minx, miny, maxx, maxy = block.bounds
    return shapely.affinity.translate(block, -(minx + maxx) / 2, -(miny + maxy) / 2)


def svg_regions(svg_file: str | Path, height_mm: float):
    """The SVG's filled shapes, scaled to height_mm tall and centred on (0, 0). Strokes are ignored."""
    from svgelements import SVG, Path as SvgPath, Shape

    svg = SVG.parse(str(svg_file), reify=True)
    shapes = []
    for el in svg.elements():
        if not isinstance(el, Shape) or el.fill is None or el.fill.value is None:
            continue
        path = abs(SvgPath(el))
        rings = []
        for sub in path.as_subpaths():
            sub = SvgPath(sub)
            if sub.length(error=1e-3) == 0:
                continue
            n = max(16, int(sub.length(error=1e-3) / max(path.bbox()[3] - path.bbox()[1], 1e-6) * 200))
            pts = [sub.point(i / n) for i in range(n)]
            rings.append([(p.x, -p.y) for p in pts])          # SVG y runs down
        if not rings:
            continue
        if str(el.values.get("fill-rule", "nonzero")).strip() == "evenodd":
            g = Polygon()
            for r in rings:
                g = g.symmetric_difference(Polygon(r).buffer(0))
        else:
            g = _fill_nonzero(rings)
        shapes.append(g)
    geom = unary_union(shapes)
    if geom.is_empty:
        raise ValueError(f"{svg_file}: no filled shapes (outlines drawn as strokes only don't count)")
    minx, miny, maxx, maxy = geom.bounds
    s = height_mm / (maxy - miny)
    geom = shapely.affinity.scale(geom, s, s, origin=(0, 0))
    minx, miny, maxx, maxy = geom.bounds
    return shapely.affinity.translate(geom, -(minx + maxx) / 2, -(miny + maxy) / 2)


def thin_share(geom, nozzle_mm: float = 0.4) -> float:
    """Share of the area in strokes thinner than two nozzle widths (they print badly or vanish)."""
    if geom.is_empty:
        return 0.0
    kept = geom.buffer(-nozzle_mm, join_style=2).buffer(nozzle_mm, join_style=2)
    return max(0.0, 1 - kept.area / geom.area)


def regions(geom, dx: float = 0.0, dy: float = 0.0, ndigits: int = 3) -> list[dict]:
    """A shapely geometry as JSON-ready regions, moved by (dx, dy)."""
    geom = shapely.affinity.translate(geom, dx, dy).buffer(0)
    polys = list(geom.geoms) if isinstance(geom, MultiPolygon) else [geom] if not geom.is_empty else []
    out = []
    for p in polys:
        p = shapely.geometry.polygon.orient(p.simplify(0.01), 1.0)       # outer anticlockwise
        ring = lambda r: [[round(x, ndigits), round(y, ndigits)] for x, y in list(r.coords)[:-1]]
        out.append({"outer": ring(p.exterior), "holes": [ring(h) for h in p.interiors]})
    return out
