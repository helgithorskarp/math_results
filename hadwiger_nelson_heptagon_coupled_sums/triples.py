"""Six complete triple graphs and a simultaneous five-component colouring."""
from pathlib import Path
from itertools import combinations, product
from hashlib import sha256
import argparse, json, math, time
import build as B

F, C = B.F, B.C
IDS = [34, 72, 116, 117]
NAMES = ['1', 'eta*rhobar', 'eta', 'etabar*rhobar', 'etabar']


def rotations():
    eta = F.sub(C.root(7)[0], F.ONE)
    etab = F.scale(C.root(7)[0], -1)
    s = F.K.ZERO+F.K.ONE
    rhob = C.canonical(F.sub(F.scale(F.ONE, 5), s), 6)
    out = [(F.ONE, 1), C.multiply((eta, 1), rhob), (eta, 1),
           C.multiply((etab, 1), rhob), (etab, 1)]
    assert out[1:] == [B.rotations()[i] for i in IDS]
    assert all(F.norm(a) == F.scale(F.ONE, d*d) for a, d in out)
    return out


def graph(pair, rotations, H, M, d0, maps):
    components = [0]+list(pair); rs = [rotations[i] for i in components]
    denominator = math.lcm(*(d for n, d in rs)); d = d0*denominator
    hh = [F.scale(h, denominator) for h in H]
    blocks = [[F.scale(F.mul(num, m), denominator//rd) for m in M] for num, rd in rs]
    formal = [[F.add(h, m) for h in hh for m in block] for block in blocks]
    common = math.gcd(d, *(x for block in formal for p in block for x in p)); d //= common
    formal = [[tuple(x//common for x in p) for p in block] for block in formal]
    points = sorted({p for block in formal for p in block}); index = {p: i for i, p in enumerate(points)}
    labels = [[index[p] for p in block] for block in formal]; sets = list(map(set, labels))
    conjugates = list(map(F.conjugate, points))
    values = [[(f(p), f(c)) for p, c in zip(points, conjugates)] for f in maps]
    edges = []; survivors = 0; unit = F.scale(F.ONE, d*d)
    for i, j in combinations(range(len(points)), 2):
        if any(((v[i][0]-v[j][0])*(v[i][1]-v[j][1])-d*d) % par[0]
               for par, v in zip(B.MODULI, values)): continue
        survivors += 1
        if F.norm(F.sub(points[i], points[j])) == unit: edges.append((i, j))
    base_pairs = [sets[0] | sets[k] for k in (1, 2)]
    extra = [e for e in edges if not any(set(e) <= ss for ss in base_pairs)]
    return {'components': components, 'rotations': rs, 'denominator': d, 'points': points,
            'labels': labels, 'edges': edges, 'new_attachment_edges': extra,
            'modular_survivors': survivors}


def colour(g, qrows, blocks=(0, 1, 2)):
    row = [-1]*len(g['points'])
    for k, q in zip(blocks, qrows):
        for ij, v in enumerate(g['labels'][k]):
            c = B.H_COLOUR[ij//7] ^ q[ij % 7]
            if row[v] not in (-1, c): return None
            row[v] = c
    if all(row[i] < 0 or row[j] < 0 or row[i] != row[j] for i, j in g['edges']): return row
    return None


def main():
    parser = argparse.ArgumentParser(); parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args(); args.out.mkdir(parents=True, exist_ok=False); start = time.perf_counter()
    H, M, d = F.construction(); rs = rotations(); maps = [B.modular_map(par) for par in B.MODULI]
    me = [(i, j) for i, j in combinations(range(7), 2)
          if F.norm(F.sub(M[i], M[j])) == F.scale(F.ONE, d*d)]
    qs = [(0,)+tail for tail in product(range(4), repeat=6)
          if all(((0,)+tail)[i] != ((0,)+tail)[j] for i, j in me)]
    assert len(qs) == 96
    graphs = [graph(pair, rs, H, M, d, maps) for pair in combinations(range(1, 5), 2)]
    domains = {}
    for k in range(1, 5):
        g = next(g for g in graphs if k in g['components']); block = g['components'].index(k)
        domains[k] = [j for j, q in enumerate(qs) if colour(g, [B.BASE_COLOUR, q], (0, block)) is not None]
    relations = {}
    for g in graphs:
        i, j = g['components'][1:]
        relations[i, j] = [(a, b) for a, b in product(domains[i], domains[j])
                           if colour(g, [B.BASE_COLOUR, qs[a], qs[b]]) is not None]
    completions = [row for row in product(*(domains[i] for i in range(1, 5)))
                   if all((row[i-1], row[j-1]) in rel for (i, j), rel in relations.items())]
    assert completions, 'No common restricted certificate; preserve the frontier, never claim five-chromaticity'
    first = completions[0]; qrows = [B.BASE_COLOUR]+[qs[i] for i in first]
    cert = {'orientation_names': NAMES, 'H_colouring': B.H_COLOUR, 'M_colourings': qrows}
    cert_raw = B.encoded(cert); (args.out/'certificate.json').write_bytes(cert_raw)
    relation_record = {'domains': [domains[i] for i in range(1, 5)],
                       'relations': [[i, j, rel] for (i, j), rel in relations.items()],
                       'lexicographically_first_completion': first, 'completion_count': len(completions)}
    relation_raw = B.encoded(relation_record); (args.out/'compatibility.json').write_bytes(relation_raw)
    (args.out/'rotations.json').write_bytes(B.encoded(rs))
    stream = sha256(); cases = []; union_points = set(); union_edges = set(); union_colours = {}
    for case, g in enumerate(graphs):
        raw = B.encoded(g); stream.update(raw); (args.out/f'{case}.graph.json').write_bytes(raw)
        row = colour(g, [qrows[k] for k in g['components']]); assert row is not None and all(c >= 0 for c in row)
        points = [C.canonical(p, g['denominator']) for p in g['points']]
        for point, c in zip(points, row):
            assert point not in union_colours or union_colours[point] == c
            union_colours[point] = c
        union_points.update(points)
        union_edges.update(tuple(sorted((points[i], points[j]))) for i, j in g['edges'])
        i, j = g['components'][1:]
        cases.append({'components': g['components'], 'vertices': len(points), 'edges': len(g['edges']),
                      'new_attachment_edges': len(g['new_attachment_edges']),
                      'allowed_M_pairs': len(relations[i, j]),
                      'pair_relation_is_cartesian': len(relations[i, j]) == len(domains[i])*len(domains[j])})
    points = sorted(union_points); index = {p: i for i, p in enumerate(points)}
    edges = sorted(tuple(sorted((index[a], index[b]))) for a, b in union_edges)
    colours = [union_colours[p] for p in points]
    assert all(colours[i] != colours[j] for i, j in edges)
    glued = B.encoded({'points': points, 'edges': edges, 'colouring': colours})
    (args.out/'glued_graph.json').write_bytes(glued)
    result = {'status': 'ONE COLOURING OF THE FIVE-COMPONENT UNION AND ALL ITS SUBGRAPHS',
              'cases': cases, 'complete_triple_graphs': len(graphs),
              'point_pair_tests': sum(len(g['points'])*(len(g['points'])-1)//2 for g in graphs),
              'modular_survivors_rechecked_exactly': sum(g['modular_survivors'] for g in graphs),
              'colour_edge_checks': sum(len(g['edges']) for g in graphs),
              'new_attachment_edge_occurrences': sum(len(g['new_attachment_edges']) for g in graphs),
              'formal_labels': 6*441, 'union_vertices': len(points), 'union_edges': len(edges),
              'glued_graph_checked_by_pair_cover': True, 'full_union_distance_scan_performed': False,
              'component_pairs_covered': 10, 'nonempty_orientation_subsets_closed': 31,
              'fixed_baseline_domain_sizes': list(map(len, domains.values())),
              'non_cartesian_relation_pairs': [[i, j] for (i, j), rel in relations.items()
                  if len(rel) != len(domains[i])*len(domains[j])],
              'fixed_H_and_baseline_XOR_completions': len(completions),
              'certificate_bytes': len(cert_raw), 'certificate_sha256': sha256(cert_raw).hexdigest(),
              'compatibility_sha256': sha256(relation_raw).hexdigest(),
              'triple_graph_stream_sha256': stream.hexdigest(), 'glued_graph_sha256': sha256(glued).hexdigest(),
              'native_solver_calls': 0}
    (args.out/'result.json').write_text(json.dumps(result, indent=2)+'\n')
    (args.out/'timing.json').write_text(json.dumps({'seconds': time.perf_counter()-start})+'\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__': main()
