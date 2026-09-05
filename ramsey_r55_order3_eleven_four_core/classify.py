#!/usr/bin/env python3
"""Exact local four-triangle core cover by obstruction masks and generator orbits."""
from itertools import combinations, product
from pathlib import Path
import argparse
import hashlib
import json
import resource
import time

PAIRS = tuple(combinations(range(4), 2))
PRIMARY = (1, 2, 3, 4, 5, 6, 7, 8, 9, 31, 32, 33, 34, 35, 36, 58, 59, 60)


def require(ok, message):
    if not ok:
        raise ValueError(message)


def digest(values):
    return hashlib.sha256(''.join(f'{x}\n' for x in sorted(values)).encode()).hexdigest()


def word(code):
    return ''.join(str(code >> i & 1) for i in range(18))


def position(a, b):
    a, b = sorted((a, b))
    i, s = divmod(a, 3)
    j, t = divmod(b, 3)
    return None if i == j else 3*PAIRS.index((i, j))+(t-s) % 3


def obstructions():
    masks = set()
    for vs in combinations(range(12), 5):
        if sorted(sum(v//3 == i for v in vs) for i in range(4)) != [1, 1, 1, 2]:
            continue
        positions = {position(a, b) for a, b in combinations(vs, 2)}-{None}
        masks.add(sum(1 << p for p in positions))
    require(len(masks) == 108 and all(p.bit_count() == 9 for p in masks), 'occupancy masks')
    return sorted(masks)


def normalized(code):
    anchors = [code >> (3*i) & 7 for i in range(3)]
    return all(w in (0, 1, 3) for w in anchors) and anchors == sorted(anchors)


def bit_map(perm, shifts, sign):
    out = []
    for i, j in PAIRS:
        for d in range(3):
            a, b = perm[i], perm[j]
            delta = sign*d+shifts[j]-shifts[i]
            if a > b:
                a, b, delta = b, a, -delta
            out.append(3*PAIRS.index((a, b))+delta % 3)
    require(sorted(out) == list(range(18)), 'bit permutation')
    return out


def generators():
    identity = list(range(4))
    maps = []
    for i in range(3):
        perm = identity.copy()
        perm[i], perm[i+1] = perm[i+1], perm[i]
        maps.append(bit_map(perm, [0]*4, 1))
    for i in range(4):
        shifts = [0]*4
        shifts[i] = 1
        maps.append(bit_map(identity, shifts, 1))
    maps.append(bit_map(identity, [0]*4, -1))
    return maps


def transport(code, mapping):
    return sum((code >> old & 1) << new for new, old in enumerate(mapping))


def classify(work):
    start = time.monotonic()
    masks = obstructions()
    domain = {sum(w << (3*i) for i, w in enumerate(words)) for words in product(range(7), repeat=6)}
    valid = {x for x in domain if not any(x & m == m for m in masks)}
    maps = generators()
    left = set(valid)
    cases, membership = [], []
    while left:
        seed = min(left)
        orbit, queue = {seed}, [seed]
        for x in queue:
            for mapping in maps:
                y = transport(x, mapping)
                if y not in orbit:
                    orbit.add(y)
                    queue.append(y)
        require(orbit <= left, 'overlap or invalid orbit')
        choices = sorted((x for x in orbit if normalized(x)), key=word)
        require(choices, 'no compatible representative')
        rep = choices[0]
        row = dict(bits=word(rep), code=rep, labeled=len(orbit), normalized=len(choices),
                   members_sha256=digest(orbit), units=[v if rep >> i & 1 else -v for i, v in enumerate(PRIMARY)])
        cases.append(row)
        membership.extend((x, rep) for x in orbit)
        left -= orbit
    cases.sort(key=lambda row: row['bits'])
    for i, row in enumerate(cases):
        row['index'] = i
    report = dict(format='r55-k11-four-core-cover-v1', raw_binary=2**18,
                  noncomplete=len(domain), forbidden_patterns=masks,
                  labeled_valid=len(valid), labeled_invalid=len(domain)-len(valid),
                  normalized_valid=sum(r['normalized'] for r in cases), normalizer_maps=3888,
                  effective_core_maps=1296, classes=len(cases), valid_sha256=digest(valid), cases=cases)
    report['membership_sha256'] = hashlib.sha256(''.join(f'{a} {b}\n' for a, b in sorted(membership)).encode()).hexdigest()
    work.mkdir(parents=True, exist_ok=True)
    (work / 'cover.json').write_text(json.dumps(report, sort_keys=True, separators=(',', ':'))+'\n')
    (work / 'membership.txt').write_text(''.join(f'{a} {b}\n' for a, b in sorted(membership)))
    measurement = dict(elapsed_seconds=round(time.monotonic()-start, 6), maxrss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    (work / 'measurement.json').write_text(json.dumps(measurement, indent=2, sort_keys=True)+'\n')
    print(json.dumps({k: report[k] for k in ('noncomplete', 'labeled_valid', 'labeled_invalid', 'classes', 'normalized_valid')}), flush=True)
    print(json.dumps(measurement), flush=True)


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--work', type=Path, required=True)
    a = p.parse_args()
    require(not a.work.resolve().is_relative_to(Path(__file__).resolve().parent.parent), 'large transient state outside Git')
    classify(a.work)
