"""Reconstruct complete primitive factors from actual physical coordinates.

No new target factor, certificate, expected record, or executable is input.
The own previously published expression/radical/frame backend is credited.
"""
from fractions import Fraction as F
from digit import T, Z, expr, coefficients, monomials, prove_zero
from geometry import model, dot, LABELS, CONTACTS


def divide(numerator, denominator):
    if not denominator:
        raise ValueError('zero polynomial divisor')
    remaining = dict(numerator)
    leading = max(denominator)
    out = {}
    while remaining:
        top = max(remaining)
        power = tuple(top[k] - leading[k] for k in range(2))
        if min(power) < 0:
            raise ValueError('nonzero full polynomial remainder')
        value, remainder = divmod(remaining[top], denominator[leading])
        if remainder:
            raise ValueError('nonintegral polynomial quotient')
        out[power] = out.get(power, 0) + value
        for (i, j), coefficient in denominator.items():
            key = (i + power[0], j + power[1])
            value2 = remaining.get(key, 0) - value * coefficient
            if value2:
                remaining[key] = value2
            else:
                remaining.pop(key, None)
        if len(out) > 1000:
            raise RuntimeError('fixed quotient guard; no mathematical conclusion')
    return {k: v for k, v in out.items() if v}


def polynomial(rows):
    return monomials([(i, j, v) for (i, j), v in sorted(rows.items())])


def rows_text(rows):
    return [[i, j, str(v)] for (i, j), v in sorted(rows.items())]


def rebuild():
    m = model()
    a, b, c, D, C, K, J, O, R = (m[k] for k in
                                  ['a', 'b', 'c', 'D', 'C', 'K', 'J', 'Omega', 'R'])
    Y, t, z = m['Y'], T, Z
    L = 7*t*t + 2*t - 1
    Q = a*D*z*z - 2*D*z + 2*t*t - t + 1
    records, derived = {}, {}

    def scalar(name, expression):
        records[name] = prove_zero(expression)

    def radical(name, expression):
        scalar(name + '_constant', expression.p)
        scalar(name + '_linear', expression.q)

    # Rebind the full actual unit/contact frame, including the larger local box.
    for i in LABELS:
        radical('entire_original_unit_' + str(i), dot(Y[i], Y[i]) - O*O)
    for i, j in CONTACTS:
        radical('entire_original_contact_' + str(i) + '_' + str(j),
                dot(Y[i], Y[j]) - O*O*t)
    # These are literal numerator identities, not a sampled core or Gram input.
    for i, j in [(6, 7), (6, 9), (7, 9), (4, 12), (8, 10)]:
        radical('physical_noncontact_' + str(i) + '_' + str(j),
                dot(Y[i], Y[j])*a*a - O*O*K)
    scalar('positive_Omega_factorization',
           O - m['h']*J*b*b*c*c*a**8*C*(b*z+1)**2*Q)
    scalar('positive_Q_identity', a*Q - D*(a*z-1)**2 - 4*t*t)
    scalar('active_center_equation', -L + 2*t*a*a - b*b*c)
    scalar('active_leaf_equation', -t*L + a*a + K - b*b*c)
    determinant_numerator = a**4 - 2*t*t*a**4 + 2*t*t*K*a*a - K*K
    scalar('intrinsic_strict_Gram',
           determinant_numerator - b**4*c*(3*t+1)**2)
    norm_numerator = t*t*(2*a*a-L)
    scalar('intrinsic_norm', norm_numerator*b*c - t*t*(5*t+3)*b*b*c)
    scalar('norm_excess', t*t*(5*t+3)-b*c-a*(5*t*t-1))

    roles = [
        ('067', (0, 6, 7), [-5, -14, 20], 15,
         a**6*b*b*c*c*(3*t-1)*(b*z+1)),
        ('579', (5, 7, 9), m['N'][10], t*a*a,
         t*a**10*b*b*c*c*(3*t-1)*(b*z+1)**2*Q),
        ('6911', (11, 6, 9), [-8, 12, -5], 9,
         a**5*b*b*c*c*(3*t-1)*(b*z+1))]
    for name, (center, i, j), normal, rhs, multiplier in roles:
        vertex_numerator = [((Y[i][k]+Y[j][k])*a*a-Y[center][k]*L)*t
                            for k in range(3)]
        excess = dot(vertex_numerator, normal) - O*b*b*c*rhs
        factor_rows = coefficients(multiplier)
        for letter, raw in [('A', excess.p), ('B', excess.q)]:
            new = divide(coefficients(raw), factor_rows)
            derived[letter + name] = new
            scalar('complete_derived_' + letter + name,
                   raw - polynomial(new)*multiplier)
    for name, multiplier in [('067', a*b**4*c*c*J*Q),
                             ('579', 4*a*a*b**4*c*c*J)]:
        raw = polynomial(derived['B'+name])**2*R-polynomial(derived['A'+name])**2
        new = divide(coefficients(raw), coefficients(multiplier))
        derived['H'+name] = new
        scalar('complete_derived_H'+name, raw-polynomial(new)*multiplier)

    # Entire B reflection circuits, not a prescribed active basis-product word.
    N = m['N']
    for k in range(3):
        radical('physical_B8_'+str(k), N[8][k]*a+N[1][k]*a-(N[2][k]+N[4][k])*2*t)
        radical('physical_B10_'+str(k), N[10][k]*a+N[4][k]*a-(N[1][k]+N[2][k])*2*t)
        radical('physical_B12_'+str(k), N[12][k]*a*a-N[1][k]*(2*t*a+4*t*t)
                -N[2][k]*(4*t*t-a*a)+N[4][k]*2*t*a)
    return m, derived, records


if __name__ == '__main__':
    import json
    m, factors, identities = rebuild()
    print(json.dumps({'derived_entire_primitive_rows': {k: rows_text(v) for k,v in factors.items()},
                      'whole_original_coordinate_identities': identities,
                      'new_target_factor_input': False,
                      'own_prior_backend_reuse_explicit': True}, sort_keys=True,separators=(',',':')))
