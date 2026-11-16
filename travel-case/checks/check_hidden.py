import sys
sys.path.insert(0, "src")
from cadgen import build123d as bd
import travel_parts as tp

def outside_holes(part, normal, plane_coord, axis):
    """Holes in the outside face(s) lying on a plane: count inner wires."""
    n = 0
    for f in part.faces():
        if f.geom_type != bd.GeomType.PLANE:
            continue
        c = f.center()
        if abs(f.normal_at() .dot(bd.Vector(*normal)) - 1) < 1e-6 and abs(getattr(c, axis) - plane_coord) < 0.01:
            n += len(f.inner_wires())
    return n

front = -tp.D / 2 - tp.DOOR_T
for s in (1, -1):
    for t in ("lower", "upper"):
        d = tp.door(s, t)
        print("door %s %s: holes in its front face %d" % (t, "right" if s > 0 else "left", outside_holes(d, (0, -1, 0), front, "Y")))
lid = tp.lid("front")
print("front lid: holes in its top face %d" % outside_holes(lid, (0, 0, 1), tp.LID_Z0 + tp.LID_T, "Z"))
print("skins: door edge pockets %.1f mm each side; door back pockets leave %.1f mm to the front; lid pockets leave %.1f mm on top" % (
    (tp.DOOR_T - tp.EDGE_MAG_D) / 2, tp.DOOR_T - tp.MAG_DEPTH, tp.LID_T - tp.EDGE_MAG_DEPTH))

# The lower doors' catches: the plunger bore stays inside the door, and lines up with its seat in the plinth.
plinth_top = tp.FLOOR
for s in (1, -1):
    d = tp.door(s, "lower")
    z0 = tp.DOOR_Z["lower"][0]
    print("lower door %s: catch bore skins %.1f mm front and back; door bottom %.1f above the plinth; seat under the bore: %s" % (
        "right" if s > 0 else "left", (tp.DOOR_T - tp.CATCH_INSERT_D) / 2, z0 - plinth_top,
        abs(tp.HINGE_Y - (-tp.D / 2 - tp.DOOR_T / 2)) < 1e-9))
lower = tp.shell_pieces()["lower"]
seat = [f for f in lower.faces() if f.geom_type == bd.GeomType.CYLINDER and f.radius is not None and abs(f.radius - tp.CATCH_SEAT_D / 2) < 1e-6]
print("catch seats found in the plinth: %d" % len(seat))

# The plunger's stop: screwed fully home it meets the hole's flat end, ball CATCH_BALL_PROUD below the edge.
for s in (1, -1):
    d = tp.door(s, "lower")
    z0 = tp.DOOR_Z["lower"][0]
    end = [f for f in d.faces() if f.geom_type == bd.GeomType.PLANE and abs(f.center().Z - (z0 + tp.CATCH_BORE_DEPTH)) < 1e-6
           and abs(f.center().X - s * tp.CATCH_X) < 0.01]
    relief = [f for f in d.faces() if f.geom_type == bd.GeomType.CYLINDER and f.radius is not None
              and abs(f.radius - tp.CATCH_RELIEF_D / 2) < 1e-6]
    tip = z0 + tp.CATCH_BORE_DEPTH - tp.CATCH_PLUNGER_L
    print("lower door %s: bore's flat end %.2f above the edge (found %d, area %.1f mm2, a 5 mm plunger's end %.1f);"
          " relief %.1f x %.1f found %d, skins %.1f; ball tip %.2f below the edge, %.2f below the plinth top"
          " (seat %.1f deep)" % (
              "right" if s > 0 else "left", tp.CATCH_BORE_DEPTH, len(end), sum(f.area for f in end), 3.14159 * 2.5 ** 2,
              tp.CATCH_RELIEF_D, tp.CATCH_RELIEF_L, len(relief), (tp.DOOR_T - tp.CATCH_RELIEF_D) / 2,
              z0 - tip, tp.FLOOR - tip, tp.CATCH_SEAT_DEPTH))
