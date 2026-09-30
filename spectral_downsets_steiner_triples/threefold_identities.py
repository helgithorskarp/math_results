"""Portable Q(v) identities and positive coefficient certificates at v=13+z.

Imports the earlier integer polynomial arithmetic, not a CAS or matrix solver.
The written proof supplies the incidence and spectral bridges.
Author: six-downset-2, researcher.
"""
from fractions import Fraction as F
from twofold_identities import RationalFunction as RF, shifted


def run():
    v = RF((0, 1))
    r, m, b, s, N = 3*(v-1)/2, v*(v-1)/2, v*(v-1)/2, (5*v-3)/2, v*v+1
    a = RF(-1)
    w = (v**3-6*v*v+23*v-36)/((v-4)*(v-3)*(v-2))
    c = (v*v-6*v+11)/((v-3)*(v-2))
    d = (v*v-v-4)/((v-4)*(v-3))
    h = (v*v+2*v-11)/((v-5)*(v-3))
    t = (v-1)/(v-5)
    alpha1, alpha2 = s-c*(v-3), s+c
    beta = t-d*d/alpha2
    gamma = t-4*d*d/(alpha2*(v-2))+d*d*(v-4)**2/((v-2)*alpha1)
    red = t*(v-6)/(v-2)+d*d*(v-4)**2/((v-2)*alpha1)
    mu = 2*v*(v**3-5*v*v+v+13)/((v-3)*(v-2)*(3*v*v-v-16))
    delta = N-25*v/2
    k = (v-2)*(v-3)/2
    eta = delta/(16*m*k)
    A = (r-3)*d*d*(v-4)**2/(v-2)
    eqs = {
        'triple_star': h+(v-4)*d+(r-9)*t-s,
        'triple_row': 1+s+(v-3)*h-6*t+(v-3)*(v-4)*d/2+(b-3*r+8)*t-N,
        'pair_star': w+(v-3)*c+(r-6)*d-s,
        'pair_row': 1+s+(v-2)*w-3*d+(v-2)*(v-3)*c/2+(b-2*r+3)*d-N,
        'point_star': a+(v-2)*w-3*d+(r-3)*h-9*t-s,
        'point_row': 1+s+(v-1)*a+(v-1)*(v-2)*w/2-r*d+(b-r)*h-2*r*t-N,
        'constant_pair': s+c-2*c*(v-1)+(c-1)*m-4,
        'constant_cross': 3*d-2*d*r+(d-1)*b+2,
        'constant_triple': s+8*t-3*r*t+(t-1)*b-1,
        'alpha1': alpha1-(3*v*v-v-16)/(2*(v-2)),
        'alpha2': alpha2-(5*v**3-26*v*v+33*v+4)/(2*(v-3)*(v-2)),
        'Schur_reduction': gamma-4*beta/(v-2)-red,
        'Schur_margin': s-t-(r-3)*red-mu,
        'gap': delta-(2*v*v-25*v+2)/2,
        'eta': eta-(2*v*v-25*v+2)/(8*v*(v-1)*(v-2)*(v-3)),
        'eight_mk_minus_v4': 8*m*k-v**4-v*(v**3-12*v*v+22*v-12),
        'constant_core_trace': s-a+(a-1)*v+4+1-(v+9)/2,
        'row1_gap': 25*v/2-73*v/6-v/3,
        'row2_gap': 25*v/2-(7*v+6)-(11*v-12)/2,
        'row3_gap': 25*v/2-(49*v/6+RF(33,(2,)))-(26*v-99)/6,
    }
    for name, expression in eqs.items():
        assert expression.is_zero(), name
    records = {
        'w_le_3_over_2': ((32, -15, 1), 2*(v-4)*(v-3)*(v-2)/v, RF(3,(2,))-w),
        'c_lt_1': ((-5, 1), (v-3)*(v-2), 1-c),
        'd_le_2': ((28, -13, 1), (v-4)*(v-3), 2-d),
        'h_le_5_over_2': ((97, -44, 3), 2*(v-5)*(v-3), RF(5,(2,))-h),
        't_le_3_over_2': ((-13, 1), 2*(v-5), RF(3,(2,))-t),
        'alpha1_gt_v': ((-16, 3, 1), 2*(v-2), alpha1-v),
        'alpha2_gt_2v': ((4, 9, -6, 1), 2*(v-3)*(v-2), alpha2-2*v),
        'mu_gt_half': ((96, -22, -3, -4, 1), 2*(v-3)*(v-2)*(3*v*v-v-16), mu-RF(1,(2,))),
        'A_lt_6v2': ((-48, -24, 93, -54, 9), 2*(v-3)*(v-2), 6*v*v-A),
        'cap_gap_positive': ((2, -25, 2), 1, 2*delta),
        'eight_mk_gt_v4': ((-12, 22, -12, 1), 1, (8*m*k-v**4)/v),
        'mu_denominator_positive': ((-16, -1, 3), 1, 3*v*v-v-16),
        'beta_bound_positive': ((-2, 1), 1, v-2),
        'repair_bound_positive': ((-12, 1), 1, v-12),
        'row1_margin': ((0, 1), 1, v),
        'row2_margin': ((-12, 11), 1, 11*v-12),
        'row3_margin': ((-99, 26), 1, 26*v-99),
        'constant_core_upper_margin': ((-9, 24), 1, 25*v-(v+9)),
    }
    positive, weak = {}, {}
    for name, (poly, den, expr) in records.items():
        assert (expr-RF(poly)/den).is_zero(), name
        coeffs = shifted(poly, base=13)
        assert any(coeffs) and all(x >= 0 for x in coeffs), name
        if coeffs[0] == 0:
            assert name == 't_le_3_over_2'
            weak[name] = coeffs
        else:
            positive[name] = coeffs
    # The four radical replacements in the three-layer norm proof.
    assert F(9,4)**2 > F(9,2)
    assert F(5,4)**2 > F(3,2)
    assert F(17,4)**2 > 18
    assert F(13,1) > 9  # sqrt(v)<=v/3 throughout the stated real domain.
    assert F(3,2)+2*F(9,4) == 6
    assert F(5,2)*F(5,4)+F(3,2)*F(17,4) == F(19,2)
    return {'agent': 'six-downset-2', 'role': 'researcher', 'domain': 'Q(v)',
            'real_sign_domain': 'v>=13; design applications are odd integer orders',
            'zero_polynomial_identities': len(eqs)+len(records),
            'identity_names': list(eqs),
            'strict_positive_coefficients_in_v_minus_13': positive,
            'nonnegative_coefficients_in_v_minus_13': weak,
            'radical_bounds': ['sqrt(9/2)<9/4', 'sqrt(3/2)<5/4', 'sqrt18<17/4',
                               'sqrt(v)<=v/3 forv>=13']}


if __name__ == '__main__':
    import json
    print(json.dumps(run(),indent=2,sort_keys=True))
