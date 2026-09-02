#!/usr/bin/env python3
"""Aggregation of declared sets into Û(A) for 4-point sets (shared by the driver pipeline and the verifier).

labels: {frozenset(points): set of vertices u} over all declared (u, B) (sibling closures + this certificate).
Û(A) = union of the labels of all declared subsets of A ⊇ U(A) = {u : G - u + A is 5-chromatic}.
Every declared set of size <= 3 carries at most 4 labels (checked), so a 4-set with |Û(A)| >= 5 is a declared 4-set
with >= 5 labels or contains two distinct declared sets; hence it is a union of declared sets.  The union-closed
family (within size 4) is enumerated and the valid 4-sets with |Û(A)| >= 5 are the candidates.
Validity (added point set of a 5-vertex-critical graph, min degree 4): Q2K and non-K points need >= 2 neighbours
in A, Q3 points with exactly three vertex neighbours need >= 1."""
import itertools


def union_closure(labels):
    by_point = {}
    for B in labels:
        for p in B:
            by_point.setdefault(p, []).append(B)
    small = {k: [B for B in labels if len(B) == k] for k in (1, 2, 3)}
    unions = set(labels); frontier = set(labels)
    while frontier:
        new = set()
        for S in frontier:
            if len(S) == 4:
                continue
            for p in S:
                for B in by_point[p]:
                    T = S | B
                    if len(T) <= 4 and T not in unions:
                        new.add(T)
            for k in range(1, 5 - len(S)):
                for B in small[k]:
                    if not (B & S):
                        T = S | B
                        if T not in unions:
                            new.add(T)
        unions |= new; frontier = new
    return unions


def uhat(labels, A):
    U = set()
    for k in range(1, len(A) + 1):
        for S in itertools.combinations(A, k):
            U |= labels.get(frozenset(S), set())
    return U


def valid(uni, A):
    for p in A:
        m = sum(1 for q in A if q != p and uni.adjacent(p, q))
        if p >= uni.n3:              # Q2K or non-K: exactly two vertex neighbours
            if m < 2:
                return False
        elif uni.q3deg[p] == 3 and m < 1:
            return False
    return True


def aggregate(uni, labels):
    hist_small = {}
    for B, U in labels.items():
        if len(B) <= 3:
            hist_small[len(U)] = hist_small.get(len(U), 0) + 1
            assert len(U) <= 4, (sorted(B), sorted(U))
    unions = union_closure(labels)
    hist4 = {}; cands = []
    for A in unions:
        if len(A) != 4:
            continue
        A = tuple(sorted(A))
        U = uhat(labels, A)
        hist4[len(U)] = hist4.get(len(U), 0) + 1
        if len(U) >= 5:
            cands.append({'A': list(A), 'Uhat': sorted(U), 'valid': valid(uni, A)})
    cands.sort(key=lambda c: c['A'])
    return {'hist_small': hist_small, 'hist4': hist4, 'n_unions': len(unions), 'candidates': cands}


def main():
    import json, sys, time
    from pathlib import Path
    from paths import HERE, N
    import uncovered_sets as us
    from known_declared import load_known_declared
    t0 = time.time()
    resdir = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / 'results'
    out = Path(sys.argv[2]) if len(sys.argv) > 2 else HERE / 'aggregate4.json'
    uni = us.Universe()
    known, src = load_known_declared()
    labels = {}
    nfiles = 0
    for u in range(N):
        for B in known[u]:
            labels.setdefault(frozenset(B), set()).add(u)
        f = resdir / f'u_{u:03d}.json'
        if f.exists():
            nfiles += 1
            for B, st in json.loads(f.read_text())['declared']:
                labels.setdefault(frozenset(B), set()).add(u)
    agg = aggregate(uni, labels)
    agg.update({'result_files': nfiles, 'declared_sets': len(labels)})
    print(f"result files {nfiles}/{N}; declared sets {len(labels)}; unions {agg['n_unions']}; hist_small {agg['hist_small']}; hist4 {dict(sorted(agg['hist4'].items()))}; candidates {len(agg['candidates'])} (valid {sum(1 for c in agg['candidates'] if c['valid'])})  ({time.time()-t0:.0f}s)")
    out.write_text(json.dumps(agg))


if __name__ == '__main__':
    main()
