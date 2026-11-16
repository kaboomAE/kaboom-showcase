"""Front sliding lid panel; its overhang carries the upper doors' magnets. Prints flat."""

from cadgen import srgb, step, stl, threemf

import travel_mount as tm
import travel_parts as tp


@step(out="../STEP/travel_lid_front.step")
@stl(out="../STL/travel_lid_front.stl")
@threemf(out="../3MF/travel_lid_front.3mf")
def travel_lid_front():
    part = tp.to_print(tp.lid("front"), (0, 0, 0))
    part.label = "travel_lid_front"
    part.color = srgb(tp.COLOURS["shell"])
    return part


if __name__ == "__main__":
    travel_lid_front()
