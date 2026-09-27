#!/usr/bin/env python3
"""Exact covariance-boundary guard; its analytic theorem is in PROOF.md.

No eigenvector, extension of the map, or Gaussian integration is computed.
A failed sufficient guard is unresolved, never a counterexample.
"""
import argparse
from fractions import Fraction as F
import json
from math import isqrt
from pathlib import Path


def need(condition, message):
    if not condition:
        raise ValueError(message)


def rational(value):
    need(type(value) in (int, str, F), 'exact integers, strings or Fractions required')
    return F(value)


def floor_log2(value):
    value = rational(value)
    need(value > 0, 'positive logarithm argument required')
    n, d = value.numerator, value.denominator
    k = n.bit_length()-d.bit_length()
    below = n < d << k if k >= 0 else n << -k < d
    return k-1 if below else k


def ceil_log2(value):
    return -floor_log2(1/rational(value))


def schedule(radius, threshold_bits, loss_floor_bits):
    R, m, k = radius, threshold_bits, loss_floor_bits
    need(all(type(x) is int for x in (R, m, k)), 'integer schedule parameters required')
    need(R >= 1 and m >= 1 and k >= 0, 'require R>=1, m>=1, k>=0')
    q = isqrt(2*(m+1))
    q += q*q < 2*(m+1)
    B = 31+47*R*R+2*(2*R+q)**2+5*k
    return {
        'status': 'COVARIANCE_BOUNDARY_SCHEDULE',
        'radius': R, 'threshold_neglog2': m, 'loss_floor_neglog2': k,
        'root_ceiling': q, 'peak_gap_neglog2': k+4+9*R*R,
        'reference_margin_neglog2': B,
        'projection_error_neglog2': B+2,
        'directional_variance_ceiling_neglog2': 2*B+4,
        'hinge_margin_neglog2': B+1,
        'scope': 'At unit variance, D>=2^-k and either marginal directional covariance<=2^-L sign all u>=2^-m. The margin applies at thresholds no higher than the actual source peak.',
        'review': 'Author proof; independent review pending.',
    }


def verify_schedule(record):
    need(isinstance(record, dict), 'schedule object required')
    expected = schedule(record.get('radius'), record.get('threshold_neglog2'),
                        record.get('loss_floor_neglog2'))
    need(record == expected, 'schedule differs from the proved formula')


def dot(x, y):
    return sum((a*b for a, b in zip(x, y)), F(0))


def sub(x, y):
    return tuple(a-b for a, b in zip(x, y))


def mean(points, weights):
    return tuple(sum((p*x[j] for p, x in zip(weights, points)), F(0))
                 for j in range(3))


def finite_guard(record, sources, targets, weights, direction, variance=1, side='source'):
    verify_schedule(record)
    need(side in ('source', 'target'), 'side must be source or target')
    need(isinstance(sources, (list, tuple)) and isinstance(targets, (list, tuple)), 'coordinate lists required')
    need(isinstance(weights, (list, tuple)), 'weight list required')
    need(len(sources) == len(targets) == len(weights) > 0, 'matching nonempty labels required')
    need(all(isinstance(x, (list, tuple)) and len(x) == 3
             for x in list(sources)+list(targets)), 'three-dimensional coordinates required')
    need(isinstance(direction, (list, tuple)) and len(direction) == 3, 'direction has three coordinates')
    xs = [tuple(map(rational, x)) for x in sources]
    ys = [tuple(map(rational, y)) for y in targets]
    ps = list(map(rational, weights))
    n = tuple(map(rational, direction))
    s = rational(variance)
    need(s > 0 and dot(n, n) > 0, 'positive variance and nonzero direction required')
    need(all(p >= 0 for p in ps) and sum(ps) == 1, 'probability weights required')
    active = [i for i, p in enumerate(ps) if p]
    xs, ys, ps = [xs[i] for i in active], [ys[i] for i in active], [ps[i] for i in active]
    mx, my = mean(xs, ps), mean(ys, ps)
    xc, yc = [sub(x, mx) for x in xs], [sub(y, my) for y in ys]
    R = record['radius']
    need(all(dot(x, x) <= s*R*R for x in xc), 'centered source radius exceeds its bound')
    D = F(0)
    for i in range(len(ps)):
        for j in range(i):
            dx, dy = sub(xs[i], xs[j]), sub(ys[i], ys[j])
            loss = dot(dx, dx)-dot(dy, dy)
            need(loss >= 0, 'an active pair expands')
            D += 2*ps[i]*ps[j]*loss/s
    D_variance = 2*sum((p*(dot(x, x)-dot(y, y))
                        for p, x, y in zip(ps, xc, yc)), F(0))/s
    need(D == D_variance, 'pair and variance loss identity failed')
    cloud = xc if side == 'source' else yc
    lam = sum((p*dot(n, x)**2 for p, x in zip(ps, cloud)), F(0))/(s*dot(n, n))
    if D == 0:
        status = 'ISOMETRIC_ZERO'
    elif lam == 0:
        status = 'PLANAR_FULL_MAJORISATION'
    elif (floor_log2(D) >= -record['loss_floor_neglog2'] and
          ceil_log2(lam) <= -record['directional_variance_ceiling_neglog2']):
        status = 'SIGNED_ABOVE_THRESHOLD'
    else:
        status = 'UNRESOLVED'
    return {
        'status': status, 'side': side, 'normalized_mean_loss': str(D),
        'normalized_directional_variance': str(lam),
        'loss_floor_log2': None if D == 0 else floor_log2(D),
        'directional_variance_ceil_log2': None if lam == 0 else ceil_log2(lam),
        'threshold_neglog2': record['threshold_neglog2'],
        'hinge_margin_neglog2': record['hinge_margin_neglog2'] if status == 'SIGNED_ABOVE_THRESHOLD' else None,
        'scope': 'The new sign covers only u>=2^-m; its margin is through the source peak. The planar and isometric branches are credited prior full comparisons.',
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--radius', type=int, required=True)
    parser.add_argument('--threshold-bits', type=int, required=True)
    parser.add_argument('--loss-floor-bits', type=int, required=True)
    parser.add_argument('--input', type=Path, help='JSON: sources, targets, weights, direction, optional variance and side; exact strings or integers')
    args = parser.parse_args()
    record = schedule(args.radius, args.threshold_bits, args.loss_floor_bits)
    if args.input is None:
        result = record
    else:
        data = json.loads(args.input.read_text())
        result = {'schedule': record, 'input_check': finite_guard(
            record, data['sources'], data['targets'], data['weights'],
            data['direction'], data.get('variance', 1), data.get('side', 'source'))}
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
