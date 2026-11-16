"""Rev F test plate for the xBloom travel case: the new hinge foot, the M3 lead-ins and the 5.8 magnet pockets.

After the second PLA results (28 Oct) the hinge's insert went: the lowest knuckle now has a
closed floor and a 2.5 mm hole the threaded rod cuts its own thread in. This small plate
checks that, and the two other changes, in PLA, cut from the real parts as before:

  A1F  hinge foot: the lower shell's lower right corner up to the top of its lowest knuckle,
       with the floor and the 2.5 mm hole.
  A2F  its door knuckle: the lower right door's edge from under the knuckle to its middle.
       Stand A2F's knuckle on A1F's and screw an M3 x 30 (or 30 mm of the rod) down through
       both until it stops on the floor: its head ends 2 mm clear of A2F. Swing it 0-180.
  M3   lead-in coupon: three 4.0 pilots with the 0.5 x 45 lead-in and 3 mm of plastic round
       each, mouths up. Press an insert into each.
  MAG  two 5.8 x 2.2 magnet pockets under 1.9 mm of plastic, as in the case.
"""

from __future__ import annotations

from cadgen import build123d as bd
from cadgen import srgb, step, stl, threemf

import travel_parts as tp
import travel_test_kit as kit

COUPON_PITCH = 10.0          # 6 mm of plastic between the coupon's pilots


def hinge_foot() -> list[tuple[str, bd.Shape, tuple]]:
    (ax, ay), zc = tp.hinge_axis(1), tp.hinge_centres("lower")[0]
    knuckle_top = zc - tp.KNUCKLE_MID / 2 - tp.KNUCKLE_GAP         # the lowest shell knuckle's top
    corner = kit._cut(tp.shell_pieces()["lower"], ax - 22, ax + 6, ay - 6, ay + 22, -1, knuckle_top)
    z0 = zc - tp.HINGE_LEN / 2 - tp.KNUCKLE_GAP                    # the door's notch round that knuckle
    edge = kit._cut(tp.door(1, "lower"), ax - 22, ax + 6, ay - 6, ay + 6, z0, zc)
    return [("A1F hinge foot, shell", corner, (0, 0, 0)), ("A2F hinge foot, door knuckle", edge, (90, 0, 0))]


def m3_coupon() -> list[tuple[str, bd.Shape, tuple]]:
    w, t = tp.INSERT_D + 2 * tp.INSERT_WALL, tp.INSERT_DEPTH + tp.INSERT_WALL
    block = tp._box(0, 3 * COUPON_PITCH, 0, w, 0, t)
    for i in range(3):
        block = block - tp._m3_pilot(((i + 0.5) * COUPON_PITCH, w / 2, t), (0, 0, -1))
    return [("M3 lead-in coupon", block, (0, 0, 0))]


def magnet_check() -> list[tuple[str, bd.Shape, tuple]]:
    t, pitch = tp.MAG_DEPTH + 1.9, 11.0
    block = tp._box(0, 2 * pitch, 0, pitch, 0, t)
    block = block - [tp._cyl(tp.MAG_D / 2, "z", ((i + 0.5) * pitch, pitch / 2, 0), t - tp.MAG_DEPTH, t + 1) for i in range(2)]
    return [("MAG 5.8 pockets", block, (0, 0, 0))]


def pieces() -> list[tuple[str, bd.Shape]]:
    items = hinge_foot() + m3_coupon() + magnet_check()
    return [(name, tp.to_print(shape, rot)) for name, shape, rot in items]


@step(out="../STEP/travel_test_kit_rev_f.step")
@stl(out="../STL/travel_test_kit_rev_f.stl")
@threemf(out="../3MF/travel_test_kit_rev_f.3mf")
def travel_test_kit_rev_f():
    plate = bd.Compound(children=kit.layout(pieces()), label="travel_test_kit_rev_f")
    plate.color = srgb(tp.COLOURS["door"])
    return plate


if __name__ == "__main__":
    travel_test_kit_rev_f()
