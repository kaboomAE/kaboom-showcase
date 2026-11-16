"""Rev F's hardware: plastic round every M3 insert, the hinge rod's foot, and the 20 magnet pockets. Built from the model."""
import sys

sys.path.insert(0, "src")
from cadgen import build123d as bd

import travel_parts as tp


def tube(mouth, into, r0, r1, a, b) -> bd.Shape:
    """A ring r0..r1 round an axis from `mouth` along `into`, from depth a to b (r0 = 0: a solid disc)."""
    d = bd.Vector(*into)
    loc = bd.Plane(origin=bd.Vector(*mouth) + d * a, z_dir=d).location
    al = (bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN)
    t = bd.Cylinder(r1, b - a, align=al)
    if r0:
        t = t - bd.Cylinder(r0, b - a, align=al)
    return t.moved(loc)


def filled(part, shape) -> float:
    return (part & shape).volume / shape.volume


shell = tp.shell_pieces()
pilots = [("joint band", shell["upper"], (x, y, tp.Z_SPLIT), (0, 0, 1)) for x, y in tp.joint_xy()]
pilots += [("handle leg", tp.handle(), (s * tp.W / 2, y, z), (s, 0, 0))
           for s in (1, -1) for y in tp.HANDLE_SCREW_Y for z in tp.HANDLE_SCREW_Z]
pilots += [("lower door back", tp.door(s, "lower"), (x, -tp.D / 2, z), (0, -1, 0))
           for s in (1, -1) for level in (0, 1) for x, z in tp._tray_screws(s, level)]
r, wall, lead = tp.INSERT_D / 2, tp.INSERT_WALL, tp.INSERT_LEAD
worst = {}
for where, part, mouth, into in pilots:
    # the knurls sit below the lead-in: from there to the pilot's end, 3 mm round it, and 3 mm past its end
    side = filled(part, tube(mouth, into, r + lead + 0.02, r + wall - 0.05, lead, tp.INSERT_DEPTH))
    end = filled(part, tube(mouth, into, 0, r, tp.INSERT_DEPTH + 0.02, tp.INSERT_DEPTH + wall - 0.05))
    hole = 1 - filled(part, tube(mouth, into, 0, r - 0.02, 0.05, tp.INSERT_DEPTH - 0.05))
    cone = 1 - filled(part, tube(mouth, into, r + 0.02, r + lead - 0.15, 0.02, 0.1))
    w = worst.setdefault(where, [0, 1.0, 1.0, 1.0, 1.0])
    w[0] += 1
    w[1:] = [min(w[1], side), min(w[2], end), min(w[3], hole), min(w[4], cone)]
for where, (n, side, end, hole, cone) in worst.items():
    print("M3 %-16s %2d pilots %.1f x %.1f: %.1f mm of plastic round them %s, past their end %s; pilot open %s, lead-in %s" % (
        where, n, tp.INSERT_D, tp.INSERT_DEPTH, wall, "yes" if side > 0.999 else "NO (%.3f)" % side,
        "yes" if end > 0.999 else "NO (%.3f)" % end, "yes" if hole > 0.999 else "NO", "yes" if cone > 0.999 else "NO"))
print("M3 inserts in the case: %d (Rev E 29: the hinge knuckles' two are gone)" % sum(w[0] for w in worst.values()))

# The hinge rod: standing on the lowest knuckle's floor, screwed into its printed hole, its top under the lid.
r0, r1 = tp.rod_span()
lid = tp.lid("front")
for s in (1, -1):
    ax, ay = tp.hinge_axis(s)
    lower = shell["lower"]
    floor = filled(lower, tp._cyl(tp.ROD_TAP_D / 2, "z", (ax, ay, 0), r0 - tp.HINGE_FLOOR + 0.02, r0 - 0.02))
    tap = 1 - filled(lower, tp._cyl(tp.ROD_TAP_D / 2 - 0.02, "z", (ax, ay, 0), r0 + 0.02, r0 + tp.ROD_TAP_DEPTH - 0.02))
    grip = filled(lower, tp._cyl(1.5, "z", (ax, ay, 0), r0 + 0.02, r0 + tp.ROD_TAP_DEPTH - 0.5)
                  - tp._cyl(tp.ROD_TAP_D / 2 + 0.02, "z", (ax, ay, 0), r0, r0 + tp.ROD_TAP_DEPTH))
    clear = all(1 - filled(p, tp._cyl(1.5, "z", (ax, ay, 0), r0 + tp.ROD_TAP_DEPTH + 0.5, r1)) > 0.999 for p in shell.values())
    end = tp._cyl(1.5, "z", (ax, ay, 0), tp.LID_Z0, tp.LID_Z0 + 0.5)
    print("hinge rod %s: %.1f long, on a %.1f floor (solid %s), in a %.1f x %.1f printed hole (open %s; the rod's thread "
          "bites it all round %s), free in the 3.3 bore above %s; its end %.1f under the lid, which covers %.0f %% of it" % (
              "right" if s > 0 else "left", r1 - r0, tp.HINGE_FLOOR, floor > 0.999, tp.ROD_TAP_D, tp.ROD_TAP_DEPTH,
              tap > 0.999, grip > 0.999, clear, tp.LID_Z0 - r1, 100 * filled(lid, end)))

# Magnet pockets: every 6 x 2 pocket at the gauge's 5.8.
parts = {"lower": shell["lower"], "upper": shell["upper"], "lid front": tp.lid("front"), "lid back": tp.lid("back")}
parts.update({"door %s %s" % (t, "right" if s > 0 else "left"): tp.door(s, t) for s in (1, -1) for t in ("lower", "upper")})
count, sizes = 0, set()
for name, p in parts.items():
    for f in p.faces():
        if f.geom_type == bd.GeomType.CYLINDER and f.radius and abs(f.radius - 2.9) < 0.15 and abs(f.radius - tp.CATCH_SEAT_D / 2) > 0.01:
            count += 1
            sizes.add(round(2 * f.radius, 2))
print("magnet pockets: %d, diameters %s, %.1f deep" % (count, sorted(sizes), tp.MAG_DEPTH))
