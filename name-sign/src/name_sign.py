"""The sample name sign ('Saeed', on the owner's MakerWorld sign's plate) as STEP and STL, from its layout.

tools/make_signs.py --sample writes src/sample_layout.json (the shaped text needs fontTools and
HarfBuzz, so it is laid out there) and the multi-colour 3MF/name_sign.3mf; this model builds the
same bodies for the drawing, the checks and the project page.
"""

from pathlib import Path

import cadgen
from cadgen import build123d as bd
from cadgen import step, stl

import sign_parts as sp

LAYOUT = Path(__file__).parent / "sample_layout.json"


@stl(out="../STL/name_sign.stl")
@step(out="../STEP/name_sign.step")
def name_sign():
    layout = sp.load(LAYOUT)
    children = []
    for part, shape in sp.sign(layout).items():
        for i, solid in enumerate(shape.solids()):
            solid.label = part if len(shape.solids()) == 1 else f"{part}_{i}"
            solid.color = cadgen.srgb(layout["colours"][part])
            children.append(solid)
    return bd.Compound(children=children, label="name_sign")


if __name__ == "__main__":
    name_sign()
