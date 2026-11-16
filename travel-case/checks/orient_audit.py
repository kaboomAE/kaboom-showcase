"""For each printed part, the overhang area (steeper than 45 degrees, off the bed) in six orientations.

Measured on the tessellated surface, so curved walls count properly. Small bridges (holes, logo
recesses) still count, so compare orientations against each other rather than against zero.
"""
import sys
sys.path.insert(0, "src")
import math
from cadgen import build123d as bd
import travel_parts as tp
import travel_mount as tm

PARTS = {
    "lower door L": lambda: tp.door(-1, "lower"),
    "lower door R": lambda: tp.door(1, "lower"),
    "acc bin": tm.bin_small,
    "acc filter": tm.filter_holder,
    "acc dripper ring": tm.dripper_ring,
    "acc cord wrap": tm.cord_wrap,
    "acc top tray": tm.top_tray,
}
ORIENT = {"as built (z up)": (0, 0, 0), "upside down": (180, 0, 0), "X+90": (90, 0, 0), "X-90": (-90, 0, 0),
          "Y+90": (0, 90, 0), "Y-90": (0, -90, 0)}
COS45 = math.cos(math.radians(45))


def overhang(shape: bd.Shape) -> float:
    verts, tris = shape.tessellate(0.2, 0.3)
    z0 = min(v.Z for v in verts)
    total = 0.0
    for a, b, c in tris:
        p, q, r = verts[a], verts[b], verts[c]
        n = (q - p).cross(r - p)
        area = n.length / 2
        if area == 0:
            continue
        nz = n.Z / n.length
        if nz < -COS45 and min(p.Z, q.Z, r.Z) - z0 > 0.4:
            total += area
    return total


for name, make in PARTS.items():
    part = make()
    row = []
    for label, rot in ORIENT.items():
        row.append((overhang(part.moved(bd.Location((0, 0, 0), rot))), label))
    row.sort()
    print("%-17s best: %s" % (name, ", ".join("%s %.0f" % (l, a) for a, l in row[:3])), "| worst %.0f" % row[-1][0])
