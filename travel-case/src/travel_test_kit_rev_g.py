"""Rev G test plate for the xBloom travel case: the teardrop mounting holes and pegs, in PLA.

Rev G swapped the accessory rails for teardrop mounting spots (travel_mount.py). Before the shells, this
plate checks the hole prints clean both ways the case prints it, which clearance fits, and
which catch the owner prefers:

  W   wall coupon: a piece of 6 mm wall printed standing, as the shells print, with two
      columns of holes 28 apart in three rows: 0.15, 0.25 and 0.35 clear of the peg, bottom
      to top (one, two and three notches on its left edge). The case has 0.25.
  L   lid coupon: a piece of lid panel printed flat, as the lids print, with two holes at
      0.25, turned as on the lid (the pegs slide along it).
  P1  peg plate, "latch": two pegs and the latch the attachments carry, a square catch
      released only by pulling its tab (one notch on its top edge).
  P2  peg plate, "click": the same with a stiffer tongue and a ramped catch that lets go to
      a firm lift (two notches).
  P3  peg plate, plain: two pegs, no catch, to feel the drop and the lip alone (three notches).

Hang each plate on each row of W and on L: pegs into the entries, push flat, drop 9.
"""

from __future__ import annotations

from cadgen import build123d as bd
from cadgen import srgb, step, stl, threemf

import travel_mount as tm
import travel_parts as tp
import travel_test_kit as kit

COUPON_W = 27.0              # half width of the wall coupon
FOOT = 18.0                  # how far the feet stand out, so the upright pieces stand steady


def _notches(n: int, edge: str, at: float, x0: float, x1: float) -> list[bd.Shape]:
    """n small V-notches: along the top edge at z=at (from x0), or down the left edge at x=at (from z x0)."""
    out = []
    for i in range(n):
        c = x0 + 3.0 * i
        if edge == "top":
            pts = [(c - 1.0, at + 0.01), (c + 1.0, at + 0.01), (c, at - 1.0)]
        else:
            pts = [(at - 0.01, c - 1.0), (at - 0.01, c + 1.0 * tm.STEEP), (at + 1.0, c)]     # its roof steep
        out.append(tp._prism_xz(pts, -50.0, 50.0))
    return out


def wall_coupon() -> list[tuple[str, bd.Shape, tuple]]:
    top = 2 * tm.PITCH + 2 * tm.DROP + tm.HOLE_BELOW + 3.0      # room over the top row for the bump going on
    slab = tp._box(-COUPON_W, COUPON_W, 0, tp.WALL, -13.0, top)
    foot = tp._box(-COUPON_W, COUPON_W, tp.WALL - 0.01, tp.WALL + FOOT, -13.0, -10.0)
    holes = [tm.hole_tool(c).moved(bd.Location((x, 0, k * tm.PITCH)))
             for k, c in enumerate(tm.CLEARS) for x in (-tm.PITCH / 2, tm.PITCH / 2)]
    marks = [m for k in range(3) for m in _notches(k + 1, "left", -COUPON_W, k * tm.PITCH - 3.0, 0)]
    return [("W wall coupon 0.15 / 0.25 / 0.35", slab + foot - holes - marks, (0, 0, 0))]


def lid_coupon() -> list[tuple[str, bd.Shape, tuple]]:
    """Two holes as on the lid, the peg plates' two pegs 28 apart across the slide, turned to print top up."""
    slab = tp._box(-40.0, 14.0, 0, tp.LID_T, -tm.PITCH / 2 - 14.0, tm.PITCH / 2 + 14.0)
    tool = tm.to_lid(tm.hole_tool())
    holes = [tool.moved(bd.Location((0, 0, v))) for v in (-tm.PITCH / 2, tm.PITCH / 2)]
    return [("L lid coupon", slab - holes, (-90, 0, 0))]


def peg_plate(catch: str | None) -> bd.Shape:
    top = tm._latch_top(0) if catch else 12.0
    plate = tm._plate(-26.0, 26.0, -12.0, top) + tm._pegs((-tm.PITCH / 2, 0), (tm.PITCH / 2, 0))
    plate = plate + tp._box(-26.0, 26.0, -tm.PLATE_T - FOOT + 6.0, -tm.PLATE_T + 0.01, -12.0, -9.0)   # a foot in front
    if catch:
        plate = tm.with_latch(plate, tm.PITCH / 2, 0, catch)
    n = {"latch": 1, "click": 2, None: 3}[catch]
    return plate - _notches(n, "top", top, -20.0, 0)


def plates() -> list[tuple[str, bd.Shape, tuple]]:
    return [("P1 peg plate, latch", peg_plate("latch"), (0, 0, 0)),
            ("P2 peg plate, click", peg_plate("click"), (0, 0, 0)),
            ("P3 peg plate, plain", peg_plate(None), (0, 0, 0))]


def pieces() -> list[tuple[str, bd.Shape]]:
    items = wall_coupon() + lid_coupon() + plates()
    return [(name, tp.to_print(shape, rot)) for name, shape, rot in items]


@step(out="../STEP/travel_test_kit_rev_g.step")
@stl(out="../STL/travel_test_kit_rev_g.stl")
@threemf(out="../3MF/travel_test_kit_rev_g.3mf")
def travel_test_kit_rev_g():
    plate = bd.Compound(children=kit.layout(pieces()), label="travel_test_kit_rev_g")
    plate.color = srgb(tp.COLOURS["door"])
    return plate


if __name__ == "__main__":
    travel_test_kit_rev_g()
