"""Fit-test kit for the xBloom travel case: small pieces cut from the real parts, on one plate.

Print it in PLA before committing the ~4 days of the full case. Every piece is the
real part's geometry inside a small box, so it tests exactly what the case will
have, in the orientation the case's own print files use, and it changes when the
model does. Pairs that go together are printed side by side:

  A  hinge: the lower shell's lower right hinge corner, and the lower right door's
     edge with its knuckle. Pin them with an M3 x 60 bolt, screwed down into the
     printed 2.5 mm hole over the lowest knuckle's floor until it stops (the case
     itself uses one long M3 rod per side; Rev E had an insert there). Swing it 0-180.
  B  shell joint: a piece of each shell half at a joint screw. M3 insert in the
     upper piece, M3 x 12 up through the lower.
  C  (retired in Rev G: the accessory rails gave way to mounting spots; travel_test_kit_rev_g.py
     tests the holes and pegs)
  D  lid rail: the upper shell's top edge (rail, lip and a magnet pocket) and a strip
     of the back lid panel's edge (its magnet pocket). Slide the strip in.
  E  lower door catch: the plinth with its seat, and a door's bottom edge with the
     M5 insert for the ball plunger. The plunger screws in until it stops on the hole's
     end, ball 1.92 mm proud (since 6 Nov 2026; travel_test_kit_catch.py prints E2 alone).
  F  IEC inlet: the back wall's cut-out and screw holes. Try the lead in it.
  G  gauge: insert pilots (M3 3.8/4.0/4.2, M5 6.4/6.6/6.8) and magnet pockets
     (5.6/5.8/6.0), to pick the sizes that suit the inserts and magnets bought. Each
     group's middle size is the one the case has: the owner's picks of 28 Oct (M3 4.0,
     M5 6.6, magnets 5.8).
  H  logo: the upper right door's face with the logo, 3 mm thick, printed face down.

travel_test_kit_retest.py prints C, D and the gauge's magnet row alone, for a quick re-check;
travel_test_kit_rev_f.py the Rev F hinge foot, the M3 lead-ins and the 5.8 magnet pockets;
travel_test_kit_rev_g.py the Rev G mounting holes: wall and lid coupons and the peg plates;
travel_test_kit_catch.py a new E2, for the plunger's fixed stop.
"""

from __future__ import annotations

from cadgen import build123d as bd
from cadgen import srgb, step, stl, threemf

import travel_parts as tp

PLATE = 250.0               # lay the pieces out within this square
GAP = 8.0


def _cut(part: bd.Shape, x0, x1, y0, y1, z0, z1) -> bd.Shape:
    return part & tp._box(x0, x1, y0, y1, z0, z1)


def hinge_pair() -> list[tuple[str, bd.Shape, tuple]]:
    s, (ax, ay) = 1, tp.hinge_axis(1)
    zc = tp.hinge_centres("lower")[0]
    top = zc + tp.HINGE_LEN / 2                                 # the top knuckle's top: the bolt's head ends 2 above
    corner = _cut(tp.shell_pieces()["lower"], ax - 22, ax + 6, ay - 6, ay + 22, -1, top)
    edge = _cut(tp.door(s, "lower"), ax - 22, ax + 6, ay - 6, ay + 6, 0, top)
    return [("A1 hinge, shell corner", corner, (0, 0, 0)), ("A2 hinge, door edge", edge, (90, 0, 0))]


def joint_pair() -> list[tuple[str, bd.Shape, tuple]]:
    x0, x1, y = tp.IN_W / 2 - 11, tp.W / 2 + 0.01, tp.Z_JOINT_Y[1]
    pieces = tp.shell_pieces()
    lower = _cut(pieces["lower"], x0, x1, y - 15, y + 15, tp.Z_SPLIT - 24, tp.Z_SPLIT)
    upper = _cut(pieces["upper"], x0, x1, y - 15, y + 15, tp.Z_SPLIT, tp.Z_SPLIT + 20)
    return [("B1 joint, lower", lower, (0, 0, 0)), ("B2 joint, upper", upper, (0, 0, 0))]


def lid_pair() -> list[tuple[str, bd.Shape, tuple]]:
    y = tp._lid_magnet_y("back")
    edge = _cut(tp.shell_pieces()["upper"], tp.IN_W / 2 - 16, tp.W / 2 + 0.01, y - 20, y + 20, tp.LID_Z0 - 18, tp.H + 1)
    strip = _cut(tp.lid("back"), tp.IN_W / 2 - 26, tp.W / 2, y - 20, y + 20, 0, 1000)
    return [("D1 lid rail, shell edge", edge, (0, 0, 0)), ("D2 lid rail, lid strip", strip, (0, 0, 0))]


def catch_pair() -> list[tuple[str, bd.Shape, tuple]]:
    x = tp.CATCH_X
    plinth = _cut(tp.shell_pieces()["lower"], x - 15, x + 15, -tp.D / 2 - tp.DOOR_T - 1, -tp.D / 2 + 12, -1, tp.FLOOR + tp.RIM_H)
    z0 = tp.DOOR_Z["lower"][0]
    bottom = _cut(tp.door(1, "lower"), x - 15, x + 15, -200, 0, z0 - 1, z0 + 24)
    return [("E1 catch, plinth", plinth, (0, 0, 0)), ("E2 catch, door bottom", bottom, (90, 0, 0))]


def iec_piece() -> list[tuple[str, bd.Shape, tuple]]:
    w = _cut(tp.shell_pieces()["lower"], tp.IEC_X - 32, tp.IEC_X + 32, tp.D / 2 - tp.WALL - 0.01, tp.D / 2 + 1,
             tp.IEC_Z - 20, tp.IEC_Z + 20)
    return [("F IEC cut-out", w, (0, 0, 0))]


GAUGE_STEP = 0.2
GAUGE = {"M3 insert": (tp.INSERT_D, tp.INSERT_DEPTH), "M5 insert": (tp.CATCH_INSERT_D, tp.CATCH_INSERT_DEPTH),
         "Magnet": (tp.MAG_D, tp.MAG_DEPTH)}


def gauge_sizes(group: str) -> tuple[float, float, float]:
    d = GAUGE[group][0]
    return tuple(round(d + k * GAUGE_STEP, 2) for k in (-1, 0, 1))


def gauge(only: tuple[str, ...] = tuple(GAUGE), name: str = "G gauge") -> list[tuple[str, bd.Shape, tuple]]:
    """Pilot and pocket sizes in a row, smallest on the left of each group, the case's own in the middle."""
    groups = [(gauge_sizes(g), GAUGE[g][1]) for g in only]
    t, pitch, x = 9.0, 11.0, 7.0
    holes = []
    for sizes, depth in groups:
        for d in sizes:
            holes.append(tp._cyl(d / 2, "z", (x, 9.0, 0), t - depth, t + 1))
            x += pitch
        x += 4.0
    block = tp._box(0, x - 4.0 + 3.0, 0, 18.0, 0, t)
    return [(name, block - holes, (0, 0, 0))]


def logo_patch() -> list[tuple[str, bd.Shape, tuple]]:
    front = -tp.D / 2 - tp.DOOR_T
    z_top = tp.LOGO_TOP + 3.0
    patch = _cut(tp.door(1, "upper"), tp.LOGO_CX - tp.LOGO_W / 2 - 4, tp.LOGO_CX + tp.LOGO_W / 2 + 4,
                 front - 1, front + 3.0, z_top - 32.0, z_top)
    return [("H logo", patch, (90, 0, 0))]


def pieces() -> list[tuple[str, bd.Shape]]:
    """Every piece turned to print, in the order they go on the plate."""
    out = []
    for name, shape, rot in hinge_pair() + joint_pair() + lid_pair() + catch_pair() + iec_piece() + gauge() + logo_patch():
        out.append((name, tp.to_print(shape, rot)))
    return out


def layout(items: list[tuple[str, bd.Shape]]) -> list[bd.Shape]:
    """Shelf-pack the pieces onto the plate, rows left to right."""
    placed, x, y, row = [], 0.0, 0.0, 0.0
    for name, shape in items:
        bb = shape.bounding_box()
        if x + bb.size.X > PLATE:
            x, y, row = 0.0, y + row + GAP, 0.0
        p = shape.moved(bd.Location((x - bb.min.X - PLATE / 2, y - bb.min.Y - PLATE / 2, -bb.min.Z)))
        p.label = name
        placed.append(p)
        x += bb.size.X + GAP
        row = max(row, bb.size.Y)
    if y + row > PLATE:
        raise ValueError(f"test kit needs {y + row:.0f} mm of plate, more than {PLATE:g}")
    return placed


@step(out="../STEP/travel_test_kit.step")
@stl(out="../STL/travel_test_kit.stl")
@threemf(out="../3MF/travel_test_kit.3mf")
def travel_test_kit():
    kit = bd.Compound(children=layout(pieces()), label="travel_test_kit")
    kit.color = srgb(tp.COLOURS["door"])
    return kit


if __name__ == "__main__":
    travel_test_kit()
