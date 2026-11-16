"""Shell, lower half: floor with the machine's rim and front sill, the lower doors' hinge knuckles. Prints as it stands."""

from cadgen import srgb, step, stl, threemf

import travel_mount as tm
import travel_parts as tp


@step(out="../STEP/travel_lower.step")
@stl(out="../STL/travel_lower.stl")
@threemf(out="../3MF/travel_lower.3mf")
def travel_lower():
    part = tp.to_print(tp.shell_pieces()["lower"], (0, 0, 0))
    part.label = "travel_lower"
    part.color = srgb(tp.COLOURS["shell"])
    return part


if __name__ == "__main__":
    travel_lower()
