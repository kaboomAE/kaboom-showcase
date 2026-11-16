"""Arched carry handle. Prints lying on its side."""

from cadgen import srgb, step, stl, threemf

import travel_mount as tm
import travel_parts as tp


@step(out="../STEP/travel_handle.step")
@stl(out="../STL/travel_handle.stl")
@threemf(out="../3MF/travel_handle.3mf")
def travel_handle():
    part = tp.to_print(tp.handle(), (90, 0, 0))
    part.label = "travel_handle"
    part.color = srgb(tp.COLOURS["accent"])
    return part


if __name__ == "__main__":
    travel_handle()
