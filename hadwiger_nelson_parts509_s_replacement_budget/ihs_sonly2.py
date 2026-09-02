#!/usr/bin/env python3
"""S-only implicit hitting set search, v2: time-limited warm-started HiGHS MILP (highspy) per
round; lower bound = ceil(MILP dual bound); base = MILP incumbent (a hitting set of the family,
not necessarily minimum).  Terminates exactly when a base is valid and its size equals the
certified lower bound; otherwise keeps generating S-killing sets (workers grow bases to valid
sets by disjoint minimal killing sets; perturbed bases; greedy-minimised valid sets are
recorded as upper bounds in state.json)."""
import json, random, sys, time, argparse, math, multiprocessing as mp
from pathlib import Path
sys.path.insert(0, str(__import__('pathlib').Path(__file__).resolve().parent))
import numpy as np, highspy

ap = argparse.ArgumentParser()
ap.add_argument('--out', default='ihs_Sonly')
ap.add_argument('--seed', type=int, default=1)
ap.add_argument('--workers', type=int, default=6)
ap.add_argument('--batch', type=int, default=18)
ap.add_argument('--milp-time', type=float, default=90.0)
ap.add_argument('--solver', default='rc2', choices=['rc2', 'highs'], help='exact oracle: RC2 MaxSAT (exact every round) or time-limited HiGHS MILP')
ap.add_argument('--ub-file', default=None, help='json with a valid Y (upper bound) to seed the incumbent')
ap.add_argument('--oracle-every', type=int, default=1, help='run the exact oracle every k rounds; in between, reuse the last hitting set (repaired) as base')
ap.add_argument('--shrink', action='store_true', help='greedily shrink each grown valid set (slow; improves the upper bound)')
args = ap.parse_args()
out = Path(args.out); out.mkdir(parents=True, exist_ok=True)
hfile = out / 'hyperedges.jsonl'
rng = random.Random(args.seed)
S = list(range(374, 509)); Sset = set(S); xv = {v: i for i, v in enumerate(S)}
L = list(range(374))
pool = json.loads(Path(str(Path(__file__).resolve().parent / 'pool_S.json')).read_text())
Q5 = sorted(pool['Q5']); Q5set = set(Q5)

def log(msg):
    print(f"[{time.strftime('%H:%M:%S')}] {msg}", flush=True)

H = []; seen = set()
def record(D, p, wit_str, persist=True):
    key = frozenset(D)
    if key in seen:
        return False
    seen.add(key)
    row = {'D': sorted(D), 'pattern': p, 'witness_vertices_are_L_plus_U_minus_D': True, 'witness': wit_str}
    H.append(row)
    if persist:
        with hfile.open('a') as f:
            f.write(json.dumps(row) + '\n')
    return True
for line in hfile.read_text().splitlines() if hfile.exists() else []:
    if line.strip():
        row = json.loads(line); record(row['D'], row['pattern'], row['witness'], persist=False)
log(f'resumed {len(H)} S-only hyperedges')

def minimal_family():
    sets = sorted({frozenset(r['D']) for r in H}, key=len)
    keep = []
    for a in sets:
        if not any(b < a for b in keep if len(b) < len(a)):
            keep.append(a)
    return keep


def rc2_min_hitting_set(fam, V):
    """Exact minimum hitting set via core-guided MaxSAT (RC2, python-sat)."""
    from pysat.examples.rc2 import RC2
    from pysat.formula import WCNF
    xvar = {v: i + 1 for i, v in enumerate(V)}
    w = WCNF()
    for D in fam:
        w.append([xvar[v] for v in D])
    for v in V:
        w.append([-xvar[v]], weight=1)
    with RC2(w, solver='cd19', adapt=True, exhaust=False, minz=False) as rc2:
        m = rc2.compute()
        return [v for v in V if m[xvar[v] - 1] > 0]

def milp(fam, incumbent, time_limit):
    if args.solver == 'rc2':
        t = time.time(); hs = rc2_min_hitting_set(fam, S)
        return 'RC2 optimal', float(len(hs)), hs, time.time() - t
    h = highspy.Highs(); h.silent()
    n = len(S); inf = highspy.kHighsInf
    lp = highspy.HighsLp()
    lp.num_col_ = n; lp.num_row_ = len(fam)
    lp.col_cost_ = np.ones(n); lp.col_lower_ = np.zeros(n); lp.col_upper_ = np.ones(n)
    lp.row_lower_ = np.ones(len(fam)); lp.row_upper_ = np.full(len(fam), inf)
    starts = [0]; index = []; value = []
    for D in fam:
        for v in D:
            index.append(xv[v]); value.append(1.0)
        starts.append(len(index))
    lp.a_matrix_.format_ = highspy.MatrixFormat.kRowwise
    lp.a_matrix_.start_ = np.array(starts, dtype=np.int32); lp.a_matrix_.index_ = np.array(index, dtype=np.int32); lp.a_matrix_.value_ = np.array(value)
    lp.integrality_ = [highspy.HighsVarType.kInteger] * n
    h.passModel(lp)
    h.setOptionValue('time_limit', float(time_limit)); h.setOptionValue('mip_rel_gap', 0.0); h.setOptionValue('mip_abs_gap', 0.999)
    if incumbent:
        sol = highspy.HighsSolution(); inc = set(incumbent); sol.col_value = [1.0 if v in inc else 0.0 for v in S]
        h.setSolution(sol)
    t = time.time(); h.run()
    info = h.getInfo(); status = h.modelStatusToString(h.getModelStatus())
    x = h.getSolution().col_value
    hs = [v for v in S if x[xv[v]] > 0.5] if info.objective_function_value < 1e30 else None
    return status, info.mip_dual_bound, hs, time.time() - t

def repair(hs, fam):
    hs = set(hs)
    unc = [D for D in fam if not (D & hs)]
    while unc:
        cnt = {}
        for D in unc:
            for v in D:
                cnt[v] = cnt.get(v, 0) + 1
        m = max(cnt.values()); v = rng.choice([u for u, c in cnt.items() if c == m]); hs.add(v)
        unc = [D for D in unc if v not in D]
    byv = {}
    for D in fam:
        for v in D:
            if v in hs:
                byv.setdefault(v, []).append(D)
    for v in sorted(hs, key=lambda _: rng.random()):
        if all(len(D & hs) >= 2 for D in byv.get(v, [])):
            hs.discard(v)
    return sorted(hs)

G = None
SHRINK = False
def worker_init(shrink=False):
    global G, SHRINK
    SHRINK = shrink
    from sgadget import SGadget
    G = SGadget()

def worker_job(task):
    base, seed = task
    r = random.Random(seed)
    Y = set(base) | Q5set; found = []
    p = G.find_sat_pattern(sorted(Y), r)
    while p is not None:
        D, wit = G.minimal_killing(G.Uset - Y, p, r)
        verts = sorted(set(L) | (G.Uset - set(D)))
        found.append((sorted(D), p, ''.join(str(wit[v]) for v in verts)))
        Y |= set(D)
        p = G.find_sat_pattern(sorted(Y), r)
    if SHRINK:  # greedy shrink of the valid Y (S part only, one sweep) to improve the upper bound
        Ys = sorted(Y - Q5set); r.shuffle(Ys)
        for v in Ys:
            if G.phi(sorted((Y - {v}))):
                Y.discard(v)
    return found, sorted(Y - Q5set)

if __name__ == '__main__':
    from sgadget import SGadget
    g = SGadget()
    t0 = time.time(); it = 0
    best_valid = None
    if args.ub_file:
        best_valid = sorted(json.loads(Path(args.ub_file).read_text())['Y'])
    bound = 0; incumbent = None
    with mp.Pool(args.workers, initializer=worker_init, initargs=(args.shrink,)) as pool_:
        while True:
            it += 1
            fam = minimal_family()
            if it % args.oracle_every == 1 or args.oracle_every == 1 or incumbent is None:
                status, dual, hs, tm = milp(fam, incumbent, args.milp_time)
                db = math.ceil(dual - 1e-6)
                if db > bound:
                    bound = db
            else:
                status, dual, hs, tm = 'reused', float(bound), list(incumbent), 0.0
            hs = repair(hs, fam) if hs else repair([], fam)
            incumbent = hs
            log(f'round {it}: |H|={len(H)} minimal {len(fam)}; MILP {status} in {tm:.0f}s: dual {dual:.2f} -> LOWER BOUND {bound}; incumbent hitting set {len(hs)}; best valid {len(best_valid) if best_valid else None}; elapsed {time.time()-t0:.0f}s')
            (out / 'state.json').write_text(json.dumps({'round': it, 'h_S_lower_bound': bound, 'milp_status': status, 'hyperedges': len(H), 'minimal': len(fam), 'best_valid': len(best_valid) if best_valid else None, 'best_valid_Y': best_valid, 'hs': hs}))
            if g.phi(sorted(set(hs) | Q5set)):
                log(f'incumbent hitting set of size {len(hs)} is VALID: h_S <= {len(hs)}')
                if best_valid is None or len(hs) < len(best_valid):
                    best_valid = hs
                if len(hs) == bound:
                    log(f'h_S = {bound} EXACTLY; Y = {hs}')
                    (out / 'RESULT.json').write_text(json.dumps({'h_S': bound, 'Y': hs, 'family_size': len(H), 'minimal': len(fam)}))
                    break
            if best_valid is not None and bound >= len(best_valid):
                log(f'h_S = {len(best_valid)} EXACTLY (bound met by best valid); Y = {best_valid}')
                (out / 'RESULT.json').write_text(json.dumps({'h_S': len(best_valid), 'Y': best_valid, 'family_size': len(H), 'minimal': len(fam)}))
                break
            tasks = [(hs, rng.randrange(1 << 30))]
            for _ in range(args.batch - 1):
                base = set(hs)
                drop = rng.sample(sorted(base), max(1, int(len(base) * rng.uniform(0.1, 0.35))))
                base -= set(drop)
                tasks.append((repair(sorted(base), fam), rng.randrange(1 << 30)))
            t1 = time.time(); new = 0
            for found, Y in pool_.imap_unordered(worker_job, tasks):
                for D, p, w in found:
                    new += record(D, p, w)
                if best_valid is None or len(Y) < len(best_valid):
                    best_valid = Y
                    (out / 'best_valid.json').write_text(json.dumps({'Y': Y, 'size': len(Y)}))
            log(f'   batch of {len(tasks)}: {new} new S-killing sets in {time.time()-t1:.0f}s; best valid |Y| {len(best_valid) if best_valid else None}')
