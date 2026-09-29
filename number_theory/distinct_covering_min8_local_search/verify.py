"""Literal progression verifier for an explicit minimum-eight covering.

Standard-library Python >=3.10. six-covering-1, researcher.
"""
import argparse
from collections import Counter
import hashlib
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def require(condition, message):
    if not condition:
        raise ValueError(message)


def verify(data):
    require(data.get('format_version') == 1, 'invalid format version')
    rows = data['congruences']
    require(bool(rows), 'empty covering')
    require(all(len(pair) == 2 and all(type(v) is int for v in pair) for pair in rows), 'malformed class')
    require(all(m >= 8 and 0 <= a < m for a, m in rows), 'invalid modulus or phase')
    moduli = [m for a, m in rows]
    require(len(set(moduli)) == len(moduli), 'repeated modulus')
    require(min(moduli) == 8, 'minimum is not exactly eight')
    L = math.lcm(*moduli)
    require(type(data['lcm']) is int and data['lcm'] == L, 'claimed LCM differs')
    require(8 <= L <= 100000, 'outside this checker resource bound')
    count = [0] * L
    for a, m in rows:
        for x in range(a, L, m):
            count[x] += 1
    holes = [x for x, value in enumerate(count) if not value]
    require(not holes, f'{len(holes)} uncovered residues')
    require(max(count) < 256, 'multiplicities do not fit the declared digest encoding')
    essential = [[m, sum(count[x] == 1 for x in range(a, L, m))] for a, m in rows]
    return {'agent': 'six-covering-1', 'role': 'researcher',
            'minimum_modulus': 8, 'lcm': L, 'classes': len(rows), 'uncovered': 0,
            'coverage_multiplicities': {str(k): v for k, v in sorted(Counter(count).items())},
            'multiplicity_bytes_sha256': hashlib.sha256(bytes(count)).hexdigest(),
            'private_points_by_modulus': essential}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--cover', type=Path, default=ROOT / 'cover.json')
    parser.add_argument('--check-expected', action='store_true')
    args = parser.parse_args()
    result = verify(json.loads(args.cover.read_text()))
    if args.check_expected:
        require(result == json.loads((ROOT / 'expected.json').read_text()), 'expected summary differs')
    print(json.dumps(result, sort_keys=True))
    print('EXPLICIT COVER VERIFIED')


if __name__ == '__main__':
    main()
