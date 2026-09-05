#!/usr/bin/env python3
"""Exact rooted density-15 proof and reusable common-root inequality audits."""
import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path
import census
import fast_search
import reference_search
import literal_search

HERE = Path(__file__).resolve().parent
require = census.require


def decode(H, B, rows):
    n, m = len(H), len(B)
    root = n + m
    adj = [set() for _ in range(root + 1)]
    for i in range(n):
        adj[i] = {j for j in range(n) if H[i] >> j & 1} | {root}
        adj[i] |= {n + b for b in range(m) if rows[i] >> b & 1}
        adj[root].add(i)
    for b in range(m):
        adj[n + b] = {n + c for c in range(m) if B[b] >> c & 1}
        adj[n + b] |= {i for i in range(n) if rows[i] >> b & 1}
    return adj


def check_graph(adj, minimum, maximum, threshold):
    require(all(i not in adj[i] and all((j in adj[i]) == (i in adj[j])
                for j in range(len(adj))) for i in range(len(adj))), 'simple undirected graph')
    require(all(minimum <= len(s) <= maximum for s in adj), 'literal degree bounds')
    edges = sum(map(len, adj)) // 2
    require(edges >= threshold, 'literal edge threshold')
    require(all(len({b in adj[a] for a, b in combinations(S, 2)}) > 1
                for S in combinations(range(len(adj)), 4)), 'literal monochromatic four-set')
    return edges


def constraints_audit():
    # Inspect each of the 64 colorings of four literal vertices, for each
    # possible split between H and B. Compare the bit-mask predicates with
    # the definition (all six edges equal), without using either search.
    tested = Counter()
    for k in (1, 2, 3):
        for mask in range(64):
            adj = census.graph(4, mask)
            literal = mask in (0, 63)
            rows = [sum(1 << (b - k) for b in range(k, 4) if adj[i] >> b & 1)
                    for i in range(k)]
            if k == 1:
                red_triangle = all(adj[a] >> b & 1 for a, b in combinations(range(1, 4), 2))
                blue_triangle = all(not (adj[a] >> b & 1) for a, b in combinations(range(1, 4), 2))
                rejected = (red_triangle and rows[0] == 7) or (blue_triangle and rows[0] == 0)
            elif k == 2:
                color = bool(adj[0] >> 1 & 1)
                common = rows[0] & rows[1] if color else 3 ^ (rows[0] | rows[1])
                rejected = common == 3 and bool(adj[2] >> 3 & 1) == color
            else:
                # Red H triangles have already been forbidden in the census.
                if all(adj[a] >> b & 1 for a, b in combinations(range(3), 2)):
                    continue
                blue = all(not (adj[a] >> b & 1) for a, b in combinations(range(3), 2))
                rejected = blue and (rows[0] | rows[1] | rows[2]) == 0
            require(bool(rejected) == literal, ('four-set truth table', k, mask))
            tested[k] += 1
    return dict(tested)


def controls():
    rook = [{j for j in range(9) if i != j and (i // 3 == j // 3 or i % 3 == j % 3)}
            for i in range(9)]
    hs, bs = sorted(rook[0]), sorted(set(range(1, 9)) - rook[0])
    H = tuple(sum(1 << j for j, w in enumerate(hs) if w in rook[v]) for v in hs)
    B = tuple(sum(1 << j for j, w in enumerate(bs) if w in rook[v]) for v in bs)
    actual = tuple(sum(1 << j for j, w in enumerate(bs) if w in rook[v]) for v in hs)
    first = fast_search.search(H, B, 18, minimum=4, maximum=4)
    second = reference_search.search(H, B, 18, minimum=4, maximum=4)
    require(first['solutions'] == second['solutions'] and len(first['solutions']) == 82
            and actual in first['solutions'], 'complete positive rook model set')
    literal = literal_search.search(H, B, 18, minimum=4, maximum=4)
    require(first['solutions'] == literal['solutions'], 'literal complete positive model agreement')
    for rows in first['solutions']:
        check_graph(decode(H, B, rows), 4, 4, 18)
    # A literal edge-list fixture proves sharpness without catalog completeness.
    edges = [tuple(map(int, line.split())) for line in (HERE / 'sharp15.edges').read_text().splitlines()]
    require(len(edges) == len(set(edges)) == 55 and all(0 <= a < b < 15 for a, b in edges), 'sharp fixture format')
    adj = [set() for _ in range(15)]
    for a, b in edges:
        adj[a].add(b)
        adj[b].add(a)
    check_graph(adj, 6, 8, 55)
    require(check_graph([set(range(15)) - {i} - s for i, s in enumerate(adj)], 6, 8, 50) == 50,
            'complement attains lower density endpoint')
    root = next(i for i in range(15) if len(adj[i]) == 8)
    hs, bs = sorted(adj[root]), sorted(set(range(15)) - adj[root] - {root})
    H = tuple(sum(1 << j for j, w in enumerate(hs) if w in adj[v]) for v in hs)
    B = tuple(sum(1 << j for j, w in enumerate(bs) if w in adj[v]) for v in bs)
    # Both searches must find a 55-edge completion on this literal split.
    boundary = []
    for module in (fast_search, reference_search, literal_search):
        found = module.search(H, B, 55, stop=True)
        require(bool(found['solutions']), '55-edge boundary search positive')
        for rows in found['solutions']:
            check_graph(decode(H, B, rows), 6, 8, 55)
        boundary.append(sum(found['nodes']))
    negative = 0
    for graph, low, high, target in ((adj, 6, 8, 56), ([set(range(4)) - {i} for i in range(4)], 3, 3, 6)):
        try:
            check_graph(graph, low, high, target)
        except ValueError:
            negative += 1
        else:
            raise ValueError('negative control accepted')
    return {'complete_rook_models': 82, 'sharp_fixture_edges': 55,
            'sharp_fixture_degrees': sorted(map(len, adj)), 'boundary_search_nodes': boundary,
            'negative_controls': negative, 'mixed_four_set_truth_tables': constraints_audit()}


def inequality_audit():
    # The exact improvement is algebraic, not a graph-realizability assertion.
    cases = 0
    for p in range(16):
        f = 15 - p
        for D in range(p * f + 1):
            for eF in range(f * (f - 1) // 2 + 1):
                delta = max(0, 8 * p + D + 2 * eF - 110)
                require(min(8 * p - D, 110 - 2 * D - 2 * eF) == 8 * p - D - delta,
                        'integer density budget identity')
                cases += 1
    # This scalar point passes the former degree cap and fails the density cap.
    p, f, D, eF, eP = 14, 1, 8, 0, 48
    require(2 * eP <= 8 * p - D and eP + D + eF == 56 > 55,
            'strict strengthening of scalar relaxation')
    require(max(0, 8 * p + D + 2 * eF - 110) == 10, 'ten-unit improvement')
    return {'algebra_cases': cases, 'strict_scalar_example': {'p': p, 'f': f, 'D': D, 'eF': eF, 'eP': eP},
            'twice_edge_budget_improvement': 10}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--engine', choices=('fast', 'reference', 'literal'), default='fast')
    ap.add_argument('--report', type=Path)
    ap.add_argument('--progress', action='store_true')
    args = ap.parse_args()
    small = census.run()
    controls_result = controls()
    engine = {'fast': fast_search, 'reference': reference_search, 'literal': literal_search}[args.engine]
    cases = []
    for h in small['eight_classes']:
        for b in small['six_classes']:
            H = census.graph(8, h['mask'])
            B = census.complement(census.graph(6, b['mask']))
            require(census.valid(H) and census.valid(B, 4, 3), 'root-side hypotheses')
            result = engine.search(H, B)
            require(not result['solutions'], ('unexpected density survivor', h, b, result['solutions']))
            cases.append({'H_mask': h['mask'], 'B_complement_mask': b['mask'], **result})
            if args.progress:
                print(f"case={len(cases)}/45 H={h['mask']} Bbar={b['mask']} nodes={sum(result['nodes'])} completions=0", flush=True)
    require(len(cases) == 45, 'complete Cartesian product of rooted types')
    report = {'engine': args.engine, 'small_census': small, 'cases': cases,
              'total_nodes': sum(sum(r['nodes']) for r in cases), 'controls': controls_result,
              'rooted_budget': inequality_audit(), 'minimum_edges': 50, 'maximum_edges': 55,
              'catalog_completeness_used': False, 'solver_used': False,
              'new_profile_exclusions': 0, 'target_graph_found': False}
    if args.report:
        args.report.write_text(json.dumps(report, sort_keys=True, indent=2) + '\n')
    print('PASS complete (3,4) small census: three order-eight and fifteen order-six types')
    print('PASS all 45 rooted cases exclude 56 or more edges')
    print('PASS complete 82-model positive control, literal sharp 55-edge fixture, and negative tests')
    print('PASS common-root density correction and strict scalar separation')
    print(f"ENGINE {args.engine}; nodes={report['total_nodes']}")
    print('THEOREM every Ramsey(4,4;15) graph has between 50 and 55 edges, inclusively')
    print('SCOPE reusable density inequalities; no new hard profile exclusion or target graph')


if __name__ == '__main__':
    main()
