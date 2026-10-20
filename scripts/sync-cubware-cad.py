#!/usr/bin/env python3
"""Synchronize Cubware CAD into the landing-page catalog.

The source repository is read-only for this script.  Each catalog item keeps
all CAD companions in ``sources`` while exposing one browser-friendly STL
mesh.  Existing STL files win over converted STEP files; STEP-only parts are
meshed with the bundled FreeCAD runtime.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import re
import shutil
import struct
import subprocess
import sys
import tempfile
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import quote


CAD_SUFFIXES = (".stl", ".step", ".stp", ".glb", ".3mf", ".fcstd", ".obj")
BACKUP_SUFFIXES = (".fcbak",)
REPOSITORY = "https://github.com/Ursa-Laboratories/Cubware"


def git_output(root: Path, *args: str) -> str:
    return subprocess.run(
        ["git", "-C", str(root), *args], capture_output=True, text=True, check=True
    ).stdout.strip()


def configuration_for(path: Path) -> str:
    return {
        "cub": "Cub", "cubxl": "CubXL", "cubxl_plus": "CubXL+",
        "shared": "Shared", "gantry": "Gantry", "misc": "Unassigned",
    }.get(path.parts[0], "Unassigned")


def category_for(path: Path) -> str:
    if "labware" in path.parts or path.parts[0] == "shared":
        return "Labware"
    if "instrument_mounts" in path.parts:
        return "Instrument mounts"
    if "deck" in path.parts:
        return "Decks"
    if path.parts[0] == "gantry":
        return "Gantry & enclosure"
    return "Other"


def summary_from_readme(path: Path | None) -> str:
    if not path:
        return ""
    text = path.read_text(errors="replace")
    for paragraph in re.split(r"\n\s*\n", text):
        paragraph = paragraph.strip()
        if not paragraph or paragraph.startswith(("#", "!", "|", "```", "-", ">")):
            continue
        paragraph = re.sub(r"\[([^]]+)\]\([^)]+\)", r"\1", paragraph)
        paragraph = re.sub(r"[*`]", "", paragraph)
        return " ".join(paragraph.split())[:500]
    return ""


def slug(value: str) -> str:
    value = value.replace("+", " plus ")
    value = re.sub(r"[^A-Za-z0-9]+", "-", value).strip("-").lower()
    return value or "part"


def source_stem(path: Path) -> str:
    name = path.name
    lower = name.lower()
    if lower.endswith(".gcode.3mf"):
        return name[: -len(".gcode.3mf")]
    return path.stem


def group_for(relative: Path) -> str:
    top = relative.parts[0].lower()
    if "labware" in {part.lower() for part in relative.parts}:
        return "Labware"
    if top == "cubxl":
        return "CubXL"
    if top == "cubxl_plus":
        return "CubXL+"
    if top in {"shared", "misc"}:
        return "Labware"
    return "Cub"  # cub/ and gantry/ belong to the small-Cub browsing group.


def subgroup_for(relative: Path) -> str:
    parts = list(relative.parts[:-1])
    return "/".join(parts)


def status_for(relative: Path) -> tuple[str, str]:
    text = "/".join(relative.parts).lower()
    if "/reference/" in f"/{text}/" or any(
        token in text for token in ("envelope", "illustrative", "publishedmachine", "indenterreference")
    ):
        return "reference", "Reference geometry or an illustrative envelope from Cubware; descriptive preview only."
    if "genmitsu_prover_v2_enclosure_d" in text:
        return "mockup", "Design and packaging mockup; Cubware says this enclosure is not a finished kit."
    if "concentric_asmi_genmitsu_v2" in text:
        return "prototype", "Prototype CAD; Cubware marks physical validation as pending."
    if "genmitsu_front_fascia" in text:
        return "prototype", "Measured prototype; Cubware says physical fit, print strength, and clearance checks are pending."
    if relative.suffix.lower() in {".step", ".stp", ".fcstd"}:
        return "source-cad", "Source CAD companion; the landing page exposes a generated mesh preview."
    return "mesh", "CAD mesh catalog entry; refer to the source README for compatibility and use."


def read_obj_as_stl(source: Path, target: Path) -> None:
    vertices: list[tuple[float, float, float]] = []
    faces: list[tuple[int, int, int]] = []
    for line in source.read_text(errors="replace").splitlines():
        line = line.strip()
        if line.startswith("v "):
            bits = line.split()
            if len(bits) >= 4:
                vertices.append(tuple(float(x) for x in bits[1:4]))
        elif line.startswith("f "):
            refs = []
            for token in line.split()[1:]:
                index = int(token.split("/")[0])
                refs.append(index - 1 if index > 0 else len(vertices) + index)
            for i in range(1, len(refs) - 1):
                faces.append((refs[0], refs[i], refs[i + 1]))
    if not vertices or not faces:
        raise ValueError("OBJ has no triangular faces")

    def normal(a, b, c):
        ux, uy, uz = (b[i] - a[i] for i in range(3))
        vx, vy, vz = (c[i] - a[i] for i in range(3))
        nx, ny, nz = uy * vz - uz * vy, uz * vx - ux * vz, ux * vy - uy * vx
        length = math.sqrt(nx * nx + ny * ny + nz * nz) or 1.0
        return nx / length, ny / length, nz / length

    header = b"Ursa Cubware OBJ conversion".ljust(80, b" ")
    with target.open("wb") as out:
        out.write(header)
        out.write(struct.pack("<I", len(faces)))
        for ia, ib, ic in faces:
            a, b, c = vertices[ia], vertices[ib], vertices[ic]
            out.write(struct.pack("<3f", *normal(a, b, c)))
            out.write(struct.pack("<3f", *a))
            out.write(struct.pack("<3f", *b))
            out.write(struct.pack("<3f", *c))
            out.write(struct.pack("<H", 0))


def freecad_python() -> str | None:
    candidates = [
        os.environ.get("FREECAD_PYTHON"),
        "/Applications/FreeCAD.app/Contents/Resources/bin/python",
        shutil.which("freecadcmd"),
        shutil.which("FreeCADCmd"),
    ]
    return next((p for p in candidates if p and Path(p).exists()), None)


def freecad_convert(plan: Path) -> int:
    # This branch runs inside FreeCAD's bundled Python process.
    lib = "/Applications/FreeCAD.app/Contents/Resources/lib"
    if lib not in sys.path:
        sys.path.insert(0, lib)
    site = "/Applications/FreeCAD.app/Contents/Resources/lib/python3.11/site-packages"
    if site not in sys.path:
        sys.path.insert(0, site)
    import FreeCAD as App  # type: ignore
    import MeshPart  # type: ignore
    import Part  # type: ignore

    failures = []
    for entry in json.loads(plan.read_text()):
        source = entry["source"]
        target = entry["target"]
        try:
            doc = App.newDocument("cad_sync")
            Part.insert(source, "cad_sync")
            shapes = [o.Shape for o in doc.Objects if hasattr(o, "Shape") and not o.Shape.isNull()]
            if not shapes:
                raise ValueError("STEP contained no nonempty shapes")
            shape = Part.makeCompound(shapes)
            mesh = MeshPart.meshFromShape(Shape=shape, LinearDeflection=0.1, AngularDeflection=0.3, Relative=False)
            mesh.write(target)
            App.closeDocument(doc.Name)
        except Exception as exc:  # pragma: no cover - depends on CAD kernel input
            failures.append({"source": source, "reason": str(exc)})
            try:
                App.closeDocument("cad_sync")
            except Exception:
                pass
    plan.with_suffix(".failures.json").write_text(json.dumps(failures, indent=2) + "\n")
    return 1 if failures else 0


def convert_steps(plan_entries: list[dict], script: Path) -> list[dict]:
    if not plan_entries:
        return []
    executable = freecad_python()
    if not executable:
        return [{"source": e["source"], "reason": "FreeCAD Python runtime not found"} for e in plan_entries]
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as handle:
        json.dump(plan_entries, handle)
        plan = Path(handle.name)
    env = os.environ.copy()
    lib = "/Applications/FreeCAD.app/Contents/Resources/lib"
    env["DYLD_LIBRARY_PATH"] = f"{lib}:{env.get('DYLD_LIBRARY_PATH', '')}" if Path(lib).exists() else env.get("DYLD_LIBRARY_PATH", "")
    try:
        result = subprocess.run(
            [executable, str(script), "--freecad-convert", str(plan)],
            env=env,
            text=True,
            capture_output=True,
            check=False,
        )
        failures_path = plan.with_suffix(".failures.json")
        failures = json.loads(failures_path.read_text()) if failures_path.exists() else []
        if result.returncode and not failures:
            failures = [{"source": e["source"], "reason": result.stderr[-1000:] or "FreeCAD conversion failed"} for e in plan_entries]
        return failures
    finally:
        for path in (plan, plan.with_suffix(".failures.json")):
            path.unlink(missing_ok=True)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cubware", type=Path, default=None)
    parser.add_argument("--landing-page", type=Path, default=None)
    parser.add_argument("--freecad-convert", type=Path, default=None)
    args = parser.parse_args()
    if args.freecad_convert:
        return freecad_convert(args.freecad_convert)

    script = Path(__file__).resolve()
    landing = (args.landing_page or script.parents[1]).resolve()
    cubware = (args.cubware or landing.parents[1] / "Cubware").resolve()
    if not cubware.is_dir() or not (cubware / "README.md").is_file():
        parser.error(f"Not a Cubware checkout: {cubware}")
    revision = git_output(cubware, "rev-parse", "HEAD")
    committed = {}
    for row in git_output(cubware, "ls-tree", "-r", "-z", "HEAD").split("\0"):
        if row:
            metadata, name = row.split("\t", 1)
            committed[name] = metadata.split()[2]
    cad_root = landing / "assets" / "cad"
    staging = tempfile.TemporaryDirectory(prefix="cubware-sync-")
    stage = Path(staging.name)
    output = stage / "catalog"
    output.mkdir(parents=True, exist_ok=True)
    source_output = stage / "sources"
    source_output.mkdir()

    def source_info(path: Path) -> dict:
        relative = path.relative_to(cubware).as_posix()
        content = path.read_bytes()
        digest = hashlib.sha256(content).hexdigest()
        blob = hashlib.sha1(f"blob {len(content)}\0".encode() + content).hexdigest()
        matches_commit = committed.get(relative) == blob
        # Content-addressed copies keep every source download available, including
        # local-only CAD. Filenames in the UI retain the original spelling.
        suffix = ".txt" if path.suffix.lower() == ".md" else path.suffix.lower()
        name = digest + suffix
        target = source_output / name
        if not target.exists():
            target.write_bytes(content)
        return {
            "path": relative, "name": path.name, "bytes": len(content),
            "format": "GCODE.3MF" if path.name.lower().endswith(".gcode.3mf") else path.suffix[1:].upper(),
            "sha256": digest, "download": f"assets/cad/sources/{name}",
            "local_changes": not matches_commit,
            "url": f"{REPOSITORY}/blob/{revision}/{quote(relative, safe='/')}" if matches_commit else None,
        }

    files = []
    excluded = []
    for path in sorted(cubware.rglob("*")):
        if not path.is_file() or ".git" in path.parts:
            continue
        relative = path.relative_to(cubware)
        lower = path.name.lower()
        if lower.endswith(CAD_SUFFIXES) or lower.endswith(BACKUP_SUFFIXES) or lower.endswith(".gcode.3mf"):
            if lower.endswith(BACKUP_SUFFIXES):
                excluded.append({"source": relative.as_posix(), "reason": "FreeCAD backup file, retained as provenance only"})
            else:
                files.append(path)

    grouped: dict[tuple[Path, str], list[Path]] = defaultdict(list)
    for path in files:
        relative = path.relative_to(cubware)
        grouped[(relative.parent, source_stem(path))].append(path)

    items = []
    conversions = []
    used_ids: set[str] = set()
    used_names: set[str] = set()
    for (parent, stem), companions in sorted(grouped.items(), key=lambda pair: str(pair[0])):
        relative = parent / next(p.name for p in companions if p.name.startswith(stem) or source_stem(p) == stem)
        group = group_for(relative)
        ordered = sorted(companions, key=lambda p: {".stl": 0, ".step": 1, ".stp": 1, ".obj": 2, ".glb": 3, ".3mf": 4, ".fcstd": 5}.get(p.suffix.lower(), 9))
        selected = next((p for p in ordered if p.suffix.lower() == ".stl"), None)
        selected_kind = "stl"
        if selected is None:
            selected = next((p for p in ordered if p.suffix.lower() in {".step", ".stp"}), None)
            selected_kind = "step"
        if selected is None:
            selected = next((p for p in ordered if p.suffix.lower() == ".obj"), None)
            selected_kind = "obj"
        if selected is None:
            selected = next((p for p in ordered if p.suffix.lower() == ".glb"), None)
            selected_kind = "glb"
        if selected is None:
            selected = ordered[0]
            selected_kind = "unavailable"

        source_rel = selected.relative_to(cubware)
        status, status_desc = status_for(source_rel)
        asset_slug = slug(str(parent / stem))
        asset_name = f"{asset_slug}.stl" if selected_kind in {"stl", "step", "obj"} else f"{asset_slug}{selected.suffix.lower()}"
        if asset_name in used_names:
            suffix = hashlib.sha1(str(parent / stem).encode()).hexdigest()[:8]
            asset_name = f"{asset_slug}-{suffix}.stl" if selected_kind in {"stl", "step", "obj"} else f"{asset_slug}-{suffix}{selected.suffix.lower()}"
        used_names.add(asset_name)
        asset_path = output / asset_name
        if selected_kind == "stl":
            shutil.copy2(selected, asset_path)
        elif selected_kind == "obj":
            try:
                read_obj_as_stl(selected, asset_path)
            except Exception as exc:
                excluded.append({"source": source_rel.as_posix(), "reason": f"OBJ conversion failed: {exc}"})
                selected_kind = "unavailable"
        elif selected_kind == "step":
            conversions.append({"source": str(selected), "target": str(asset_path)})
        elif selected_kind == "glb":
            shutil.copy2(selected, asset_path)

        item_id = slug(str(parent / stem))
        if item_id in used_ids:
            item_id = f"{item_id}-{hashlib.sha1(str(parent / stem).encode()).hexdigest()[:8]}"
        used_ids.add(item_id)
        source_paths = [p.relative_to(cubware).as_posix() for p in sorted(companions)]
        # Do not inherit a distant README: that can describe a different part.
        readme = next((p for p in selected.parent.iterdir() if p.name.lower() == "readme.md"), None)
        preview = selected.with_suffix(".png")
        sources = [source_info(p) for p in sorted(companions)]
        items.append({
            "id": item_id,
            "label": stem.replace("_", " "),
            "group": group,
            "subgroup": subgroup_for(relative),
            "file": f"assets/cad/catalog/{asset_name}" if selected_kind != "unavailable" else None,
            "preview_kind": selected_kind,
            "preview_error": "No supported mesh or STEP source is available." if selected_kind == "unavailable" else None,
            "source": source_rel.as_posix(),
            "sources": source_paths,
            "desc": status_desc,
            "status": status,
            "configuration": configuration_for(source_rel),
            "category": category_for(source_rel),
            "formats": sorted({s["format"] for s in sources}),
            "source_files": sources,
            "local_changes": any(s["local_changes"] for s in sources),
            "readme": source_info(readme) if readme else None,
            "summary": summary_from_readme(readme),
            "image": source_info(preview)["download"] if preview.is_file() else None,
        })

    failures = convert_steps(conversions, script)
    failed_sources = {
        Path(f["source"]).resolve().relative_to(cubware).as_posix()
        for f in failures
    }
    for failure in failures:
        excluded.append({"source": Path(failure["source"]).resolve().relative_to(cubware).as_posix(), "reason": f"STEP conversion failed: {failure['reason']}"})
    for item in items:
        if item["source"] in failed_sources:
            item["file"] = None
            item["preview_error"] = "STEP preview conversion failed. Original CAD is available below."

    # Deduplicate byte-identical generated meshes while preserving every source item.
    first_for_hash: dict[str, str] = {}
    for item in items:
        if not item["file"]:
            continue
        path = stage / Path(item["file"]).relative_to("assets/cad")
        if not path.exists():
            continue
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        if digest in first_for_hash:
            path.unlink()
            item["file"] = first_for_hash[digest]
        else:
            first_for_hash[digest] = item["file"]

    catalog = {
        "version": 2,
        "source": "Cubware",
        "repository": REPOSITORY,
        "source_revision": revision,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "parts": sorted(items, key=lambda item: (item["group"], item["subgroup"], item["label"])),
        "excluded_sources": sorted(excluded, key=lambda entry: entry["source"]),
    }
    # Finish generation before touching the served snapshot. Replace the manifest
    # last; an interrupted conversion cannot erase the existing catalog.
    cad_root.mkdir(parents=True, exist_ok=True)
    for folder in ("catalog", "sources"):
        shutil.copytree(stage / folder, cad_root / folder, dirs_exist_ok=True)
    manifest = cad_root / "catalog.json"
    temporary_manifest = manifest.with_suffix(".json.tmp")
    temporary_manifest.write_text(json.dumps(catalog, indent=2, ensure_ascii=False) + "\n")
    temporary_manifest.replace(manifest)
    for folder in ("catalog", "sources"):
        keep = {p.name for p in (stage / folder).iterdir()}
        for path in (cad_root / folder).iterdir():
            if path.is_file() and path.name not in keep:
                path.unlink()
    staging.cleanup()
    print(f"cataloged {len(items)} entries; generated {len(conversions) - len(failures)} STEP meshes; excluded {len(excluded)} source files")
    if failures:
        print(f"conversion failures: {len(failures)}", file=sys.stderr)
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
