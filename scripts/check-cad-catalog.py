#!/usr/bin/env python3
"""Check recursive Cubware source coverage and preview mesh integrity."""
import argparse
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
for part in parts:
    assert part['group'] in {'Cub', 'CubXL', 'CubXL+', 'Labware'}
    mesh = (site / part['file']).resolve()
    assert mesh.is_relative_to(site), f'Mesh outside website: {mesh}'
    data = mesh.read_bytes()
    assert len(data) >= 84, f'Empty mesh: {mesh}'
    triangles = struct.unpack('<I', data[80:84])[0]
    binary = len(data) == 84 + 50 * triangles and triangles > 0
    ascii_stl = data.lstrip().startswith(b'solid') and b'facet normal' in data and b'endsolid' in data
    assert binary or ascii_stl, f'Invalid STL: {mesh}'
print(f'{len(parts)} entries cover all {len(expected)} CAD sources; every preview mesh passes.')
