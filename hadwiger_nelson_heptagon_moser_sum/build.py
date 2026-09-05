"""Exact sum graph, its Cartesian-product edge images, and XOR colourings."""
import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path
import time

import field as F


def unit_edges(points, denominator):
    return [(i, j) for i, j in combinations(range(len(points)), 2)
            if F.norm(F.sub(points[i], points[j])) == F.scale(F.ONE, denominator**2)]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=False)
    started = time.perf_counter()
    H, M, d = F.construction()
    he, me = unit_edges(H, d), unit_edges(M, d)
    assert len(he) == 42 and len(me) == 11
    assert all(F.norm(F.sub(H[a], H[b])) == F.scale(F.ONE, d*d)
               for a, b in [(0, 7), (0, 14), (7, 14)])
    G = sorted({F.add(h, m) for h in H for m in M})
    index = {p: i for i, p in enumerate(G)}
    representations = [[] for _ in G]
    for i, h in enumerate(H):
        for j, m in enumerate(M):
            representations[index[F.add(h, m)]].append((i, j))
    edges = unit_edges(G, d)
    factor = {tuple(sorted((index[F.add(H[a], m)], index[F.add(H[b], m)])))
              for a, b in he for m in M}
    factor |= {tuple(sorted((index[F.add(h, M[a])], index[F.add(h, M[b])])) )
               for a, b in me for h in H}
    assert factor <= set(edges)
    data = {'denominator': d, 'H': H, 'M': M, 'points': G, 'H_edges': he,
            'M_edges': me, 'edges': edges, 'representations': representations,
            'factor_edges': sorted(factor), 'extra_edges': sorted(set(edges)-factor)}
    raw = (json.dumps(data, separators=(',', ':'))+'\n').encode()
    (args.out/'graph.json').write_bytes(raw)
    potentials = json.loads((F.PARENT/'potentials.json').read_text())
    spindle_rows = [(0, 1, 2, 3)+tail for tail in product(range(4), repeat=3)
                    if all(((0, 1, 2, 3)+tail)[a] != ((0, 1, 2, 3)+tail)[b] for a, b in me)]
    colourings, recipes = [], []
    for pi, p in enumerate(potentials):
        assert [p[i] for i in [0, 7, 14]] == [0, 1, 2]
        assert all(p[a] != p[b] for a, b in he)
        for q in spindle_rows:
            c = []
            for fiber in representations:
                colours = {p[a]^q[b] for a, b in fiber}
                assert len(colours) == 1
                c.append(colours.pop())
            assert all(c[a] != c[b] for a, b in edges)
            colourings.append(bytes(c))
            recipes.append({'potential_index': pi, 'p': p, 'q': list(q), 'colouring': c})
    assert len(colourings) == len(set(colourings)) == 420
    certificate = recipes[0]
    (args.out/'certificate.json').write_text(json.dumps(certificate, indent=2)+'\n')
    Hdiff = {F.sub(a, b) for a in H for b in H if a != b}
    Mdiff = {F.sub(a, b) for a in M for b in M if a != b}
    result = {'denominator': d, 'field_degree': 24,
              'H_vertices': len(H), 'H_edges': len(he), 'M_vertices': len(M), 'M_edges': len(me),
              'formal_sum_pairs': len(H)*len(M), 'vertices': len(G), 'unit_edges': len(edges),
              'all_sum_pairs_scanned': len(G)*(len(G)-1)//2,
              'multiplicity_histogram': dict(sorted(Counter(map(len, representations)).items())),
              'collision_fibers': [{'vertex': i, 'representations': r}
                                   for i, r in enumerate(representations) if len(r) > 1],
              'product_edge_occurrences': len(M)*len(he)+len(H)*len(me),
              'distinct_product_edge_images': len(factor), 'extra_unit_edges': len(set(edges)-factor),
              'supplied_H_colourings': len(potentials), 'compatible_normalized_M_colourings': len(spindle_rows),
              'distinct_XOR_colourings_checked': len(colourings),
              'XOR_edge_checks': len(colourings)*len(edges),
              'H_nonzero_directed_differences': len(Hdiff), 'M_nonzero_directed_differences': len(Mdiff),
              'generic_rotation_exception_bound': 3*len(Hdiff)*len(Mdiff),
              'graph_sha256': sha256(raw).hexdigest(),
              'colouring_stream_sha256': sha256(b''.join(sorted(colourings))).hexdigest()}
    (args.out/'result.json').write_text(json.dumps(result, indent=2)+'\n')
    (args.out/'timing.json').write_text(json.dumps({'seconds': time.perf_counter()-started})+'\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
