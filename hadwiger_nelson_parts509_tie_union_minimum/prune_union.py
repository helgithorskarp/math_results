#!/usr/bin/env python3
"""Prune a union: iteratively delete vertices of degree <= 3 within the union (they are never in a
vertex-critical, hence never in a minimum-order, 5-chromatic subgraph); restrict the forced-vertex
file accordingly (forced status is unchanged for surviving vertices: A* − u is 5-chromatic iff the
pruned A' − u is, because deleting a vertex of degree <= 3 preserves 4-colourability both ways).
usage: prune_union.py UNION FORCED AMBIENT OUT_UNION OUT_FORCED"""
import os, json, sys
U = json.loads(open(sys.argv[1]).read()); Fj = json.loads(open(sys.argv[2]).read()); amb = json.loads(open(sys.argv[3]).read())
S = set(U['start'])
adj = {v: set() for v in S}
for a, b in amb['edges']:
    if a in S and b in S:
        adj[a].add(b); adj[b].add(a)
removed = []
changed = True
while changed:
    changed = False
    for v in sorted(S):
        if len(adj[v]) <= 3:
            S.remove(v); removed.append(v)
            for w in adj[v]:
                adj[w].discard(v)
            adj.pop(v); changed = True
assert all(u < 509 for u in removed) is False or True
start = sorted(S)
print(f'pruned {len(removed)} vertices (degree <= 3 iteratively): {removed[:20]}{"..." if len(removed) > 20 else ""}; union {len(U["start"])} -> {len(start)}')
assert not any(v < 509 for v in removed), 'a Parts vertex would be pruned'
old_star = sorted(U['start'])
wit = {}
for u, w in Fj['witness'].items():
    u = int(u)
    if u not in S:
        continue
    verts = [v for v in old_star if v != u]
    col = dict(zip(verts, w))
    wit[str(u)] = ''.join(col[v] for v in start if v != u)
forced = [u for u in Fj['forced'] if u in S]; unforced = [u for u in Fj['unforced'] if u in S]
assert len(forced) + len(unforced) == len(start)
json.dump({'start': start, 'added_points': [p for p in U['added_points'] if p in S], 'deleted_vertices': U.get('deleted_vertices', []), 'pruned': removed, 'note': 'pruned: ' + U.get('note', '')}, open(sys.argv[4], 'w'))
json.dump({'vertices': start, 'forced': forced, 'unforced': unforced, 'witness': wit}, open(sys.argv[5], 'w'))
print(f'forced {len(forced)}, unforced {len(unforced)} in the pruned union; wrote {sys.argv[4]}, {sys.argv[5]}')
