"""Independent tensor-basis, quadratic-elimination audit of all126 envelopes.

Uses a different polynomial and different modular homomorphisms from the producer.
"""
from pathlib import Path
from itertools import combinations
from collections import Counter
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
    assert (omega*omega-omega+1) % p == 0
    assert (w*w-w+3) % p == 0
    weights = [pow(z, i % 6, p)*pow(omega, i//6 % 2, p)*pow(w, i//12, p) % p
               for i in range(24)]
    return lambda row: sum(x*y for x, y in zip(row, weights)) % p


def square_residual(a, b, x, y, d):
    unit = A.scale(A.O, d*d)
    assert a != A.Z and A.norm(b) == unit
    n = A.norm(a)
    q = A.sub(unit, A.add(A.norm(x), A.norm(y)))
    c = A.mul(A.mul(a, A.conjugate(b)), A.mul(A.conjugate(x), y))
    aa = A.sub(A.scale(q, -2*d*d), A.add(c, A.conjugate(c)))
    bb = A.sub(c, A.conjugate(c))
    return A.sub(A.mul(n, A.mul(aa, aa)),
                 A.mul(A.sub(n, A.scale(unit, 4)), A.mul(bb, bb)))


def validate_certificate(cert, expected_events, extras, he, me):
    assert cert['case_row_format'] == ['hi', 'hj', 'mi', 'mj', 'M_colouring_index', 'extra_edges']
    assert A.proper(cert['H_colouring'], he, 21)
    qs = cert['M_colourings']
    assert len(qs) == 6 and len({tuple(q) for q in qs}) == 6
    assert all(A.proper(q, me, 7) for q in qs)
    assert [tuple(row[:4]) for row in cert['cases']] == expected_events
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
    expected = json.loads((here/'contact_envelopes_expected.json').read_text())
    assert expected == json.loads((args.work/'result.json').read_text())
    raw = (here/'contact_envelopes_certificate.json').read_bytes()
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
    neighbours = [set() for _ in H]
    for i, j in he: neighbours[i].add(j); neighbours[j].add(i)
    nonunit_pairs = {(i, j) for i, j in combinations(range(21), 2) if [i, j] not in he}
    uncovered = {(i, j) for i, j in nonunit_pairs if not neighbours[i] & neighbours[j]}
    assert len(nonunit_pairs) == 168 and len(uncovered) == 63
    lookup = {point: i for i, point in enumerate(H)}
    assert len(lookup) == 21 and {A.mul(A.zp(1), h) for h in H} == set(H)
    def orbit(pair):
        i, j = pair
        out = frozenset(tuple(sorted((lookup[A.mul(A.zp(k), H[i])],
                                     lookup[A.mul(A.zp(k), H[j])]))) for k in range(7))
        assert len(out) == 7
        return out
    orbit_sets = {orbit(pair) for pair in uncovered}
    assert len(orbit_sets) == 9 and set().union(*orbit_sets) == uncovered
    hpairs = sorted(min(o) for o in orbit_sets)
    bpairs = []
    differences = set()
    for i in range(7):
        for j in range(7):
            if i == j: continue
            b = A.sub(M[i], M[j])
            if A.norm(b) == unit and b not in differences:
                differences.add(b); bpairs.append((i, j))
    assert len(bpairs) == 14
    events = [(hi, hj, bi, bj) for hi, hj in hpairs for bi, bj in bpairs]
    assert len(events) == 126
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
                vv = f(A.conjugate(x))*f(y) % mod
                vb = f(x)*f(A.conjugate(y)) % mod
                values.append((vv, vb, f(q)))
            mixed.append(((v, w), x, y, values))
    assert len(factor) == 525 and len(mixed) == 8820
    extras, rebuilt = [], []
    survivors = checked_edges = 0
    for hi, hj, bi, bj in events:
        a, b = A.sub(H[hj], H[hi]), A.sub(M[bi], M[bj])
        n = A.norm(a)
        W = A.mul(a, A.conjugate(b))
        mapped = [(f(W), f(A.conjugate(W)), f(n)) for f in maps]
        extra = []
        for pair, x, y, values in mixed:
            possible = True
            for parameters, (ww, wb, nn), (v, vb, qq) in zip(MODULI, mapped, values):
                mod = parameters[0]
                c, cb = ww*v % mod, wb*vb % mod
                aa, bb = (-2*d*d*qq-c-cb) % mod, (c-cb) % mod
                if (nn*aa*aa-(nn-4*d*d)*bb*bb) % mod:
                    possible = False; break
            if not possible: continue
            survivors += 1
            if square_residual(a, b, x, y, d) == A.Z: extra.append(pair)
        extras.append(extra)
        edges = sorted(factor+extra)
        rebuilt.append({'event': [hi, hj, bi, bj], 'vertices': 147, 'edges': [list(e) for e in edges]})
        checked_edges += len(edges)
    assert rebuilt == supplied_graphs  # Complete edge lists, not just hashes or counts.
    validate_certificate(cert, events, extras, he, me)
    for row, g in zip(cert['cases'], rebuilt):
        colours = [cert['H_colouring'][i] ^ cert['M_colourings'][row[4]][j]
                   for i in range(21) for j in range(7)]
        assert A.proper(colours, g['edges'], 147)
    assert sum(map(len, extras)) == 198
    assert Counter(map(len, extras)) == {1: 54, 2: 72}
    assert checked_edges == expected['colour_edge_checks'] == 66348
    # Both-nonunit event bound, including the exact sign and rotation quotient sizes.
    hd = {A.sub(x, y) for x in H for y in H if x != y}
    md = {A.sub(x, y) for x in M for y in M if x != y}
    nh = {a for a in hd if A.norm(a) != unit}
    nm = {b for b in md if A.norm(b) != unit}
    assert len(hd) == 420 and len(nh) == 336 and len(nm) == 20
    assert len({frozenset((a, A.scale(a, -1))) for a in nh}) == 168
    nonunit_orbits = {orbit(pair) for pair in nonunit_pairs}
    assert len(nonunit_orbits) == 24 and set().union(*nonunit_orbits) == nonunit_pairs
    assert all(A.scale(b, -1) in nm for b in nm)
    assert expected['remaining_possible_exception_bound'] == 2*168*20 == 6720
    assert expected['C7_possible_exception_orbit_bound'] == 2*24*20 == 960
    # One-root-only edge: the envelope deliberately combines the two placements.
    eta = A.sub(A.OMEGA, A.O)
    assert A.norm(A.add(A.O, eta)) == A.norm(A.add(A.O, A.conjugate(eta))) == A.O
    assert square_residual(A.O, A.O, A.O, eta, 1) == A.Z
    assert A.norm(A.add(A.O, A.mul(eta, eta))) == A.O
    assert A.norm(A.add(A.O, A.mul(A.conjugate(eta), eta))) == A.scale(A.O, 4)
    # Dependent rows, excluded edge, tangent contact, and infeasible contact.
    assert square_residual(A.O, A.O, A.O, A.Z, 1) == A.Z
    assert square_residual(A.O, A.O, A.Z, A.scale(A.O, 2), 1) != A.Z
    assert square_residual(A.scale(A.O, 2), A.O, A.scale(A.O, 2), A.O, 1) == A.Z
    assert A.norm(A.add(A.scale(A.O, 2), A.scale(A.O, -1))) == A.O
    assert square_residual(A.scale(A.O, 3), A.O, A.scale(A.O, 3), A.O, 1) == A.Z
    # A proper colouring of formal labels need not descend through a collision.
    assert A.proper([0, 2, 1, 3], [(0, 1), (0, 2), (1, 3), (2, 3)], 4)
    sums = [i+j for i in range(2) for j in range(2)]
    assert len(set(sums)) == 3 and sums[1] == sums[2] and [0, 2, 1, 3][1] != [0, 2, 1, 3][2]
    rejected = 0
    mutations = []
    bad = copy.deepcopy(cert); bad['cases'].pop(); mutations.append(bad)
    bad = copy.deepcopy(cert); bad['cases'][0][5].pop(); mutations.append(bad)
    bad = copy.deepcopy(cert); bad['cases'][0][4] = 6; mutations.append(bad)
    bad = copy.deepcopy(cert); bad['H_colouring'] = [0]*21; mutations.append(bad)
    for bad in mutations:
        try: validate_certificate(bad, events, extras, he, me)
        except AssertionError: rejected += 1
    for a, b in ((A.Z, A.O), (A.O, A.scale(A.O, 2))):
        try: square_residual(a, b, A.O, A.O, 1)
        except AssertionError: rejected += 1
    assert rejected == 6
    out = {'status': expected['status'], 'independent_polynomial': 'squared quadratic-root elimination',
           'independent_moduli': MODULI, 'H_uncovered_pairs_checked': 63,
           'H_pair_C7_orbits_checked': 9, 'cohort_equations_checked': 126,
           'mixed_pair_tests': len(mixed)*126, 'all_pair_tests_including_unmixed': 10731*126,
           'modular_survivors_rechecked_exactly': survivors,
           'modular_false_positives': survivors-198, 'extra_envelope_edges_compared': 198,
           'complete_graphs_compared_entrywise': 126, 'colour_edge_checks': checked_edges,
           'one_branch_only_edge_control': True, 'dependent_rows_control': True,
           'tangent_contact_control': True, 'infeasible_contact_control': True,
           'collision_requires_separate_colour_descent': True,
           'invalid_inputs_or_certificates_rejected': rejected,
           'remaining_possible_exception_bound': 6720, 'C7_possible_exception_orbit_bound': 960,
           'contact_roots_extracted': False, 'actual_root_graphs_constructed': 0,
           'remaining_both_nonunit_events_enumerated': False, 'native_solver_calls': 0,
           'seconds': time.perf_counter()-start}
    (args.work/'audit.json').write_text(json.dumps(out, indent=2)+'\n')
    print(json.dumps(out, indent=2))


if __name__ == '__main__': main()
