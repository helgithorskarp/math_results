"""Portable exact polynomial replay of the BC-adjusted residual.

No CAS, interpolation, solver status or sampled positivity is an input.
All sparse coefficients of each polynomial are regenerated explicitly.
The old original moment identities and lower BC bound are credited.
"""
from forms import F, require, encode, exact


def add(*polynomials):
    out = {}
    for polynomial in polynomials:
        for power, value in polynomial.items():
            out[power] = out.get(power, F(0))+value
    return {power: value for power, value in out.items() if value}


def scale(polynomial, coefficient):
    return {power: value*coefficient for power, value in polynomial.items() if value*coefficient}


def mul(a, b):
    out = {}
    for (i, j), value in a.items():
        for (r, s), coefficient in b.items():
            power = (i+r, j+s)
            out[power] = out.get(power, F(0))+value*coefficient
    return {power: value for power, value in out.items() if value}


def constant(n):
    return {(0, 0): F(n)} if n else {}


Q, K = {(1, 0): F(1)}, {(0, 1): F(1)}


def divide(numerator, denominator):
    quotient, remainder = {}, dict(numerator)
    leading, coefficient = max(denominator.items())
    while remainder:
        power, value = max(remainder.items())
        delta = tuple(x-y for x, y in zip(power, leading))
        require(min(delta) >= 0, 'nondivisible whole polynomial')
        monomial = {delta: value/coefficient}
        quotient = add(quotient, monomial)
        remainder = add(remainder, scale(mul(monomial, denominator), -1))
    require(mul(quotient, denominator) == numerator, 'entire accepted polynomial division identity')
    return quotient


def coefficients(q=Q, k=K):
    q2, k2 = mul(q, q), mul(k, k)
    q3 = mul(q2, q)
    ell = add(scale(q, 5), constant(4), scale(k, -1))
    g2 = add(q2, scale(q, 7), constant(8), scale(k, -2))
    T2 = mul(q, g2)
    V2 = add(mul(ell, g2), scale(mul(q, add(scale(q, 3), constant(4))), -8))
    Aq = add(mul(add(scale(k, 2), constant(1)), q2), mul(k, q), scale(k, -2))
    Bq = add(mul(q, add(mul(add(q, scale(k, -1)), add(scale(q, 3), constant(4))), scale(k, 3))), scale(k, 2))
    C0 = mul(ell, add(constant(1), scale(k, -1)))
    E2 = add(q2, mul(add(constant(13), scale(k, -6)), q), scale(k2, 2), scale(k, -10), constant(14))
    S2 = add(mul(mul(q, add(q, constant(1))), add(scale(q, 3), constant(5))),
             scale(add(q, constant(1)), 6), scale(k, -4))
    cost_den = scale(add(scale(q3, 12), scale(q2, 19), scale(q, 4), constant(-4)), 3)
    cost_num = mul(mul(add(scale(q, 3), constant(2)), add(scale(q, 3), constant(4))),
                   add(scale(q2, 3), scale(q, 3), constant(-2)))
    vp = add(mul(cost_den, V2), scale(cost_num, 4))
    cp = add(mul(cost_den, C0), scale(cost_num, 2))
    dn = add(mul(mul(q2, T2), vp), scale(mul(cost_den, mul(Bq, Bq)), -4))
    an = scale(mul(q, add(mul(vp, Aq), scale(mul(Bq, cp), 2))), 2)
    bn = scale(add(mul(mul(q2, T2), cp), scale(mul(cost_den, mul(Bq, Aq)), 2)), 2)
    derivative = add(mul(S2, dn), scale(add(mul(an, q), mul(bn, add(scale(q, 2), scale(k, -1)))), -4))
    residual = add(mul(mul(q, add(mul(cost_den, E2), scale(cost_num, 4))), dn),
                   scale(mul(mul(cost_den, an), Aq), -2), scale(mul(mul(q, bn), cp), -2))
    return {'cap_block_denominator': dn, 'a_numerator': an, 'b_numerator': bn,
            'Delta_numerator': derivative, 'residual_numerator': residual,
            'cost_denominator': cost_den}


def evaluate(polynomial, q, k):
    return sum(value*q**i*k**j for (i, j), value in polynomial.items())


def scalars(q, k):
    require(type(q) is int and type(k) is int and k >= 2 and q >= 3*k, 'proved uniform quadrant')
    N, s = (q*q+13*q+16)//2-k, 3*q+4
    g, ell, h = N-s, 5*q+4-k, F(1, 3*q+5)
    e = F(q*q+(13-6*k)*q+2*k*k-10*k+14, 2)
    A, C0 = F((2*k+1)*q+k)-F(2*k, q), F(ell*(1-k))
    T, B, V = F(q*g), -(q-k)*s-k*(3+F(2, q)), F(ell*g-4*q*s)
    S = F(q*(q+1), 2)+3*(q+1)*h-2*k*h
    cost = F((3*q+2)*(3*q+4)*(3*q*q+3*q-2), 3*(12*q**3+19*q*q+4*q-4))
    determinant = T*(V+2*cost)-B*B
    require(T > 0 and determinant > 0, 'positive adjusted homogeneous cap block')
    aa = ((V+2*cost)*A-B*(C0+2*cost))/determinant
    bb = (T*(C0+2*cost)-B*A)/determinant
    residual = e+2*cost-aa*A-bb*(C0+2*cost)
    slope = S-2*h*(aa*q+bb*(2*q-k))
    require(slope > 0, 'positive adjusted original cap slope')
    old_determinant = T*V-B*B
    a0, b0 = (V*A-B*C0)/old_determinant, (T*C0-B*A)/old_determinant
    old_residual = e-a0*A-b0*C0
    require(residual == old_residual+2*cost*(1-b0)**2*old_determinant/determinant,
            'entire exact rank-one adjusted residual identity')
    old_combined = old_residual+2*cost*(1-b0)**2
    require(old_combined-residual == 4*cost*cost*T*(1-b0)**2/determinant >= 0,
            'provable weak dominance over the previous combined obstruction')
    return {'q': q, 'k': k, 'cost': cost, 'a': aa, 'b': bb, 'adjusted_cap_minimum': residual,
            'Delta_pairing': slope, 'determinant': determinant,
            'old_combined_obstruction': old_combined,
            'moment': [[e, A, C0], [A, T, B], [C0, B, V]]}


def positive_coefficients(p, name):
    require(p.get((0, 0), F(0)) > 0 and all(value >= 0 for value in p.values()),
            'ALL shifted coefficients positive on the complete quadrant: '+name)


def check():
    ordinary = coefficients()
    quotient = divide(ordinary['residual_numerator'], mul(Q, ordinary['cost_denominator']))
    # x>=0,u>=0 is exactly k=2+x,q=3k+u.
    shifted = coefficients(add(constant(6), scale(K, 3), Q), add(constant(2), K))
    signs = {}
    for name in ('cap_block_denominator', 'Delta_numerator'):
        p = shifted[name]
        positive_coefficients(p, name)
        signs[name] = {'constant': p[(0, 0)], 'coefficient_count': len(p),
                       'coefficients': [[list(power), value] for power, value in sorted(p.items())]}
    controls = []
    for q, k in ((6, 2), (15, 5), (20, 6), (21, 6), (22, 6), (74, 15), (240, 50)):
        row = scalars(q, k)
        at = lambda name: evaluate(ordinary[name], q, k)
        dn = at('cap_block_denominator')
        require(dn == 4*q*q*at('cost_denominator')*row['determinant'] and
                at('a_numerator') == dn*row['a'] and at('b_numerator') == dn*row['b'] and
                at('Delta_numerator') == 2*(3*q+5)*dn*row['Delta_pairing'] and
                evaluate(quotient, q, k) == 2*dn*row['adjusted_cap_minimum'],
                'entire exact rational denominator identities')
        controls.append(row)
    return {'coverage': 'ALL integers k>=2,q>=3k by full shifted coefficients; controls are calibration only',
            'signs': signs, 'necessary_polynomial': [[list(power), value] for power, value in sorted(quotient.items())],
            'necessary_polynomial_count': len(quotient), 'controls': controls,
            'old_moments_are_credited9582': True, 'lower_BC_orientation_are_credited9766': True,
            'new_scope_is_only_necessary_core_face_compression': True}
