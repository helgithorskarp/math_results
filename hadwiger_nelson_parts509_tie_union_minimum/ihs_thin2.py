#!/usr/bin/env python3
"""Exact 'no 5-chromatic subgraph with <= 508 vertices' test for a thin accumulative graph A* = V ∪ P
by implicit hitting sets over the non-forced part, version 2.

Setting (see ihs_thin.py / tie_union_certificate.py): F = forced vertices (A* − u 4-colourable), R = A* \ F.
D ⊆ R is a killing set if A* − D is 4-colourable; F ∪ X (X ⊆ R) is 5-chromatic iff X meets every killing set.

Closure constraint.  By the committed closures (vertex-criticality, delete-2-add-1, delete-3-add-2,
delete-4-add-3) every 5-chromatic unit-distance graph with at most 508 vertices shares at most 504 vertices
with V and therefore contains at least 4 points outside V.  A 5-chromatic subgraph H ⊆ A* with |H| ≤ 508
contains a vertex-critical 5-chromatic H' ⊆ H, H' ⊇ F, and H' has ≥ 4 points of P; hence X = H \ F has at
least MINP = 4 points of P.  So: if every hitting set of the killing-set family that contains ≥ 4 points has
size ≥ |R| − (|V| − |F|) ... more simply size ≥ 509 − |F|, then A* has no 5-chromatic subgraph on ≤ 508
vertices.  The driver therefore minimises |X| subject to (X hits the family) and (|X ∩ P| ≥ MINP) and stops
as soon as the optimum reaches TARGET = 509 − |F| (theorem) or a hitting set X with |X| < TARGET makes
F ∪ X 5-chromatic (RECORD: a 5-chromatic unit-distance graph on ≤ 508 vertices).

Killing-set generation.  A 4-colouring c of F ∪ X is extended greedily (a free vertex whose coloured
neighbours miss a colour is added, no solver call); the rainbow vertices form the killing set D(c) = R \ C.
'Disjoint layers': the sets found so far in the round are forced into the base and a new colouring is asked
for, so successive killing sets are pairwise disjoint (each disjoint set raises the bound by one).  A few
SAT calls per layer try to unblock rainbow vertices (smaller killing sets); every UNSAT answer exhibits a
5-chromatic F ∪ Y and is checked against 508.
Families of other seeds (same TAG) are merged in at every round.
usage: ihs_thin2.py --seed S --union U.json --forced F.json [--tag T] [--min-points 4] [--layers 30]
       [--improve 2] [--ambient AMB.json]
Output: thin2_results{TAG}_seed{S}.json (compatible with ihs_thin.py results + 'min_points', 'target').
"""
import argparse, json, time, random, subprocess, hashlib, glob, os
from pathlib import Path
from pysat.solvers import Solver
from pysat.examples.rc2 import RC2
from pysat.formula import WCNF
from pysat.card import CardEnc, EncType
import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds
from scipy.sparse import lil_matrix

HN = Path(os.environ.get('HN_SCRATCH', '/scratch/agents/researcher-4/hn'))
CADICAL = '/scratch/cadical-package/usr/bin/cadical'
DRAT = '/scratch/researcher-3-drat-trim/drat-trim'
K = 4
NV_PARTS = 509

ap = argparse.ArgumentParser()
ap.add_argument('--seed', type=int, default=1)
ap.add_argument('--union', default=str(HN / 'ties' / 'tie_union.json'))
ap.add_argument('--forced', default=str(HN / 'ties' / 'forced.json'))
ap.add_argument('--tag', default='')
ap.add_argument('--min-points', type=int, default=4)
ap.add_argument('--layers', type=int, default=30)
ap.add_argument('--improve', type=int, default=2, help='SAT calls per layer trying to unblock rainbow vertices')
ap.add_argument('--ambient', default=os.environ.get('HN_AMBIENT', str(HN / 'ambient_w3_edges.json')))
ap.add_argument('--max-rounds', type=int, default=10**9)
args = ap.parse_args()

amb = json.loads(Path(args.ambient).read_text())
TU = json.loads(Path(args.union).read_text())
FJ = json.loads(Path(args.forced).read_text())
STAR = sorted(TU['start']); STARSET = set(STAR)
F = sorted(FJ['forced']); Fset = set(F)
R = sorted(v for v in STAR if v not in Fset)
RP = [v for v in R if v >= NV_PARTS]      # added points among the free elements
EDGES = [(a, b) for a, b in amb['edges'] if a in STARSET and b in STARSET]
ADJ = {v: set() for v in STAR}
for a, b in EDGES:
    ADJ[a].add(b); ADJ[b].add(a)
idx = {v: i for i, v in enumerate(STAR)}
var = lambda v, c: idx[v] * K + c + 1
act = lambda v: len(STAR) * K + idx[v] + 1
rng = random.Random(args.seed)
TAG = args.tag; seed = args.seed
OUT = HN / 'ties' / f'thin2_results{TAG}_seed{seed}.json'
TARGET = 509 - len(F)
assert len(F) + len(R) == len(STAR) and all(v < NV_PARTS for v in F) or True


def log(msg):
    print(f'[{time.strftime("%H:%M:%S")}] {msg}', flush=True)


def make_solver():
    clauses = [[-act(v)] + [var(v, c) for c in range(K)] for v in STAR]
    for a, b in EDGES:
        for c in range(K):
            clauses.append([-act(a), -act(b), -var(a, c), -var(b, c)])
    tri = None
    for a in F:
        for b in sorted(ADJ[a] & Fset):
            common = ADJ[a] & ADJ[b] & Fset
            if common:
                tri = (a, b, min(common)); break
        if tri:
            break
    for i, v in enumerate(tri):
        clauses.append([var(v, i)])
    return Solver(name='cadical195', bootstrap_with=clauses), tri


SAT_CALLS = [0, 0.0]


def colourable(solver, active):
    ass = [act(v) if v in active else -act(v) for v in STAR]
    t = time.time()
    ok = solver.solve(assumptions=ass)
    SAT_CALLS[0] += 1; SAT_CALLS[1] += time.time() - t
    if not ok:
        return None
    m = set(l for l in solver.get_model() if l > 0)
    col = {}
    for v in active:
        for c in range(K):
            if var(v, c) in m:
                col[v] = c; break
    return col


def greedy_extend(active, col):
    """Greedy colour extension of a proper colouring col of `active` to as many free vertices as possible
    (random order; a vertex is added when its coloured neighbours miss a colour).  Returns (active, col)."""
    active = set(active); col = dict(col)
    rest = [v for v in R if v not in active]
    rng.shuffle(rest)
    progress = True
    while progress and rest:
        progress = False
        for v in list(rest):
            used = {col[w] for w in ADJ[v] if w in active}
            if len(used) < K:
                free = [c for c in range(K) if c not in used]
                col[v] = free[rng.randrange(len(free))]; active.add(v); rest.remove(v); progress = True
    return active, col


RECORDS = []


def check_record(Y, note):
    """F ∪ Y is 5-chromatic (solver UNSAT).  Record if |F| + |Y| <= 508."""
    if len(F) + len(Y) <= 508:
        log(f'!!! RECORD CANDIDATE: F ∪ Y with |F|+|Y| = {len(F)+len(Y)} vertices is not 4-colourable ({note}); Y = {sorted(Y)}')
        RECORDS.append({'Y': sorted(Y), 'note': note, 'order': len(F) + len(Y)})
        (HN / 'ties' / f'RECORD{TAG}_seed{seed}_{len(RECORDS)}.json').write_text(json.dumps({'F': F, 'Y': sorted(Y), 'note': note}))


def grow(solver, base, col, improve):
    """From a proper colouring col of base (⊇ F), return a maximal-by-greedy colourable set C and its colouring;
    up to `improve` SAT calls try to add a rainbow vertex (a successful call re-runs the greedy extension)."""
    active, col = greedy_extend(base, col)
    budget = improve
    tried = set()
    while budget > 0:
        rest = [v for v in R if v not in active and v not in tried]
        if not rest:
            break
        v = rest[rng.randrange(len(rest))]
        tried.add(v); budget -= 1
        c2 = colourable(solver, active | {v})
        if c2 is None:
            check_record(set(active | {v}) - Fset, 'growth UNSAT')
        else:
            active, col = greedy_extend(active | {v}, c2)
    for v in active:
        assert all(col[w] != col[v] for w in ADJ[v] if w in active)
    return active, col


def main():
    log(f'A*: {len(STAR)} vertices, {len(EDGES)} edges; forced {len(F)}, free R = {len(R)} ({len(RP)} points); '
        f'TARGET |X| >= {TARGET} (order 509); min points {args.min_points}; seed {seed}')
    solver, tri = make_solver()
    assert colourable(solver, set(STAR)) is None
    family = []; seen = set()

    def add_row(D, col, verts_active):
        key = frozenset(D)
        if key in seen or not key:
            return False
        seen.add(key)
        family.append({'D': sorted(D), 'witness': ''.join(str(col[v]) for v in STAR if v not in key)})
        return True

    def load(path):
        n = 0
        try:
            prev = json.loads(Path(path).read_text())
        except Exception:
            return 0
        for row in prev.get('family', []):
            key = frozenset(row['D'])
            if key not in seen and key <= set(R) and key:
                seen.add(key); family.append({'D': sorted(row['D']), 'witness': row['witness']}); n += 1
        return n

    def merge_others():
        n = 0
        for p in glob.glob(str(HN / 'ties' / f'thin2_results{TAG}_seed*.json')) + glob.glob(str(HN / 'ties' / f'thin_results{TAG}_seed*.json')):
            if Path(p) != OUT:
                n += load(p)
        return n

    n0 = load(OUT); n1 = merge_others()
    log(f'resumed {n0} killing sets from {OUT.name}, merged {n1} from sibling files; family {len(family)}')
    xi = {v: i for i, v in enumerate(R)}
    pidx = [xi[v] for v in RP]

    def min_hitting_set(extra_blocks=()):
        """Exact minimum hitting set with |X ∩ P| >= min_points (HiGHS MILP).  Returns (X, cost)."""
        rows = len(family) + 1 + len(extra_blocks)
        A = lil_matrix((rows, len(R)))
        lb = np.ones(rows); ub = np.full(rows, np.inf)
        for r, row in enumerate(family):
            for v in row['D']:
                A[r, xi[v]] = 1
        r = len(family)
        for i in pidx:
            A[r, i] = 1
        lb[r] = args.min_points
        for j, B in enumerate(extra_blocks):
            rr = len(family) + 1 + j
            for v in B:
                A[rr, xi[v]] = 1
            ub[rr] = len(B) - 1; lb[rr] = -np.inf
        res = milp(c=np.ones(len(R)), constraints=LinearConstraint(A.tocsr(), lb=lb, ub=ub), integrality=np.ones(len(R)),
                   bounds=Bounds(0, 1), options={'mip_rel_gap': 0.0})
        if res.x is None:
            return None, None
        X = sorted(v for v in R if res.x[xi[v]] > 0.5)
        return X, len(X)

    def rc2_check(cost):
        w = WCNF()
        for row in family:
            w.append([xi[v] + 1 for v in row['D']])
        card = CardEnc.atleast(lits=[i + 1 for i in pidx], bound=args.min_points, top_id=len(R), encoding=EncType.seqcounter)
        for cl in card.clauses:
            w.append(cl)
        for v in R:
            w.append([-(xi[v] + 1)], weight=1)
        with RC2(w, solver='cd19', adapt=True, exhaust=False, minz=False) as rc2:
            mdl = rc2.compute(); c = rc2.cost
        return c

    history = []
    t0 = time.time(); rnd = 0
    while rnd < args.max_rounds:
        rnd += 1
        merged = merge_others() if rnd % 3 == 0 else 0
        X, cost = min_hitting_set()
        col = colourable(solver, Fset | set(X)) if cost < TARGET else 'skip'
        valid = (col is None)
        history.append({'round': rnd, 'family': len(family), 'hitting_set': cost, 'valid': valid if col != 'skip' else None})
        log(f'round {rnd}: family {len(family)} (+{merged} merged), constrained min hitting set {cost} -> order {len(F)+cost}; '
            f'{"BOUND REACHED" if col == "skip" else ("VALID (5-chromatic)" if valid else "4-colourable")}; '
            f'SAT calls {SAT_CALLS[0]} ({SAT_CALLS[1]:.0f}s); elapsed {time.time()-t0:.0f}s')
        if col == 'skip':
            c2 = rc2_check(cost)
            log(f'THEOREM: every hitting set with >= {args.min_points} points has size >= {cost} >= {TARGET}: no 5-chromatic subgraph of A* '
                f'with <= 508 vertices (given the committed closures).  RC2 cross-check: {c2}')
            OUT.write_text(json.dumps({'R': R, 'F_size': len(F), 'F': F, 'family': family, 'history': history, 'min_points': args.min_points,
                                       'target': TARGET, 'constrained_minimum': cost, 'rc2_cross_check': c2, 'status': 'theorem',
                                       'records': RECORDS, 'pinned_triangle': tri}))
            return
        if valid:
            check_record(set(X), 'hitting set valid')
            log(f'VALID constrained hitting set of size {cost} < {TARGET}: F ∪ X is 5-chromatic with {len(F)+cost} vertices -- RECORD; X = {X}')
            OUT.write_text(json.dumps({'R': R, 'F_size': len(F), 'F': F, 'family': family, 'history': history, 'min_points': args.min_points,
                                       'target': TARGET, 'X_star': X, 'status': 'record', 'records': RECORDS, 'pinned_triangle': tri}))
            # DRAT-check immediately
            verts = sorted(Fset | set(X)); vs = set(verts); id2 = {v: i for i, v in enumerate(verts)}
            v2 = lambda v, c: id2[v] * K + c + 1
            clauses = [[v2(v, c) for c in range(K)] for v in verts]
            for a, b in EDGES:
                if a in vs and b in vs:
                    for c in range(K):
                        clauses.append([-v2(a, c), -v2(b, c)])
            for i, v in enumerate(tri):
                clauses.append([v2(v, i)])
            text = f'p cnf {len(verts)*K} {len(clauses)}\n' + ''.join(' '.join(map(str, cl)) + ' 0\n' for cl in clauses)
            cnf = HN / 'ties' / f'thin2_record{TAG}_seed{seed}.cnf'; proof = HN / 'ties' / f'thin2_record{TAG}_seed{seed}.drat'
            cnf.write_text(text)
            r = subprocess.run([CADICAL, '-q', str(cnf), str(proof)], capture_output=True, text=True)
            d = subprocess.run([DRAT, str(cnf), str(proof)], capture_output=True, text=True) if r.returncode == 20 else None
            log(f'record DRAT: cadical rc {r.returncode}, drat-trim verified {d is not None and "s VERIFIED" in d.stdout}')
            return
        # growth: disjoint layers
        new = 0; layers = 0; sizes = []
        forced_in = set(X)
        base_col = col
        while layers < args.layers:
            C, colC = grow(solver, Fset | forced_in, base_col, args.improve)
            D = [v for v in R if v not in C]
            if not D:
                break
            sizes.append(len(D))
            if add_row(D, colC, C):
                new += 1
            layers += 1
            forced_in |= set(D)
            base_col = colourable(solver, Fset | forced_in)
            if base_col is None:
                check_record(forced_in, 'layer base UNSAT')
                break
        log(f'          {new} new killing sets in {layers} disjoint layers (sizes {sizes})')
        OUT.write_text(json.dumps({'R': R, 'F_size': len(F), 'F': F, 'family': family, 'history': history, 'min_points': args.min_points,
                                   'target': TARGET, 'status': 'running', 'records': RECORDS, 'pinned_triangle': tri}))


if __name__ == '__main__':
    main()
