# Cubware CAD catalog

The website's recursive catalog is `catalog.json`; preview meshes live in
`catalog/`. It covers all nested CAD entries in the local Cubware checkout,
including STEP-only parts and separate revisions. Files with the same folder
and stem are companions in one entry. Byte-identical preview assets share a
file, but their source entries remain separately discoverable.

Current inventory: 209 CAD source files, 139 entries, 129 preview STL assets.
Two FreeCAD backup files are recorded separately as excluded. Slicer files and
native FreeCAD documents are recorded as companions to their matching parts.

To refresh from the website directory:

```sh
python3 scripts/sync-cubware-cad.py --cubware ../../Cubware
python3 scripts/check-cad-catalog.py --cubware ../../Cubware
```

STEP conversion uses the installed FreeCAD Python runtime on macOS; override
its path with `FREECAD_PYTHON` when needed. Cubware is read-only. The sync script
rebuilds the generated `catalog/` folder. Review any reported conversion failures
before publishing; the coverage check fails if any primary source was omitted.

The viewer retains prototype, enclosure mockup, and reference-only notices
from the source READMEs. Preview meshes do not establish physical compatibility
or fabrication readiness. Original source paths are preserved in every entry.
