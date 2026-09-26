#!/usr/bin/env python3
"""Validate every finite obligation in PROOF.md with exact rationals and Arb."""
import argparse
from fractions import Fraction as Q
import hashlib
import json
from math import factorial
from pathlib import Path
import sys
import flint
from flint import arb, ctx

ROOT = Path(__file__).resolve().parent
P = (8, 12, 7, 15, 44, 21, 11, 23, 43)
A = ((1, 0, 1), (0, 1, 1), (-1, 0, 1), (0, -1, 1))
B = ((1, 1, 1), (-1, 1, 1), (-1, -1, 1), (1, -1, 1))
X = ((0, 0, 0),) + A + tuple(tuple(-v for v in b) for b in B)
Y = ((0, 0, 0),) + A + B
YC = tuple((x, y, z - 1) for x, y, z in Y)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def ball(q):
    q = Q(q)
    return arb(q.numerator) / q.denominator


def squared(x):
    return sum(v * v for v in x)


def distance(x, y):
    return squared(tuple(a - b for a, b in zip(x, y)))


def grid(nt, nf, equal_z=False):
    """Exact cell centroids enclosed by outward Arb balls, with exact coverage."""
    pi = arb.pi()
    cells = []
    for i in range(nt):
        if equal_z:
            zl = arb(2 * i - nt) / nt
            zh = arb(2 * i + 2 - nt) / nt
            den = zh - zl
            # Antiderivative of sqrt(1-z^2); endpoint square roots are exact.
            def primitive(z):
                return (z * (1 - z * z).sqrt() + z.asin()) / 2
            radial = (primitive(zh) - primitive(zl)) / den
            z = (zl + zh) / 2
        else:
            lo, hi = pi * i / nt, pi * (i + 1) / nt
            den = lo.cos() - hi.cos()
            radial = ((hi - lo) / 2 - ((2 * hi).sin() - (2 * lo).sin()) / 4) / den
            z = (lo.cos() + hi.cos()) / 2
        for j in range(nf):
            lo, hi = 2 * pi * j / nf, 2 * pi * (j + 1) / nf
            c = (radial * (hi.sin() - lo.sin()) / (hi - lo),
                 radial * (lo.cos() - hi.cos()) / (hi - lo), z)
            weight = den / (2 * nf)
            require(weight > 0, 'nonpositive cell weight')
            dx = tuple(sum(t * a for t, a in zip(c, x)) for x in X)
            dy = tuple(sum(t * a for t, a in zip(c, y)) for y in YC)
            cells.append((weight, c, dx, dy))
    require(sum(w for w, *_ in cells).contains(1), 'mass normalization')
    for k in range(3):
        require(sum(w * c[k] for w, c, *_ in cells).contains(0), 'centroid normalization')
    defect = sum(w * (1 - sum(t * t for t in c)) for w, c, *_ in cells)
    require(defect > 0 and defect < ball(Q(1, 269)), 'unexpected grid defect')
    return cells, defect


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--precision', type=int, default=128)
    parser.add_argument('--equal-z-grid', action='store_true',
                        help='recheck the same bounds with an independent cell geometry')
    args = parser.parse_args()
    require(args.precision >= 96, 'precision below documented minimum')
    ctx.prec = args.precision
    raw = (ROOT / 'EXPECTED.json').read_bytes()
    cert = json.loads(raw)
    require(cert['precision_bits'] == 128 and cert['lower_denominator'] == 10**6,
            'unexpected certificate format')
    require(sum(P) == 184 and min(P) == 7 and len(set(P)) == 9, 'weights')
    losses = [distance(X[i], X[j]) - distance(Y[i], Y[j])
              for i in range(9) for j in range(i)]
    require(losses.count(0) == 28 and losses.count(8) == 8, 'finite contraction')
    require(max(map(squared, X)) == 3 and max(map(squared, YC)) == 2, 'support radii')
    knots = [(Q(row['lambda']), Q(row['lower_numerator'], cert['lower_denominator']))
             for row in cert['knots']]
    require(knots[0][0] == Q(1, 4) and knots[-1][0] == 24, 'parameter coverage')
    require(all(a[0] < b[0] for a, b in zip(knots, knots[1:])), 'knot order')
    if args.equal_z_grid:
        cells, defect = grid(32, 128, equal_z=True)
    else:
        require((cert['theta_cells'], cert['phi_cells']) == (16, 64), 'grid contract')
        cells, defect = grid(16, 64)
    for lam, lower in knots:
        lam_ball = ball(lam)
        quadrature = arb(0)
        for weight, c, dx, dy in cells:
            # The common normalization log(184) cancels exactly.
            lx = sum(p * (lam_ball * x).exp() for p, x in zip(P, dx)).log()
            ly = sum(p * (lam_ball * y).exp() for p, y in zip(P, dy)).log()
            quadrature += weight * (lx - ly)
        bound = quadrature - lam_ball * lam_ball * defect
        require(bound > ball(lower), f'unverified spherical lower bound at {lam}')
    margins = [min(left[1], right[1]) - Q(3, 8) * (right[0] - left[0])**2
               for left, right in zip(knots, knots[1:])]
    require(min(margins) == Q(cert['compact_interval_margin']), 'interval margin changed')
    require(min(margins) > Q(1, 100), 'uncovered parameter interval')
    # Tail: support-function gap >=1/6, proved analytically in PROOF.md.
    require(sum(Q(399, 100)**k / factorial(k) for k in range(5)) > Q(184, 7),
            'exact exponential lower sum does not prove tail overlap')
    epsilon = Q(cert['weight_l1_radius'])
    eta = epsilon / Q(7, 184)
    require(epsilon == Q(1, 25000) and epsilon < Q(1, 4000), 'weight neighborhood')
    require(2 * eta / (1 - eta) == Q(23, 10926), 'relative mass bound')
    require(Q(1, 100) - 2 * eta / (1 - eta) > Q(1, 128), 'robust spherical gap')
    require(cert['central_variance'] == 3 * 44 * 100 == 13200, 'central variance')
    require(cert['robust_variance'] == 3 * 44 * 128 == 16896, 'robust variance')
    # Point-mass Jensen control: the integral of a linear log-MGF is zero.
    require(sum(w * sum(c) for w, c, *_ in cells).contains(0), 'point-mass control')
    digest = hashlib.sha256(raw).hexdigest()
    print('ASYMMETRIC_EVENTUAL_MAJORISATION_CERTIFICATE_PASS')
    print('certificate_sha256=' + digest)
    print(f'knots={len(knots)} intervals={len(margins)} cells={len(cells)} precision={ctx.prec}')
    print('compact_lower=' + str(min(margins)))
    print('python=' + sys.version.split()[0] + ' python-flint=' + flint.__version__)


if __name__ == '__main__':
    main()
