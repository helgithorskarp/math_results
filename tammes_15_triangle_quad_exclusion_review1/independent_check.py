#!/usr/bin/env python3
"""Exact auxiliary audit by six-reviewer-1; no author-code import or solver.

This checks polynomial reductions, a monotone root bracket, literal small
incidence possibilities, and integer Gram inequalities. README.md supplies
the geometric proof. The program does not enumerate spherical embeddings.
"""
from fractions import Fraction as F
from hashlib import sha256
from itertools import product
from math import comb, gcd, lcm
from pathlib import Path
import json


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def clean(p):
    p = list(map(F, p))
    while len(p) > 1 and p[-1] == 0:
        p.pop()
    return tuple(p)


def plus(p, q):
    return clean([(p[k] if k < len(p) else 0) +
                  (q[k] if k < len(q) else 0)
                  for k in range(max(len(p), len(q)))])


def times(p, q):
    result = [F(0)] * (len(p) + len(q) - 1)
    for i, a in enumerate(p):
        for j, b in enumerate(q):
            result[i+j] += a*b
    return clean(result)


def negative(p):
    return tuple(-a for a in p)


def square(p):
    return times(p, p)


def at(p, x):
    # Direct power sum, rather than the author's Horner/Bernstein checks.
    return sum((a*x**k for k, a in enumerate(p)), F(0))


def derivative(p):
    return clean([k*p[k] for k in range(1, len(p))] or [0])


def translated(p, a):
    # Power-basis coefficients of p(a+t), from the binomial theorem.
    return clean([sum((p[j]*comb(j, k)*a**(j-k)
                       for j in range(k, len(p))), F(0))
                  for k in range(len(p))])


def remainder(p, divisor):
    # Polynomial long division, used instead of a quadratic-field object.
    r = clean(p)
    divisor = clean(divisor)
    require(divisor != (0,), 'zero polynomial divisor')
    while r != (0,) and len(r) >= len(divisor):
        k, a = len(r)-len(divisor), r[-1]/divisor[-1]
        r = plus(r, negative((F(0),)*k + tuple(a*b for b in divisor)))
    return r


def identity(p, q, label):
    require(clean(p) == clean(q), label)


def arithmetic():
    c, H, D = (0, 1), (1, 2), (1, 2, -1)
    c2, c3, c4 = square(c), times(square(c), c), square(square(c))
    # tan((A-y)/2) cancellation, with H=h^2=1+2c.
    identity(plus(times((0, 2), H), D), times((1, 1), (1, 3)),
             'z half-angle numerator')
    identity(plus(D, negative(times((2,), c3))),
             times(times((1, -1), (1, 1)), H),
             'z half-angle denominator')
    Ynum, Yden = square(D), times((4,), times(H, c4))
    P = plus(Ynum, negative(times((3,), Yden)))
    H3 = times(square(H), H)
    Q = plus(times(H3, square((1, -1))),
             negative(times(c3, square((1, 3)))))
    identity(P, (1, 4, 2, -4, -11, -24), 'P expansion')
    identity(Q, (1, 4, 1, -11, -10, -1), 'Q expansion')
    # Every coefficient is strictly negative, hence derivatives are negative
    # for every t>=0, not only at sampled points of the parameter interval.
    shifted = {name: translated(derivative(p), F(1, 2))
               for name, p in [('P', P), ('Q', Q)]}
    require(all(a < 0 for p in shifted.values() for a in p),
            'global derivative sign in shifted power basis')
    require(at(Q, F(3, 5)) == F(32, 3125) > 0, 'Q endpoint')
    lo, hi = F(119, 200), F(3, 5)
    require(at(P, lo) > 0 > at(P, hi), 'root endpoint signs')
    for _ in range(48):
        mid = (lo+hi)/2
        if at(P, mid) > 0:
            lo = mid
        else:
            hi = mid
    # Publish a reader-friendly rational decimal bracket; it too is checked.
    scale = 10**12
    k = (lo.numerator*scale)//lo.denominator
    root_lo, root_hi = F(k, scale), F(k+1, scale)
    require(root_lo <= lo < hi <= root_hi, 'decimal root bracket containment')
    require(at(P, root_lo) > 0 > at(P, root_hi), 'decimal root bracket signs')
    endpoint_margin = at(P, F(119, 200))/at(Yden, F(119, 200))
    require(endpoint_margin == F(3081381928, 43916928699), 'original y margin')
    # The w=pi-alpha equation and both final contradictions.
    root_eq = plus(times(c2, (1, 3)), negative(times(H, (1, -1))))
    f = (-1, 0, 3)
    identity(root_eq, times((1, 1), f), 'w root factorization')
    diagonal_num = plus(times(c2, (3, 2)), (-1,))
    identity(diagonal_num, times((-1, 2), square((1, 1))),
             'positive acute-diagonal numerator')
    require(remainder(plus(Ynum, negative(times((0, 6), Yden))), f) == (0,),
            'tan squared y equals 6c at the special root')
    cos_num = square(plus(Yden, negative(Ynum)))
    cos_den = square(plus(Yden, Ynum))
    require(remainder(plus(times(cos_num, (13, 12)),
                           negative(times(cos_den, (13, -12)))), f) == (0,),
            'cos squared y reduction')
    incompatible = plus(times((2, 2), (13, -12)), (-13, -12))
    identity(remainder(incompatible, f), (5, -10), 'second equality remainder')
    # An explicit Bezout identity excludes a common real or complex solution.
    identity(plus(times((-4,), f), times((F(-3, 5), F(-6, 5)), (5, -10))),
             (1,), 'final incompatible-equations Bezout certificate')
    return {
        'P_coefficients_ascending': list(map(int, P)),
        'Q_coefficients_ascending': list(map(int, Q)),
        'derivative_coefficients_at_c_equals_half_plus_t':
            {name: list(map(str, p)) for name, p in shifted.items()},
        'Q_at_three_fifths': str(at(Q, F(3, 5))),
        'P_at_119_over_200': str(at(P, F(119, 200))),
        'P_at_three_fifths': str(at(P, F(3, 5))),
        'beta_strict_lower': f'{k//scale}.{k%scale:012d}',
        'beta_strict_upper': f'{(k+1)//scale}.{(k+1)%scale:012d}',
        'original_tan_squared_y_minus_three': str(endpoint_margin),
        'special_root_polynomial': list(f),
        'second_equality_mod_special_root': ['5', '-10'],
        'final_Bezout_constant': 1,
        'parameter_endpoint_beta_included': False,
    }


def incidence():
    profiles = {}
    for N in (15, 16, 17):
        all_profiles, screened = [], []
        for n3 in range(N+1):
            for n4 in range(N-n3+1):
                n5 = N-n3-n4
                if 3*n3+4*n4+5*n5 != 2*(3*N-12):
                    continue
                all_profiles.append([n3, n4, n5])
                if n5 % 2 == 0 and n5 <= n4+2*n3:
                    screened.append([n3, n4, n5])
        profiles[str(N)] = {'q6_degree_profiles': all_profiles,
                            'after_marked_corner_capacity': screened}
    require(profiles['15']['after_marked_corner_capacity'] == [[0, 9, 6], [2, 5, 8]],
            'fifteen-point degree cases')
    require(profiles['16']['after_marked_corner_capacity'] == [[0, 8, 8]],
            'sixteen-point equality case')
    require(profiles['17']['after_marked_corner_capacity'] == [],
            'first empty large-N case')
    # Full labeled assignments, rather than comparing only a total count.
    arrangements = [[list(a), list(b)]
                    for a in product((0, 1), repeat=5)
                    for b in product((0, 1, 2), repeat=2)
                    if sum(a)+sum(b) == 8]
    types = sorted({(sum(a), *sorted(b)) for a, b in arrangements})
    require(len(arrangements) == 7 and types == [(4, 2, 2), (5, 1, 2)],
            'complete marked corner assignment cases')
    diagonal_multigraphs = [[a, b, c] for a, b, c in product(range(3), repeat=3)
                           if a+b == a+c == b+c == 2]
    require(diagonal_multigraphs == [[1, 1, 1]], 'three-vertex diagonal graph')
    deficits = [[a, b, c, d] for a, b, c, d in product(range(3), repeat=4)
                if a+b+2*c+2*d == 2]
    require(len(deficits) == 5, 'q7 deficit types')
    return {
        'profiles': profiles,
        'labeled_marked_corner_assignments_for_2_5_8': arrangements,
        'assignment_types': list(map(list, types)),
        'loopless_diagonal_multigraph_edge_multiplicities': diagonal_multigraphs,
        'N16_required_z_corners': 8,
        'N16_available_z_corners': 4,
        'general_q6_capacity_gap': '48-3*N-n3',
        'q7_deficit_columns': ['n4_delta1', 'n5_delta1', 'n4_delta2', 'n5_delta2'],
        'q7_deficit_types': deficits,
        'geometric_exclusions_supplied_by': 'README.md, not this computation',
    }


def integer_rows(raw):
    rows = [tuple(F(s) for s in line.split(','))
            for line in raw.decode('ascii').splitlines()]
    require(len(rows) == 15 and all(len(v) == 3 for v in rows), 'coordinate dimensions')
    result = []
    for v in rows:
        scale = lcm(*(x.denominator for x in v))
        ints = [int(x*scale) for x in v]
        common = gcd(*ints)
        require(common > 0, 'zero direction')
        result.append(tuple(x//common for x in ints))
    return result


def allowed_pair(v, w, bound):
    Nv, Nw = sum(x*x for x in v), sum(x*x for x in w)
    require(Nv > 0 and Nw > 0 and 0 < bound < 1, 'Gram input domain')
    dot = sum(x*y for x, y in zip(v, w))
    margin = bound.numerator**2*Nv*Nw - bound.denominator**2*dot*dot
    return dot <= 0 or margin > 0, dot, margin, Nv, Nw


def coordinates():
    raw = Path(__file__).with_name('incumbent_decimal.csv').read_bytes()
    rows, bound = integer_rows(raw), F(119, 200)
    entries, positive_margins = [], []
    for i in range(15):
        for j in range(i):
            ok, dot, margin, Ni, Nj = allowed_pair(rows[i], rows[j], bound)
            require(ok, f'pair {j},{i} fails strict threshold')
            entries.append([j, i, (dot > 0)-(dot < 0)])
            if dot > 0:
                positive_margins.append(F(margin, bound.numerator**2*Ni*Nj))
            # Independent positive rescaling must preserve the normalized test.
            scaled = allowed_pair(tuple((i+1)*x for x in rows[i]),
                                  tuple((j+2)*x for x in rows[j]), bound)
            require(scaled[0] == ok and (scaled[1] > 0)-(scaled[1] < 0) == entries[-1][2],
                    'normalization invariance')
    require(len(entries) == 105, 'pair coverage')
    # Boundary controls: positive dot, strict equality, zero dot, negative dot.
    axis, test = (1, 0, 0), (12, 5, 0)
    require(not allowed_pair(axis, test, F(12, 13))[0], 'threshold equality accepted')
    require(not allowed_pair(axis, test, F(11, 12))[0], 'above-threshold pair accepted')
    require(allowed_pair(axis, test, F(13, 14))[0], 'below-threshold pair rejected')
    require(allowed_pair(axis, (0, 1, 0), bound)[0], 'zero dot rejected')
    require(allowed_pair(axis, (-1, 0, 0), bound)[0], 'negative dot rejected')
    require(not allowed_pair(axis, axis, bound)[0], 'duplicate direction accepted')
    return {
        'input_sha256': sha256(raw).hexdigest(),
        'interpretation': 'primitive integer directions, individually normalized',
        'points': 15,
        'strict_cosine_upper_bound': str(bound),
        'all_105_pair_indices_and_dot_signs': entries,
        'minimum_relative_margin_among_positive_dots': str(min(positive_margins)),
        'positive_rescaling_checks': 105,
        'boundary_controls_passed': 6,
        'exact_candidate_contacts_or_optimality_certified': False,
    }


if __name__ == '__main__':
    result = {'agent': 'six-reviewer-1', 'role': 'independent reviewer',
              'arithmetic': arithmetic(), 'incidence': incidence(),
              'threshold_packing': coordinates()}
    print(json.dumps(result, indent=2, sort_keys=True))
