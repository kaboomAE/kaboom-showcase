"""KABOOM's teardrop mounting spots on the travel case's outside, and the sample attachments (helper, not a model).

Rev G. Rev F's dovetail rails needed support and a rail could crack off; the owner chose
KABOOM's own teardrop holes and latching pegs instead, and then (on seeing a full pegboard)
spots for 8 to 10 attachments at most, the rest of the case smooth. So there are nine SPOTS:
each is the two holes, 28 apart, one attachment's two pegs hang on (the lid's tray spot has a
third, for its latch). Every wall attachment has the same two pegs, so any of them fits any
spot. The spots sit on the case's own lines: 75 mm either side of the seam on the sides and
the back, centred or 42 mm off the middle, the back's lower one clear of the power inlet.

The hole. Every hole is the same, HOLE_DEPTH deep in the 6 mm wall, so 2 mm stays behind it
and nothing shows inside. Seen face on, a peg goes in at the ENTRY, at the top, and drops
DROP down a SLOT to its SEAT, where the LIP either side of the slot holds its head. The entry
is the peg's head shape with steep points above and below: its pointed roof prints with
no support on the shell halves, which print standing up. Behind the lip the hole widens at
50 degrees to its full width, so the lid panels, which print flat, print their lips without
support too (their holes are the same, turned so the peg slides along the lid).

The peg. A short neck and a wider head, both diamonds in section (a circle with 50 degree
points above and below), so a peg prints lying along the bed, upright or upside down, with
no overhang: the layers run along the peg, never across its root. The head's sides flare
at 50 degrees from the neck, matching the lip's back. Pegs are part of their attachment.

The latch. One peg of each attachment has a sprung tongue cut in the plate above it, with
a bump on its back. Pushed onto the wall at the entries, the bump presses on the wall and
the tongue bends; drop the attachment and the bump snaps into the entry the peg came in by,
filling it, so the attachment can't lift and come off however the case is carried, tilted
or knocked. Pull the tab at the tongue's end to lift it out. Two catches were drawn for the
PLA test kit: "latch" (a square catch, released only by the tab) and "click" (its top
ramped, a stiffer tongue: lifts off with a firm pull). The attachments carry the latch.

Everything is built in one local frame per face and placed by frame(): local X along the
face, local Z up (on the lid, toward the front), local +Y into the wall, the wall's surface
at y = 0 and an attachment's body at y < 0. Pegs and holes are drawn in their PROFILE frame,
the drop down -Z; on the lid that frame is turned so the drop runs along local +X.
"""

from __future__ import annotations

import math

from cadgen import build123d as bd

import travel_parts as tp

PITCH = 28.0
# Every face that has to print without support leans at POINT from the horizontal: 5 degrees
# steeper than the usual 45, so none sits on the line (studio/print_audit.py counts 45 as over).
POINT = math.radians(50.0)
STEEP = math.tan(POINT)      # rise per mm across, on those faces
FLARE = 1.0 / STEEP          # how much the lip's back and the head's sides widen per mm in
# The peg (profile frame: x along the face, z up, seated at the origin)
R = 4.0                      # head: a circle this radius with a point above and below (the diamond)
NECK = 2.4                   # the neck's half width: the head stands 1.6 proud of it each side
NECK_L = 1.8                 # plate to head: the lip and 0.2
PEG_L = 3.6                  # plate to the head's back, 0.4 off the hole's floor
# The hole
HOLE_DEPTH = 4.0             # 2.0 of the 6 mm wall stays behind it (the house rule asks 1.9)
LIP = 1.6
DROP = 9.0                   # entry to seat: the head's ears are well under the lip at the seat
CLEAR = 0.25                 # hole over peg, each side; the Rev G kit tries 0.15 / 0.25 / 0.35
CLEARS = (0.15, 0.25, 0.35)
PLATE_T = 4.0                # attachment back plates
# The latch: a tongue in the plate, its bump in the entry of the hole its peg came in by
TONGUE_W = 8.0
TONGUE_L = 22.0              # free end to root
TONGUE_GAP = 1.0             # cut round it, through the plate
TONGUE_T = {"latch": 1.6, "click": 2.2}
BUMP_UP = 2.5                # the bump's foot above the entry's centre (at the plate)
BUMP_H = 1.2                 # how far it stands into the hole: the tongue bends this much going on
BUMP_CLEAR = 0.4             # under the entry's roof once seated: the most it can lift
TAB = 4.0                    # the pull at the tongue's free end, on its front

# The spots. A seat is where a peg sits once dropped; its hole runs from HOLE_BELOW under it to
# HOLE_ABOVE over it. A spot's frame is the attachment's: its seats are at SPOT_SEATS in it.
LOWER, UPPER = tp.Z_SPLIT - 75.0, tp.Z_SPLIT + 75.0      # 145 (Rev F's lower rail) and 295
OFF = 42.0                                               # the side spots either side of the middle
SPOT_SEATS = ((-PITCH / 2, 0.0), (PITCH / 2, 0.0))       # every wall spot; the latch is over the right one
LID_SEATS = ((-PITCH / 2, 0.0), (PITCH / 2, 0.0), (PITCH / 2, PITCH))   # the tray's two, and its latch's (local u, v)
SPOTS = {                                                # name: (face, along, height or depth)
    "right upper": ("right", 0.0, UPPER),
    "right lower front": ("right", -OFF, LOWER),
    "right lower back": ("right", OFF, LOWER),
    "left upper": ("left", 0.0, UPPER),
    "left lower front": ("left", -OFF, LOWER),
    "left lower back": ("left", OFF, LOWER),
    "back upper": ("back", 0.0, UPPER),
    "back lower": ("back", -OFF, LOWER),                 # beside the power inlet, not over it (it is at x +51)
    "lid": ("top", 0.0, 2 * PITCH),                      # the back lid panel
}
HOLE_HALF = R + CLEAR
HOLE_BELOW = HOLE_HALF / math.cos(POINT)
HOLE_ABOVE = DROP + HOLE_BELOW
# Where no hole may reach (world coordinates of the face, with room round them)
HANDLE_ZONE = (-tp.HANDLE_DEPTH / 2 - 4.0, tp.HANDLE_DEPTH / 2 + 4.0, tp.H - tp.HANDLE_LEG - 4.0)   # y0, y1, z0
IEC_ZONE = (tp.IEC_X - 28.0, tp.IEC_X + 28.0, tp.IEC_Z - 16.0, tp.IEC_Z + 16.0)   # the inlet's flange, x0 x1 z0 z1
SEAM_ROOM = 4.0


def frame(face: str, a: float, b: float) -> bd.Location:
    """Local frame centred at (a, b) on a face: sides take (y, z), back (x, z), top (x, y)."""
    top = tp.LID_Z0 + tp.LID_T
    origin, x_dir, z_dir = {
        "right": ((tp.W / 2, a, b), (0, 1, 0), (0, 0, 1)),
        "left": ((-tp.W / 2, a, b), (0, -1, 0), (0, 0, 1)),
        "back": ((a, tp.D / 2, b), (-1, 0, 0), (0, 0, 1)),
        "top": ((a, b, top), (-1, 0, 0), (0, -1, 0)),
    }[face]
    return bd.Location(bd.Plane(origin=origin, x_dir=x_dir, z_dir=z_dir))


# --- profile shapes --------------------------------------------------------------

def _stadium(a: float, z0: float, z1: float) -> bd.Face:
    """The diamond of radius a (a circle with a point above and below, its sides at POINT), swept from z0 up to z1.

    Drawn in XY as (x, z). With z0 == z1 it is the diamond itself.
    """
    tip = a / math.cos(POINT)                            # centre to point
    phi = math.pi / 2 - POINT                            # where the point's sides touch the circle
    kx, kz = a * math.cos(phi), a * math.sin(phi)
    mx, mz = a * math.cos(phi / 2), a * math.sin(phi / 2)
    e = [bd.Line((0, z1 + tip), (kx, z1 + kz)), bd.ThreePointArc((kx, z1 + kz), (mx, z1 + mz), (a, z1))]
    if z1 > z0:
        e.append(bd.Line((a, z1), (a, z0)))
    e += [bd.ThreePointArc((a, z0), (mx, z0 - mz), (kx, z0 - kz)), bd.Line((kx, z0 - kz), (0, z0 - tip)),
          bd.Line((0, z0 - tip), (-kx, z0 - kz)), bd.ThreePointArc((-kx, z0 - kz), (-mx, z0 - mz), (-a, z0))]
    if z1 > z0:
        e.append(bd.Line((-a, z0), (-a, z1)))
    e += [bd.ThreePointArc((-a, z1), (-mx, z1 + mz), (-kx, z1 + kz)), bd.Line((-kx, z1 + kz), (0, z1 + tip))]
    return bd.Face(bd.Wire(e))


def _strip(a: float, w: float, z0: float, z1: float) -> bd.Face:
    """The middle 2w of the diamond of radius a, swept from z0 up to z1: the neck, or the slot."""
    t, s = a / math.cos(POINT), w * STEEP
    pts = [(0, z1 + t), (w, z1 + t - s), (w, z0 - t + s), (0, z0 - t), (-w, z0 - t + s), (-w, z1 + t - s)]
    return bd.Face(bd.Wire.make_polygon([bd.Vector(x, z) for x, z in pts], close=True))


def _prism(face: bd.Face, y0: float, y1: float) -> bd.Solid:
    """A profile face drawn in XY as (x, z), run along local Y from y0 to y1."""
    return bd.extrude(face, amount=y1 - y0, dir=(0, 0, 1)).moved(bd.Location((0, 0, -y1))).rotate(bd.Axis.X, 90)


def _flare(w: float, y0: float, y1: float) -> bd.Solid:
    """|x| <= w at y0, widening by FLARE a mm to y1: the head's and the lip's sides."""
    g = (y1 - y0) * FLARE
    return tp._prism_xy([(-w, y0), (w, y0), (w + g, y1), (-w - g, y1)], -100, 100)


def _profile_yz(pts: list[tuple[float, float]], x0: float, x1: float) -> bd.Shape:
    return tp._prism_yz(pts, x0, x1)


# --- the hole and the peg (profile frame) -------------------------------------------

def hole_tool(clear: float = CLEAR) -> bd.Shape:
    """One hole, its seat at the origin, as the solid it removes: entry, slot, and the widening behind the lip."""
    a, w = R + clear, NECK + clear
    parts = [_prism(_stadium(a, DROP, DROP), -1.0, HOLE_DEPTH),             # the entry, the full depth
             _prism(_strip(a, w, 0, DROP), -1.0, LIP + 0.01),               # the slot through the lip
             _prism(_stadium(a, 0, DROP), LIP, HOLE_DEPTH) & _flare(w, LIP, HOLE_DEPTH)]
    tool = parts[0].fuse(parts[1], parts[2]).clean()
    return tool


def peg() -> bd.Shape:
    """One peg, seated at the origin: the neck from inside the plate, then the head flaring out."""
    neck = _prism(_strip(R, NECK, 0, 0), -0.5, NECK_L + 0.01)
    head = _prism(_stadium(R, 0, 0), NECK_L, PEG_L) & _flare(NECK, NECK_L, PEG_L)
    return neck.fuse(head).clean()


def _latch_frame(xh: float, zh: float) -> tuple[float, float, float]:
    """The bump's entry centre and the tongue's free end and root, for a latch over the hole seated at (xh, zh)."""
    ze = zh + DROP
    free = ze + 1.0
    return ze, free, free + TONGUE_L


def latch_cut(xh: float, zh: float, catch: str = "latch") -> list[bd.Shape]:
    """What the latch takes out of the plate: the slot round its tongue, and the plate thinned over it."""
    t = TONGUE_T[catch]
    _, free, root = _latch_frame(xh, zh)
    h, g = TONGUE_W / 2, TONGUE_GAP
    v = free - g / math.cos(POINT)                       # the slot's V end, parallel to the tongue's
    k = (h + g) * STEEP
    slot = [(xh - h - g, root), (xh - h - g, v + k), (xh, v), (xh + h + g, v + k), (xh + h + g, root)]
    cut = _prism(bd.Face(bd.Wire.make_polygon([bd.Vector(x, z) for x, z in slot], close=True)), -PLATE_T - 1, 1)
    # Over the tongue the plate's front is cut back at POINT to its thickness, so the step at the
    # root prints without support either way up.
    d = (PLATE_T + 1 - t) * STEEP
    wedge = _profile_yz([(-t, root - 0.01), (-PLATE_T - 1, root - 0.01), (-PLATE_T - 1, root + d)], xh - h, xh + h)
    return [cut, wedge]


def latch_parts(xh: float, zh: float, catch: str = "latch") -> list[bd.Shape]:
    """The tongue, its bump (in the entry when seated) and its pull, for a latch over the hole seated at (xh, zh)."""
    t = TONGUE_T[catch]
    ze, free, root = _latch_frame(xh, zh)
    h = TONGUE_W / 2
    k = h * STEEP
    pts = [(xh - h, root + 0.5), (xh - h, free + k), (xh, free), (xh + h, free + k), (xh + h, root + 0.5)]
    tongue = _prism(bd.Face(bd.Wire.make_polygon([bd.Vector(x, z) for x, z in pts], close=True)), -t, 0.01)
    # The bump: the top of the entry's own shape, BUMP_CLEAR inside it, its underside ramped at
    # POINT (no overhang); "click" ramps its top at 45 degrees too, so a firm lift cams the tongue out.
    a = R + CLEAR - BUMP_CLEAR
    apex = ze + a / math.cos(POINT)
    body = _prism(_stadium(a, ze, ze), -0.01, BUMP_H).moved(bd.Location((xh, 0, 0))) & tp._box(xh - a, xh + a, -1, BUMP_H + 1, ze + BUMP_UP, apex + 1)
    big = BUMP_H + 2
    body = body - _profile_yz([(-0.01, ze + BUMP_UP), (big, ze + BUMP_UP), (big, ze + BUMP_UP + big * STEEP + 0.01)], xh - a - 1, xh + a + 1)
    if catch == "click":
        body = body - _profile_yz([(-0.01, apex + 1), (-0.01, apex - 0.01), (big, apex - big - 0.01), (big, apex + 1)],
                                  xh - a - 1, xh + a + 1)
    z0 = free + k
    tab = _profile_yz([(-t + 0.01, z0), (-t + 0.01, z0 + 2 * TAB * STEEP), (-t - TAB, z0 + TAB * STEEP)], xh - h, xh + h)
    return [tongue, body, tab]


def with_latch(body: bd.Shape, xh: float, zh: float, catch: str = "latch") -> bd.Shape:
    return (body - latch_cut(xh, zh, catch)) + latch_parts(xh, zh, catch)


# --- the grid on the case ----------------------------------------------------------

def _clear_of_everything(face: str, a: float, b: float) -> bool:
    """Whether a hole seated at (a, b) on a side or the back keeps clear of the seam, the handle and the inlet."""
    z0, z1 = b - HOLE_BELOW, b + HOLE_ABOVE
    if z0 < tp.Z_SPLIT + SEAM_ROOM and z1 > tp.Z_SPLIT - SEAM_ROOM:
        return False
    if face in ("right", "left"):
        y0, y1, hz = HANDLE_ZONE
        return not (a + HOLE_HALF > y0 and a - HOLE_HALF < y1 and z1 > hz)
    x0, x1, iz0, iz1 = IEC_ZONE
    return not (a + HOLE_HALF > x0 and a - HOLE_HALF < x1 and z1 > iz0 and z0 < iz1)


def seats(face: str, half: str | None = None) -> list[bd.Location]:
    """Every seat on a face (top: half picks the lid panel), as the frame its hole is cut in."""
    out = []
    for f, a, b in SPOTS.values():
        if f != face or (face == "top" and (b > 0) != (half == "back")):
            continue
        at = LID_SEATS if face == "top" else SPOT_SEATS
        out += [frame(f, a, b) * bd.Location((u, 0, v)) for u, v in at]
    return out


def holes(face: str, half: str | None = None) -> list[tuple[float, float]]:
    """The seats on a side or the back as (along, height) in world terms (y or x, z); on the lid (x, y)."""
    pts = [loc.position for loc in seats(face, half)]
    if face in ("right", "left"):
        return [(p.Y, p.Z) for p in pts]
    return [(p.X, p.Z) if face == "back" else (p.X, p.Y) for p in pts]


def to_lid(shape: bd.Shape) -> bd.Shape:
    """Turn a profile-frame shape for the lid: the drop runs along local +X (profile (x, z) -> local (-z, x))."""
    return shape.rotate(bd.Axis.Y, -90)


def grid_cuts(face: str, half: str | None = None, clear: float = CLEAR) -> list[bd.Shape]:
    """Every hole on a face (top: half picks the lid panel), placed."""
    tool = hole_tool(clear)
    if face == "top":
        tool = to_lid(tool)
    return [tool.moved(loc) for loc in seats(face, half)]


def place(face: str, a: float, b: float) -> bd.Location:
    """Where an attachment sits, seated: its plate on the wall (0.01 off it, so no faces coincide)."""
    return frame(face, a, b) * bd.Location((0, -0.01, 0))


# --- attachments (local frame; the models place or print them) ---------------------

def _plate(u0: float, u1: float, v0: float, v1: float) -> bd.Solid:
    return tp._box(u0, u1, -PLATE_T, 0, v0, v1)


def _pegs(*at: tuple[float, float]) -> list[bd.Shape]:
    p = peg()
    return [p.moved(bd.Location((x, 0, z))) for x, z in at]


def _open_box(w: float, d: float, h: float, v0: float, t: float = 2.0) -> bd.Shape:
    """Open-top box standing off the plate, w wide, d deep, h tall from v0."""
    outer = tp._box(-w / 2, w / 2, -PLATE_T - d, -PLATE_T + 0.01, v0, v0 + h)
    inner = tp._box(-w / 2 + t, w / 2 - t, -PLATE_T - d + t, -PLATE_T - 0.5, v0 + t, v0 + h + 1)
    return outer - inner


def _latch_top(zh: float) -> float:
    """How far up the plate must go for a latch over a peg seated at height zh."""
    return _latch_frame(0, zh)[2] + PLATE_T + 1.5


def bin_small() -> bd.Shape:
    """Open-top bin, 48 x 36 x 45 inside: brush, scoop, dosing cup. Two pegs 28 apart, the latch over the right one."""
    w, h, v0 = 52.0, 49.0, -45.0
    body = _plate(-w / 2, w / 2, v0, _latch_top(0)) + _open_box(w, 40.0, h, v0) + _pegs((-PITCH / 2, 0), (PITCH / 2, 0))
    return with_latch(body, PITCH / 2, 0)


def filter_holder() -> bd.Shape:
    """Upright sleeve for a stack of 155 mm flat filter papers, a scoop cut in front to grab one."""
    w, d, h, t = 166.0, 16.0, 116.0, 2.0
    v0 = -110.0
    sleeve = _open_box(w, d, h, v0, t) - tp._cyl(38.0, "y", (0, 0, v0 + h), -PLATE_T - d - 1, -PLATE_T - d + t + 1)
    body = _plate(-w / 2, w / 2, v0, _latch_top(0)) + sleeve + _pegs(*SPOT_SEATS)
    return with_latch(body, PITCH / 2, 0)


def dripper_ring(inner_d: float = 100.0) -> bd.Shape:
    """Ring that hangs the dripper by its rim, on a gusset. inner_d is a guess: measure the dripper.

    Its ring sits above the latch's tongue, which keeps clear of where the ring meets the plate.
    """
    ring_h, ring_t = 10.0, 3.0
    r = inner_d / 2
    cy = -PLATE_T - ring_t - r + 1.5      # sunk 1.5 into the plate: tangent, it met the plate on a line only
    top = _latch_top(0) + ring_h          # the ring's underside just over the tongue's root
    ring = tp._cyl(r + ring_t, "z", (0, cy, 0), top - ring_h, top) - tp._cyl(r, "z", (0, cy, 0), top - ring_h - 1, top + 1)
    plate = _plate(-30.0, 30.0, -14.0, top)
    gusset = tp._prism_yz([(-PLATE_T, top - ring_h), (-PLATE_T - 30.0, top - ring_h), (-PLATE_T, -14.0)], -3.0, 3.0)
    body = plate + ring + gusset + _pegs(*SPOT_SEATS)
    return with_latch(body, PITCH / 2, 0)


def cord_wrap() -> bd.Shape:
    """Two horns to coil the power cord on the back: over the top one, under the bottom one.

    Each horn's underside slopes at 50 degrees, so it prints upright with no support, and the
    loops under the bottom horn slide in to the plate.
    """
    hw, reach = 20.0, 26.0
    out, fall = -PLATE_T - reach, (reach + 0.01) * STEEP
    upper = tp._prism_yz([(-PLATE_T + 0.01, -6.0), (out, -6.0), (out, -10.0), (-PLATE_T + 0.01, -10.0 - fall)], -hw, hw)
    lip = tp._box(-hw, hw, out, out + 4.0, -6.01, 0.0)
    lower = tp._prism_yz([(-PLATE_T + 0.01, -48.0), (out, -48.0), (out, -52.0), (-PLATE_T + 0.01, -52.0 - fall)], -hw, hw)
    body = _plate(-24.0, 24.0, -54.0 - fall, _latch_top(0)) + [upper, lip, lower] + _pegs((-PITCH / 2, 0), (PITCH / 2, 0))
    return with_latch(body, PITCH / 2, 0)


def top_tray() -> bd.Shape:
    """Shallow tray for spare xPods or recipe cards on the back lid panel.

    Two pegs 28 apart on one row; it slides 9 along the lid to seat. The latch is on a flange
    off the tray's front edge, its bump in a hole of the next row, so its pull is outside the tray.
    """
    w, d, h, t = 108.0, 52.0, 16.0, 2.0
    v0 = -40.0
    outer = tp._box(-w / 2, w / 2, -PLATE_T - h, -PLATE_T + 0.01, v0, v0 + d)
    inner = tp._box(-w / 2 + t, w / 2 - t, -PLATE_T - h - 1, -PLATE_T - 0.5, v0 + t, v0 + d - t)
    # The flange: profile (x, z) = local (v, -u); the latch's hole is seated at u = 14 on the row v = 28.
    flange = _plate(-24.0, 8.0, v0 + d - 0.01, 2 * PITCH - 20.0)
    body = _plate(-w / 2, w / 2, v0, v0 + d) + (outer - inner) + flange
    pegs = [to_lid(p) for p in _pegs((0, PITCH / 2), (0, -PITCH / 2))]
    body = body + pegs
    body = body - [to_lid(c) for c in latch_cut(PITCH, -PITCH / 2)]
    return body + [to_lid(p) for p in latch_parts(PITCH, -PITCH / 2)]


# How each attachment turns from its local frame (z up, as it hangs) to print without support:
# upright for the open boxes and the cord wrap, upside down for the ring (its top on the bed),
# on its side for the lid tray. Each keeps its pegs lying along the bed.
PRINT_ROT = {
    "travel_acc_bin": (0, 0, 0),
    "travel_acc_filter_holder": (0, 0, 0),
    "travel_acc_dripper_ring": (180, 0, 0),
    "travel_acc_cord_wrap": (0, 0, 0),
    "travel_acc_top_tray": (0, 90, 0),
}

# Which attachment goes where (checks/check_mount.py tries each on each: no collision, doors
# swinging clear, on its face's flat and off the power inlet). The tray is the lid's.
FITS = {
    "travel_acc_bin": "any of the 8 wall spots",
    "travel_acc_filter_holder": "the 3 upper spots (166 wide: lower down it would reach the doors or the corners)",
    "travel_acc_dripper_ring": "7 wall spots, all but the back's lower one (it would reach past the corner)",
    "travel_acc_cord_wrap": "any of the 8 wall spots; the back's lower one is beside the inlet",
    "travel_acc_top_tray": "the lid",
}
# The samples in the assembly, spot by spot (the others are left free).
SAMPLE_SPOTS = (
    ("travel_acc_dripper_ring", "right upper"),
    ("travel_acc_bin", "right lower back"),
    ("travel_acc_filter_holder", "left upper"),
    ("travel_acc_bin", "left lower front"),
    ("travel_acc_cord_wrap", "back lower"),
    ("travel_acc_top_tray", "lid"),
)
SAMPLES = tuple((name, *SPOTS[spot]) for name, spot in SAMPLE_SPOTS)

# Each attachment's pegs, seated, in its local frame (for the checks and drawings)
PEGS = {name: SPOT_SEATS for name in FITS}               # the tray's are local (u, v) on the lid
