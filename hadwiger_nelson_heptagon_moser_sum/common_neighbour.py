"""Common-unit-neighbour reduction for mixed contacts with a unit H difference."""
from pathlib import Path
from itertools import combinations
from hashlib import sha256
import argparse, json, time
import field as F
from collisions import canonical


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=False)
    start = time.perf_counter()
    H, M, d = F.construction()
    target = F.scale(F.ONE, d*d)
    edges = {(i, j) for i, j in combinations(range(7), 2)
             if F.norm(F.sub(M[i], M[j])) == target}
    neighbours = [set() for _ in M]
    for i, j in edges:
        neighbours[i].add(j); neighbours[j].add(i)
    certificate = [{'pair': [i, j], 'unit_edge': (i, j) in edges,
                    'common_neighbours': sorted(neighbours[i] & neighbours[j])}
                   for i, j in combinations(range(7), 2)]
    raw = (json.dumps(certificate, separators=(',', ':'))+'\n').encode()
    (args.out/'certificate.json').write_bytes(raw)
    unit_h = [(i, j, F.sub(a, b)) for i, a in enumerate(H) for j, b in enumerate(H)
              if i != j and F.norm(F.sub(a, b)) == target]
    assert len(unit_h) == len({a for i, j, a in unit_h}) == 84
    rows = []
    for record in certificate:
        i, j = record['pair']
        if not record['common_neighbours']:
            assert record['unit_edge']; continue
        c = record['common_neighbours'][0]
        u, v = F.sub(M[i], M[c]), F.sub(M[j], M[c])
        b = F.sub(v, u)
        for hi, hj, a in unit_h:
            roots = [canonical(F.mul(a, F.conjugate(u)), d*d),
                     canonical(F.scale(F.mul(a, F.conjugate(v)), -1), d*d)]
            assert roots[0] != roots[1]  # No antipodal pair in this fixed M.
            for branch, r in enumerate(roots):
                rn, rd = r
                assert F.norm(rn) == F.scale(F.ONE, rd*rd)
                combined = F.add(F.scale(a, rd), F.mul(rn, b))
                assert F.norm(combined) == F.scale(F.ONE, (d*rd)**2)
                rows.append({'H_pair': [hi, hj], 'M_pair': [i, j], 'centre': c,
                             'branch': branch, 'r': r})
    root_raw = (json.dumps(rows, separators=(',', ':'))+'\n').encode()
    (args.out/'roots.json').write_bytes(root_raw)
    distinct = {(tuple(row['r'][0]), row['r'][1]) for row in rows}
    nonunit_h = {F.sub(a, b) for a in H for b in H
                 if a != b and F.norm(F.sub(a, b)) != target}
    representatives = {a for a in nonunit_h if a < F.scale(a, -1)}
    assert nonunit_h == representatives | {F.scale(a, -1) for a in representatives}
    md = {F.sub(a, b) for a in M for b in M if a != b}
    result = {'status': 'EVERY UNIT-H MIXED CONTACT IS IN THE CLOSED COLLISION SET',
              'M_pairs': len(certificate), 'M_unit_edges': len(edges),
              'M_common_neighbour_pairs': sum(bool(r['common_neighbours']) for r in certificate),
              'M_nonedges': sum(not r['unit_edge'] for r in certificate),
              'uncovered_pairs': [r['pair'] for r in certificate if not r['common_neighbours']],
              'unit_H_directed_differences': len(unit_h), 'explicit_root_checks': len(rows),
              'distinct_common_neighbour_rotations': len(distinct),
              'nonunit_H_directed_differences': len(nonunit_h),
              'nonunit_H_difference_sign_classes': len(representatives),
              'M_directed_differences': len(md),
              'remaining_possible_exception_bound': 2*len(representatives)*len(md),
              'certificate_sha256': sha256(raw).hexdigest(),
              'root_transcript_sha256': sha256(root_raw).hexdigest(),
              'new_sum_graphs_constructed': 0, 'remaining_angles_enumerated': False}
    (args.out/'result.json').write_text(json.dumps(result, indent=2)+'\n')
    (args.out/'timing.json').write_text(json.dumps({'seconds': time.perf_counter()-start})+'\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__': main()
