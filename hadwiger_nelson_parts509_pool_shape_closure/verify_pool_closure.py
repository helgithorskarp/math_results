#!/usr/bin/env python3
"""Verifier for the pool-restricted delete-(a+1)-add-a closures of the Parts 509 graph.

Checks, from scratch and without trusting the search:

 1. Geometry.  Re-parses Parts's 509 exact points and the 1,158 completion points of the
    committed swap closure, recomputes *every* unit pair inside L u U exactly in
    Q(sqrt3, sqrt5, sqrt11) (228,826 pairs, integer arithmetic), and checks that the pool
    is sealed: every unit edge from L to U ends in the 19-vertex interface I_L.
 2. Killing sets.  Replays the stored colouring of every killing set D against that edge
    list: class-p witness colouring of L (from the committed interface lemma) together
    with the stored colours on U \\ D must be a proper 4-colouring of L u (U \\ D).  This
    is solver-free and certifies that any blocking X (L u X not 4-colourable) meets D.
 3. Closures.  For each closed a, rebuilds the DIMACS instance
        clauses of the listed killing sets  +  |R| = a+1  +  |A| = a
    with the self-contained Sinz encoder of cardenc.py, checks its SHA-256 against the
    certificate, and shows it is unsatisfiable -- with a SAT solver by default, or by
    checking a supplied DRAT proof with drat-trim (--drat DIR --drat-trim BIN).

Usage:
    python3 verify_pool_closure.py                       # geometry + witnesses + SAT
    python3 verify_pool_closure.py --drat proofs --drat-trim /path/to/drat-trim
"""
from __future__ import annotations
import argparse, hashlib, json, subprocess, sys, time
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import cardenc
import exactgeom

ap = argparse.ArgumentParser()
ap.add_argument('--repo', default=str(HERE.parent), help='root of the math_results checkout')
ap.add_argument('--drat', default=None, help='directory holding master_a<a>.drat proofs')
ap.add_argument('--drat-trim', default='drat-trim')
ap.add_argument('--skip-sat', action='store_true')
args = ap.parse_args()
REPO = Path(args.repo)
ok_all = True


def say(m):
    print(m, flush=True)


t0 = time.time()
say('(1) exact geometry')
pts, cp = exactgeom.build(REPO)
D, ipts = exactgeom.scale_points(pts)
pool = json.loads((REPO / 'hadwiger_nelson_parts509_s_replacement_budget' / 'pool_S.json').read_text())
U = sorted(pool['W_S'])
L = list(range(374))
E = exactgeom.unit_pairs(ipts, D, L + U)
adj = {v: set() for v in L + U}
for a, b in E:
    adj[a].add(b); adj[b].add(a)
Lset, Uset = set(L), set(U)
cross = [(a, b) if a in Lset else (b, a) for a, b in E if (a in Lset) != (b in Lset)]
IL = sorted({l for l, u in cross})
iface = json.loads((REPO / 'hadwiger_nelson_parts509_interface_lemma' / 'interface_L.json').read_text())
witL = [row['witness_colouring_L'] for row in iface['classes']]
say(f'    {len(pts)} exact points, denominator {D}; |E(L u U)| = {len(E)}; '
    f'|E(L)| = {sum(1 for a,b in E if a in Lset and b in Lset)}, '
    f'|E(U)| = {sum(1 for a,b in E if a in Uset and b in Uset)}, cross = {len(cross)}')
say(f'    sealed: interface {IL == iface["interface_L"]} ({len(IL)} vertices); '
    f'|S| = {sum(1 for v in U if v < 509)}, |Q5| = {sum(1 for v in U if v >= 509)}')
ok_all &= (IL == iface['interface_L'])
# the class witnesses must be proper 4-colourings of L
for p, w in enumerate(witL):
    for a, b in E:
        if a in Lset and b in Lset and w[a] == w[b]:
            say(f'    FAIL: class {p} witness is not proper on L'); ok_all = False
say(f'    {len(witL)} interface-class witness colourings of L are proper')

say('(2) killing sets')
ks = json.loads((HERE / 'killing_sets.json').read_text())
assert ks['U'] == U, 'pool mismatch'
bad = 0
for row in ks['sets']:
    Dset = set(row['D'])
    col = {v: int(witL[row['p']][v]) for v in L}
    c = row['c']
    for i, v in enumerate(U):
        if v in Dset:
            if c[i] != '.':
                bad += 1; break
        else:
            col[v] = int(c[i])
    verts = Lset | (Uset - Dset)
    if set(col) != verts:
        bad += 1; continue
    for a, b in E:
        if a in verts and b in verts and col[a] == col[b]:
            bad += 1; break
say(f'    {len(ks["sets"])} killing sets replayed exactly, {bad} failures '
    f'({time.time()-t0:.0f}s)')
ok_all &= (bad == 0)

say('(3) closures')
cl = json.loads((HERE / 'closures.json').read_text())
S = cl['S']; Q5 = cl['Q5']
rid = {v: i + 1 for i, v in enumerate(S)}
qid = {w: len(S) + i + 1 for i, w in enumerate(Q5)}
Sset, Qset = set(S), set(Q5)
closed = []
for a in sorted(cl['closures'], key=int):
    info = cl['closures'][a]
    a_i = int(a)
    nv = len(S) + len(Q5)
    clauses = []
    for i in info['sets']:
        Dl = ks['sets'][i]['D']
        clauses.append([-rid[v] for v in Dl if v in Sset] + [qid[w] for w in Dl if w in Qset])
    c1, nv = cardenc.equals_tot([rid[v] for v in S], a_i + 1, nv); clauses += c1
    c2, nv = cardenc.equals_tot([qid[w] for w in Q5], a_i, nv); clauses += c2
    txt = f'p cnf {nv} {len(clauses)}\n' + ''.join(' '.join(map(str, c)) + ' 0\n' for c in clauses)
    h = hashlib.sha256(txt.encode()).hexdigest()
    match = (h == info['cnf_sha256'])
    verdict = 'hash-ok' if match else 'HASH MISMATCH'
    ok_all &= match
    if args.drat:
        cnfp = Path(args.drat) / f'master_a{a}.cnf'
        cnfp.write_text(txt)
        pr = Path(args.drat) / f'master_a{a}.drat'
        r = subprocess.run([args.drat_trim, str(cnfp), str(pr)], capture_output=True, text=True)
        v = 's VERIFIED' in r.stdout
        verdict += f'; drat-trim {"VERIFIED" if v else "FAILED"}'
        ok_all &= v
    elif not args.skip_sat:
        from pysat.solvers import Solver
        s = Solver(name='cadical195', bootstrap_with=clauses)
        r = s.solve(); s.delete()
        verdict += f'; SAT solver says {"UNSAT" if not r else "SATISFIABLE (!!)"}'
        ok_all &= (not r)
    say(f'    a={a}: {len(info["sets"])} killing sets, {nv} vars, {len(clauses)} clauses; {verdict}')
    closed.append(a_i)
say(f'closed values of a: {sorted(closed)}')
say(f'all_checks={ok_all}  ({time.time()-t0:.0f}s)')
sys.exit(0 if ok_all else 1)
