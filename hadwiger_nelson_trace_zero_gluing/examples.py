"""Exact trace-zero geometries and full distances in E[u], u^2=W."""
from coloring import *
from itertools import combinations
from collections import defaultdict
from math import isqrt
import json


F = load('gadget_inputs', 'hadwiger_nelson_mixed505_all_gadget_anchors/verify.py',
         '526b12cbd9d28217e59feb7191c93ace4e5a572ebeadd66cdf384393126aee38')
SEEDS = {0: (5, 0, 2, 1, 2), 1: (10, 0, 1, 7, 4),
         2: (4, 0, 1, 1, 2), 3: (8, 0, 1, 7, 2), 4: (16, 0, 3, 11, 6)}


def unit_patch():
    eta = e(Q(1, 2), 0, Q(1, 2))
    eta2 = mul(eta, eta)
    return [ZERO, ONE, eta, eta2, scale(ONE, -1), scale(eta, -1), scale(eta2, -1)]


def inputs():
    A, V = F.read_points(159), F.read_points(214)
    B = list(dict.fromkeys([tuple(6*x for x in a) for a in A]+
        [(5*a-11*d, 5*b-c, 5*c+11*b, 5*d+a) for a, b, c, d in A]))
    require(len(B) == 292 and len(V) == 214, 'gadget order mismatch')
    return [tuple(Q(x, 72) for x in b) for b in B], [tuple(Q(x, 12) for x in v) for v in V]


def cases():
    B, V = inputs()
    out = []
    for k, (den, a, b, c, d) in SEEDS.items():
        x, y = e(Q(a, den), 0, Q(b, den)), e(Q(c, den), 0, Q(d, den))
        require(add(norm(x), norm(y)) == ONE and depth(x) == depth(y) == k, 'seed mismatch')
        out.append((f'wheel_depth_{k}', [add(x, z) for z in unit_patch()],
                    [add(y, z) for z in unit_patch()], c, d, k))
        if k in (0, 1, 2, 3):
            out.append((f'mixed506_depth_{k}', [add(sub(z, B[0]), x) for z in B],
                        [add(sub(z, V[0]), y) for z in V], c, d, k))
    out.append(('common_centre', unit_patch(), unit_patch(), 1, 2, 0))
    out.append(('no_cross_edges', unit_patch(), [add(e(10), z) for z in unit_patch()], 1, 2, None))
    return out


def connected(n, edges):
    adj = [set() for _ in range(n)]
    for i, j in edges:
        adj[i].add(j); adj[j].add(i)
    seen, todo = {0}, [0]
    for v in todo:
        for w in adj[v]-seen:
            seen.add(w); todo.append(w)
    return len(seen) == n


def rational_square(q):
    return q >= 0 and isqrt(q.numerator)**2 == q.numerator and isqrt(q.denominator)**2 == q.denominator


def norm_int(x):
    a, b, c, d = x
    return (a*a+33*b*b+3*c*c+11*d*d, 2*(a*b+c*d), 0, 0)


def distance_line(i, j, values):
    return f'{i},{j}:'+','.join(f'{x.numerator}/{x.denominator}' for x in values)+'\n'


def run(case):
    name, P, Qs, c, d, expected_depth = case
    n, total = len(P), len(P)+len(Qs)
    N = c*c+3*d*d
    require(not rational_square(Q(N)) and not rational_square(Q(N, 33)), 'rotation is in E')
    v = (c, 0, -d, 0)
    Wnum = mul(v, v)
    require(norm(Wnum) == (N*N, 0, 0, 0), 'rotation square not norm one')
    D = lcm(*(x.denominator for p in P+Qs for x in p))
    Z = (0, 0, 0, 0)
    pts = [(tuple(int(x*D) for x in p), Z) for p in P]+[(Z, tuple(int(x*D) for x in q)) for q in Qs]
    first, aliases = {}, []
    for idx, p in enumerate(pts):
        aliases.append(first.setdefault(p, idx))
    cross, internal_P, internal_Q, raw_edges = [], [], [], []
    distance_hash = sha256()
    pairs = 0
    for i, j in combinations(range(total), 2):
        pairs += 1
        A, B = sub(pts[i][0], pts[j][0]), sub(pts[i][1], pts[j][1])
        const = add(norm_int(A), norm_int(B))
        linear_num = add(mul(mul(A, bar(B)), bar(Wnum)), scale(mul(B, bar(A)), N))
        root_num = mul(linear_num, v)
        require(const[2:] == root_num[2:] == (0, 0), 'distance is not real')
        values = [Q(const[0], D*D), Q(const[1], D*D),
                  Q(root_num[0], N*N*D*D), Q(root_num[1], N*N*D*D)]
        distance_hash.update(distance_line(i, j, values).encode())
        if const == (D*D, 0, 0, 0) and linear_num == Z:
            raw_edges.append((i, j))
            if j < n:
                internal_P.append((i, j))
            elif i >= n:
                internal_Q.append((i-n, j-n))
            else:
                cross.append((i, j-n))
    require(connected(n, internal_P) and connected(total-n, internal_Q), 'source disconnected')
    cp, cq, recipe = glue(P, Qs, cross)
    if expected_depth is not None:
        require(recipe['depth'] == expected_depth, 'wrong depth branch')
    colours = cp+cq
    require(all(colours[i] == colours[aliases[i]] for i in range(total)), 'overlap colours disagree')
    edges = sorted({tuple(sorted((aliases[i], aliases[j]))) for i, j in raw_edges})
    require(all(i != j and colours[i] != colours[j] for i, j in edges), 'improper colouring')
    # Count cross C4s only on four distinct physical vertices.
    adj = defaultdict(set)
    for i, j in cross:
        adj[i].add(j)
    fours = 0
    for i, j in combinations(range(n), 2):
        for k, l in combinations(sorted(adj[i] & adj[j]), 2):
            fours += len({aliases[i], aliases[j], aliases[n+k], aliases[n+l]}) == 4
    require(fours == 0, 'calibration unexpectedly has a C4')
    return {'case': name, 'source_orders': [n, total-n], 'source_internal_edges': [len(internal_P), len(internal_Q)],
            'rotation_numerator': [c, d], 'rotation_root_squared': N, 'rotation_outside_E': True,
            'vertices': len(first), 'overlaps': total-len(first), 'pairs_checked': pairs,
            'squared_distance_sha256': distance_hash.hexdigest(), 'strict_edges': len(edges),
            'edge_sha256': sha256(''.join(f'{i},{j}\n' for i, j in edges).encode()).hexdigest(),
            'colours': ''.join(map(str, colours)), 'cross_edges': cross, 'cross_four_cycles': fours,
            'recipe': recipe, 'connected_sources': True}


def main():
    rows = [run(c) for c in cases()]
    print(json.dumps({'cases': rows, 'cases_checked': len(rows),
                      'total_pair_checks': sum(r['pairs_checked'] for r in rows),
                      'uniform_claim_requires_PROOF_md': True}, indent=2))


if __name__ == '__main__':
    main()
