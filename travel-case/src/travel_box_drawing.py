"""Engineering drawing: the assembled xBloom travel case (general arrangement)."""

from __future__ import annotations

from pathlib import Path

from cadgen import build123d as bd
from cadgen import read_scene
from cadgen.eng_drawing import Sheet, eng_drawing

import travel_parts as tp

COMMON = dict(material="ASA", revision="G", units="mm",
              revisions=[("A", "2026-10-19", "INITIAL RELEASE"),
                         ("B", "2026-10-20", "ASA; THICKER HANDLE; R5 HINGES; LOWER DOOR CATCH"),
                         ("C", "2026-10-20", "426 MACHINE HEIGHT; KABOOM LOGO + @kaboom.ae"),
                         ("D", "2026-10-20", "SEPARATE TRAYS; SUPPORT-FREE PRINTING"),
                         ("E", "2026-10-20", "ONE M3 HINGE ROD PER SIDE"),
                         ("F", "2026-10-28", "NO HINGE INSERT; LEAD-INS; M5 6.6; MAGNETS 5.8"),
                         ("G", "2026-10-29", "MOUNTING SPOTS REPLACE THE RAILS")])
CASE = ("lower", "upper", "lid_front", "lid_back", "door_lower_left", "door_lower_right",
        "door_upper_left", "door_upper_right", "handle")


@eng_drawing(out="../PDF/travel_box_drawing.pdf")
def travel_box_drawing():
    scene = read_scene(Path(__file__).parent / "../STEP/travel_box.step")
    leaves = {leaf.label: leaf.shape() for leaf in scene.leaves()}
    case = bd.Compound(children=[leaves[name] for name in CASE])
    fitted = bd.Compound(children=[s for name, s in leaves.items() if name in CASE or name.startswith("acc_")])

    ga = Sheet("A1", scale=0.5, title="TRAVEL CASE - GENERAL ARRANGEMENT", part_number="TC-001",
               notes=["ASSEMBLY OF TC-101/102 SHELL, TC-111..114 DOORS, TC-115..118 TRAYS, TC-121/122 LIDS, TC-131 HANDLE.",
                      "SHELL HALVES JOIN WITH 11 M3 x 12 INTO HEAT-SET INSERTS.",
                      "DOORS TURN ON ONE M3 ROD PER SIDE; OPEN THE LEFT DOOR OF EACH PAIR FIRST.",
                      "LOWER DOORS: HIDDEN BALL CATCHES CLICK INTO THE PLINTH.",
                      "FRONT LID SLIDES FORWARD, BACK LID BACKWARD; THE TANK LIFTS OUT UNDER THE BACK LID.",
                      f"FITS AN XBLOOM STUDIO {tp.M_BODY_W:g} x {tp.M_DEPTH:g} x {tp.M_HEIGHT:g}."], **COMMON)
    top, front, right, _ = ga.three_views(case, iso=True)
    top.overall()
    front.overall()
    right.overall()

    kit = Sheet("A1", scale=0.4, title="TRAVEL CASE - WITH SAMPLE ATTACHMENTS", part_number="TC-002",
                notes=["SAMPLE ATTACHMENTS TC-311..315 ON 6 OF THE 9 MOUNTING SPOTS: 3 PER SIDE, 2 ON THE BACK, 1 ON THE LID.",
                       "EACH SPOT IS 2 BLIND HOLES 28 APART; EACH ATTACHMENT HANGS ON 2 PEGS AND LATCHES. SEE TC-301."], **COMMON)
    top, front, right, _ = kit.three_views(fitted, iso=True)
    top.overall()
    front.overall()
    right.overall()
    return [ga, kit]


if __name__ == "__main__":
    travel_box_drawing()
