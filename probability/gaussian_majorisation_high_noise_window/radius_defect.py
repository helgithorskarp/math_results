"""Exact consumer of SMALL_RADIUS_DEFECT.md; no floating-point sign decisions."""
import argparse
from fractions import Fraction as F
import json
from math import comb, factorial
from pathlib import Path


def require(condition, message):
    if not condition:
        raise ValueError(message)


def rational(value):
    require(type(value) in (str, int) or isinstance(value, F),
            'Use integer or string rational input, not floating point')
    return F(value)


def radius_certificate(radius_squared, variance=1):
    r2, s = rational(radius_squared), rational(variance)
    require(r2 >= 0 and s > 0, 'Nonnegative radius and positive variance required')
    if r2 == 0:
        k = None
        bound = {'numerator': '0', 'denominator': '1', 'binary_exponent': 0}
        reason = 'Point support: exact equality'
    else:
        k = s // (8 * r2)
        if k >= 2:
            bound = {'numerator': str(k), 'denominator': '1',
                     'binary_exponent': 4 - 5 * k}
            reason = 'Exponential support-radius defect bound'
        else:
            bound = {'numerator': '7', 'denominator': '50', 'binary_exponent': 0}
            reason = 'Accepted uniform defect bound; radius rule not stronger'
    return {'schema': 'gaussian_radius_defect_v1', 'radius_squared': str(r2),
            'variance': str(s), 'epsilon': str(r2 / s), 'k': k,
            'defect_upper_bound': bound, 'reason': reason,
            'covers': ['every density threshold', 'every beta degree and index',
                       'every finite Hankel matrix after adding E times its monomial Gram matrix'],
            'exact_majorisation_certified': r2 == 0,
            'geometric_radius_is_supplied_input': True}


def tolerance_certificate(bits):
    require(type(bits) is int and bits >= 0, 'Nonnegative integer bit budget required')
    k = 1 + (bits + 3) // 4
    return {'schema': 'gaussian_radius_tolerance_v1', 'bits': bits, 'k': k,
            'sufficient_radius_squared_over_variance': str(F(1, 8 * k)),
            'requested_upper_bound': {'numerator': '1', 'denominator': '1',
                                      'binary_exponent': -bits},
            'radius_rule_bound': {'numerator': str(k), 'denominator': '1',
                                  'binary_exponent': 4 - 5 * k},
            'integer_budget_check': 4 - 4 * k <= -bits,
            'proof_of_unexpanded_comparison': 'k<=2^k for every integer k>=1'}


def distance_squared(a, b):
    return sum((x - y) ** 2 for x, y in zip(a, b))


def instance_certificate(data, variance=None):
    require(isinstance(data, dict), 'Input must be an object')
    points = []
    for field in ['source', 'target']:
        raw = data.get(field)
        require(isinstance(raw, list) and raw, 'Nonempty source/target arrays required')
        require(all(isinstance(v, list) and len(v) == 3 for v in raw),
                'Every point must have three coordinates')
        points.append([tuple(rational(x) for x in v) for v in raw])
    x, y = points
    raw_weights = data.get('weights')
    require(isinstance(raw_weights, list), 'Probability weights required')
    w = [rational(v) for v in raw_weights]
    require(len(x) == len(y) == len(w), 'Source, target and weight sizes differ')
    require(all(v >= 0 for v in w) and sum(w) == 1, 'Invalid probability weights')
    s = rational(data.get('variance', 1) if variance is None else variance)
    require(s > 0, 'Variance must be positive')
    n = len(x)
    for i in range(n):
        for j in range(i):
            require(distance_squared(y[i], y[j]) <= distance_squared(x[i], x[j]),
                    'Input is not a contraction')
    active = [i for i in range(n) if w[i] > 0]
    r2, anchor = min((max(distance_squared(x[i], x[j]) for j in active), i)
                     for i in active)
    target_r2 = max(distance_squared(y[anchor], y[j]) for j in active)
    require(target_r2 <= r2, 'Checked contraction did not retain the anchor radius')
    answer = radius_certificate(r2, s)
    answer.update({'geometric_radius_is_supplied_input': False,
                   'labels': n, 'active_labels': len(active), 'source_anchor_index': anchor,
                   'target_radius_squared': str(target_r2),
                   'pair_contractions_checked': n * (n - 1) // 2,
                   'radius_method': 'minimum over active source-site anchors; not a minimum enclosing ball'})
    return answer


def expanded_bound(record):
    """Small-control helper only; production output always stays compressed."""
    b = record['defect_upper_bound']
    e = b['binary_exponent']
    require(abs(e) <= 10000, 'Control expansion limit exceeded')
    value = F(int(b['numerator']), int(b['denominator']))
    return value * (2 ** e if e >= 0 else F(1, 2 ** (-e)))


def exact_rank(rows):
    a = [[F(v) for v in row] for row in rows]
    rank = 0
    for column in range(len(a[0])):
        pivot = next((i for i in range(rank, len(a)) if a[i][column]), None)
        if pivot is None:
            continue
        a[rank], a[pivot] = a[pivot], a[rank]
        divisor = a[rank][column]
        a[rank] = [v / divisor for v in a[rank]]
        for i in range(rank + 1, len(a)):
            c = a[i][column]
            a[i] = [v - c * q for v, q in zip(a[i], a[rank])]
        rank += 1
        if rank == len(a):
            break
    return rank


def check():
    # Independently expanded shell polynomial and cleared cutoff identity.
    shell = {(3 - j, j): comb(3, j) * (1 - (-1) ** j)
             for j in range(4) if j % 2}
    require(shell == {(2, 1): 6, (0, 3): 2}, 'Shell cancellation failed')
    left = [16, -40, 25]
    right = [16, -16 - 24, 24 + 1]
    require(left == right, 'Cleared cutoff identity failed')
    require(F(16 ** 2, 2 ** 3) == F(8 ** 2, 2), 'Squared normalization failed')
    exp_lower = sum(F(4) ** j / factorial(j) for j in range(5))
    exp_upper = 1 + F(3, 4) + F(9, 32) / (1 - F(1, 4))
    require(exp_lower == F(103, 3) and exp_lower > 32, 'exp(4) premise failed')
    require(exp_upper == F(17, 8), 'exp(3/4) upper premise failed')
    prefactor = 4 * F(3, 8) * F(17, 8) * F(205, 48)
    require(prefactor == F(3485, 256) and prefactor < 16, 'Rational prefactor failed')
    for k in range(1, 129):
        require(k <= 2 ** k, 'Integer power comparison failed')
        require(4 * k + F(1, 4) + F(1, 48 * k) <= F(205, 48) * k,
                'Scalar bracket bound failed')
        if k >= 2:
            cert = radius_certificate(F(1, 8 * k))
            require(expanded_bound(cert) == 16 * k * F(1, 2 ** (5 * k)),
                    'Compressed radius result failed')
            require(expanded_bound(cert) < F(7, 50), 'Fallback comparison failed')
    for bits in range(129):
        cert = tolerance_certificate(bits)
        k = cert['k']
        require(16 * k * F(1, 2 ** (5 * k)) <= F(1, 2 ** bits),
                'Requested tolerance failed')
        require(cert['integer_budget_check'], 'Budget exponent failed')
    # Actual admissible paired-rank-six fold, credited to R2 and rescaled.
    source = [[F(0)] * 3]
    for axis in range(3):
        for sign in [1, -1]:
            row = [F(0)] * 3
            row[axis] = F(sign, 8)
            source.append(row)
    target = [[abs(v) for v in row] for row in source]
    fixture = {'source': source, 'target': target,
               'weights': [F(i, 28) for i in range(1, 8)]}
    control = instance_certificate(fixture)
    rank = exact_rank([source[i] + target[i] for i in range(1, 7)])
    require(rank == 6 and control['k'] == 8, 'Rank-six control failed')
    require(expanded_bound(control) == F(1, 2 ** 33), 'Rank-six defect bound failed')
    # Zero masses must not enlarge the support radius, while invalid maps still fail.
    zero = instance_certificate({'source': [[0, 0, 0], [100, 0, 0]],
                                 'target': [[3, 0, 0], [3, 0, 0]], 'weights': [1, 0]})
    require(zero['exact_majorisation_certified'] and zero['active_labels'] == 1,
            'Zero-mass support reduction failed')
    translation = [F(3), F(-5), F(2)]
    moved = {'source': [[v + z for v, z in zip(row, translation)] for row in source],
             'target': [[v - z for v, z in zip(row, translation)] for row in target],
             'weights': fixture['weights']}
    require(instance_certificate(moved)['defect_upper_bound'] == control['defect_upper_bound'],
            'Independent translation invariance failed')
    scale = {'source': [[3 * v for v in row] for row in source],
             'target': [[3 * v for v in row] for row in target],
             'weights': fixture['weights'], 'variance': 9}
    require(instance_certificate(scale)['defect_upper_bound'] == control['defect_upper_bound'],
            'Variance/space scaling failed')
    huge = tolerance_certificate(1000000)
    require(huge['k'] == 250001 and huge['radius_rule_bound']['binary_exponent'] == -1250001,
            'Large compressed budget failed')
    require(len(json.dumps(huge)) < 600, 'Large budget accidentally expanded')
    invalid = [
        lambda: radius_certificate(-1), lambda: radius_certificate(1, 0),
        lambda: tolerance_certificate(-1), lambda: tolerance_certificate(True),
        lambda: radius_certificate(0.1),
        lambda: instance_certificate({'source': [[0, 0, 0]], 'target': [[0, 0, 0]], 'weights': [2]}),
        lambda: instance_certificate({'source': [[0, 0, 0], [0, 0, 0]],
                                      'target': [[0, 0, 0], [1, 0, 0]], 'weights': ['1/2', '1/2']}),
        lambda: instance_certificate({'source': target, 'target': source, 'weights': fixture['weights']}),
        lambda: instance_certificate({'source': [[0, 0]], 'target': [[0, 0, 0]], 'weights': [1]}),
        lambda: instance_certificate({'source': [[0, 0, 0], [1, 0, 0]],
                                      'target': [[0, 0, 0], [0, 0, 0]], 'weights': [-1, 2]}),
    ]
    for call in invalid:
        try:
            call()
        except ValueError:
            continue
        raise ValueError('Malformed-input control was accepted')
    return {'status': 'EXPONENTIAL_RADIUS_DEFECT_CERTIFICATES_PASS',
            'shell_polynomial': [[*key, value] for key, value in sorted(shell.items())],
            'cutoff_polynomial': left, 'exp4_lower': str(exp_lower),
            'exp_three_quarters_upper': str(exp_upper), 'prefactor_upper': str(prefactor),
            'small_radius_parameters_checked': 128, 'small_bit_budgets_checked': 129,
            'malformed_inputs_rejected': len(invalid), 'paired_rank': rank,
            'rank_six_control': control, 'million_bit_budget': huge,
            'table': [radius_certificate(F(1, 8 * k)) for k in [1, 2, 4, 8, 16]]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--check', action='store_true')
    group.add_argument('--bits', type=int)
    group.add_argument('--radius-squared')
    group.add_argument('--input', type=Path)
    parser.add_argument('--variance')
    args = parser.parse_args()
    if args.check:
        answer = check()
        expected = Path(__file__).with_name('RADIUS_EXPECTED.json')
        require(expected.exists(), 'Missing pinned expected record')
        require(answer == json.loads(expected.read_text()), 'Expected-record mismatch')
    elif args.bits is not None:
        require(args.variance is None, '--bits gives a dimensionless radius ratio')
        answer = tolerance_certificate(args.bits)
    elif args.input:
        answer = instance_certificate(json.loads(args.input.read_text()), args.variance)
    else:
        answer = radius_certificate(args.radius_squared, args.variance or '1')
    print(json.dumps(answer, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
