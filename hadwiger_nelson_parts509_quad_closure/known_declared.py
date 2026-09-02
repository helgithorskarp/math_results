#!/usr/bin/env python3
"""Declared sets of the published closures per vertex u, as K-point index sets (Q3 index i -> i; Q2K index p ->
n_q3 + p), read from the sibling certificates:
  swap_certificate.json   : 11 certified swap points -> singletons {q} at their vertex u
  pair_certificate.json   : declared pairs of u not containing a swap point of u (174)
  triple_certificate.json : explicitly declared triples per u (2,184: solver-UNSAT or budget)
  triple_certificate.json : Q2K clusters (types ii, iii-a, iii-b-K, rebuilt in the certificate's canonical order
                            through cluster_U.build_q2k_clusters of the triple closure) with a non-empty Û list (282)
Returns {u: [sorted point lists]} (2,651 declared sets on 139 vertices) and the source counts."""
import json, importlib.util
from paths import COMPLETION, SWAP_CERT, PAIR_CERT, TRIPLE_CERT, TRIPLE, Q2K_EXTRA, N


def load_known_declared():
    comp = json.loads(COMPLETION.read_text())
    q3nb = [tuple(sorted(r['neighbors'])) for r in comp['points']]
    n3 = len(q3nb)
    nb_index = {nb: i for i, nb in enumerate(q3nb)}
    assert len(nb_index) == n3
    per_u = {u: set() for u in range(N)}
    src = {}
    swap = json.loads(SWAP_CERT.read_text())
    swaps_u = {}
    for s in swap['swaps']:
        q = nb_index[tuple(sorted(s['q_neighbors']))]
        r = comp['points'][q]
        assert r['x'] == s['q_x'] and r['y'] == s['q_y']
        per_u[s['u']].add((q,)); swaps_u.setdefault(s['u'], set()).add(q)
    src['swaps'] = sum(len(v) for v in swaps_u.values())
    pair = json.loads(PAIR_CERT.read_text())
    n = 0
    for u, lst in enumerate(pair['declared_pairs']):
        sw = swaps_u.get(u, set())
        for a, b in lst:
            if a in sw or b in sw:
                continue
            per_u[u].add(tuple(sorted((a, b)))); n += 1
    src['pairs'] = n
    tc = json.loads(TRIPLE_CERT.read_text())
    n = 0
    for u, lst in enumerate(tc['declared_triples']):
        for t in lst:
            a, b, c = t[:3]
            per_u[u].add(tuple(sorted((a, b, c)))); n += 1
    src['triples'] = n
    spec = importlib.util.spec_from_file_location('cu', TRIPLE / 'cluster_U.py')
    cu = importlib.util.module_from_spec(spec); spec.loader.exec_module(cu)
    cls = cu.build_q2k_clusters(Q2K_EXTRA)
    assert len(cls) == tc['cluster_count'] == len(tc['cluster_U'])
    n = 0
    for cl, U in zip(cls, tc['cluster_U']):
        if not U:
            continue
        pts = tuple(sorted(n3 + p['q2k'] if 'q2k' in p else p['q3'] for p in cl['points']))
        for u in U:
            per_u[u].add(pts); n += 1
    src['q2k_clusters'] = n
    assert all(not U for U in tc['nonk_cluster_U'])
    return {u: sorted(list(s) for s in per_u[u]) for u in range(N)}, src


if __name__ == '__main__':
    per_u, src = load_known_declared()
    print('sources', src, 'total', sum(len(v) for v in per_u.values()), 'vertices', sum(1 for v in per_u.values() if v))
