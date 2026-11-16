"""Engineering drawing: the two sliding lid panels and the carry handle of the xBloom travel case."""

from __future__ import annotations

from cadgen import build123d as bd
from cadgen.eng_drawing import Sheet, eng_drawing

import travel_mount as tm
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


@eng_drawing(out="../PDF/travel_lids_handle_drawing.pdf")
def travel_lids_handle_drawing():
    sheets = []
    for half, number in (("front", "TC-121"), ("back", "TC-122")):
        notes = ["SHOWN AS INSTALLED. PRINT FLAT, TOP FACE UP.",
                 f"{tp.LID_T:g} THICK; SLIDES IN THE SHELL'S RAILS, 0.5 CLEAR EACH SIDE, {tp.LID_RISE:g} UNDER THE LIP.",
                 ("NO MOUNTING SPOT: THE TOP TRAY'S SPOT IS ON THE BACK PANEL." if half == "front" else
                  f"THE TOP TRAY'S SPOT: {len(tm.holes('top', half))} BLIND HOLES, {tm.HOLE_DEPTH:g} DEEP; PEGS SLIDE {tm.DROP:g} ALONG X TO SEAT. SEE TC-301."),
                 "MAGNETS 6 x 2 GLUED IN FROM BELOW; CHECK POLARITY AGAINST THE RAILS."]
        if half == "front":
            notes.append("OVERHANG COVERS THE UPPER DOORS' TOP EDGE; 2 MORE MAGNETS UNDER IT.")
        sheet = Sheet("A3", scale=0.5, title=f"TRAVEL CASE - LID PANEL, {half.upper()}", part_number=number,
                      notes=notes, **COMMON)
        lid = tp.lid(half)
        top, front, right, _ = sheet.three_views(lid, iso=True)
        top.overall()
        front.overall()
        right.overall()
        top.hole((tp.IN_W / 2 - tp.RAIL_W / 2, -70.0 if half == "front" else 70.0, tp.LID_Z0), tp.MAG_D,
                 depth=tp.MAG_DEPTH, count=2, label="MAGNET 6 x 2, FROM BELOW")
        sheets.append(sheet)

    handle = Sheet("A3", scale=0.5, title="TRAVEL CASE - CARRY HANDLE", part_number="TC-131",
                   notes=["SHOWN AS INSTALLED, Z FROM THE TOP OF THE WALLS. PRINT ON ITS SIDE.",
                          f"BAR {tp.HANDLE_BAR:g} x {tp.HANDLE_DEPTH:g}, EVERY EDGE R{tp.HANDLE_EDGE_R:g}.",
                          "ARCH THROUGH THREE POINTS: BOTH KNEES AND THE CROWN.",
                          "M3 HEAT-SET INSERTS IN THE LEGS; M3 x 12 SCREWS FROM INSIDE THE CASE.",
                          "PRINT WITH 6 WALLS AND 40% INFILL."],
                   **COMMON)
    h = tp.handle().moved(bd.Location((0, 0, -tp.H)))            # datum: the top of the side walls
    top, front, right = handle.three_views(h)
    top.overall()
    front.overall()
    right.overall()
    front.hole((tp.W / 2 + tp.HANDLE_BAR, tp.HANDLE_SCREW_Y[0], tp.HANDLE_SCREW_Z[0] - tp.H), tp.INSERT_D, depth=tp.INSERT_DEPTH,
               count=8, angle=-45, label="M3 HEAT-SET INSERT, 0.5 x 45 LEAD-IN")
    sheets.append(handle)
    return sheets


if __name__ == "__main__":
    travel_lids_handle_drawing()
