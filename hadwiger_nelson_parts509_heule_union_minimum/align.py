#!/usr/bin/env python3
"""Exact alignment of a Heule graph (CNP-SAT vtx file, coordinates in Q(sqrt3,sqrt5,sqrt11)) with the Parts 509 graph.
Candidates: origin-fixing isometries (rotation, optionally after reflection y -> -y) mapping some vertex h of H to some
vertex p of P with the same exact squared radius; float overlap count -> best candidates -> exact verification.
usage: align.py H.vtx [--top 5] [--out aligned.json]
"""
import sys, json, time, argparse
from fractions import Fraction
from pathlib import Path
import numpy as np
sys.path.insert(0, str(Path.home() / 'math_results' / 'hadwiger_nelson_parts509_criticality'))
sys.path.insert(0, str(Path.home() / 'math_results' / 'hadwiger_nelson_parts509_swap_closure'))
import parts509 as ps
import kfield as kf
PARTS = Path.home() / 'math_results' / 'hadwiger_nelson_parts509_criticality' / 'parts509.vtx'
K = 3


def fl(x):
    return kf.to_float(x, K)


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('vtx'); ap.add_argument('--top', type=int, default=5); ap.add_argument('--out')
    ap.add_argument('--reflect', action='store_true', help='also try reflections')
    args = ap.parse_args(); t0 = time.time()
    P = ps.parse_points(PARTS); H = ps.parse_points(Path(args.vtx))
    Pf = np.array([[fl(x), fl(y)] for x, y in P]); Hf = np.array([[fl(x), fl(y)] for x, y in H])
    print(f'P {len(P)} points, H {len(H)} points, parsed in {time.time()-t0:.1f}s')
    r2P = {}; r2H = {}
    for i, (x, y) in enumerate(P):
        r2P.setdefault(ps.f_add(ps.f_sq(x), ps.f_sq(y)), []).append(i)
    for i, (x, y) in enumerate(H):
        r2H.setdefault(ps.f_add(ps.f_sq(x), ps.f_sq(y)), []).append(i)
    common = [r for r in r2H if r in r2P and r != ps.ZERO]
    print(f'radius classes: P {len(r2P)}, H {len(r2H)}, common nonzero {len(common)}; origin in H: {ps.ZERO in [tuple(x) for x in []] or H[0] == (ps.ZERO, ps.ZERO)}')
    # candidate rotations (float first)
    key = lambda pt: (round(pt[0] * 1e6), round(pt[1] * 1e6))
    Pset = {}
    for i, pt in enumerate(Pf):
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                Pset.setdefault((key(pt)[0] + dx, key(pt)[1] + dy), i)
    cands = []
    seen = set()
    for r in common:
        for hi in r2H[r]:
            for pi in r2P[r]:
                for refl in ((False, True) if args.reflect else (False,)):
                    h = Hf[hi] * (np.array([1, -1]) if refl else 1); p = Pf[pi]
                    rr = float(np.dot(h, h))
                    c = (h[0] * p[0] + h[1] * p[1]) / rr; s = (h[0] * p[1] - h[1] * p[0]) / rr
                    k = (round(c * 1e7), round(s * 1e7), refl)
                    if k in seen: continue
                    seen.add(k)
                    R = np.array([[c, -s], [s, c]])
                    Hr = (Hf * (np.array([1, -1]) if refl else 1)) @ R.T
                    n = sum(1 for pt in Hr if key(pt) in Pset)
                    cands.append((n, c, s, refl, hi, pi))
    cands.sort(reverse=True)
    print(f'{len(cands)} distinct candidate isometries; top float overlaps: {[c[0] for c in cands[:10]]} ({time.time()-t0:.1f}s)')
    Pexact = {pt: i for i, pt in enumerate(P)}
    results = []
    for n, c, s, refl, hi, pi in cands[:args.top]:
        h = H[hi]; p = P[pi]
        hx, hy = h; px, py = p
        if refl: hy = kf.neg(hy)
        rr = ps.f_add(ps.f_sq(hx), ps.f_sq(hy))
        inv = kf.inv(rr, K)
        cos = kf.mul(ps.f_add(ps.f_mul(hx, px), ps.f_mul(hy, py)), inv, K)
        sin = kf.mul(ps.f_sub(ps.f_mul(hx, py), ps.f_mul(hy, px)), inv, K)
        assert ps.f_add(ps.f_sq(cos), ps.f_sq(sin)) == ps.ONE
        rot = []
        for x, y in H:
            if refl: y = kf.neg(y)
            rot.append((ps.f_sub(ps.f_mul(cos, x), ps.f_mul(sin, y)), ps.f_add(ps.f_mul(sin, x), ps.f_mul(cos, y))))
        match = [Pexact.get(pt, -1) for pt in rot]
        n_exact = sum(1 for m in match if m >= 0)
        results.append({'float_overlap': n, 'exact_overlap': n_exact, 'reflect': refl, 'cos': kf.to_strings(cos), 'sin': kf.to_strings(sin),
                        'anchor': [hi, pi], 'map_H_to_P': match, 'union_size': len(P) + len(H) - n_exact})
        print(f'  cand h={hi}->p={pi} refl={refl}: float {n}, exact {n_exact}, union {len(P)+len(H)-n_exact}')
    if args.out:
        best = results[0]
        n, c, s, refl, hi, pi = cands[0]
        rot_strs = None
        # store aligned exact coordinates of H for the best candidate
        h = H[hi]; p = P[pi]; hx, hy = h; px, py = p
        if refl: hy = kf.neg(hy)
        inv = kf.inv(ps.f_add(ps.f_sq(hx), ps.f_sq(hy)), K)
        cos = kf.mul(ps.f_add(ps.f_mul(hx, px), ps.f_mul(hy, py)), inv, K)
        sin = kf.mul(ps.f_sub(ps.f_mul(hx, py), ps.f_mul(hy, px)), inv, K)
        rot = []
        for x, y in H:
            if refl: y = kf.neg(y)
            rot.append([kf.to_strings(ps.f_sub(ps.f_mul(cos, x), ps.f_mul(sin, y))), kf.to_strings(ps.f_add(ps.f_mul(sin, x), ps.f_mul(cos, y)))])
        json.dump({'vtx': args.vtx, 'best': best, 'aligned_H': rot, 'all': results}, open(args.out, 'w'))
        print('wrote', args.out)


if __name__ == '__main__':
    main()
