#!/usr/bin/env python3
"""Blocking-set machinery for the sealed sqrt5 pool of the Parts 509 graph.

G = L u S (Parts's 509 points, L = the 374 sqrt5-free ones).  U = S u Q5 (303 points,
Q5 = the 168 completion points involving sqrt5).  Every unit edge from L to U lands in
the 19-vertex interface I_L (36 such edges: 30 into S, 6 into Q5), so for X subset U

    L u X is 4-colourable
      <=> some proper 4-colouring of U[X] is compatible across the cross edges with a
          proper 4-colouring of L
      <=> for one of the 20 interface classes p of the committed interface lemma
          (origin colour 0, modulo permutations of {1,2,3}) the list instance
          (U[X], list_p) is colourable, where list_p(v) = {0,1,2,3} minus the colours
          p assigns to N(v) n I_L.

Phi(X) := "L u X is not 4-colourable" = AND_p "list instance p on X is infeasible".
One incremental SAT solver per class; X enters only through activation assumptions.
Geometry comes from pool_geometry.json, recomputed exactly by exactgeom.py.
"""
from __future__ import annotations
import json, time
from pathlib import Path
from pysat.solvers import Solver

HERE = Path(__file__).resolve().parent
REPO = Path.home() / 'math_results'
K = 4


class Pool:
    def __init__(self, solver_name='cadical195'):
        gf = HERE / 'pool_geometry.json'
        if not gf.exists():                      # rebuild the exact geometry on demand
            import subprocess, sys as _sys
            subprocess.run([_sys.executable, str(HERE / 'exactgeom.py')], check=True)
        g = json.loads(gf.read_text())
        self.L = list(g['L'])
        self.U = list(g['U'])
        self.Lset, self.Uset = set(self.L), set(self.U)
        self.S = [v for v in self.U if v < 509]
        self.Q5 = [v for v in self.U if v >= 509]
        self.adj = {v: set() for v in self.L + self.U}
        for a, b in g['edges']:
            self.adj[a].add(b); self.adj[b].add(a)
        self.EU = [(a, b) for a, b in g['edges'] if a in self.Uset and b in self.Uset]
        self.cross = [(a, b) if a in self.Lset else (b, a) for a, b in g['edges']
                      if (a in self.Lset) != (b in self.Lset)]
        self.IL = sorted({l for l, u in self.cross})
        iface = json.loads((REPO / 'hadwiger_nelson_parts509_interface_lemma' / 'interface_L.json').read_text())
        assert iface['interface_L'] == self.IL, (iface['interface_L'], self.IL)
        self.witL = [row['witness_colouring_L'] for row in iface['classes']]
        self.patterns = []
        for w in self.witL:
            assert w[0] == '0'
            self.patterns.append({l: int(w[l]) for l in self.IL})
        self.np = len(self.patterns)
        self.idx = {v: i for i, v in enumerate(self.U)}
        m = len(self.U)
        self.m = m
        self.forb = []          # forb[p][v] = set of colours excluded by the pattern
        for pat in self.patterns:
            f = {v: set() for v in self.U}
            for l, u in self.cross:
                f[u].add(pat[l])
            self.forb.append(f)
        self.solvers = []
        base = []
        for v in self.U:
            base.append([-self.act(v)] + [self.var(v, c) for c in range(K)])
        for a, b in self.EU:
            for c in range(K):
                base.append([-self.act(a), -self.act(b), -self.var(a, c), -self.var(b, c)])
        self.base = base
        for p in range(self.np):
            cl = list(base)
            for v in self.U:
                for c in self.forb[p][v]:
                    cl.append([-self.act(v), -self.var(v, c)])
            self.solvers.append(Solver(name=solver_name, bootstrap_with=cl))
        self.calls = 0
        self.time = 0.0
        self.hits = [0] * self.np

    def var(self, v, c):
        return self.idx[v] * K + c + 1

    def act(self, v):
        return self.m * K + self.idx[v] + 1

    def _assume(self, Xset):
        return [self.act(v) if v in Xset else -self.act(v) for v in self.U]

    def sat_p(self, Xset, p, assume=None):
        a = self._assume(Xset) if assume is None else assume
        t = time.time()
        r = self.solvers[p].solve(assumptions=a)
        self.time += time.time() - t; self.calls += 1
        if r:
            self.hits[p] += 1
        return r

    def find_sat_pattern(self, Xset, order=None):
        a = self._assume(Xset)
        if order is None:
            order = sorted(range(self.np), key=lambda p: -self.hits[p])
        for p in order:
            if self.sat_p(Xset, p, assume=a):
                return p
        return None

    def phi(self, Xset):
        """True iff L u X is not 4-colourable."""
        return self.find_sat_pattern(set(Xset)) is None

    def colouring(self, Xset, p):
        """Proper 4-colouring of L u X compatible with class p, or None."""
        if not self.sat_p(set(Xset), p):
            return None
        model = self.solvers[p].get_model()
        col = {}
        for v in Xset:
            for c in range(K):
                if model[self.var(v, c) - 1] > 0:
                    col[v] = c
                    break
        w = self.witL[p]
        for v in self.L:
            col[v] = int(w[v])
        assert self.check(col, Xset)
        return col

    def check(self, col, Xset):
        verts = set(self.L) | set(Xset)
        for v in verts:
            if col.get(v) not in range(K):
                return False
            for w in self.adj[v]:
                if w in verts and col[w] == col[v]:
                    return False
        return True

    def grow(self, col, Xset):
        """Greedily extend a proper colouring of L u X to a maximal pool superset."""
        X = set(Xset); col = dict(col)
        changed = True
        while changed:
            changed = False
            for v in self.U:
                if v in X:
                    continue
                used = {col[w] for w in self.adj[v] if w in X or w in self.Lset}
                for c in range(K):
                    if c not in used:
                        col[v] = c; X.add(v); changed = True
                        break
        return X, col

    def minimal_killing(self, D, p, rng=None, priority=None):
        """Shrink a class-p killing set D (U \\ D is p-colourable) to an inclusion-minimal one."""
        keep = set(D)
        wit = self.colouring(self.Uset - keep, p)
        assert wit is not None
        X2, wit = self.grow(wit, self.Uset - keep)
        keep = self.Uset - X2
        order = sorted(keep)
        if rng:
            rng.shuffle(order)
        if priority is not None:
            order.sort(key=lambda v: -priority.get(v, 0.0))
        for v in order:
            trial = keep - {v}
            c = self.colouring(self.Uset - trial, p)
            if c is not None:
                X2, c = self.grow(c, self.Uset - trial)
                keep = self.Uset - X2
                wit = c
        return sorted(keep), wit
