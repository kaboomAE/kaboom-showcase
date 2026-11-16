"""Upper right door. Prints front face down."""

from cadgen import srgb, step, stl, threemf

import travel_mount as tm
import travel_parts as tp


@step(out="../STEP/travel_door_upper_right.step")
@stl(out="../STL/travel_door_upper_right.stl")
@threemf(out="../3MF/travel_door_upper_right.3mf")
def travel_door_upper_right():
    part = tp.to_print(tp.door(1, "upper"), (90, 0, 0))
    part.label = "travel_door_upper_right"
    part.color = srgb(tp.COLOURS["door"])
    return part


if __name__ == "__main__":
    travel_door_upper_right()
