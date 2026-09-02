#!/usr/bin/env python3
"""Exact confirmation of unit distances among non-K intersection points.

A non-K point is p = m + s*t*n with m the midpoint of a vertex pair (i, j),
n = (-(yi - yj), xi - xj), t = sqrt(rho) > 0, rho = (4 - d^2)/(4 d^2) in K not
a square in K, s = +-1.  For two such points (t1 = sqrt(rho1), t2 = sqrt(rho2)):
  Case A  rho1*rho2 = k^2 with k in K, k > 0: t2 = k t1 / rho1, so
          p1 - p2 = a + t1 b with a, b in K^2 and |p1-p2|^2 = |a|^2 + rho1 |b|^2 + 2 t1 (a.b);
          unit iff |a|^2 + rho1|b|^2 = 1 and a.b = 0.
  Case B  otherwise {1, t1, t2, t1 t2} is a K-basis of K(t1, t2) and unit iff
          (m1-m2).n1 = (m1-m2).n2 = n1.n2 = 0 and |m1-m2|^2 + rho1|n1|^2 + rho2|n2|^2 = 1.
A non-K point is at unit distance from no point of K^2 other than its two
generating vertices (three K^2 unit neighbours would force p in K^2).

Usage: nonk_exact.py q2k_extra.json out.json [--workers W]
"""
from __future__ import annotations
import argparse, importlib.util, json, sys, time
from pathlib import Path
from multiprocessing import Pool

HERE = Path(__file__).resolve().parent
_CAND = [HERE.parent, Path.home() / 'math_results']
SWAPDIR = next(p / 'hadwiger_nelson_parts509_swap_closure' for p in _CAND
               if (p / 'hadwiger_nelson_parts509_swap_closure' / 'swap_certificate.json').exists())
BASEDIR = next(p / 'hadwiger_nelson_parts509_criticality' for p in _CAND
               if (p / 'hadwiger_nelson_parts509_criticality' / 'parts509.py').exists())
sys.path.insert(0, str(SWAPDIR))
import kfield as kf
KK = 3
FOUR = kf.const(KK, 4)
ONE = kf.one(KK)
ZERO = kf.zero(KK)
_G = {}


def load_points():
    spec = importlib.util.spec_from_file_location('parts509_nk', BASEDIR / 'parts509.py')
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    return m.parse_points(BASEDIR / 'parts509.vtx')


def geom(pts, i, j, s):
    xi, yi = pts[i]; xj, yj = pts[j]
    dx = kf.sub(xi, xj); dy = kf.sub(yi, yj)
    d2 = kf.add(kf.mul(dx, dx, KK), kf.mul(dy, dy, KK))
    rho = kf.mul(kf.sub(FOUR, d2), kf.inv(kf.scale(d2, 4), KK), KK)
    m = (kf.scale(kf.add(xi, xj), kf.Fraction(1, 2)), kf.scale(kf.add(yi, yj), kf.Fraction(1, 2)))
    n = (kf.neg(dy), dx)
    return m, n, rho, s


def dot(a, b):
    return kf.add(kf.mul(a[0], b[0], KK), kf.mul(a[1], b[1], KK))


def unit_nonk_pair(g1, g2):
    (m1, n1, r1, s1), (m2, n2, r2, s2) = g1, g2
    a = (kf.sub(m1[0], m2[0]), kf.sub(m1[1], m2[1]))
    k = kf.field_sqrt(kf.mul(r1, r2, KK), KK)
    if k is not None:
        if kf.sign(k) < 0:
            k = kf.neg(k)
        c = kf.mul(k, kf.inv(r1, KK), KK)                 # t2 = c * t1
        b = (kf.sub(kf.scale(n1[0], s1), kf.scale(kf.mul(c, n2[0], KK), s2)),
             kf.sub(kf.scale(n1[1], s1), kf.scale(kf.mul(c, n2[1], KK), s2)))
        val = kf.add(dot(a, a), kf.mul(r1, dot(b, b), KK))
        return val == ONE and dot(a, b) == ZERO, 'A'
    ok = (dot(a, n1) == ZERO and dot(a, n2) == ZERO and dot(n1, n2) == ZERO and
          kf.add(kf.add(dot(a, a), kf.mul(r1, dot(n1, n1), KK)), kf.mul(r2, dot(n2, n2), KK)) == ONE)
    return ok, 'B'


def unit_nonk_kpoint(g, q):
    """Exact test |p - q|^2 == 1 for a non-K point p and a K-point q: p - q = (m - q) + s t n,
    squared norm = |m-q|^2 + rho|n|^2 + 2 s t (m-q).n; unit iff (m-q).n = 0 and |m-q|^2 + rho|n|^2 = 1."""
    m, n, rho, s = g
    a = (kf.sub(m[0], q[0]), kf.sub(m[1], q[1]))
    return dot(a, n) == ZERO and kf.add(dot(a, a), kf.mul(rho, dot(n, n), KK)) == ONE


def _init(pts, labels):
    _G['pts'] = pts; _G['labels'] = labels


def _confirm(chunk):
    pts, labels = _G['pts'], _G['labels']
    out = []
    for (i, j) in chunk:
        g1 = geom(pts, *labels[i]); g2 = geom(pts, *labels[j])
        ok, case = unit_nonk_pair(g1, g2)
        out.append((i, j, ok, case))
    return out


def _confirm_k(chunk):
    pts, labels = _G['pts'], _G['labels']
    kp = _G['kpts']
    out = []
    for (i, j) in chunk:
        g = geom(pts, *labels[i])
        out.append((i, j, unit_nonk_kpoint(g, kp[j])))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('extra'); ap.add_argument('out'); ap.add_argument('--workers', type=int, default=3)
    args = ap.parse_args()
    t0 = time.time()
    ex = json.loads(Path(args.extra).read_text())
    pts = load_points()
    labels = [tuple(l) for l in ex['nonk_labels']]
    cNN = [tuple(p) for p in ex['nonk_unit_pair_candidates']]
    chunks = [cNN[k:k + 2000] for k in range(0, len(cNN), 2000)]
    confirmed, cases = [], {'A': 0, 'B': 0}
    with Pool(args.workers, initializer=_init, initargs=(pts, labels)) as pool:
        for res in pool.imap_unordered(_confirm, chunks):
            for i, j, ok, case in res:
                if ok:
                    confirmed.append((i, j)); cases[case] += 1
    confirmed.sort()
    print(f'non-K candidates {len(cNN)}: exact unit pairs {len(confirmed)} (case A {cases["A"]}, case B {cases["B"]})  ({time.time()-t0:.0f}s)', flush=True)
    nb = {}
    for i, j in confirmed:
        nb.setdefault(i, set()).add(j); nb.setdefault(j, set()).add(i)
    cs = set(confirmed)
    tri = sorted((i, j, k) for i, j in confirmed for k in nb[i] & nb[j] if k > j)
    print(f'exact unit triangles among non-K points: {len(tri)}', flush=True)
    # sanity: candidates against K-points must all be non-unit
    comp = json.loads((SWAPDIR / 'completion_points.json').read_text())
    q3 = [(kf.from_strings(r['x']), kf.from_strings(r['y'])) for r in comp['points']]
    q2k = [(kf.from_strings(p['x']), kf.from_strings(p['y'])) for p in ex['q2k']]
    bad = 0
    for lst, kp in ((ex['nonk_vs_q3_candidates'], q3), (ex['nonk_vs_q2k_candidates'], q2k)):
        for i, j in lst:
            if unit_nonk_kpoint(geom(pts, *labels[i]), kp[j]):
                bad += 1
    print(f'non-K vs K-point candidates confirmed unit (must be 0): {bad}', flush=True)
    clusters = []
    for (i, j, k) in tri:
        clusters.append({'id': f'nonk:{":".join(map(str, labels[i]))}:{":".join(map(str, labels[j]))}:{":".join(map(str, labels[k]))}',
                         'labels': [list(labels[i]), list(labels[j]), list(labels[k])],
                         'points': [{'nbrs': [labels[x][0], labels[x][1]]} for x in (i, j, k)],
                         'edges': [[0, 1], [0, 2], [1, 2]]})
    out = {'candidates': len(cNN), 'unit_pairs': [[list(labels[i]), list(labels[j])] for i, j in confirmed],
           'cases': cases, 'triangles': len(tri), 'k_point_candidates_unit': bad, 'clusters': clusters}
    Path(args.out).write_text(json.dumps(out))
    print(f'wrote {args.out}  ({time.time()-t0:.0f}s)', flush=True)


if __name__ == '__main__':
    main()
