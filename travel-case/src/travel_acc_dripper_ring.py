"""Sample attachment: ring that hangs the Omni dripper by its rim (diameter to be measured), on two latching pegs. Prints upside down, ring on the bed."""

from cadgen import srgb, step, stl, threemf

import travel_mount as tm
import travel_parts as tp


@step(out="../STEP/travel_acc_dripper_ring.step")
@stl(out="../STL/travel_acc_dripper_ring.stl")
@threemf(out="../3MF/travel_acc_dripper_ring.3mf")
def travel_acc_dripper_ring():
    part = tp.to_print(tm.dripper_ring(), tm.PRINT_ROT['travel_acc_dripper_ring'])
    part.label = "travel_acc_dripper_ring"
    part.color = srgb(tp.COLOURS["accent"])
    return part


if __name__ == "__main__":
    travel_acc_dripper_ring()
