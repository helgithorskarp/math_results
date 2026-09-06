"""Independent tensor-basis incidence and root audit, with geometric controls."""
from pathlib import Path
from itertools import combinations
from hashlib import sha256
import argparse, copy, json, time
import audit as A
import contacts_audit as V


def check_incidence(records, M, d):
    expected = []
    for i, j in combinations(range(len(M)), 2):
        common = [k for k in range(len(M)) if k != i and k != j
                  and A.norm(A.sub(M[i], M[k])) == A.scale(A.O, d*d)
                  and A.norm(A.sub(M[j], M[k])) == A.scale(A.O, d*d)]
        expected.append({'pair': [i, j], 'unit_edge': A.norm(A.sub(M[i], M[j])) == A.scale(A.O, d*d),
                         'common_neighbours': common})
    assert records == expected


def control_roots(a, u, v):
    assert all(A.norm(x) == A.O for x in (a, u, v)) and u != v
    b = A.sub(v, u)
    roots = {A.mul(a, A.conjugate(u)), A.scale(A.mul(a, A.conjugate(v)), -1)}
    assert all(A.norm(r) == A.O and A.norm(A.add(a, A.mul(r, b))) == A.O for r in roots)
    return roots


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--work', type=Path, required=True)
    args = parser.parse_args()
    start = time.perf_counter()
    here = Path(__file__).resolve().parent
    expected = json.loads((here/'common_neighbour_expected.json').read_text())
    assert expected == json.loads((args.work/'result.json').read_text())
    raw = (here/'common_neighbour_certificate.json').read_bytes()
    assert raw == (args.work/'certificate.json').read_bytes()
    assert sha256(raw).hexdigest() == expected['certificate_sha256']
    certificate = json.loads(raw)
    H, M = V.factors()
    check_incidence(certificate, M, 42)
    assert len(certificate) == 21
    assert sum(not r['unit_edge'] for r in certificate) == 10
    assert [r['pair'] for r in certificate if not r['common_neighbours']] == [[3, 6]]
    assert next(r for r in certificate if r['pair'] == [3, 6])['unit_edge']
    unit = A.scale(A.O, 42**2)
    hd = {A.sub(a, b) for a in H for b in H if a != b}
    unit_h = {(i, j): A.sub(a, b) for i, a in enumerate(H) for j, b in enumerate(H)
              if i != j and A.norm(A.sub(a, b)) == unit}
    assert len(hd) == 420 and len(unit_h) == len(set(unit_h.values())) == 84
    inherited = json.loads((here/'contacts_certificate.json').read_text())
    closed = set()
    for record in inherited:
        r = V.decode(record['r'])
        orbit = {V.multiply((A.zp(k), 1), r) for k in range(7)}
        assert len(orbit) == 7 and not closed.intersection(orbit)
        closed.update(orbit)
    assert len(closed) == 252
    transcript = (args.work/'roots.json').read_bytes()
    assert sha256(transcript).hexdigest() == expected['root_transcript_sha256']
    rows = json.loads(transcript)
    assert len(rows) == 3360
    supplied = {}
    for row in rows:
        key = tuple(row['H_pair'])+tuple(row['M_pair'])+(row['centre'], row['branch'])
        assert key not in supplied
        supplied[key] = V.decode(row['r'])
    actual = {}
    branch_counts = [0, 0]
    for rec in certificate:
        if not rec['common_neighbours']: continue
        i, j = rec['pair']; c = rec['common_neighbours'][0]
        u, v = A.sub(M[i], M[c]), A.sub(M[j], M[c])
        b = A.sub(v, u)
        assert u != v and u != A.scale(v, -1)
        for (hi, hj), a in unit_h.items():
            for branch, (direction, sign) in enumerate(((u, 1), (v, -1))):
                r = V.canonical(A.scale(A.mul(a, A.conjugate(direction)), sign), 42**2)
                rn, rd = r
                assert A.norm(rn) == A.scale(A.O, rd*rd)
                assert A.norm(A.add(A.scale(a, rd), A.mul(rn, b))) == A.scale(A.O, (42*rd)**2)
                # Verify the collision itself using the original labelled factor points.
                if branch == 0:
                    left = A.add(A.scale(H[hi], rd), A.mul(rn, M[c]))
                    right = A.add(A.scale(H[hj], rd), A.mul(rn, M[i]))
                else:
                    left = A.add(A.scale(H[hi], rd), A.mul(rn, M[j]))
                    right = A.add(A.scale(H[hj], rd), A.mul(rn, M[c]))
                assert left == right and r in closed
                actual[hi, hj, i, j, c, branch] = r
                branch_counts[branch] += 1
    assert actual == supplied
    assert set(actual.values()) == closed
    nonunit = hd-set(unit_h.values())
    # Count sign orbits without relying on the producer's coordinate ordering.
    sign_orbits = {frozenset((a, A.scale(a, -1))) for a in nonunit}
    assert all(len(o) == 2 for o in sign_orbits)
    md = {A.sub(a, b) for a in M for b in M if a != b}
    assert len(nonunit) == 336 and len(sign_orbits) == 168 and len(md) == 34
    assert 2*len(sign_orbits)*len(md) == expected['remaining_possible_exception_bound'] == 11424
    # Two roots, antipodal tangency, and failures of omitted hypotheses.
    assert len(control_roots(A.O, A.O, A.OMEGA)) == 2
    assert control_roots(A.O, A.O, A.scale(A.O, -1)) == {A.O}
    rejected = 0
    for args0 in ((A.O, A.O, A.O), (A.scale(A.O, 2), A.O, A.OMEGA)):
        try: control_roots(*args0)
        except AssertionError: rejected += 1
    bad = copy.deepcopy(certificate); bad[0]['common_neighbours'] = []
    for changed in (bad, certificate[:-1]):
        try: check_incidence(changed, M, 42)
        except AssertionError: rejected += 1
    assert rejected == 4
    # A={0,1}, B={0,2}, r=-1: a mixed unit edge but four distinct sums.
    # The common unit neighbour1 exists in the plane, but is absent from B.
    segment_a, segment_b = [A.Z, A.O], [A.Z, A.scale(A.O, 2)]
    r = A.scale(A.O, -1)
    points = {A.add(a, A.mul(r, b)) for a in segment_a for b in segment_b}
    assert len(points) == 4 and A.norm(A.add(A.O, A.mul(r, segment_b[1]))) == A.O
    out = {'status': 'ALL UNIT-H CONTACTS REDUCE TO THE CLOSED COLLISION SET',
           'M_pair_incidence_rows_compared': 21, 'covered_M_pairs': 20,
           'covered_M_nonedges': 10, 'uncovered_unit_pair': [3, 6],
           'unit_H_directed_differences': 84, 'roots_compared_entrywise': len(actual),
           'explicit_labelled_collisions_checked': sum(branch_counts),
           'branch_checks': branch_counts, 'distinct_rotations_equal_closed_set': len(closed),
           'nonunit_H_difference_sign_classes': len(sign_orbits),
           'remaining_possible_exception_bound': 11424,
           'two_root_control': True, 'antipodal_tangency_control': True,
           'invalid_inputs_or_certificates_rejected': rejected,
           'common_neighbour_outside_factor_is_insufficient': True,
           'new_sum_graphs_constructed': 0, 'remaining_angles_enumerated': False,
           'seconds': time.perf_counter()-start}
    (args.work/'audit.json').write_text(json.dumps(out, indent=2)+'\n')
    print(json.dumps(out, indent=2))


if __name__ == '__main__': main()
