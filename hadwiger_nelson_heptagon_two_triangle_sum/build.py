"""Exact one-instance construction and symbolic extension certificate."""
from pathlib import Path
from itertools import combinations, product
from collections import Counter
from hashlib import sha256
import argparse, json, sys, time

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent/'hadwiger_nelson_heptagon_moser_sum'))
import field as F
from rotation_family import modular_map, MODULI

H_LABELS = [0, 1, 2, 3, 4, 5, 6, 7, 14, 8, 15]
P = [0, 1, 0, 1, 0, 1, 2, 1, 2, 0, 2]


def encoded(x): return (json.dumps(x, separators=(',', ':'))+'\n').encode()


def template(a, b, c):
    x, y = (1 << a) ^ (1 << b), (1 << a) ^ (1 << c)
    return [0, x, y, x ^ y, x, y, 0]


def evaluate(mask, colouring):
    value = 0
    for h, c in enumerate(colouring):
        if mask & (1 << h): value ^= c
    return value


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--out', type=Path, required=True)
    args = ap.parse_args(); args.out.mkdir(parents=True, exist_ok=False); start = time.perf_counter()
    H, M, d = F.construction(); H = [H[i] for i in H_LABELS]
    r = tuple(F.K.POW[6])+(0,)*12; R = [F.mul(r, m) for m in M]
    assert F.norm(r) == F.ONE
    N = sorted({F.add(a, b) for a in M for b in R})
    assert len(N) == 49
    points = sorted({F.add(h, n) for h in H for n in N})
    assert len(points) == 483 <= 508
    index = {p: i for i, p in enumerate(points)}
    labels = [[[index[F.add(h, F.add(a, b))] for b in R] for a in M] for h in H]
    fibres = [[] for _ in points]
    for h, a, b in product(range(11), range(7), range(7)): fibres[labels[h][a][b]].append([h, a, b])
    target = F.scale(F.ONE, d*d)
    he, me, re = [[(i, j) for i, j in combinations(range(len(X)), 2)
                  if F.norm(F.sub(X[i], X[j])) == target] for X in (H, M, R)]
    assert tuple(map(len, (he, me, re))) == (13, 11, 11) and me == re
    conjugates = list(map(F.conjugate, points)); maps = [modular_map(par) for par in MODULI]
    values = [[(f(p), f(c)) for p, c in zip(points, conjugates)] for f in maps]
    edges = []; survivors = 0
    for i, j in combinations(range(len(points)), 2):
        if any(((v[i][0]-v[j][0])*(v[i][1]-v[j][1])-d*d) % par[0]
               for par, v in zip(MODULI, values)): continue
        survivors += 1
        if F.norm(F.sub(points[i], points[j])) == target: edges.append((i, j))
    factor = {tuple(sorted((labels[i][a][b], labels[j][a][b])))
              for i, j in he for a, b in product(range(7), repeat=2)}
    factor |= {tuple(sorted((labels[h][i][b], labels[h][j][b])))
               for i, j in me for h, b in product(range(11), range(7))}
    factor |= {tuple(sorted((labels[h][a][i], labels[h][a][j])))
               for i, j in re for h, a in product(range(11), range(7))}
    assert set(edges) == factor and len(edges) == 2061
    q, u = template(0, 7, 8), template(1, 9, 10)
    masks = []
    for fibre in fibres:
        choices = {(1 << h) ^ q[a] ^ u[b] for h, a, b in fibre}
        assert len(choices) == 1
        masks.append(choices.pop())
    assert all(masks[labels[h][0][0]] == 1 << h for h in range(11))
    host_differences = {(1 << i) ^ (1 << j): (i, j) for i, j in he}
    edge_types = Counter(host_differences[masks[i] ^ masks[j]] for i, j in edges)
    assert len(P) == 11 and all(0 <= c < 3 for c in P) and all(P[i] != P[j] for i, j in he)
    colour = [evaluate(mask, P) for mask in masks]
    assert all(0 <= c < 4 for c in colour) and all(colour[i] != colour[j] for i, j in edges)
    cert_raw = encoded({'H_colouring': P})
    graph = {'denominator': d, 'H_labels': H_LABELS, 'rotation': r, 'H': H, 'M': M, 'R': R,
             'N': N, 'points': points, 'labels': labels, 'fibres': fibres, 'H_edges': he,
             'M_edges': me, 'R_edges': re, 'edges': edges, 'factor_edges': sorted(factor),
             'M_template': q, 'R_template': u, 'symbolic_masks': masks, 'colouring': colour}
    graph_raw = encoded(graph)
    (args.out/'graph.json').write_bytes(graph_raw); (args.out/'certificate.json').write_bytes(cert_raw)
    result = {'status': 'EVERY HOST FOUR-COLOURING EXTENDS; THE 483-POINT GRAPH HAS CHROMATIC NUMBER FOUR',
              'H_vertices': 11, 'M_vertices': 7, 'R_vertices': 7, 'M_plus_R_vertices': 49,
              'H_edges': len(he), 'M_edges': len(me), 'R_edges': len(re),
              'formal_labels': 539, 'vertices': len(points), 'edges': len(edges),
              'factor_edges': len(factor), 'extra_mixed_edges': 0,
              'fibre_histogram': dict(sorted(Counter(map(len, fibres)).items())),
              'collision_inherited_H_labels': sorted({H_LABELS[h] for f in fibres if len(f)>1 for h,a,b in f}),
              'full_pair_tests': len(points)*(len(points)-1)//2,
              'modular_survivors_checked_exactly': survivors, 'modular_false_positives': survivors-len(edges),
              'symbolic_fibre_checks': len(fibres), 'distinct_symbolic_masks': len(set(masks)),
              'symbolic_host_edge_difference_checks': len(edges), 'host_embeddings_preserved': 11,
              'edge_projection_histogram': [list(e)+[n] for e, n in sorted(edge_types.items())],
              'every_host_four_colouring_extends': True, 'all_subgraphs_four_colourable': True,
              'explicit_host_colours_used': len(set(P)), 'explicit_full_colours_used': len(set(colour)),
              'certificate_bytes': len(cert_raw), 'certificate_sha256': sha256(cert_raw).hexdigest(),
              'graph_sha256': sha256(graph_raw).hexdigest(), 'native_solver_calls': 0, 'target_found': False}
    (args.out/'result.json').write_text(json.dumps(result, indent=2)+'\n')
    (args.out/'timing.json').write_text(json.dumps({'seconds': time.perf_counter()-start})+'\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__': main()
