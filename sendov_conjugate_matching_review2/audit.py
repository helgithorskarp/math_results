"""Independent exact audit and denominator1600 refinement.

No target code or target output imported. Python>=3.11, standard library.
"""
from fractions import Fraction as Q
from itertools import permutations
from math import comb, factorial
from pathlib import Path
import argparse
import hashlib
import json

from algebra import identities
from intervals import I, norm, example_reciprocals, costs, BITS


def require(ok, message):
    if not ok:
        raise ValueError(message)


def integrate(n, c, power):
    # Coefficients of (1+ct)^n built by repeated list convolution.
    polynomial = [Q(1)]
    for _ in range(n):
        new = [Q(0)]*(len(polynomial)+1)
        for i, x in enumerate(polynomial):
            new[i] += x
            new[i+1] += c*x
        polynomial = new
    return sum(x/Q(i+power+1) for i, x in enumerate(polynomial))


def constants():
    old1 = 9*integrate(7, Q(8, 7), 1)
    old2 = 72*integrate(6, Q(4, 3), 2)
    require(old1 == Q(570801247, 1647086), 'original K1')
    require(old2 == Q(9598808, 5103), 'original K2')
    require(old1+old2 < 2250, 'original uniform loss')
    As = 9*integrate(7, Q(15, 14), 1)
    Ap = Q(9, 2)*(integrate(6, Q(7, 6), 1)+integrate(6, Q(7, 6), 2))
    Css = 9*integrate(6, Q(7, 6), 2)
    Csp = 36*integrate(5, Q(13, 10), 2)
    Cpp = 144*integrate(4, Q(3, 2), 2)
    B = Ap/4+3*Cpp/8
    require(As >= Css/2, 'singleton aggregation')
    require(Ap < Cpp/2, 'pair aggregation')
    require(As < B and Csp < 2*B and B < 450, 'mixed uniform loss')
    require(B == Q(46880404327, 104509440), 'exact new loss constant')
    margin = Q(9, 32)-B/1600
    require(margin > 0, 'weak1600 boundary has strict margin')
    result = {key: str(value) for key, value in
            {'old_K1': old1, 'old_K2': old2, 'A_single': As, 'A_pair': Ap,
             'C_single_single': Css, 'C_single_pair': Csp, 'C_pair_pair': Cpp,
             'B_uniform': B, 'retained_margin_1600': margin,
             'squared_budget_factor': Q(9000, 1600), 'new_denominator': Q(1600)}.items()}
    rows = []
    for p, denominator in enumerate((1000, 1000, 1300, 1500, 1600)):
        coefficient = As if p == 0 else max(As, Ap/p+Cpp*Q(p-1, 2*p))
        require(Csp <= 2*coefficient, 'mixed count-dependent aggregation')
        require(coefficient < Q(9*denominator, 32), 'count-dependent criterion')
        rows.append({'pairs': p, 'loss_coefficient': str(coefficient), 'denominator': denominator,
                     'strict_margin': str(Q(9, 32)-coefficient/denominator)})
    result['pair_count_criteria'] = rows
    return result


def involutions(n):
    """Enumerate independently as order-at-most-two permutations."""
    for permutation in permutations(range(n)):
        if all(permutation[permutation[i]] == i for i in range(n)):
            yield tuple((i,) if j == i else (i, j)
                        for i, j in enumerate(permutation) if j >= i)


def value(partition, singles, pairs):
    return sum((singles[g[0]] if len(g) == 1 else pairs[g] for g in partition), Q(0))


def edge_dp(singles, pairs):
    """Minimum disjoint edge set, with singleton costs as the baseline.

    Process edges in fixed order. This is a different recurrence from the
    target's least-unassigned-index subset recursion.
    """
    states = {0: Q(0)}
    for (i, j), c in sorted(pairs.items()):
        used = (1 << i) | (1 << j)
        new = states.copy()
        for mask, cost in states.items():
            if not mask & used:
                next_mask = mask | used
                candidate = cost+c-singles[i]-singles[j]
                if next_mask not in new or candidate < new[next_mask]:
                    new[next_mask] = candidate
        states = new
    return sum(singles, Q(0))+min(states.values())


def matching_checks():
    all_partitions = list(involutions(8))
    counts = {k: sum(sum(len(g) == 2 for g in p) == k for p in all_partitions) for k in range(5)}
    require(counts == {0: 1, 1: 28, 2: 210, 3: 420, 4: 105}, 'partition distribution')
    require(len(set(all_partitions)) == len(all_partitions) == 764, 'unique complete partition census')
    for n in range(9):
        require(len(list(involutions(n))) == sum(factorial(n)//(2**k*factorial(k)*factorial(n-2*k))
                                              for k in range(n//2+1)), 'small partition census')
    minima = []
    for seed in (2, 11, 37, 101):
        singles = [Q((seed+7*i*i)%29, i+1) for i in range(8)]
        pairs = {(i, j): Q((seed+5*i*j+3*j*j)%41, i+j+1) for i in range(8) for j in range(i+1, 8)}
        exhaustive = min(value(p, singles, pairs) for p in all_partitions)
        require(edge_dp(singles, pairs) == exhaustive, 'independent matching algorithms disagree')
        minima.append(str(exhaustive))
    h = hashlib.sha256(json.dumps(all_partitions, separators=(',', ':')).encode()).hexdigest()
    return all_partitions, {'partitions': 764, 'counts_by_pairs': counts, 'cost_tables': 4,
                            'exact_minima': minima, 'partition_sha256': h}


def example(epsilon, partitions):
    q = example_reciprocals(epsilon)
    singles, pairs = costs(q)
    low_s, up_s = [x.lo for x in singles], [x.hi for x in singles]
    low_p, up_p = {k: x.lo for k, x in pairs.items()}, {k: x.hi for k, x in pairs.items()}
    low = min(value(p, low_s, low_p) for p in partitions)
    up, witness = min((value(p, up_s, up_p), p) for p in partitions)
    require(edge_dp(low_s, low_p) == low and edge_dp(up_s, up_p) == up,
            'interval matching endpoints not independently confirmed')
    a, t, eps = Q(9, 10), Q(99, 100), Q(epsilon)
    require(0 < eps < Q(1, 100) and t+eps < 1, 'original roots in disk')
    old, new = (1-a)/9000, (1-a)/1600
    angular = sum((norm(x, y)-x).lo for x, y in q)
    singleton_sum = sum(low_s, Q(0))
    root_product = (a*a+(t-eps)**2)**4
    require(root_product > 9, 'example outside other-root product criterion')
    require(angular > (1-a)/2400, 'example outside positive-axis angular criterion')
    result = {'epsilon': str(eps), 'M_star_interval': [str(low), str(up)],
            'M_star_squared_interval': [str(low*low), str(up*up)],
            'old_squared_threshold': str(old), 'new_squared_threshold': str(new),
            'satisfies_original_9000': up*up <= old, 'fails_original_9000': low*low > old,
            'satisfies_new_1600': up*up <= new, 'upper_bound_attaining_partition': witness,
            'root_product_lower': str(root_product), 'angular_loss_lower': str(angular),
            'singleton_defect_squared_lower': str(singleton_sum*singleton_sum),
            'prior_positive_axis_squared_threshold': str((1-a)/1250),
            'principal_sqrt_branch': 'positive real part; discriminant real part positive',
            'reciprocal_coordinates': [[x.output(), y.output()] for x, y in q]}
    require(singleton_sum*singleton_sum > (1-a)/1250, 'outside prior positive-axis criterion')
    if eps == Q(1, 1600):
        require(Q(56, 10000) < low <= up < Q(57, 10000), 'simple separating interval')
        result['simple_M_star_interval'] = ['7/1250', '57/10000']
    return result


def interval_controls():
    require(I(-2, 3).square().output() == ['0', '9'], 'zero-crossing square')
    require(I(-3, -2).square().output() == ['4', '9'], 'negative square')
    require((I(1, 2)*I(-3, 4)).output() == ['-6', '8'], 'mixed multiplication')
    for q in (Q(0), Q(1), Q(2), Q(1, 3), Q(49, 25)):
        r = I(q).sqrt()
        require(r.lo*r.lo <= q <= r.hi*r.hi, 'sqrt outward control')
    require(norm(3, 4).output() == ['5', '5'], 'rational norm exact')
    return 9


def run():
    algebra = identities()
    constants_output = constants()
    parts, matching = matching_checks()
    controls = interval_controls()
    original = example(Q(1, 50000), parts)
    separating = example(Q(1, 1600), parts)
    require(original['satisfies_original_9000'], 'original example criterion')
    require(separating['fails_original_9000'] and separating['satisfies_new_1600'], 'strict criterion separation')
    rejects = 0
    for check in [lambda: require(not next(iter(algebra.values())).__add__(1).normal().terms, 'changed algebra identity'),
                  lambda: require(Q(constants_output['B_uniform']) < 400, 'changed loss constant'),
                  lambda: require(len(parts[:-1]) == 764, 'missing partition'),
                  lambda: I(-1).sqrt(), lambda: I(1)/I(-1, 1),
                  lambda: require(Q(separating['M_star_squared_interval'][1]) <= Q(separating['old_squared_threshold']), 'false old threshold')]:
        try:
            check()
        except ValueError:
            rejects += 1
        else:
            raise ValueError('corruption accepted')
    return {'agent': 'six-reviewer-2', 'role': 'independent mathematical reviewer',
            'arithmetic': 'Python integers/Fraction; exact two-circle polynomial normal forms and dyadic outward square roots',
            'universal_algebraic_identities': sorted(algebra), 'constants': constants_output,
            'matching': matching, 'interval_bits': BITS, 'interval_control_checks': controls,
            'original_example': original, 'separating_example': separating, 'mutation_rejections': rejects}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    result = json.dumps(run(), indent=2, sort_keys=True)+'\n'
    if args.output:
        args.output.write_text(result)
    else:
        print(result, end='')
