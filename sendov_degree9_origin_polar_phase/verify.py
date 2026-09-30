"""Replay every exact coefficient and the two fixed-weight obstructions."""
from fractions import Fraction as F
from pathlib import Path
from math import comb
import hashlib
import json
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from algebra import (ONE, coefficients, chebyshev_norm, quotient_norm,
                     phase_polynomials, suba, bernstein, inverse_bernstein,
                     gaussian_sum, norm2, polar_modulus_integral, evaluate,
                     add, scale, mul)


def require(ok, message):
    if not ok:
        raise ArithmeticError(message)


def digest(values):
    return hashlib.sha256(('\n'.join(str(x) for x in values)+'\n').encode()).hexdigest()


R_BOXES = [(F(0), F(1, 2)), (F(1, 2), F(3, 4)),
           (F(3, 4), F(7, 8)), (F(7, 8), F(1))]
D_BOXES = [(F(0), F(1, 2)), (F(1, 2), F(5, 8)), (F(5, 8), F(3, 4)),
           (F(3, 4), F(7, 8)), (F(7, 8), F(1))]


def validate_cover(boxes):
    require(boxes[0][0] == 0 and boxes[-1][1] == 1, 'outer coverage')
    require(all(lo < hi for lo, hi in boxes), 'nonempty cells')
    require(all(boxes[k][1] == boxes[k+1][0] for k in range(len(boxes)-1)),
            'missing or duplicate cells')


def validate_cell(name, lo, hi, p):
    local = suba(p, lo, hi)
    deg, vals = bernstein(local)
    wanted = (18, 8) if name == 'R' else (36, 16)
    require(deg == wanted, 'complete degree extent')
    require(inverse_bernstein(vals) == local, 'full inverse basis identity')
    flat = [c for row in vals for c in row]
    require(all(c >= 0 for c in flat), 'negative certificate coefficient')
    if name == 'R' or hi < 1:
        require(all(c > 0 for c in flat), 'strict positive cell')
    else:
        require(all(c > 0 for c in vals[0]), 'strictness row')
        require(all(c == 0 for c in vals[-1]), 'endpoint equality row')
    return {'name': name, 'interval': [str(lo), str(hi)], 'degree': list(deg),
            'count': len(flat), 'minimum': str(min(flat)),
            'zeros': sum(c == 0 for c in flat), 'sha256': digest(flat)}


def delta_coeffs(p, degree=4):
    # p(a,1), followed by a=1-delta; exact full polynomial substitution.
    local = suba(p, F(1), F(0))
    return [sum(c for (i, j), c in local.items() if i == k)
            for k in range(degree+1)]


def build_summary():
    b, oc, cc = coefficients()
    no, nc, r, d = phase_polynomials()
    require(no == quotient_norm(oc), 'full origin norm identity')
    require(nc == quotient_norm(cc), 'full polar norm identity')
    validate_cover(R_BOXES)
    validate_cover(D_BOXES)
    cells = [validate_cell(name, lo, hi, p)
             for name, p, boxes in [('R', r, R_BOXES), ('D', d, D_BOXES)]
             for lo, hi in boxes]
    require(sum(c['count'] for c in cells) == 3829, 'complete coefficient count')

    # Positive-real family, q=1: C=I. Its exact Taylor coefficients prove
    # the limiting upper weights without numerical asymptotics.
    cpos = {}
    for c in cc:
        cpos = add(cpos, c)
    t0 = mul(b, add(no, scale(ONE, -1)))
    tw = add(ONE, scale(cpos, -1))
    ts = add(ONE, scale(mul(cpos, cpos), -1))
    v0, vw, vs = delta_coeffs(t0), delta_coeffs(tw), delta_coeffs(ts)
    require(v0[:4] == [0, 0, F(4), F(4)], 'origin endpoint coefficients')
    require(vw[:4] == [0, 0, F(-16, 3), F(28, 3)], 'weak endpoint coefficients')
    require(vs[:4] == [0, 0, F(-32, 3), F(56, 3)], 'squared endpoint coefficients')
    mixed = [u+F(3, 4)*v for u, v in zip(v0, vw)]
    require(mixed[:4] == [0, 0, 0, F(11)], 'sharp positive-real face')

    # Explicit Gaussian-rational tuple in the abstract feasible domain.
    a = F(102, 149)
    q = F(51, 149), F(140, 149)
    bv = 1-a*a
    require(norm2(q) == 1, 'unit modulus')
    require(bv+2*a*q[0]-1 == 0, 'critical disk equality')
    require(F(1) >= 1/(1+a), 'radial lower bound')
    o, c = gaussian_sum(oc, a, q), gaussian_sum(cc, a, q)
    o2, c2 = norm2(o), norm2(c)
    iv = polar_modulus_integral(a, q[0])
    require(o2 == evaluate(no, a, q[0]), 'rational origin cross-check')
    require(c2 == evaluate(nc, a, q[0]), 'rational polar cross-check')
    require(o2 < F(1, 1000) and bv > F(1, 2) and iv < 1, 'strict rational controls')
    jw = o2-1+F(3, 4)*(1-iv)/bv
    js = o2-1+F(3, 8)*(1-c2)/bv
    require(jw < 0 and js < 0 and c2 < 1, 'two obstruction inequalities')
    lowerw, lowers = bv*(1-o2)/(1-iv), bv*(1-o2)/(1-c2)
    require(lowerw > F(3, 4) and lowers > F(3, 8), 'incompatible fixed weights')

    return {'status': 'PASS: exact arithmetic, no floating-point proof input',
            'full_norm_identities': 2, 'full_inverse_basis_identities': len(cells),
            'bernstein_coefficients': 3829, 'cells': cells,
            'positive_real_taylor': {'b_origin_excess': list(map(str, v0)),
             'one_minus_polar': list(map(str, vw)),
             'one_minus_polar_squared': list(map(str, vs)),
             'sharp_weight_numerator': list(map(str, mixed))},
            'rational_obstruction': {'a': str(a), 'q': list(map(str, q)),
             'origin': list(map(str, o)), 'origin_squared': str(o2),
             'polar': list(map(str, c)), 'polar_squared': str(c2),
             'modulus_integral': str(iv), 'weak_J_at_3_over_4': str(jw),
             'squared_J_at_3_over_8': str(js), 'weak_weight_lower': str(lowerw),
             'squared_weight_lower': str(lowers)}}


def mutation_controls():
    rejected = 0
    for boxes in [D_BOXES[:-1], D_BOXES+[D_BOXES[-1]]]:
        try:
            validate_cover(boxes)
        except ArithmeticError:
            rejected += 1
    _, _, r, d = phase_polynomials()
    for p in [add(d, {(0, 0): F(-1000000)}),
              add(d, {(37, 0): F(1)})]:
        try:
            validate_cell('D', F(0), F(1, 2), p)
        except ArithmeticError:
            rejected += 1
    deg, vals = bernstein(suba(r, F(0), F(1, 2)))
    vals[0][0] += 1
    require(inverse_bernstein(vals) != suba(r, F(0), F(1, 2)), 'coefficient mutation')
    rejected += 1
    require(rejected == 5, 'mutation controls')
    return rejected


def main():
    summary = build_summary()
    expected = json.loads(Path(__file__).with_name('expected.json').read_text())
    require(summary == expected, 'fixed compact manifest mismatch')
    rejects = mutation_controls()
    print('PASS: 3829 exact Bernstein coefficients; 2 complete norm identities;')
    print('9 complete inverse basis identities; 2 fixed-weight obstructions;')
    print('sharp weight 3/4 on the coalesced unit face; 5 mutations rejected.')
    print('No unrestricted polynomial or arbitrary two-value theorem is asserted.')


if __name__ == '__main__':
    main()
