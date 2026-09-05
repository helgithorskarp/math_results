"""Alternate-basis proof of the spectrum intersection and full collision cover."""
from pathlib import Path
from itertools import combinations
from collections import Counter
from hashlib import sha256
import argparse, copy, json, time
import audit as A
import contacts_audit as V


def pair_values(points):
    return {(i, j): V.canonical(A.norm(A.sub(points[i], points[j])), 42**2)
            for i, j in combinations(range(len(points)), 2)}


def verify_spectrum(record, actual):
    norms = [V.decode(n) for n in record['norms']]
    assert len(set(norms)) == len(norms)
    supplied = {(i, j): norms[k] for i, j, k in record['pairs']}
    assert len(supplied) == len(record['pairs']) and supplied == actual
    counts = Counter(actual.values())
    assert [counts[n] for n in norms] == record['multiplicities']
    return set(norms)


def verify_rotations(rows, actual):
    values = {V.decode(row['r']): row['multiplicity'] for row in rows}
    assert len(values) == len(rows) and values == actual


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--work', type=Path, required=True)
    args = parser.parse_args()
    start = time.perf_counter()
    here = Path(__file__).resolve().parent
    expected = json.loads((here/'collisions_expected.json').read_text())
    assert expected == json.loads((args.work/'result.json').read_text())
    raw = (here/'collisions_certificate.json').read_bytes()
    assert raw == (args.work/'certificate.json').read_bytes()
    assert sha256(raw).hexdigest() == expected['certificate_sha256']
    certificate = json.loads(raw)
    assert certificate['coordinate_denominator'] == 42
    H, M = V.factors()
    assert len(H) == len(set(H)) == 21 and len(M) == len(set(M)) == 7
    hp, mp = pair_values(H), pair_values(M)
    hs = verify_spectrum(certificate['H'], hp)
    ms = verify_spectrum(certificate['M'], mp)
    assert len(hs) == 25 and len(ms) == 7
    one = (A.O, 1)
    assert hs & ms == {one}
    assert {n for n in hs if not any(n[0][1:])} == {one}
    # sqrt(33)=(1-2*omega)*s. The specified complex embedding makes it positive.
    gamma = A.mul(A.sub(A.O, A.scale(A.OMEGA, 2)), A.S)
    assert A.mul(gamma, gamma) == A.scale(A.O, 33)
    assert A.conjugate(gamma) == gamma
    assert any(gamma[12:])  # gamma is outside the K subspace in this basis.
    labels = [(1, 0, 1, 11), (3, 0, 1, 2), (1, 0, 3, 2),
              (7, 1, 6, 1), (7, -1, 6, 1), (9, 1, 6, 2), (9, -1, 6, 2)]
    exact_m_spectrum = {V.canonical(A.add(A.scale(A.O, a), A.scale(gamma, b)), d): count
                        for a, b, d, count in labels}
    assert Counter(mp.values()) == exact_m_spectrum
    # Every H norm lies in K, seen both from its producer s-coefficients and
    # from the independent tensor coordinates having no w coefficient.
    assert all(not any(n[0][12:]) for n in hs)
    assert all(not any(row[0][12:]) for row in certificate['H']['norms'])
    hd = {A.sub(a, b) for a in H for b in H if a != b}
    md = {A.sub(a, b) for a in M for b in M if a != b}
    assert (len(hd), len(md)) == (420, 34)
    hn, mn = {a: A.norm(a) for a in hd}, {b: A.norm(b) for b in md}
    rotations = Counter()
    for a in hd:
        for b in md:
            if hn[a] == mn[b]:
                assert hn[a] == A.scale(A.O, 42**2)
                rotations[V.canonical(A.mul(a, A.conjugate(b)), 42**2)] += 1
    assert len(rotations) == 252 and sum(rotations.values()) == 1176
    assert Counter(rotations.values()) == {2: 84, 6: 168}
    rotation_raw = (args.work/'rotations.json').read_bytes()
    rows = json.loads(rotation_raw)
    verify_rotations(rows, rotations)
    assert sha256(rotation_raw).hexdigest() == expected['rotation_stream_sha256']
    inherited = json.loads((here/'contacts_certificate.json').read_text())
    covered = set()
    for record in inherited:
        r = V.decode(record['r'])
        orbit = {V.multiply((A.zp(j), 1), r) for j in range(7)}
        assert len(orbit) == 7 and not covered.intersection(orbit)
        covered.update(orbit)
    assert len(inherited) == 36 and covered == set(rotations)
    assert {A.mul(A.zp(1), h) for h in H} == set(H)
    # Controls target the data comparisons on which completeness depends.
    bad_pair = copy.deepcopy(certificate['H']); bad_pair['pairs'].pop()
    bad_norm = copy.deepcopy(certificate['H']); bad_norm['norms'][0][0][0] += 1
    bad_count = copy.deepcopy(certificate['H']); bad_count['multiplicities'][0] += 1
    rejected = 0
    for changed in (bad_pair, bad_norm, bad_count):
        try: verify_spectrum(changed, hp)
        except AssertionError: rejected += 1
    for changed in (rows[:-1], rows+rows[:1]):
        try: verify_rotations(changed, rotations)
        except AssertionError: rejected += 1
    assert rejected == 5
    # Disjoint spectra are not a universal property: two segments share length2.
    segment = [A.Z, A.scale(A.O, 84)]
    assert set(pair_values(segment).values()) == {(A.scale(A.O, 4), 1)}
    out = {'status': 'ONLY UNIT LENGTH IS SHARED; ALL COLLISION ORIENTATIONS ARE CLOSED',
           'H_pair_values_compared': len(hp), 'M_pair_values_compared': len(mp),
           'H_squared_distances': len(hs), 'M_squared_distances': len(ms),
           'M_radical_spectrum_verified': True, 'spectrum_intersection': [1],
           'difference_pair_comparisons': len(hd)*len(md),
           'equal_length_difference_pairs': sum(rotations.values()),
           'collision_rotations_compared_entrywise': len(rotations),
           'inherited_disjoint_orbits_covering_collision_set': len(inherited),
           'corrupt_certificates_rejected': rejected, 'nonunit_common_length_control': True,
           'new_graphs_constructed': 0, 'old_graph_audit_repeated': False,
           'seconds': time.perf_counter()-start}
    (args.work/'audit.json').write_text(json.dumps(out, indent=2)+'\n')
    print(json.dumps(out, indent=2))


if __name__ == '__main__': main()
