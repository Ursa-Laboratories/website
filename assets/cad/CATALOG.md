# Cubware parts library

Browse [the parts library](../../cubware.html) to search the complete snapshot,
filter by configuration, category or file format, and inspect each part in 3D.
The smaller viewer remains on [Build It](../../build.html#build-cad).

Select a part and use **Copy link** to share it. Drag to rotate, scroll to zoom,
or right-drag to pan. The Iso, Top, Front and Side controls set standard views.
With the canvas focused, use arrow keys to rotate and + / - to zoom.
**Reset** restores the solid isometric view.

**Source files** downloads the original files, with their original filenames.
**Download preview mesh** retrieves the browser mesh, which may have been
tessellated from STEP or converted from OBJ. Bounding boxes are reported in
model units because STL does not encode physical units.

## Refresh from Cubware

This is a published snapshot, not a live GitHub connection. From the website
checkout, with Cubware at `../../Cubware`:

```sh
python3 scripts/sync-cubware-cad.py --cubware ../../Cubware
python3 scripts/check-cad-catalog.py --cubware ../../Cubware
python3 -m unittest discover -s scripts -p 'test_cad_sync.py'
python3 -m http.server 8000
```

Open `http://localhost:8000/cubware.html`. Review the snapshot date, file counts,
and **Missing 3D preview** / **Local changes** filters before publishing.
Commit the page changes, `assets/cad/catalog.json`, `assets/cad/catalog/`, and
`assets/cad/sources/` to the website's main branch to publish via GitHub Pages.
Refreshing only your local files does not update the public site.

STEP conversion uses the installed FreeCAD Python runtime on macOS. Set
`FREECAD_PYTHON` to another compatible FreeCAD Python runtime when needed.
Missing FreeCAD or a failed conversion retains the entry and its original
downloads, marks the missing preview, and returns a failing exit code.
The source coverage check verifies every CAD source and each download's SHA-256.

## What is included

All nested STL, STEP/STP, OBJ, GLB, 3MF and FCStd files are cataloged. Files in
the same folder with the same stem share an entry. Revision-bearing names
remain separate, as do identical files stored in different source folders.
Byte-identical previews share a mesh file. FreeCAD backups are recorded as
excluded. A standalone slicer project or native CAD file without a supported
mesh remains searchable and downloadable with an explicit missing-preview state.

The manifest records a UTC refresh time, Cubware's commit, source hashes and
whether each source matches that commit. **Local changes** means at least one
CAD source differs from, or is absent in, that commit; it is not a validation
status. Original sources, available images and direct-folder README snapshots
are included so local designs do not depend on nonexistent GitHub links.

Part notes link to the pinned GitHub file when it matches the snapshot,
otherwise to a local plain-text copy. Source paths, status notices and notes
come from Cubware. Configuration/category filters follow repository folders,
not independently verified compatibility. Geometry previews do not establish
physical fit or fabrication readiness.

## Maintenance

The sync command treats Cubware as read-only. It generates into a temporary
directory, copies completed assets, and replaces the manifest last. Old generated
assets are removed only after the replacement snapshot is available. A missing
source checkout cannot erase the existing snapshot.

The library uses the same pinned Three.js version as the Build It viewer.
Catalog browsing and downloads work independently of the 3D module: if WebGL or
the module CDN is unavailable, the page reports the preview failure while
leaving the source files available.
