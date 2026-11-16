"""Engineering drawing: the four doors of the xBloom travel case and the lower doors' trays, as installed (shut)."""

from __future__ import annotations

from cadgen.eng_drawing import Sheet, eng_drawing

import travel_parts as tp

COMMON = dict(material="ASA", revision="G1", units="mm",
              revisions=[("A", "2026-10-19", "INITIAL RELEASE"),
                         ("B", "2026-10-20", "ASA; THICKER HANDLE; R5 HINGES; LOWER DOOR CATCH"),
                         ("C", "2026-10-20", "426 MACHINE HEIGHT; KABOOM LOGO + @kaboom.ae"),
                         ("D", "2026-10-20", "SEPARATE TRAYS; SUPPORT-FREE PRINTING"),
                         ("E", "2026-10-20", "ONE M3 HINGE ROD PER SIDE"),
                         ("F", "2026-10-28", "NO HINGE INSERT; LEAD-INS; M5 6.6; MAGNETS 5.8"),
                         ("G", "2026-10-29", "MOUNTING SPOTS REPLACE THE RAILS"),
                         ("G1", "2026-11-06", "CATCH: PLUNGER STOPS AT THE BORE'S END")])
PARTS = {
    (-1, "upper"): ("TC-111", "UPPER LEFT DOOR"),
    (1, "upper"): ("TC-112", "UPPER RIGHT DOOR"),
    (-1, "lower"): ("TC-113", "LOWER LEFT DOOR"),
    (1, "lower"): ("TC-114", "LOWER RIGHT DOOR"),
}
TRAYS = {
    (-1, 0): ("TC-115", "LOWER LEFT DOOR, LOWER TRAY"),
    (-1, 1): ("TC-116", "LOWER LEFT DOOR, UPPER TRAY"),
    (1, 0): ("TC-117", "LOWER RIGHT DOOR, LOWER TRAY"),
    (1, 1): ("TC-118", "LOWER RIGHT DOOR, UPPER TRAY"),
}


@eng_drawing(out="../PDF/travel_doors_drawing.pdf")
def travel_doors_drawing():
    sheets = []
    mid_y = -tp.D / 2 - tp.DOOR_T / 2
    back = -tp.D / 2
    for (s, tier), (number, name) in PARTS.items():
        z0, z1 = tp.DOOR_Z[tier]
        notes = [
            "SHOWN AS INSTALLED, SHUT. PRINT FRONT FACE DOWN, NO SUPPORTS.",
            f"{tp.DOOR_T:g} THICK. 45 DEG MEETING EDGE; THE LEFT DOOR LAPS OVER THE RIGHT.",
            f"HINGE KNUCKLE R{tp.HINGE_R:g} x {tp.KNUCKLE_MID - 2 * tp.KNUCKLE_GAP:g} LONG, 0.5 CLEAR OF THE SHELL'S.",
            "PRINT WITH 6 WALLS: THE KNUCKLE LIES ACROSS ITS LAYERS.",
            "MAGNETS 6 x 2 GLUED IN; CHECK POLARITY AGAINST THEIR PARTNERS.",
        ]
        if tier == "upper" and s > 0:
            notes.append(f"KABOOM LOGO, {tp.LOGO_W:g} WIDE, AND {tp.SOCIAL} BELOW: DEBOSSED {tp.LOGO_DEPTH:g}.")
        if tier == "lower":
            pair = "TC-117/118" if s > 0 else "TC-115/116"
            notes.append(f"TRAYS {pair} SCREW TO THE BACK FACE: 4 M3 INSERTS, M3 x 8.")
            notes.append("CATCH: M5 INSERT (8 LONG) + M5 x 12 BALL PLUNGER UP INTO THE BOTTOM EDGE.")
            notes.append(f"CATCH BORE: {tp.CATCH_INSERT_D:g} x {tp.CATCH_INSERT_DEPTH:g}, {tp.CATCH_RELIEF_D:g} x {tp.CATCH_RELIEF_L:g} RELIEF,"
                         f" {tp.CATCH_BORE_D:g} TO A FLAT END {tp.CATCH_BORE_DEPTH:.2f} FROM THE EDGE.")
            notes.append(f"THE PLUNGER SCREWS IN TO THAT END: BALL {tp.CATCH_BALL_PROUD:g} PROUD. NOTHING TO ADJUST.")
        sheet = Sheet("A2", scale=0.5, title=f"TRAVEL CASE - {name}", part_number=number, notes=notes, **COMMON)
        door = tp.door(s, tier)
        top, front, right, _ = sheet.three_views(door, iso=True)
        top.overall()
        front.overall()
        right.overall()
        ax, ay = tp.hinge_axis(s)
        top.hole((ax, ay, z1), tp.ROD_CLEAR_D, thru=True, label="CHANNEL FOR THE M3 HINGE ROD, FULL HEIGHT")
        top.hole((s * tp.EDGE_MAG_X, mid_y, z1), tp.EDGE_MAG_D, depth=tp.EDGE_MAG_DEPTH, angle=135 if s > 0 else 45,
                 label="MAGNET 6 x 2, TOP EDGE")
        if tier == "lower":
            top.hole((s * tp.CATCH_X, tp.HINGE_Y, z0), tp.CATCH_INSERT_D, depth=tp.CATCH_INSERT_DEPTH,
                     angle=135 if s > 0 else 45, label="M5 INSERT, BALL PLUNGER, FROM BELOW")
            x, z = tp._tray_screws(s, 0)[0]
            front.hole((x, back, z), tp.INSERT_D, depth=tp.INSERT_DEPTH, count=4, angle=-45 if s > 0 else -135,
                       label="M3 INSERT, BACK FACE, FOR THE TRAYS, 0.5 x 45 LEAD-IN")
        sheets.append(sheet)

    for (s, level), (number, name) in TRAYS.items():
        notes = [
            "SHOWN AS INSTALLED. PRINT STANDING ON ITS FLOOR: NO SUPPORTS.",
            f"WALLS AND FLOOR {tp.BIN_WALL:g}; {tp.TRAY_PLATE:g} PLATE ON THE DOOR SIDE; {tp.BIN_LIP:g} LIP ON THE MACHINE SIDE.",
            "OUTLINE KEEPS THE DOOR SWING CLEAR: DON'T ENLARGE IT.",
            "2 M3 x 8 FROM INSIDE INTO THE DOOR'S INSERTS.",
        ]
        if s > 0 and level == 0:
            notes.append("TAKES THE OMNI DRIPPER 2 TABLE HOLDER (82 x 55) STANDING UP.")
        sheet = Sheet("A3", scale=0.5, title=f"TRAVEL CASE - {name}", part_number=number, notes=notes, **COMMON)
        t = tp.tray(s, level)
        top, front, right, _ = sheet.three_views(t, iso=True)
        top.overall()
        front.overall()
        right.overall()
        x, z = tp._tray_screws(s, level)[0]
        front.hole((x, back, z), tp.CLEAR_D, thru=True, count=2, angle=-150, label="M3 x 8 TO THE DOOR")
        sheets.append(sheet)
    return sheets


if __name__ == "__main__":
    travel_doors_drawing()
