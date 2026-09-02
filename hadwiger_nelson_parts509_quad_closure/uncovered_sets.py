#!/usr/bin/env python3
"""All-anchored delete-5-add-4 closure of the Parts-509 graph: per-vertex enumeration of uncovered point sets.

Universe Q = K-points (Q3 then Q2K, indices 0..nk-1) + non-K points (indices nk..), all with >= 2 vertex neighbours.
For a vertex u and a proper 4-colouring c of G - u, a point set A is *covered* by c if the list-colouring instance
(free colours of each point = colours absent from its surviving vertex neighbours; distinct colours on internal unit
edges) is feasible.  c *fails* on A otherwise; failing is monotone under supersets and a minimal failing set is
connected in the internal unit graph, so for |A| <= 4 it is determined by the minimal failing sets of size <= 4:
empty lists (singletons), equal-singleton unit edges, failing connected triples and connected 4-sets (K-points),
failing non-K unit triangles and diamonds (non-K points are never adjacent to K-points, never have lists of size < 2,
and trees / even cycles with lists of size >= 2 are always colourable).

enumerate_uncovered(u) returns all minimal-ish uncovered sets w.r.t. the current rows: every set A (|A| <= 4)
uncovered by all rows contains one of the returned sets or a declared set (branching over minimal failing sets of
an unsatisfied row; nodes containing a declared set are pruned).
"""
import json, itertools, time, sys
from pathlib import Path
import numpy as np
from paths import HERE, N, K
import tables
SING = np.array([False, True, True, False, True, False, False, False, True, False, False, False, False, False, False, False])  # mask is a singleton


class Universe:
    def __init__(self, path=None):
        """path: cached universe4.json written by build_universe.py; None = rebuild from the sibling data."""
        if path is None and (HERE / 'universe4.json').exists():
            path = HERE / 'universe4.json'
        if path is None:
            import build_universe
            U = build_universe.build()
        else:
            U = json.loads(Path(path).read_text())
        self.n3, self.n2 = U['n_q3'], U['n_q2k']
        self.nk = self.n3 + self.n2
        self.nbrs = U['nbrs']
        maxd = max(len(nb) for nb in self.nbrs)
        self.NB = np.full((self.nk, maxd), N, dtype=np.int64)
        for i, nb in enumerate(self.nbrs):
            self.NB[i, :len(nb)] = nb
        self.q3deg = np.array([len(nb) for nb in self.nbrs[:self.n3]])
        self.kedges = np.array(U['kedges'], dtype=np.int64)
        self.kadj = [set() for _ in range(self.nk)]
        for a, b in U['kedges']:
            self.kadj[a].add(b); self.kadj[b].add(a)
        self.conn3 = np.array(U['conn3'], dtype=np.int64); self.conn4 = np.array(U['conn4'], dtype=np.int64)
        sh3 = np.array(U['shape3'], dtype=np.int64); sh4 = np.array(U['shape4'], dtype=np.int64)
        self.T2, self.S2, _ = tables.build(2); self.T3, self.S3, _ = tables.build(3); self.T4, self.S4, self.P4 = tables.build(4)
        self.sh3i = np.array([self.S3[tuple(s)] for s in sh3.tolist()]); self.sh4i = np.array([self.S4[tuple(s)] for s in sh4.tolist()])
        self.sh3 = sh3; self.sh4 = sh4
        # sub-structure of conn4: shape index of each of the 4 sub-triples, edge bits of the 6 pairs
        self.sub3_shape = []
        P4 = self.P4
        for tri in itertools.combinations(range(4), 3):
            e_idx = [P4.index((tri[i], tri[j])) for i, j in itertools.combinations(range(3), 2)]
            self.sub3_shape.append(np.array([self.S3[tuple(s)] for s in sh4[:, e_idx].tolist()]))
        self.sub3 = list(itertools.combinations(range(4), 3))
        # non-K
        self.nonk_labels = U['nonk_labels']; self.nonk_nbrs = np.array(U['nonk_nbrs'], dtype=np.int64)
        self.nn = len(self.nonk_labels)
        self.nonk_edges = U['nonk_edges']
        self.nadj = {}
        for a, b in self.nonk_edges:
            self.nadj.setdefault(a, set()).add(b); self.nadj.setdefault(b, set()).add(a)
        self.ntri = np.array(U['nonk_triangles'], dtype=np.int64).reshape(-1, 3)
        self.ndia = np.array(U['nonk_diamonds'], dtype=np.int64).reshape(-1, 4)
        # diamond shape: sorted 4-tuple; need edge bits -> compute per diamond
        self.ndia_shape = np.array([self.S4[tuple(int(b in self.nadj.get(a, ())) for a, b in itertools.combinations(d, 2))] for d in self.ndia.tolist()], dtype=np.int64) if len(self.ndia) else np.zeros(0, dtype=np.int64)
        self.ndia_sub = []
        for tri in self.sub3:
            self.ndia_sub.append(np.array([self.S3[tuple(int(d[j] in self.nadj.get(d[i], ())) for i, j in itertools.combinations(tri, 2))] for d in self.ndia.tolist()], dtype=np.int64) if len(self.ndia) else np.zeros(0, dtype=np.int64))
        assert len(U['nonk_k4']) == 0

    def point_nbrs(self, p):
        return self.nbrs[p] if p < self.nk else self.nonk_nbrs[p - self.nk].tolist()

    def adjacent(self, p, q):
        if p < self.nk and q < self.nk:
            return q in self.kadj[p]
        if p >= self.nk and q >= self.nk:
            return (q - self.nk) in self.nadj.get(p - self.nk, ())
        return False

    def masks_for(self, row, u):
        """Free-colour masks (int8) of all K points and all non-K points under colouring row of G - u."""
        col = np.array(list(row) + [-1], dtype=np.int64)
        cc = col[self.NB]
        bits = np.where(cc >= 0, np.left_shift(1, np.maximum(cc, 0)), 0)
        bits[self.NB == u] = 0
        mk = (15 & ~np.bitwise_or.reduce(bits, axis=1)).astype(np.int8)
        cn = col[self.nonk_nbrs]
        bn = np.where(cn >= 0, np.left_shift(1, np.maximum(cn, 0)), 0)
        bn[self.nonk_nbrs == u] = 0
        mn = (15 & ~np.bitwise_or.reduce(bn, axis=1)).astype(np.int8)
        return mk, mn

    def failing_family(self, mk, mn):
        """Minimal failing sets (tuples of global point ids) of one row, grouped by size, plus a per-point index."""
        m = mk.astype(np.int64)
        singles = np.nonzero(m == 0)[0]
        ke = self.kedges
        ma, mb = m[ke[:, 0]], m[ke[:, 1]]
        pf = (ma == mb) & SING[ma]
        pairs = [tuple(e) for e in ke[pf].tolist()]
        c3 = self.conn3
        idx3 = m[c3[:, 0]] | (m[c3[:, 1]] << 4) | (m[c3[:, 2]] << 8)
        f3 = self.T3[self.sh3i, idx3]
        f3 &= ~(m[c3] == 0).any(axis=1)
        for e, (i, j) in enumerate(itertools.combinations(range(3), 2)):
            f3 &= ~((self.sh3[:, e] == 1) & (m[c3[:, i]] == m[c3[:, j]]) & SING[m[c3[:, i]]])
        triples = [tuple(t) for t in c3[f3].tolist()]
        c4 = self.conn4
        idx4 = m[c4[:, 0]] | (m[c4[:, 1]] << 4) | (m[c4[:, 2]] << 8) | (m[c4[:, 3]] << 12)
        f4 = self.T4[self.sh4i, idx4]
        f4 &= ~(m[c4] == 0).any(axis=1)
        for e, (i, j) in enumerate(itertools.combinations(range(4), 2)):
            f4 &= ~((self.sh4[:, e] == 1) & (m[c4[:, i]] == m[c4[:, j]]) & SING[m[c4[:, i]]])
        for tri, shp in zip(self.sub3, self.sub3_shape):
            idx = m[c4[:, tri[0]]] | (m[c4[:, tri[1]]] << 4) | (m[c4[:, tri[2]]] << 8)
            f4 &= ~self.T3[shp, idx]
        quads = [tuple(t) for t in c4[f4].tolist()]
        # non-K triangles and diamonds
        mnn = mn.astype(np.int64)
        t = self.ntri
        idxt = mnn[t[:, 0]] | (mnn[t[:, 1]] << 4) | (mnn[t[:, 2]] << 8)
        ft = self.T3[self.S3[(1, 1, 1)], idxt]
        ntri = [tuple(self.nk + x for x in tr) for tr in t[ft].tolist()]
        d = self.ndia
        if len(d):
            idxd = mnn[d[:, 0]] | (mnn[d[:, 1]] << 4) | (mnn[d[:, 2]] << 8) | (mnn[d[:, 3]] << 12)
            fd = self.T4[self.ndia_shape, idxd]
            for tri, shp in zip(self.sub3, self.ndia_sub):
                idx = mnn[d[:, tri[0]]] | (mnn[d[:, tri[1]]] << 4) | (mnn[d[:, tri[2]]] << 8)
                fd &= ~self.T3[shp, idx]
            ndia = [tuple(self.nk + x for x in dd) for dd in d[fd].tolist()]
        else:
            ndia = []
        fam = {1: [(int(s),) for s in singles.tolist()], 2: pairs, 3: triples + ntri, 4: quads + ndia}
        index = {}
        for k in (2, 3, 4):
            for B in fam[k]:
                for p in B:
                    index.setdefault(p, []).append(B)
        return fam, index


class VertexState:
    """Rows (masks + failing families) and declared sets for one vertex u."""
    def __init__(self, uni, u, rows, declared):
        self.uni, self.u = uni, u
        self.MK, self.MN, self.fams, self.index, self.counts = [], [], [], [], []
        self.declared = set(frozenset(s) for s in declared)
        for r in rows:
            self.add_row(r)

    def add_row(self, row):
        mk, mn = self.uni.masks_for(row, self.u)
        fam, index = self.uni.failing_family(mk, mn)
        self.MK.append(mk); self.MN.append(mn); self.fams.append(fam); self.index.append(index)
        self.counts.append([len(fam[k]) for k in (1, 2, 3, 4)])
        self._stack = None

    def stack(self):
        if getattr(self, '_stack', None) is None:
            self._MK = np.stack(self.MK); self._MN = np.stack(self.MN); self._stack = True
        return self._MK, self._MN

    def masks_of(self, A):
        MK, MN = self.stack()
        cols = [MK[:, p].astype(np.int64) if p < self.uni.nk else MN[:, p - self.uni.nk].astype(np.int64) for p in A]
        return cols

    def fails(self, A):
        """Boolean array over rows: row fails on point set A (tuple, sorted)."""
        uni = self.uni
        cols = self.masks_of(A)
        k = len(A)
        if k == 1:
            return cols[0] == 0
        idx = cols[0]
        for i in range(1, k):
            idx = idx | (cols[i] << (4 * i))
        shape = tuple(int(uni.adjacent(A[i], A[j])) for i, j in itertools.combinations(range(k), 2))
        if k == 2:
            return uni.T2[uni.S2[shape], idx]
        if k == 3:
            return uni.T3[uni.S3[shape], idx]
        return uni.T4[uni.S4[shape], idx]

    def contains_declared(self, A):
        for k in range(1, len(A) + 1):
            for S in itertools.combinations(A, k):
                if frozenset(S) in self.declared:
                    return True
        return False

    def ext(self, c, A, b):
        """Failing sets B of row c with 0 < |B - A| <= b."""
        fam, index = self.fams[c], self.index[c]
        Aset = set(A)
        out = set()
        for k in range(1, b + 1):
            for B in fam[k]:
                out.add(B)
        for a in A:
            for B in index.get(a, ()):
                if 0 < len(set(B) - Aset) <= b:
                    out.add(B)
        return [B for B in out if not set(B) <= Aset]

    def enumerate_uncovered(self, node_limit=None):
        """All minimal-ish uncovered sets (|A| <= 4) not containing a declared set."""
        R = len(self.fams)
        leaves = set()
        stats = {'nodes': 0, 'pruned': 0}
        all_rows = np.arange(R)

        def choose(unsat, A, b):
            best, bc = None, None
            for c in unsat:
                cnt = self.counts[c]
                est = sum(cnt[k - 1] for k in range(1, b + 1))
                if A:
                    est += sum(len(self.index[c].get(a, ())) for a in A)
                if best is None or est < best:
                    best, bc = est, c
            return bc

        def rec(A, unsat):
            stats['nodes'] += 1
            if node_limit and stats['nodes'] > node_limit:
                raise RuntimeError('node limit')
            if self.contains_declared(A):
                stats['pruned'] += 1; return
            if not unsat:
                leaves.add(A); return
            b = 4 - len(A)
            if b == 0:
                return
            if b == 1:
                # last point: intersection over unsatisfied rows of the points that complete a failing set
                cand = None
                for c in unsat:
                    P = set(self.fams[c][1][i][0] for i in range(len(self.fams[c][1])))
                    Aset = set(A)
                    for a in A:
                        for B in self.index[c].get(a, ()):
                            d = set(B) - Aset
                            if len(d) == 1:
                                P.add(next(iter(d)))
                    cand = P if cand is None else (cand & P)
                    if not cand:
                        return
                for p in cand:
                    A2 = tuple(sorted(A + (p,)))
                    stats['nodes'] += 1
                    if not self.contains_declared(A2):
                        leaves.add(A2)
                return
            c = choose(unsat, A, b)
            for B in self.ext(c, A, b):
                A2 = tuple(sorted(set(A) | set(B)))
                f = self.fails(A2)
                unsat2 = [c2 for c2 in unsat if not f[c2]]
                rec(A2, unsat2)

        rec((), list(range(R)))
        return sorted(leaves), stats


def load_libraries():
    import libraries
    return libraries.load_libraries()


if __name__ == '__main__':
    t0 = time.time()
    uni = Universe()
    print('universe', time.time() - t0, flush=True)
    parts, edges, lib, qnb, qq_edges, ntrip = load_libraries()
    print('libraries', time.time() - t0, flush=True)
    from known_declared import load_known_declared
    known, src = load_known_declared()
    for u in [int(a) for a in sys.argv[1:]] or [0]:
        t1 = time.time()
        st = VertexState(uni, u, lib[u], known[u])
        t2 = time.time()
        leaves, stats = st.enumerate_uncovered()
        print(f'u={u}: rows {len(lib[u])}, families {[sum(x) for x in zip(*st.counts)]} ({t2-t1:.1f}s); leaves {len(leaves)} sizes {np.bincount([len(l) for l in leaves]).tolist() if leaves else []} nodes {stats} ({time.time()-t2:.1f}s)', flush=True)
        print('  sample', leaves[:10])
