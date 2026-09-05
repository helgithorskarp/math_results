"""Exact geometries in E[u], including non-real traces and a whole-field grid."""
from arithmetic import *
from itertools import combinations
from math import isqrt
import json

F = load('source_gadgets', 'hadwiger_nelson_mixed505_all_gadget_anchors/verify.py',
         '526b12cbd9d28217e59feb7191c93ace4e5a572ebeadd66cdf384393126aee38')


def wheel():
    eta = e(Q(1, 2), 0, Q(1, 2)); eta2 = mul(eta, eta)
    return [ZERO, ONE, eta, eta2, scale(ONE, -1), scale(eta, -1), scale(eta2, -1)]


def gadgets():
    A, V = F.read_points(159), F.read_points(214)
    B = list(dict.fromkeys([tuple(6*x for x in p) for p in A]+
        [(5*a-11*d, 5*b-c, 5*c+11*b, 5*d+a) for a, b, c, d in A]))
    require(len(B) == 292 and len(V) == 214, 'gadget sizes changed')
    return [tuple(Q(x, 72) for x in p) for p in B], [tuple(Q(x, 12) for x in p) for p in V]


def cases():
    H = wheel(); B, V = gadgets(); omega = e(Q(-1, 2), 0, Q(1, 2)); out = []
    def pair(name, a, b, P, Qs, kind='connected_sources'):
        rho = omega if 'nonreal' in name else ONE
        Qs = [mul(bar(rho), q) for q in Qs]
        out.append({'name': name, 'a': a, 'b': b, 'rho': rho, 'P': P, 'Q': Qs,
                    'points': [(x, ZERO) for x in P]+[(ZERO, y) for y in Qs], 'kind': kind})
    def shifted(source, x): return [add(sub(p, source[0]), x) for p in source]
    for label, a, b, x, y in [('even_control', 2, 3, ONE, e(Q(4, 3))),
                             ('unit', 1, 6, ONE, e(Q(1, 3)))]:
        pair(label+'_wheels', a, b, shifted(H, x), shifted(H, y))
        pair(label+'_mixed506', a, b, shifted(B, x), shifted(V, y))
    for k, m, a, b in [(1, 1, 1, 3), (2, 3, 19, 27), (3, 5, 43, 75)]:
        x = e(0, 0, Q(m, 1 << k))
        pair(f'even_depth_{k}_wheels', a, b, shifted(H, x), shifted(H, x))
        if k == 2:
            pair('even_nonreal_mixed506', a, b, shifted(B, x), shifted(V, x))
    pair('even_old_path', 2, 3, [e(0), e(Q(4, 3)), e(Q(-8, 27))],
         [e(1), e(Q(7, 9)), e(Q(-95, 81))], 'local_coset_control')
    pair('even_common_centre', 2, 3, H, H)
    pair('even_no_cross', 2, 3, H, [add(e(10), x) for x in H])
    for name, rho, x0, y0 in [('unit_nonreal_grid', omega, ZERO, ZERO),
                              ('unit_fractional_grid', ONE, e(Q(1, 2)), e(Q(1, 4)))]:
        pts = [(add(x0, x), add(y0, y)) for x in H for y in H]
        out.append({'name': name, 'a': 1, 'b': 6, 'rho': rho, 'points': pts, 'kind': 'whole_field_grid'})
    return out


def nint(p):
    a, b, c, d = p
    return (a*a+33*b*b+3*c*c+11*d*d, 2*(a*b+c*d), 0, 0)


def connected(n, edges):
    adj = [set() for _ in range(n)]
    for i, j in edges: adj[i].add(j); adj[j].add(i)
    seen, todo = {0}, [0]
    for i in todo:
        for j in adj[i]-seen: seen.add(j); todo.append(j)
    return len(seen) == n


def square(q):
    return q >= 0 and isqrt(q.numerator)**2 == q.numerator and isqrt(q.denominator)**2 == q.denominator


def run(case):
    a, b, rho, pts = case['a'], case['b'], case['rho'], case['points']
    D = b*b-a*a
    require(D > 0 and not square(Q(D, 3)) and not square(Q(D, 99)), 'rotation not quadratic outside E')
    require(norm(rho) == ONE, 'rho is not a unit rotation')
    T, J = scale(rho, Q(2*a, b)), mul(rho, rho)
    require(mul(J, bar(J)) == ONE and T == mul(J, bar(T)), 'minimal polynomial not self-reciprocal')
    transformed = [(x, mul(y, rho)) for x, y in pts]
    L = lcm(*(v.denominator for p in transformed for x in p for v in x))
    integers = [(tuple(int(v*L) for v in x), tuple(int(v*L) for v in y)) for x, y in transformed]
    aliases, first = [], {}
    for i, p in enumerate(pts): aliases.append(first.setdefault(p, i))
    edges, cross, EP, EQ, h = [], [], [], [], sha256()
    n = len(case.get('P', []))
    for i, j in combinations(range(len(pts)), 2):
        A, B = sub(integers[i][0], integers[j][0]), sub(integers[i][1], integers[j][1])
        c, cb = mul(bar(A), B), mul(A, bar(B))
        constant = add(scale(add(nint(A), nint(B)), b), scale(add(c, cb), a))
        imaginary = sub(c, cb)
        require(constant[2:] == (0, 0) and imaginary[:2] == (0, 0), 'non-real distance')
        values = [Q(constant[0], b*L*L), Q(constant[1], b*L*L),
                  Q(-imaginary[2], b*L*L), Q(-imaginary[3], b*L*L)]
        h.update((f'{i},{j}:'+','.join(f'{v.numerator}/{v.denominator}' for v in values)+'\n').encode())
        if values == [0, 0, 0, 0]: require(aliases[i] == aliases[j], 'unaccounted overlap')
        if values == [1, 0, 0, 0]:
            edges.append(tuple(sorted((aliases[i], aliases[j]))))
            if n:
                if j < n: EP.append((i, j))
                elif i >= n: EQ.append((i-n, j-n))
                else: cross.append((i, j-n))
    edges = sorted(set(edges))
    if local(T, 1) == (0, 0):
        cp, cq, recipe = glue_even(case['P'], case['Q'], T, cross)
        colours = cp+cq
    else:
        colours = [field_colour(x, y, T) for x, y in pts]
        recipe = {'branch': 'unit_trace_whole_field', 'root_mod16': unit_root(T, 4)}
    require(all(colours[i] == colours[aliases[i]] for i in range(len(pts))), 'overlap colours disagree')
    require(all(i != j and colours[i] != colours[j] for i, j in edges), 'improper colouring')
    source_connected = [connected(n, EP), connected(len(pts)-n, EQ)] if n else None
    if case['kind'] == 'connected_sources': require(all(source_connected), 'source is disconnected')
    naive = None
    if case['name'] == 'unit_wheels':
        naive = sum(C.residue(case['P'][i]) == C.residue(case['Q'][j]) for i, j in cross)
        require(naive > 0, 'unit-trace negative colouring control missing')
    radial_failures = sum(add(norm(case['P'][i]), norm(case['Q'][j])) != ONE for i, j in cross) if n else None
    return {'case': case['name'], 'kind': case['kind'], 'rotation_a_b_D': [a, b, D],
            'rho': list(map(str, rho)), 'relative_trace': list(map(str, T)), 'constant_J': list(map(str, J)),
            'vertices': len(first), 'labelled_vertices': len(pts), 'overlaps': len(pts)-len(first),
            'pairs_checked': len(pts)*(len(pts)-1)//2, 'strict_edges': len(edges),
            'squared_distance_sha256': h.hexdigest(),
            'edge_sha256': sha256(''.join(f'{i},{j}\n' for i, j in edges).encode()).hexdigest(),
            'colours': ''.join(map(str, colours)), 'cross_edges': cross, 'source_connected': source_connected,
            'source_internal_edges': [len(EP), len(EQ)] if n else None, 'recipe': recipe,
            'cross_edges_failing_radial_identity': radial_failures, 'naive_residue_collisions': naive}


def main():
    rows = [run(case) for case in cases()]
    print(json.dumps({'cases_checked': len(rows), 'total_pair_checks': sum(r['pairs_checked'] for r in rows),
                      'cases': rows, 'uniform_claim_requires_PROOF_md': True}, indent=2))


if __name__ == '__main__': main()
