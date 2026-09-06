"""Separate tensor-basis audit of H incidence, labelled collisions, and event cover.

Does not import the producer, field.py, or its pair-orbit routine.
"""
from pathlib import Path
from itertools import combinations
from hashlib import sha256
import argparse, copy, json, time
import audit as A
import contacts_audit as V


def incidence_check(rows, H):
    unit = A.scale(A.O, 42**2)
    expected = []
    for i, j in combinations(range(21), 2):
        common = [k for k in range(21) if k not in (i, j)
                  and A.norm(A.sub(H[i], H[k])) == unit
                  and A.norm(A.sub(H[j], H[k])) == unit]
        expected.append([i, j, A.norm(A.sub(H[i], H[j])) == unit, common])
    assert rows == expected


def orbit_check(supplied, pairs, H):
    # Act directly on exact coordinates, not the producer's block-label formula.
    point_index = {point: i for i, point in enumerate(H)}
    expected = set()
    for i, j in pairs:
        orbit = frozenset(tuple(sorted((point_index[A.mul(A.zp(k), H[i])],
                                       point_index[A.mul(A.zp(k), H[j])])))
                          for k in range(7))
        assert len(orbit) == 7 and orbit <= pairs
        expected.add(orbit)
    actual = [frozenset(map(tuple, orbit)) for orbit in supplied]
    assert len(actual) == len(set(actual)) and set(actual) == expected
    assert all(len(orbit) == 7 and list(map(tuple, row)) == sorted(orbit)
               for orbit, row in zip(actual, supplied))
    assert [row[0] for row in supplied] == sorted(row[0] for row in supplied)


def dual_roots(u, v, b):
    assert u != v and all(A.norm(x) == A.O for x in (u, v, b))
    roots = {A.mul(u, A.conjugate(b)), A.scale(A.mul(v, A.conjugate(b)), -1)}
    assert all(A.norm(r) == A.O and A.norm(A.add(A.sub(v, u), A.mul(r, b))) == A.O
               for r in roots)
    return roots


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--work', type=Path, required=True)
    args = parser.parse_args()
    start = time.perf_counter()
    here = Path(__file__).resolve().parent
    expected = json.loads((here/'dual_neighbour_expected.json').read_text())
    assert expected == json.loads((args.work/'result.json').read_text())
    raw = (here/'dual_neighbour_certificate.json').read_bytes()
    assert raw == (args.work/'certificate.json').read_bytes()
    assert sha256(raw).hexdigest() == expected['certificate_sha256']
    cert = json.loads(raw)
    assert cert['H_pair_row_format'] == ['i', 'j', 'unit_edge', 'common_neighbours']
    H, M = V.factors()
    incidence_check(cert['H_pair_rows'], H)
    unit = A.scale(A.O, 42**2)
    incidence = cert['H_pair_rows']
    assert len(incidence) == 210
    assert all(len(common) <= 1 for i, j, edge, common in incidence)
    assert sum(edge for i, j, edge, common in incidence) == 42
    assert sum(edge and bool(common) for i, j, edge, common in incidence) == 21
    assert sum(not edge and bool(common) for i, j, edge, common in incidence) == 105
    nonunit_pairs = {(i, j) for i, j, edge, common in incidence if not edge}
    uncovered = {(i, j) for i, j, edge, common in incidence if not edge and not common}
    assert len(nonunit_pairs) == 168 and len(uncovered) == 63
    assert {A.mul(A.zp(1), point) for point in H} == set(H)
    orbits = cert['nonunit_H_pair_C7_orbits']
    orbit_check(orbits, nonunit_pairs, H)
    indices = cert['uncovered_nonunit_orbit_indices']
    assert indices == sorted(set(indices)) and all(0 <= k < len(orbits) for k in indices)
    orbit_check([orbits[k] for k in indices], uncovered, H)
    assert len(orbits) == 24 and len(indices) == 9
    # Difference uniqueness makes each unordered H pair exactly one sign class.
    hd = {A.sub(a, b) for a in H for b in H if a != b}
    assert len(hd) == 420
    sign_classes = {frozenset((a, A.scale(a, -1))) for a in hd}
    assert len(sign_classes) == 210 and all(len(s) == 2 for s in sign_classes)
    md = {A.sub(a, b) for a in M for b in M if a != b}
    um = {b for b in md if A.norm(b) == unit}
    nm = md-um
    assert len(um) == 14 and len(nm) == 20
    assert all(A.scale(b, -1) in um for b in um)
    assert all(A.scale(b, -1) in nm for b in nm)
    supplied_um = cert['unit_M_difference_labels']
    assert all(len(pair) == 2 and all(isinstance(x, int) and 0 <= x < 7 for x in pair)
               and pair[0] != pair[1] for pair in supplied_um)
    assert len(supplied_um) == len({A.sub(M[p], M[q]) for p, q in supplied_um}) == 14
    assert {A.sub(M[p], M[q]) for p, q in supplied_um} == um
    inherited = json.loads((here/'contacts_certificate.json').read_text())
    closed = set()
    for rec in inherited:
        r = V.decode(rec['r'])
        orbit = {V.multiply((A.zp(k), 1), r) for k in range(7)}
        assert len(orbit) == 7 and not closed.intersection(orbit)
        closed.update(orbit)
    assert len(closed) == 252
    transcript = (args.work/'roots.json').read_bytes()
    assert sha256(transcript).hexdigest() == expected['root_transcript_sha256']
    rows = json.loads(transcript)
    supplied = {}
    for row in rows:
        key = tuple(row['H_pair'])+tuple(row['M_pair'])+(row['centre'], row['branch'])
        assert key not in supplied
        supplied[key] = V.decode(row['r'])
    actual = {}
    branches = [0, 0]
    nonunit_checks = 0
    for i, j, edge, common in incidence:
        if not common: continue
        c = common[0]
        u, v = A.sub(H[i], H[c]), A.sub(H[j], H[c])
        a = A.sub(H[j], H[i])
        assert A.norm(u) == A.norm(v) == unit and u != v and u != A.scale(v, -1)
        for p, q in supplied_um:
            b = A.sub(M[p], M[q])
            for branch, (direction, sign) in enumerate(((u, 1), (v, -1))):
                r = V.canonical(A.scale(A.mul(direction, A.conjugate(b)), sign), 42**2)
                rn, rd = r
                assert A.norm(rn) == A.scale(A.O, rd*rd)
                assert A.norm(A.add(A.scale(a, rd), A.mul(rn, b))) == A.scale(A.O, (42*rd)**2)
                left_h, right_h = (i, c) if branch == 0 else (c, j)
                left = A.add(A.scale(H[left_h], rd), A.mul(rn, M[q]))
                right = A.add(A.scale(H[right_h], rd), A.mul(rn, M[p]))
                assert (left_h, q) != (right_h, p) and left == right and r in closed
                actual[i, j, p, q, c, branch] = r
                branches[branch] += 1
                nonunit_checks += not edge
    assert actual == supplied and len(actual) == 3528 and nonunit_checks == 2940
    assert set(actual.values()) == closed
    # Check the full residual event index set against the sign-and-C7 reduced set.
    # No contact roots or sum graphs for this residual set are computed.
    full = {(A.sub(H[j], H[i]), b) for i, j in nonunit_pairs for b in nm}
    full.update((A.sub(H[j], H[i]), b) for i, j in uncovered for b in um)
    representative_events = [(tuple(orbit[0]), b) for orbit in orbits for b in nm]
    representative_events += [(tuple(orbits[k][0]), b) for k in indices for b in um]
    covered = set()
    reversals = 0
    for (i, j), b in representative_events:
        for k in range(7):
            x, y = A.mul(A.zp(k), H[i]), A.mul(A.zp(k), H[j])
            ii, jj = H.index(x), H.index(y)
            aa, bb = A.sub(y, x), b
            if ii > jj:
                aa, bb = A.scale(aa, -1), A.scale(bb, -1)
                reversals += 1
            covered.add((aa, bb))
    assert full == covered and len(full) == 4242 and len(representative_events) == 606
    assert reversals > 0
    assert expected['remaining_possible_exception_bound'] == 2*len(full) == 8484
    assert expected['C7_possible_exception_orbit_bound'] == 2*len(representative_events) == 1212
    assert expected['unit_M_frontier_H_pair_representatives'] == [orbits[k][0] for k in indices]
    assert expected['unit_M_frontier_representative_equations'] == 9*14 == 126
    assert expected['unit_M_frontier_representative_root_bound'] == 252
    # Geometric controls and certificate corruption rejection.
    assert len(dual_roots(A.O, A.OMEGA, A.OMEGA)) == 2
    assert dual_roots(A.O, A.scale(A.O, -1), A.O) == {A.O}
    rejected = 0
    bad_rows = copy.deepcopy(incidence)
    next(row for row in bad_rows if row[3])[3] = []
    for changed in (bad_rows, incidence[:-1]):
        try: incidence_check(changed, H)
        except AssertionError: rejected += 1
    bad_orbits = copy.deepcopy(orbits); bad_orbits[0] = bad_orbits[0][:-1]
    for changed in (bad_orbits, orbits[:-1], orbits+[orbits[0]]):
        try: orbit_check(changed, nonunit_pairs, H)
        except AssertionError: rejected += 1
    for inputs in ((A.O, A.O, A.O), (A.O, A.OMEGA, A.scale(A.O, 2))):
        try: dual_roots(*inputs)
        except AssertionError: rejected += 1
    assert rejected == 7
    out = {'status': expected['status'], 'H_incidence_rows_compared': 210,
           'covered_nonunit_H_pairs': 105, 'uncovered_nonunit_H_pairs': 63,
           'C7_nonunit_pair_orbits_checked': 24, 'C7_uncovered_pair_orbits_checked': 9,
           'explicit_root_records_compared': len(actual), 'labelled_collisions_checked': len(actual),
           'nonunit_H_root_records': nonunit_checks, 'branch_checks': branches,
           'distinct_rotations_equal_closed_set': 252,
           'residual_event_indices_compared_entrywise': len(full),
           'C7_representative_equations': len(representative_events),
           'sign_reversals_in_C7_expansion': reversals,
           'remaining_possible_exception_bound': 8484, 'C7_possible_exception_orbit_bound': 1212,
           'two_root_control': True, 'antipodal_tangency_control': True,
           'invalid_inputs_or_certificates_rejected': rejected,
           'new_sum_graphs_constructed': 0, 'remaining_angles_enumerated': False,
           'seconds': time.perf_counter()-start}
    (args.work/'audit.json').write_text(json.dumps(out, indent=2)+'\n')
    print(json.dumps(out, indent=2))


if __name__ == '__main__': main()
