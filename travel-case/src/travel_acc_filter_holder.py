"""Sample attachment: sleeve for a stack of 155 mm filter papers, on two latching pegs. Prints upright, no supports."""

from cadgen import srgb, step, stl, threemf

import travel_mount as tm
import travel_parts as tp


@step(out="../STEP/travel_acc_filter_holder.step")
@stl(out="../STL/travel_acc_filter_holder.stl")
@threemf(out="../3MF/travel_acc_filter_holder.3mf")
def travel_acc_filter_holder():
    part = tp.to_print(tm.filter_holder(), tm.PRINT_ROT['travel_acc_filter_holder'])
    part.label = "travel_acc_filter_holder"
    part.color = srgb(tp.COLOURS["accent"])
    return part


if __name__ == "__main__":
    travel_acc_filter_holder()
