#!/usr/bin/env python3
"""Definition-level audit of the 98 anchor cubes and their exact CNF layering."""
from itertools import combinations, combinations_with_replacement, product
from pathlib import Path
import argparse
import hashlib
import json
import random

ROOT = Path(__file__).resolve().parent
PARENT = ROOT.parent / 'ramsey_r55_order3_ten_cycle_obstruction'
BASE_HEADER = b'p cnf 28950 927000\n'
CUBE_HEADER = b'p cnf 28950 927027\n'
BASE_SHA256 = 'f01c990a1dae17fb7bc1cd633d785cd819ba9f4d1a1eeacd69b4034663af104e'


def require(condition, message):
    if not condition:
        raise ValueError(message)


def load_weights():
    return json.loads((PARENT / 'anchor_r4.json').read_text())['weights']


def require_parent():
    manifest = json.loads((ROOT / 'parent_manifest.json').read_text())
    for name, digest in manifest['files'].items():
        require(hashlib.sha256((PARENT / name).read_bytes()).hexdigest() == digest,
                'parent source mismatch: ' + name)


def orbit_edge_ids():
    """Recover primary variable names by iterating actual unordered pairs."""
    sigma = [3 * (v // 3) + (v + 1) % 3 if v < 30 else v for v in range(43)]
    unseen = set(combinations(range(43), 2))
    groups = []
    while unseen:
        edge = min(unseen)
        orbit = set()
        while edge not in orbit:
            orbit.add(edge)
            edge = tuple(sorted(sigma[v] for v in edge))
        unseen.difference_update(orbit)
        groups.append(sorted(orbit))
    cross = [g for g in groups if g[0][1] < 30 and g[0][0] // 3 != g[0][1] // 3]
    fixed = [g for g in groups if g[0][0] >= 30]
    links = [g for g in groups if g[0][0] < 30 <= g[0][1]]
    cross.sort(key=lambda g: g[0])
    fixed.sort(key=lambda g: g[0])
    links.sort(key=lambda g: (g[0][1], g[0][0]))
    require((len(groups), len(cross), len(fixed), len(links)) == (353, 135, 78, 130),
            'wrong pair-orbit decomposition')
    result = {}
    for variable, orbit in enumerate(cross + fixed + links, 1):
        for edge in orbit:
            result[edge] = variable
    return result


def coverage():
    stored = load_weights()
    arithmetic = set()
    labeled_count = 0
    for weights in product(range(4), repeat=9):
        if 3 in weights[:3]:
            continue
        # Definition-level fixed-neighbor/degree feasibility, independent of
        # the deficit filter used in the second enumeration.
        if not any(a + 3 * weights.count(3) <= 4 and 18 <= 2 + a + sum(weights) <= 24
                   for a in range(14)):
            continue
        labeled_count += 1
        arithmetic.add(tuple(sorted(weights[:3]) + sorted(weights[3:])))
    partitions = []
    for red in combinations_with_replacement(range(3), 3):
        for blue in combinations_with_replacement(range(4), 6):
            weights = red + blue
            deficit = sum(2 - w + 3 * (w == 3) for w in weights)
            if deficit <= 6 and weights.count(3) <= 1:
                partitions.append(weights)
    require(sorted(arithmetic) == partitions == [tuple(w) for w in stored], 'cube coverage mismatch')
    require(len(partitions) == 98, 'wrong cube count')
    for bits in product((0, 1), repeat=3):
        rotations = {bits[s:] + bits[:s] for s in range(3)}
        require(tuple(sorted(bits, reverse=True)) in rotations, 'phase normalization failed')
    ids = orbit_edge_ids()
    for index, weights in enumerate(stored):
        units = [ids[0, 3 * j + t] * (1 if t < weights[j - 1] else -1)
                 for j in range(1, 10) for t in range(3)]
        direct = [(1 + 3 * j + t) * (1 if t < w else -1)
                  for j, w in enumerate(weights) for t in range(3)]
        require(units == direct and len({abs(x) for x in units}) == 27, 'cube variable meaning')
        require(all(index == other or weights != row for other, row in enumerate(stored)), 'duplicate cube')
    return {'normalized_cubes': 98, 'labeled_feasible_weight_vectors': labeled_count,
            'binary_anchor_words_checked': 8, 'unit_literals_per_cube': 27}


def normalization():
    """Relabel actual invariant graphs, including every four-red color choice."""
    rng = random.Random(55031098)
    ids = orbit_edge_ids()
    pairs = list(combinations(range(43), 2))
    sigma = [3 * (v // 3) + (v + 1) % 3 if v < 30 else v for v in range(43)]
    tested = 0
    for reds in combinations(range(10), 4):
        values = {x: bool(rng.randrange(2)) for x in set(ids.values())}
        graph = {edge: values[ids[edge]] if edge in ids else edge[0] // 3 in reds for edge in pairs}
        order = list(reds) + [i for i in range(10) if i not in reds]
        mapping = [3 * i + t for i in order for t in range(3)] + list(range(30, 43))

        def color(u, v):
            return graph[tuple(sorted((mapping[u], mapping[v])))]

        for j in range(1, 10):
            old = mapping[3 * j:3 * j + 3]
            for shift in range(3):
                mapping[3 * j:3 * j + 3] = old[shift:] + old[:shift]
                word = tuple(color(0, 3 * j + t) for t in range(3))
                if word == tuple(sorted(word, reverse=True)):
                    break
            else:
                raise ValueError('missing phase representative')
        nonanchor = sorted(range(1, 10), key=lambda j: (j >= 4, sum(color(0, 3 * j + t) for t in range(3))))
        blocks = [mapping[3 * j:3 * j + 3] for j in nonanchor]
        mapping[3:30] = [v for block in blocks for v in block]
        fixed = sorted(range(30, 43), key=lambda f: tuple(color(3 * j, f) for j in range(10)))
        mapping[30:] = [mapping[f] for f in fixed]
        require(sorted(mapping) == list(range(43)), 'not a relabeling')
        require(all(mapping[sigma[v]] == sigma[mapping[v]] for v in range(43)), 'not in the centralizer')
        words = [tuple(color(0, 3 * j + t) for t in range(3)) for j in range(1, 10)]
        require(all(word == tuple(sorted(word, reverse=True)) for word in words), 'phase lost')
        weights = [sum(word) for word in words]
        require(weights[:3] == sorted(weights[:3]) and weights[3:] == sorted(weights[3:]), 'weight ordering')
        signatures = [tuple(color(3 * j, f) for j in range(10)) for f in range(30, 43)]
        require(signatures == sorted(signatures), 'fixed signature ordering')
        require(all(color(3 * j, 3 * j + 1) == (j < 4) for j in range(10)), 'internal color lost')
        require(all(color(u, v) == color(sigma[u], sigma[v]) for u, v in pairs), 'invariance lost')
        tested += 1
    return tested


def check_cube(base, cube, index):
    require(0 <= index < 98, 'cube index out of range')
    ids = orbit_edge_ids()
    weights = load_weights()[index]
    units = [ids[0, 3 * j + t] * (1 if t < weights[j - 1] else -1)
             for j in range(1, 10) for t in range(3)]
    base_hash = hashlib.sha256()
    cube_hash = hashlib.sha256()
    with base.open('rb') as source, cube.open('rb') as target:
        header = source.readline()
        require(header == BASE_HEADER, 'wrong parent header')
        base_hash.update(header)
        header = target.readline()
        require(header == CUBE_HEADER, 'wrong cube header')
        cube_hash.update(header)
        while data := source.read(1024 * 1024):
            base_hash.update(data)
            got = target.read(len(data))
            require(got == data, 'cube changed a parent clause')
            cube_hash.update(got)
        tail = target.read()
        require(tail == ''.join(f'{lit} 0\n' for lit in units).encode(), 'wrong anchor units or trailing data')
        cube_hash.update(tail)
    require(base_hash.hexdigest() == BASE_SHA256, 'wrong complete parent formula')
    return {'bytes': cube.stat().st_size, 'sha256': cube_hash.hexdigest()}


def audit():
    require_parent()
    result = coverage()
    result['actual_graph_relabelings'] = normalization()
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--base', type=Path)
    parser.add_argument('--cube', type=Path)
    parser.add_argument('--index', type=int)
    args = parser.parse_args()
    result = audit()
    if args.base is not None or args.cube is not None or args.index is not None:
        require(args.base is not None and args.cube is not None and args.index is not None, 'need all cube arguments')
        result['cube'] = check_cube(args.base, args.cube, args.index)
    print(json.dumps(result, sort_keys=True))
