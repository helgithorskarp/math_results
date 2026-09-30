#!/usr/bin/env python3
"""Certify the three seven-edge high-core obstructions on seventeen points."""
from collections import Counter
from hashlib import sha256
from itertools import combinations, permutations, product
from pathlib import Path
import argparse
import json
import time

from check_unit_eight import rejection_tree, CoverFound, Incomplete

HERE = Path(__file__).resolve().parent
HIGH = tuple(range(5))
LOW = tuple(range(5, 17))
ATTACHED = tuple(range(5, 11))
MATCHED = tuple(range(11, 17))
ALL_PAIRS = tuple(combinations(range(17), 2))
NAMES = ('triangle', 'path', 'wedge_edge')


def require(condition, message):
    if not condition:
        raise ValueError(message)


def encoded(value):
    return (json.dumps(value, sort_keys=True, separators=(',', ':')) + '\n').encode('ascii')


def digest(value):
    return sha256(encoded(value)).hexdigest()


def pairs(q):
    return frozenset(combinations(q, 2))


def moved(q, permutation):
    return tuple(sorted(permutation[x] for x in q))


def action(prefix, permutation):
    return tuple(sorted(moved(q, permutation) for q in prefix))


def model(name):
    covered = {'triangle': ((0, 1), (0, 2), (1, 2)),
               'path': ((0, 1), (1, 2), (2, 3)),
               'wedge_edge': ((0, 1), (1, 2), (3, 4))}[name]
    leaves, next_point = {}, 5
    for h in HIGH:
        degree = sum(h in e for e in covered)
        leaves[h] = tuple(range(next_point, next_point + degree))
        next_point += degree
    require(next_point == 11, 'six attached leaves required')
    leave = frozenset((set(combinations(HIGH, 2)) - set(covered)) |
                      {(h, x) for h in HIGH for x in leaves[h]} |
                      {(11, 12), (13, 14), (15, 16)})
    require(len(leave) == 16, 'leave has wrong size')
    return {'name': name, 'covered': covered, 'leaves': leaves, 'leave': leave}


def legal(m, prefix):
    used = set()
    for q in prefix:
        require(len(q) == len(set(q)) == 4 and tuple(sorted(q)) == q, 'invalid quadruple')
        e = pairs(q)
        if e & (m['leave'] | used):
            return False
        used.update(e)
    return True


def leave_group(m):
    maps = []
    for h in permutations(HIGH):
        if {moved(e, h) for e in m['covered']} != set(m['covered']):
            continue
        fibers = [tuple(permutations(m['leaves'][h[i]])) for i in HIGH]
        for attached_maps in product(*fibers):
            for order in permutations(range(3)):
                for flips in product(range(2), repeat=3):
                    p = list(h) + list(LOW)
                    for i in HIGH:
                        for x, y in zip(m['leaves'][i], attached_maps[i]):
                            p[x] = y
                    for i in range(3):
                        for j in range(2):
                            p[11 + 2*i + j] = 11 + 2*order[i] + (j ^ flips[i])
                    p = tuple(p)
                    require(len(set(p)) == 17 and {moved(e, p) for e in m['leave']} == set(m['leave']),
                            'map is not an actual leave permutation')
                    maps.append(p)
    expected = 4608 if m['name'] == 'triangle' else 384
    require(len(maps) == len(set(maps)) == expected, 'wrong leave group size')
    require(tuple(range(17)) in maps, 'identity missing')
    return tuple(sorted(maps))


def quotient(raw, group):
    unseen, records = set(raw), []
    while unseen:
        root = min(unseen)
        orbit = {action(root, p) for p in group}
        require(orbit <= raw and orbit <= unseen, 'invalid or overlapping orbit')
        stabilizer = tuple(p for p in group if action(root, p) == root)
        require(len(orbit) * len(stabilizer) == len(group), 'orbit-stabilizer failure')
        unseen.difference_update(orbit)
        records.append((root, len(orbit), stabilizer))
    require(sum(n for _, n, _ in records) == len(raw), 'incomplete quotient')
    return records


def double_tails(m):
    options = [tuple((a, b) + t for t in combinations(LOW, 2) if legal(m, ((a, b) + t,)))
               for a, b in m['covered']]
    return frozenset(p for p in product(*options) if legal(m, p))


def zero_frames(m, tail, node_limit=200000, seconds=10):
    """Enumerate a complete multiset cover by three zero-high quadruples."""
    counts = Counter(ATTACHED)
    for q in tail:
        counts.update(x for x in q if x in LOW)
    require(sum(counts.values()) == 12, 'wrong zero incidence total')
    forbidden = m['leave'] | frozenset().union(*(pairs(q) for q in tail))
    columns = tuple(q for q in combinations(sorted(counts), 4) if not pairs(q) & forbidden)
    edges = tuple(pairs(q) for q in columns)
    bypoint = {x: tuple(i for i, q in enumerate(columns) if x in q) for x in counts}
    found, nodes, start = set(), 0, time.monotonic()

    def visit(left, used, chosen):
        nonlocal nodes
        nodes += 1
        if nodes > node_limit or (nodes % 128 == 0 and time.monotonic() - start > seconds):
            raise Incomplete('INCOMPLETE: zero-frame carrier guard reached')
        if len(chosen) == 2:
            if len(left) != 4 or set(left.values()) != {1}:
                return
            q = tuple(sorted(left))
            if not pairs(q) & (forbidden | used):
                found.add(tuple(sorted(tuple(columns[i] for i in chosen) + (q,))))
            return
        require(bool(left), 'unexpected empty zero incidence multiset')
        _, pivot = min((sum(not edges[i] & used and all(left.get(x, 0) for x in columns[i])
                           for i in bypoint[v]), v) for v in left)
        for i in bypoint[pivot]:
            if edges[i] & used or any(not left.get(x, 0) for x in columns[i]):
                continue
            remaining = Counter(left)
            for x in columns[i]:
                remaining[x] -= 1
                if not remaining[x]:
                    del remaining[x]
            visit(remaining, used | edges[i], chosen + (i,))

    visit(counts, frozenset(), ())
    for z in found:
        require(legal(m, tail + z) and Counter(x for q in z for x in q) == counts,
                'invalid zero-frame carrier element')
    return frozenset(found)


def triple_frames(m):
    raw = set()
    for x in MATCHED:
        for first in combinations(ATTACHED, 3):
            second = tuple(v for v in ATTACHED if v not in first)
            z1, z2 = tuple(sorted((x,) + first)), tuple(sorted((x,) + second))
            if z1 < z2:
                prefix = ((0, 1, 2, x), z1, z2)
                require(legal(m, prefix), 'invalid triple-high prefix')
                raw.add(prefix)
    return frozenset(raw)


def exact_case(m, branch, prefix, orbit, stabilizer, index):
    require(legal(m, prefix), 'invalid fixed prefix')
    used = frozenset().union(*(pairs(q) for q in prefix))
    rows = tuple(e for e in ALL_PAIRS if e not in m['leave'] | used)
    remaining = set(rows)
    columns = tuple((h,) + t for h in HIGH for t in combinations(LOW, 3)
                    if pairs((h,) + t) <= remaining)
    require(len(rows) == (102 if branch == 'triple' else 84), 'wrong pair count')
    return {'index': index, 'model': m['name'], 'branch': branch,
            'fixed_quads': prefix, 'orbit_size': orbit, 'stabilizer_order': stabilizer,
            'rows': rows, 'columns': columns, 'input_sha256': digest([prefix, rows, columns])}


def generate():
    cases, summaries, carriers = [], [], {}
    for name in NAMES:
        m = model(name)
        g = leave_group(m)
        raw = double_tails(m)
        tail_records = quotient(raw, g)
        fibers = []
        carriers[name] = {'group': g, 'tails': raw, 'zeros': {}}
        if name == 'triangle':
            triple = triple_frames(m)
            q = quotient(triple, g)
            carriers[name]['triples'] = triple
            for prefix, n, stabilizer in q:
                cases.append(exact_case(m, 'triple', prefix, n, len(stabilizer), len(cases)))
            summaries.append({'model': name, 'branch': 'triple', 'group_order': len(g),
                              'group_sha256': digest(g), 'raw_prefixes': len(triple),
                              'raw_prefixes_sha256': digest(sorted(triple)), 'prefix_orbits': len(q)})
        first = len(cases)
        weight = 0
        for tail, n, stabilizer in tail_records:
            zero = zero_frames(m, tail)
            zq = quotient(zero, stabilizer)
            carriers[name]['zeros'][tail] = zero
            weight += n * len(zero)
            fibers.append([tail, n, len(stabilizer), sorted(zero)])
            for z, zn, zstabilizer in zq:
                cases.append(exact_case(m, 'double', tail + z, n * zn, len(zstabilizer), len(cases)))
        summaries.append({'model': name, 'branch': 'double', 'group_order': len(g),
                          'group_sha256': digest(g), 'raw_tails': len(raw),
                          'raw_tails_sha256': digest(sorted(raw)), 'tail_orbits': len(tail_records),
                          'raw_prefixes': weight, 'prefix_orbits': len(cases) - first,
                          'zero_fibers_sha256': digest(fibers)})
    require([s['prefix_orbits'] for s in summaries] == [2, 205, 1486, 1995], 'unexpected case census')
    return cases, summaries, carriers


def build():
    cases, summaries, _ = generate()
    trees, nodes = [], []
    for c in cases:
        tree, n = rejection_tree(c['rows'], c['columns'])
        trees.append(tree)
        nodes.append(n)
    stream = digest([[c['fixed_quads'], c['rows'], c['columns']] for c in cases])
    certificate = {'schema': 'all-unit-seven-cores-v1', 'carrier_summary_sha256': digest(summaries),
                   'input_stream_sha256': stream, 'trees': trees}
    branch_reports = []
    for summary in summaries:
        selected = [c for c in cases if c['model'] == summary['model'] and c['branch'] == summary['branch']]
        counts = [nodes[c['index']] for c in selected]
        branch_reports.append(summary | {'nodes': sum(counts), 'maximum_nodes_per_case': max(counts),
                                        'rows': len(selected[0]['rows']),
                                        'column_range': [min(len(c['columns']) for c in selected),
                                                         max(len(c['columns']) for c in selected)]})
    report = {'agent': 'six-code-1', 'role': 'researcher', 'status': 'COMPLETE_EXACT_NO_COVERS',
              'branches': branch_reports, 'cases': len(cases), 'nodes': sum(nodes),
              'maximum_nodes_per_case': max(nodes), 'nodes_per_case_sha256': digest(nodes),
              'input_stream_sha256': stream, 'carrier_summary_sha256': digest(summaries),
              'certificate_sha256': sha256(encoded(certificate)).hexdigest(),
              'certificate_bytes': len(encoded(certificate)), 'global_72_word_exclusion': False,
              'independent_peer_review': False, 'ordinary_bridges_formalized': False}
    return certificate, report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write-certificate', action='store_true')
    args = parser.parse_args()
    certificate, report = build()
    if args.write_certificate:
        (HERE / 'unit_seven_certificate.json').write_bytes(encoded(certificate))
        (HERE / 'unit_seven_expected.json').write_bytes(encoded(report))
    else:
        require((HERE / 'unit_seven_certificate.json').read_bytes() == encoded(certificate),
                'certificate differs entry by entry')
        require(json.loads((HERE / 'unit_seven_expected.json').read_text()) == report, 'expected report differs')
    print(json.dumps(report, sort_keys=True, indent=2))


if __name__ == '__main__':
    main()
