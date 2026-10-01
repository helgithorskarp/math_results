#!/usr/bin/env python3
"""Generate the precisely scoped projected-seed family and obstruction certificate."""
import argparse
import collections
import hashlib
import functools
import itertools
import json
from pathlib import Path
import subprocess
import time

ROOT = Path(__file__).resolve().parent


@functools.lru_cache(maxsize=None)
def initial(n):
    return [sum(((x >> i) & 1) << x for x in range(1 << n)) for i in range(n)]


def sorts(gates, n):
    wires = initial(n).copy()
    for a, b in gates:
        wires[a], wires[b] = wires[a] & wires[b], wires[a] | wires[b]
    return not any(wires[i] & ~wires[i + 1] for i in range(n - 1))


def projection(gates, n, low, high):
    physical = []
    kept = 0
    for i in range(n):
        if i in low:
            physical.append(-1)
        elif i in high:
            physical.append(-2)
        else:
            physical.append(kept)
            kept += 1
    oriented = []
    for a, b in gates:
        x, y = physical[a], physical[b]
        if x >= 0 and y >= 0:
            oriented.append((x, y))
        elif (x == -2 and y != -2) or (y == -1 and x != -1):
            physical[a], physical[b] = y, x
    permutation = list(range(kept))
    result = []
    for a, b in oriented:
        x, y = permutation[a], permutation[b]
        result.append((min(x, y), max(x, y)))
        if x > y:
            permutation[a], permutation[b] = y, x
    trailing = [permutation[x] for x in physical if x >= 0]
    if trailing != list(range(kept)):
        raise RuntimeError('unexpected output frame')
    return tuple(result)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--work-dir', type=Path, default=ROOT.parents[2] / 'scratch' / 'projection-deletion-barrier')
    args = parser.parse_args()
    work = args.work_dir
    work.mkdir(parents=True, exist_ok=True)
    doc = json.loads((ROOT / 'parents.json').read_text())
    unique = {}
    tables = {}
    for parent in doc['parents']:
        n, gates = parent['n'], parent['gates']
        if len(gates) != parent['m'] or not sorts(gates, n):
            raise RuntimeError('invalid parent: ' + parent['name'])
        histogram = collections.Counter()
        for deleted in itertools.combinations(range(n), n - 13):
            for signs in itertools.product((0, 1), repeat=n - 13):
                low = {i for i, sign in zip(deleted, signs) if not sign}
                high = set(deleted) - low
                projected = projection(gates, n, low, high)
                histogram[len(projected)] += 1
                if len(projected) <= 46:
                    unique[projected] = (parent['name'], sorted(low), sorted(high))
        tables[parent['name']] = dict(sorted(histogram.items()))
    seeds = sorted(unique)
    for net in seeds:
        if not sorts(net, 13):
            raise RuntimeError('projected seed is not a sorter')
    text = str(len(seeds)) + '\n' + ''.join(
        '13 ' + str(len(net)) + '\n' + ''.join(f'{a} {b}\n' for a, b in net)
        for net in seeds)
    (work / 'seeds.txt').write_text(text)
    (work / 'projection_counts.json').write_text(json.dumps(tables, sort_keys=True) + '\n')
    print('seeds', len(seeds), 'sizes', dict(collections.Counter(map(len, seeds))))
    compiler = ['g++', '-std=c++20', '-O3', '-Wall', '-Wextra', '-Wpedantic',
                '-Wconversion', '-Wshadow']
    subprocess.run(compiler + [str(ROOT / 'enumerate.cpp'), '-o', str(work / 'enumerate')], check=True)
    start = time.monotonic()
    subprocess.run([str(work / 'enumerate'), str(work / 'seeds.txt'),
                    str(work / 'certificate.json'), str(work / 'positive45.txt')], check=True)
    result = json.loads((work / 'certificate.json').read_text())
    result['candidates45'] = sum(len(net) for net in seeds if len(net) == 46)
    result['seeds_sha256'] = hashlib.sha256(text.encode()).hexdigest()
    result['projection_counts'] = tables
    (work / 'certificate.json').write_text(json.dumps(result, indent=2, sort_keys=True) + '\n')
    print('enumeration_seconds', round(time.monotonic() - start, 3))
    existing = ROOT / 'certificate.json'
    if existing.exists() and existing.read_bytes() != (work / 'certificate.json').read_bytes():
        raise RuntimeError('certificate mismatch')


if __name__ == '__main__':
    main()
