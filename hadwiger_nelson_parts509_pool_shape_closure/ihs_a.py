#!/usr/bin/env python3
"""Pool-restricted delete-(a+1)-add-a closure by decision-form implicit hitting sets.

Reduction.  A blocking X subset U (i.e. L u X not 4-colourable) with |X| <= 134 exists
iff one exists of the special shape

    X = (S \\ R) u A,   R subset S, |R| = a + 1,   A subset Q5, |A| = a,

for some a >= 0: a blocking X with |X n S| = 135 - d and |X n Q5| = a satisfies
d >= a + 1 because |X| <= 134, and putting back d - a - 1 deleted vertices of S keeps the
graph blocking (a supergraph of a non-4-colourable graph is non-4-colourable).

a = 0 is excluded by the vertex-criticality of Parts's graph, a = 1, 2, 3 by the committed
delete-2-add-1, delete-3-add-2 and delete-4-add-3 closures.  This program decides the
remaining values one at a time.

Master: variables r_v (v in S, "deleted") and q_w (w in Q5, "added"), sum r = a+1,
sum q = a, and for every certified killing set D the clause

    OR_{v in D n S} (not r_v)   OR   OR_{w in D n Q5} q_w                        (*)

(valid because X must meet D).  A model gives a candidate (R, A); the 20-class oracle
either certifies it blocking -- a 508-vertex 5-chromatic unit-distance graph, i.e. a new
record -- or returns fresh killing sets, which are added as clauses.  Master UNSAT closes
the value a.
"""
from __future__ import annotations
import argparse, json, random, sys, time
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from pool5 import Pool
from pysat.formula import IDPool
from pysat.card import CardEnc, EncType
from pysat.solvers import Solver

ap = argparse.ArgumentParser()
ap.add_argument('--a', type=int, required=True)
ap.add_argument('--out', default=None)
ap.add_argument('--seed', type=int, default=1)
ap.add_argument('--family', default=str(HERE / 'family_min.json'))
ap.add_argument('--extra', nargs='*', default=[])
ap.add_argument('--time-limit', type=float, default=1e9)
ap.add_argument('--rounds', type=int, default=10 ** 9)
ap.add_argument('--useful-cut', action='store_true',
                help='every added point needs 4 neighbours in L u X (valid once a-1 is closed)')
ap.add_argument('--solver', default='cadical195')
args = ap.parse_args()
a = args.a
out = Path(args.out or (HERE / f'ihs_a{a}')); out.mkdir(exist_ok=True)


def log(m):
    print(f"[{time.strftime('%H:%M:%S')}] {m}", flush=True)


rng = random.Random(args.seed)
P = Pool()
S, Q5, U = P.S, P.Q5, P.U
Uset = set(U); Sset = set(S); Qset = set(Q5)
Lset = set(P.L)
rid = {v: i + 1 for i, v in enumerate(S)}                    # r_v
qid = {w: len(S) + i + 1 for i, w in enumerate(Q5)}          # q_w
ids = IDPool(start_from=len(S) + len(Q5) + 1)

fam = [frozenset(d) for d in json.loads(Path(args.family).read_text())['sets']]
for path in args.extra:
    if Path(path).exists():
        for line in open(path):
            if line.strip():
                fam.append(frozenset(json.loads(line)['D']))
fam = list(set(fam))
seen = set(fam)

master = Solver(name=args.solver)


def clause_for(D):
    return [-rid[v] for v in D if v in Sset] + [qid[w] for w in D if w in Qset]


for D in seen:
    master.add_clause(clause_for(D))
for cl in CardEnc.equals(lits=[rid[v] for v in S], bound=a + 1, vpool=ids,
                         encoding=EncType.totalizer).clauses:
    master.add_clause(cl)
for cl in CardEnc.equals(lits=[qid[w] for w in Q5], bound=a, vpool=ids,
                         encoding=EncType.totalizer).clauses:
    master.add_clause(cl)
if args.useful_cut and a >= 1:
    # deg_{L u X}(w) >= 4 for every added w:  degLS(w) - |N(w) n R| + |N(w) n A| >= 4
    nc = 0
    for w in Q5:
        nLS = len(P.adj[w] & (Lset | Sset))
        nbS = sorted(P.adj[w] & Sset)
        nbQ = sorted(P.adj[w] & Qset)
        # encode  sum_{v in nbS} r_v - sum_{w' in nbQ} q_{w'} <= nLS - 4   (given q_w)
        lits = [rid[v] for v in nbS] + [-qid[x] for x in nbQ]
        bound = nLS - 4 + len(nbQ)
        if bound >= len(lits):
            continue
        if bound < 0:
            master.add_clause([-qid[w]]); nc += 1; continue
        for cl in CardEnc.atmost(lits=lits, bound=bound, vpool=ids,
                                 encoding=EncType.totalizer).clauses:
            master.add_clause(cl + [-qid[w]])
        nc += 1
    log(f'useful-point cuts for {nc} candidate points')
log(f'a={a}: |R|={a+1} deletions, |A|={a} additions; seed family {len(seen)} killing sets')

hfile = out / 'new_killing_sets.jsonl'
t0 = time.time(); rounds = 0; new_total = 0; last_log = time.time()
res = 'timeout'
while rounds < args.rounds and time.time() - t0 < args.time_limit:
    rounds += 1
    t = time.time()
    sat = master.solve()
    tm = time.time() - t
    if not sat:
        res = 'unsat'
        log(f'MASTER UNSAT: no blocking (S\\R) u A with |R|={a+1}, |A|={a}. '
            f'{rounds} rounds, {len(seen)} killing sets, {time.time()-t0:.0f}s')
        break
    model = master.get_model()
    R = {v for v in S if model[rid[v] - 1] > 0}
    A = {w for w in Q5 if model[qid[w] - 1] > 0}
    X = (Sset - R) | A
    Y = set(X)
    found = 0
    p = P.find_sat_pattern(Y)
    if p is None:
        res = 'record'
        log(f'*** BLOCKING: |X|={len(X)} = 134, R={sorted(R)}, A={sorted(A)} ***')
        (out / 'record.json').write_text(json.dumps({'X': sorted(X), 'R': sorted(R), 'A': sorted(A)}))
        break
    while p is not None:
        D, wit = P.minimal_killing(Uset - Y, p, rng)
        Dk = frozenset(D)
        if Dk not in seen:
            seen.add(Dk)
            master.add_clause(clause_for(Dk))
            verts = sorted(Lset | (Uset - Dk))
            with hfile.open('a') as f:
                f.write(json.dumps({'D': sorted(Dk), 'pattern': p,
                                    'witness': ''.join(str(wit[v]) for v in verts)}) + '\n')
            found += 1; new_total += 1
        Y |= set(D)
        p = P.find_sat_pattern(Y)
    if rounds % 10 == 0 or time.time() - last_log > 180:
        last_log = time.time()
        log(f'round {rounds}: +{found} sets (total {len(seen)}), grown {len(Y)}; '
            f'master {tm:.1f}s oracle {P.time:.0f}s elapsed {time.time()-t0:.0f}s')
(out / 'result.json').write_text(json.dumps(
    {'a': a, 'result': res, 'rounds': rounds, 'sets': len(seen), 'new': new_total,
     'elapsed': time.time() - t0}))
log(f'result={res} rounds={rounds} sets={len(seen)} new={new_total}')
