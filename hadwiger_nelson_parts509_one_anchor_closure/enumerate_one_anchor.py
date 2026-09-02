#!/usr/bin/env python3
"""One-anchor configurations for the delete-5-add-4 closure of the Parts-509 graph (production version).

See the README for the reduction (committed one-anchor lemma).  For each anchor v ∈ V and each q ∈ Q (Q = Q3 ∪ Q2K ∪ nonK, the
points with >= 2 vertex neighbours) with |v - q| < 2, the two intersection points of the unit circles are
generated; coincident points (radius 1e-6) are grouped (scipy connected components); a group is a
candidate one-anchor point x with generator set Gx ⊆ Q (its Q-neighbours, complete up to the float
tolerance).  Groups are discarded ONLY when exact arithmetic shows x is not an added one-anchor point:
  (a) x = w ∈ V exactly: w is at unit distance (exact, in K) from v and from a K-rational generator q,
      hence w is one of the two exact intersection points of circle(v), circle(q), which are >= 6e-5
      apart because |v - q| < 2 - 1e-9; x is within 1e-6 of w, so x = w.
  (b) x = p ∈ Q3 ∪ Q2K exactly (then n(x) >= 2, x belongs to the all-anchored family): same argument
      with p in place of w (unit distance from v and from a K generator q, or from a non-K generator
      y = m + s t n via (p-m).n = 0 and |p-m|^2 + rho |n|^2 = 1, exact in K).
  (c) x = p non-K point of Q exactly: p's vertex neighbours are exactly its two generators {i, j}, so
      v ∈ {i, j} is required; and p at unit distance from a non-K generator y of x is decided by the
      exact non-K unit-pair list of the committed delete-4-add-3 closure (nonk_exact.json).
Everything else is kept (over-inclusive).  The neighbour lists and internal edges of the new points x, y use
the tolerance TOLX = 1e-5 (over-inclusive): if two distinct intersection points within 1e-6 of each other were
merged by the clustering, the merged coordinate is within 1e-6 of each true point, so every true unit
distance is still within TOLX; extra (false) edges only make the SAT tests more conservative.  Q-points keep
their exact neighbour lists.  Tangent pairs (|v - q| = 2) contribute the midpoint.  Configurations:
  type I : {x, y1, y2, y3}, y's ⊆ Gx, with the necessary degree condition that a point of Q with exactly
           two vertex neighbours (Q2K / non-K) has a second neighbour inside A;
  type II: {x, y, b, d}: b, d ∈ Gx with |b - d| = sqrt3 (tol 1e-6), y = reflection of x in line bd,
           y has a vertex at unit distance (tol 1e-7).
usage: enumerate_one_anchor.py OUTDIR [--workers W] [--anchors a b ...]   (env ONE_ANCHOR_UNIVERSE = output dir of build_universe.py, default ./universe)
"""
import json, sys, time, argparse, importlib.util, os
from pathlib import Path
from multiprocessing import Pool
from fractions import Fraction
import numpy as np
from scipy.spatial import cKDTree
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components

from paths import HERE, CRIT, COMPLETION, Q2K_EXTRA, NONK_EXACT
sys.path.insert(0, str(HERE))
QD = Path(os.environ.get('ONE_ANCHOR_UNIVERSE', str(HERE / 'universe')))   # output of build_universe.py
import kfield as kf
KK = 3; ONE = kf.one(KK); FOUR = kf.const(KK, 4); HALF = Fraction(1, 2)
TOL = 1e-7; TOLX = 1e-5; CL = 1e-6; SQ3 = np.sqrt(3.0)   # TOLX: over-inclusive tolerance for the new points x, y
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
    D.update(P=P, V=V, types=types, nbrs=nbrs, labels=labels, VE=VE, QE=Q3E + Q2E, upairs=upairs,
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
    Y = np.nonzero((d <= 2.0) & (d > 1e-9))[0]        # tangent / near-tangent pairs included (h = 0 gives the midpoint)
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
    st = {'anchor': int(v_idx), 'groups2': 0, 'disc_V': 0, 'disc_QK': 0, 'disc_QN': 0, 'kept': 0, 'kept_K2': 0,
          'kept_K1': 0, 'kept_N': 0, 'near_unresolved': 0, 'typeI': 0, 'typeII': 0, 'maxg': 0, 'points': []}
    confs = []
    vE = D['VE'][v_idx]
    for gi in range(len(sizes)):
        if sizes[gi] < 2:
            continue
        mem = order[starts[gi]:starts[gi] + sizes[gi]]
        G = np.unique(gen[mem]); g = len(G)
        if g < 2:
            continue
        st['groups2'] += 1
        x = X[mem].mean(axis=0)
        Kgens = [int(q) for q in G if isK[q]]; Ngens = [int(q) for q in G if not isK[q]]
        # (a) vertex?
        dV, iV = D['treeV'].query(x)
        if dV < CL:
            w = D['VE'][iV]
            if d2(w, vE) == ONE and any(kpoint_unit_to_gen(w, q) for q in Kgens + Ngens):
                st['disc_V'] += 1; continue
            st['near_unresolved'] += 1
        # (b)/(c) point of Q?
        dQ, iQ = D['treeQ'].query(x)
        if dQ < CL:
            if isK[iQ]:
                p = D['QE'][iQ]
                if d2(p, vE) == ONE and any(kpoint_unit_to_gen(p, q) for q in Kgens + Ngens):
                    st['disc_QK'] += 1; continue
            else:
                labp = tuple(D['labels'][iQ - NQ3 - NQ2K])
                if v_idx in labp[:2] and any((labp, tuple(D['labels'][y - NQ3 - NQ2K])) in D['upairs'] for y in Ngens):
                    st['disc_QN'] += 1; continue
            st['near_unresolved'] += 1
        st['kept'] += 1; st['maxg'] = max(st['maxg'], g)
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
    ap = argparse.ArgumentParser(); ap.add_argument('outdir'); ap.add_argument('--workers', type=int, default=2)
    ap.add_argument('--anchors', type=int, nargs='*', default=None)
    args = ap.parse_args()
    out = Path(args.outdir); out.mkdir(exist_ok=True)
    load()
    anchors = args.anchors if args.anchors else list(range(len(D['V'])))
    t0 = time.time(); stats = []; allconfs = []
    with Pool(args.workers, initializer=load) as pool:
        for st, confs in pool.imap_unordered(per_anchor, anchors, chunksize=1):
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
    print(f'total {time.time()-t0:.0f}s', flush=True)


if __name__ == '__main__':
    main()
