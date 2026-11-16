"""ASA needed per colour group, from each print file's solid volume and how full it prints.

Fill fractions follow the README settings (0.2 mm, 20 % gyroid; 5 walls on the shells, 6 on
the doors and handle, 4 elsewhere): thick shell walls and plates print mostly solid, the 10 mm
doors about two-thirds, thin trays and attachments nearly solid. ASA is about 1.07 g/cm3.
"""
from cadgen import read_step

ASA = 1.07
GROUPS = {
    "shell": {"travel_lower": 0.72, "travel_upper": 0.72, "travel_lid_front": 0.6, "travel_lid_back": 0.6},
    "doors": {"travel_door_upper_left": 0.65, "travel_door_upper_right": 0.65, "travel_door_lower_left": 0.65,
              "travel_door_lower_right": 0.65, "travel_tray_left_lower": 0.95, "travel_tray_left_upper": 0.95,
              "travel_tray_right_lower": 0.95, "travel_tray_right_upper": 0.95},
    "accent": {"travel_handle": 0.8, "travel_acc_bin": 0.95, "travel_acc_filter_holder": 0.95,
               "travel_acc_dripper_ring": 0.95, "travel_acc_cord_wrap": 0.95, "travel_acc_top_tray": 0.95},
}
COUNT = {"travel_acc_bin": 2}
total = 0.0
for group, parts in GROUPS.items():
    grams = 0.0
    for name, fill in parts.items():
        v = sum(s.volume for s in read_step(f"STEP/{name}.step").solids()) / 1000
        grams += v * fill * ASA * COUNT.get(name, 1)
    grams *= 1.05                                   # brims, purge, a failed first layer
    total += grams
    print("%-7s %5.0f g" % (group, grams))
print("total   %5.0f g" % total)
