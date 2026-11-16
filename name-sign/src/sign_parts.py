"""The name sign, from a layout (tools/make_signs.py writes one per order).

A rounded plate, a raised border, the name raised on it and an optional icon beside it, each its
own body so the 3MF can give each a filament. Keyholes in the back to hang it on a nail or screw,
and/or pockets for 6 x 2 mm magnets (the owner's MakerWorld sign had eight).
Prints face up, back on the bed: the colours change only in the top 0.6-0.8 mm.
The other products' parts too (make_signs.extras lays them out): the keychain's tab and AirTag
pocket, the desk plate's tongue and weighted base, flush inlays (a face on the back in the first
layers, the number plate's band in the top ones), the villa sign's screw holes.

Dimensions in mm. The plate lies in XY, centred on the origin, its back at z 0.
"""

from __future__ import annotations

import json
import math
from pathlib import Path

from cadgen import build123d as bd

# The defaults copy the owner's MakerWorld sign (Make My Sign, 180 x 67.4)
PLATE_T = 4.08               # as the MakerWorld sign's plate
BORDER_INSET, BORDER_W, BORDER_H = 2.0, 2.0, 0.8
RAISE = 0.6                  # name and icon above the plate's face
# Keyhole, from the back: a nail head goes in the round end and slides along the slot under the lip
KEY_D = 7.0                  # entry, and the chamber the head slides in
KEY_SHANK = 3.2              # slot through the lip
KEY_SLOT = 6.0               # how far the slot runs from the entry's centre
KEY_LIP = 1.2                # lip the head hooks behind (on the bed)
KEY_CHAMBER = 1.6            # above the lip: leaves 1.2 mm of plate over it
# Magnet pocket, from the back, for a 6 x 2 mm disc, as the MakerWorld sign has them (measured from
# the owner's file): a round pocket with two relief tabs across it, end to end, to lever a magnet
# out or let a tight one seat; 2.0 deep, so 2.08 mm of plate over it. The owner's diameter: 6.01.
MAG_D, MAG_DEPTH = 6.01, 2.0
MAG_TAB_W, MAG_TAB_LEN = 2.0, 7.6     # the tabs: 2 mm wide, 7.6 mm end to end along the sign's height
MAG_TAB_R = 0.2                       # their corners


def _rounded(w: float, h: float, r: float) -> bd.Face:
    return bd.Face(bd.Wire.make_polygon(_rounded_pts(w, h, r), close=True))


def _rounded_pts(w: float, h: float, r: float, steps: int = 24) -> list[tuple[float, float]]:
    """A rounded rectangle's outline, corners sampled into straight runs (as the text is)."""
    import math
    r = max(0.01, min(r, w / 2 - 0.01, h / 2 - 0.01))
    pts = []
    for cx, cy, a0 in ((w / 2 - r, h / 2 - r, 0), (-w / 2 + r, h / 2 - r, 90), (-w / 2 + r, -h / 2 + r, 180), (w / 2 - r, -h / 2 + r, 270)):
        for i in range(steps + 1):
            a = math.radians(a0 + 90 * i / steps)
            pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


def _face(region: dict) -> bd.Face:
    outer = bd.Wire.make_polygon([(x, y) for x, y in region["outer"]], close=True)
    holes = [bd.Wire.make_polygon([(x, y) for x, y in h], close=True) for h in region["holes"]]
    return bd.Face(outer, holes)


def _raised(regions: list[dict], z0: float, height: float) -> bd.Shape | None:
    solids = [bd.extrude(_face(r), amount=height).moved(bd.Location((0, 0, z0))) for r in regions]
    if not solids:
        return None
    return bd.Compound(solids) if len(solids) > 1 else solids[0]


def keyhole(x: float, y: float, double: bool) -> bd.Shape:
    """What one keyhole takes out of the plate's back."""
    ends = (-KEY_SLOT, KEY_SLOT) if double else (0.0, KEY_SLOT)

    def run(width: float, z0: float, z1: float) -> bd.Shape:
        slot = bd.Box(width, ends[1] - ends[0], z1 - z0, align=(bd.Align.CENTER, bd.Align.MIN, bd.Align.MIN))
        slot = slot.moved(bd.Location((x, y + ends[0], z0)))
        tips = [bd.Cylinder(width / 2, z1 - z0, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN)).moved(bd.Location((x, y + e, z0)))
                for e in ends]
        return slot + tips

    entry = bd.Cylinder(KEY_D / 2, KEY_LIP + KEY_CHAMBER + 0.01, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))
    entry = entry.moved(bd.Location((x, y, -0.01)))
    return entry + run(KEY_SHANK, -0.01, KEY_LIP + 0.01) + run(KEY_D, KEY_LIP, KEY_LIP + KEY_CHAMBER)


def magnet(x: float, y: float) -> bd.Shape:
    """What one magnet pocket takes out of the plate's back: the round pocket and its relief tabs."""
    h = MAG_DEPTH + 0.01
    disc = bd.Cylinder(MAG_D / 2, h, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))
    tabs = bd.Box(MAG_TAB_W, MAG_TAB_LEN, h, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))
    tabs = bd.fillet(tabs.edges().filter_by(bd.Axis.Z), MAG_TAB_R)
    return (disc + tabs).moved(bd.Location((x, y, -0.01)))


def through(x: float, y: float, d: float, t: float, csk: float | None = None) -> bd.Shape:
    """A hole through the plate; with csk, countersunk from the face (90°, for a flat-head screw).
    Printed face up, the countersink opens upwards: no overhang."""
    cut = bd.Cylinder(d / 2, t + 0.02, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN)).moved(bd.Location((x, y, -0.01)))
    if csk:
        depth = (csk - d) / 2
        cut = cut + bd.Cone(d / 2, csk / 2 + 0.01, depth + 0.01, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN)).moved(bd.Location((x, y, t - depth)))
    return cut


def stand(st: dict) -> bd.Shape:
    """The desk plate's stand, as it prints and as it sits: a wedge-shaped bar whose slot holds the
    plate's tongue leaning back by st['lean'] degrees. Its front is -y. Both slot walls lean only
    that far from upright, so it prints without supports. With weights: round pockets in its
    underside for steel washers or coins, closed by a felt pad (their roofs bridge)."""
    L, D, H, top = st["l"], st["depth"], st["height"], st["top"]
    profile = bd.Polygon((-D / 2, 0), (D / 2, 0), (top / 2, H), (-top / 2, H), align=None)
    bar = bd.extrude(bd.Plane.YZ * profile, amount=L / 2, both=True)
    lean = math.radians(st["lean"])
    deep = st["slot_depth"]
    # the slot's bottom, down the slot from its mouth in the top face (forward as it goes down)
    yb, zb = st["slot_y"] - deep * math.sin(lean), H - deep * math.cos(lean)
    slot = bd.Box(st["slot_w"], st["slot_t"], deep + 10, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))
    slot = slot.rotate(bd.Axis.X, -st["lean"]).moved(bd.Location((0, yb, zb)))
    cuts = [slot]
    wt = st.get("weights")
    if wt:
        cuts += [bd.Cylinder(wt["d"] / 2, wt["depth"] + 0.01, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN)).moved(bd.Location((x, wt["y"], -0.01)))
                 for x in wt["x"]]
    return bar - cuts


def _outline(p: dict) -> bd.Face:
    """The plate's face: its rounded rectangle, or the outline make_signs gives it (the keychain's tab)."""
    if p.get("outline"):
        return bd.Face(bd.Wire.make_polygon([(x, y) for x, y in p["outline"]], close=True))
    return _rounded(p["w"], p["h"], p["r"])


def airtag_pocket(a: dict) -> bd.Shape:
    """What the AirTag holder takes out of the plate: the window through the lip, the round pocket
    and its channel out to the plate's bottom edge, less the ridge across the channel's floor."""
    x, y, d = a["x"], a["y"], a["d"]
    window = bd.Cylinder(a["window"] / 2, a["lip"] + 0.02, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN)).moved(bd.Location((x, y, -0.01)))
    pocket = bd.Cylinder(d / 2, a["t"], align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN)).moved(bd.Location((x, y, a["lip"])))
    channel = bd.Box(d, y + 200, a["t"], align=(bd.Align.CENTER, bd.Align.MAX, bd.Align.MIN)).moved(bd.Location((x, y, a["lip"])))
    # the ridge: a low rounded bump across the channel's floor (half an ellipse, lying along x)
    pts = [(a["ridge_y"] + a["ridge_w"] / 2 * math.cos(math.pi * i / 16), a["lip"] + a["ridge"] * math.sin(math.pi * i / 16)) for i in range(17)]
    profile = bd.Polygon(*pts, (a["ridge_y"] - a["ridge_w"] / 2, a["lip"] - 0.05), (a["ridge_y"] + a["ridge_w"] / 2, a["lip"] - 0.05), align=None)
    ridge = bd.extrude(bd.Plane.YZ * profile, amount=d / 2 + 1, both=True).moved(bd.Location((x, 0, 0)))
    return window + pocket + channel - ridge


def airtag_model(a: dict) -> bd.Shape:
    """The AirTag, near enough for the fit checks: 31.9 across, 8.0 thick, its edge rounded, lying
    on the lip in its pocket."""
    tag = bd.Cylinder(a["tag"]["d"] / 2, a["tag"]["t"], align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))
    tag = bd.fillet(tag.edges(), 2.5)
    return tag.moved(bd.Location((a["x"], a["y"], a["lip"])))


def sign(layout: dict) -> dict[str, bd.Shape]:
    """The sign's bodies by name: plate, border, text, text2, icon (the last four only when present);
    a product's also collar, number, divider and stand (sign_parts' extras, make_signs.extras)."""
    p = layout["plate"]
    w, h, r, t = p["w"], p["h"], p["r"], p.get("t", PLATE_T)
    plate = bd.extrude(_outline(p), amount=t)
    if p.get("tongue"):                   # the desk plate's: below the plate, into the stand's slot
        tg = p["tongue"]
        plate = plate + bd.Box(tg["w"], tg["h"] + 1, t, align=(bd.Align.CENTER, bd.Align.MAX, bd.Align.MIN)).moved(bd.Location((0, -h / 2 + 1, 0)))
    if layout.get("lugs"):                # the keychain's tab, raised in the plate's colour round its hole
        lug = _raised(layout["lugs"], t, layout["raise"]["lug"])
        plate = plate + lug
    holes = [keyhole(k["x"], k["y"], k.get("double", False)) for k in layout.get("holes", [])]
    holes += [magnet(m["x"], m["y"]) for m in layout.get("magnets", [])]
    holes += [through(c["x"], c["y"], c["d"], t + (layout["raise"].get("lug", 0) if layout.get("lugs") else 0), c.get("csk")) for c in layout.get("through", [])]
    if layout.get("airtag"):
        holes.append(airtag_pocket(layout["airtag"]))
    if holes:
        plate = plate - holes
    # Flush inlays, each its own colour: the back face in the first layers, a band in the top ones
    inlays = {}
    for name, inl in (layout.get("inlays") or {}).items():
        z0 = 0.0 if inl["at"] == "bottom" else t - inl["depth"]
        body = _raised(inl["regions"], z0, inl["depth"])
        if body is not None:
            inlays[name] = body
            plate = plate - body
    out = {"plate": plate, **inlays}
    b = layout.get("border")
    if b:
        outer = _rounded(w - 2 * b["inset"], h - 2 * b["inset"], r - b["inset"])
        inner = _rounded(w - 2 * (b["inset"] + b["width"]), h - 2 * (b["inset"] + b["width"]), r - b["inset"] - b["width"])
        out["border"] = bd.extrude(outer - inner, amount=b.get("h", BORDER_H)).moved(bd.Location((0, 0, t)))
    for name in ("text", "text2", "icon", "number", "divider", "inverse"):
        body = _raised(layout.get(name) or [], t, layout.get("raise", {}).get(name, RAISE))
        if body is not None:
            out[name] = body
    if layout.get("collars"):             # the keychain's: a raised ring round the key-ring hole, one with the border
        rings = [bd.extrude(bd.Face(bd.Wire.make_circle(c["d"] / 2)) - bd.Face(bd.Wire.make_circle(c["hole"] / 2)),
                            amount=layout.get("raise", {}).get("collar", RAISE)).moved(bd.Location((c["x"], c["y"], t)))
                 for c in layout["collars"]]
        collar = rings[0] if len(rings) == 1 else bd.Compound(rings)
        if "border" in out:
            out["border"] = out["border"] + collar
        else:
            out["collar"] = collar
    if layout.get("stand"):
        st = layout["stand"]
        out["stand"] = stand(st).moved(bd.Location((st["at"][0], st["at"][1], 0)))
    return out


def standing(layout: dict, bodies: dict[str, bd.Shape]) -> dict[str, bd.Shape]:
    """The desk plate as it stands on a desk: the plate's bodies turned up into the stand's slot
    (for its render; the print files keep them lying flat beside each other)."""
    st, p = layout["stand"], layout["plate"]
    lean = math.radians(st["lean"])
    # the tongue's bottom edge, middle of its thickness, goes to the slot's bottom
    yb, zb = st["slot_y"] - st["slot_depth"] * math.sin(lean), st["height"] - st["slot_depth"] * math.cos(lean)
    bottom = -p["h"] / 2 - p["tongue"]["h"]
    out = {"stand": bodies["stand"].moved(bd.Location((-st["at"][0], -st["at"][1], 0)))}
    for name, body in bodies.items():
        if name == "stand":
            continue
        up = body.moved(bd.Location((0, -bottom, -p.get("t", PLATE_T) / 2)))          # tongue's bottom middle at the origin
        up = up.rotate(bd.Axis.X, 90 - st["lean"])
        out[name] = up.moved(bd.Location((0, yb, zb)))
    return out


def load(path: str | Path) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))
