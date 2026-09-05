#!/usr/bin/env python3
"""Definition-level exact audit of the explicit 43-vertex partial realization.

This imports no solver or formula generator on its mathematical proof path.
It checks the actual graph, not an auxiliary assignment or aggregate primal.
"""
import argparse
from collections import Counter
from functools import lru_cache
import hashlib
from itertools import combinations, product
import json
from math import comb
from pathlib import Path

HERE = Path(__file__).resolve().parent
Y = (0,8,8,6,10,4,4,0)
PARENT_SHA = 'c5f5bcd1df4b52026d5e813d764865fc938905972b3fcd205c0b30eca8f5837e'


def require(condition, description):
    if not condition:
        raise ValueError(description)


def decode(document):
    require(document['format'] == 'r55-triple-degree-exact-mixed-graph-v1', 'format')
    text_rows = document['red_adjacency_hex']
    require(len(text_rows) == 43, 'graph order')
    require(all(type(row) is str and row and all(c in '0123456789abcdef' for c in row)
                for row in text_rows), 'hexadecimal adjacency encoding')
    rows = tuple(int(row,16) for row in text_rows)
    for u, row in enumerate(rows):
        require(0 <= row < 1 << 43 and not (row >> u & 1), 'loop or out-of-range bit')
        require(all((row >> v & 1) == (rows[v] >> u & 1) for v in range(43)), 'asymmetric adjacency')
    return rows


def mono_fives_literal(rows):
    red, blue = [], []
    for five in combinations(range(len(rows)), 5):
        colors = {bool(rows[u] >> v & 1) for u,v in combinations(five, 2)}
        if len(colors) == 1:
            (red if True in colors else blue).append(five)
    return tuple(red), tuple(blue)


def monochromatic_bitsets(rows, color, size=5):
    n = len(rows)
    universe = (1 << n)-1
    adjacency = rows if color else tuple(universe ^ row ^ (1 << u) for u,row in enumerate(rows))
    answer = []
    def visit(chosen, candidates):
        if len(chosen) == size:
            answer.append(chosen)
            return
        while candidates.bit_count() >= size-len(chosen):
            bit = candidates & -candidates
            candidates ^= bit
            vertex = bit.bit_length()-1
            visit(chosen+(vertex,), candidates & adjacency[vertex])
    visit((), universe)
    return tuple(answer)


@lru_cache(None)
def upper(a,b):
    require(a >= 1 and b >= 1, 'Ramsey parameters')
    if min(a,b) == 1:
        return 1
    x, y = upper(a-1,b), upper(a,b-1)
    return x+y-int(x % 2 == y % 2 == 0)


def local_profiles(rows):
    red_neighbors = tuple({v for v in range(len(rows)) if row >> v & 1} for row in rows)
    profiles = []
    universe = set(range(len(rows)))
    for u, neighbors in enumerate(red_neighbors):
        opposite = universe-neighbors-{u}
        red_edges = sum(v in red_neighbors[w] for w,v in combinations(sorted(neighbors),2))
        blue_edges = sum(v not in red_neighbors[w] for w,v in combinations(sorted(opposite),2))
        profiles.append((red_edges,blue_edges))
    return red_neighbors, tuple(profiles)


def inspect(document, check_parent=True):
    rows = decode(document)
    require(tuple(row.bit_count() for row in rows) == (20,)*3+(21,)*40, 'prescribed individual degrees')
    require(all(rows[u] >> v & 1 for u,v in combinations(range(3),2)), 'red exceptional triangle')
    signatures = tuple(row & 7 for row in rows[3:])
    require(tuple(signatures.count(s) for s in range(8)) == Y, 'prescribed signature multiplicities')
    require(signatures == tuple(s for s,n in enumerate(Y) for _ in range(n)), 'canonical cell labeling')
    if check_parent:
        raw = (HERE.parent/'ramsey_r55_external_root_lifting/CERTIFICATE.json').read_bytes()
        require(hashlib.sha256(raw).hexdigest() == PARENT_SHA, 'parent certificate provenance')
        matches = [record for record in json.loads(raw) if record['mask'] == 7 and tuple(record['y']) == Y]
        require(len(matches) == 1 and matches[0]['first_failed_stage'] is None, 'input not in retained parent cases')
    red_neighbors, profiles = local_profiles(rows)
    require(all(red <= 93 and blue <= 107 for red,blue in profiles[:3]), 'exceptional local edge-count caps')
    red_fives, blue_fives = mono_fives_literal(rows)
    require(red_fives == monochromatic_bitsets(rows, True), 'red five-set reconstruction mismatch')
    require(blue_fives == monochromatic_bitsets(rows, False), 'blue five-set reconstruction mismatch')
    require(all(min(five) >= 3 for five in red_fives+blue_fives), 'monochromatic five-set meeting E')

    all_vertices = set(range(43))
    root_count = lifted = external = 0
    min_slack = None
    sides = []
    for word in product(range(3), repeat=3):
        A = {i for i,value in enumerate(word) if value == 1}
        B = {i for i,value in enumerate(word) if value == 2}
        if not A | B:
            continue
        if any(v not in red_neighbors[u] for u,v in combinations(sorted(A),2)):
            continue
        if any(v in red_neighbors[u] for u,v in combinations(sorted(B),2)):
            continue
        S = {v for v in all_vertices-A-B if A <= red_neighbors[v] and not B & red_neighbors[v]}
        require(len(S) <= upper(5-len(A),5-len(B))-1, 'root-union capacity')
        root_count += 1
        if len(A) == len(B) == 1:
            sides.append(len(S))
        for u in all_vertices-A-B:
            if A <= red_neighbors[u]:
                slack = upper(4-len(A),5-len(B))-1-len(S & red_neighbors[u])
                require(slack >= 0, 'pointwise red external-root lifting')
                lifted += 1
                external += int(u not in S)
                min_slack = slack if min_slack is None else min(min_slack,slack)
            if not B & red_neighbors[u]:
                slack = upper(5-len(A),4-len(B))-1-len(S-red_neighbors[u]-{u})
                require(slack >= 0, 'pointwise blue external-root lifting')
                lifted += 1
                external += int(u not in S)
                min_slack = slack if min_slack is None else min(min_slack,slack)
        if len(A) == len(B) == 1 and len(S) in (15,16):
            edges = sum(v in red_neighbors[u] for u,v in combinations(sorted(S),2))
            lower, higher = (50,55) if len(S) == 15 else (58,62)
            require(lower <= edges <= higher, 'rooted density cap')

    # Report, rather than silently omit, the stronger requirements that fail.
    neighborhood_gaps = []
    for u in range(3):
        NR = red_neighbors[u]
        NB = all_vertices-NR-{u}
        red_four = sum(all(v in red_neighbors[w] for w,v in combinations(four,2))
                       for four in combinations(sorted(NR),4))
        blue_four = sum(all(v not in red_neighbors[w] for w,v in combinations(four,2))
                        for four in combinations(sorted(NB),4))
        require(red_four == blue_four == 0, 'mixed four-plus-root obstruction')
        neighborhood_gaps.append({'vertex': u,
            'blue_K5_in_red_neighborhood': sum(set(five) <= NR for five in blue_fives),
            'red_K5_in_blue_neighborhood': sum(set(five) <= NB for five in red_fives)})
    bad_central_caps = [u for u in range(3,43) if profiles[u][0] > 100 or profiles[u][1] > 100]
    cell_edges = Counter()
    for u,v in combinations(range(3,43),2):
        if v in red_neighbors[u]:
            cell_edges[tuple(sorted((rows[u]&7, rows[v]&7)))] += 1
    return {
        'order': 43, 'red_edges': sum(row.bit_count() for row in rows)//2,
        'degree_histogram': {'20':3,'21':40}, 'signature_vector': list(Y),
        'exceptional_local_profiles': [list(pair) for pair in profiles[:3]],
        'all_local_profiles': [list(pair) for pair in profiles],
        'mixed_five_sets_checked': comb(43,5)-comb(40,5),
        'all_five_sets_checked': comb(43,5),
        'monochromatic_fives_meeting_E': 0,
        'central_red_K5': len(red_fives), 'central_blue_K5': len(blue_fives),
        'first_red_K5': list(red_fives[0]) if red_fives else None,
        'first_blue_K5': list(blue_fives[0]) if blue_fives else None,
        'valid_root_pairs': root_count, 'pointwise_lifts': lifted,
        'genuinely_external_pointwise_lifts': external, 'minimum_lifting_slack': min_slack,
        'ordered_one_way_side_sizes': sorted(sides),
        'active_order15_or16_density_sides': sum(size in (15,16) for size in sides),
        'full_neighborhood_gaps': neighborhood_gaps,
        'central_vertices_failing_hard_local_caps': bad_central_caps,
        'aggregate_cell_edges': [[a,b,value] for (a,b),value in sorted(cell_edges.items())],
        'scope': 'degree-exact mixed-clique/root-lifting realization; NOT a Ramsey(5,5;43) graph',
    }


def controls(document):
    cases = 0
    edges = tuple(combinations(range(5),2))
    for mask in range(1024):
        rows = [0]*5
        for bit,(u,v) in enumerate(edges):
            if mask >> bit & 1:
                rows[u] |= 1 << v
                rows[v] |= 1 << u
        red, blue = mono_fives_literal(rows)
        require(red == monochromatic_bitsets(rows,True) and blue == monochromatic_bitsets(rows,False),
                'small graph algorithms disagree')
        require(bool(red) == (mask == 1023) and bool(blue) == (mask == 0), 'small monochromatic control')
        cases += 1
    # Shape, graph semantics, and the full Ramsey target are distinct gates.
    rejected = []
    for name, mutate in (
        ('missing_vertex', lambda r: r.pop()),
        ('self_loop', lambda r: r.__setitem__(0,format(int(r[0],16) | 1,'x'))),
        ('asymmetric_edge', lambda r: r.__setitem__(3,format(int(r[3],16) ^ (1 << 4),'x'))),
    ):
        mutant = {'format': document['format'], 'red_adjacency_hex': list(document['red_adjacency_hex'])}
        mutate(mutant['red_adjacency_hex'])
        try:
            decode(mutant)
        except ValueError:
            rejected.append(name)
        else:
            raise ValueError('bad graph representation accepted')
    rows = decode(document)
    altered = list(rows)
    altered[3] ^= 1 << 4
    altered[4] ^= 1 << 3
    mutant = {'format': document['format'], 'red_adjacency_hex': [format(r,'x') for r in altered]}
    try:
        inspect(mutant, check_parent=False)
    except ValueError:
        rejected.append('changed_individual_degrees')
    else:
        raise ValueError('changed degree sequence accepted')
    try:
        red,blue = mono_fives_literal(rows)
        require(not red and not blue, 'not a target Ramsey graph')
    except ValueError:
        rejected.append('false_full_Ramsey_claim')
    else:
        raise ValueError('unexpected target; perform full campaign completion audit')
    return {'small_graphs': cases, 'negative_controls_rejected': rejected}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--graph', type=Path, default=HERE/'GRAPH.json')
    parser.add_argument('--report', type=Path)
    args = parser.parse_args()
    document = json.loads(args.graph.read_text())
    report = inspect(document)
    report['controls'] = controls(document)
    report['graph_sha256'] = hashlib.sha256(args.graph.read_bytes()).hexdigest()
    if args.report:
        args.report.write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')
    print(json.dumps({key: report[key] for key in (
        'order','red_edges','exceptional_local_profiles','monochromatic_fives_meeting_E',
        'central_red_K5','central_blue_K5','pointwise_lifts','full_neighborhood_gaps',
        'graph_sha256','scope')},sort_keys=True))


if __name__ == '__main__':
    main()
