"""Sample attachment: small open bin for the brush, scoop or dosing cup, on two latching pegs. Prints upright, no supports."""

from cadgen import srgb, step, stl, threemf

import travel_mount as tm
import travel_parts as tp


@step(out="../STEP/travel_acc_bin.step")
@stl(out="../STL/travel_acc_bin.stl")
@threemf(out="../3MF/travel_acc_bin.3mf")
def travel_acc_bin():
    part = tp.to_print(tm.bin_small(), tm.PRINT_ROT['travel_acc_bin'])
    part.label = "travel_acc_bin"
    part.color = srgb(tp.COLOURS["accent"])
    return part


if __name__ == "__main__":
    travel_acc_bin()
