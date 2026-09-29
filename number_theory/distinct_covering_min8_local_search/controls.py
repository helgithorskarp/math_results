"""Malformed and noncovering certificate rejection controls."""
import copy
import json
import math
from verify import ROOT, verify


def main():
    good = json.loads((ROOT / 'cover.json').read_text())
    summary = verify(good)
    seed = [tuple(map(int, line.split())) for line in (ROOT / 'seed.tsv').read_text().splitlines()]
    if len(seed) != 66 or len({m for a,m in seed}) != 66 or min(m for a,m in seed) != 7:
        raise ValueError('invalid supplied initializer')
    if math.lcm(*(m for a,m in seed)) != 10080 or not all(any(x%m==a for a,m in seed) for x in range(10080)):
        raise ValueError('initializer does not cover its claimed period')
    if sum(list(pair) in good['congruences'] for pair in seed if pair[1] != 7) != 29:
        raise ValueError('seed-retention provenance differs')
    bad = []
    c = copy.deepcopy(good)
    c['congruences'].append(c['congruences'][1])
    bad.append(c)
    c = copy.deepcopy(good)
    c['congruences'] = [pair for pair in c['congruences'] if pair[1] != 8]
    bad.append(c)
    c = copy.deepcopy(good)
    c['lcm'] += 8
    bad.append(c)
    essential = next(m for m, points in summary['private_points_by_modulus'] if points)
    c = copy.deepcopy(good)
    for pair in c['congruences']:
        if pair[1] == essential:
            pair[0] = (pair[0] + 1) % essential
    bad.append(c)
    c = copy.deepcopy(good)
    c['congruences'][0][0] = c['congruences'][0][1]
    bad.append(c)
    for c in bad:
        try:
            verify(c)
        except ValueError:
            continue
        raise ValueError('corrupted certificate was accepted')
    print('5 corrupted certificates rejected')
    print('66-class initializer and 29 retained designated classes checked')


if __name__ == '__main__':
    main()
