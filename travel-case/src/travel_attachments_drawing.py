"""Engineering drawing: the mounting hole, the peg and its latch, and the sample attachments.

Attachments are drawn in their mounting frame: X along the wall, Z up, the wall's
surface at Y = 0 and the attachment in front of it (Y < 0).
"""

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


@eng_drawing(out="../PDF/travel_attachments_drawing.pdf")
def travel_attachments_drawing():
    sheets = []

    # --- the mounting hole, on a coupon of wall, and the peg with its latch ------------
    a, w = tm.R + tm.CLEAR, tm.NECK + tm.CLEAR
    coupon = tp._box(-14, 14, 0, tp.WALL, -12, 24) - tm.hole_tool()
    hole = Sheet("A3", scale=3.0, title="TRAVEL CASE - MOUNTING HOLE", part_number="TC-301",
                 notes=["ONE HOLE IN A PIECE OF 6 WALL, SEEN FROM OUTSIDE. EVERY HOLE ON THE CASE IS THIS ONE;",
                        f"ON THE LID IT IS TURNED 90 DEG (PEGS SLIDE ALONG X). A SPOT IS TWO, {tm.PITCH:g} APART.",
                        f"BLIND, {tm.HOLE_DEPTH:g} DEEP: {tp.WALL - tm.HOLE_DEPTH:g} OF WALL LEFT BEHIND, NOTHING SHOWS INSIDE.",
                        f"ENTRY DIA {2 * a:g} WITH 50 DEG POINTS ABOVE AND BELOW: THE ROOF PRINTS WITHOUT SUPPORT.",
                        f"SLOT {2 * w:g} WIDE THROUGH A {tm.LIP:g} LIP; BEHIND THE LIP THE HOLE WIDENS AT 50 DEG.",
                        f"THE PEG SEATS {tm.DROP:g} BELOW THE ENTRY'S CENTRE (DIMENSIONS FROM THE SEAT).",
                        f"{tm.CLEAR:g} CLEAR OF THE PEG EACH SIDE; THE PLA KIT TRIES {' / '.join('%g' % c for c in tm.CLEARS)}."],
                 **COMMON)
    top, front, right, _ = hole.three_views(coupon, iso=True, gap=40)
    front.overall()
    front.dim((-a, 0, tm.DROP), (a, 0, tm.DROP))                 # the slot's width is in note 5
    front.dim((0, 0, 0), (0, 0, tm.DROP), orientation="v")
    front.dim((0, 0, tm.DROP), (0, 0, tm.HOLE_ABOVE), orientation="v")
    right.dim((0, 0, -tm.HOLE_BELOW), (0, tm.HOLE_DEPTH, -tm.HOLE_BELOW), orientation="h")
    sheets.append(hole)

    plate = (tm._plate(-26, 26, -12, 34) + tm._pegs((-tm.PITCH / 2, 0), (tm.PITCH / 2, 0)))
    plate = tm.with_latch(plate, tm.PITCH / 2, 0)
    pegs = Sheet("A3", scale=2.0, title="TRAVEL CASE - PEGS AND LATCH", part_number="TC-302",
                 notes=["A PLAIN PLATE WITH TWO PEGS, THE LATCH OVER THE RIGHT ONE: EVERY ATTACHMENT HAS THESE.",
                        f"PEG: A DIAMOND, DIA {2 * tm.R:g} WITH 50 DEG POINTS, ON A NECK {2 * tm.NECK:g} WIDE, {tm.NECK_L:g} LONG;",
                        f"THE HEAD FLARES 50 DEG FROM THE NECK, {tm.PEG_L:g} FROM THE PLATE. PEGS PRINT LYING ALONG THE BED.",
                        f"LATCH: TONGUE {tm.TONGUE_W:g} x {tm.TONGUE_L:g} x {tm.TONGUE_T['latch']:g} IN A {tm.TONGUE_GAP:g} SLOT, "
                        f"ITS BUMP {tm.BUMP_H:g} PROUD;", "THE BUMP FILLS THE ENTRY ONCE THE PEGS HAVE DROPPED. PULL THE TAB TO LIFT OFF.",
                        "HANG: PEGS INTO THE ENTRIES, PUSH FLAT, DROP 9."], **COMMON)
    top, front, right, _ = pegs.three_views(plate, iso=True)
    front.overall()
    right.overall()
    sheets.append(pegs)

    upright, on_side = "PRINT UPRIGHT, AS DRAWN: NO SUPPORTS.", "PRINT ON ITS SIDE, AS IN ITS PRINT FILE: NO SUPPORTS."
    samples = (
        ("TC-311", "SMALL BIN", tm.bin_small(), 1.0, upright, ["2 PEGS 28 APART, LATCH OVER THE RIGHT ONE.", "48 x 36 x 45 INSIDE."]),
        ("TC-312", "FILTER SLEEVE", tm.filter_holder(), 0.5, upright, ["2 PEGS 28 APART, LATCH OVER THE RIGHT ONE; AN UPPER SPOT.",
                                                                       "FOR 155 FLAT FILTER PAPERS."]),
        ("TC-313", "DRIPPER RING", tm.dripper_ring(), 0.5, "PRINT UPSIDE DOWN, RING ON THE BED: NO SUPPORTS.",
         ["2 PEGS 28 APART, LATCH OVER THE RIGHT ONE, BELOW THE RING.", "RING DIA 100 INSIDE: MEASURE THE DRIPPER'S RIM FIRST."]),
        ("TC-314", "CORD WRAP", tm.cord_wrap(), 0.5, upright, ["2 PEGS 28 APART, LATCH OVER THE RIGHT ONE.",
                                                               "HORNS' UNDERSIDES AT 50 DEG: COIL OVER THE TOP ONE, UNDER THE BOTTOM ONE."]),
        ("TC-315", "TOP TRAY", tm.top_tray(), 0.5, on_side, ["2 PEGS 28 APART FOR THE LID; SLIDES 9 ALONG THE LID TO SEAT.",
                                                             "LATCH ON THE FLANGE, ITS BUMP IN THE NEXT ROW'S HOLE."]),
    )
    for number, name, shape, scale, how, extra in samples:
        sheet = Sheet("A3", scale=scale, title=f"TRAVEL CASE - ATTACHMENT, {name}", part_number=number,
                      notes=["DRAWN IN THE MOUNTING FRAME: WALL SURFACE AT THE BACK OF THE PLATE.",
                             how, "HOLE AND PEG: SEE TC-301, TC-302.", *extra], **COMMON)
        top, front, right, _ = sheet.three_views(shape, iso=True)
        top.overall()
        front.overall()
        right.overall()
        sheets.append(sheet)
    return sheets


if __name__ == "__main__":
    travel_attachments_drawing()
