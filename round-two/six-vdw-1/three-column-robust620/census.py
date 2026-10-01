"""Exact C20 row census for the arbitrary F31 XOR C20 construction."""
import argparse
from collections import Counter
import hashlib
import json
import math
from pathlib import Path


def require(ok, message):
    if not ok:
        raise ValueError(message)


def row(mask):
    first = [(mask >> i) & 1 for i in range(10)]
    return first + [1 - b for b in first]


def mask_of(bits):
    require(len(bits) == 20 and all(bits[i + 10] == 1 - bits[i] for i in range(10)), 'opposite halves')
    return sum(bits[i] << i for i in range(10))


def run(directory):
    units = [a for a in range(20) if math.gcd(a, 20) == 1]
    rejected = []
    survivors = {}
    for mask in range(1024):
        bits = row(mask)
        witness = next(((s, d, bits[s]) for d in range(1, 20) for s in range(20)
                        if all(bits[(s + j*d) % 20] == bits[s] for j in range(1, 7))), None)
        if witness is not None:
            rejected.append([mask, *witness])
        else:
            patterns = sorted({sum(bits[(s + j*d) % 20] << j for j in range(7))
                               for d in range(20) for s in range(20)})
            require(all((p ^ 127) in patterns for p in patterns), 'pattern complement closure')
            survivors[mask] = patterns
    remaining = set(survivors)
    orbits = []
    while remaining:
        representative = min(remaining)
        bits = row(representative)
        images = sorted({mask_of([bits[(a*i + b) % 20] for i in range(20)])
                         for a in units for b in range(20)})
        require(all(m in survivors for m in images), 'row affine invariance')
        require(all(survivors[m] == survivors[representative] for m in images), 'pattern affine invariance')
        require(set(images) <= remaining, 'disjoint complete affine orbits')
        require(160 % len(images) == 0, 'orbit divides group order')
        patterns = survivors[representative]
        orbits.append({'representative': representative, 'members': images,
                       'patterns': patterns, 'missing_patterns': sorted(set(range(128)) - set(patterns))})
        remaining.difference_update(images)
    result = {'author': 'six-vdw-1', 'role': 'researcher',
              'status': 'COMPLETE_ROW_CENSUS_REQUIRES_SEPARATE_AUDIT',
              'opposite_half_rows': 1024, 'rejected_rows': len(rejected),
              'surviving_rows': len(survivors), 'affine_group_order': 160,
              'affine_orbits': len(orbits), 'rejection_records': rejected, 'orbits': orbits}
    directory.mkdir(parents=True, exist_ok=True)
    raw = (json.dumps(result, sort_keys=True, indent=2) + '\n').encode()
    (directory / 'rows.json').write_bytes(raw)
    print(json.dumps({'status': result['status'], 'rejected': len(rejected),
                      'survivors': len(survivors), 'orbits': len(orbits),
                      'orbit_sizes': dict(Counter(len(o['members']) for o in orbits)),
                      'signature_sizes': dict(Counter(len(o['patterns']) for o in orbits)),
                      'full_signature_orbits': sum(len(o['patterns']) == 128 for o in orbits),
                      'rows_sha256': hashlib.sha256(raw).hexdigest()}), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('directory', type=Path)
    run(parser.parse_args().directory)
