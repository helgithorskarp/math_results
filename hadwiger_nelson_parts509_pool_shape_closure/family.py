#!/usr/bin/env python3
"""Load, exactly verify and normalise a family of killing sets for the sealed pool.

A killing set D subset U is certified by an explicit proper 4-colouring of L u (U \\ D)
(the witness string is indexed by the ambient vertex index; only L u U \\ D is used).
Any blocking X (i.e. L u X not 4-colourable) must meet every killing set, because
X n D = empty would give X subset U \\ D and the witness would 4-colour L u X.
Verification is solver-free: replay the colouring against the exactly recomputed edge list.
"""
from __future__ import annotations
import json, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent


def load_geometry():
    g = json.loads((HERE / 'pool_geometry.json').read_text())
    L, U = list(g['L']), list(g['U'])
    adj = {v: set() for v in L + U}
    for a, b in g['edges']:
        adj[a].add(b); adj[b].add(a)
    return L, U, adj


def verify_witness(col, D, L, U, adj):
    """col: dict vertex -> colour on L u (U \\ D).  Returns True iff proper 4-colouring."""
    verts = set(L) | (set(U) - set(D))
    if set(col) != verts:
        return False
    for v in verts:
        if col[v] not in (0, 1, 2, 3):
            return False
        for w in adj[v]:
            if w in verts and col[w] == col[v]:
                return False
    return True


def load_family(paths, L, U, adj, verify=True):
    Uset = set(U)
    seen = {}
    bad = 0
    for path in paths:
        for line in open(path):
            line = line.strip()
            if not line:
                continue
            r = json.loads(line)
            D = frozenset(r['D'])
            if not D <= Uset:
                bad += 1
                continue
            if verify and D not in seen:
                w = r['witness']
                verts = sorted(set(L) | (Uset - D))
                ok = len(w) == len(verts)
                col = {v: int(w[i]) for i, v in enumerate(verts)} if ok else {}
                if not ok or not verify_witness(col, D, L, U, adj):
                    bad += 1
                    continue
            seen.setdefault(D, r.get('pattern'))
    return seen, bad


def minimalise(sets):
    """Keep only inclusion-minimal sets."""
    order = sorted(sets, key=len)
    keep = []
    for a in order:
        if not any(b <= a for b in keep):
            keep.append(a)
    return keep


if __name__ == '__main__':
    L, U, adj = load_geometry()
    paths = sys.argv[1:]
    if not paths:
        raise SystemExit('usage: family.py FAMILY.jsonl [FAMILY.jsonl ...]')
    fam, bad = load_family(paths, L, U, adj)
    print('distinct killing sets', len(fam), 'rejected', bad)
    mins = minimalise(list(fam))
    print('inclusion-minimal', len(mins))
    from collections import Counter
    print('size histogram', sorted(Counter(len(d) for d in mins).items())[:20])
    singles = [sorted(d)[0] for d in mins if len(d) == 1]
    print('forced vertices (singletons):', len(singles), singles)
    json.dump({'sets': [sorted(d) for d in mins]}, open(HERE / 'family_min.json', 'w'))
