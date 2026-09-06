"""Independent tensor geometry and set-valued symbolic extension audit.

No producer import, modular distance filter, floating point or solver.
"""
from pathlib import Path
from itertools import combinations, product
from collections import Counter
from hashlib import sha256
import argparse, json, sys, time

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent/'hadwiger_nelson_heptagon_moser_sum'))
import audit as A
import contacts_audit as V


def audit_symbols(supports, labels, edges, host_edges):
    assert len(supports) == 483
    assert all(isinstance(s, frozenset) and s <= set(range(11)) for s in supports)
    assert all(supports[labels[h][0][0]] == frozenset({h}) for h in range(11))
    allowed = {frozenset(e) for e in host_edges}
    types = Counter()
    for i, j in edges:
        difference = supports[i] ^ supports[j]
        assert difference in allowed
        types[tuple(sorted(difference))] += 1
    return types


def evaluate(supports, p, edges, he):
    assert A.proper(p, he, 11)
    out = []
    for support in supports:
        c = 0
        for h in support: c ^= p[h]
        out.append(c)
    assert A.proper(out, edges, len(supports))
    return out


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--work', type=Path, required=True)
    args = ap.parse_args(); start = time.perf_counter()
    expected = json.loads((HERE/'expected.json').read_text())
    assert expected == json.loads((args.work/'result.json').read_text())
    cert_raw = (HERE/'certificate.json').read_bytes()
    assert cert_raw == (args.work/'certificate.json').read_bytes()
    assert len(cert_raw) == expected['certificate_bytes'] and sha256(cert_raw).hexdigest() == expected['certificate_sha256']
    cert = json.loads(cert_raw); assert set(cert) == {'H_colouring'}
    graph_raw = (args.work/'graph.json').read_bytes()
    assert sha256(graph_raw).hexdigest() == expected['graph_sha256']
    g = json.loads(graph_raw); assert g['denominator'] == 42
    hl = [0, 1, 2, 3, 4, 5, 6, 7, 14, 8, 15]
    assert g['H_labels'] == hl
    all_h, M = V.factors(); H = [all_h[i] for i in hl]; d = 42
    r = A.zp(1); assert A.norm(r) == A.O and A.decode(g['rotation']) == r
    assert all(A.mul(r, all_h[j]) == all_h[7*(j//7)+(j+1)%7] for j in range(21))
    R = [A.mul(r, m) for m in M]
    def decode(rows):
        for row in rows: V.canonical(row, d)
        return [A.decode(row) for row in rows]
    assert decode(g['H']) == H and decode(g['M']) == M and decode(g['R']) == R
    N = decode(g['N']); assert len(N) == len(set(N)) == 49
    assert set(N) == {A.add(a, b) for a in M for b in R}
    points = decode(g['points']); assert len(points) == len(set(points)) == 483
    assert set(points) == {A.add(h, A.add(a, b)) for h in H for a in M for b in R}
    index = {p: i for i, p in enumerate(points)}
    labels = [[[index[A.add(h, A.add(a, b))] for b in R] for a in M] for h in H]
    fibres = [[] for _ in points]
    for h, a, b in product(range(11), range(7), range(7)): fibres[labels[h][a][b]].append([h, a, b])
    assert labels == g['labels'] and fibres == g['fibres']
    assert {str(k): v for k, v in sorted(Counter(map(len, fibres)).items())} == expected['fibre_histogram']
    he, me, re = [V.unit_edges(X, d) for X in (H, M, R)]
    assert [he, me, re] == [g['H_edges'], g['M_edges'], g['R_edges']]
    assert tuple(map(len, (he, me, re))) == (13, 11, 11) and me == re
    assert all([a, b] in he for tri in ((0, 7, 8), (1, 9, 10)) for a, b in combinations(tri, 2))
    print('DIRECT SCAN: all 116403 unordered pairs in the tensor basis', flush=True)
    edges = V.unit_edges(points, d)
    assert edges == g['edges'] and len(edges) == 2061
    factor = set()
    # Independently traverse complete copies of each factor in the triple sum.
    for a, b in product(range(7), repeat=2):
        for i, j in he: factor.add(tuple(sorted((labels[i][a][b], labels[j][a][b]))))
    for h, b in product(range(11), range(7)):
        for i, j in me: factor.add(tuple(sorted((labels[h][i][b], labels[h][j][b]))))
    for h, a in product(range(11), range(7)):
        for i, j in re: factor.add(tuple(sorted((labels[h][a][i], labels[h][a][j]))))
    assert sorted(factor) == list(map(tuple, g['factor_edges'])) == list(map(tuple, edges))
    # Symbolic variables are sets, and cancellation is symmetric difference.
    # This check covers every host colouring at once; it does not enumerate a library.
    qa = [frozenset(s) for s in ((), (0, 7), (0, 8), (7, 8), (0, 7), (0, 8), ())]
    qb = [frozenset(s) for s in ((), (1, 9), (1, 10), (9, 10), (1, 9), (1, 10), ())]
    supports = []
    for fibre in fibres:
        choices = {frozenset({h}) ^ qa[a] ^ qb[b] for h, a, b in fibre}
        assert len(choices) == 1
        supports.append(choices.pop())
    bits = lambda s: sum(2**h for h in s)
    assert list(map(bits, qa)) == g['M_template'] and list(map(bits, qb)) == g['R_template']
    assert list(map(bits, supports)) == g['symbolic_masks']
    types = audit_symbols(supports, labels, edges, he)
    assert [list(e)+[n] for e, n in sorted(types.items())] == expected['edge_projection_histogram']
    assert len(set(supports)) == expected['distinct_symbolic_masks'] == 112
    colour = evaluate(supports, cert['H_colouring'], edges, he)
    assert colour == g['colouring'] and len(set(colour)) == 4
    assert set(cert['H_colouring']) == {0, 1, 2}
    # A retained spindle proves that the complete graph needs at least four colours.
    assert all(e in me for e in [[0, 1], [0, 2], [1, 2]])
    assert not any(A.proper([0, 1, 2]+list(tail), me, 7) for tail in product(range(3), repeat=4))
    embedding = [labels[0][a][0] for a in range(7)]
    assert len(set(embedding)) == 7
    assert all(tuple(sorted((embedding[i], embedding[j]))) in factor for i, j in me)
    rejected = 0
    for bad in ([0]*11, cert['H_colouring'][:-1], [4]+cert['H_colouring'][1:]):
        try: evaluate(supports, bad, edges, he)
        except AssertionError: rejected += 1
    bad = supports.copy(); bad[edges[0][0]] = bad[edges[0][1]]
    try: audit_symbols(bad, labels, edges, he)
    except AssertionError: rejected += 1
    bad_colour = colour.copy(); bad_colour[edges[0][0]] = bad_colour[edges[0][1]]
    assert not A.proper(bad_colour, edges, len(points)); rejected += 1
    assert rejected == 5
    result = {'status': expected['status'], 'exact_support_and_all_fibres_compared_entrywise': True,
              'distance_method': 'All pairs directly in characteristic zero; no modular filter',
              'full_pair_norm_checks': len(points)*(len(points)-1)//2, 'factor_pair_norm_checks': 97,
              'complete_unit_edge_list_compared_entrywise': True, 'vertices': len(points), 'edges': len(edges),
              'factor_edges': len(factor), 'extra_mixed_edges': 0, 'formal_labels_compared': 539,
              'symbolic_fibres_checked': len(fibres), 'set_valued_host_edge_differences_checked': len(edges),
              'host_colours_preserved': 11, 'every_host_four_colouring_extends': True,
              'colour_edge_checks': len(edges), 'all_subgraphs_four_colourable': True,
              'normalized_spindle_three_colourings_rejected': 81, 'spindle_embeddings_checked': 1,
              'invalid_inputs_or_certificates_rejected': rejected, 'native_solver_calls': 0,
              'seconds': time.perf_counter()-start}
    (args.work/'audit.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__': main()
