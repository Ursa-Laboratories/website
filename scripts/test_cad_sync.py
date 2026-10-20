"""Offline regression checks for catalog coverage and refresh failure behavior."""
import importlib.util
import json
import struct
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

spec = importlib.util.spec_from_file_location("cad_sync", Path(__file__).with_name("sync-cubware-cad.py"))
sync = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sync)


class CatalogSyncTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.cubware = self.root / "Cubware"
        self.site = self.root / "site"
        self.cubware.mkdir()
        (self.cubware / "README.md").write_text("# Cubware\n")
        self.mesh = b"test".ljust(80, b" ") + struct.pack("<I12fH", 1, *([0.0] * 12), 0)

    def source(self, name, content):
        path = self.cubware / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content)
        return path

    def run_sync(self, failures=None):
        args = ["sync", "--cubware", str(self.cubware), "--landing-page", str(self.site)]
        def git_result(root, *git_args):
            return "a" * 40 if git_args[0] == "rev-parse" else ""
        with patch("sys.argv", args), patch.object(sync, "git_output", side_effect=git_result), \
                patch.object(sync, "convert_steps", return_value=failures or []):
            code = sync.main()
        catalog = json.loads((self.site / "assets/cad/catalog.json").read_text())
        return code, catalog

    def test_companions_duplicates_and_unsupported_sources_are_preserved(self):
        self.source("cub/labware/A.stl", self.mesh)
        self.source("cub/labware/A.step", b"source CAD")
        self.source("cub/labware/A.gcode.3mf", b"sliced companion")
        self.source("shared/A.stl", self.mesh)
        self.source("misc/Native.FCStd", b"native CAD")
        self.source("misc/Layout.3mf", b"slicer project")
        code, catalog = self.run_sync()
        self.assertEqual(code, 0)
        self.assertEqual(len(catalog["parts"]), 4)
        self.assertEqual(sum(len(p["sources"]) for p in catalog["parts"]), 6)
        meshes = [p["file"] for p in catalog["parts"] if p["file"]]
        self.assertEqual(len(set(meshes)), 1)
        unavailable = [p for p in catalog["parts"] if not p["file"]]
        self.assertEqual(len(unavailable), 2)
        self.assertTrue(all(p["preview_error"] for p in unavailable))
        for part in catalog["parts"]:
            for source in part["source_files"]:
                self.assertEqual((self.site / source["download"]).read_bytes(),
                                 (self.cubware / source["path"]).read_bytes())
                self.assertTrue(source["local_changes"])

    def test_failed_step_conversion_retains_source_and_original_download(self):
        path = self.source("cub/Camera.step", b"STEP source")
        code, catalog = self.run_sync([{"source": str(path), "reason": "No FreeCAD"}])
        self.assertEqual(code, 1)
        self.assertEqual(catalog["parts"][0]["sources"], ["cub/Camera.step"])
        self.assertIsNone(catalog["parts"][0]["file"])
        self.assertIn("failed", catalog["parts"][0]["preview_error"])
        self.assertTrue((self.site / catalog["parts"][0]["source_files"][0]["download"]).exists())

    def test_missing_checkout_keeps_existing_snapshot(self):
        manifest = self.site / "assets/cad/catalog.json"
        manifest.parent.mkdir(parents=True)
        manifest.write_text('{"existing": true}')
        args = ["sync", "--cubware", str(self.root / "missing"), "--landing-page", str(self.site)]
        with patch("sys.argv", args), self.assertRaises(SystemExit):
            sync.main()
        self.assertEqual(json.loads(manifest.read_text()), {"existing": True})


if __name__ == "__main__":
    unittest.main()
