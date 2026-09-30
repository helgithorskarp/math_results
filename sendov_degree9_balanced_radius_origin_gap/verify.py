"""Complete exact certificates for the balanced-radius two-channel gap.

No floating-point or external package is used. Checks remain active with -O.
"""
from fractions import Fraction as F
from itertools import product
from math import factorial
from pathlib import Path
import hashlib
import json
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from algebra import (ONE, A, add, scale, mul, power, degrees,
                     origin_coefficients, multinomial_coefficients,
                     chebyshev_norm, quotient_norm, coupled_axis,
                     coupled_horner, affine_axis, divide_delta,
                     bernstein, inverse_bernstein)

BOXES = [(F(0), F(1, 2)), (F(1, 2), F(3, 4)),
         (F(3, 4), F(7, 8)), (F(7, 8), F(1))]
DEGREE = (19, 8, 8)
POLAR_BETAS = list(map(F, ['8/9', '15/14', '94/75', '41/30',
                          '19/15', '1', '2/3']))


def require(ok, message):
    if not ok:
        raise ArithmeticError(message)


def digest(values):
    return hashlib.sha256(('\n'.join(str(z) for z in values)+'\n').encode()).hexdigest()


def validate_cover(boxes):
    require(bool(boxes) and boxes[0][0] == 0 and boxes[-1][1] == 1,
            'outer coverage')
    require(all(lo < hi for lo, hi in boxes), 'nonempty cells')
    require(all(boxes[j][1] == boxes[j+1][0] for j in range(len(boxes)-1)),
            'missing or duplicate cells')


def validate_values(ds, vals):
    require(ds == DEGREE, 'complete degree extent')
    require(all(len(m) == 3 and all(0 <= m[j] <= ds[j] for j in range(3))
                for m in vals), 'coefficient index extent')
    require(all(z >= 0 for z in vals.values()), 'negative certificate coefficient')


def validate_cell(lo, hi, p):
    local = affine_axis(p, 0, lo, hi)
    ds, vals = bernstein(local)
    validate_values(ds, vals)
    require(inverse_bernstein(ds, vals) == local, 'full inverse basis identity')
    indices = list(product(*(range(n+1) for n in ds)))
    flat = [vals.get(m, F(0)) for m in indices]
    zeros = [list(m) for m, z in zip(indices, flat) if not z]
    expected_zeros = [] if hi < 1 else [[19, 8, k] for k in range(9)]
    require(zeros == expected_zeros, 'complete origin zero pattern')
    return {'interval': [str(lo), str(hi)], 'degree': list(ds),
            'count': len(flat), 'minimum': str(min(flat)),
            'zero_indices': zeros, 'sha256': digest(flat)}


def specialize(p, axis, value):
    out = {}
    for m, z in p.items():
        key = list(m)
        key[axis] = 0
        out = add(out, {tuple(key): z*value**m[axis]})
    return out


def sharp_origin_limit(no):
    # c=x=1 gives u=v=1. The new first variable is delta=1-tau.
    diagonal = specialize(specialize(no, 1, F(1)), 2, F(1))
    shifted = affine_axis(diagonal, 0, F(1), F(0))
    geometric = {(j, 0, 0): F(1) for j in range(9)}
    require(shifted == mul(geometric, geometric), 'complete sharp-limit identity')
    leading = [shifted.get((j, 0, 0), F(0)) for j in range(5)]
    require(leading == list(map(F, [1, 2, 3, 4, 5])), 'sharp leading coefficient')
    return list(map(str, leading))


def polar_certificate():
    # Here A is the separate parameter a^2, not a. D=1-A.
    d = add(ONE, scale(A, -1))
    quadratic = [A, scale(mul(A, d), 2), power(d, 2)]
    cs = [ONE]
    for _ in range(4):
        nxt = [{} for _ in range(len(cs)+2)]
        for j, z in enumerate(cs):
            for k, t in enumerate(quadratic):
                nxt[j+k] = add(nxt[j+k], mul(z, t))
        cs = nxt
    integral = {}
    for k, z in enumerate(cs):
        integral = add(integral, scale(z, F(1, k+1)))
    independent = {}
    for n1 in range(5):
        for n2 in range(5-n1):
            n0 = 4-n1-n2
            coefficient = F(factorial(4)*2**n1,
                            factorial(n0)*factorial(n1)*factorial(n2)*
                            (n1+2*n2+1))
            independent = add(independent, scale(
                mul(power(A, n0+n1), power(d, n1+2*n2)), coefficient))
    require(integral == independent, 'complete independent polar integral')
    defect = add(ONE, scale(integral, -1))
    q = divide_delta(divide_delta(defect))
    require(mul(power(d, 2), q) == defect, 'complete squared polar factor')
    ds, vals = bernstein(q)
    require(ds == (6, 0, 0), 'complete polar degree')
    flat = [vals.get((j, 0, 0), F(0)) for j in range(7)]
    require(flat == POLAR_BETAS and min(flat) == F(2, 3), 'polar Bernstein bound')
    require(inverse_bernstein(ds, vals) == q, 'complete polar inverse basis')
    return {'parameter': 'A=a^2', 'degree': list(ds), 'count': 7,
            'bernstein_coefficients': list(map(str, flat)),
            'minimum': str(min(flat)), 'sha256': digest(flat)}


def constants():
    polar = F(8)*F(63, 50)**7
    origin = 9*8*4*3**7
    h_scale = F(1, 2000000)
    margin = F(1, 2)-origin*h_scale
    require(polar < 50, 'polar telescoping bound')
    require(origin == 629856, 'normalized origin telescoping constant')
    require(h_scale < F(1, 100), 'small imbalance window')
    require(F(5, 4)+h_scale < F(63, 50), 'polar factor bound')
    require(50*h_scale == F(1, 40000) < F(2, 3), 'polar forcing gap')
    require(margin == F(11567, 62500) > F(1, 8), 'strict final origin gap')
    derivative = F(4)*F(5, 4)**6
    pressure = F(2, 3)/derivative
    require(derivative == F(15625, 1024), 'optional mean derivative constant')
    require(pressure == F(2048, 46875), 'optional quantitative mean pressure')
    return {'radius_difference_coefficient': '1/1000000',
            'half_difference_coefficient': str(h_scale),
            'polar_telescoping': str(polar), 'polar_upper': '50',
            'normalized_origin_telescoping': origin,
            'polar_defect_loss_coefficient': '1/40000',
            'derived_origin_gap_coefficient': str(margin),
            'stated_origin_gap_coefficient': '1/8',
            'mean_derivative_coefficient': str(derivative),
            'optional_mean_pressure_coefficient': str(pressure)}


# A separate exact Gaussian-rational computation; no polynomial norm routines.
def ga(z, w):
    return (z[0]+w[0], z[1]+w[1])


def gs(z, t):
    return (z[0]*t, z[1]*t)


def gm(z, w):
    return (z[0]*w[0]-z[1]*w[1], z[0]*w[1]+z[1]*w[0])


def gp(z, n):
    out = (F(1), F(0))
    for _ in range(n):
        out = gm(out, z)
    return out


def norm2(z):
    return z[0]**2+z[1]**2


def gi(z):
    n = norm2(z)
    require(n > 0, 'nonzero Gaussian inverse')
    return (z[0]/n, -z[1]/n)


def gaussian_integral(constant, linear, multiplier):
    cs = [(F(1), F(0))]
    for _ in range(8):
        nxt = [(F(0), F(0)) for _ in range(len(cs)+1)]
        for j, z in enumerate(cs):
            nxt[j] = ga(nxt[j], gm(z, constant))
            nxt[j+1] = ga(nxt[j+1], gm(z, linear))
        cs = nxt
    out = (F(0), F(0))
    for j, z in enumerate(cs):
        out = ga(out, gs(z, F(multiplier, j+1)))
    return out


def monotonicity_obstruction():
    a, r = F(3, 4), F(199, 200)
    b = 1-a*a
    q = (F(5, 13), F(12, 13))
    one = (F(1), F(0))
    require(norm2(q) == 1, 'unit Gaussian phase')
    require(F(1, 1+a) <= r < 1, 'feasible radial interval')
    values, slacks, polar_norms = [], [], []
    for radius in [F(1), r]:
        w = gs(q, radius)
        slack = 2*a*w[0]+b*norm2(w)-1
        require(slack > 0, 'strict individual reciprocal-disk slack')
        slacks.append(slack)
        aq = gs(w, a)
        origin = gaussian_integral(one, gs(aq, -1), 9)
        closed = gm(ga(one, gs(gp(ga(one, gs(aq, -1)), 9), -1)), gi(aq))
        require(origin == closed, 'full Gaussian origin integral identity')
        values.append(norm2(origin)/radius**16)
        linear = gs(w, b)
        polar = gaussian_integral((a, F(0)), linear, 1)
        polar_closed = gs(gm(ga(gp(ga((a, F(0)), linear), 9),
                                   (-a**9, F(0))), gi(linear)), F(1, 9))
        require(polar == polar_closed, 'full Gaussian polar integral identity')
        polar_norms.append(norm2(polar))
        require(polar_norms[-1] < 1, 'obstruction is not a joint-channel witness')
    difference = values[1]-values[0]
    require(difference < 0, 'normalized-origin radial monotonicity fails')
    require(slacks == [F(3, 208), F(59691, 8320000)], 'exact disk slacks')
    return {'a': str(a), 'phase': list(map(str, q)), 'radius': str(r),
            'strict_disk_slacks': list(map(str, slacks)),
            'normalized_origin_squared_unit_radial': list(map(str, values)),
            'radial_minus_unit': str(difference),
            'polar_squared_unit_radial': list(map(str, polar_norms)),
            'is_polynomial_counterexample': False}


def build_summary():
    hs, oc = origin_coefficients()
    require(hs == multinomial_coefficients(), 'nine full quadratic coefficients')
    no = chebyshev_norm(oc)
    require(no == quotient_norm(oc), 'complete independent origin norm')
    raw = add(add(no, scale(ONE, -3)), scale(A, 2))
    coupled = coupled_axis(coupled_axis(raw, 1), 2)
    require(coupled == coupled_horner(coupled_horner(raw, 1), 2),
            'complete independent phase substitutions')
    q = divide_delta(coupled)
    require(degrees(q) == DEGREE, 'complete divided origin degree')
    validate_cover(BOXES)
    cells = [validate_cell(lo, hi, q) for lo, hi in BOXES]
    polar = polar_certificate()
    require(sum(row['count'] for row in cells)+polar['count'] == 6487,
            'complete certificate count')
    return {'status': 'PASS: exact arithmetic; no floating-point proof input',
            'full_quadratic_coefficient_identities': 9,
            'full_origin_norm_identities': 1,
            'full_phase_substitution_identities': 1,
            'full_delta_factor_identities': 3,
            'full_polar_integral_identities': 1,
            'full_inverse_basis_identities': 5,
            'bernstein_coefficients': 6487, 'origin_cells': cells,
            'origin_sharp_delta_coefficients': sharp_origin_limit(no),
            'polar': polar, 'constants': constants(),
            'monotonicity_obstruction': monotonicity_obstruction()}


def mutation_controls():
    rejected = 0
    for boxes in [BOXES[:-1], BOXES+[BOXES[-1]]]:
        try:
            validate_cover(boxes)
        except ArithmeticError:
            rejected += 1
    for ds, vals in [(DEGREE, {(0, 0, 0): F(-1)}),
                     ((20, 8, 8), {(0, 0, 0): F(1)})]:
        try:
            validate_values(ds, vals)
        except ArithmeticError:
            rejected += 1
    local = {(0, 0, 0): F(1), (2, 1, 1): F(3)}
    ds, vals = bernstein(local)
    vals[0, 0, 0] += 1
    require(inverse_bernstein(ds, vals) != local, 'changed coefficient detected')
    rejected += 1
    require(rejected == 5, 'mutation control count')
    return rejected


def main():
    summary = build_summary()
    expected = json.loads(Path(__file__).with_name('expected.json').read_text())
    require(summary == expected, 'fixed compact manifest mismatch')
    mutation_controls()
    print('PASS: 6487 exact Bernstein coefficients; complete norm and factor identities;')
    print('5 full inverse basis identities; 5 mutations rejected; exact radial obstruction.')
    print('Near-balanced two-channel origin gap: |O|/(r^4 s^4) > 1+(1-a)/8.')
    print('The unrestricted two-value and general first-power conjectures remain unproved.')


if __name__ == '__main__':
    main()
