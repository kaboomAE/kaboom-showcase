"""Can the back lid panel slide all the way off the back, for full access to the tank from above?"""
import sys
sys.path.insert(0, "src")
from cadgen import build123d as bd
from cadgen import geometry as g
import travel_parts as tp

fixed = list(tp.shell_pieces().values()) + [tp.handle()]
lid = tp.lid("back")
hits = []
for dy in range(0, 131, 10):
    moved = lid.moved(bd.Location((0, dy, 0)))
    v = sum(g.overlap_volume(a, b) for a in moved.solids() for f in fixed for b in f.solids())
    if v > 0.01:
        hits.append((dy, round(v, 2)))
print("back panel slid 0..130 (off the back at %.1f): %s" % (tp.D / 2 - tp.LID_GAP / 2, hits or "clear"))
print("gap behind the machine, for fingers: %.1f mm" % (tp.D / 2 - tp.WALL - tp.M_BACK_Y))
