#!/usr/bin/env python3
"""Exact supplementary audit of the paired-layer majorisation theorems.

Python standard library only. The checker verifies finite identities and
rational budgets, including a whole shear interval by polynomial bounds.
It does not replace the continuum proofs or the credited external theorems.
"""
import argparse
from fractions import Fraction as F
import hashlib
from itertools import product
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
S0 = F(1, 10**10)
R = F(13, 20)
E0 = F(1, 1000)


def require(condition, message):
    if not condition:
        raise ArithmeticError(message)


def norm2(x):
    return sum(v * v for v in x)


def dist2(x, y):
    return norm2(tuple(a - b for a, b in zip(x, y)))


def dot(x, y):
    return sum(a * b for a, b in zip(x, y))


def j_reflect(x):
    return (-x[0], -x[1], x[2])


def geometry_conditions(a, b, anchor):
    if not a or not b or not 0 <= anchor < len(a):
        return False
    if len(set(a)) != len(a) or len(set(b)) != len(b):
        return False
    if any(len(z) != 3 or z[2] != 1 for z in a + b):
        return False
    if set(map(j_reflect, a)) != set(a) or set(map(j_reflect, b)) != set(b):
        return False
    if any(not F(7, 5)**2 <= norm2(z) <= 4 for z in a):
        return False
    if any(not F(17, 10)**2 <= norm2(z) <= 4 for z in b):
        return False
    if any(dot(x, y) < 0 for x in a for y in b):
        return False
    d = [dist2(a[anchor], z) for z in b]
    return min(d) >= F(9, 10)**2 and min(d) <= F(101, 100)**2


def weight_conditions(w, n, anchor):
    return (len(w) == n and sum(w) == 1 and min(w) >= F(1, 32)
            and w[0] <= F(1, 16) and w[anchor + 1] >= F(1, 5))


# Coefficient tuples of exact univariate polynomials in epsilon.
def poly(*coefficients):
    out = list(map(F, coefficients)) or [F(0)]
    while len(out) > 1 and out[-1] == 0:
        out.pop()
    return tuple(out)


def padd(a, b):
    return poly(*(sum(c[k] if k < len(c) else 0 for c in (a, b))
                  for k in range(max(len(a), len(b)))))


def pneg(a):
    return poly(*(-v for v in a))


def pmul(a, b):
    out = [F(0)] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i + j] += x * y
    return poly(*out)


def pdot(x, y):
    out = poly(0)
    for a, b in zip(x, y):
        out = padd(out, pmul(a, b))
    return out


def psub(x, y):
    return tuple(padd(a, pneg(b)) for a, b in zip(x, y))


def peval(p, epsilon):
    out = F(0)
    for c in reversed(p):
        out = out * epsilon + c
    return out


def interval(p):
    """Certified enclosure for every real |epsilon| <= E0."""
    radius = sum(abs(c) * E0**k for k, c in enumerate(p) if k)
    return p[0] - radius, p[0] + radius


def shear_audit():
    z, one, minus, e, me = poly(0), poly(1), poly(-1), poly(0, 1), poly(0, -1)
    a = ((one, z, one), (e, one, one),
         (minus, z, one), (me, minus, one))
    b = ((one, poly(1, -1), one), (minus, poly(1, 1), one),
         (minus, poly(-1, 1), one), (one, poly(-1, -1), one))
    for cloud in (a, b):
        reflected = {(pneg(x), pneg(y), h) for x, y, h in cloud}
        require(reflected == set(cloud), 'Polynomial transverse symmetry')
    cross = [[pdot(x, y) for y in b] for x in a]
    expected_cross = [[2, 0, 0, 2], [2, 2, 0, 0],
                      [0, 2, 2, 0], [0, 0, 2, 2]]
    require(cross == [[poly(v) for v in row] for row in expected_cross],
            'Shear-independent cross dot matrix')
    require([pdot(x, x) for x in a] == [poly(2), poly(2, 0, 1)] * 2,
            'A squared norm polynomials')
    require([pdot(x, x) for x in b] == [poly(3, -2, 1), poly(3, 2, 1)] * 2,
            'B squared norm polynomials')
    for x in a:
        lower, upper = interval(pdot(x, x))
        require(F(7, 5)**2 <= lower <= upper <= 4, 'Uniform A norm bounds')
    for x in b:
        lower, upper = interval(pdot(x, x))
        require(F(17, 10)**2 <= lower <= upper <= 4, 'Uniform B norm bounds')
    # Enumerate the four vertices of |x| <= 1, |epsilon*x+y| <= 1.
    corners = [(x, padd(pmul(e, x), y)) for x, y, _ in b]
    require(set(corners) == set(product((one, minus), repeat=2)),
            'All four vertices of the full dual section')
    distances = [pdot(psub(a[3], x), psub(a[3], x)) for x in b]
    require(distances == [poly(5, -2, 2), poly(5, 2, 2),
                          poly(1, -2, 2), poly(1, 2, 2)],
            'Anchor cross-distance polynomials')
    require(all(interval(p)[0] >= F(9, 10)**2 for p in distances),
            'Uniform anchor separation')
    require(all(interval(p)[1] <= F(101, 100)**2 for p in distances[2:]),
            'Uniform anchor neighbor')
    # Exact rational controls supplement (not replace) the interval argument.
    fixtures = {}
    for epsilon in (-E0, F(0), E0):
        ac = tuple(tuple(peval(v, epsilon) for v in x) for x in a)
        bc = tuple(tuple(peval(v, epsilon) for v in x) for x in b)
        require(geometry_conditions(ac, bc, 3), 'Rational shear fixture')
        source = ((F(0), F(0), F(0)),) + ac + tuple(tuple(-v for v in x) for x in bc)
        target = ((F(0), F(0), F(0)),) + ac + bc
        losses = [dist2(source[i], source[j]) - dist2(target[i], target[j])
                  for i in range(9) for j in range(i)]
        require(losses.count(0) == 28 and losses.count(8) == 8,
                'Labelled contraction losses at rational fixture')
        fixtures[str(epsilon)] = {'zero_losses': 28, 'losses_equal_8': 8}
        if epsilon == 0:
            base_a, base_b = ac, bc
    rays = base_a + base_b
    old_angles = {dot(rays[i], rays[j])**2 / (norm2(rays[i]) * norm2(rays[j]))
                  for i in range(8) for j in range(i)}
    require(old_angles == {F(0), F(1, 4), F(1, 9), F(2, 3)},
            'Original distinct-ray squared cosines')
    angle = (1 + E0)**2 / (2 * (2 + E0**2))
    require(angle not in old_angles, 'Sheared rays differ from the centered fixed-ray class')
    numerator, denominator = poly(1, 2, 1), poly(4, 0, 2)
    nlo, nhi = interval(numerator)
    dlo, dhi = interval(denominator)
    require(dlo > 0 and nlo / dhi > F(1, 5) and nhi / dlo < F(1, 3),
            'Uniform squared-angle interval for the entire shear family')
    require(padd(pmul(poly(4), numerator), pneg(denominator))
            == pmul(poly(0, 2), poly(4, 1)), 'Squared-angle equality factor')
    require(4 - E0 > 0, 'Only zero shear can have squared cosine one quarter')
    invalid_b = list(base_b)
    invalid_b[0] = (F(1), F(1), F(2))
    require(not geometry_conditions(base_a, tuple(invalid_b), 3),
            'Invalid geometry rejected')
    return {'epsilon_interval': [str(-E0), str(E0)],
            'cross_dot_matrix': expected_cross,
            'anchor_distance_polynomials': [[str(v) for v in p] for p in distances],
            'rational_fixtures': fixtures,
            'new_squared_cosine_at_positive_endpoint': str(angle),
            'all_nonzero_shears_leave_centered_fixed_ray_angles': True}, base_a, base_b


def factorial(n):
    out = 1
    for i in range(2, n + 1):
        out *= i
    return out


def audit():
    shear, a, b = shear_audit()
    # Every nested pair of section memberships and every origin membership.
    configurations = 0
    for e, ep, f, fp, c in product((0, 1), repeat=5):
        if ep > e or fp > f:
            continue
        value = (int(bool(e or fp or c)) + int(bool(ep or f or c))
                 - int(bool(e or f or c)) - int(bool(ep or fp or c)))
        expected = int(bool(e and not ep and f and not fp and not c))
        require(value == expected, 'Section indicator identity')
        configurations += 1
    # Inscribed ball for a continuum of radii, then the infinite-radius box.
    rmin = F(3, 5)
    dmax = F(101, 100)
    constant = F(1, 10000) - F(81, 100) - dmax**2 / 4
    require(constant == -F(42597, 40000), 'Ball polynomial constant')
    slack = F(89, 50) * rmin + constant
    require(slack == F(123, 40000) > 0, 'Inscribed ball slack')
    require(F(1, 10) - F(1, 100) > 0, 'Ball excludes origin and lower layers')
    require(F(4, 10**6) >= 8 * F(1, 2000000), 'Intermediate volume budget')
    require(dmax / 2 < 1, 'Large-radius box offsets')
    require(F(3, 8) * 8 - F(9, 4) > 0, 'Large-radius box slack')
    require(F(1, 16) > F(1, 2000000), 'Large-radius volume budget')
    # exp(4)>32, pi<4, log(32)<4, N<=32, and s<=r^2.
    exp4_lower = sum(F(4)**k / factorial(k) for k in range(5))
    require(exp4_lower > 32, 'Antipodal factor and log bound')
    error_budget = 4 * 4 * (32 * 4 + 2)
    require(error_budget == 2080, 'Low-threshold error coefficient')
    low_margin = F(1, 2000000) - error_budget * S0
    require(low_margin > 0, 'Low-threshold comparison')
    require(rmin**2 - 8 * S0 > 0 and S0 < rmin**2, 'Radius and Mills budgets')
    a_gap = F(7, 5)**2 / 2 - R * F(7, 5)
    b_gap = F(17, 10)**2 / 2 - R * F(17, 10)
    require(a_gap == F(7, 100) and b_gap == F(17, 50), 'Core dominance gaps')
    require(min(a_gap, b_gap) > F(1, 40), 'Core dominance exponent')
    require(2 * 128 * 3200 == 819200 and 819200 * S0 < 1,
            'Strong log-concavity budget')
    eta_bound = 102400 * S0**2
    require(eta_bound < F(1, 2), 'Relative off-core mass budget')
    require(R**2 / (2 * S0) > 1, 'Interior maximum budget')
    # Localization and origin coarea-band constants.
    cut = F(9, 50)
    require(R**2 / 2 > cut and (1 - 2 * S0)**2 / 2 > cut, 'Thin-slab exclusion')
    p_exp = (F(7, 5) - R)**2 / 2
    q_exp = (F(17, 10) - R)**2 / 2
    require(p_exp == F(9, 32) and q_exp == F(441, 800), 'Origin perturbation exponents')
    require(q_exp - cut == F(297, 800), 'Level-band exponent')
    require(1 + F(297, 800) / S0 >= 4, 'Q0<=t/2')
    neg_exp = p_exp + q_exp - cut
    require(neg_exp == F(261, 400), 'Negative contribution exponent')
    require(128 * 4 * R <= 512, 'Negative contribution coefficient')
    # Positive contribution near an arbitrary admissible heavy anchor.
    rho_upper = F(1, 1000)
    require(S0 / 100 <= rho_upper**2, 'rho bound')
    require(1 - F(1, 200) > F(1, 2), 'Anchor exceeds half its mass')
    pos_exp = F(13, 25)
    require((dmax + rho_upper)**2 / 2 < pos_exp, 'Nearest target upper exponent')
    require((2 - rho_upper)**2 / 2 > F(3, 2), 'Source cloud lower exponent')
    require(F(3, 2) - pos_exp == F(49, 50), 'Signal subtraction exponent')
    require(1 + F(49, 50) / S0 >= 64, 'Positive signal subtraction')
    require((F(9, 10) - rho_upper)**2 / 2 > cut, 'Reflected partners inactive')
    require(F(7, 5) - rho_upper > R and 1 - rho_upper > 2 * S0,
            'Positive ball outside origin and thin slab')
    exponent_margin = neg_exp - pos_exp
    require(exponent_margin == F(53, 400) > F(1, 10), 'Exponential dominance margin')
    sqrt_s0 = F(1, 100000)
    require(sqrt_s0**2 == S0, 'Exact variance square root')
    signal_ratio = 1 / (200 * S0 * sqrt_s0)
    require(signal_ratio > 512 * 16000, 'Positive contribution dominates negative mass')
    require(F(3, 32) < F(1, 10), 'High-threshold origin exclusion')
    # The full inherited neighborhood satisfies our weight hypotheses.
    p = tuple(F(k, 184) for k in (8, 12, 7, 15, 44, 21, 11, 23, 43))
    delta = F(1, 4000)
    require(weight_conditions(p, 9, 3), 'Central law admissible')
    require(min(p) - delta > F(1, 32), 'Neighborhood minimum weight')
    require(p[0] + delta < F(1, 16) and p[4] - delta > F(1, 5),
            'Neighborhood origin and anchor weights')
    invalid = list(p)
    invalid[0] = F(1, 10)
    invalid[4] -= F(1, 10) - p[0]
    require(not weight_conditions(invalid, 9, 3), 'Invalid core weight rejected')
    # A deliberately excessive variance violates the actual comparison budget.
    require(F(1, 2000000) - error_budget * F(1, 100) < 0,
            'Invalid variance control fails the comparison budget')
    # The full-variance assembly uses the cited J0,w>=1/128 and stability theorem.
    # These finite budgets do not independently verify those external premises.
    spatial_low, spatial_high = F(1, 1000), F(1, 16384)
    require((F(7, 5) + spatial_low)**2 < 2, 'Perturbed A lower norm')
    require((F(17, 10) + spatial_low)**2 < 3, 'Perturbed B lower norm')
    require((2 - spatial_low)**2 > 3, 'Perturbed upper norm')
    require(1 - 2 * spatial_low > F(9, 10), 'Perturbed anchor separation')
    require(1 + 2 * spatial_low < F(101, 100), 'Perturbed anchor neighbor')
    require(spatial_high < spatial_low, 'Endpoint spatial radius nesting')
    spherical_join = 32
    kappa = F(1, 128) - 2 * spherical_join * spatial_high
    require(kappa == F(1, 256), 'Uniform compact-parameter spherical margin')
    require(F(1, 6) - 2 * spatial_high >= F(1, 8), 'Perturbed mean-support margin')
    exp_seven_halves = sum(F(7, 2)**k / factorial(k) for k in range(8))
    require(exp_seven_halves > 32, 'Entire spherical tail: log32<7/2')
    require(F(spherical_join, 8) - F(7, 2) == F(1, 2) > kappa,
            'Tail matches the compact spherical margin')
    variance_high = 4 * max(8, 44 / kappa)
    require(variance_high == 45056 and S0 < variance_high, 'Variance interval assembly')
    require(F(1, 25000) < F(1, 4000), 'Compact stability weight inclusion')
    require(F(1, 128) - 64 * F(1, 32) < 0, 'Excessive displacement fails spherical budget')
    return {'status': 'PAIRED_LAYERS_MAJORISATION_EXACT_AUDIT_PASS',
            'scope': 'Supplement to the small-variance proof and all-variance completion; external theorem dependencies and existential middle radius remain explicit',
            'variance_upper': str(S0), 'maximum_labelled_sites': 32,
            'minimum_weight': '1/32', 'origin_weight_upper': '1/16', 'anchor_weight_lower': '1/5',
            'nested_section_configurations': configurations, 'ball_slack': str(slack),
            'volume_gap_coefficient': '1/2000000', 'low_threshold_error_coefficient': error_budget,
            'low_threshold_margin_coefficient': str(low_margin), 'eta_upper': str(eta_bound),
            'negative_exponent': str(neg_exp), 'positive_exponent': str(pos_exp),
            'exponent_margin': str(exponent_margin), 'signal_ratio_lower_bound': str(signal_ratio),
            'required_signal_ratio': 512 * 16000, 'shear_family': shear,
            'central_weights': list(map(str, p)), 'included_neighborhood_l1': str(delta),
            'all_variance_completion': {
                'weight_neighborhood_l1': '1/25000',
                'small_variance_geometry_radius': str(spatial_low),
                'high_variance_geometry_radius': str(spatial_high),
                'spherical_parameter_join': spherical_join,
                'borrowed_base_spherical_gap': '1/128',
                'perturbed_spherical_gap': str(kappa),
                'high_variance_lower': str(variance_high),
                'middle_variance_interval': [str(S0), str(variance_high)],
                'uniform_spatial_radius': 'min(epsilon_I,1/16384)>0; numerical value not certified'},
            'invalid_controls_rejected': 4}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--write-expected', action='store_true')
    args = ap.parse_args()
    result = audit()
    encoded = json.dumps(result, sort_keys=True, separators=(',', ':')).encode()
    digest = hashlib.sha256(encoded).hexdigest()
    record = {'audit': result, 'certificate_sha256': digest}
    target = ROOT / 'EXPECTED.json'
    if args.write_expected:
        target.write_text(json.dumps(record, indent=2) + '\n')
    else:
        require(json.loads(target.read_text()) == record, 'Expected audit mismatch')
    print(result['status'])
    print('certificate_sha256=' + digest)


if __name__ == '__main__':
    main()
