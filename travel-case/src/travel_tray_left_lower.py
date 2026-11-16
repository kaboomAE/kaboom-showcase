"""Lower tray of the lower left door. Prints standing on its floor, no supports."""

from cadgen import srgb, step, stl, threemf

import travel_mount as tm
import travel_parts as tp


@step(out="../STEP/travel_tray_left_lower.step")
@stl(out="../STL/travel_tray_left_lower.stl")
@threemf(out="../3MF/travel_tray_left_lower.3mf")
def travel_tray_left_lower():
    part = tp.to_print(tp.tray(-1, 0), (0, 0, 0))
    part.label = "travel_tray_left_lower"
    part.color = srgb(tp.COLOURS["door"])
    return part


if __name__ == "__main__":
    travel_tray_left_lower()
