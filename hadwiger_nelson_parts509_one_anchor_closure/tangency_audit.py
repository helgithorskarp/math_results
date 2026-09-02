#!/usr/bin/env python3
"""Exact audit of the circle-intersection cutoff |v - q| <= 2 of the one-anchor enumeration.

For every anchor v ∈ V and every q ∈ Q (Q3 ∪ Q2K ∪ nonK) with binary64 distance within 1e-6 of 2 the
distance is decided exactly (K arithmetic for K-points; for a non-K point q = m + s t n with t² = rho ∈ K
not a square, |v - q|² = 4 iff (v - m)·n = 0 and |v - m|² + rho |n|² = 4).  For every exact tangency the
unique common unit neighbour of v and q, the midpoint (v + q)/2, is classified exactly: a vertex, a point of
Q3 ∪ Q2K, a non-K point of Q, or none (a midpoint that the enumeration screen `d <= 2.0` could miss when
binary64 rounds the distance above 2).  The audit also reports the minimum gap 2 - |v - q| over the exactly
non-tangent screened pairs with |v - q| < 2 (this bounds from below the separation 2 sqrt(1 - d²/4) of the
two intersection points of any non-tangent pair) and the largest binary64 deviation |d - 2| over exact
tangencies.
usage: tangency_audit.py [--universe DIR] [--out audit.json] [--window 1e-6]
"""
import json, sys, time, argparse, math, importlib.util, os
from pathlib import Path
from fractions import Fraction
import numpy as np
from scipy.spatial import cKDTree
from paths import HERE, CRIT, COMPLETION, Q2K_EXTRA, NONK_EXACT
sys.path.insert(0, str(HERE))
import kfield as kf
KK = 3; ONE = kf.one(KK); FOUR = kf.const(KK, 4); HALF = Fraction(1, 2)
NQ3, NQ2K = 1158, 2705


def d2(p, q):
    dx = kf.sub(p[0], q[0]); dy = kf.sub(p[1], q[1])
    return kf.add(kf.mul(dx, dx, KK), kf.mul(dy, dy, KK))


def nonk_geom(VE, lab):
    i, j, s = lab
    xi, yi = VE[i]; xj, yj = VE[j]
    dx = kf.sub(xi, xj); dy = kf.sub(yi, yj)
    dd = kf.add(kf.mul(dx, dx, KK), kf.mul(dy, dy, KK))
    rho = kf.mul(kf.sub(FOUR, dd), kf.inv(kf.scale(dd, 4), KK), KK)
    m = (kf.scale(kf.add(xi, xj), HALF), kf.scale(kf.add(yi, yj), HALF))
    n = (kf.neg(dy), dx)
    return m, n, rho


def kpoint_dist2_to_nonk_equals(p, VE, lab, target):
    """Exact: is |p - y|² = target for the K-point p and the non-K point y = m + s t n?"""
    m, n, rho = nonk_geom(VE, lab)
    w = (kf.sub(p[0], m[0]), kf.sub(p[1], m[1]))
    dot = kf.add(kf.mul(w[0], n[0], KK), kf.mul(w[1], n[1], KK))
    if not kf.is_zero(dot):
        return False
    val = kf.add(kf.add(kf.mul(w[0], w[0], KK), kf.mul(w[1], w[1], KK)),
                 kf.mul(rho, kf.add(kf.mul(n[0], n[0], KK), kf.mul(n[1], n[1], KK)), KK))
    return val == target


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--universe', default=os.environ.get('ONE_ANCHOR_UNIVERSE', str(HERE / 'universe')))
    ap.add_argument('--out', default='tangency_audit.json'); ap.add_argument('--window', type=float, default=1e-6)
    args = ap.parse_args(); t0 = time.time()
    QD = Path(args.universe)
    P = np.load(QD / 'P_float.npy'); V = np.load(QD / 'V_float.npy')
    meta = json.loads((QD / 'universe_meta.json').read_text()); labels = [tuple(l) for l in meta['nonk_labels']]
    types = meta['types']
    spec = importlib.util.spec_from_file_location('parts509', CRIT / 'parts509.py')
    parts = importlib.util.module_from_spec(spec); spec.loader.exec_module(parts)
    VE = parts.parse_points(CRIT / 'parts509.vtx')
    comp = json.loads(COMPLETION.read_text())
    QE = [(kf.from_strings(r['x']), kf.from_strings(r['y'])) for r in comp['points']]
    ex = json.loads(Q2K_EXTRA.read_text())
    QE += [(kf.from_strings(r['x']), kf.from_strings(r['y'])) for r in ex['q2k']]
    assert len(QE) == NQ3 + NQ2K and len(labels) == len(P) - NQ3 - NQ2K
    nx = json.loads(NONK_EXACT.read_text())
    upairs = set()
    for a, b in nx['unit_pairs']:
        upairs.add((tuple(a), tuple(b))); upairs.add((tuple(b), tuple(a)))
    treeV = cKDTree(V); treeQ = cKDTree(P)

    def is_tangent(v, q):
        if q < NQ3 + NQ2K:
            return d2(VE[v], QE[q]) == FOUR
        return kpoint_dist2_to_nonk_equals(VE[v], VE, labels[q - NQ3 - NQ2K], FOUR)

    def unit(p, q):
        """exact: K-point p at unit distance from Q-point q"""
        if q < NQ3 + NQ2K:
            return d2(p, QE[q]) == ONE
        return kpoint_dist2_to_nonk_equals(p, VE, labels[q - NQ3 - NQ2K], ONE)

    screened = 0; tang = []; nontang_below = []; nontang_above = 0
    for v in range(len(V)):
        d = np.hypot(P[:, 0] - V[v, 0], P[:, 1] - V[v, 1])
        idx = np.nonzero(np.abs(d - 2.0) < args.window)[0]
        for q in idx:
            q = int(q); screened += 1
            if is_tangent(v, q):
                tang.append((v, q, float(d[q])))
            elif d[q] < 2.0:
                nontang_below.append((v, q, float(2.0 - d[q])))
            else:
                nontang_above += 1
    print(f'screened pairs (|d-2| < {args.window}): {screened}; exact tangencies {len(tang)}; non-tangent with d < 2: {len(nontang_below)}, with d >= 2: {nontang_above}  ({time.time()-t0:.0f}s)', flush=True)
    omitted = [t for t in tang if t[2] > 2.0]
    maxdev = max((abs(t[2] - 2.0) for t in tang), default=0.0)
    # classify midpoints of all exact tangencies
    classes = {'vertex': 0, 'q3': 0, 'q2k': 0, 'nonk': 0, 'none': 0}; omitted_classes = {'vertex': 0, 'q3': 0, 'q2k': 0, 'nonk': 0, 'none': 0}
    none_list = []
    for v, q, dq in tang:
        x = (V[v] + P[q]) / 2
        cls = None
        dv, iv = treeV.query(x)
        if dv < 1e-6:
            w = VE[int(iv)]
            if d2(w, VE[v]) == ONE and unit(w, q):
                cls = 'vertex'
        if cls is None:
            dqq, iq = treeQ.query(x); iq = int(iq)
            if dqq < 1e-6:
                if iq < NQ3 + NQ2K:
                    p = QE[iq]
                    if d2(p, VE[v]) == ONE and unit(p, q):
                        cls = 'q3' if iq < NQ3 else 'q2k'
                else:
                    labp = labels[iq - NQ3 - NQ2K]
                    if v in labp[:2] and q >= NQ3 + NQ2K and (labp, labels[q - NQ3 - NQ2K]) in upairs:
                        cls = 'nonk'
        if cls is None:
            cls = 'none'; none_list.append((v, q, [float(x[0]), float(x[1])]))
        classes[cls] += 1
        if dq > 2.0:
            omitted_classes[cls] += 1
    mingap = min((g for _, _, g in nontang_below), default=None)
    minsep = 2 * math.sqrt(mingap * (1 - mingap / 4)) if mingap is not None else None
    res = {'window': args.window, 'screened_pairs': screened, 'exact_tangencies': len(tang), 'tangencies_with_binary64_d_above_2': len(omitted),
           'max_binary64_deviation_of_tangencies': maxdev, 'midpoint_classes': classes, 'omitted_midpoint_classes': omitted_classes,
           'unclassified_midpoints': none_list, 'nontangent_pairs_with_d_below_2': len(nontang_below),
           'min_gap_2_minus_d': mingap, 'min_intersection_separation': minsep,
           'min_gap_pair': min(nontang_below, key=lambda t: t[2])[:2] if nontang_below else None,
           'nontangent_screened_pairs_with_d_at_least_2': nontang_above, 'seconds': round(time.time() - t0, 1)}
    Path(args.out).write_text(json.dumps(res, indent=1))
    print(f'exact tangencies {len(tang)}, binary64 d > 2 for {len(omitted)} of them (max |d-2| {maxdev:.3e}); midpoints: {classes}; omitted: {omitted_classes}')
    print(f'min non-tangent gap 2-d = {mingap} (pair {res["min_gap_pair"]}), intersection separation >= {minsep}')
    print(f'unclassified midpoints: {len(none_list)}  -> {"OK" if not none_list else "ATTENTION"}  ({time.time()-t0:.0f}s)')


if __name__ == '__main__':
    main()
