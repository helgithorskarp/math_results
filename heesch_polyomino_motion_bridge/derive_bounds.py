"""Compute the new unrestricted upper consequences of the prior certificates.

This checks provenance/completeness hashes and integer arithmetic. It does
not regenerate or reverify the underlying UNSAT proofs. See the dependency's
verify_growth.py for that separate trust boundary and full replay.
"""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import sys

from motion import check_dependency, dimensions, unrestricted_upper

MANIFEST_SHA256 = '8f96c536c15f739130b6ca7e5a67fcba1ff1e51fa4bbc18b16d652182c24ff85'
FAMILY_SHA256 = '935192a6bead7d979d7ed60f3907e52278962940d9b3c008d18af94a85fc36ef'


def derive(prior):
    check_dependency(prior)
    sys.path.insert(0, str(prior.resolve()))
    from growth import generate_family, serialization
    manifest_path = prior/'growth20_manifest.json'
    raw = manifest_path.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == MANIFEST_SHA256, 'manifest provenance mismatch'
    manifest = json.loads(raw)
    seed = json.loads((prior/'kaplan17.json').read_text())['cells']
    family, layers = generate_family(seed, manifest['added_cells'])
    assert hashlib.sha256(serialization(family).encode()).hexdigest() == FAMILY_SHA256
    assert manifest['family_sha256'] == FAMILY_SHA256
    assert len(family) == len(manifest['cases']) == 1233
    assert [row['i'] for row in manifest['cases']] == list(range(1233))
    finite = Counter()
    by_radius = {}
    infinite = 0
    for row, tile in zip(manifest['cases'], family):
        assert dimensions(tile)[0] == 20
        if 'radius' in row:
            radius = row['radius']
            upper = unrestricted_upper(tile, radius)
            # A separately arranged integer arithmetic expression.
            m, w, h, span = dimensions(tile)
            numerator = w*h + 2*(radius+span)*(w+h) + 4*(radius+span)**2
            assert upper+1 == numerator // m
            finite[upper] += 1
            by_radius.setdefault(radius, []).append(upper)
        else:
            assert 'periodic' in row
            infinite += 1
    assert sum(finite.values()) == 825 and infinite == 408
    return {'agent': 'six-heesch-1', 'role': 'researcher',
            'dependency_manifest_sha256': MANIFEST_SHA256,
            'dependency_family_sha256': FAMILY_SHA256,
            'family_size': len(family), 'growth_layer_counts': layers,
            'arbitrary_motion_finite_cases': sum(finite.values()),
            'previous_periodic_plane_tilers': infinite,
            'unrestricted_upper_histogram': {str(k): finite[k] for k in sorted(finite)},
            'by_grid_blocking_radius': {str(r): {'cases': len(v), 'min_upper': min(v),
                                               'max_upper': max(v)} for r, v in sorted(by_radius.items())},
            'attributed17_seed_upper_from_radius10': unrestricted_upper(seed, 10),
            'trust': 'written bridge plus previously checked grid certificates; arithmetic application only',
            'new_depth_five_witness': False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--prior-dir', type=Path, default=Path(__file__).parent.parent/'heesch_polyomino_euler_cnf')
    parser.add_argument('--expected', type=Path)
    args = parser.parse_args()
    result = derive(args.prior_dir)
    if args.expected:
        assert result == json.loads(args.expected.read_text()), 'expected output mismatch'
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
