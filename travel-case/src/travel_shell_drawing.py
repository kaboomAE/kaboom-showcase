"""Engineering drawing: the two shell halves of the xBloom travel case, shown as installed."""

from __future__ import annotations

from cadgen.eng_drawing import Sheet, eng_drawing

import travel_mount as tm
import travel_parts as tp

COMMON = dict(material="ASA", revision="G", units="mm",
              revisions=[("A", "2026-10-19", "INITIAL RELEASE"),
                         ("B", "2026-10-20", "ASA; THICKER HANDLE; R5 HINGES; LOWER DOOR CATCH"),
                         ("C", "2026-10-20", "426 MACHINE HEIGHT; KABOOM LOGO + @kaboom.ae"),
                         ("D", "2026-10-20", "SEPARATE TRAYS; SUPPORT-FREE PRINTING"),
                         ("E", "2026-10-20", "ONE M3 HINGE ROD PER SIDE"),
                         ("F", "2026-10-28", "NO HINGE INSERT; LEAD-INS; M5 6.6; MAGNETS 5.8"),
                         ("G", "2026-10-29", "MOUNTING SPOTS REPLACE THE RAILS")])


@eng_drawing(out="../PDF/travel_shell_drawing.pdf")
def travel_shell_drawing():
    pieces = tp.shell_pieces()
    hx, hy = tp.hinge_axis(1)
    band_x = tp.IN_W / 2 - tp.BAND / 2

    # --- lower half --------------------------------------------------------------
    lower = Sheet("A2", scale=0.5, title="TRAVEL CASE - SHELL, LOWER HALF", part_number="TC-101",
                  notes=["SHOWN AS INSTALLED. PRINT UPRIGHT AS SHOWN, NO SUPPORTS.",
                         "WALLS 6. BACK CORNERS R10 OUTSIDE, R4 INSIDE.",
                         f"MOUNTING SPOTS: 3 PER SIDE, 2 ON THE BACK, EACH 2 BLIND HOLES {tm.PITCH:g} APART, "
                         f"{tm.HOLE_DEPTH:g} DEEP, SEATS {tm.LOWER:g} AND {tm.UPPER:g} UP: SEE TC-301.",
                         f"IEC C14 CUT-OUT {tp.IEC_CUT[0]:g} x {tp.IEC_CUT[1]:g} IN BACK WALL, CENTRE "
                         f"X {tp.IEC_X:.1f} FROM CL, {tp.IEC_Z:g} UP; 2x DIA 3.4 AT {tp.IEC_SCREW_PITCH:g} PITCH.",
                         f"MACHINE RIM {tp.RIM_H:g} HIGH, 4.5 WIDE, 0.5 CLEAR OF THE BASE.",
                         f"PLINTH {tp.DOOR_T:g} DEEP UNDER THE LOWER DOORS, CORNERS R{tp.LID_FRONT_R:g}.",
                         "PRINT WITH 5 WALLS."], **COMMON)
    top, front, right, _ = lower.three_views(pieces["lower"], iso=True)
    top.overall()
    front.overall()
    right.overall()
    rim_y = 0.0
    front.dim((-tp.M_BASE_W / 2 - 0.5, rim_y, tp.FLOOR + tp.RIM_H), (tp.M_BASE_W / 2 + 0.5, rim_y, tp.FLOOR + tp.RIM_H))
    top.hole((band_x, tm_y(), tp.Z_SPLIT), tp.CLEAR_D, depth=20, count=2 * len(tp.Z_JOINT_Y) + len(tp.Z_JOINT_BACK_X),
             label="M3 x 12, SPOT FACE DIA 6.5 BELOW")
    top.hole((hx, hy, tp.hinge_centres("lower")[1] + tp.HINGE_LEN / 2), tp.HINGE_PIN_D, thru=True, count=2, label="M3 HINGE ROD; 2.5 x 6 PRINTED HOLE OVER A 2 FLOOR IN THE LOWEST KNUCKLE")
    front.hole((tp.EDGE_MAG_X, -tp.D / 2, tp._sill_magnet_z()), tp.MAG_D, depth=tp.MAG_DEPTH, count=2, angle=-40, label="MAGNET 6 x 2")
    right.dim((tp.W / 2, 0, 0), (tp.W / 2, 0, tm.LOWER))                         # the lower spots' seats
    top.hole((tp.CATCH_X, tp.HINGE_Y, tp.FLOOR), tp.CATCH_SEAT_D, depth=tp.CATCH_SEAT_DEPTH, count=2, angle=-60,
             label="CATCH SEAT")

    # --- upper half --------------------------------------------------------------
    upper = Sheet("A2", scale=0.5, title="TRAVEL CASE - SHELL, UPPER HALF", part_number="TC-102",
                  notes=["SHOWN AS INSTALLED. PRINT UPRIGHT AS SHOWN, NO SUPPORTS.",
                         "WALLS 6. LID RAILS 7 WIDE WITH 3 LIPS OVER THE LID.",
                         "M3 HEAT-SET INSERTS PRESSED FROM BELOW INTO THE JOINT BAND'S BOSSES; 0.5 x 45 LEAD-IN.",
                         "MOUNTING HOLES: SEE TC-301; TEARDROP ROOFS POINT UP AS PRINTED.",
                         "PRINT WITH 5 WALLS."], **COMMON)
    top, front, right, _ = upper.three_views(pieces["upper"], iso=True)
    top.overall()
    front.overall()
    right.overall()
    top.hole((band_x, tm_y(), tp.Z_SPLIT), tp.INSERT_D, depth=tp.INSERT_DEPTH,
             count=2 * len(tp.Z_JOINT_Y) + len(tp.Z_JOINT_BACK_X), label="M3 HEAT-SET INSERT, FROM BELOW, 0.5 x 45 LEAD-IN")
    top.hole((tp.IN_W / 2 - tp.RAIL_W / 2, -70.0, tp.LID_Z0), tp.MAG_D, depth=tp.MAG_DEPTH, count=4, label="MAGNET 6 x 2")
    right.hole((tp.W / 2, tp.HANDLE_SCREW_Y[0], tp.HANDLE_SCREW_Z[0]), tp.CLEAR_D, thru=True, count=8, label="HANDLE M3 x 12")
    right.dim((tp.W / 2, 0, tp.Z_SPLIT), (tp.W / 2, 0, tm.UPPER))               # the upper spots' seats, 75 over the seam
    return [lower, upper]


def tm_y() -> float:
    return tp.Z_JOINT_Y[0]


if __name__ == "__main__":
    travel_shell_drawing()
