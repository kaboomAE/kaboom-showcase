"""Sample attachment: shallow tray for the back lid panel, on two latching pegs. Prints on its side, no supports."""

from cadgen import srgb, step, stl, threemf

import travel_mount as tm
import travel_parts as tp


@step(out="../STEP/travel_acc_top_tray.step")
@stl(out="../STL/travel_acc_top_tray.stl")
@threemf(out="../3MF/travel_acc_top_tray.3mf")
def travel_acc_top_tray():
    part = tp.to_print(tm.top_tray(), tm.PRINT_ROT['travel_acc_top_tray'])
    part.label = "travel_acc_top_tray"
    part.color = srgb(tp.COLOURS["accent"])
    return part


if __name__ == "__main__":
    travel_acc_top_tray()
