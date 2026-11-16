"""Does the owner's 82 x 55 Omni Dripper 2 holder stand in the lower right door's bin, on its lower shelf?"""
import sys
sys.path.insert(0, "src")
from cadgen import build123d as bd
from cadgen import geometry as g
import travel_parts as tp

R, HT = 41.0, 55.0
door = tp.tray(1, 0)
floor = tp.BIN_Z[0] + tp.BIN_WALL
shelf = tp.BIN_Z[0] + (tp.BIN_Z[1] - tp.BIN_Z[0]) / 2          # underside of the upper shelf
print("lower compartment clear height %.1f, holder %.1f" % (shelf - floor, HT))
best = None
for x in range(0, 50, 4):
    for y in range(-82, -40, 4):
        cup = tp._cyl(R + 0.5, "z", (x, y, 0), floor + 0.1, floor + HT).solids()[0]
        ov = sum(g.overlap_volume(cup, s) for s in door.solids())
        if ov < 0.01:
            # how much bin wall is round it: the gap to the door's solid
            gap = min(cup.distance_to(s) for s in door.solids())
            if best is None or gap > best[2]:
                best = (x, y, gap)
print("fits:", best is not None, "best centre and play:", best)
