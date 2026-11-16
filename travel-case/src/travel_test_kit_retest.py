"""Re-test plate for the xBloom travel case: the fit-test kit's D pair and its magnet row alone.

After the first PLA test the accessory rail (C) and the lid rail (D) were loosened. This small
plate re-checks the lid rail and the magnet row (5.6 / 5.8 / 6.0 since Rev F), in PLA; print it
once more in ASA before the shell halves to see the fits carry over. The rail's pair left it in
Rev G, when mounting spots replaced the rails (travel_test_kit_rev_g.py tests that).
"""

from __future__ import annotations

from cadgen import build123d as bd
from cadgen import srgb, step, stl, threemf

import travel_parts as tp
import travel_test_kit as kit


def pieces() -> list[tuple[str, bd.Shape]]:
    items = kit.lid_pair() + kit.gauge(("Magnet",), "G magnet gauge")
    return [(name, tp.to_print(shape, rot)) for name, shape, rot in items]


@step(out="../STEP/travel_test_kit_retest.step")
@stl(out="../STL/travel_test_kit_retest.stl")
@threemf(out="../3MF/travel_test_kit_retest.3mf")
def travel_test_kit_retest():
    plate = bd.Compound(children=kit.layout(pieces()), label="travel_test_kit_retest")
    plate.color = srgb(tp.COLOURS["door"])
    return plate


if __name__ == "__main__":
    travel_test_kit_retest()
