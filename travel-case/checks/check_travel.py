import sys

sys.path.insert(0, "src")
from cadgen import build123d as bd
from cadgen import geometry as g
from cadgen import read_step

import travel_parts as tp

PIECES = ["travel_lower", "travel_upper", "travel_lid_front", "travel_lid_back",
          "travel_door_lower_left", "travel_door_lower_right", "travel_door_upper_left", "travel_door_upper_right",
          "travel_handle", "travel_tray_left_lower", "travel_tray_left_upper", "travel_tray_right_lower",
          "travel_tray_right_upper", "travel_acc_bin", "travel_acc_filter_holder", "travel_acc_dripper_ring", "travel_acc_cord_wrap", "travel_acc_top_tray"]


def overlap(a: bd.Shape, b: bd.Shape) -> float:
    return sum(g.overlap_volume(x, y) for x in a.solids() for y in b.solids())


def gap(a: bd.Shape, b: bd.Shape) -> float:
    return min(x.distance_to(y) for x in a.solids() for y in b.solids())


print("case %.0f x %.0f x %.1f (handle top %.0f); machine %.0f deep" % (
    tp.W, tp.D, tp.H, tp.handle().bounding_box().max.Z, tp.M_DEPTH))
total = 0.0
for name in PIECES:
    s = read_step(f"STEP/{name}.step")
    bb = s.bounding_box()
    v = sum(x.volume for x in s.solids()) / 1000
    total += v
    print("%-18s %5.1f x %5.1f x %5.1f  solids %d valid %s  %5.0f cm3  %s" % (
        name, bb.size.X, bb.size.Y, bb.size.Z, len(s.solids()), s.is_valid, v,
        "fits 256" if max(bb.size.X, bb.size.Y, bb.size.Z) <= 256 else "TOO BIG"))
print("solid volume of all prints %.0f cm3" % total)

asm = read_step("STEP/travel_box.step")
leaves = asm.solids()
bad = [(i, j, round(v, 2)) for i in range(len(leaves)) for j in range(i + 1, len(leaves))
       if (v := g.overlap_volume(leaves[i], leaves[j])) > 0.01]
print("assembly solids %d valid %s; shut, overlapping pairs: %s" % (len(leaves), asm.is_valid, bad))

shell = tp.shell_pieces()
machine = [c for c in tp.machine_reference().children if c.label == "xbloom_studio"][0]
doors = {(sd, t): tp.door(sd, t) if t == "upper" else bd.Compound(children=[tp.door(sd, t), tp.tray(sd, 0), tp.tray(sd, 1)])
         for sd in (1, -1) for t in ("lower", "upper")}
print("gap, upper doors to the buttons: %.1f mm" % min(gap(doors[(sd, "upper")], machine) for sd in (1, -1)))
print("gap, lower doors' bins to the machine: %.1f mm" % min(gap(doors[(sd, "lower")], machine) for sd in (1, -1)))
fixed = list(shell.values()) + [tp.handle(), tp.lid("back"), tp.lid("front").moved(bd.Location((0, -60, 0))), machine]


def swung(sd: int, t: str, ang: float) -> bd.Shape:
    ax, ay = tp.hinge_axis(sd)
    rot = bd.Location((ax, ay, 0)) * bd.Location((0, 0, 0), (0, 0, sd * ang)) * bd.Location((-ax, -ay, 0))
    return doors[(sd, t)].moved(rot)


# The left door of each pair opens first, then the right; uppers before lowers.
order = [((-1, "upper"), {}), ((1, "upper"), {(-1, "upper"): 115}),
         ((-1, "lower"), {(-1, "upper"): 115, (1, "upper"): 115}),
         ((1, "lower"), {(-1, "upper"): 115, (1, "upper"): 115, (-1, "lower"): 180})]
for (sd, t), opened in order:
    others = [swung(k[0], k[1], opened.get(k, 0)) for k in doors if k != (sd, t)]
    hits = [(a, round(overlap(swung(sd, t, a), f), 1)) for a in range(10, 181, 10) for f in fixed + others
            if overlap(swung(sd, t, a), f) > 0.01]
    print("door %s %s swing 10..180: %s" % (t, "right" if sd > 0 else "left", hits[:6] if hits else "clear"))
blocked = overlap(swung(1, "lower", 10), doors[(-1, "lower")]) > 0.01
print("lower right door blocked while the lower left is shut: %s" % blocked)

tank = [c for c in tp.machine_reference().children if c.label == "water_tank"][0]
lid_back = tp.lid("back").moved(bd.Location((0, 110, 0)))
hits = [dz for dz in range(0, 361, 20) for f in list(shell.values()) + [tp.handle(), tp.lid("front"), lid_back]
        if overlap(tank.moved(bd.Location((0, 0, dz))), f) > 0.01]
print("tank lifted 0..360 with the back panel slid 110: %s" % (hits if hits else "clear"))
