#!/usr/bin/env python3
"""One-anchor configurations for the delete-5-add-4 closure of the Parts-509 graph (production version).

See the README for the reduction (committed one-anchor lemma).  For each anchor v ∈ V and each q ∈ Q (Q = Q3 ∪ Q2K ∪ nonK, the
points with >= 2 vertex neighbours) with |v - q| < 2, the two intersection points of the unit circles are
generated; coincident points (radius 1e-6) are grouped (scipy connected components); a group is a
candidate one-anchor point x with generator set Gx ⊆ Q (its Q-neighbours, complete up to the float
tolerance).  Groups are discarded ONLY when exact arithmetic shows x is not an added one-anchor point:
A member X_k (generator q_k) is *identified* with an exact point w ∈ V ∪ Q when w is a unit neighbour of the
anchor v, w is a unit neighbour of q_k, and |X_k - w| < TD = 1e-6 (binary64).  All unit incidences used here
are looked up in the committed exact lists (V-V and V-Q3 edges of the ambient graph, the V-neighbour lists of
Q3 / Q2K / non-K points, the K-internal edges Q3-Q3 / Q2K-Q3 / Q2K-Q2K, the exact non-K unit pairs of
nonk_exact.json; non-K points have no unit neighbour in K² other than their two generating vertices).
Soundness: the exact point x_k* of the member lies on circle(v) and circle(q_k), so x_k* ∈ {w, w'} with w'
the second intersection point; |x_k* - w| <= TD + E with E <= 1e-7 the forward error of a member, while
|w - w'| = 2 sqrt(1 - |v - q_k|²/4) >= 7.45e-6 for every non-tangent anchor-Q pair (audited minimum gap
2 - |v - q| >= 1.388e-11, tangency_audit.py) and w = w' for a tangent pair; hence x_k* = w.  Identified
members are removed from the group (they represent w, which is a vertex or a point with >= 2 vertex
neighbours, never an added one-anchor point); the identification is repeated with the residual centroid
(candidates w within CL + radius of the centroid); the residual members, if they have >= 2 generators, form
the candidate point x (centroid of the residual).  A true one-anchor point x* ≠ w never loses a member to
identification (its members would have x_k* = w), so the residual's generator set contains N_Q(x*).
Everything else is kept (over-inclusive).  A group is a single-linkage component and may be chained beyond
the linking radius CL = 1e-6; the rule above does not depend on the component radius.  For the kept
residuals the neighbour lists and internal edges of the new points x, y use the tolerance TOLX = 1e-5
around the residual centroid; this is over-inclusive for every exact point represented provided the
residual radius r (max member-centroid distance) satisfies r + E < TOLX, which the run certifies
(max_radius over all kept residuals, asserted < TOLX - 2e-7; a 4-colouring extending to a superset of the
true constraints extends to the true ones).  Q-points keep their exact neighbour lists.  The screen is
outward-rounded, d <= 2 + 2^-40: exact tangencies whose binary64 distance rounds above 2 (79 pairs) are
included (they contribute the midpoint); pairs slightly above 2 contribute a spurious midpoint, which is
harmless (over-inclusive; such a member is never identified because no point is at unit distance from both
ends of a pair at distance > 2).  Configurations:
  type I : {x, y1, y2, y3}, y's ⊆ Gx, with the necessary degree condition that a point of Q with exactly
           two vertex neighbours (Q2K / non-K) has a second neighbour inside A;
  type II: {x, y, b, d}: b, d ∈ Gx with |b - d| = sqrt3 (tol 1e-6), y = reflection of x in line bd,
           y has a vertex at unit distance (tol 1e-7).
usage: enumerate_one_anchor.py OUTDIR [--workers W] [--anchors a b ...] [--universe DIR]   (DIR = output dir of build_universe.py; default env ONE_ANCHOR_UNIVERSE or ./universe)
"""
import json, sys, time, argparse, importlib.util, os
from pathlib import Path
from multiprocessing import Pool
from fractions import Fraction
import numpy as np
from scipy.spatial import cKDTree
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components

from paths import HERE, CRIT, PAIR, COMPLETION, Q2K_EXTRA, NONK_EXACT
sys.path.insert(0, str(HERE))
QD = Path(os.environ.get('ONE_ANCHOR_UNIVERSE', str(HERE / 'universe')))   # output of build_universe.py
import kfield as kf
KK = 3; ONE = kf.one(KK); FOUR = kf.const(KK, 4); HALF = Fraction(1, 2)
TOL = 1e-7; TOLX = 1e-5; CL = 1e-6; TD = 1e-6; EFWD = 1e-7; SQ3 = np.sqrt(3.0)   # TOLX: over-inclusive tolerance for the new points x, y; TD: per-member discard radius; EFWD: forward error bound of a member
DMAX = 2.0 + 2.0 ** -40   # outward-rounded circle-intersection cutoff
NQ3, NQ2K = 1158, 2705
D = {}


def d2(p, q):
    dx = kf.sub(p[0], q[0]); dy = kf.sub(p[1], q[1])
    return kf.add(kf.mul(dx, dx, KK), kf.mul(dy, dy, KK))


def load():
    P = np.load(QD / 'P_float.npy'); V = np.load(QD / 'V_float.npy')
    meta = json.loads((QD / 'universe_meta.json').read_text())
    types = np.array(meta['types']); nbrs = meta['nbrs']; labels = meta['nonk_labels']
    assert len(labels) == len(P) - NQ3 - NQ2K
    spec = importlib.util.spec_from_file_location('parts509', CRIT / 'parts509.py')
    parts = importlib.util.module_from_spec(spec); spec.loader.exec_module(parts)
    VE = parts.parse_points(CRIT / 'parts509.vtx')
    comp = json.loads(COMPLETION.read_text())
    Q3E = [(kf.from_strings(r['x']), kf.from_strings(r['y'])) for r in comp['points']]
    ex = json.loads(Q2K_EXTRA.read_text())
    Q2E = [(kf.from_strings(r['x']), kf.from_strings(r['y'])) for r in ex['q2k']]
    nx = json.loads(NONK_EXACT.read_text())
    upairs = set()
    for a, b in nx['unit_pairs']:
        upairs.add((tuple(a), tuple(b))); upairs.add((tuple(b), tuple(a)))
    lab2idx = {tuple(l): NQ3 + NQ2K + k for k, l in enumerate(labels)}
    # exact incidence lookups from the committed lists
    amb = json.loads((PAIR / 'ambient_w3_edges.json').read_text())
    NV = len(VE)
    vadj = [set() for _ in range(NV)]
    kedges = set()
    for a, b in amb['edges']:
        if a < NV and b < NV:
            vadj[a].add(b); vadj[b].add(a)
        elif a >= NV and b >= NV:
            kedges.add((min(a, b) - NV, max(a, b) - NV))          # Q3-Q3 (universe indices = Q3 indices)
    for p, a in ex['adj_q2k_q3']:
        kedges.add((a, NQ3 + p))
    for p, q in ex['adj_q2k_q2k']:
        kedges.add((NQ3 + min(p, q), NQ3 + max(p, q)))
    qnbrs = [set(n) for n in nbrs]
    for q3i, r in enumerate(comp['points']):                      # consistency of the V-Q3 lists with the ambient edges
        assert qnbrs[q3i] == {a for a, b in amb['edges'] if b == NV + q3i and a < NV} | {b for a, b in amb['edges'] if a == NV + q3i and b < NV}
    D.update(P=P, V=V, types=types, nbrs=nbrs, qnbrs=qnbrs, labels=labels, VE=VE, QE=Q3E + Q2E, upairs=upairs, vadj=vadj, kedges=kedges,
             treeV=cKDTree(V), treeQ=cKDTree(P), isK=(types != 'nonk'))


def nonk_geom(lab):
    i, j, s = lab
    xi, yi = D['VE'][i]; xj, yj = D['VE'][j]
    dx = kf.sub(xi, xj); dy = kf.sub(yi, yj)
    dd = kf.add(kf.mul(dx, dx, KK), kf.mul(dy, dy, KK))
    rho = kf.mul(kf.sub(FOUR, dd), kf.inv(kf.scale(dd, 4), KK), KK)
    m = (kf.scale(kf.add(xi, xj), HALF), kf.scale(kf.add(yi, yj), HALF))
    n = (kf.neg(dy), dx)
    return m, n, rho


def kpoint_unit_to_nonk(p, lab):
    """Exact: is the K-point p at unit distance from the non-K point m + s t n?  (s irrelevant: needs (p-m).n = 0.)"""
    m, n, rho = nonk_geom(lab)
    w = (kf.sub(p[0], m[0]), kf.sub(p[1], m[1]))
    dot = kf.add(kf.mul(w[0], n[0], KK), kf.mul(w[1], n[1], KK))
    if not kf.is_zero(dot):
        return False
    val = kf.add(kf.add(kf.mul(w[0], w[0], KK), kf.mul(w[1], w[1], KK)), kf.mul(rho, kf.add(kf.mul(n[0], n[0], KK), kf.mul(n[1], n[1], KK)), KK))
    return val == ONE


def kpoint_unit_to_gen(p, g):
    """Exact unit distance between K-point p and generator g (index into P)."""
    if D['isK'][g]:
        return d2(p, D['QE'][g]) == ONE
    return kpoint_unit_to_nonk(p, D['labels'][g - NQ3 - NQ2K])


def per_anchor(v_idx):
    P, V, types, nbrs, isK = D['P'], D['V'], D['types'], D['nbrs'], D['isK']
    c = V[v_idx]; t0 = time.time()
    d = np.hypot(P[:, 0] - c[0], P[:, 1] - c[1])
    Y = np.nonzero((d <= DMAX) & (d > 1e-9))[0]       # outward-rounded: exact tangencies included (h = 0 gives the midpoint)
    dd = P[Y] - c[None, :]; dist = np.hypot(dd[:, 0], dd[:, 1])
    h = np.sqrt(np.maximum(1 - dist ** 2 / 4, 0.0)); m = c[None, :] + dd / 2
    n = np.stack([-dd[:, 1], dd[:, 0]], axis=1) / dist[:, None]
    X = np.stack([m + h[:, None] * n, m - h[:, None] * n], axis=1).reshape(-1, 2); gen = np.repeat(Y, 2)
    tree = cKDTree(X); pairs = tree.query_pairs(CL, output_type='ndarray'); nX = len(X)
    if len(pairs):
        A = coo_matrix((np.ones(len(pairs)), (pairs[:, 0], pairs[:, 1])), shape=(nX, nX))
        ncomp, lab = connected_components(A, directed=False)
    else:
        lab = np.arange(nX)
    order = np.argsort(lab, kind='stable'); ls = lab[order]
    starts = np.r_[0, np.nonzero(np.diff(ls))[0] + 1, len(ls)]; sizes = np.diff(starts)
    st = {'anchor': int(v_idx), 'groups2': 0, 'disc_V': 0, 'disc_QK': 0, 'disc_QN': 0, 'split': 0, 'residual_small': 0, 'kept': 0,
          'kept_K2': 0, 'kept_K1': 0, 'kept_N': 0, 'near_unresolved': 0, 'typeI': 0, 'typeII': 0, 'maxg': 0, 'points': [],
          'max_radius': 0.0, 'chained_kept': 0}
    confs = []
    vE = D['VE'][v_idx]
    qnbrs, vadj, kedges, labels, upairs, treeV, treeQ = D['qnbrs'], D['vadj'], D['kedges'], D['labels'], D['upairs'], D['treeV'], D['treeQ']

    def adj_exact(w_is_vertex, w, q):
        # exact unit incidence between the identified point w (vertex index, or universe index) and the generator q
        if w_is_vertex:
            return w in qnbrs[q]
        if isK[w]:
            return isK[q] and q != w and (min(w, q), max(w, q)) in kedges
        return (not isK[q]) and (tuple(labels[w - NQ3 - NQ2K]), tuple(labels[q - NQ3 - NQ2K])) in upairs

    for gi in range(len(sizes)):
        if sizes[gi] < 2:
            continue
        mem = order[starts[gi]:starts[gi] + sizes[gi]]
        Xm = X[mem]; gm = gen[mem]
        if len(np.unique(gm)) < 2:
            continue
        st['groups2'] += 1
        alive = np.ones(len(mem), dtype=bool); ident = {'V': 0, 'QK': 0, 'QN': 0}; near = False
        while alive.any():
            xa = Xm[alive].mean(axis=0); ra = float(np.max(np.hypot(Xm[alive, 0] - xa[0], Xm[alive, 1] - xa[1])))
            removed = False
            for iV in treeV.query_ball_point(xa, CL + ra):
                if iV not in vadj[v_idx]:
                    near = True; continue
                close = np.hypot(Xm[:, 0] - V[iV, 0], Xm[:, 1] - V[iV, 1]) < TD
                ok = alive & close & np.array([adj_exact(True, iV, int(q)) for q in gm])
                if ok.any():
                    alive &= ~ok; ident['V'] += int(ok.sum()); removed = True
                elif (alive & close).any():
                    near = True
            for iQ in treeQ.query_ball_point(xa, CL + ra):
                if v_idx not in qnbrs[iQ]:
                    near = True; continue
                close = np.hypot(Xm[:, 0] - P[iQ, 0], Xm[:, 1] - P[iQ, 1]) < TD
                ok = alive & close & np.array([adj_exact(False, iQ, int(q)) for q in gm])
                if ok.any():
                    alive &= ~ok; ident['QK' if isK[iQ] else 'QN'] += int(ok.sum()); removed = True
                elif (alive & close).any():
                    near = True
            if not removed:
                break
        nid = sum(ident.values())
        if not alive.any():
            key = max(ident, key=ident.get); st['disc_' + key] += 1
            continue
        if nid:
            st['split'] += 1
        elif near:
            st['near_unresolved'] += 1
        G = np.unique(gm[alive]); g = len(G)
        if g < 2:
            st['residual_small'] += 1; continue
        x = Xm[alive].mean(axis=0)
        r = float(np.max(np.hypot(Xm[alive, 0] - x[0], Xm[alive, 1] - x[1])))
        Kgens = [int(q) for q in G if isK[q]]; Ngens = [int(q) for q in G if not isK[q]]
        st['kept'] += 1; st['maxg'] = max(st['maxg'], g)
        st['max_radius'] = max(st['max_radius'], r)
        if r >= CL:
            st['chained_kept'] += 1
        if len(Kgens) >= 2: st['kept_K2'] += 1
        elif len(Kgens) == 1: st['kept_K1'] += 1
        else: st['kept_N'] += 1
        dv = np.hypot(V[:, 0] - x[0], V[:, 1] - x[1])
        nx = [int(i) for i in np.nonzero(np.abs(dv - 1) < TOLX)[0]]
        assert v_idx in nx
        st['points'].append({'x': [float(x[0]), float(x[1])], 'nbrs': nx, 'gens': [int(q) for q in G]})
        Pg = P[G]
        dg = np.hypot(Pg[:, None, 0] - Pg[None, :, 0], Pg[:, None, 1] - Pg[None, :, 1])
        adj = np.abs(dg - 1) < TOLX; r3 = np.abs(dg - SQ3) < TOLX
        k = g
        needs = [types[G[t]] != 'q3' for t in range(k)]      # needs a second neighbour inside A
        for a in range(k):
            for b in range(a + 1, k):
                for cc in range(b + 1, k):
                    T = (a, b, cc)
                    if any(needs[t] and not any(adj[t, s] for s in T if s != t) for t in T):
                        continue
                    pts = [{'nbrs': nx, 'x': [float(x[0]), float(x[1])]}] + [{'nbrs': nbrs[G[t]], 'q': int(G[t])} for t in T]
                    edges = [[0, 1], [0, 2], [0, 3]] + [[1 + i, 1 + j] for i in range(3) for j in range(i + 1, 3) if adj[T[i], T[j]]]
                    confs.append({'id': f'I:{v_idx}:{G[a]}:{G[b]}:{G[cc]}', 'type': 'I', 'points': pts, 'edges': edges})
                    st['typeI'] += 1
        for a in range(k):
            for b in range(a + 1, k):
                if not r3[a, b]:
                    continue
                pb, pd = Pg[a], Pg[b]
                u = pd - pb; u = u / np.hypot(*u); w = x - pb
                y = pb + 2 * (w @ u) * u - w
                if abs(np.hypot(*(y - x)) - 1) > TOLX:
                    continue
                dy = np.hypot(V[:, 0] - y[0], V[:, 1] - y[1])
                ny = [int(i) for i in np.nonzero(np.abs(dy - 1) < TOLX)[0]]
                if not ny:
                    continue
                pts = [{'nbrs': nx, 'x': [float(x[0]), float(x[1])]}, {'nbrs': ny, 'x': [float(y[0]), float(y[1])]},
                       {'nbrs': nbrs[G[a]], 'q': int(G[a])}, {'nbrs': nbrs[G[b]], 'q': int(G[b])}]
                confs.append({'id': f'II:{v_idx}:{G[a]}:{G[b]}', 'type': 'II', 'points': pts, 'edges': [[0, 1], [0, 2], [0, 3], [1, 2], [1, 3]]})
                st['typeII'] += 1
    st['seconds'] = round(time.time() - t0, 1)
    return st, confs


def main():
    global QD
    ap = argparse.ArgumentParser(); ap.add_argument('outdir'); ap.add_argument('--workers', type=int, default=2)
    ap.add_argument('--anchors', type=int, nargs='*', default=None)
    ap.add_argument('--universe', default=None, help='output directory of build_universe.py (default: env ONE_ANCHOR_UNIVERSE or ./universe)')
    args = ap.parse_args()
    if args.universe:
        QD = Path(args.universe); os.environ['ONE_ANCHOR_UNIVERSE'] = str(QD)
    out = Path(args.outdir); out.mkdir(exist_ok=True)
    load()
    anchors = args.anchors if args.anchors else list(range(len(D['V'])))
    t0 = time.time(); stats = []; allconfs = []
    # per-anchor checkpoints (OUTDIR/anchors/a_XXX.json) make the run resumable: finished anchors are skipped
    ck = out / 'anchors'; ck.mkdir(exist_ok=True)
    for a in anchors:
        f = ck / f'a_{a:03d}.json'
        if f.exists():
            d = json.loads(f.read_text()); stats.append(d['stats']); allconfs.extend(d['configs'])
    todo = [a for a in anchors if not (ck / f'a_{a:03d}.json').exists()]
    print(f'{len(anchors) - len(todo)} anchors loaded from checkpoints, {len(todo)} to do', flush=True)
    with Pool(args.workers, initializer=load) as pool:
        for st, confs in pool.imap_unordered(per_anchor, todo, chunksize=1):
            (ck / f"a_{st['anchor']:03d}.json").write_text(json.dumps({'stats': st, 'configs': confs}))
            stats.append(st); allconfs.extend(confs)
            s = {k: v for k, v in st.items() if k != 'points'}
            print(f"anchor {st['anchor']}: {s}  | totals: configs {len(allconfs)} (I {sum(x['typeI'] for x in stats)}, II {sum(x['typeII'] for x in stats)}), kept points {sum(x['kept'] for x in stats)}, unresolved {sum(x['near_unresolved'] for x in stats)}; {len(stats)}/{len(anchors)} anchors, {time.time()-t0:.0f}s", flush=True)
    seen = {}
    for cf in allconfs:
        key = tuple(sorted(('q', p['q']) if 'q' in p else ('x', round(p['x'][0], 6), round(p['x'][1], 6)) for p in cf['points']))
        seen.setdefault(key, cf)
    uniq = list(seen.values())
    print(f'configurations: {len(allconfs)} raw, {len(uniq)} distinct; type I {sum(c["type"]=="I" for c in uniq)}, type II {sum(c["type"]=="II" for c in uniq)}', flush=True)
    (out / 'configs.json').write_text(json.dumps(uniq))
    (out / 'stats.json').write_text(json.dumps(stats))
    max_r = max(x['max_radius'] for x in stats); chained = sum(x['chained_kept'] for x in stats)
    print(f'radius certificate: max residual radius over kept candidate points {max_r:.3e} (chained kept groups {chained}); '
          f'bound TOLX - 2*EFWD = {TOLX - 2 * EFWD:.3e}: {"OK" if max_r < TOLX - 2 * EFWD else "VIOLATED"}', flush=True)
    print(f"groups {sum(x['groups2'] for x in stats)}: discarded as vertex {sum(x['disc_V'] for x in stats)}, as K-point of Q {sum(x['disc_QK'] for x in stats)}, "
          f"as non-K point of Q {sum(x['disc_QN'] for x in stats)}, split {sum(x['split'] for x in stats)} (residual with < 2 generators {sum(x['residual_small'] for x in stats)}), "
          f"kept {sum(x['kept'] for x in stats)}, near-unresolved kept {sum(x['near_unresolved'] for x in stats)}", flush=True)
    assert max_r < TOLX - 2 * EFWD, 'component radius certificate violated: neighbour lists might not be over-inclusive'
    print(f'total {time.time()-t0:.0f}s', flush=True)


if __name__ == '__main__':
    main()
