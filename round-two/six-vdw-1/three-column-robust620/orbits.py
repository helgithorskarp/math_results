"""Complete affine orbit census of three exceptional residues in F31."""
import argparse
import hashlib
from itertools import combinations
import json
from pathlib import Path


def require(ok, message):
    if not ok:
        raise ValueError(message)


def run(directory):
    remaining = set(combinations(range(31), 3))
    classes = []
    while remaining:
        holes = min(remaining)
        images = sorted({tuple(sorted((a*x+b) % 31 for x in holes))
                         for a in range(1, 31) for b in range(31)})
        require(set(images) <= remaining, 'overlapping affine field classes')
        require(930 % len(images) == 0, 'field orbit/stabilizer count')
        classes.append({'holes': list(holes), 'orbit_size': len(images), 'members': [list(x) for x in images]})
        remaining.difference_update(images)
    require([c['holes'] for c in classes] == [[0, 1, t] for t in [2, 3, 4, 5, 6, 12]], 'native case list')
    result = {'author': 'six-vdw-1', 'role': 'researcher',
              'status': 'COMPLETE_FIELD_TRIPLE_CENSUS_REQUIRES_SEPARATE_AUDIT',
              'affine_group_order': 930, 'labeled_triples': 4495, 'classes': classes}
    directory.mkdir(parents=True, exist_ok=True)
    raw = (json.dumps(result, sort_keys=True, indent=2)+'\n').encode()
    (directory / 'triples.json').write_bytes(raw)
    print(json.dumps({'classes': len(classes), 'orbit_sizes': [c['orbit_size'] for c in classes],
                      'triples_sha256': hashlib.sha256(raw).hexdigest()}), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(); parser.add_argument('directory', type=Path)
    run(parser.parse_args().directory)
