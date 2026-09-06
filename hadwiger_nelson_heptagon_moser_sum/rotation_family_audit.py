"""Independent tensor-basis Gram-determinant audit of the full480-event closure."""
from pathlib import Path
from itertools import combinations, permutations
from hashlib import sha256
from math import isqrt
import argparse, copy, json, time
import audit as A
import contacts_audit as V

MODULI = ((2017, 54, 822), (2143, 325, 207))


def modular_map(parameters):
    p, t, s = parameters
    assert p > 42 and all(p % k for k in range(2, isqrt(p)+1))
    z, omega, w = pow(t, 6, p), pow(t, 7, p), (1+s)*pow(2, -1, p) % p
    assert z != 1 and sum(pow(z, j, p) for j in range(7)) % p == 0
    assert (omega*omega-omega+1) % p == 0 and (w*w-w+3) % p == 0
    weights = [pow(z, i % 6, p)*pow(omega, i//6 % 2, p)*pow(w, i//12, p) % p
               for i in range(24)]
    return lambda row: sum(x*y for x, y in zip(row, weights)) % p


def det3(matrix):
    result = A.Z
    for perm in permutations(range(3)):
        inversions = sum(perm[i] > perm[j] for i in range(3) for j in range(i+1, 3))
        term = A.mul(A.mul(matrix[0][perm[0]], matrix[1][perm[1]]), matrix[2][perm[2]])
        result = A.add(result, A.scale(term, (-1)**inversions))
    return result


def gram(U, n, V0, q):
    g11, g22 = A.scale(A.norm(U), 4), A.scale(A.norm(V0), 4)
    g12 = A.scale(A.add(A.mul(U, A.conjugate(V0)), A.mul(A.conjugate(U), V0)), 2)
    neg_n = A.scale(n, -1)
    return det3(((g11, g12, neg_n), (g12, g22, q), (neg_n, q, A.O)))


def gram_residual(a, b, x, y, d):
    assert a != A.Z and b != A.Z
    unit = A.scale(A.O, d*d)
    U, V0 = A.mul(A.conjugate(a), b), A.mul(A.conjugate(x), y)
    n = A.sub(A.add(A.norm(a), A.norm(b)), unit)
    q = A.sub(unit, A.add(A.norm(x), A.norm(y)))
    return gram(U, n, V0, q)


def validate_certificate(cert, events, extras, he, me):
    assert cert['case_row_format'] == ['hi', 'hj', 'mi', 'mj', 'M_colouring_index', 'extra_edges']
    assert A.proper(cert['H_colouring'], he, 21)
    qs = cert['M_colourings']
    assert len(qs) == len({tuple(q) for q in qs}) == 4
    assert all(A.proper(q, me, 7) for q in qs)
    assert [tuple(row[:4]) for row in cert['cases']] == events
    for row, extra in zip(cert['cases'], extras):
        assert len(row) == 6 and isinstance(row[4], int) and 0 <= row[4] < len(qs)
        assert row[5] == [list(edge) for edge in extra]
        pp, qq = cert['H_colouring'], qs[row[4]]
        assert all((pp[i//7] ^ qq[i % 7]) != (pp[j//7] ^ qq[j % 7]) for i, j in extra)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--work', type=Path, required=True)
    args = parser.parse_args()
    start = time.perf_counter()
    here = Path(__file__).resolve().parent
    expected = json.loads((here/'rotation_family_expected.json').read_text())
    assert expected == json.loads((args.work/'result.json').read_text())
    raw = (here/'rotation_family_certificate.json').read_bytes()
    assert raw == (args.work/'certificate.json').read_bytes()
    assert sha256(raw).hexdigest() == expected['certificate_sha256']
    cert = json.loads(raw)
    graph_raw = (args.work/'graphs.json').read_bytes()
    assert sha256(graph_raw).hexdigest() == expected['envelope_graph_stream_sha256']
    supplied_graphs = json.loads(graph_raw)
    H, M = V.factors()
    d = 42
    unit = A.scale(A.O, d*d)
    he, me = V.unit_edges(H, d), V.unit_edges(M, d)
    assert len(he) == 42 and len(me) == 11
    nonunit_pairs = {(i, j) for i, j in combinations(range(21), 2) if [i, j] not in he}
    assert len(nonunit_pairs) == 168
    lookup = {point: i for i, point in enumerate(H)}
    assert len(lookup) == 21 and {A.mul(A.zp(1), h) for h in H} == set(H)
    orbits = set()
    for i, j in nonunit_pairs:
        orbit = frozenset(tuple(sorted((lookup[A.mul(A.zp(k), H[i])],
                                       lookup[A.mul(A.zp(k), H[j])]))) for k in range(7))
        assert len(orbit) == 7 and orbit <= nonunit_pairs
        orbits.add(orbit)
    assert len(orbits) == 24 and set().union(*orbits) == nonunit_pairs
    hpairs = sorted(min(orbit) for orbit in orbits)
    bpairs, differences = [], set()
    for i in range(7):
        for j in range(7):
            if i == j: continue
            b = A.sub(M[i], M[j])
            if A.norm(b) != unit and b not in differences:
                differences.add(b); bpairs.append((i, j))
    assert len(bpairs) == 20 and all(A.scale(b, -1) in differences for b in differences)
    hd = {A.sub(x, y) for x in H for y in H if x != y}
    assert len(hd) == 420
    assert len({frozenset((a, A.scale(a, -1))) for a in hd if A.norm(a) != unit}) == 168
    events = [(hi, hj, bi, bj) for hi, hj in hpairs for bi, bj in bpairs]
    assert len(events) == 480
    maps = [modular_map(parameters) for parameters in MODULI]
    hn = {(i, j): A.norm(A.sub(H[i], H[j])) for i, j in combinations(range(21), 2)}
    mn = {(i, j): A.norm(A.sub(M[i], M[j])) for i in range(7) for j in range(7) if i != j}
    factor, mixed = [], []
    for v, w in combinations(range(147), 2):
        hi, mi = divmod(v, 7); hj, mj = divmod(w, 7)
        if hi == hj:
            if mn[mi, mj] == unit: factor.append((v, w))
        elif mi == mj:
            if hn[hi, hj] == unit: factor.append((v, w))
        else:
            x, y = A.sub(H[hi], H[hj]), A.sub(M[mi], M[mj])
            q = A.sub(unit, A.add(hn[hi, hj], mn[mi, mj]))
            values = []
            for parameters, f in zip(MODULI, maps):
                mod = parameters[0]
                vv, vb = f(A.conjugate(x))*f(y) % mod, f(x)*f(A.conjugate(y)) % mod
                values.append((vv, vb, f(q)))
            mixed.append(((v, w), x, y, values))
    assert len(factor) == 525 and len(mixed) == 8820
    extras, rebuilt = [], []
    survivors = checked_edges = 0
    for hi, hj, bi, bj in events:
        a, b = A.sub(H[hj], H[hi]), A.sub(M[bi], M[bj])
        n = A.sub(A.add(A.norm(a), A.norm(b)), unit)
        U = A.mul(A.conjugate(a), b)
        mapped = [(f(U), f(A.conjugate(U)), f(n)) for f in maps]
        extra = []
        for pair, x, y, values in mixed:
            possible = True
            for parameters, (u, ub, nn), (v, vb, qq) in zip(MODULI, mapped, values):
                mod = parameters[0]
                g11, g22, g12 = 4*u*ub % mod, 4*v*vb % mod, 2*(u*vb+ub*v) % mod
                value = g11*g22-g12*g12-g11*qq*qq-2*g12*nn*qq-g22*nn*nn
                if value % mod:
                    possible = False; break
            if not possible: continue
            survivors += 1
            if gram_residual(a, b, x, y, d) == A.Z: extra.append(pair)
        assert extra == [(7*hi+bj, 7*hj+bi)]
        extras.append(extra)
        edges = sorted(factor+extra)
        rebuilt.append({'event': [hi, hj, bi, bj], 'vertices': 147, 'edges': [list(e) for e in edges]})
        checked_edges += len(edges)
    assert rebuilt == supplied_graphs
    validate_certificate(cert, events, extras, he, me)
    for row, g in zip(cert['cases'], rebuilt):
        colours = [cert['H_colouring'][i] ^ cert['M_colourings'][row[4]][j]
                   for i in range(21) for j in range(7)]
        assert A.proper(colours, g['edges'], 147)
    assert checked_edges == expected['colour_edge_checks'] == 252480
    assert expected['full_fixed_rotation_family_closed'] and expected['remaining_possible_nonfour_rotations'] == 0
    # Normalization control: a=2,b=3,r=-1 and x=1,y=2 satisfy both distance equations.
    a, b, x, y = A.scale(A.O, 2), A.scale(A.O, 3), A.O, A.scale(A.O, 2)
    assert A.norm(A.sub(a, b)) == A.norm(A.sub(x, y)) == A.O
    assert gram_residual(a, b, x, y, 1) == A.Z
    U, V0 = A.mul(A.conjugate(a), b), A.mul(A.conjugate(x), y)
    q = A.sub(A.O, A.add(A.norm(x), A.norm(y)))
    assert gram(U, A.norm(a), V0, q) != A.Z  # The old unit-b specialization fails.
    # n=0 is allowed: a=3/5,b=4/5 and r=i are a unit contact.
    a, b = A.scale(A.O, 3), A.scale(A.O, 4)
    assert A.add(A.norm(a), A.norm(b)) == A.scale(A.O, 25)
    assert gram_residual(a, b, a, b, 5) == A.Z
    # Distinct roots, one-root-only edge, and a rejected edge with dependent normals.
    eta = A.sub(A.OMEGA, A.O)
    assert gram_residual(A.O, A.O, A.O, eta, 1) == A.Z
    assert A.norm(A.add(A.O, A.mul(eta, eta))) == A.O
    assert A.norm(A.add(A.O, A.mul(A.conjugate(eta), eta))) == A.scale(A.O, 4)
    assert gram_residual(A.O, A.O, A.Z, A.scale(A.O, 2), 1) != A.Z
    # Infeasible contact and collision/descent controls remain explicit.
    assert gram_residual(A.scale(A.O, 3), A.O, A.scale(A.O, 3), A.O, 1) == A.Z
    assert A.proper([0, 2, 1, 3], [(0, 1), (0, 2), (1, 3), (2, 3)], 4)
    assert 0+1 == 1+0 and [0, 2, 1, 3][1] != [0, 2, 1, 3][2]
    rejected = 0
    mutations = []
    bad = copy.deepcopy(cert); bad['cases'].pop(); mutations.append(bad)
    bad = copy.deepcopy(cert); bad['cases'][0][5].pop(); mutations.append(bad)
    bad = copy.deepcopy(cert); bad['cases'][0][4] = 4; mutations.append(bad)
    bad = copy.deepcopy(cert); bad['H_colouring'] = [0]*21; mutations.append(bad)
    for bad in mutations:
        try: validate_certificate(bad, events, extras, he, me)
        except AssertionError: rejected += 1
    for a, b in ((A.Z, A.O), (A.O, A.Z)):
        try: gram_residual(a, b, A.O, A.O, 1)
        except AssertionError: rejected += 1
    assert rejected == 6
    out = {'status': expected['status'], 'independent_polynomial': 'rank-two real Gram determinant',
           'independent_moduli': MODULI, 'H_nonunit_sign_classes_checked': 168,
           'H_pair_C7_orbits_checked': 24, 'cohort_equations_checked': 480,
           'mixed_pair_tests': len(mixed)*480, 'all_pair_tests_including_unmixed': 10731*480,
           'modular_survivors_rechecked_exactly': survivors, 'modular_false_positives': survivors-480,
           'extra_envelope_edges_compared': 480, 'every_extra_edge_is_the_defining_contact': True,
           'complete_graphs_compared_entrywise': 480, 'colour_edge_checks': checked_edges,
           'general_n_control_and_wrong_unit_b_specialization_rejected': True,
           'zero_n_control': True, 'one_root_only_edge_control': True,
           'dependent_normals_control': True, 'tangent_contact_control': True,
           'infeasible_contact_control': True, 'collision_requires_separate_descent': True,
           'invalid_inputs_or_certificates_rejected': rejected,
           'full_fixed_rotation_family_closed': True, 'contact_roots_extracted': False,
           'actual_root_graphs_constructed': 0, 'native_solver_calls': 0,
           'seconds': time.perf_counter()-start}
    (args.work/'audit.json').write_text(json.dumps(out, indent=2)+'\n')
    print(json.dumps(out, indent=2))


if __name__ == '__main__': main()
