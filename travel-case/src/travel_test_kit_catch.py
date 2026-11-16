"""Catch plate for the xBloom travel case: a new E2, the lower door's bottom edge, alone.

The first E2 (5 Nov 2026) took an M5 insert and a plunger screwed in until it stopped, by
chance, with the ball 1.92 mm proud, and that clicked about right on E1. The hole now ends where
a plunger screwed fully home leaves its ball 1.92 mm proud (tp.CATCH_BORE_DEPTH), with a short
relief past the insert for the plastic it pushes ahead. Heat-set an 8 mm-long M5 insert flush,
screw a plunger in until it stops, and check the ball stands 1.9 mm proud and clicks on the
first kit's E1, whose seat hasn't changed.
"""

from __future__ import annotations

from cadgen import build123d as bd
from cadgen import srgb, step, stl, threemf

import travel_parts as tp
import travel_test_kit as kit


def pieces() -> list[tuple[str, bd.Shape]]:
    items = [p for p in kit.catch_pair() if p[0].startswith("E2")]
    return [(name, tp.to_print(shape, rot)) for name, shape, rot in items]


@step(out="../STEP/travel_test_kit_catch.step")
@stl(out="../STL/travel_test_kit_catch.stl")
@threemf(out="../3MF/travel_test_kit_catch.3mf")
def travel_test_kit_catch():
    plate = bd.Compound(children=kit.layout(pieces()), label="travel_test_kit_catch")
    plate.color = srgb(tp.COLOURS["door"])
    return plate


if __name__ == "__main__":
    travel_test_kit_catch()
