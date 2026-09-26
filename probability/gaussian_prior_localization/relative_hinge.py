#!/usr/bin/env python3
"""Threshold-relative Gaussian hinge intervals; see RELATIVE_HINGE.md.

All certificate arithmetic uses Python integers and Fraction.  The input is
at variance one.  Negative upper bounds certify every threshold in a window.
"""
from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction as F
from hashlib import sha256
from itertools import product
import json
from pathlib import Path

import direct_hinge as base

HERE = Path(__file__).resolve().parent
need, rat, ceilq = base.need, base.rat, base.ceilq


def centered_instance(obj, require_contraction=True):
    xg, yg, W, _, contracted = base.read_instance(obj, require_contraction)
    out = []
    for groups in (xg, yg):
        center = [F(min(v[i] for v in groups) + max(v[i] for v in groups), 2)
                  for i in range(3)]
        out.append(Counter({tuple(v[i] - center[i] for i in range(3)): w
                            for v, w in groups.items()}))
    R = max(abs(a) for groups in out for v in groups for a in v)
    return *out, W, R, contracted


def compressed_histograms(groups, W, h, M, bits):
    """Group identical coordinate tables, retaining their exact multiplicity.

    This uses equality of interval vectors across ALL atoms, not an assumed
    symmetry of a configuration. Every full lattice index is accounted for.
    """
    Q = 1 << bits
    atoms = sorted(groups.items())
    axis = []
    for k in range(3):
        table = Counter()
        for j in range(-M, M + 1):
            signature = tuple(base.exp_neg((h * j - v[k]) ** 2 / 2, bits)
                              for v, _ in atoms)
            table[signature] += 1
        axis.append(table)
    lohist, hihist = Counter(), Counter()
    divisor, widths = W * Q * Q, 0
    for (xs, nx), (ys, ny), (zs, nz) in product(*(a.items() for a in axis)):
        lo = sum(w * xs[i][0] * ys[i][0] * zs[i][0]
                 for i, (_, w) in enumerate(atoms)) // divisor
        hi_num = sum(w * xs[i][1] * ys[i][1] * zs[i][1]
                     for i, (_, w) in enumerate(atoms))
        hi = min(Q, (hi_num + divisor - 1) // divisor)
        need(0 <= lo <= hi <= Q and hi - lo <= 8, "density enclosure width")
        n = nx * ny * nz
        lohist[lo] += n
        hihist[hi] += n
        widths += n * (hi - lo)
    sites = (2 * M + 1) ** 3
    need(sum(lohist.values()) == sum(hihist.values()) == sites,
         "compressed lattice coverage failure")
    digest = sha256()
    for lh in (lohist, hihist):
        for a, n in sorted(lh.items()):
            digest.update(f"{a}:{n}\n".encode())
        digest.update(b"END\n")
    return lohist, hihist, widths, digest.hexdigest(), [len(a) for a in axis]


def ratio_max(source, target, left, right):
    """Max sum[min(target,z)-min(source,z)]/z, for ALL left<=z<=right.

    The ratio of an affine function by positive z is monotone between
    successive knots. Endpoint evaluation therefore covers the whole window.
    """
    need(0 < left <= right, "positive ordered ratio window required")
    need(all(isinstance(v, int) and v >= 0 and isinstance(n, int) and n > 0
             for hist in (source, target) for v, n in hist.items()),
         "invalid histogram")
    need(sum(source.values()) == sum(target.values()), "unequal histogram sizes")
    value = sum(n * min(F(v), left) for v, n in target.items())
    value -= sum(n * min(F(v), left) for v, n in source.items())
    slope = sum(n for v, n in target.items() if v > left)
    slope -= sum(n for v, n in source.items() if v > left)
    best, arg, prev = value / left, left, left
    knots = sorted({F(v) for hist in (source, target) for v in hist
                    if left < v < right} | {right})
    for knot in knots:
        value += slope * (knot - prev)
        trial = value / knot
        if trial > best:
            best, arg = trial, knot
        slope += source.get(knot, 0) - target.get(knot, 0)
        prev = knot
    return best, arg


def error_bound(R, h, M, umin, r, bits):
    need(R >= 0 and h > 0 and isinstance(M, int) and M >= 0,
         "invalid spatial budget")
    need(0 < umin <= 1 and r >= 0, "invalid threshold budget")
    S = (M + F(1, 2)) * h
    T = S - R
    need(T > 0, "cube must extend beyond both supports")
    Q = 1 << bits
    need(F(base.exp_neg(r * r / 2, bits)[1], Q) <= umin,
         "r does not certify exp(-r^2/2)<=umin")
    B = 4 * R * max(F(0), 4 * R * R - 1) + 4 * max(F(1), 2 * R + r)
    quad = 3 * h * h * S * S * B
    tail = 38 * F(base.exp_neg(T * T / 2, bits)[1], Q) / (T * umin)
    return quad, tail, B, S, T


def enclose_window(obj, h, tail_radius, bits, umin, umax, r,
                   require_contraction=True):
    need(isinstance(bits, int) and not isinstance(bits, bool) and bits >= 16,
         "precision must be an integer >=16")
    need(h > 0 and tail_radius > 0 and 0 < umin <= umax <= 1,
         "invalid window or grid")
    xg, yg, W, R, contracted = centered_instance(obj, require_contraction)
    M = ceilq((R + tail_radius) / h)
    quad, tail, B, S, T = error_bound(R, h, M, umin, r, bits + 12)
    xl, xu, xwidth, xhash, xcounts = compressed_histograms(xg, W, h, M, bits)
    yl, yu, ywidth, yhash, ycounts = compressed_histograms(yg, W, h, M, bits)
    Q = 1 << bits
    lo, la = ratio_max(xu, yl, umin * Q, umax * Q)
    hi, ha = ratio_max(xl, yu, umin * Q, umax * Q)
    lo, hi = h ** 3 * lo, h ** 3 * hi
    arithmetic = h ** 3 * (xwidth + ywidth) / (Q * umin)
    need(0 <= hi - lo <= arithmetic, "relative arithmetic width failure")
    lower, upper = lo - quad - tail, hi + quad + tail
    return {
        "status": "STRICT_WINDOW_SIGN" if upper < 0 else
                  "ADVERSE_THRESHOLD" if lower > 0 else "UNRESOLVED_WINDOW",
        "contraction": contracted,
        "sign_convention": "H=(source hinge)-(target hinge); divide by C*u",
        "variance": 1, "window": [str(umin), str(umax)],
        "step": str(h), "bits": bits, "support_box_radius": str(R),
        "log_radius_upper": str(r), "half_grid": M,
        "cube_half_width": str(S), "tail_radius": str(T),
        "lattice_sites_per_endpoint": (2 * M + 1) ** 3,
        "coordinate_groups": [xcounts, ycounts],
        "variation_constant": str(B), "quadrature_relative_error": str(quad),
        "tail_relative_error": str(tail),
        "discrete_relative_max_interval": [str(lo), str(hi)],
        "maximum_relative_gap_interval": [str(lower), str(upper)],
        "maximizing_lower_threshold": str(la / Q),
        "maximizing_upper_threshold": str(ha / Q),
        "arithmetic_width_upper": str(arithmetic),
        "histogram_sha256": [xhash, yhash],
    }


def controls():
    pinned = json.loads((HERE / 'RELATIVE_INPUTS.json').read_text())['dependencies']
    repo = HERE.parent.parent
    for item in pinned:
        need(sha256((repo / item['path']).read_bytes()).hexdigest() == item['sha256'],
             'pinned dependency mismatch: ' + item['path'])
    sweep = 0
    for xs in product(range(3), repeat=3):
        for ys in product(range(3), repeat=3):
            xh, yh = Counter(xs), Counter(ys)
            for a, b in [(F(1, 3), F(7, 3)), (F(1), F(2)), (F(3, 2), F(3, 2))]:
                out, arg = ratio_max(xh, yh, a, b)
                points = {a, b} | {F(x) for x in xs + ys if a <= x <= b}
                direct = max(sum(min(F(y), t) - min(F(x), t)
                                 for x, y in zip(xs, ys)) / t for t in points)
                need(out == direct and a <= arg <= b, "all-knot direct check")
                sweep += 1
    hist = 0
    cases = [Counter({(F(0),) * 3: 1}),
             Counter({(F(-1), F(0), F(0)): 1, (F(1), F(0), F(0)): 1}),
             Counter({(F(0), F(1, 3), F(-1, 4)): 2,
                      (F(2, 5), F(-1, 7), F(0)): 3})]
    for groups in cases:
        for M in [1, 2, 3]:
            compressed = compressed_histograms(groups, sum(groups.values()), F(1, 3), M, 32)
            plain = base.density_histograms(groups, sum(groups.values()), F(1, 3), M, 32)
            need(compressed[:3] == plain[:3], "full histogram comparison failed")
            hist += 1
    # Independent midpoint Peano identity, including corners inside a cell.
    peano = 0
    for c in [F(i, 8) for i in range(-8, 9)]:
        integral = (1 - c) ** 2 / 2 if c >= -1 else -2 * c
        midpoint = 2 * max(-c, F(0))
        need(abs(midpoint - integral) <= F(1, 2), "hinged midpoint Peano bound")
        peano += 1
    for R, rr in [(F(0), F(1)), (F(1, 2), F(3)), (F(1), F(61, 10))]:
        B = 4 * R * max(F(0), 4 * R * R - 1) + 4 * max(F(1), 2 * R + rr)
        need(B >= 4, "variation budget")
    rejected = 0
    bad = [lambda: ratio_max(Counter({0: 1}), Counter({0: 1}), F(0), F(1)),
           lambda: ratio_max(Counter({0: 1}), Counter({0: 2}), F(1), F(2)),
           lambda: error_bound(F(1), F(1), 0, F(1, 2), F(2), 40),
           lambda: error_bound(F(1), F(1), 4, F(1, 1024), F(1), 40)]
    for fn in bad:
        try:
            fn()
        except ValueError:
            rejected += 1
        else:
            raise ValueError("invalid control accepted")
    fixture = {"source": [[-1, 0, 0], [1, 0, 0]],
               "target": [[0, 0, 0], [0, 0, 0]], "weights": ["1/2", "1/2"]}
    signed = enclose_window(fixture, F(1, 10), F(9), 56,
                           F(1, 2 ** 26), F(1, 2 ** 24), F(61, 10))
    need(signed['status'] == 'STRICT_WINDOW_SIGN', "signed Gaussian control failed")
    need(F(signed['maximum_relative_gap_interval'][1]) < -20,
         "relative sign reserve below claimed value")
    old_quad, old_tail = base.quadrature_error(F(1, 10), F(9), 68)
    old_C_lower, _ = base.gaussian_constant(56)
    old_error_upper = (old_quad + old_tail) / (old_C_lower * F(1, 2 ** 26))
    need(old_error_upper > 1_000_000, "old-error comparison control")
    identity = {"source": [[0, 0, 0]], "target": [[0, 0, 0]], "weights": [1]}
    equality = enclose_window(identity, F(1), F(3), 32,
                             F(1, 4), F(1, 2), F(2))
    need(F(equality['maximum_relative_gap_interval'][0]) <= 0 <=
         F(equality['maximum_relative_gap_interval'][1]), "equality control")
    return {"status": "RELATIVE_HINGE_WINDOW_CERTIFICATES_PASS",
            "pinned_dependency_checks": len(pinned),
            "direct_sweep_controls": sweep, "full_histogram_controls": hist,
            "midpoint_controls": peano, "rejected_controls": rejected,
            "signed_control": signed, "identity_control": equality,
            "old_absolute_error_divided_by_C_umin_upper": str(old_error_upper)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    parser.add_argument('--expected', type=Path, default=HERE / 'RELATIVE_EXPECTED.json')
    parser.add_argument('--input', type=Path)
    parser.add_argument('--step', type=rat, default=F(1, 10))
    parser.add_argument('--tail', type=rat, default=F(9))
    parser.add_argument('--bits', type=int, default=56)
    parser.add_argument('--umin', type=rat)
    parser.add_argument('--umax', type=rat)
    parser.add_argument('--log-radius', type=rat)
    parser.add_argument('--allow-noncontraction', action='store_true')
    args = parser.parse_args()
    if args.check:
        result = controls()
        need(result == json.loads(args.expected.read_text()), "expected record mismatch")
        print(result['status'], sha256(args.expected.read_bytes()).hexdigest())
    else:
        need(args.input is not None and all(x is not None for x in
             [args.umin, args.umax, args.log_radius]), "input and window arguments required")
        result = enclose_window(json.loads(args.input.read_text()), args.step, args.tail,
                                args.bits, args.umin, args.umax, args.log_radius,
                                not args.allow_noncontraction)
        print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
