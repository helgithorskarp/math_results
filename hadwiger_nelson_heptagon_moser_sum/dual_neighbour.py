"""Complete H incidence, factor-exchanged contact roots, and residual event indices."""
from pathlib import Path
from itertools import combinations
from collections import Counter
from hashlib import sha256
import argparse, json, time
import field as F
from collisions import canonical


def rotate_label(i, k):
    return 7*(i//7)+(i%7+k)%7


def pair_orbits(pairs):
    remaining = set(pairs)
    out = []
    while remaining:
        i, j = min(remaining)
        orbit = sorted({tuple(sorted((rotate_label(i, k), rotate_label(j, k))))
                        for k in range(7)})
        assert len(orbit) == 7 and set(orbit) <= remaining
        out.append(orbit)
        remaining.difference_update(orbit)
    return out


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=False)
    start = time.perf_counter()
    H, M, d = F.construction()
    unit = F.scale(F.ONE, d*d)
    edges = {(i, j) for i, j in combinations(range(21), 2)
             if F.norm(F.sub(H[i], H[j])) == unit}
    neighbours = [set() for _ in H]
    for i, j in edges:
        neighbours[i].add(j); neighbours[j].add(i)
    incidence = [[i, j, (i, j) in edges, sorted(neighbours[i] & neighbours[j])]
                 for i, j in combinations(range(21), 2)]
    nonunit_pairs = {(i, j) for i, j, edge, common in incidence if not edge}
    uncovered = {(i, j) for i, j, edge, common in incidence if not edge and not common}
    orbits = pair_orbits(nonunit_pairs)
    uncovered_indices = [k for k, orbit in enumerate(orbits) if set(orbit) <= uncovered]
    assert set().union(*(set(orbits[k]) for k in uncovered_indices)) == uncovered
    z = F.K.power(6)+F.K.ZERO
    assert all(F.mul(z, H[i]) == H[rotate_label(i, 1)] for i in range(21))
    hd = {F.sub(a, b) for a in H for b in H if a != b}
    assert len(hd) == 420  # Hence unordered endpoint pairs are difference sign classes.
    md = {}
    for p, mp in enumerate(M):
        for q, mq in enumerate(M):
            if p != q: md.setdefault(F.sub(mp, mq), [p, q])
    um = {b: pair for b, pair in md.items() if F.norm(b) == unit}
    nm = set(md)-set(um)
    certificate = {'H_pair_row_format': ['i', 'j', 'unit_edge', 'common_neighbours'],
                   'H_pair_rows': incidence, 'nonunit_H_pair_C7_orbits': orbits,
                   'uncovered_nonunit_orbit_indices': uncovered_indices,
                   'unit_M_difference_labels': list(um.values())}
    raw = (json.dumps(certificate, separators=(',', ':'))+'\n').encode()
    (args.out/'certificate.json').write_bytes(raw)
    rows = []
    for i, j, edge, common in incidence:
        if not common: continue
        c = common[0]
        u, v = F.sub(H[i], H[c]), F.sub(H[j], H[c])
        a = F.sub(v, u)
        for b, (p, q) in um.items():
            roots = [canonical(F.mul(u, F.conjugate(b)), d*d),
                     canonical(F.scale(F.mul(v, F.conjugate(b)), -1), d*d)]
            assert roots[0] != roots[1]
            for branch, r in enumerate(roots):
                rn, rd = r
                assert F.norm(rn) == F.scale(F.ONE, rd*rd)
                assert F.norm(F.add(F.scale(a, rd), F.mul(rn, b))) == F.scale(F.ONE, (d*rd)**2)
                rows.append({'H_pair': [i, j], 'M_pair': [p, q], 'centre': c,
                             'branch': branch, 'r': r})
    root_raw = (json.dumps(rows, separators=(',', ':'))+'\n').encode()
    (args.out/'roots.json').write_bytes(root_raw)
    distinct = {(tuple(row['r'][0]), row['r'][1]) for row in rows}
    inventory = Counter((edge, len(common)) for i, j, edge, common in incidence)
    result = {'status': 'DUAL COMMON-NEIGHBOUR EXCLUSION AND RESIDUAL INDEX SET VERIFIED',
              'H_pairs': len(incidence), 'H_unit_edges': len(edges),
              'H_pair_inventory': [{'unit_edge': e, 'common_neighbours': c, 'pairs': n}
                                   for (e, c), n in sorted(inventory.items())],
              'H_nonunit_sign_classes': len(nonunit_pairs),
              'H_uncovered_nonunit_sign_classes': len(uncovered),
              'H_nonunit_C7_orbits': len(orbits),
              'H_uncovered_nonunit_C7_orbits': len(uncovered_indices),
              'M_unit_directed_differences': len(um),
              'M_nonunit_directed_differences': len(nm),
              'explicit_root_checks': len(rows),
              'distinct_common_neighbour_rotations': len(distinct),
              'residual_equations': len(nonunit_pairs)*len(nm)+len(uncovered)*len(um),
              'remaining_possible_exception_bound': 2*(len(nonunit_pairs)*len(nm)+len(uncovered)*len(um)),
              'C7_representative_equations': len(orbits)*len(nm)+len(uncovered_indices)*len(um),
              'C7_possible_exception_orbit_bound': 2*(len(orbits)*len(nm)+len(uncovered_indices)*len(um)),
              'unit_M_frontier_H_pair_representatives': [orbits[k][0] for k in uncovered_indices],
              'unit_M_frontier_representative_equations': len(uncovered_indices)*len(um),
              'unit_M_frontier_representative_root_bound': 2*len(uncovered_indices)*len(um),
              'certificate_sha256': sha256(raw).hexdigest(),
              'root_transcript_sha256': sha256(root_raw).hexdigest(),
              'new_sum_graphs_constructed': 0, 'remaining_angles_enumerated': False}
    (args.out/'result.json').write_text(json.dumps(result, indent=2)+'\n')
    (args.out/'timing.json').write_text(json.dumps({'seconds': time.perf_counter()-start})+'\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__': main()
