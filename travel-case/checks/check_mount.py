"""The pegboard: holes blind and clear of everything, pegs that go in, drop, hold and latch, attachments on seats, doors clear."""
import sys
sys.path.insert(0, "src")
from cadgen import build123d as bd
from cadgen import geometry as g
from cadgen import read_step
import travel_mount as tm
import travel_parts as tp


def ov(a, b):
    return sum(g.overlap_volume(x, y) for x in a.solids() for y in b.solids())


def at(shape, dx=0.0, dy=0.0, dz=0.0):
    return shape.moved(bd.Location((dx, dy, dz)))


# --- the spots -----------------------------------------------------------------
counts = {f: len(tm.holes(f)) for f in ("right", "left", "back")}
lids = {h: len(tm.holes("top", h)) for h in ("front", "back")}
print("%d mounting spots: %s" % (len(tm.SPOTS), ", ".join(tm.SPOTS)))
print("holes: right %(right)d, left %(left)d, back %(back)d" % counts, "| lid front %(front)d, back %(back)d" % lids,
      "| %d in all" % (sum(counts.values()) + sum(lids.values())))
print("each hole %.1f wide, %.1f tall (%.1f under its seat, %.1f over), %.1f deep: %.1f of the %.0f wall behind it (rule 1.9)" % (
    2 * tm.HOLE_HALF, tm.HOLE_BELOW + tm.HOLE_ABOVE, tm.HOLE_BELOW, tm.HOLE_ABOVE, tm.HOLE_DEPTH, tp.WALL - tm.HOLE_DEPTH, tp.WALL))
seam = min(min(abs(b - tm.HOLE_BELOW - tp.Z_SPLIT), abs(b + tm.HOLE_ABOVE - tp.Z_SPLIT)) for f in counts for _, b in tm.holes(f))
print("closest hole edge to the seam: %.1f mm; every hole clear of the seam, handle and inlet zones: %s" % (
    seam, all(tm._clear_of_everything(f, a, b) for f in counts for a, b in tm.holes(f))))

# Every hole blind: nothing reaches within 1.9 of the inside, and none touches another cut.
inner = tp._plan_rounded_back(-tp.IN_W / 2, tp.IN_W / 2, -tp.D / 2 - 1, tp.D / 2 - tp.WALL, tp.BACK_R_IN, tp.FLOOR, tp.H + 1)
others = [tp._box(tp.IEC_X - tp.IEC_CUT[0] / 2, tp.IEC_X + tp.IEC_CUT[0] / 2, tp.D / 2 - tp.WALL - 1, tp.D / 2 + 1,
                  tp.IEC_Z - tp.IEC_CUT[1] / 2, tp.IEC_Z + tp.IEC_CUT[1] / 2)]
others += [tp._cyl(tp.CLEAR_D / 2, "y", (tp.IEC_X + dx, 0, tp.IEC_Z), 0, tp.D) for dx in (-tp.IEC_SCREW_PITCH / 2, tp.IEC_SCREW_PITCH / 2)]
others += [tp._cyl(tp.CLEAR_D / 2, "x", (0, y, z), -tp.W, tp.W) for y in tp.HANDLE_SCREW_Y for z in tp.HANDLE_SCREW_Z]
handle = tp.handle()
behind, near, legs = [], [], []
for f in counts:
    for tool in tm.grid_cuts(f):
        behind.append(tool.distance_to(inner))
        near.append(min(tool.distance_to(o) for o in others))
        legs.append(tool.distance_to(handle))
print("wall holes: least wall behind %.2f; nearest other cut (IEC, its screws, handle screws) %.1f; handle legs %.1f" % (
    min(behind), min(near), min(legs)))
mag_r = tp.MAG_D / 2
lid_mags = [tp._cyl(mag_r, "z", (s * (tp.IN_W / 2 - tp.RAIL_W / 2), y, 0), tp.LID_Z0 - 1, tp.LID_Z0 + tp.MAG_DEPTH)
            for s in (1, -1) for y in (-70.0, 70.0)]
lip_x = tp.IN_W / 2 - 5.0
lid_tools = [t for h in ("front", "back") for t in tm.grid_cuts("top", h)]
print("lid holes (the tray spot): deepest leaves %.2f under them; nearest magnet pocket %.1f; widest reach |x| %.1f under the shell's lips from %.1f" % (
    tp.LID_T - tm.HOLE_DEPTH, min(t.distance_to(m) for t in lid_tools for m in lid_mags),
    max(max(abs(t.bounding_box().min.X), abs(t.bounding_box().max.X)) for t in lid_tools), lip_x))

# --- one hole and one peg, in a piece of wall ------------------------------------
wall = tp._box(-30, 30, 0, tp.WALL, -40, 60) - tm.hole_tool()
peg = tm.peg()
print("peg into the entry: overlap %.3f; on the way down: %s; seated: %.3f, %.2f clear" % (
    ov(at(peg, dy=-0.01, dz=tm.DROP), wall), max(ov(at(peg, dy=-0.01, dz=tm.DROP - d), wall) for d in range(1, 9)),
    ov(at(peg, dy=-0.01), wall), at(peg, dy=-0.01).distance_to(wall)))
pull = next(d / 100 for d in range(1, 200) if ov(at(peg, dy=-d / 100), wall) > 0.01)
print("seated, the head meets the lip's back after pulling out %.2f; the lip holds each ear %.1f wide (%.1f with clearance)" % (
    pull, tm.R - tm.NECK, tm.R - tm.NECK - tm.CLEAR))


def free(lift):
    """Whether a seated peg lifted by `lift` comes straight out."""
    return all(ov(at(peg, dy=-k / 4, dz=lift), wall) < 0.01 for k in range(0, 17))


unlock = next(l / 10 for l in range(0, 100) if free(l / 10))
for c in tm.CLEARS:
    w = tp._box(-30, 30, 0, tp.WALL, -40, 60) - tm.hole_tool(c)
    print("  clearance %.2f: seated overlap %.3f, gap %.2f; enters %.3f" % (
        c, ov(at(peg, dy=-0.01), w), at(peg, dy=-0.01).distance_to(w), ov(at(peg, dy=-0.01, dz=tm.DROP), w)))

# --- the latch ------------------------------------------------------------------
plate = tm._plate(-20, 20, -12, tm._latch_top(0)) + tm._pegs((0, 0))
for catch in ("latch", "click"):
    p = tm.with_latch(plate, 0, 0, catch)
    seated, going_on = ov(at(p, dy=-0.01), wall), ov(at(p, dy=-0.01, dz=tm.DROP), wall)
    lift = next(l / 100 for l in range(1, 300) if ov(at(p, dy=-0.01, dz=l / 100), wall) > 0.01)
    t = tm.TONGUE_T[catch]
    for name, e in (("PLA", 3500.0), ("ASA", 2200.0)):
        k = 3 * e * (tm.TONGUE_W * t ** 3 / 12) / (tm.TONGUE_L - tm.BUMP_UP) ** 3
        strain = 1.5 * t * tm.BUMP_H / (tm.TONGUE_L - tm.BUMP_UP) ** 2
        if name == "ASA":
            print("%s: seated overlap %.3f; pushed on at the entries the bump stands %.3f mm3 into the wall (the tongue bends %.1f, "
                  "%s %.1f N, strain %.1f%%); lifts %.2f before the bump bears, %.1f short of the %.1f that frees the peg" % (
                      catch, seated, going_on, tm.BUMP_H, name, k * tm.BUMP_H, 100 * strain, lift, unlock - lift, unlock))

# --- the attachments: pegs on seats, nothing overlaps, doors clear ----------------
makers = {"travel_acc_bin": tm.bin_small, "travel_acc_filter_holder": tm.filter_holder, "travel_acc_dripper_ring": tm.dripper_ring,
          "travel_acc_cord_wrap": tm.cord_wrap, "travel_acc_top_tray": tm.top_tray}
for name, face, a, b in tm.SAMPLES:
    loc = tm.frame(face, a, b)
    spots = [s.position for s in tm.seats(face, "back" if face == "top" else None)]
    hits = []
    for u, v in tm.PEGS[name]:
        pos = (loc * bd.Location((u, 0, v))).position
        hits.append(min((pos - s).length for s in spots))
    print("%-25s on %-5s: pegs %.2f from their seats" % (name, face, max(hits)))

asm = read_step("STEP/travel_box.step")
leaves = asm.solids()
bad = [(i, j, round(v, 2)) for i in range(len(leaves)) for j in range(i + 1, len(leaves))
       if (v := g.overlap_volume(leaves[i], leaves[j])) > 0.01]
print("assembly solids %d valid %s; overlapping pairs: %s" % (len(leaves), asm.is_valid, bad))

accs = [makers[n]().moved(tm.place(f, a, b)) for n, f, a, b in tm.SAMPLES if f != "top"]
for s in (1, -1):
    for t in ("lower", "upper"):
        ax, ay = tp.hinge_axis(s)
        hits = set()
        for ang in range(10, 181, 10):
            d = tp.door(s, t).moved(bd.Location((ax, ay, 0)) * bd.Location((0, 0, 0), (0, 0, s * ang)) * bd.Location((-ax, -ay, 0)))
            for a in accs:
                if sum(g.overlap_volume(x, y) for x in d.solids() for y in a.solids()) > 0.01:
                    hits.add(ang)
        print("door %s %s vs attachments: %s" % (t, "right" if s > 0 else "left", sorted(hits) or "clear"))
tray = tm.top_tray().moved(tm.place("top", 0.0, 2 * tm.PITCH))
lid = tp.lid("back")
print("top tray on the back lid: overlap %.3f; slid back with the lid for the tank, it rides along (a fastened mate)" % ov(tray, lid))

# --- which attachment fits which spot: each wall attachment on each wall spot ------------
shell = tp.shell_pieces()
static = [handle, shell["lower"], shell["upper"], tp.lid("front"), tp.lid("back")]
doors = []
for s in (1, -1):
    for t in ("lower", "upper"):
        ax, ay = tp.hinge_axis(s)
        for ang in range(0, 181, 15):
            doors.append(tp.door(s, t).moved(bd.Location((ax, ay, 0)) * bd.Location((0, 0, 0), (0, 0, s * ang)) * bd.Location((-ax, -ay, 0))))
wall_spots = {k: v for k, v in tm.SPOTS.items() if v[0] != "top"}
for name, make in makers.items():
    if name == "travel_acc_top_tray":
        continue
    shape, ok = make(), []
    for spot, (face, a, b) in wall_spots.items():
        placed = shape.moved(tm.place(face, a, b))
        bb = placed.bounding_box()
        hit = any(ov(placed, o) > 0.01 for o in static) or any(
            ov(placed, d) > 0.01 for d in doors if d.bounding_box().max.Z > bb.min.Z and d.bounding_box().min.Z < bb.max.Z)
        # It must also stay on its face's flat (clear of the doors' edge and the back corners) and off the power inlet.
        if face == "back":
            hit = hit or bb.min.X < -tp.W / 2 + tp.BACK_R or bb.max.X > tp.W / 2 - tp.BACK_R or (
                bb.max.X > tp.IEC_X - tp.IEC_CUT[0] / 2 and bb.min.X < tp.IEC_X + tp.IEC_CUT[0] / 2 and bb.min.Z < tp.IEC_Z + tp.IEC_CUT[1] / 2)
        else:
            hit = hit or bb.min.Y < -tp.D / 2 + 22.0 or bb.max.Y > tp.D / 2 - tp.BACK_R
        if not hit:
            ok.append(spot)
    print("%-25s fits %d of %d wall spots: %s" % (name, len(ok), len(wall_spots), ", ".join(ok)))
