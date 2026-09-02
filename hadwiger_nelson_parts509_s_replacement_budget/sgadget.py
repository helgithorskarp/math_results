#!/usr/bin/env python3
"""S-side search machinery for the Parts-509 composition G = L ∪ S.

Universe U = pool_S.json['W_S'] (the 135 vertices of S plus the 168 completion
points whose coordinates involve sqrt5).  Every ambient edge between L and U has
its L-endpoint in the 19-vertex interface I_L, and interface_L.json lists the 20
colour classes (origin colour 0, modulo permutations of {1,2,3}) of proper
4-colourings of L restricted to I_L, each with a full witness colouring of L.

For X ⊆ U:  L ∪ X is 4-colourable  ⟺  some proper 4-colouring of X is
compatible (across the cross edges) with one of the 120 interface colourings of
L  ⟺  (permuting colours 1,2,3 of X) some proper 4-colouring of X is compatible
with one of the 20 class representatives.  So

    Φ(X) := 'L ∪ X is not 4-colourable'  =  AND over the 20 patterns p of
            Φ_p(X) := 'no proper 4-colouring of X is compatible with p'.

Each Φ_p is one SAT call with unit constraints on the cross-edge endpoints.
`colouring_p` returns a full proper 4-colouring of L ∪ X (pattern p's witness
on L, model on X) and checks it exactly against the ambient edge list.
"""
from __future__ import annotations
import json, random, time
from pathlib import Path
from pysat.solvers import Solver

HERE = Path(__file__).resolve().parent
PAIR = HERE.parent / 'hadwiger_nelson_parts509_pair_closure'
IFACE = HERE.parent / 'hadwiger_nelson_parts509_interface_lemma'
K = 4


class SGadget:
    def __init__(self, solver_name='cadical195', level=1):
        assert level == 1, 'only the level-1 pool is published here'
        amb = json.loads((PAIR / 'ambient_w3_edges.json').read_text())
        pool = json.loads((HERE / 'pool_S.json').read_text())
        self.U = sorted(pool['W_S'])
        self.Q5 = sorted(pool['Q5'])
        self.level = level
        self.n_amb = amb['vertices']
        self.adj = [set() for _ in range(self.n_amb)]
        for a, b in amb['edges']:
            self.adj[a].add(b); self.adj[b].add(a)
        self.L = list(range(374))
        Lset = set(self.L)
        self.S135 = list(range(374, 509))
        self.Uset = set(self.U)
        iface_repo = json.loads((IFACE / 'interface_L.json').read_text())
        iface = {'interface': iface_repo['interface_L'], 'witness_colourings': [row['witness_colouring_L'] for row in iface_repo['classes']]}
        self.IL = iface['interface']
        ILset = set(self.IL)
        self.cross = []
        for u in self.U:
            for l in self.adj[u] & Lset:
                assert l in ILset, (u, l)
                self.cross.append((l, u))
        self.witL = iface['witness_colourings']
        # pattern p = interface colouring of witness p (origin colour 0)
        self.patterns = []
        for w in self.witL:
            assert w[0] == '0'
            self.patterns.append({l: int(w[l]) for l in self.IL})
        self.np = len(self.patterns)
        m = len(self.U)
        self.idx = {v: i for i, v in enumerate(self.U)}
        self.var = lambda v, c: self.idx[v] * K + c + 1
        self.act = lambda v: m * K + self.idx[v] + 1
        self.zsel = lambda p: m * K + m + p + 1
        clauses = []
        for v in self.U:
            clauses.append([-self.act(v)] + [self.var(v, c) for c in range(K)])
        for v in self.U:
            for w in self.adj[v]:
                if w in self.Uset and w > v:
                    for c in range(K):
                        clauses.append([-self.act(v), -self.act(w), -self.var(v, c), -self.var(w, c)])
        for p, pat in enumerate(self.patterns):
            for l, u in self.cross:
                clauses.append([-self.zsel(p), -self.act(u), -self.var(u, pat[l])])
        self.nvars = m * K + m + self.np
        self.clauses = clauses
        self.solver = Solver(name=solver_name, bootstrap_with=clauses)
        self.calls = 0
        self.time = 0.0
        self.sat_hits = [0] * self.np

    def _assume(self, X, p):
        Xs = set(X)
        assert Xs <= self.Uset, 'X must lie inside the pool U'
        a = [self.act(v) if v in Xs else -self.act(v) for v in self.U]
        a += [self.zsel(q) if q == p else -self.zsel(q) for q in range(self.np)]
        return a

    def sat_p(self, X, p):
        """True iff X has a proper 4-colouring compatible with pattern p."""
        t = time.time()
        r = self.solver.solve(assumptions=self._assume(X, p))
        self.time += time.time() - t; self.calls += 1
        if r:
            self.sat_hits[p] += 1
        return r

    def find_sat_pattern(self, X, rng=None):
        """Return a pattern index p with sat_p(X, p), or None if Φ(X) holds.
        With an rng the patterns are tried in random order (diversifies killing sets)."""
        if rng is not None:
            order = list(range(self.np)); rng.shuffle(order)
        else:
            order = sorted(range(self.np), key=lambda p: -self.sat_hits[p])
        for p in order:
            if self.sat_p(X, p):
                return p
        return None

    def phi(self, X):
        return self.find_sat_pattern(X) is None

    def colouring_p(self, X, p):
        """Full proper 4-colouring of L ∪ X compatible with pattern p, or None."""
        if not self.sat_p(X, p):
            return None
        model = self.solver.get_model()
        col = {}
        for v in X:
            for c in range(K):
                if model[self.var(v, c) - 1] > 0:
                    col[v] = c; break
        w = self.witL[p]
        for v in self.L:
            col[v] = int(w[v])
        assert self.check(col, X), 'witness colouring failed the exact edge check'
        return col

    def check(self, col, X):
        """Solver-free check that col is a proper 4-colouring of L ∪ X (ambient edges)."""
        verts = set(self.L) | set(X)
        for v in verts:
            if col.get(v) not in range(K):
                return False
            for w in self.adj[v]:
                if w in verts and col[w] == col[v]:
                    return False
        return True

    def grow(self, col, X):
        """Greedily extend a colouring of L ∪ X to more pool vertices; returns (X', col')."""
        X = set(X); col = dict(col)
        changed = True
        while changed:
            changed = False
            for v in self.U:
                if v in X:
                    continue
                used = {col[w] for w in self.adj[v] if (w in X or w < 374)}
                for c in range(K):
                    if c not in used:
                        col[v] = c; X.add(v); changed = True
                        break
        return X, col

    def minimal_killing(self, D, p, rng=None, grow=True, priority=None):
        """Shrink a pattern-p killing set D (U\D has a p-compatible colouring) to a
        minimal one.  Returns (sorted D', witness colouring of L ∪ (U\D')).
        `priority` (dict vertex -> weight): vertices of high weight are tried first for
        removal from D, so D concentrates on low-weight vertices."""
        keep = set(D)
        wit = self.colouring_p(sorted(self.Uset - keep), p)
        assert wit is not None
        if grow:
            X2, wit = self.grow(wit, self.Uset - keep)
            keep = self.Uset - X2
        order = sorted(keep)
        if rng:
            rng.shuffle(order)
        if priority is not None:
            order.sort(key=lambda v: -priority.get(v, 0.0))
        for v in order:
            trial = keep - {v}
            c = self.colouring_p(sorted(self.Uset - trial), p)
            if c is not None:
                keep = trial; wit = c
                if grow:
                    X2, wit = self.grow(wit, self.Uset - keep)
                    keep = self.Uset - X2
        return sorted(keep), wit
