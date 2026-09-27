#!/usr/bin/env python3
"""Compressed exact schedules for EFFECTIVE.md; no Gaussian sign sampling.

The supplied radius and covariance are premises until check_input verifies
finite rational data. Passing the guard signs the stated volume/threshold
range, not all thresholds. Author theorem: independent review pending.
"""
import argparse
from fractions import Fraction as F
from itertools import combinations
import json
from math import isqrt
from pathlib import Path


def need(condition, message):
    if not condition:
        raise ValueError(message)


def rational(value):
    need(type(value) in (int, str, F), 'use exact integers, strings or Fractions')
    return F(value)


def ceiling(value):
    return -(-value.numerator // value.denominator)


def floor_log2(value):
    value = rational(value)
    need(value > 0, 'logarithm argument must be positive')
    n, d = value.numerator, value.denominator
    k = n.bit_length() - d.bit_length()
    below = n < (d << k) if k >= 0 else (n << -k) < d
    return k-1 if below else k


def ceil_log2(value):
    return -floor_log2(1/rational(value))


def schedule(radius, covariance_floor, volume_radius):
    R, k, r = map(rational, (radius, covariance_floor, volume_radius))
    need(R > 0 and k > 0 and r > 0, 'positive radius, covariance and volume radius')
    need(3*k <= R*R, 'nonempty centered radius/covariance class requires 3 kappa <= R^2')
    e0 = ceiling((r+R)**2/2+(r+3*R)**2)
    eb = ceiling((r+R)**2/2+(r+4*R)**2+2*R**2)
    ep = ceiling((r+6*R)**2/2)
    eg = ceiling((r+4*R)**2+(r+R)**2)
    ew = ceiling((r+R)**2)
    a0, ab = 6+2*e0, 7+2*eb
    k0, k1 = ceil_log2(2*R**2/k), ceil_log2(16*R/k)
    k2 = ceil_log2(2*R)+2*ew
    ell = ceil_log2(96*R**3/k+6*R)
    A = max(1, -floor_log2(k/(8*R**2)),
            2*ep-floor_log2(k/(16*R)),
            2*eg-floor_log2(k/(48*R**2)))
    h = max(a0, ab+3)
    t2 = max(0, -floor_log2(R), h+2+k1)
    t1 = max(t2+1, 2*t2+ceil_log2(12*R),
             2*t2-floor_log2(k/(576*R**3)),
             ab+2*t2-floor_log2(k/(48*R**2)))
    j = 1+max(-1, ceil_log2(12*R**2)+k0+2*t1)
    constraints = [ceil_log2(8*R**4/k**3), A+2*t1+k0,
                   t2+j-floor_log2(k/(16*R)),
                   h+4*t2+3+2*ell+2*k0,
                   2*h+4*t2+6+2*k2+3*k0]
    return {
        'status': 'EFFECTIVE_MEAN_LOSS_SCHEDULE',
        'radius': str(R), 'covariance_floor': str(k), 'volume_radius': str(r),
        'loss_cutoff_neglog2': max(0, *constraints),
        'margin_neglog2': h+1,
        'budgets': {'gaussian_exponent_ceilings': [e0, eb, ep, eg, ew],
                    'c0_neglog2': a0, 'one_point_neglog2': ab,
                    'K0_log2': k0, 'K1_log2': k1, 'K2_log2': k2,
                    'L_log2': ell, 'rare_mass_neglog2': A,
                    'core_margin_neglog2': h, 'bulk_scale_neglog2': t2,
                    'anchor_scale_neglog2': t1, 'sum_upper_log2': j,
                    'loss_constraint_exponents': constraints},
        'scope': 'If normalized mean pair loss D <= 2^-N, actual aligned source-top-set gain >= 2^-M v D for 0 < v <= (4 pi/3) r^3 in Gaussian-normalized coordinates.',
        'review': 'Author proof; independent review pending.',
    }


def threshold_schedule(radius, covariance_floor, threshold_bits):
    need(type(threshold_bits) is int and threshold_bits >= 1, 'positive integer threshold bits')
    R = rational(radius)
    root = isqrt(2*threshold_bits)
    if root*root < 2*threshold_bits:
        root += 1
    record = schedule(R, covariance_floor, R+root)
    record['threshold_left_neglog2'] = threshold_bits
    record['threshold_scope'] = 'Every hinge with normalized threshold u >= 2^-threshold_left_neglog2 is nonnegative when the loss guard passes.'
    return record


def verify_schedule(record):
    need(isinstance(record, dict), 'schedule must be an object')
    if 'threshold_left_neglog2' in record:
        expected = threshold_schedule(record.get('radius'), record.get('covariance_floor'),
                                      record['threshold_left_neglog2'])
    else:
        expected = schedule(record.get('radius'), record.get('covariance_floor'),
                            record.get('volume_radius'))
    need(record == expected, 'schedule contents differ from the proved construction')
    return True


def dot(x, y):
    return sum((a*b for a, b in zip(x, y)), F(0))


def sub(x, y):
    return tuple(a-b for a, b in zip(x, y))


def determinant(matrix):
    if len(matrix) == 1:
        return matrix[0][0]
    return sum(((-1)**j*matrix[0][j]*determinant(
        [[row[k] for k in range(len(matrix)) if k != j] for row in matrix[1:]])
        for j in range(len(matrix))), F(0))


def check_input(record, sources, targets, weights, variance=1):
    """Validate a finite rational input; UNRESOLVED means only guard failure."""
    verify_schedule(record)
    need(isinstance(sources, (list, tuple)) and isinstance(targets, (list, tuple)), 'coordinate arrays')
    need(len(sources) == len(targets) == len(weights) and len(weights) > 0, 'matching nonempty labels')
    need(all(len(x) == 3 for x in list(sources)+list(targets)), 'three-dimensional coordinates')
    xs = [tuple(map(rational, x)) for x in sources]
    ys = [tuple(map(rational, y)) for y in targets]
    ws = list(map(rational, weights))
    s = rational(variance)
    need(s > 0 and all(w >= 0 for w in ws) and sum(ws) == 1, 'positive variance and probability weights')
    active = [i for i, w in enumerate(ws) if w]
    xs, ys, ws = [xs[i] for i in active], [ys[i] for i in active], [ws[i] for i in active]
    n = len(ws)
    mean_x = tuple(sum((w*x[j] for w, x in zip(ws, xs)), F(0)) for j in range(3))
    centered = [sub(x, mean_x) for x in xs]
    R, k = F(record['radius']), F(record['covariance_floor'])
    need(all(dot(x, x) <= s*R*R for x in centered), 'source radius exceeds the premise')
    cov = [[sum((w*x[i]*x[j] for w, x in zip(ws, centered)), F(0))/s
            -(k if i == j else 0) for j in range(3)] for i in range(3)]
    for size in range(1, 4):
        for ids in combinations(range(3), size):
            need(determinant([[cov[i][j] for j in ids] for i in ids]) >= 0,
                 'source covariance below the premise')
    D = F(0)
    for i in range(n):
        for j in range(i):
            dx, dy = sub(xs[i], xs[j]), sub(ys[i], ys[j])
            loss = dot(dx, dx)-dot(dy, dy)
            need(loss >= 0, 'labelled pair expands')
            D += 2*ws[i]*ws[j]*loss/s
    if D == 0:
        status = 'ISOMETRIC_ZERO'
    elif ceil_log2(D) <= -record['loss_cutoff_neglog2']:
        status = 'SIGNED_BOUNDED_VOLUME'
    else:
        status = 'UNRESOLVED'
    return {'status': status, 'normalized_loss': str(D),
            'loss_ceil_log2': None if D == 0 else ceil_log2(D),
            'loss_cutoff_neglog2': record['loss_cutoff_neglog2'],
            'margin_neglog2': record['margin_neglog2'],
            'volume_radius': record['volume_radius'],
            'threshold_left_neglog2': record.get('threshold_left_neglog2'),
            'scope': 'Only the stated volume range, plus the stated threshold range when present. No full-majorisation decision is made.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--radius', required=True)
    parser.add_argument('--covariance', required=True)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--volume-radius')
    group.add_argument('--threshold-bits', type=int)
    parser.add_argument('--input', type=Path, help='JSON sources, targets, weights, optional variance; all exact strings or integers')
    args = parser.parse_args()
    record = (schedule(args.radius, args.covariance, args.volume_radius)
              if args.volume_radius is not None else
              threshold_schedule(args.radius, args.covariance, args.threshold_bits))
    if args.input is not None:
        data = json.loads(args.input.read_text())
        result = check_input(record, data['sources'], data['targets'], data['weights'], data.get('variance', 1))
        print(json.dumps({'schedule': record, 'input_check': result}, indent=2, sort_keys=True))
    else:
        print(json.dumps(record, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
