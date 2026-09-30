"""Reject corrupt witnesses and check the attributed public initializer."""
import copy
import hashlib
import json
import math
from verify import ROOT, verify


def main():
    good = json.loads((ROOT / 'cover.json').read_text())
    summary = verify(good)
    provenance = json.loads((ROOT / 'provenance.json').read_text())
    raw = (ROOT / 'seed.tsv').read_bytes()
    seed = [tuple(map(int, line.split())) for line in raw.decode().splitlines()]
    if len(seed) != 82 or len({m for a, m in seed}) != 82:
        raise ValueError('Incorrect initializer size or distinctness')
    if min(m for a, m in seed) != 8 or any(not 0 <= a < m for a, m in seed):
        raise ValueError('Incorrect initializer phases or exact minimum')
    if math.lcm(*(m for a, m in seed)) != 30240:
        raise ValueError('Incorrect initializer LCM')
    if not all(any(x % m == a for a, m in seed) for x in range(30240)):
        raise ValueError('Initializer does not cover its entire period')
    if hashlib.sha256(raw).hexdigest() != provenance['seed_tsv_sha256']:
        raise ValueError('Initializer bytes disagree with provenance')
    retained = sum(list(pair) in good['congruences'] for pair in seed)
    if retained != 3 or retained != provenance['retained_initializer_classes']:
        raise ValueError('Initializer retention differs')
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
    for data in bad:
        try:
            verify(data)
        except ValueError:
            continue
        raise ValueError('Corrupted certificate accepted')
    if not all(points > 0 for m, points in summary['private_points_by_modulus']):
        raise ValueError('A claimed irredundant class has no private point')
    print('5 corrupted certificates rejected')
    print('82-class reviewer initializer and 3 retained classes checked')


if __name__ == '__main__':
    main()
