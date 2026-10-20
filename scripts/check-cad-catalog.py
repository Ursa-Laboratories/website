#!/usr/bin/env python3
"""Check recursive Cubware source coverage and preview mesh integrity."""
import argparse
import hashlib
import json
import struct
from pathlib import Path

site = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--cubware', type=Path, default=site.parents[1] / 'Cubware')
args = parser.parse_args()
root = args.cubware.resolve()
assert root.is_dir(), f'Cubware directory not found: {root}'
catalog = json.loads((site / 'assets/cad/catalog.json').read_text())
parts = catalog['parts']
extensions = {'.stl', '.step', '.stp', '.glb', '.obj', '.fcstd', '.3mf'}
expected = {p.relative_to(root).as_posix() for p in root.rglob('*')
            if p.is_file() and p.suffix.lower() in extensions and '.git' not in p.parts}
covered = [source for part in parts for source in part['sources']]
assert len(set(covered)) == len(covered), 'Source appears in multiple catalog entries'
assert set(covered) == expected, f'Source coverage differs: missing={expected-set(covered)}, stale={set(covered)-expected}'
assert len({part['id'] for part in parts}) == len(parts), 'Duplicate part IDs'
missing_previews = 0
for part in parts:
    assert part['group'] in {'Cub', 'CubXL', 'CubXL+', 'Labware'}
    for source in part['source_files']:
        original = root / source['path']
        download = (site / source['download']).resolve()
        assert download.is_relative_to(site), f'Download outside website: {download}'
        assert hashlib.sha256(original.read_bytes()).hexdigest() == source['sha256'], f'Stale source: {original}'
        assert hashlib.sha256(download.read_bytes()).hexdigest() == source['sha256'], f'Download differs: {download}'
    for companion in (part.get('readme'),):
        if companion:
            assert (site / companion['download']).is_file(), f'Missing notes: {part["id"]}'
    if not part['file']:
        assert part['preview_error'], f'Missing preview reason: {part["id"]}'
        missing_previews += 1
        continue
    mesh = (site / part['file']).resolve()
    assert mesh.is_relative_to(site), f'Mesh outside website: {mesh}'
    data = mesh.read_bytes()
    if mesh.suffix == '.glb':
        assert data[:4] == b'glTF' and struct.unpack('<I', data[8:12])[0] == len(data), f'Invalid GLB: {mesh}'
        continue
    assert len(data) >= 84, f'Empty mesh: {mesh}'
    triangles = struct.unpack('<I', data[80:84])[0]
    binary = len(data) == 84 + 50 * triangles and triangles > 0
    ascii_stl = data.lstrip().startswith(b'solid') and b'facet normal' in data and b'endsolid' in data
    assert binary or ascii_stl, f'Invalid STL: {mesh}'
print(f'{len(parts)} entries cover all {len(expected)} CAD sources; source downloads match, every available preview mesh passes. {missing_previews} entries have no preview.')
