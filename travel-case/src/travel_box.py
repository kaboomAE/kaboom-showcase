"""Printed brew-in-the-box travel case for the xBloom Studio, assembled with the machine in it.

Each printed part is turned from its print orientation back into place; a
see-through stand-in for the machine checks the fit. Geometry, dimensions and
colours live in travel_parts.py.
"""

from __future__ import annotations

import cadgen
from cadgen import build123d as bd
from cadgen import step

import travel_mount as tm
import travel_parts as tp
from travel_acc_bin import travel_acc_bin
from travel_acc_cord_wrap import travel_acc_cord_wrap
from travel_acc_dripper_ring import travel_acc_dripper_ring
from travel_acc_filter_holder import travel_acc_filter_holder
from travel_acc_top_tray import travel_acc_top_tray
from travel_door_lower_left import travel_door_lower_left
from travel_door_lower_right import travel_door_lower_right
from travel_door_upper_left import travel_door_upper_left
from travel_door_upper_right import travel_door_upper_right
from travel_handle import travel_handle
from travel_lid_back import travel_lid_back
from travel_lid_front import travel_lid_front
from travel_lower import travel_lower
from travel_tray_left_lower import travel_tray_left_lower
from travel_tray_left_upper import travel_tray_left_upper
from travel_tray_right_lower import travel_tray_right_lower
from travel_tray_right_upper import travel_tray_right_upper
from travel_upper import travel_upper

_L = (-tp.W / 2, tp.HINGE_Y, 0.0)
_R = (tp.W / 2, tp.HINGE_Y, 0.0)
_FACE_Y = -tp.D / 2 - tp.DOOR_T
KINEMATICS = {
    "mates": [
        cadgen.revolute("door_lower_left", parent="#lower", child="#door_lower_left",
                        origin=_L, direction=(0, 0, -1), limits=(0, 180)),
        cadgen.revolute("door_lower_right", parent="#lower", child="#door_lower_right",
                        origin=_R, direction=(0, 0, 1), limits=(0, 180)),
        cadgen.revolute("door_upper_left", parent="#upper", child="#door_upper_left",
                        origin=_L, direction=(0, 0, -1), limits=(0, 180)),
        cadgen.revolute("door_upper_right", parent="#upper", child="#door_upper_right",
                        origin=_R, direction=(0, 0, 1), limits=(0, 180)),
        cadgen.slider("lid_front", parent="#upper", child="#lid_front",
                      origin=(0, 0, 0), direction=(0, -1, 0), limits=(0, 130)),
        cadgen.slider("lid_back", parent="#upper", child="#lid_back",
                      origin=(0, 0, 0), direction=(0, 1, 0), limits=(0, 120)),
        cadgen.fastened("tray_on_lid", parent="#lid_back", child="#acc_top_tray"),
        # The lower doors' trays are screwed on, so they swing with their doors.
        *[cadgen.fastened(f"tray_{side}_{level}", parent=f"#door_lower_{side}", child=f"#tray_{side}_{level}")
          for side in ("left", "right") for level in ("lower", "upper")],
        # The machine's tank lifts straight up once the back lid panel is slid clear of it.
        cadgen.slider("tank", parent="#xbloom_studio", child="#water_tank",
                      origin=(0, 0, 0), direction=(0, 0, 1), limits=(0, 360)),
    ],
    "couplings": [cadgen.couple(
        "doors", {"door_lower_left": 1, "door_lower_right": 1, "door_upper_left": 1, "door_upper_right": 1},
        limits=(0, 180),
    )],
    "poses": {
        "packed": {"doors": 0, "lid_front": 0, "lid_back": 0, "tank": 0},
        "brewing": {"doors": 180, "lid_front": 60, "lid_back": 0, "tank": 0},
        "tank_out": {"doors": 0, "lid_front": 0, "lid_back": 110, "tank": 360},
        "unpacking": {"doors": 150, "lid_front": 130, "lid_back": 110, "tank": 0},
    },
}


def _like(child: bd.Shape, ref: bd.Shape, rotation: tuple[float, float, float]) -> bd.Shape:
    """Turn a printed child back by rotation and set it where its in-place reference is."""
    turned = child.moved(bd.Location((0, 0, 0), rotation))
    rb, tb = ref.bounding_box(), turned.bounding_box()
    return turned.moved(bd.Location((rb.min.X - tb.min.X, rb.min.Y - tb.min.Y, rb.min.Z - tb.min.Z)))


def _onto(printed: bd.Shape, local: bd.Shape, rot: tuple[float, float, float], loc: bd.Location) -> bd.Shape:
    """Undo an attachment's print orientation (one-axis rot) back to its local frame, then place it."""
    back = printed.moved(bd.Location((0, 0, 0), tuple(-a for a in rot)))
    pb, lb = back.bounding_box(), local.bounding_box()
    back = back.moved(bd.Location((lb.min.X - pb.min.X, lb.min.Y - pb.min.Y, lb.min.Z - pb.min.Z)))
    return back.moved(loc)


@step(
    out="../STEP/travel_box.step",
    kinematics=KINEMATICS,
    materials={
        "definitions": {"ghost": {"name": "Reference only", "baseColor": "#7A8590", "opacity": 0.3}},
        "assignments": [{"targets": ["#xbloom_studio_reference"], "material": "ghost"}],
    },
)
def travel_box():
    shell = tp.shell_pieces()
    up, door_rot = (0, 0, 0), (-90, 0, 0)
    placed = [
        ("lower", travel_lower(), shell["lower"], up),
        ("upper", travel_upper(), shell["upper"], up),
        ("lid_front", travel_lid_front(), tp.lid("front"), up),
        ("lid_back", travel_lid_back(), tp.lid("back"), up),
        ("door_lower_left", travel_door_lower_left(), tp.door(-1, "lower"), door_rot),
        ("door_lower_right", travel_door_lower_right(), tp.door(1, "lower"), door_rot),
        ("door_upper_left", travel_door_upper_left(), tp.door(-1, "upper"), door_rot),
        ("door_upper_right", travel_door_upper_right(), tp.door(1, "upper"), door_rot),
        ("handle", travel_handle(), tp.handle(), (-90, 0, 0)),
        ("tray_left_lower", travel_tray_left_lower(), tp.tray(-1, 0), up),
        ("tray_left_upper", travel_tray_left_upper(), tp.tray(-1, 1), up),
        ("tray_right_lower", travel_tray_right_lower(), tp.tray(1, 0), up),
        ("tray_right_upper", travel_tray_right_upper(), tp.tray(1, 1), up),
    ]
    parts: list[bd.Shape] = []
    for label, child, ref, rot in placed:
        p = _like(child, ref, rot)
        p.label = label
        parts.append(p)
    # Sample attachments on the mounting grid
    makers = {
        "travel_acc_bin": (travel_acc_bin, tm.bin_small),
        "travel_acc_filter_holder": (travel_acc_filter_holder, tm.filter_holder),
        "travel_acc_dripper_ring": (travel_acc_dripper_ring, tm.dripper_ring),
        "travel_acc_cord_wrap": (travel_acc_cord_wrap, tm.cord_wrap),
        "travel_acc_top_tray": (travel_acc_top_tray, tm.top_tray),
    }
    for i, (name, face, a, b) in enumerate(tm.SAMPLES):
        model, local = makers[name]
        acc = _onto(model(), local(), tm.PRINT_ROT[name], tm.place(face, a, b))
        acc.label = "acc_top_tray" if name == "travel_acc_top_tray" else f"acc_{face}_{i}"
        parts.append(acc)
    # The hinge rods (bought: M3 threaded rod), one per side through both doors' knuckles. Its
    # bottom 6 mm is drawn at the printed hole's 2.5: the thread it cuts there is the plastic's.
    r0, r1 = tp.rod_span()
    for side, s in (("left", -1), ("right", 1)):
        ax, ay = tp.hinge_axis(s)
        t = r0 + tp.ROD_TAP_DEPTH
        rod = tp._cyl(1.5, "z", (ax, ay, 0), t, r1) + tp._cyl(tp.ROD_TAP_D / 2, "z", (ax, ay, 0), r0, t + 0.01)
        rod.label = f"hinge_rod_{side}"
        rod.color = cadgen.srgb("#9AA0A6")
        parts.append(rod)
    parts.append(tp.machine_reference())
    return bd.Compound(children=parts, label="xbloom_travel_box")


if __name__ == "__main__":
    travel_box()
