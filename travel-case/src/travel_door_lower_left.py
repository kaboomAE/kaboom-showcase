"""Lower left door, opens first; its two trays screw on behind. Prints front face down."""

from cadgen import srgb, step, stl, threemf

import travel_mount as tm
import travel_parts as tp


@step(out="../STEP/travel_door_lower_left.step")
@stl(out="../STL/travel_door_lower_left.stl")
@threemf(out="../3MF/travel_door_lower_left.3mf")
def travel_door_lower_left():
    part = tp.to_print(tp.door(-1, "lower"), (90, 0, 0))
    part.label = "travel_door_lower_left"
    part.color = srgb(tp.COLOURS["door"])
    return part


if __name__ == "__main__":
    travel_door_lower_left()
