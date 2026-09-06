"""Tensor-basis check of the six triple graphs, pair cover and common colouring."""
from pathlib import Path
from itertools import combinations, product
from hashlib import sha256
import argparse, copy, json, math, time
import check as Q

A, V = Q.A, Q.V
HERE = Path(__file__).resolve().parent
NAMES = ['1', 'eta*rhobar', 'eta', 'etabar*rhobar', 'etabar']
PAIRS = list(combinations(range(1, 5), 2))


def prescribed_rotations():
    eta, etab = A.sub(A.OMEGA, A.O), A.scale(A.OMEGA, -1)
    rhob = V.canonical(A.sub(A.scale(A.O, 3), A.W), 3)
    rs = [(A.O, 1), V.multiply((eta, 1), rhob), (eta, 1),
          V.multiply((etab, 1), rhob), (etab, 1)]
    assert all(A.norm(a) == A.scale(A.O, d*d) for a, d in rs)
    assert len(set(rs)) == 5
    return rs


def check_pair_cover(cases):
    assert cases == [[0, i, j] for i, j in PAIRS]
    covered = {tuple(sorted(pair)) for case in cases for pair in combinations(case, 2)}
    assert covered == set(combinations(range(5), 2))


def valid_colour(g, p, rows, blocks=None):
    if blocks is None: blocks = list(range(3))
    values = [set() for _ in g['points']]
    for block, row in zip(blocks, rows):
        assert len(row) == 7 and all(type(c) is int and 0 <= c < 4 for c in row)
        for h in range(21):
            for m in range(7): values[g['labels'][block][7*h+m]].add(p[h] ^ row[m])
    if any(len(v) > 1 for v in values): return None
    colour = [next(iter(v)) if v else -1 for v in values]
    if any(colour[i] >= 0 and colour[i] == colour[j] for i, j in g['edges']): return None
    return colour


def main():
    parser = argparse.ArgumentParser(); parser.add_argument('--work', type=Path, required=True)
    args = parser.parse_args(); start = time.perf_counter()
    expected = json.loads((HERE/'triples_expected.json').read_text())
    assert expected == json.loads((args.work/'result.json').read_text())
    raw = (HERE/'triples_certificate.json').read_bytes()
    assert raw == (args.work/'certificate.json').read_bytes()
    assert len(raw) == expected['certificate_bytes'] and sha256(raw).hexdigest() == expected['certificate_sha256']
    cert = json.loads(raw); assert cert['orientation_names'] == NAMES
    p, colours = cert['H_colouring'], cert['M_colourings']
    assert len(colours) == 5
    H, M = V.factors(); he, me = V.unit_edges(H, 42), V.unit_edges(M, 42)
    assert A.proper(p, he, 21) and all(A.proper(c, me, 7) and c[0] == 0 for c in colours)
    assert len(he) == 42 and len(me) == 11 and M[0] == A.Z
    assert [0, 1] in me and [0, 2] in me and [1, 2] in me
    assert not any(A.proper([0, 1, 2]+list(tail), me, 7) for tail in product(range(3), repeat=4))
    # An independent complete enumeration of normalized M colourings.
    rows = []; row = [0]+[-1]*6
    def extend(i):
        if i == 7: rows.append(row.copy()); return
        for c in range(4):
            row[i] = c
            if all(row[a] < 0 or row[b] < 0 or row[a] != row[b] for a, b in me): extend(i+1)
        row[i] = -1
    extend(1); assert len(rows) == 96 and rows == sorted(rows)
    rs = json.loads((args.work/'rotations.json').read_text())
    assert list(map(V.decode, rs)) == prescribed_rotations()
    maps = [Q.modular_map(par) for par in Q.MODULI]
    graphs = []; stream = sha256(); total_pairs = total_edges = total_extra = survivors = 0
    global_colour = {}; global_edges = set(); global_components = [set() for _ in range(5)]
    for case, (a, b) in enumerate(PAIRS):
        raw = (args.work/f'{case}.graph.json').read_bytes(); stream.update(raw); g = json.loads(raw)
        components = [0, a, b]; assert g['components'] == components
        selected = [rs[i] for i in components]; assert g['rotations'] == selected
        scale = math.lcm(*(den for num, den in selected)); d = 42*scale
        hh = [A.scale(h, scale) for h in H]
        mm = [[A.scale(A.mul(A.decode(num), m), scale//den) for m in M] for num, den in selected]
        formal = [[A.add(h, m) for h in hh for m in block] for block in mm]
        gd = g['denominator']; assert type(gd) is int and gd > 0 and d % gd == 0
        points = []
        for point in g['points']:
            V.canonical(point, gd)
            points.append(A.scale(A.decode(point), d//gd))
        assert len(set(points)) == len(points) and set(points) == set().union(*map(set, formal))
        index = {point: i for i, point in enumerate(points)}
        labels = [[index[point] for point in block] for block in formal]
        assert labels == g['labels']
        edges, count = Q.exact_edges(points, d, maps); assert edges == g['edges']
        sets = list(map(set, labels)); base_pairs = [sets[0] | sets[k] for k in (1, 2)]
        extra = [edge for edge in edges if not any(set(edge) <= ss for ss in base_pairs)]
        assert extra == g['new_attachment_edges']
        cc = valid_colour(g, p, [colours[k] for k in components])
        assert cc is not None and A.proper(cc, edges, len(points))
        assert len(set(labels[0][:7])) == 7
        edge_set = set(map(tuple, edges))
        assert all(tuple(sorted((labels[0][i], labels[0][j]))) in edge_set for i, j in me)
        rational = [V.canonical(point, d) for point in points]
        for point, c in zip(rational, cc):
            assert point not in global_colour or global_colour[point] == c
            global_colour[point] = c
        global_edges.update(frozenset((rational[i], rational[j])) for i, j in edges)
        for local, k in enumerate(components):
            component = {rational[i] for i in labels[local]}
            assert not global_components[k] or global_components[k] == component
            global_components[k] = component
        graphs.append(g); total_pairs += len(points)*(len(points)-1)//2
        total_edges += len(edges); total_extra += len(extra); survivors += count
    check_pair_cover([g['components'] for g in graphs])
    assert stream.hexdigest() == expected['triple_graph_stream_sha256']
    # Check the glued support/edge stream entrywise by exact rational coordinates.
    glued_raw = (args.work/'glued_graph.json').read_bytes()
    assert sha256(glued_raw).hexdigest() == expected['glued_graph_sha256']
    glued = json.loads(glued_raw); points = list(map(V.decode, glued['points']))
    assert len(set(points)) == len(points) and set(points) == set(global_colour) == set().union(*global_components)
    assert {frozenset((points[i], points[j])) for i, j in glued['edges']} == global_edges
    assert len(glued['edges']) == len(global_edges)
    assert glued['colouring'] == [global_colour[p] for p in points]
    assert A.proper(glued['colouring'], glued['edges'], len(points))
    # Pair coverage implies every full-union unit edge appears in a checked triple.
    # No distance predicate is rerun on the larger union.
    assert len(points) == expected['union_vertices'] == 513 and len(global_edges) == expected['union_edges'] == 2097
    assert total_pairs == expected['point_pair_tests'] and total_edges == expected['colour_edge_checks']
    assert total_extra == expected['new_attachment_edge_occurrences']
    # Reconstruct the complete fixed-p, fixed-baseline compatibility system.
    domains = {}
    for k in range(1, 5):
        g = next(g for g in graphs if k in g['components']); local = g['components'].index(k)
        domains[k] = [i for i, q in enumerate(rows) if valid_colour(g, p, [colours[0], q], [0, local]) is not None]
    relations = {}
    cases = []
    for g in graphs:
        i, j = g['components'][1:]
        rel = [(a, b) for a in domains[i] for b in domains[j]
               if valid_colour(g, p, [colours[0], rows[a], rows[b]]) is not None]
        relations[i, j] = rel
        cases.append({'components': g['components'], 'vertices': len(g['points']), 'edges': len(g['edges']),
                      'new_attachment_edges': len(g['new_attachment_edges']), 'allowed_M_pairs': len(rel),
                      'pair_relation_is_cartesian': len(rel) == len(domains[i])*len(domains[j])})
    assert cases == expected['cases']
    assignments = [row for row in product(*(domains[i] for i in range(1, 5)))
                   if all((row[i-1], row[j-1]) in rel for (i, j), rel in relations.items())]
    record = {'domains': [domains[i] for i in range(1, 5)],
              'relations': [[i, j, [list(pair) for pair in rel]] for (i, j), rel in relations.items()],
              'lexicographically_first_completion': list(assignments[0]), 'completion_count': len(assignments)}
    compatibility_raw = (HERE/'triples_compatibility.json').read_bytes()
    assert compatibility_raw == (args.work/'compatibility.json').read_bytes()
    assert sha256(compatibility_raw).hexdigest() == expected['compatibility_sha256']
    assert record == json.loads(compatibility_raw)
    assert colours[1:] == [rows[i] for i in assignments[0]]
    restrictive = [pair for pair, rel in relations.items() if len(rel) != len(domains[pair[0]])*len(domains[pair[1]])]
    assert restrictive == [(1, 3), (2, 4)]
    assert len(assignments) == len(relations[1, 3])*len(relations[2, 4]) == 1809
    assert len(assignments) == expected['fixed_H_and_baseline_XOR_completions']
    rejected = 0
    bad = copy.deepcopy([g['components'] for g in graphs]); bad.pop()
    try: check_pair_cover(bad)
    except AssertionError: rejected += 1
    bad = copy.deepcopy([g['components'] for g in graphs]); bad[-1] = bad[0]
    try: check_pair_cover(bad)
    except AssertionError: rejected += 1
    g = graphs[0]; bad = copy.deepcopy([colours[k] for k in g['components']]); bad[1][0] = 1
    assert valid_colour(g, p, bad) is None; rejected += 1
    bad = list(glued['colouring']); i, j = glued['edges'][0]; bad[i] = bad[j]
    assert not A.proper(bad, glued['edges'], len(points)); rejected += 1
    assert rejected == 4
    result = {'status': expected['status'], 'complete_triple_graphs_compared': 6,
              'formal_labels_compared': 2646, 'point_pair_tests': total_pairs,
              'modular_survivors_rechecked_exactly': survivors, 'modular_false_positives': survivors-total_edges,
              'triple_colour_edge_checks': total_edges, 'new_attachment_edge_checks': total_extra,
              'glued_union_vertices': len(points), 'glued_union_edges_checked': len(global_edges),
              'full_union_distance_scan_performed': False, 'component_pairs_covered': 10,
              'fixed_baseline_domain_sizes': list(map(len, domains.values())),
              'pair_relations_compared_entrywise': 6, 'restricted_pair_counts': [67, 27],
              'fixed_H_and_baseline_XOR_completions': len(assignments),
              'nonempty_orientation_subsets_closed': 31, 'spindle_embeddings_checked': 6,
              'normalized_three_colour_assignments_rejected': 81, 'invalid_controls_rejected': rejected,
              'native_solver_calls': 0, 'seconds': time.perf_counter()-start}
    (args.work/'audit.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__': main()
