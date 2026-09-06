"""Exact 252-placement census of (H+M) union (H+rM), with a fixed baseline colour."""
from pathlib import Path
from itertools import combinations, product
from collections import Counter
from hashlib import sha256
import argparse, json, math, sys, time

HERE = Path(__file__).resolve().parent
PARENT = HERE.parent/'hadwiger_nelson_heptagon_moser_sum'
sys.path.insert(0, str(PARENT))
import field as F
import contacts as C
from rotation_family import modular_map, MODULI

H_COLOUR = [0,1,0,2,0,1,3,1,3,3,0,2,2,0,2,2,1,1,3,0,2]
BASE_COLOUR = [0,1,2,3,1,2,0]


def encoded(obj):
    return (json.dumps(obj, separators=(',', ':'))+'\n').encode()


def rotations():
    inherited = json.loads((PARENT/'contacts_certificate.json').read_text())
    angles = sorted({C.multiply(C.root(6*k), (tuple(row['r'][0]), row['r'][1]))
                     for row in inherited for k in range(7)})
    assert len(inherited) == 36 and len(angles) == 252
    assert all(F.norm(a) == F.scale(F.ONE, d*d) for a, d in angles)
    return angles


def graph(r, H, M, d0, maps):
    rn, rd = r; d = d0*rd
    hh = [F.scale(h, rd) for h in H]
    blocks = [[F.scale(m, rd) for m in M], [F.mul(rn, m) for m in M]]
    formal = [[F.add(h, m) for h in hh for m in block] for block in blocks]
    common = math.gcd(d, *(x for block in formal for point in block for x in point))
    d //= common
    formal = [[tuple(x//common for x in p) for p in block] for block in formal]
    points = sorted(set(formal[0]+formal[1])); index = {p: i for i, p in enumerate(points)}
    labels = [[index[p] for p in block] for block in formal]
    sets = list(map(set, labels)); overlap = sorted(sets[0] & sets[1])
    conjugates = list(map(F.conjugate, points))
    values = [[(f(p), f(c)) for p, c in zip(points, conjugates)] for f in maps]
    edges = []; survivors = 0; unit = F.scale(F.ONE, d*d)
    for i, j in combinations(range(len(points)), 2):
        if any(((v[i][0]-v[j][0])*(v[i][1]-v[j][1])-d*d) % par[0]
               for par, v in zip(MODULI, values)): continue
        survivors += 1
        if F.norm(F.sub(points[i], points[j])) == unit: edges.append((i, j))
    component = [[e for e in edges if e[0] in ss and e[1] in ss] for ss in sets]
    cross = [e for e in edges if not any(e[0] in ss and e[1] in ss for ss in sets)]
    return {'r': r, 'denominator': d, 'points': points, 'labels': labels, 'edges': edges,
            'component_edges': component, 'new_cross_edges': cross, 'overlap': overlap,
            'modular_survivors': survivors}


def colouring(g, p, q0, q1):
    row = [-1]*len(g['points'])
    for labels, q in zip(g['labels'], (q0, q1)):
        for ij, vertex in enumerate(labels):
            colour = p[ij//7] ^ q[ij % 7]
            if row[vertex] not in (-1, colour): return None
            row[vertex] = colour
    if not all(0 <= c < 4 for c in row): return None
    return row if all(row[i] != row[j] for i, j in g['edges']) else None


def main():
    parser = argparse.ArgumentParser(); parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args(); args.out.mkdir(parents=True, exist_ok=False)
    start = time.perf_counter()
    H, M, d = F.construction(); angles = rotations()
    maps = [modular_map(par) for par in MODULI]
    me = [(i, j) for i, j in combinations(range(7), 2)
          if F.norm(F.sub(M[i], M[j])) == F.scale(F.ONE, d*d)]
    qs = [(0,)+tail for tail in product(range(4), repeat=6)
          if all(((0,)+tail)[i] != ((0,)+tail)[j] for i, j in me)]
    assert len(qs) == 96
    (args.out/'rotations.json').write_bytes(encoded(angles))
    pool, cases = [], []; stream = sha256(); hist = Counter(); support_hashes = set()
    pairs = survivors = edge_checks = cross_total = 0
    for ri, r in enumerate(angles):
        g = graph(r, H, M, d, maps)
        q = next((q for q in qs if colouring(g, H_COLOUR, BASE_COLOUR, q) is not None), None)
        assert q is not None, ('No compatible fixed-baseline witness', ri)
        if q not in pool: pool.append(q)
        cases.append(pool.index(q))
        raw = encoded(g); stream.update(raw)
        (args.out/f'{ri:03}.graph.json').write_bytes(raw)
        support_hashes.add(sha256(encoded([g['denominator'], g['points']])).hexdigest())
        n, e, x, o = len(g['points']), len(g['edges']), len(g['new_cross_edges']), len(g['overlap'])
        hist[n, e, x, o] += 1
        pairs += n*(n-1)//2; survivors += g['modular_survivors']; edge_checks += e; cross_total += x
        print(json.dumps({'case': ri, 'vertices': n, 'edges': e, 'new_cross_edges': x,
                          'status': 'FIXED BASELINE EXTENDS'}), flush=True)
    cert = {'H_colouring': H_COLOUR, 'baseline_M_colouring': BASE_COLOUR,
            'rotated_M_colourings': pool, 'case_M_indices': cases}
    raw = encoded(cert); (args.out/'certificate.json').write_bytes(raw)
    result = {'status': 'ALL252 COUPLED SUMS ARE FOUR-CHROMATIC', 'rotations': len(angles),
              'distinct_supports': len(support_hashes), 'fixed_baseline_colourings': 1,
              'rotated_M_colourings_used': len(pool), 'full_pair_tests': pairs,
              'modular_survivors_rechecked_exactly': survivors, 'modular_false_positives': survivors-edge_checks,
              'colour_edge_checks': edge_checks, 'new_cross_edge_occurrences': cross_total,
              'case_histogram_columns': ['vertices', 'edges', 'new_cross_edges', 'overlap', 'rotations'],
              'case_histogram': [list(key)+[count] for key, count in sorted(hist.items())],
              'certificate_sha256': sha256(raw).hexdigest(), 'certificate_bytes': len(raw),
              'graph_stream_sha256': stream.hexdigest(),
              'rotation_stream_sha256': sha256(encoded(angles)).hexdigest(), 'native_solver_calls': 0}
    (args.out/'result.json').write_text(json.dumps(result, indent=2)+'\n')
    (args.out/'timing.json').write_text(json.dumps({'seconds': time.perf_counter()-start})+'\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__': main()
