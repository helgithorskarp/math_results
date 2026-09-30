"""Reconstruct the complete exact two-phase certificate and radial constants."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import hashlib
import json
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from algebra import (ONE, A, B, C, X, add, scale, mul, power, degrees,
                     multinomial_coefficients, quotient_norm, phase_polynomials,
                     coupled_axis, coupled_horner, affine_axis,
                     bernstein, inverse_bernstein)

BOXES = [(F(0), F(1, 2)), (F(1, 2), F(5, 8)), (F(5, 8), F(3, 4)),
         (F(3, 4), F(7, 8)), (F(7, 8), F(1))]
DEGREES = {'R': (22, 8, 8), 'K': (42, 16, 16)}


def require(ok, message):
    if not ok:
        raise ArithmeticError(message)


def validate_cover(boxes):
    require(boxes[0][0] == 0 and boxes[-1][1] == 1, 'outer coverage')
    require(all(lo < hi for lo, hi in boxes), 'nonempty cells')
    require(all(boxes[j][1] == boxes[j+1][0] for j in range(len(boxes)-1)),
            'missing or duplicate cells')


def validate_values(name, ds, vals):
    require(ds == DEGREES[name], 'complete degree extent')
    require(all(len(m) == 3 and all(0 <= m[j] <= ds[j] for j in range(3))
                for m in vals), 'coefficient index extent')
    require(all(z >= 0 for z in vals.values()), 'negative certificate coefficient')
    if name == 'R':
        require(len(vals) == (ds[0]+1)*(ds[1]+1)*(ds[2]+1)
                and all(z > 0 for z in vals.values()), 'strict positive R')


def digest(values):
    return hashlib.sha256(('\n'.join(str(z) for z in values)+'\n').encode()).hexdigest()


def validate_cell(name, lo, hi, p):
    local = affine_axis(p, 0, lo, hi)
    ds, vals = bernstein(local)
    validate_values(name, ds, vals)
    require(inverse_bernstein(ds, vals) == local, 'full inverse basis identity')
    indices = list(product(*(range(n+1) for n in ds)))
    flat = [vals.get(m, F(0)) for m in indices]
    zeros = [list(m) for m, z in zip(indices, flat) if not z]
    if name == 'K':
        require(not zeros if hi < 1 else len(zeros) == 2, 'K zero pattern')
    return {'name': name, 'interval': [str(lo), str(hi)], 'degree': list(ds),
            'count': len(flat), 'minimum': str(min(flat)),
            'zero_indices': zeros, 'sha256': digest(flat)}


def verify_projection():
    # Here c,x represent positive radii r,s. Clear the denominators r*s
    # in 1/r+1/s-b(r+s) = 2a^2+(2-a^2)(2-r-s)
    #                            +(r-1)^2/r+(s-1)^2/s.
    rs = mul(C, X)
    a2 = power(A, 2)
    sigma = add(scale(ONE, 2), scale(add(C, X), -1))
    left = add(add(C, X), scale(mul(mul(B, add(C, X)), rs), -1))
    right = add(scale(mul(a2, rs), 2),
                mul(mul(add(scale(ONE, 2), scale(a2, -1)), sigma), rs))
    right = add(right, mul(power(add(C, scale(ONE, -1)), 2), X))
    right = add(right, mul(power(add(X, scale(ONE, -1)), 2), C))
    require(left == right, 'complete cleared projection identity')


def radial_constants():
    origin = F(72)*F(199, 99)**7*F(100, 99)
    polar = F(8)*F(63, 50)**7
    require(origin < 10000 and polar < 50, 'exact telescoping bounds')
    require(F(1, 40000) <= F(1, 100), 'radial window')
    require(F(40000)*F(1, 40000) == 1, 'square window')
    require(F(50)*F(1, 40000) < 1, 'positive polar lower bound')
    require(F(1, 100)+F(1, 1000) == F(11, 1000), 'maximum margin')
    require(F(11, 1000*120100) < F(1, 40000), 'large-radius gap case')
    return {'origin_telescoping': str(origin), 'origin_upper': '10000',
            'polar_telescoping': str(polar), 'polar_upper': '50',
            'radial_window': '1/40000', 'D_upper_coefficient': '120100',
            'necessary_gap_delta2_coefficient': '1/12010000',
            'necessary_gap_angular_coefficient': '1/120100000'}


def build_summary(progress=False):
    hs, oc, cc, no, nc, r, h, k = phase_polynomials()
    require(hs == multinomial_coefficients(), 'nine full quadratic coefficients')
    require(no == quotient_norm(oc), 'full origin norm identity')
    require(nc == quotient_norm(cc), 'full polar norm identity')
    require(mul(B, h) == add(mul(r, r), scale(nc, -1)), 'complete b-factor identity')
    verify_projection()
    coupled = {}
    for name, p in [('R', r), ('K', k)]:
        q = coupled_axis(coupled_axis(p, 1), 2)
        require(q == coupled_horner(coupled_horner(p, 1), 2),
                'complete independent coupled substitution')
        require(degrees(q) == DEGREES[name], 'complete coupled degree')
        coupled[name] = q
    validate_cover(BOXES)
    cells = []
    for name in ['R', 'K']:
        for lo, hi in BOXES:
            row = validate_cell(name, lo, hi, coupled[name])
            cells.append(row)
            if progress:
                print('Checked', name, str(lo), str(hi), row['count'], flush=True)
    require(sum(row['count'] for row in cells) == 71450, 'complete coefficient count')
    return {'status': 'PASS: exact arithmetic; no floating-point proof input',
            'full_quadratic_coefficient_identities': 9, 'full_norm_identities': 2,
            'full_b_factor_identities': 1, 'full_coupled_substitution_identities': 2,
            'full_inverse_basis_identities': 10, 'full_projection_identities': 1,
            'bernstein_coefficients': 71450, 'cells': cells,
            'margin': {'delta2_coefficient': '1/100', 'angular_coefficient': '1/1000'},
            'radial_constants': radial_constants()}


def mutation_controls():
    rejected = 0
    for boxes in [BOXES[:-1], BOXES+[BOXES[-1]]]:
        try:
            validate_cover(boxes)
        except ArithmeticError:
            rejected += 1
    for ds, vals in [(DEGREES['K'], {(0, 0, 0): F(-1)}),
                     ((43, 16, 16), {(0, 0, 0): F(1)})]:
        try:
            validate_values('K', ds, vals)
        except ArithmeticError:
            rejected += 1
    # Change a coefficient in a small tensor with a completely known inverse.
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
    print('PASS: 71450 exact Bernstein coefficients; 2 complete norm identities;')
    print('10 complete inverse basis identities; 2 independent phase substitutions;')
    print('quantitative two-unit-phase margin and abstract radial gap; 5 mutations rejected.')
    print('The unrestricted two-value and general first-power conjectures remain unproved.')


if __name__ == '__main__':
    main()
