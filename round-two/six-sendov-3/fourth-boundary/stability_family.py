"""Exact split-real construction proving sharpness of the next-profile rate.

Split two of the six real critical points by +/-lambda eta^(5/2).
The complete defining coefficients remain polynomial in eta and lambda^2.
Every original-root branch is checked through fifth order at lambda=1,
and the full generic fifth polynomial response retains lambda as a symbol.
"""
from fractions import Fraction as F


def build(context):
    p = context['p']
    K, Z = context['K'], context['Z']
    add, mul, power, scale = p.kadd, p.kmul, p.kpower, p.kscale
    eta, z = context['eta'], context['z']
    L0, Lp, opening = context['L0'], context['Lp'], context['opening']
    base_pol, base_obj = context['pol'], context['objective']
    marked, H = context['marked'], context['H']
    vals, repair = context['vals'], context['repair']
    lo, hi = context['lo'], context['hi']
    lam = p.kpv(2)
    checks = 0

    def equal(a, b, label):
        nonlocal checks
        if a != b:
            raise RuntimeError(label)
        checks += 1

    small_factor = add(z, scale(L0, -1))
    opposed_factor = add(power(add(z, scale(Lp, -1)), 2),
        scale(mul(eta, power(opening, 2)), H/2))
    derivative = scale(mul(power(small_factor, 4),
        add(power(small_factor, 2), scale(mul(power(lam, 2), power(eta, 5)), -1)),
        opposed_factor), 9)
    primitive = p.kintegrate(derivative)
    pol = add(primitive, scale(p.ksubstitute(primitive, 1, marked), -1))
    equal(p.ksubstitute(pol, 1, marked), {}, 'complete split-real anchor')
    for order in range(5):
        equal(p.kcoefficient(pol, order), p.kcoefficient(base_pol, order),
              'full split-real polynomial unchanged through fourth '+str(order))
    delta_pol = add(pol, scale(base_pol, -1))
    target = scale(mul(power(eta, 5), power(lam, 2),
                   add(power(z, 7), p.kpc(-1))), K(F(-9, 7)))
    equal(delta_pol, target, 'generic complete fifth response of split-real factors')
    # Every lambda dependence at this order is the displayed quadratic.
    equal(all(e[2] == 2 for e in delta_pol), True,
          'complete generic quadratic lambda dependence')
    branches = []
    for j, omega in enumerate(context['roots']):
        base_rad = [K(v) for v in context['branches'][j]['radial']]
        root, residual, radial, evaluate = p.residual_roots(pol, omega, 1, 0)
        equal(residual, [Z(0,q=omega.q)]*6, 'complete split-real residual '+str(j))
        equal(radial[:4], base_rad[:4], 'split-real lower radial coefficients '+str(j))
        response = ((omega**7).real_field()-1)/7
        equal(radial[4], base_rad[4]+response,
              'full fifth radial response '+str(j))
        if j == 0:
            equal(root, [omega, Z(-1,q=0)]+[Z(0,q=0)]*4,
                  'split-real exact marked root')
        elif j in [1,2,7,8]:
            equal((-radial[0]).interval(lo,hi)[0] > 0, True,
                  'split-real inactive first inward '+str(j))
        else:
            equal((-radial[4]).interval(lo,hi)[0] > 0, True,
                  'split-real active fifth inward '+str(j))
            equal((-response).interval(lo,hi)[0] > 0, True,
                  'split-real strictly more inward '+str(j))
        branches.append({'index':j, 'radial':[v.record() for v in radial],
                         'fifth_response':response.record()})

    # For D=marked-L0, the two split reciprocals sum to
    # 2/D+2 lambda^2 eta^5/[D(D^2-lambda^2 eta^5)]. Through eta5
    # their extra contribution is exactly 2 lambda^2 eta5/D^3.
    delta_D = add(marked, scale(L0,-1), p.kpc(-1))
    inverse_D = add(*(scale(power(delta_D,j), (-1)**j) for j in range(6)))
    extra = scale(mul(power(lam,2), power(eta,5), power(inverse_D,3)),2)
    objective = add(base_obj, extra)
    equal(extra, scale(mul(power(lam,2),power(eta,5)),2),
          'generic fifth critical-distance increase')
    for order in range(5):
        equal(p.kcoefficient(objective,order), p.kcoefficient(base_obj,order),
              'split-real objective unchanged through fourth '+str(order))
    first_h_error = add(scale(eta, vals['theta_star']),
                        scale(power(eta,2), vals['phi_star']))
    first_u_error = add(scale(eta, vals['mstar']), scale(power(eta,2), vals['nstar']),
                        scale(power(eta,3), repair))
    E_squared = add(scale(power(first_h_error,2),H), scale(power(first_u_error,2),8),
                    scale(mul(power(lam,2),eta),2))
    equal(p.kcoefficient(E_squared,0), {}, 'next-profile distance tends to zero')
    equal(p.kcoefficient(E_squared,1), scale(power(lam,2),2),
          'positive sharp next-profile distance-square limit')
    record = {'checks':checks, 'generic_split_parameter':'lambda',
              'profile_limit_squared':'2 lambda^2',
              'fifth_objective_increase':'2 lambda^2',
              'generic_polynomial_hash':p.kphash(pol),
              'generic_fifth_response_hash':p.kphash(delta_pol),
              'generic_objective_hash':p.kphash(objective),
              'next_profile_distance_squared_hash':p.kphash(E_squared),
              'all_nine_root_branches_at_lambda1':branches}
    return record, {'delta_pol':delta_pol, 'target':target,
                    'profile_limit':p.kcoefficient(E_squared,1), 'p':p}
