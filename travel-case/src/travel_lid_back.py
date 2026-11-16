"""Back sliding lid panel. Prints flat."""

from cadgen import srgb, step, stl, threemf

import travel_mount as tm
import travel_parts as tp


@step(out="../STEP/travel_lid_back.step")
@stl(out="../STL/travel_lid_back.stl")
@threemf(out="../3MF/travel_lid_back.3mf")
def travel_lid_back():
    part = tp.to_print(tp.lid("back"), (0, 0, 0))
    part.label = "travel_lid_back"
    part.color = srgb(tp.COLOURS["shell"])
    return part


if __name__ == "__main__":
    travel_lid_back()
