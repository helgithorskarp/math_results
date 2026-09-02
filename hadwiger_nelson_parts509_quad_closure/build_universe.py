#!/usr/bin/env python3
"""Universe for the all-anchored delete-5-add-4 closure, rebuilt from the committed sibling data.

K-points: Q3 (completion points with >= 3 vertex neighbours, exact K-coordinates, sibling swap closure) followed by
Q2K (K-rational points with exactly two vertex neighbours, q2k_extra.json of the sibling triple closure); internal
unit edges among K-points: Q3-Q3 (ambient_w3_edges.json of the pair closure, exhaustively tested there), Q2K-Q3 and
Q2K-Q2K (exact, q2k_extra.json).  Non-K points (nonk_labels of q2k_extra.json, exactly two vertex neighbours =
their generating pair): unit edges only among themselves (nonk_exact.json, exact), never adjacent to K-points
(a point at unit distance from three points of K^2 is their circumcentre, hence in K^2).
Also lists the connected 3- and 4-subsets of the K-internal graph with their edge patterns, and the non-K unit
triangles, diamonds and K4s.
usage: build_universe.py [OUT.json]   (default: universe4.json next to this file; written for caching only)
"""
import json, sys, time, itertools, hashlib
from pathlib import Path
from paths import COMPLETION, AMBIENT, Q2K_EXTRA, NONK_EXACT, N, HERE


def build():
    t0 = time.time()
    comp = json.loads(COMPLETION.read_text())
    q3nb = [sorted(r['neighbors']) for r in comp['points']]
    assert all(len(nb) >= 3 for nb in q3nb)
    amb = json.loads(AMBIENT.read_text())
    q3q3 = sorted(set((min(a, b) - N, max(a, b) - N) for a, b in amb['edges'] if a >= N and b >= N))
    ex = json.loads(Q2K_EXTRA.read_text())
    q2k = ex['q2k']
    n3, n2 = len(q3nb), len(q2k)
    nbrs = q3nb + [sorted(r['neighbors']) for r in q2k]
    assert all(len(nb) == 2 for nb in nbrs[n3:])
    kedges = set(q3q3)
    for p, a in ex['adj_q2k_q3']:
        kedges.add((a, n3 + p))
    for p, q in ex['adj_q2k_q2k']:
        kedges.add((n3 + min(p, q), n3 + max(p, q)))
    kedges = sorted(kedges)
    nk = n3 + n2
    adj = [set() for _ in range(nk)]
    for a, b in kedges:
        adj[a].add(b); adj[b].add(a)
    kedges_set = set(kedges)
    conn3, conn4 = set(), set()
    for a, b in kedges:
        for c in (adj[a] | adj[b]) - {a, b}:
            conn3.add(tuple(sorted((a, b, c))))
    conn3 = sorted(conn3)
    for t in conn3:
        for c in (adj[t[0]] | adj[t[1]] | adj[t[2]]) - set(t):
            conn4.add(tuple(sorted(t + (c,))))
    conn4 = sorted(conn4)

    def shape(S):
        return tuple(int((S[i], S[j]) in kedges_set) for i, j in itertools.combinations(range(len(S)), 2))
    sh3 = [shape(t) for t in conn3]; sh4 = [shape(t) for t in conn4]
    nx = json.loads(NONK_EXACT.read_text())
    labels = ex['nonk_labels']
    lab_index = {tuple(l): i for i, l in enumerate(labels)}
    assert len(lab_index) == len(labels)
    nonk_nbrs = [[l[0], l[1]] for l in labels]
    nonk_edges = sorted(set(tuple(sorted((lab_index[tuple(a)], lab_index[tuple(b)]))) for a, b in nx['unit_pairs']))
    assert len(nonk_edges) == len(nx['unit_pairs']) == nx['cases']['A'] and nx['cases']['B'] == 0
    assert nx['k_point_candidates_unit'] == 0
    nadj = {}
    for a, b in nonk_edges:
        nadj.setdefault(a, set()).add(b); nadj.setdefault(b, set()).add(a)
    tri = set()
    for a, b in nonk_edges:
        for c in nadj[a] & nadj[b]:
            tri.add(tuple(sorted((a, b, c))))
    tri = sorted(tri)
    assert len(tri) == nx['triangles']
    dia, k4 = set(), set()
    for a, b in nonk_edges:
        cn = sorted(nadj[a] & nadj[b])
        for c, d in itertools.combinations(cn, 2):
            S = tuple(sorted((a, b, c, d)))
            (k4 if d in nadj[c] else dia).add(S)
    dia = sorted(dia - k4); k4 = sorted(k4)
    out = {'n_q3': n3, 'n_q2k': n2, 'nbrs': nbrs, 'kedges': kedges, 'conn3': conn3, 'shape3': sh3, 'conn4': conn4, 'shape4': sh4,
           'nonk_labels': labels, 'nonk_nbrs': nonk_nbrs, 'nonk_edges': nonk_edges, 'nonk_triangles': tri, 'nonk_diamonds': dia, 'nonk_k4': k4,
           'summary': {'q3': n3, 'q2k': n2, 'k_edges': len(kedges), 'q3q3': len(q3q3), 'q2k_q3': len(ex['adj_q2k_q3']), 'q2k_q2k': len(ex['adj_q2k_q2k']),
                       'conn3': len(conn3), 'k_triangles': sum(1 for s in sh3 if sum(s) == 3), 'conn4': len(conn4),
                       'nonk_points': len(labels), 'nonk_edges': len(nonk_edges), 'nonk_triangles': len(tri), 'nonk_diamonds': len(dia), 'nonk_k4': len(k4),
                       'seconds': round(time.time() - t0, 1)}}
    return out


def main():
    out = build()
    dest = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / 'universe4.json'
    s = json.dumps(out)
    dest.write_text(s)
    print(json.dumps(out['summary']))
    print('universe sha256 (without summary):', hashlib.sha256(json.dumps({k: v for k, v in out.items() if k != 'summary'}).encode()).hexdigest())


if __name__ == '__main__':
    main()
