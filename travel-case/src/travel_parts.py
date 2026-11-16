"""Geometry for the xBloom Studio brew-in-the-box travel case (helper, not a model).

Fully 3D printed, and only as deep as the machine needs. The machine travels
standing up on the floor of the case, held by a low rim round its base. Two
pairs of doors open from the middle, an upper pair and a lower pair; the
lower pair's bins sit inside the machine's own brewing recess when shut, so
the accessories travel in space the machine leaves empty. Two lid panels slide
out, forward and back, under an arched carry handle: slide the back one to
lift the tank out, the front one to reach the top of the machine. Power comes
in through a panel-mount IEC inlet in the back wall.

The left door of each pair laps over the right one at a 45 degree meeting edge,
so the left one opens first. That order is what lets the lower right door
carry a deep bin: it only swings once the left door is folded fully open
(180 degrees, flat out to the side), while the left door's own bin stays small
enough to pass the right door.

Held shut for travel with nothing showing outside: magnets buried in the upper
doors' top edges hold them to the front lid panel (which they hold in turn);
magnets in the horizontal edges where the doors meet hold each lower door to the
one above; magnets low on the lower doors' backs hold them to the sill along
the front of the floor. The lower doors, which carry the weight of the bins,
also stand on a plinth (the floor carried forward under them), and a spring
ball plunger in each one's bottom edge clicks into a hole in the plinth.

Every piece fits a 256 mm cube. The shell is cut once, at Z_SPLIT; bands on the
inside faces there carry M3 heat-set inserts on one side and screw holes on the
other, so nothing shows outside but the seam. The back corners are rounded.

Machine figures from the owner's drawings (mm), measured from the front tip of
its buttons: 166.6 wide (base 170), 423 tall (426 published, used here), 204 deep, 5.1 kg. The buttons stand 15.4
proud of the head. Below the head and the left column the front is open: full
width, 110 deep, from the tray (28 above the base) to 174.5 above the tray, and
on the right under the head up to 232 above the tray, where the dripper hangs.
The tank is 82.6 wide on the machine's left, its bottom 327.8 below the top; the
IEC C14 inlet is centred 43 above the base, 32.7 in from the right edge seen
from the front, in a surround 2.8 proud of the back.

Datum: case centred on the origin, +Z up, front facing -Y. Parts are built in
place; the models that export them turn them to their print orientation.
"""

from __future__ import annotations

import json
from pathlib import Path

from cadgen import build123d as bd

# --- colours: "cafe creme", for the Moonlight (white) Studio -----------------------
COLOURS = {
    "shell": "#EDE6DA",      # warm off-white
    "door": "#C8A47E",       # light oak
    "accent": "#3B2F2A",     # espresso: handle, attachments
}

# --- the machine (y measured back from the front tip of the buttons) -------------
M_BASE_W = 170.0
M_BODY_W = 166.6
M_DEPTH = 204.0
M_HEIGHT = 426.0             # xBloom's published height; the owner's model measures 423, so 3 more for safety
M_WEIGHT = 5.1               # kg, published net weight
M_TRAY_Z = 28.0              # tray surface above the base
M_BUTTON_PROUD = 15.4        # buttons stand this far in front of the head and column
M_BUTTON_D = 16.0
M_BUTTON_Z = M_TRAY_Z + 247.0
M_BUTTON_X = (16.0, 42.0, 68.0)
M_RECESS_DEPTH = 110.0       # from the button tips to the back of the recess
M_RECESS_TOP = M_TRAY_Z + 174.5            # full-width part, under the left column
M_RECESS_RIGHT_TOP = M_TRAY_Z + 232.0      # right half, under the head
M_DRIPPER_X = 42.0
M_TANK_W = 82.6
M_TANK_DROP = 327.8          # top of machine to bottom of tank
M_TANK_DEPTH = 50.0          # not measured: 946 ml over ~300 mm of a 82.6 wide tank is ~40 inside, ~50 outside
M_SOCKET_Z = 43.0            # above the machine's base
M_SOCKET_X = M_BODY_W / 2 - 32.7

# --- the shell ---------------------------------------------------------------
WALL = 6.0
SIDE_CLR = 9.0               # each side of the machine: room for the joint bands
FRONT_CLR = 5.0              # door inside face to the button tips
REAR_BAY = 30.0              # a right-angle C13 plug behind the machine
IN_W = M_BASE_W + 2 * SIDE_CLR                  # 188
W = IN_W + 2 * WALL                             # 200
D = FRONT_CLR + M_DEPTH + REAR_BAY + WALL       # 245: open front to back face
BACK_R = 10.0                # outside back corners
BACK_R_IN = BACK_R - WALL    # inside, so the wall keeps its thickness round the corner
FLOOR = 6.0
DECK_Z = FLOOR                                  # machine stands on the floor
RIM_H = 10.0                                    # locating rim round the machine's base
RIM_T = 4.5
LID_Z0 = DECK_Z + M_HEIGHT + 2.0                # underside of the lid panels
LID_T = 6.0
LID_RISE = 0.6               # over the lid panels, under the lip; 0.5 in Rev E, which sat between 0.2 mm
                             # layers (so it could print 0.4) under a 5 mm overhang that droops a little
LIP_Z0 = LID_Z0 + LID_T + LID_RISE
H = LID_Z0 + LID_T + 3.5                        # top of the side walls (the lip is 2.9 thick)
RAIL_W = 7.0                                    # lid rail, wide enough for a magnet

M_FRONT_Y = -D / 2 + FRONT_CLR                  # button tips
M_BACK_Y = M_FRONT_Y + M_DEPTH

# --- the one joint -------------------------------------------------------------
Z_SPLIT = 220.0
BAND = 8.0
BAND_A = 6.0                 # screw side
BAND_B = 8.0                 # insert side
CLEAR_D = 3.4
INSERT_D = 4.0               # M3 heat-set insert pilot: the owner's G gauge picked 4.0 (28 Oct)
INSERT_DEPTH = 6.5
INSERT_LEAD = 0.5            # 45 degree lead-in at every M3 pilot's mouth, so the insert starts centred
INSERT_WALL = 3.0            # plastic round every M3 pilot below its lead-in, and past its end (Rev E's joint band: 2.0, 1.5)
HEAD_D = 6.5
Z_JOINT_Y = (-90.0, -30.0, 30.0, 90.0)
Z_JOINT_BACK_X = (-70.0, 0.0, 70.0)

# --- magnets: 6 x 2 mm discs everywhere --------------------------------------------
MAG_D = 5.8                  # the owner's G gauge, 28 Oct, and the studio's pocket since (Rev E 6.2, then 6.0)
MAG_DEPTH = 2.2
EDGE_MAG_D = MAG_D           # in the doors' edges, where DOOR_T leaves 1.9 mm each side
EDGE_MAG_DEPTH = MAG_DEPTH
EDGE_MAG_X = 50.0            # either side of the middle, one per door

# --- doors: a pair per tier, hinged at the sides, meeting in the middle ------------
DOOR_T = 10.0               # thick enough to bury a 6 mm magnet in its edge
HINGE_R = 5.0                # flush with both door faces; 3.35 mm of plastic round the pin
HINGE_Y = -D / 2 - DOOR_T / 2                   # hinge axes run inside the doors' thickness
HINGE_LEN = 60.0
KNUCKLE_MID = 30.0           # the door's own knuckle gets half: it prints lying down, across its layers
HINGE_PIN_D = 3.3            # in the shell's knuckles, for the hinge rod
# One M3 threaded rod per side is the hinge pin for both doors on that side: they share one
# axis. It drops in from the top (front lid off) through every knuckle and a channel along
# the doors' hinge edges, and screws into a printed hole in the lowest knuckle, standing on
# that knuckle's closed floor. A bolt per hinge can't work: the door panel runs on past each
# hinge, so there's no way in and no room for a head or a nut. Rev E had an insert there,
# which the iron couldn't reach straight under the knuckle. The rod has to be held, not just
# stood in: the lid doesn't trap it, since its axis is on the case's side face, under the
# lid's rounded front corner (the lid covers 5 % of its end), so a loose rod could slide out
# of the top with the case on its side and drop the doors.
ROD_CLEAR_D = 3.5            # the channel in the doors, which turn on the rod
HINGE_FLOOR = 2.0            # the lowest knuckle's printed floor, under the rod's end
ROD_TAP_D = 2.5              # the threaded rod cuts its own thread in this printed hole
ROD_TAP_DEPTH = 6.0
KNUCKLE_GAP = 0.5
DOOR_Z = {"lower": (FLOOR + 0.5, Z_SPLIT - 0.25), "upper": (Z_SPLIT + 0.25, LID_Z0)}   # lower doors stand on the plinth
MEET_GAP = 0.5               # across the 45 degree meeting edge
PULL_R = 14.0
# Bins on the lower pair, inside the machine's recess when shut. The left door opens first,
# so its bin keeps inside FIRST_BIN_R of its hinge (clear of the right door, which starts past
# 100) and the right door's bin keeps outside that circle and inside SECOND_BIN_R of its own.
BIN_X = (-(IN_W / 2 - BAND - 1.0), IN_W / 2 - BAND - 1.0)   # clear of the joint bands
BIN_Z = (DECK_Z + M_TRAY_Z + 2.0, Z_SPLIT - 20.0)
BIN_REACH = FRONT_CLR + M_RECESS_DEPTH - 3.0    # out from the doors' inside face
FIRST_BIN_R = 98.0
BIN_SPLIT_GAP = 3.0
SECOND_BIN_R = 191.0         # the right bin, swinging after the left door, stays clear of the left wall
BIN_WALL = 2.0
BIN_LIP = 35.0
# The storage is two separate trays per lower door, screwed to its back face, so the door and
# every tray print without support (a one-piece door and bin can't: some wall always overhangs).
TRAY_PLATE = 3.0             # the tray's door-side wall, which takes the screws
TRAY_GAP = 0.5               # between a door's lower and upper tray
TRAY_SCREW_X = (25.0, 65.0)  # from the middle, clear of the pull, the catch and the magnets
# Hidden catch on each lower door: a spring ball plunger screwed up into the door's bottom
# edge (M5 heat-set insert) drops into a small hole in the plinth's top. The door's bottom
# edge slides across the plinth as it swings, so the ball is cammed out of its hole rather
# than pulled straight off it, which is what makes it hold.
CATCH_X = 40.0               # either side of the middle: 60 from the hinge, for leverage
CATCH_INSERT_D = 6.6         # M5 heat-set insert pilot: the owner's G gauge picked 6.6 (28 Oct; Rev E 6.4)
CATCH_INSERT_DEPTH = 8.0     # the 8 mm-long M5 insert (7 mm knurl) of the assortment, flush with the edge
# The plunger screws in until its back end meets the hole's flat end: that sets the ball's
# height, with nothing to adjust (its hex drive is at the bottom of a blind hole). The owner's
# test-kit piece E (5 Nov 2026): a plunger stopped with the ball 1.92 mm proud clicked about
# right over the 2.5 seat, and E1 and E2 sat flat with it, so the ball retracts that far.
CATCH_PLUNGER_L = 12.14      # the M5 x 12 plunger, hex end to the ball's tip, ball free (owner's calliper)
CATCH_BALL_PROUD = 1.92      # below the door's bottom edge, the plunger home
CATCH_BORE_D = 5.3           # the plunger's thread runs on past the insert, free
CATCH_BORE_DEPTH = CATCH_PLUNGER_L - CATCH_BALL_PROUD   # 10.22: the hole's end is the stop
CATCH_RELIEF_D = 6.2         # just past the insert: room for the plastic it pushes ahead of it
CATCH_RELIEF_L = 1.0         # so that ridge can't stop the plunger short (it did on E2)
CATCH_SEAT_D = 2.5           # smaller than the ball, so it seats on the hole's edge
CATCH_SEAT_DEPTH = 1.5
# The owner's KABOOM logo, debossed into the upper right door's front face near the top,
# clear of the meeting edge, the hinge knuckles' grooves and the top edge's magnet.
# The outlines are the studio's brand/kaboom_logo.json, traced by studio/logo_trace.py.
STUDIO = Path(__file__).resolve().parents[3]          # projects/<project>/src/ -> the studio
LOGO_FILE = STUDIO / "brand" / "kaboom_logo.json"
LOGO_W = 74.0
LOGO_DEPTH = 0.6
LOGO_CX = 53.0               # the door's front face runs from x 10.25 to 100
LOGO_TOP = LID_Z0 - 20.0
SOCIAL = "@kaboom.ae"        # the owner's Instagram, centred under the wordmark
SOCIAL_SIZE = 5.5            # bold Arial: about 34 x 5 mm, strokes near 0.8 mm
SOCIAL_GAP = 3.5             # below the logo

# --- lid, handle, inlet --------------------------------------------------------
LID_GAP = 1.0
LID_FRONT_R = 10.0
HANDLE_SAG = 48.0            # keeps a 40+ mm gap for the hand over the lid with the thicker bar
HANDLE_BAR = 18.0            # bar thickness, the same through the legs and the arch
HANDLE_DEPTH = 28.0          # grip width, front to back: about twice the bending strength of 14 x 24
HANDLE_LEG = 80.0
HANDLE_EDGE_R = 6.0          # rounds every edge of the bar's section
HANDLE_KNEE_R = 15.0         # where the legs turn into the arch, on the bar's centre line
HANDLE_SCREW_Z = (H - 66.0, H - 30.0)   # 36 apart, so the leg's bending pulls less on each insert
HANDLE_SCREW_Y = (-4.0, 4.0)        # on the flat of the legs: 2.0 to the edge rounding at the mouth (Rev E's 5.5 left 0.5)
IEC_CUT = (28.0, 20.0)       # panel-mount IEC C14 inlet; check against the one bought
IEC_SCREW_PITCH = 40.0
IEC_X = M_SOCKET_X
IEC_Z = DECK_Z + M_SOCKET_Z + 60.0


# --- helpers -----------------------------------------------------------------

def _box(x0, x1, y0, y1, z0, z1) -> bd.Solid:
    return bd.Box(x1 - x0, y1 - y0, z1 - z0, align=(bd.Align.MIN, bd.Align.MIN, bd.Align.MIN)).moved(
        bd.Location((x0, y0, z0))
    )


def _place(shape: bd.Shape, x0=None, y0=None, z0=None) -> bd.Shape:
    bb = shape.bounding_box()
    return shape.moved(bd.Location((
        0 if x0 is None else x0 - bb.min.X,
        0 if y0 is None else y0 - bb.min.Y,
        0 if z0 is None else z0 - bb.min.Z,
    )))


def _prism_xz(pts: list[tuple[float, float]], y0: float, y1: float) -> bd.Shape:
    """A profile given as (x, z) points, run along Y from y0 to y1."""
    face = bd.Polygon(*pts, align=None)
    solid = bd.extrude(face, amount=y1 - y0).rotate(bd.Axis.X, 90)
    bb = face.bounding_box()
    return _place(solid, x0=bb.min.X, y0=y0, z0=bb.min.Y)


def _prism_yz(pts: list[tuple[float, float]], x0: float, x1: float) -> bd.Shape:
    """A profile given as (y, z) points, run along X from x0 to x1."""
    face = bd.Polygon(*pts, align=None)
    solid = bd.extrude(face, amount=x1 - x0).rotate(bd.Axis.X, 90).rotate(bd.Axis.Z, 90)
    bb = face.bounding_box()
    return _place(solid, x0=x0, y0=bb.min.X, z0=bb.min.Y)


def _prism_xy(pts: list[tuple[float, float]], z0: float, z1: float) -> bd.Shape:
    """A plan profile given as (x, y) points, run up Z from z0 to z1 (either winding)."""
    area = sum(x0 * y1 - x1 * y0 for (x0, y0), (x1, y1) in zip(pts, pts[1:] + pts[:1]))
    if area < 0:
        pts = pts[::-1]
    return bd.extrude(bd.Polygon(*pts, align=None), amount=z1 - z0).moved(bd.Location((0, 0, z0)))


def _cyl(r: float, axis: str, c: tuple[float, float, float], a0: float, a1: float) -> bd.Solid:
    """Cylinder along axis 'x', 'y' or 'z', its centre line through c, running a0..a1 along the axis."""
    rot = {"x": (0, 90, 0), "y": (-90, 0, 0), "z": (0, 0, 0)}[axis]
    cyl = bd.Cylinder(r, a1 - a0, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN), rotation=rot)
    pos = list(c)
    pos["xyz".index(axis)] = a0
    return cyl.moved(bd.Location(tuple(pos)))


def _lead_in(mouth: tuple[float, float, float], into: tuple[float, float, float]) -> bd.Solid:
    """The 45 degree lead-in at an M3 pilot's mouth, INSERT_LEAD deep, carried 1 mm out of the face."""
    r = INSERT_D / 2
    cone = bd.Cone(r + INSERT_LEAD + 1.0, r, INSERT_LEAD + 1.0, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))
    d = bd.Vector(*into)
    return cone.moved(bd.Plane(origin=bd.Vector(*mouth) - d, z_dir=d).location)


def _m3_pilot(mouth: tuple[float, float, float], into: tuple[float, float, float]) -> list[bd.Solid]:
    """An M3 heat-set insert's pilot from its mouth on a face, running `into` the part, with its lead-in."""
    d = bd.Vector(*into)
    pilot = bd.Cylinder(INSERT_D / 2, INSERT_DEPTH + 1.0, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))
    return [pilot.moved(bd.Plane(origin=bd.Vector(*mouth) - d, z_dir=d).location), _lead_in(mouth, into)]


def _plan_rounded_back(x0: float, x1: float, y0: float, y1: float, r: float, z0: float, z1: float) -> bd.Shape:
    """A block whose two back (+Y) vertical edges are rounded to radius r."""
    face = bd.Rectangle(x1 - x0, y1 - y0, align=(bd.Align.MIN, bd.Align.MIN)).moved(bd.Location((x0, y0)))
    face = bd.fillet(face.vertices().group_by(bd.Axis.Y)[-1], radius=r)
    return bd.extrude(face, amount=z1 - z0).moved(bd.Location((0, 0, z0)))


def _side_ledge(s: int, z_top: float, depth: float, thick: float, y0: float, y1: float) -> bd.Shape:
    """A ledge on side s's inside face with a 45 degree chamfer under it, so it prints without support."""
    wx = s * IN_W / 2
    ix = s * (IN_W / 2 - depth)
    return _prism_xz([(wx, z_top), (ix, z_top), (ix, z_top - thick), (wx, z_top - thick - depth)], y0, y1)


def _back_ledge(z_top: float, depth: float, thick: float) -> bd.Shape:
    wy = D / 2 - WALL
    iy = wy - depth
    return _prism_yz([(wy, z_top), (iy, z_top), (iy, z_top - thick), (wy, z_top - thick - depth)], -IN_W / 2, IN_W / 2)


def _knuckle_spans(zc: float, middle: bool) -> list[tuple[float, float]]:
    half = KNUCKLE_MID / 2
    if middle:
        return [(zc - half + KNUCKLE_GAP, zc + half - KNUCKLE_GAP)]
    return [(zc - HINGE_LEN / 2, zc - half - KNUCKLE_GAP), (zc + half + KNUCKLE_GAP, zc + HINGE_LEN / 2)]


def hinge_axis(s: int) -> tuple[float, float]:
    """Hinge axis (x, y) for the right (+1) or left (-1) door of a pair."""
    return s * W / 2, HINGE_Y


def hinge_centres(tier: str) -> tuple[float, float]:
    z0, z1 = DOOR_Z[tier]
    return z0 + 46.0, z1 - 40.0


def rod_span() -> tuple[float, float]:
    """Bottom and top of a side's hinge rod: from the lowest knuckle's floor to 1 mm under the doors' top edge."""
    bottom = hinge_centres("lower")[0] - HINGE_LEN / 2          # the lowest knuckle's bottom face
    return bottom + HINGE_FLOOR, LID_Z0 - 1.0


def _rod_cuts(s: int) -> list[bd.Solid]:
    """What the hinge rod takes out of the shell: its hole up every knuckle, and the hole it screws into.

    The lowest knuckle keeps a closed floor; above it the 2.5 mm hole the rod threads itself
    into, then a 45 degree cone up to the 3.3 bore that steers the rod's end into it. The
    shell prints upright, so all of it is a plain vertical hole over a solid floor.
    """
    ax, ay = hinge_axis(s)
    f = hinge_centres("lower")[0] - HINGE_LEN / 2 + HINGE_FLOOR
    t = f + ROD_TAP_DEPTH
    flare = (HINGE_PIN_D - ROD_TAP_D) / 2
    cone = bd.Cone(ROD_TAP_D / 2, HINGE_PIN_D / 2, flare, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))
    return [_cyl(HINGE_PIN_D / 2, "z", (ax, ay, 0), t, LID_Z0 + 1),
            cone.moved(bd.Location((ax, ay, t - flare))),
            _cyl(ROD_TAP_D / 2, "z", (ax, ay, 0), f, t)]


def _body_knuckles(s: int, tier: str) -> list[bd.Shape]:
    ax, ay = hinge_axis(s)
    out = []
    for zc in hinge_centres(tier):
        for z0, z1 in _knuckle_spans(zc, middle=False):
            out.append(_cyl(HINGE_R, "z", (ax, ay, 0), z0, z1))
            x0, x1 = sorted((ax, ax - s * WALL))
            out.append(_box(x0, x1, ay, -D / 2 + 0.01, z0, z1))                     # web to the wall's front edge
    return out


def _edge_pocket(s: int, z: float, up: bool) -> bd.Solid:
    """A magnet pocket at height z, mid-thickness of the doors: up=True runs up from z, else down."""
    x, y = s * EDGE_MAG_X, -D / 2 - DOOR_T / 2
    return _cyl(EDGE_MAG_D / 2, "z", (x, y, 0), *((z, z + EDGE_MAG_DEPTH) if up else (z - EDGE_MAG_DEPTH, z)))


def _sill_magnet_z() -> float:
    """Height of the lower doors' magnets, in the face of the front sill above the plinth."""
    return FLOOR + RIM_H / 2


def _lid_magnet_y(half: str) -> float:
    return -70.0 if half == "front" else 70.0


# --- the shell ---------------------------------------------------------------

def _outline(z0: float = -1.0, z1: float = 1000.0) -> bd.Shape:
    return _plan_rounded_back(-W / 2, W / 2, -D / 2 - 50, D / 2, BACK_R, z0, z1)


def _shell() -> bd.Shape:
    """The whole printed shell before it is cut: sides, back, floor, ledges, lid rails, joint bands."""
    outer = _plan_rounded_back(-W / 2, W / 2, -D / 2, D / 2, BACK_R, 0, H)
    inner = _plan_rounded_back(-IN_W / 2, IN_W / 2, -D / 2 - 1, D / 2 - WALL, BACK_R_IN, FLOOR, H + 1)
    body = outer - inner
    # The back wall stops under the lid so the back lid panel slides out over it, and the
    # inside corner rounding goes too at that height, so the panel's corners pass.
    body = body - _box(-IN_W / 2, IN_W / 2, D / 2 - WALL - BACK_R_IN - 1, D / 2 + 1, LID_Z0, H + 1)
    adds = []
    for s in (1, -1):
        adds.append(_side_ledge(s, LID_Z0, RAIL_W, 4.0, -D / 2, D / 2))                # lid rail
        x0, x1 = sorted((s * IN_W / 2, s * (IN_W / 2 - 5.0)))
        adds.append(_box(x0, x1, -D / 2, D / 2, LIP_Z0, H))                            # lid lip
        adds.append(_side_ledge(s, Z_SPLIT + BAND_B, BAND, BAND_A + BAND_B, -D / 2, D / 2 - WALL))  # joint band
    # Rim round the machine's base, its front run carried across the full width as a sill
    rim_out = _box(-M_BASE_W / 2 - 0.5 - RIM_T, M_BASE_W / 2 + 0.5 + RIM_T, M_FRONT_Y - 0.5 - RIM_T + 0.01, M_BACK_Y + 0.5 + RIM_T,
                   FLOOR - 0.01, FLOOR + RIM_H)
    rim_in = _box(-M_BASE_W / 2 - 0.5, M_BASE_W / 2 + 0.5, M_FRONT_Y - 0.5, M_BACK_Y + 0.5, FLOOR - 1, FLOOR + RIM_H + 1)
    adds.append(rim_out - rim_in)
    adds.append(_box(-IN_W / 2, IN_W / 2, -D / 2, M_FRONT_Y - 0.5, FLOOR - 0.01, FLOOR + RIM_H))
    adds.append(_back_ledge(Z_SPLIT + BAND_B, BAND, BAND_A + BAND_B))
    adds += [_joint_boss(x, y) for x, y in joint_xy()]
    adds.append(_plinth())
    body = (body + adds) & _outline()

    holes = [_cyl(MAG_D / 2, "y", (s * EDGE_MAG_X, 0, _sill_magnet_z()), -D / 2 - 1, -D / 2 + MAG_DEPTH) for s in (1, -1)]
    holes += [_cyl(CATCH_SEAT_D / 2, "z", (s * CATCH_X, HINGE_Y, 0), FLOOR - CATCH_SEAT_DEPTH, FLOOR + 1) for s in (1, -1)]
    for x, y in joint_xy():
        holes += _joint_hole(x, y)
    holes.append(_box(IEC_X - IEC_CUT[0] / 2, IEC_X + IEC_CUT[0] / 2, D / 2 - WALL - 1, D / 2 + 1,
                      IEC_Z - IEC_CUT[1] / 2, IEC_Z + IEC_CUT[1] / 2))
    for dx in (-IEC_SCREW_PITCH / 2, IEC_SCREW_PITCH / 2):
        holes.append(_cyl(CLEAR_D / 2, "y", (IEC_X + dx, 0, IEC_Z), D / 2 - WALL - 1, D / 2 + 1))
    for s in (1, -1):
        for y in HANDLE_SCREW_Y:
            for z in HANDLE_SCREW_Z:
                holes.append(_cyl(CLEAR_D / 2, "x", (0, y, z), *sorted((s * (IN_W / 2 - 1), s * (W / 2 + 1)))))
    for half in ("front", "back"):
        for s in (1, -1):
            holes.append(_cyl(MAG_D / 2, "z", (s * (IN_W / 2 - RAIL_W / 2), _lid_magnet_y(half), 0), LID_Z0 - MAG_DEPTH, LID_Z0 + 1))
    import travel_mount as tm                                    # the outside mounting grid
    for face in ("right", "left", "back"):
        holes += tm.grid_cuts(face)
    return body - holes


def _plinth() -> bd.Shape:
    """The floor carried forward under the lower doors, as deep as they are thick.

    It echoes the front lid panel's overhang at the top: the same depth, the same
    rounded front corners. The doors stand on it, and their catches drop into it.
    A 1 mm chamfer on its top front edge lets the catch's ball ride up onto it.
    """
    y0, y1 = -D / 2 - DOOR_T, -D / 2 + 0.01
    plinth = _prism_yz([(y0, 0), (y1, 0), (y1, FLOOR), (y0 + 1.0, FLOOR), (y0, FLOOR - 1.0)], -W / 2, W / 2)
    return plinth - [_corner_cut(s, y0, -1, FLOOR + 1) for s in (1, -1)]


def joint_xy() -> list[tuple[float, float]]:
    """Plan positions of the 11 screws that join the shell halves: 4 down each side band, 3 across the back."""
    return ([(s * (IN_W / 2 - BAND / 2), y) for s in (1, -1) for y in Z_JOINT_Y]
            + [(x, D / 2 - WALL - BAND / 2) for x in Z_JOINT_BACK_X])


def _joint_boss(x: float, y: float) -> bd.Solid:
    """A round boss on the upper band round each joint insert: INSERT_WALL of plastic beside and over it.

    The band alone left 2.0 mm on its open side and 1.5 over the insert. The boss stands on the
    upper half's bed face, so it prints with no overhang; the joint faces are the band's as before.
    """
    return _cyl(INSERT_D / 2 + INSERT_WALL, "z", (x, y, 0), Z_SPLIT, Z_SPLIT + INSERT_DEPTH + INSERT_WALL)


def _joint_hole(x: float, y: float) -> list[bd.Solid]:
    """Vertical screw across the joint: head spot-faced under the band, insert above the cut."""
    return [
        _cyl(CLEAR_D / 2, "z", (x, y, 0), Z_SPLIT - 20, Z_SPLIT),
        _cyl(HEAD_D / 2, "z", (x, y, 0), Z_SPLIT - 30, Z_SPLIT - BAND_A),
        _cyl(INSERT_D / 2, "z", (x, y, 0), Z_SPLIT, Z_SPLIT + INSERT_DEPTH),
    ]


def shell_pieces() -> dict[str, bd.Shape]:
    """The shell cut into its two printed pieces, in place, each with its doors' hinge knuckles."""
    shell = _shell()
    big = 1000.0
    out = {}
    for name, tier, (z0, z1) in (("lower", "lower", (-1, Z_SPLIT)), ("upper", "upper", (Z_SPLIT, big))):
        piece = shell & _box(-big, big, -big, big, z0, z1)
        for s in (1, -1):
            piece = piece + _body_knuckles(s, tier) - _rod_cuts(s)
        if name == "upper":                                 # the inserts' lead-ins, on its bed face
            piece = piece - [_lead_in((x, y, Z_SPLIT), (0, 0, 1)) for x, y in joint_xy()]
        out[name] = piece
    return out


def _bin_region(s: int, shrink: float, z0: float, z1: float) -> bd.Shape:
    """The plan a lower door's storage may fill, from z0 to z1, shrunk by `shrink` (for walls).

    The left door's keeps within FIRST_BIN_R of its hinge; the right door's within SECOND_BIN_R
    of its own and clear of the left door's circle.
    """
    rx, ry = hinge_axis(1)
    lx, ly = hinge_axis(-1)
    if s < 0:
        return _cyl(FIRST_BIN_R - shrink, "z", (lx, ly, 0), z0, z1)
    return _cyl(SECOND_BIN_R - shrink, "z", (rx, ry, 0), z0, z1) - _cyl(FIRST_BIN_R + BIN_SPLIT_GAP + shrink, "z", (lx, ly, 0), z0 - 1, z1 + 1)


def _tray_z(level: int) -> tuple[float, float]:
    """Bottom and top of a lower door's lower (0) or upper (1) tray."""
    bz0, bz1 = BIN_Z
    mid = (bz0 + bz1) / 2
    return (bz0, mid - TRAY_GAP / 2) if level == 0 else (mid + TRAY_GAP / 2, bz1)


def _tray_screws(s: int, level: int) -> list[tuple[float, float]]:
    """(x, z) of the two screws that hold a tray to its door, at the tray plate's mid-height."""
    z0, z1 = _tray_z(level)
    return [(s * x, (z0 + z1) / 2) for x in TRAY_SCREW_X]


def tray(s: int, level: int) -> bd.Shape:
    """A storage tray for a lower door, in place: s=+1 right, -1 left; level 0 lower, 1 upper.

    An open-top tray with a low lip on the machine side and a 3 mm plate on the door side
    that screws to the door's back face. It prints standing on its floor with every wall
    vertical, so it needs no support; the two trays of a door stack with a 0.5 mm gap and
    together fill exactly the space the old one-piece bin did.
    """
    z0, z1 = _tray_z(level)
    y0, y1 = -D / 2, -D / 2 + BIN_REACH
    body = _box(BIN_X[0], BIN_X[1], y0, y1, z0, z1) & _bin_region(s, 0, z0 - 1, z1 + 1)
    inner = _bin_region(s, BIN_WALL, z0 - 1, z1 + 2)
    cav = _box(BIN_X[0] + BIN_WALL, BIN_X[1] - BIN_WALL, y0 + TRAY_PLATE, y1 - BIN_WALL, z0 + BIN_WALL, z1 + 1) & inner
    lip = _box(BIN_X[0] + BIN_WALL, BIN_X[1] - BIN_WALL, y1 - BIN_WALL - 1, y1 + 1, z0 + BIN_WALL + BIN_LIP, z1 + 1) & inner
    body = body - cav - lip
    lz0, lz1 = DOOR_Z["lower"]
    body = body - _cyl(PULL_R, "y", (DOOR_T / 2, 0, (lz0 + lz1) / 2), y0 - 1, y0 + 1)     # the door's pull, carried 1 mm in
    return body - [_cyl(CLEAR_D / 2, "y", (x, 0, z), y0 - 1, y0 + TRAY_PLATE + 1) for x, z in _tray_screws(s, level)]


def door(s: int, tier: str) -> bd.Shape:
    """A door, shut. s=+1 right, -1 left; tier "lower" (its trays screw on: see tray()) or "upper".

    The two meet on a 45 degree edge: the left one laps over the right, so it opens first.
    """
    z0, z1 = DOOR_Z[tier]
    ax, ay = hinge_axis(s)
    back, front = -D / 2, -D / 2 - DOOR_T
    g = MEET_GAP / 2
    if s < 0:
        plan = [(-W / 2, back), (-W / 2, front), (DOOR_T - g, front), (-g, back)]
    else:
        plan = [(W / 2, back), (W / 2, front), (DOOR_T + g, front), (g, back)]
    leaf = _prism_xy(plan, z0, z1)
    cuts, adds = [], []
    for zc in hinge_centres(tier):
        for k0, k1 in _knuckle_spans(zc, middle=False):
            x0, x1 = sorted((s * (W / 2 + 1), s * (W / 2 - WALL - 1.0)))
            cuts.append(_box(x0, x1, front - 1, back + 1, k0 - KNUCKLE_GAP, k1 + KNUCKLE_GAP))
            cuts.append(_cyl(HINGE_R + 0.5, "z", (ax, ay, 0), k0 - KNUCKLE_GAP, k1 + KNUCKLE_GAP))
        for k0, k1 in _knuckle_spans(zc, middle=True):
            adds.append(_cyl(HINGE_R, "z", (ax, ay, 0), k0, k1))
    body = (leaf + adds) - cuts
    body = body - _cyl(ROD_CLEAR_D / 2, "z", (ax, ay, 0), z0 - 1, z1 + 1)      # the rod's channel, edge to edge
    body = body - _cyl(PULL_R, "y", (DOOR_T / 2, 0, (z0 + z1) / 2), front - 1, back + 1)    # round pull, half in each
    # Hidden magnets: into the top and bottom edges, and low on the lower doors' backs.
    body = body - _edge_pocket(s, z1, up=False)                   # top edge
    if tier == "upper":
        body = body - _edge_pocket(s, z0, up=True)                # meets the lower door
        if s > 0:
            body = body - logo_cut()
    else:
        body = body - _cyl(MAG_D / 2, "y", (s * EDGE_MAG_X, 0, _sill_magnet_z()), back - MAG_DEPTH, back + 1)
        body = body - catch_bore(s)
        # M3 heat-set inserts for the two trays, into the back face; 3.5 mm stays in front of them.
        for level in (0, 1):
            for x, z in _tray_screws(s, level):
                body = body - _m3_pilot((x, back, z), (0, -1, 0))
    return body


def logo_cut() -> list[bd.Shape]:
    """The logo's regions as thin solids standing LOGO_DEPTH into the doors' front face, in place.

    The door prints face down, so the deboss forms in its first few layers on the bed.
    """
    data = json.loads(LOGO_FILE.read_text(encoding="utf-8"))
    x0, z0 = LOGO_CX - LOGO_W / 2, LOGO_TOP - data["aspect"] * LOGO_W
    front = -D / 2 - DOOR_T

    def solid(pts: list[list[float]], scale: float = LOGO_W, at: tuple[float, float] = (x0, z0)) -> bd.Shape:
        p = [(at[0] + u * scale, at[1] + v * scale) for u, v in pts]
        if sum(a[0] * b[1] - b[0] * a[1] for a, b in zip(p, p[1:] + p[:1])) < 0:
            p = p[::-1]
        # Drawn in XY as (x, z), turned up into XZ: the extrusion then runs back from the face.
        s = bd.extrude(bd.Polygon(*p, align=None), amount=LOGO_DEPTH + 0.5).rotate(bd.Axis.X, 90)
        return s.moved(bd.Location((0, front + LOGO_DEPTH, 0)))

    out = []
    for region in data["regions"]:
        s = solid(region["outer"])
        if region["holes"]:
            s = s - [solid(h) for h in region["holes"]]
        out.append(s)

    # The Instagram handle, centred under the wordmark (the regions right of the icon).
    words = [r for r in data["regions"] if min(u for u, _ in r["outer"]) > 0.15]
    u0 = min(u for r in words for u, _ in r["outer"])
    u1 = max(u for r in words for u, _ in r["outer"])
    # The letters' curves are sampled into short straight runs, like the traced logo, so the
    # drawings' edge-on views don't collapse them to nothing.
    text = bd.Text(SOCIAL, SOCIAL_SIZE, font="Arial", font_style=bd.FontStyle.BOLD)
    bb = text.bounding_box()
    at = (x0 + (u0 + u1) / 2 * LOGO_W - (bb.min.X + bb.max.X) / 2, z0 - SOCIAL_GAP - bb.max.Y)
    for face in text.faces():
        s = solid(_sampled(face.outer_wire()), 1.0, at)
        holes = face.inner_wires()
        if holes:
            s = s - [solid(_sampled(w), 1.0, at) for w in holes]
        out.append(s)
    return out


def _sampled(wire: bd.Wire, step: float = 0.15) -> list[list[float]]:
    """A planar wire's outline as (x, y) points about `step` apart, for _prism-style extrusion."""
    n = max(8, int(wire.length / step))
    return [[p.X, p.Y] for p in (wire.position_at(i / n) for i in range(n))]


def catch_bore(s: int) -> list[bd.Solid]:
    """The lower door's ball-plunger hole, up into its bottom edge: insert pilot, a short relief for
    the plastic the insert pushes ahead, then the thread's run-on to a flat end, where the plunger stops."""
    z0 = DOOR_Z["lower"][0]
    c = (s * CATCH_X, HINGE_Y, 0)
    return [_cyl(CATCH_INSERT_D / 2, "z", c, z0 - 1, z0 + CATCH_INSERT_DEPTH),
            _cyl(CATCH_RELIEF_D / 2, "z", c, z0, z0 + CATCH_INSERT_DEPTH + CATCH_RELIEF_L),
            _cyl(CATCH_BORE_D / 2, "z", c, z0, z0 + CATCH_BORE_DEPTH)]


def lid(half: str) -> bd.Shape:
    """Sliding lid panel, in place. The front one covers the doors' top edge, magnets over theirs."""
    x0, x1 = -IN_W / 2 + 0.5, IN_W / 2 - 0.5
    if half == "front":
        front = -D / 2 - DOOR_T
        panel = _box(x0, x1, -D / 2 - 1.0, -LID_GAP / 2, LID_Z0, LID_Z0 + LID_T)
        over = _box(-W / 2, W / 2, front, -D / 2, LID_Z0, LID_Z0 + LID_T)                   # over the doors
        over = over - [_corner_cut(s, front, LID_Z0 - 1, LID_Z0 + LID_T + 1) for s in (1, -1)]
        panel = panel + over
        panel = panel - [_edge_pocket(s, LID_Z0, up=True) for s in (1, -1)]   # over the upper doors' magnets
        edge = -LID_GAP / 2
    else:
        panel = _box(x0, x1, LID_GAP / 2, D / 2, LID_Z0, LID_Z0 + LID_T) & _outline()
        edge = LID_GAP / 2
    panel = panel - _cyl(15.0, "z", (0, edge, 0), LID_Z0 - 1, LID_Z0 + LID_T + 1)
    for s in (1, -1):
        panel = panel - _cyl(MAG_D / 2, "z", (s * (IN_W / 2 - RAIL_W / 2), _lid_magnet_y(half), 0), LID_Z0 - 0.01, LID_Z0 + MAG_DEPTH)
    import travel_mount as tm                                    # the outside mounting grid
    return panel - tm.grid_cuts("top", half)


def _corner_cut(s: int, front: float, z0: float, z1: float) -> bd.Shape:
    """What rounds a front corner of the lid's overhang (or the plinth) in plan, between z0 and z1."""
    r = LID_FRONT_R
    cx, cy = s * (W / 2 - r), front + r
    x0, x1 = sorted((cx, s * (W / 2 + 1)))
    square = _box(x0, x1, front - 1, cy, z0, z1)
    return square - _cyl(r, "z", (cx, cy, 0), z0 - 1, z1 + 1)


def handle() -> bd.Shape:
    """Arched carry handle, legs screwed to both side walls at mid-depth, in place.

    One continuous bar of even thickness, drawn as a centre line and offset to both
    sides with rounded ends; then every edge of its section is rounded, so the grip
    is a soft stadium with nothing sharp under the fingers.
    """
    t = HANDLE_BAR
    x = W / 2 + t / 2                                   # leg centre lines, legs flat on the walls
    knee = H + 9.0                                      # legs turn into the arch just above the walls, rounding and all
    centre = bd.Wire([
        bd.Line((x, H - HANDLE_LEG + t / 2), (x, knee)),
        bd.ThreePointArc((x, knee), (0, H + HANDLE_SAG), (-x, knee)),
        bd.Line((-x, knee), (-x, H - HANDLE_LEG + t / 2)),
    ])
    # Round the knees in the centre line, so the bar runs tangent all the way round and its
    # offset sides carry no little corner arcs.
    centre = centre.fillet_2d(HANDLE_KNEE_R, [v for v in centre.vertices() if abs(v.Y - knee) < 1e-6])
    profile = bd.Face(centre.offset_2d(t / 2, kind=bd.Kind.ARC, side=bd.Side.BOTH, closed=True))
    solid = bd.extrude(profile, amount=HANDLE_DEPTH)
    solid = bd.fillet(solid.edges().filter_by(bd.Axis.Z, reverse=True), radius=HANDLE_EDGE_R)
    solid = solid.rotate(bd.Axis.X, 90)
    bb = profile.bounding_box()
    solid = _place(solid, x0=bb.min.X, y0=-HANDLE_DEPTH / 2, z0=bb.min.Y)
    for s in (1, -1):
        for y in HANDLE_SCREW_Y:
            for z in HANDLE_SCREW_Z:
                solid = solid - _m3_pilot((s * W / 2, y, z), (s, 0, 0))
    return solid


def to_print(shape: bd.Shape, rotation: tuple[float, float, float]) -> bd.Shape:
    """Turn an in-place part into its print orientation, centred, resting on z=0."""
    turned = shape.moved(bd.Location((0, 0, 0), rotation))
    bb = turned.bounding_box()
    return turned.moved(bd.Location((-(bb.min.X + bb.max.X) / 2, -(bb.min.Y + bb.max.Y) / 2, -bb.min.Z)))


# --- the machine, for checking fit only ---------------------------------------

def machine_reference() -> bd.Shape:
    """Stand-in for the Studio: base and tray, body with its open brewing recess, buttons, dripper, tank, plug."""
    f = M_FRONT_Y
    hw = M_BODY_W / 2
    base = _box(-M_BASE_W / 2, M_BASE_W / 2, f, M_BACK_Y, DECK_Z, DECK_Z + M_TRAY_Z)
    body = _box(-hw, hw, f + M_BUTTON_PROUD, M_BACK_Y, DECK_Z + M_TRAY_Z, DECK_Z + M_HEIGHT)
    recess = _box(-hw - 1, hw + 1, f - 1, f + M_RECESS_DEPTH, DECK_Z + M_TRAY_Z, DECK_Z + M_RECESS_TOP)
    recess_right = _box(0, hw + 1, f - 1, f + M_RECESS_DEPTH, DECK_Z + M_RECESS_TOP - 1, DECK_Z + M_RECESS_RIGHT_TOP)
    tank = _box(-hw, -hw + M_TANK_W, M_BACK_Y - M_TANK_DEPTH, M_BACK_Y + 0.5,
                DECK_Z + M_HEIGHT - M_TANK_DROP, DECK_Z + M_HEIGHT + 0.5)
    shell = base + (body - recess - recess_right - tank)
    buttons = [_cyl(M_BUTTON_D / 2, "y", (x, 0, DECK_Z + M_BUTTON_Z), f, f + M_BUTTON_PROUD + 1) for x in M_BUTTON_X]
    dripper = _cyl(30.0, "z", (M_DRIPPER_X, f + 55.0, 0), DECK_Z + M_TRAY_Z + 195.0, DECK_Z + M_RECESS_RIGHT_TOP + 0.5)
    machine = shell + buttons + [dripper]
    plug = _box(M_SOCKET_X - 17.5, M_SOCKET_X + 17.5, M_BACK_Y, M_BACK_Y + 25, DECK_Z + M_SOCKET_Z - 14, DECK_Z + M_SOCKET_Z + 14)
    machine.label = "xbloom_studio"
    tank.label = "water_tank"
    plug.label = "right_angle_c13_plug"
    return bd.Compound(children=[machine, tank, plug], label="xbloom_studio_reference")
