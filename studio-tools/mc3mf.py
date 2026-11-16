"""A multi-colour 3MF: one object whose parts each name their filament, the way Bambu Studio,
OrcaSlicer and Snapmaker Orca save them, so the file opens with its colours already assigned.

    write(path, name, parts, colours, printer, material, settings=None)

parts: [(part name, shape, filament number from 1)], shapes being build123d shapes in place;
colours: the filaments' hex colours, in filament order; printer: the printer's slice block in
printers/printers.yaml (its presets, and 'project': the application tag, model and bed size the
file opens with). Orca needs the project settings and the plate block to keep the parts'
filaments: without them its command line crashes or puts everything on filament 1. settings:
slicer settings for this object only ({"wall_loops": 4}), saved the way Orca saves an object's own.

At most MAX_FILAMENTS colours in one print (the owner's rule, 2026-10-30: the U1 has 4 toolheads, the
X1C one 4-slot AMS): write() refuses more. colours_in(path) reads what a 3MF prints in, over_limit(folder)
lists the files past it.
"""

from __future__ import annotations

import json
import re
import uuid
import zipfile
from pathlib import Path
from xml.sax.saxutils import escape, quoteattr

MAX_FILAMENTS = 4
TOL, ANGLE = 0.002, 0.05     # tessellation: chord in mm, angle in radians (a 6.01 pocket measures 6.01)
NS = ('xmlns="http://schemas.microsoft.com/3dmanufacturing/core/2015/02" '
      'xmlns:p="http://schemas.microsoft.com/3dmanufacturing/production/2015/06" requiredextensions="p"')
CONTENT_TYPES = ('<?xml version="1.0" encoding="UTF-8"?>\n<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
                 '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
                 '<Default Extension="model" ContentType="application/vnd.ms-package.3dmanufacturing-3dmodel+xml"/>'
                 '<Default Extension="config" ContentType="text/xml"/></Types>')
RELS = ('<?xml version="1.0" encoding="UTF-8"?>\n<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        '<Relationship Target="{target}" Id="rel-1" Type="http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel"/></Relationships>')
PLATE = ('  <plate>\n    <metadata key="plater_id" value="1"/>\n    <model_instance>\n'
         '      <metadata key="object_id" value="1"/>\n      <metadata key="instance_id" value="0"/>\n'
         '    </model_instance>\n  </plate>\n  <assemble>\n'
         '    <assemble_item object_id="1" instance_id="0" offset="0 0 0"/>\n  </assemble>\n')


def mesh(shape) -> tuple[list[tuple[float, float, float]], list[tuple[int, int, int]]]:
    """Triangles of a shape with shared corners merged, so each body is one closed mesh."""
    verts, tris = shape.tessellate(TOL, ANGLE)
    index: dict[tuple, int] = {}
    out_v: list[tuple[float, float, float]] = []
    remap = []
    for v in verts:
        key = (round(v.X, 4), round(v.Y, 4), round(v.Z, 4))
        if key not in index:
            index[key] = len(out_v)
            out_v.append(key)
        remap.append(index[key])
    out_t = []
    for a, b, c in tris:
        a, b, c = remap[a], remap[b], remap[c]
        if a != b and b != c and a != c:
            out_t.append((a, b, c))
    return out_v, out_t


def write(path: str | Path, name: str, parts: list[tuple[str, object, int]], colours: list[str],
          printer: dict, material: str = "PLA", settings: dict | None = None) -> Path:
    if len(colours) > MAX_FILAMENTS:
        raise ValueError(f"{name}: this print needs {len(colours)} colours and one print takes at most {MAX_FILAMENTS} "
                         f"({', '.join(colours)}): merge some or split it into separate prints")
    path = Path(path)
    proj = printer["project"]
    bed_w, bed_d = (float(v) for v in proj["bed"].split("x"))
    objects, settings_parts, components = [], [], []
    for n, (part, shape, filament) in enumerate(parts, start=2):
        v, t = mesh(shape)
        vs = "".join(f'<vertex x="{x:g}" y="{y:g}" z="{z:g}"/>' for x, y, z in v)
        ts = "".join(f'<triangle v1="{a}" v2="{b}" v3="{c}"/>' for a, b, c in t)
        objects.append(f'<object id="{n}" p:UUID="{uuid.uuid4()}" type="model"><mesh><vertices>{vs}</vertices>'
                       f'<triangles>{ts}</triangles></mesh></object>')
        components.append(f'<component p:path="/3D/Objects/object_1.model" objectid="{n}" p:UUID="{uuid.uuid4()}"/>')
        settings_parts.append(f'    <part id="{n}" subtype="normal_part">\n'
                              f'      <metadata key="name" value={quoteattr(part)}/>\n'
                              f'      <metadata key="extruder" value="{filament}"/>\n    </part>\n')
    objects_model = (f'<?xml version="1.0" encoding="UTF-8"?>\n<model unit="millimeter" xml:lang="en-US" {NS}>'
                     f'<resources>{"".join(objects)}</resources><build/></model>')
    root_model = (f'<?xml version="1.0" encoding="UTF-8"?>\n<model unit="millimeter" xml:lang="en-US" {NS}>\n'
                  f' <metadata name="Application">{proj["application"]}</metadata>\n'
                  f' <metadata name="Title">{escape(name)}</metadata>\n'
                  f' <metadata name="Designer">KABOOM Studio</metadata>\n'
                  f' <resources>\n  <object id="1" p:UUID="{uuid.uuid4()}" type="model"><components>{"".join(components)}'
                  f'</components></object>\n </resources>\n'
                  f' <build p:UUID="{uuid.uuid4()}"><item objectid="1" p:UUID="{uuid.uuid4()}" '
                  f'transform="1 0 0 0 1 0 0 0 1 {bed_w / 2:g} {bed_d / 2:g} 0" printable="1"/></build>\n</model>')
    settings = ('<?xml version="1.0" encoding="UTF-8"?>\n<config>\n  <object id="1">\n'
                f'    <metadata key="name" value={quoteattr(name)}/>\n    <metadata key="extruder" value="1"/>\n'
                + "".join(f'    <metadata key={quoteattr(str(k))} value={quoteattr(str(v))}/>\n' for k, v in (settings or {}).items())
                + "".join(settings_parts) + "  </object>\n" + PLATE + "</config>\n")
    n = len(colours)
    project = {
        "printable_area": ["0x0", f"{bed_w:g}x0", f"{bed_w:g}x{bed_d:g}", f"0x{bed_d:g}"], "printable_height": proj["height"],
        "bed_exclude_area": [], "printer_settings_id": printer["printer"], "print_settings_id": printer["process"],
        "printer_model": proj["model"], "printer_variant": "0.4", "nozzle_diameter": ["0.4"],
        "filament_colour": colours, "filament_settings_id": [printer["filament"][material]] * n,
        "filament_diameter": ["1.75"] * n, "filament_is_support": ["0"] * n,
    }
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", CONTENT_TYPES)
        z.writestr("_rels/.rels", RELS.format(target="/3D/3dmodel.model"))
        z.writestr("3D/3dmodel.model", root_model)
        z.writestr("3D/_rels/3dmodel.model.rels", RELS.format(target="/3D/Objects/object_1.model"))
        z.writestr("3D/Objects/object_1.model", objects_model)
        z.writestr("Metadata/model_settings.config", settings)
        z.writestr("Metadata/project_settings.config", json.dumps(project, indent=1))
    return path


def colours_in(path: str | Path) -> list[str]:
    """The different colours a 3MF's parts print in, from its project settings and each part's
    extruder (a file that lists more filaments than its parts use counts what they use). A slicer's
    colour painting on one body isn't read."""
    with zipfile.ZipFile(path) as z:
        names = set(z.namelist())
        if "Metadata/project_settings.config" not in names or "Metadata/model_settings.config" not in names:
            return []
        colours = json.loads(z.read("Metadata/project_settings.config")).get("filament_colour") or []
        used = {int(e) for e in re.findall(r'key="extruder"\s+value="(\d+)"', z.read("Metadata/model_settings.config").decode("utf-8", "replace"))}
    return sorted({str(colours[e - 1]).upper() if 0 < e <= len(colours) else f"filament {e}" for e in used})


def over_limit(folder: str | Path) -> list[tuple[Path, list[str]]]:
    """Every 3MF under a folder past MAX_FILAMENTS colours, with its colours (a sliced .gcode.3mf is
    the same print as its model, so it isn't read)."""
    out = []
    for f in sorted(Path(folder).rglob("*.3mf")):
        if f.name.endswith(".gcode.3mf") or ".cache" in f.parts:
            continue
        try:
            cols = colours_in(f)
        except (OSError, ValueError, zipfile.BadZipFile):
            continue
        if len(cols) > MAX_FILAMENTS:
            out.append((f, cols))
    return out
