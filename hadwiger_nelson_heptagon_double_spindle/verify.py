"""Direct characteristic-zero tensor-basis audit; no modular distance filter."""
from pathlib import Path
from itertools import combinations, combinations_with_replacement, product
from collections import Counter
from hashlib import sha256
import argparse, copy, json, sys, time

HERE = Path(__file__).resolve().parent
PARENT = HERE.parent/'hadwiger_nelson_heptagon_moser_sum'
sys.path.insert(0, str(PARENT))
import audit as A
import contacts_audit as V


def descend(p, q, labels, n, edges, he, me):
    assert A.proper(p, he, 21) and A.proper(q, me, 7)
    assert len(labels) == 21 and all(len(row) == 7 and all(len(col) == 7 for col in row) for row in labels)
    values = [set() for _ in range(n)]
    for h, a, b in product(range(21), range(7), range(7)):
        vertex = labels[h][a][b]
        assert type(vertex) is int and 0 <= vertex < n
        values[vertex].add(p[h] ^ q[a] ^ q[b])
    assert all(len(v) == 1 for v in values)
    colour = [next(iter(v)) for v in values]
    assert A.proper(colour, edges, n)
    return colour


def main():
    parser = argparse.ArgumentParser(); parser.add_argument('--work', type=Path, required=True)
    args = parser.parse_args(); start = time.perf_counter()
    expected = json.loads((HERE/'expected.json').read_text())
    assert expected == json.loads((args.work/'result.json').read_text())
    raw = (HERE/'certificate.json').read_bytes()
    assert raw == (args.work/'certificate.json').read_bytes()
    assert len(raw) == expected['certificate_bytes'] and sha256(raw).hexdigest() == expected['certificate_sha256']
    cert = json.loads(raw); p, q = cert['H_colouring'], cert['M_colouring']
    graph_raw = (args.work/'graph.json').read_bytes()
    assert sha256(graph_raw).hexdigest() == expected['full_graph_sha256']
    g = json.loads(graph_raw); assert g['denominator'] == 42
    H, M = V.factors(); d = 42
    # Enumerate 28 unordered pairs, independently of the producer's 49 ordered pairs.
    unordered = {(i, j): A.add(M[i], M[j]) for i, j in combinations_with_replacement(range(7), 2)}
    Nset = set(unordered.values()); assert len(unordered) == 28 and len(Nset) == 26
    fibres = {}
    for pair, point in unordered.items(): fibres.setdefault(point, []).append(pair)
    duplicate_pairs = sorted(sorted(pairs) for pairs in fibres.values() if len(pairs) > 1)
    assert duplicate_pairs == [[(0, 3), (1, 2)], [(0, 6), (4, 5)]]
    def decode(rows):
        for row in rows: V.canonical(row, d)
        return list(map(A.decode, rows))
    assert decode(g['H']) == H and decode(g['M']) == M
    N = decode(g['N']); assert len(N) == len(set(N)) == 26 and set(N) == Nset
    points = decode(g['points'])
    assert len(points) == len(set(points)) == 522 and set(points) == {A.add(h, n) for h in H for n in N}
    index = {point: i for i, point in enumerate(points)}; ni = {point: i for i, point in enumerate(N)}
    labels = [[[index[A.add(h, A.add(a, b))] for b in M] for a in M] for h in H]
    nlabels = [[ni[A.add(a, b)] for b in M] for a in M]
    hnlabels = [[index[A.add(h, n)] for n in N] for h in H]
    assert labels == g['labels'] and nlabels == g['N_labels'] and hnlabels == g['HN_labels']
    he, me, ne = V.unit_edges(H, d), V.unit_edges(M, d), V.unit_edges(N, d)
    assert [he, me, ne] == [g['H_edges'], g['M_edges'], g['N_edges']]
    assert tuple(map(len, (he, me, ne))) == (42, 11, 69)
    print('DIRECT SCAN: every one of the 135981 full-support pairs', flush=True)
    # No finite-field, floating-point, approximate or cached producer predicate.
    target = A.scale(A.O, d*d)
    edges = [[i, j] for i, j in combinations(range(len(points)), 2)
             if A.norm(A.sub(points[i], points[j])) == target]
    assert edges == g['edges']
    factor = {tuple(sorted((hnlabels[i][n], hnlabels[j][n]))) for i, j in he for n in range(26)}
    factor |= {tuple(sorted((hnlabels[h][i], hnlabels[h][j]))) for i, j in ne for h in range(21)}
    assert sorted(factor) == list(map(tuple, g['factor_edges']))
    assert factor <= set(map(tuple, edges))
    extra = sorted(set(map(tuple, edges))-factor)
    assert extra == list(map(tuple, g['extra_edges'])) and len(extra) == 2
    colour = descend(p, q, labels, len(points), edges, he, me)
    assert colour == g['colouring']
    # Universal extension: after relabelling the triangle colours, the
    # nonfactor conditions mention no other H colour variable.
    nvalues = [set() for _ in N]
    for a in range(7):
        for b in range(7): nvalues[nlabels[a][b]].add(q[a] ^ q[b])
    assert all(len(values) == 1 for values in nvalues)
    psi = [next(iter(values)) for values in nvalues]
    assert A.proper(psi, ne, 26) and psi[ni[A.Z]] == 0
    fibres = [[] for _ in points]
    for h, row in enumerate(hnlabels):
        for n, vertex in enumerate(row): fibres[vertex].append((h, n))
    collision_h = sorted({h for fibre in fibres if len(fibre) > 1 for h, n in fibre})
    extra_h = sorted({h for edge in extra for v in edge for h, n in fibres[v]})
    assert collision_h == expected['collision_H_labels'] == [0, 7, 14]
    assert extra_h == expected['extra_edge_H_labels'] == [7, 14]
    assert [p[h] for h in (0, 7, 14)] == [0, 1, 2]
    assert all(edge in he for edge in [[0, 7], [0, 14], [7, 14]])
    assert {str(k): v for k, v in sorted(Counter(map(len, fibres)).items())} == expected['HN_fibre_size_histogram']
    assert expected['every_proper_H_four_colouring_extends'] is True
    # Consistency on every nontrivial fibre and every extra edge follows from
    # these fixed triangle colours, as verified in the full witness above.
    # The spindle's triangle may be normalized in any hypothetical three-colouring.
    assert [0, 1] in me and [0, 2] in me and [1, 2] in me
    assert not any(A.proper([0, 1, 2]+list(tail), me, 7) for tail in product(range(3), repeat=4))
    embeddings = [labels[h][0] for h in range(21)]
    es = set(map(tuple, edges))
    assert all(len(set(row)) == 7 and all(tuple(sorted((row[i], row[j]))) in es for i, j in me)
               for row in embeddings)
    restriction_raw = (args.work/'restrictions.json').read_bytes()
    assert sha256(restriction_raw).hexdigest() == expected['restriction_stream_sha256']
    supplied = json.loads(restriction_raw); assert len(supplied) == 210
    restrictions = []; retained_checks = 0; histogram = Counter()
    for i, j in combinations(range(21), 2):
        # Rebuild each support from exact coordinate sums, not deletion of global vertex labels.
        support = {A.add(h, n) for k, h in enumerate(H) if k not in (i, j) for n in N}
        retained = sorted(index[point] for point in support); selected = set(retained)
        ee = [edge for edge in edges if set(edge) <= selected]
        assert len(selected) <= 19*26 <= 508 and all(colour[a] != colour[b] for a, b in ee)
        witness_h = next(k for k in range(21) if k not in (i, j))
        assert set(embeddings[witness_h]) <= selected
        restrictions.append({'omitted_H': [i, j], 'retained_vertices': retained, 'edges': ee})
        histogram[len(retained), len(ee)] += 1; retained_checks += len(ee)
    assert restrictions == supplied
    assert len({tuple(row['retained_vertices']) for row in restrictions}) == 210
    assert [list(k)+[v] for k, v in sorted(histogram.items())] == expected['target_support_histogram']
    assert retained_checks == expected['target_restriction_colour_edge_checks']
    assert len(points) == expected['full_vertices'] and len(edges) == expected['full_edges']
    assert len(factor) == expected['factor_edge_images']
    rejected = 0
    bad = copy.deepcopy(labels); bad[0][0][0] = len(points)
    try: descend(p, q, bad, len(points), edges, he, me)
    except AssertionError: rejected += 1
    for bad_p, bad_q in (([0]*21, q), (p, [0]*7), (p[:-1], q)):
        try: descend(bad_p, bad_q, labels, len(points), edges, he, me)
        except AssertionError: rejected += 1
    bad_colour = colour.copy(); bad_colour[edges[0][0]] = bad_colour[edges[0][1]]
    assert not A.proper(bad_colour, edges, len(points)); rejected += 1
    assert rejected == 5
    result = {'status': expected['status'], 'independent_distance_method': 'Every pair directly in characteristic zero; no modular filter',
              'unordered_M_pairs_checked': 28, 'distinct_M_pair_sums': 26,
              'duplicate_unordered_pair_classes': [[[i, j] for i, j in pairs] for pairs in duplicate_pairs],
              'full_supports_compared': 1, 'full_unit_graphs_compared_entrywise': 1,
              'full_pair_norm_checks': len(points)*(len(points)-1)//2, 'formal_HMM_labels_compared': 1029,
              'HN_labels_compared': 546, 'full_colour_edge_checks': len(edges),
              'factor_edge_images': len(factor), 'extra_mixed_edges': len(extra),
              'collision_H_labels': collision_h, 'extra_edge_H_labels': extra_h,
              'N_colour_edge_checks': len(ne), 'zero_N_point_has_colour_zero': True,
              'all_nonfactor_constraints_use_only_the_normalized_H_triangle': True,
              'every_proper_H_four_colouring_extends': True,
              'target_supports_and_edge_lists_compared_entrywise': 210,
              'target_restriction_colour_edge_checks': retained_checks,
              'target_spindle_embeddings_checked': 210, 'normalized_three_colour_assignments_rejected': 81,
              'invalid_inputs_or_colourings_rejected': rejected, 'native_solver_calls': 0,
              'seconds': time.perf_counter()-start}
    (args.work/'audit.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__': main()
