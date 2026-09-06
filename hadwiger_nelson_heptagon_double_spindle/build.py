"""Exact fixed sum H+M+M and all 210 two-host-omission restrictions."""
from pathlib import Path
from itertools import combinations
from collections import Counter
from hashlib import sha256
import argparse, json, sys, time

HERE = Path(__file__).resolve().parent
PARENT = HERE.parent/'hadwiger_nelson_heptagon_moser_sum'
sys.path.insert(0, str(PARENT))
import field as F
from rotation_family import modular_map, MODULI

P = [0,1,0,2,0,1,3,1,3,3,0,2,2,0,2,2,1,1,3,0,2]
Q = [0,1,2,3,2,3,1]


def encoded(obj): return (json.dumps(obj, separators=(',', ':'))+'\n').encode()


def main():
    parser = argparse.ArgumentParser(); parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args(); args.out.mkdir(parents=True, exist_ok=False); start = time.perf_counter()
    H, M, d = F.construction(); N = sorted({F.add(a, b) for a in M for b in M})
    assert len(N) == 26
    assert F.add(M[0], M[3]) == F.add(M[1], M[2])
    assert F.add(M[0], M[6]) == F.add(M[4], M[5])
    points = sorted({F.add(h, n) for h in H for n in N}); index = {p: i for i, p in enumerate(points)}
    labels = [[[index[F.add(h, F.add(a, b))] for b in M] for a in M] for h in H]
    nindex = {point: i for i, point in enumerate(N)}
    nlabels = [[nindex[F.add(a, b)] for b in M] for a in M]
    hnlabels = [[index[F.add(h, n)] for n in N] for h in H]
    maps = [modular_map(par) for par in MODULI]
    conjugates = list(map(F.conjugate, points))
    values = [[(f(p), f(c)) for p, c in zip(points, conjugates)] for f in maps]
    edges = []; survivors = 0; target = F.scale(F.ONE, d*d)
    for i, j in combinations(range(len(points)), 2):
        if any(((v[i][0]-v[j][0])*(v[i][1]-v[j][1])-d*d) % par[0]
               for par, v in zip(MODULI, values)): continue
        survivors += 1
        if F.norm(F.sub(points[i], points[j])) == target: edges.append((i, j))
    he, me, ne = [[(i, j) for i, j in combinations(range(len(X)), 2)
                   if F.norm(F.sub(X[i], X[j])) == target] for X in (H, M, N)]
    factor = {tuple(sorted((hnlabels[i][n], hnlabels[j][n]))) for i, j in he for n in range(26)}
    factor |= {tuple(sorted((hnlabels[h][i], hnlabels[h][j]))) for i, j in ne for h in range(21)}
    assert factor <= set(edges)
    extra = sorted(set(edges)-factor)
    colouring = [-1]*len(points)
    for h in range(21):
        for a in range(7):
            for b in range(7):
                v = labels[h][a][b]; c = P[h] ^ Q[a] ^ Q[b]
                assert colouring[v] in (-1, c)
                colouring[v] = c
    assert all(0 <= c < 4 for c in colouring) and all(colouring[i] != colouring[j] for i, j in edges)
    # Exact support of the constraints: only the normalized H triangle occurs
    # in collisions or nonfactor edges. All other H colours remain arbitrary.
    ncolour = [-1]*26
    for a in range(7):
        for b in range(7):
            n = nlabels[a][b]; c = Q[a] ^ Q[b]
            assert ncolour[n] in (-1, c)
            ncolour[n] = c
    assert all(ncolour[i] != ncolour[j] for i, j in ne)
    fibres = [[] for _ in points]
    for h, row in enumerate(hnlabels):
        for n, v in enumerate(row): fibres[v].append((h, n))
    collision_h = sorted({h for fibre in fibres if len(fibre) > 1 for h, n in fibre})
    extra_h = sorted({h for edge in extra for v in edge for h, n in fibres[v]})
    assert collision_h == [0, 7, 14] and extra_h == [7, 14]
    assert all(edge in he for edge in [(0, 7), (0, 14), (7, 14)])
    assert [P[h] for h in (0, 7, 14)] == [0, 1, 2]
    restrictions = []
    for i, j in combinations(range(21), 2):
        retained = sorted({v for h, row in enumerate(hnlabels) if h not in (i, j) for v in row})
        support = set(retained); retained_edges = [(a, b) for a, b in edges if a in support and b in support]
        assert len(retained) <= 19*26 <= 508
        assert all(colouring[a] != colouring[b] for a, b in retained_edges)
        restrictions.append({'omitted_H': [i, j], 'retained_vertices': retained, 'edges': retained_edges})
    assert len(restrictions) == 210
    cert = {'H_colouring': P, 'M_colouring': Q}
    graph = {'denominator': d, 'H': H, 'M': M, 'N': N, 'points': points, 'labels': labels,
             'N_labels': nlabels, 'HN_labels': hnlabels, 'H_edges': he, 'M_edges': me, 'N_edges': ne,
             'edges': edges, 'factor_edges': sorted(factor), 'extra_edges': extra, 'colouring': colouring}
    raw = encoded(graph); restriction_raw = encoded(restrictions); cert_raw = encoded(cert)
    (args.out/'graph.json').write_bytes(raw); (args.out/'restrictions.json').write_bytes(restriction_raw)
    (args.out/'certificate.json').write_bytes(cert_raw)
    hist = Counter((len(row['retained_vertices']), len(row['edges'])) for row in restrictions)
    result = {'status': 'H+M+M AND ALL ITS SUBGRAPHS ARE FOUR-COLOURABLE', 'H_vertices': len(H),
              'M_vertices': len(M), 'N_vertices': len(N), 'H_edges': len(he), 'M_edges': len(me),
              'N_edges': len(ne), 'full_vertices': len(points), 'full_edges': len(edges),
              'factor_edge_images': len(factor), 'extra_mixed_edges': len(extra),
              'HN_fibre_size_histogram': dict(sorted(Counter(map(len, fibres)).items())),
              'collision_H_labels': collision_h, 'extra_edge_H_labels': extra_h,
              'every_proper_H_four_colouring_extends': True,
              'N_colour_edge_checks': len(ne),
              'formal_ordered_HMM_labels': 21*7*7, 'distinct_HN_formal_labels': 21*26,
              'full_pair_tests': len(points)*(len(points)-1)//2,
              'modular_survivors_rechecked_exactly': survivors, 'modular_false_positives': survivors-len(edges),
              'full_colour_edge_checks': len(edges), 'target_supports': len(restrictions),
              'target_supports_distinct': len({tuple(row['retained_vertices']) for row in restrictions}),
              'target_support_histogram_columns': ['vertices', 'edges', 'number_of_H_pairs'],
              'target_support_histogram': [list(key)+[count] for key, count in sorted(hist.items())],
              'target_restriction_colour_edge_checks': sum(len(row['edges']) for row in restrictions),
              'certificate_bytes': len(cert_raw), 'certificate_sha256': sha256(cert_raw).hexdigest(),
              'full_graph_sha256': sha256(raw).hexdigest(), 'restriction_stream_sha256': sha256(restriction_raw).hexdigest(),
              'native_solver_calls': 0}
    (args.out/'result.json').write_text(json.dumps(result, indent=2)+'\n')
    (args.out/'timing.json').write_text(json.dumps({'seconds': time.perf_counter()-start})+'\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__': main()
