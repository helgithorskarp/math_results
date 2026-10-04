"""Untrusted exact inverse producer; the separate checker never imports it."""
from fractions import Fraction
from itertools import combinations
from pathlib import Path
import argparse
import json


def produce():
    z = list(range(3, 12)); w = list(range(12, 21))
    bad = sorted([sum(1 << i for i in t) for t in combinations(z, 2)] +
                 [sum(1 << i for i in t) for t in combinations(w, 2)] +
                 [6 + (1 << i) for i in w])
    root = bad[0]; visited = {root}; queue = [root]; edges = []
    for u in queue:
        for v in bad:
            if v not in visited and not u & v:
                visited.add(v); queue.append(v); edges.append(sorted([u, v]))
    edges.append([12288, 49152])
    n = len(bad)
    A = [[Fraction(int(v in e)) for e in edges] +
         [Fraction(int(i == j)) for j in range(n)] for i, v in enumerate(bad)]
    for j in range(n):
        p = next(i for i in range(j, n) if A[i][j])
        A[j], A[p] = A[p], A[j]
        a = A[j][j]; A[j] = [v / a for v in A[j]]
        for i in range(n):
            if i != j and A[i][j]:
                a = A[i][j]; A[i] = [v - a * t for v, t in zip(A[i], A[j])]
    inverse2 = [[2 * v for v in row[n:]] for row in A]
    if any(v.denominator != 1 for row in inverse2 for v in row):
        raise ValueError('not an inverse over2')
    return {'actual_agent': 'six-downset-3', 'role': 'researcher', 'q': 18,
            'k': 9, 'actual_N': 278, 's': 58,
            'dependency_graph': 'bafkreifiauc33i6a3pumyecwlfcprotceve2xb6c47iavaqyvhcpexv3qy',
            'dependency_source': '88c6c7ea0905fe51d4ecab5703a3e9cd18d3344c',
            'dependency_not_rechecked': True,
            'real_tau_interval': ['0', '1/128'], 'eta': '1/1152921504606846976',
            'rho_eta_denominator_power': 14,
            'selected_edge_numerator': 2, 'pivot_compensation_multiplier': 1,
            'good_gauge_numerator': -2, 'anchored_a_numerator': -2,
            'bad_vertex_order': bad, 'pivot_edge_order': edges,
            'inverse_denominator': 2,
            'twice_inverse_rows': [' '.join(str(int(v)) for v in row) for row in inverse2]}


if __name__ == '__main__':
    ap = argparse.ArgumentParser(); ap.add_argument('--out', type=Path, required=True)
    args = ap.parse_args()
    args.out.write_text(json.dumps(produce(), sort_keys=True, indent=2) + '\n')
