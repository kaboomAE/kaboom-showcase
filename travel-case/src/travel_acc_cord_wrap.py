"""Sample attachment: two horns to coil the power cord on the back, on two latching pegs. Prints upright, no supports."""

from cadgen import srgb, step, stl, threemf

import travel_mount as tm
import travel_parts as tp


@step(out="../STEP/travel_acc_cord_wrap.step")
@stl(out="../STL/travel_acc_cord_wrap.stl")
@threemf(out="../3MF/travel_acc_cord_wrap.3mf")
def travel_acc_cord_wrap():
    part = tp.to_print(tm.cord_wrap(), tm.PRINT_ROT['travel_acc_cord_wrap'])
    part.label = "travel_acc_cord_wrap"
    part.color = srgb(tp.COLOURS["accent"])
    return part


if __name__ == "__main__":
    travel_acc_cord_wrap()
