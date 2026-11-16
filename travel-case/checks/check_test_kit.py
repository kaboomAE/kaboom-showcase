"""The test kit: every piece one valid solid, pairs fit in place as in the case, the hinge swings, the plate holds it."""
import sys
sys.path.insert(0, "src")
from cadgen import build123d as bd
from cadgen import geometry as g
from cadgen import read_step
import travel_mount as tm
import travel_parts as tp
import travel_test_kit as kit
import travel_test_kit_rev_f as kitf
import travel_test_kit_rev_g as kitg


def ov(a, b):
    return sum(g.overlap_volume(x, y) for x in a.solids() for y in b.solids())


for name, shape, _ in (kit.hinge_pair() + kit.joint_pair() + kit.lid_pair() + kit.catch_pair()
                       + kit.iec_piece() + kit.gauge() + kit.logo_patch()
                       + kitf.hinge_foot() + kitf.m3_coupon() + kitf.magnet_check()
                       + kitg.wall_coupon() + kitg.lid_coupon() + kitg.plates()):
    bb = shape.bounding_box()
    print("%-26s solids %d valid %s  %5.1f x %5.1f x %5.1f  %5.1f cm3" % (
        name, len(shape.solids()), shape.is_valid, bb.size.X, bb.size.Y, bb.size.Z, shape.volume / 1000))

ax, ay = tp.hinge_axis(1)
zc = tp.hinge_centres("lower")[0]
floor = tp.rod_span()[0]
for label, pair, top, bolt in (("A", kit.hinge_pair(), zc + tp.HINGE_LEN / 2, 60), ("A F", kitf.hinge_foot(), zc, 30)):
    (_, corner, _), (_, edge, _) = pair
    hits = []
    for a in range(0, 181, 10):
        turned = edge.moved(bd.Location((ax, ay, 0)) * bd.Location((0, 0, 0), (0, 0, a)) * bd.Location((-ax, -ay, 0)))
        if ov(turned, corner) > 0.01:
            hits.append(a)
    print("hinge %s: door edge swings 0..180 against the shell corner: %s; an M3 x %d stopped on the floor (z %.1f)"
          " leaves its head %.1f above the pieces, %.1f of it in the %.1f hole" % (
              label, hits or "clear", bolt, floor, floor + bolt - top, tp.ROD_TAP_DEPTH, tp.ROD_TAP_D))

(_, lower, _), (_, upper, _) = kit.joint_pair()
print("joint: halves overlap %.3f, touch %s" % (ov(lower, upper), lower.distance_to(upper) < 1e-6))
(_, coupon, _), = kitg.wall_coupon()
(_, lidc, _), = kitg.lid_coupon()
for name, plate, _ in kitg.plates():
    rows = []
    for k, c in enumerate(tm.CLEARS):
        seated = plate.moved(bd.Location((0, -0.01, k * tm.PITCH)))
        entry = plate.moved(bd.Location((0, -0.01, k * tm.PITCH + tm.DROP)))
        rows.append("%.2f: seated %.3f, at the entries %.1f" % (c, ov(seated, coupon), ov(entry, coupon)))
    on_lid = tm.to_lid(plate).moved(bd.Location((0, -0.01, 0)))
    print("%s on the wall coupon (mm3 overlap; at the entries it is the bump, which the tongue lifts) %s; on the lid coupon %.3f" % (
        name, "; ".join(rows), ov(on_lid, lidc)))
(_, edge_d, _), (_, strip, _) = kit.lid_pair()
print("lid: strip in its slot overlaps %.3f, %.2f under the lip (lip underside %.1f above the piece's base: on a 0.2 layer %s);"
      " slides out the back: %s" % (
    ov(strip, edge_d), tp.LID_RISE, tp.LIP_Z0 - (tp.LID_Z0 - 18), abs(round((tp.LIP_Z0 - tp.LID_Z0 + 18) / 0.2) * 0.2 - (tp.LIP_Z0 - tp.LID_Z0 + 18)) < 1e-6,
    all(ov(strip.moved(bd.Location((0, d, 0))), edge_d) < 0.01 for d in range(0, 60, 5))))
print("gauge rows: " + "; ".join("%s %s" % (gr, "/".join("%g" % d for d in kit.gauge_sizes(gr))) for gr in kit.GAUGE))
(_, plinth, _), (_, bottom, _) = kit.catch_pair()
print("catch: door bottom over the plinth overlaps %.3f, gap %.2f" % (ov(plinth, bottom), plinth.distance_to(bottom)))
z0 = tp.DOOR_Z["lower"][0]
print("catch: E2 holds the whole bore (%.2f deep, the piece %.0f tall from the edge), its end %.1f below the piece's top" % (
    tp.CATCH_BORE_DEPTH, bottom.bounding_box().max.Z - z0, bottom.bounding_box().max.Z - z0 - tp.CATCH_BORE_DEPTH))

for name in ("travel_test_kit", "travel_test_kit_retest", "travel_test_kit_rev_f", "travel_test_kit_catch"):
    k = read_step(f"STEP/{name}.step")
    bb = k.bounding_box()
    print("%s plate: %d pieces over %.0f x %.0f mm, %.0f mm tall, %.0f cm3 of plastic" % (
        name, len(k.solids()), bb.size.X, bb.size.Y, bb.size.Z, sum(s.volume for s in k.solids()) / 1000))
