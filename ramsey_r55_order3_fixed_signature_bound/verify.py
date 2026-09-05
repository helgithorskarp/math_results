#!/usr/bin/env python3
"""Exact fixed-signature census and literal sharp local fixture verification."""
from itertools import combinations, product
from pathlib import Path
from collections import Counter
import argparse
import hashlib
import json

ROOT = Path(__file__).resolve().parent
CORE = ROOT.parent / 'ramsey_r55_order3_ten_cycle_phase_sweep' / 'minority_core.edges'
CORE_SHA = '8a411934f12e1403f79b9087f5bace3e865be908e1a94861c2baecee8844e9c4'
SIGNATURES = tuple(s for s in range(1, 16) if s.bit_count() <= 2)


def require(ok, message):
    if not ok:
        raise ValueError(message)


def read_edges(path):
    lines = path.read_text().splitlines()
    require(bool(lines), 'empty graph')
    n, m = map(int, lines[0].split())
    edges = [tuple(map(int, line.split())) for line in lines[1:]]
    require(len(edges) == m and all(len(e) == 2 and 0 <= e[0] < e[1] < n for e in edges), 'graph dimensions')
    require(edges == sorted(set(edges)), 'duplicate or unsorted edges')
    return n, set(edges)


def core_graph():
    require(hashlib.sha256(CORE.read_bytes()).hexdigest() == CORE_SHA, 'changed core fixture')
    n, red = read_edges(CORE)
    require(n == 12 and len(red) == 42, 'core size')
    # Check the definition separately from its hash.
    for a, b in combinations(range(12), 2):
        i, u = divmod(a, 3)
        j, v = divmod(b, 3)
        expected = True if i == j else ((v-u) % 3 == 0 if (i, j) in ((0, 1), (2, 3)) else (v-u) % 3 in (0, 1))
        require(((a, b) in red) == expected, 'wrong defined core')
    require(not any(all(e not in red for e in combinations(vs, 2))
                    for vs in combinations(range(12), 3)), 'core has blue triangle')
    for i, j in combinations(range(4), 2):
        require(any((a, b) not in red for a in range(3*i, 3*i+3) for b in range(3*j, 3*j+3)), 'missing cross blue edge')
    fours = ((0, 3, 6, 7), (0, 3, 9, 10), (0, 2, 6, 9), (3, 5, 6, 9))
    require({tuple(sorted({v//3 for v in vs})) for vs in fours} == set(combinations(range(4), 3)), 'three-cycle support cover')
    require(all(all(e in red for e in combinations(vs, 2)) for vs in fours), 'wrong displayed red K4')
    return red


def families():
    """All pairwise-intersecting nonempty signature families, with capacities."""
    answer = []
    for mask in range(1, 1 << len(SIGNATURES)):
        indices = [i for i in range(10) if mask >> i & 1]
        if not all(SIGNATURES[i] & SIGNATURES[j] for i, j in combinations(indices, 2)):
            continue
        union = 0
        for i in indices:
            union |= SIGNATURES[i]
        answer.append((tuple(indices), max(2, union.bit_count())))
    require(len(answer) == 58, 'signature family count')
    return answer


def forced_blue(core, counts):
    """Only forced blue edges: an absent edge here may be red OR undetermined."""
    signatures = [0] * (13-sum(counts)) + [s for s, n in zip(SIGNATURES, counts) for _ in range(n)]
    require(len(signatures) == 13, 'fixed signature multiplicity')
    blue = [0] * 25

    def add(a, b):
        blue[a] |= 1 << b
        blue[b] |= 1 << a

    for a, b in combinations(range(12), 2):
        if (a, b) not in core:
            add(a, b)
    for f, signature in enumerate(signatures, 12):
        for v in range(12):
            if not (signature >> (v//3) & 1):
                add(v, f)
    for a, b in combinations(range(13), 2):
        if signatures[a] & signatures[b]:
            add(a+12, b+12)
    return blue


def has_clique(adj, size):
    def visit(candidates, need):
        if need == 0:
            return True
        while candidates.bit_count() >= need:
            bit = candidates & -candidates
            candidates ^= bit
            v = bit.bit_length()-1
            if visit(candidates & adj[v], need-1):
                return True
        return False
    return visit((1 << len(adj))-1, size)


def census(core):
    rows = families()
    histogram = Counter()
    digest = hashlib.sha256()
    equality = []
    total = 0
    literal_graphs = 0
    for counts in product(range(3), repeat=10):
        total += 1
        feasible = sum(counts) <= 13 and all(sum(counts[i] for i in ids) <= cap for ids, cap in rows)
        # Independent construction of the actual forced-edge graph, with no
        # signature-family capacity or union-size calculation in this branch.
        literal = False
        if sum(counts) <= 13:
            literal_graphs += 1
            literal = not has_clique(forced_blue(core, counts), 5)
        require(feasible == literal, 'family/graph disagreement: '+repr(counts))
        if not feasible:
            continue
        mapping = dict(zip(SIGNATURES, counts))
        X = sum(mapping[1 << i] for i in range(4))
        Y = sum(mapping[(1 << i) | (1 << j)] for i, j in combinations(range(4), 2))
        require(X+2*Y <= 16 and 3*X+2*Y <= 24 and X+Y <= 10, 'hand inequality audit')
        z = 13-X-Y
        histogram[z] += 1
        digest.update((str(z)+' '+','.join(map(str, counts))+'\n').encode())
        if z == 3:
            equality.append(list(counts))
    require(total == 59049 and sum(histogram.values()) == 1868, 'census dimensions')
    require(equality == [[1]*10], 'equality pattern')
    return {'assignments_checked': total, 'literal_forced_graphs_checked': literal_graphs,
            'intersecting_signature_families': len(rows), 'surviving_multiplicity_vectors': sum(histogram.values()),
            'survivor_stream_sha256': digest.hexdigest(),
            'histogram_by_empty_signature_count': dict(sorted(histogram.items())),
            'equality_nonempty_counts': equality[0], 'equality_empty_count': 3,
            'survivors_are_graph_realizations': False}


def inspect_fixture(core, path):
    n, edges = read_edges(path)
    require(n == 25 and len(edges) == 132, 'sharp fixture size')
    require({e for e in edges if e[1] < 12} == core, 'fixture changed minority core')
    signatures = []
    for f in range(12, 25):
        s = 0
        for i in range(4):
            values = [(v, f) in edges for v in range(3*i, 3*i+3)]
            require(len(set(values)) == 1, 'nonuniform fixed incidence')
            if values[0]:
                s |= 1 << i
        signatures.append(s)
    require(signatures == [0]*3+list(SIGNATURES), 'sharp signature pattern')
    sigma = [3*(v//3)+(v+1) % 3 if v < 12 else v for v in range(25)]
    require(all((e in edges) == (tuple(sorted(sigma[v] for v in e)) in edges)
                for e in combinations(range(25), 2)), 'fixture not invariant')
    bad = []
    checked = 0
    for vs in combinations(range(25), 5):
        checked += 1
        if len({e in edges for e in combinations(vs, 2)}) == 1:
            bad.append(vs)
    require(not bad and checked == 53130, 'fixture has monochromatic K5: '+repr(bad[:1]))
    return {'vertices': n, 'red_edges': len(edges), 'five_sets_checked': checked,
            'red_degrees': [sum(v in e for e in edges) for v in range(n)],
            'fixed_signatures': signatures, 'automorphism_cycle_type': '1^13 3^4',
            'local_bound_attained': True, 'is_a_43_vertex_target': False}


def negative_controls(core):
    checks = []
    # A single signature repeated three times forces a blue K5.
    counts = [0]*10
    counts[0] = 3
    require(has_clique(forced_blue(core, counts), 5), 'missed blue triangle plus core edge')
    checks.append('three_singleton_copies')
    # Three pair signatures on a three-element support cannot have four copies.
    counts = [0]*10
    for s, n in ((3, 2), (5, 1), (6, 1)):
        counts[SIGNATURES.index(s)] = n
    require(has_clique(forced_blue(core, counts), 5), 'missed blue K4 plus core vertex')
    checks.append('four_intersecting_copies_on_three_indices')
    counts = [1]*10
    require(not has_clique(forced_blue(core, counts), 5), 'equality forced-blue control failed')
    # Adding a red edge inside the common red neighborhood of triangle 0
    # creates an explicit red K5 in the literal positive fixture.
    _, edges = read_edges(ROOT / 'sharp25.edges')
    fixed = [f for f in range(12, 25) if (0, f) in edges]
    f, g = fixed[:2]
    require((f, g) not in edges, 'chosen corruption was already red')
    corrupted = edges | {(f, g)}
    require(all(e in corrupted for e in combinations((0, 1, 2, f, g), 2)), 'fixture corruption not detected')
    checks.append('red_edge_in_common_neighborhood')
    return checks


def clique_controls():
    # Definition-level cross-check for every labeled graph on five vertices.
    pairs = list(combinations(range(5), 2))
    for mask in range(1 << len(pairs)):
        adj = [0]*5
        edges = set()
        for i, (a, b) in enumerate(pairs):
            if mask >> i & 1:
                edges.add((a, b))
                adj[a] |= 1 << b
                adj[b] |= 1 << a
        for k in range(1, 6):
            direct = any(all(e in edges for e in combinations(vs, 2)) for vs in combinations(range(5), k))
            require(has_clique(adj, k) == direct, 'clique recursion mismatch')
    return 5120


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--report', type=Path)
    args = parser.parse_args()
    core = core_graph()
    report = {'signature_bit_order': [0, 1, 2, 3], 'nonempty_signature_masks': list(SIGNATURES),
              'census': census(core), 'fixture': inspect_fixture(core, ROOT / 'sharp25.edges'),
              'negative_controls': negative_controls(core), 'small_clique_checks': clique_controls()}
    if args.report:
        args.report.write_text(json.dumps(report, indent=2, sort_keys=True)+'\n')
    print(json.dumps({'surviving_vectors': report['census']['surviving_multiplicity_vectors'],
                      'minimum_empty_fixed_vertices': report['census']['equality_empty_count'],
                      'equality_pattern_unique': True, 'literal_fixture_vertices': 25,
                      'monochromatic_five_sets_in_fixture': 0}, sort_keys=True))


if __name__ == '__main__':
    main()
