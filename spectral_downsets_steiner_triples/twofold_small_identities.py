"""Exact all-order margins extending the twofold certificate to v>=9.

Standard-library polynomial arithmetic over Q(v), with positive-denominator
identities and nonnegative coefficients after v=9+z (or v=10+z for norms).
No interpolation or floating-point PSD assertion. six-downset-2, researcher.
"""
from fractions import Fraction as F
from twofold_identities import RationalFunction as RF, run as base_identities, shifted
from uniform_twofold import weights


def run():
    v = RF((0, 1))
    den = (v-3)*(v-4)
    w = 1+4*v*(2*v-5)/(3*(v-2)*den)
    c = 1+4/(3*(v-2)*(v-3))
    d = (v*v-v-4)/den
    h = (v*v-7)/den
    t = (v-1)/(v-4)
    m, k = v*(v-1)/2, (v-2)*(v-3)/2
    delta = (5*v*v-41*v+6)/6
    A = (v*v-v-4)**2/((v-3)*(v-2))
    records = {
        'w_le_7_over_4': ((-216, 314, -113, 9), 12*(v-2)*den, RF(7, (4,))-w),
        'c_le_4_over_3': ((2, -5, 1), 3*(v-2)*(v-3), RF(4, (3,))-c),
        'd_le_7_over_3': ((96, -46, 4), 3*den, RF(7, (3,))-d),
        'h_le_5_over_2': ((74, -35, 3), 2*den, RF(5, (2,))-h),
        't_le_8_over_5': ((-27, 3), 5*(v-4), RF(8, (5,))-t),
        'alpha1_gt_v': ((-16, 6), 3*(v-2), (3*v*v-16)/(3*(v-2))-v),
        'mu_gt_one': ((-12, 3, 1), 1, v*v+3*v-12),
        'cap_gap_positive': ((6, -41, 5), 1, 6*delta),
        'eta_lt_inverse_v2': ((-72, 126, -31, 7), 1,
                              6*(8*m*k-delta*v*v)/v),
        'A_lt_4v2': ((-16, -8, 31, -18, 3), (v-3)*(v-2), 4*v*v-A),
        'beta_lower_positive': ((-49, 18), 1, 18*v-49),
        'repaired_Schur_positive': ((-8, 1), 1, v-8),
        'constant_layer_cap': ((-10, 20), 1, 21*v-(v+10)),
    }
    positives = {}
    nonnegative = {}
    for name, (numerator, denominator, expression) in records.items():
        assert (expression-RF(numerator)/denominator).is_zero(), name
        coefficients = shifted(numerator, base=9)
        assert all(x >= 0 for x in coefficients) and any(coefficients), name
        if coefficients[0] == 0:
            # Equality at v=9 is allowed only for this weak weight bound.
            assert name == 't_le_8_over_5'
            nonnegative[name] = coefficients
        else:
            positives[name] = coefficients

    row_bounds = [RF(18, (5,))+(RF(21, (4,))+RF(53, (10,)))*RF(8, (25,)),
                  2+RF(21, (4,))*RF(8, (25,))+RF(7, (3,)),
                  2+RF(53, (10,))*RF(8, (25,))+RF(7, (3,))]
    row_values = [F(872, 125), F(451, 75), F(2261, 375)]
    for expression, value in zip(row_bounds, row_values):
        assert (expression-RF(value.numerator, (value.denominator,))).is_zero()
    norm10 = {'row1_gap': (0, 3), 'row2_gap': (-25, 74),
              'row3_gap': (-2625, 364), 'sqrt_v_bound': (-625, 64)}
    for name, poly in norm10.items():
        coefficients = shifted(poly, base=10)
        assert coefficients[0] > 0 and all(x >= 0 for x in coefficients), name
        norm10[name] = coefficients
    assert (7*v-row_bounds[0]*v-RF((0, 3))/(125)).is_zero()
    assert (7*v-row_bounds[1]*v-RF(1, (3,))-RF((-25, 74))/75).is_zero()
    assert (7*v-row_bounds[2]*v-7-RF((-2625, 364))/375).is_zero()
    # Squared radical bounds; each right side is nonnegative on its domain.
    assert (((v-RF(5, (2,)))**2-(v-2)*(v-3))-RF(1, (4,))).is_zero()
    radical9 = [(7, F(8, 3)), (6, F(5, 2)), (24, F(5)), (42, F(13, 2))]
    for radicand, bound in radical9:
        assert bound*bound >= radicand
    assert F(3, 2)**2 > 2 and F(7, 4)**2 > 3 and F(5, 2)**2 > 6
    w9 = weights(9)
    assert w9 == {'a': F(-2, 3), 'b': F(61, 35), 'c': F(65, 63),
                  'd': F(34, 15), 'h': F(37, 15), 't': F(8, 5)}
    diagonal = [17-w9['a']+9*w9['t'], 17+w9['c'], 17+5*w9['t']]
    cross = [w9['b']*F(8, 3)+4*w9['d'],
             w9['h']*F(5, 2)+5*w9['t'], w9['d']*(F(13, 2)+F(5, 2))]
    rows9 = [diagonal[0]+cross[0]+cross[1],
             diagonal[1]+cross[0]+cross[2],
             diagonal[2]+cross[1]+cross[2]]
    assert rows9 == [F(12589, 210), F(16426, 315), F(1787, 30)]
    assert all(x < 63 for x in rows9)
    return {'agent': 'six-downset-2', 'role': 'researcher', 'domain': 'Q(v)',
            'input_scope': 'every simple 2-(v,3,2) design, v>=9',
            'base_algebra': base_identities(),
            'additional_zero_polynomial_identities': len(records)+len(row_values)+4,
            'strict_positive_coefficients_in_v_minus_9': positives,
            'nonnegative_coefficients_in_v_minus_9': nonnegative,
            'strict_positive_coefficients_in_v_minus_10': norm10,
            'v9_diagonal_bounds': [str(x) for x in diagonal],
            'v9_cross_bounds': [str(x) for x in cross],
            'v9_row_bounds': [str(x) for x in rows9],
            'v9_row_gaps': [str(63-x) for x in rows9]}


if __name__ == '__main__':
    import json
    print(json.dumps(run(), indent=2, sort_keys=True))
