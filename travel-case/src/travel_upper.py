"""Shell, upper half: sides, back wall, lid rails and lips, the upper doors' hinge knuckles. Prints as it stands."""

from cadgen import srgb, step, stl, threemf

import travel_mount as tm
import travel_parts as tp


@step(out="../STEP/travel_upper.step")
@stl(out="../STL/travel_upper.stl")
@threemf(out="../3MF/travel_upper.3mf")
def travel_upper():
    part = tp.to_print(tp.shell_pieces()["upper"], (0, 0, 0))
    part.label = "travel_upper"
    part.color = srgb(tp.COLOURS["shell"])
    return part


if __name__ == "__main__":
    travel_upper()
