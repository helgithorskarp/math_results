#!/usr/bin/env python3
"""Exact joint origin/polar certificate; no grid or floating-point proof."""
from fractions import Fraction as Q
from math import factorial, comb

from origin import trim, add, scale, mul, power, value, to_a, bernstein, formulas, require, gaussian_mul, digest, polarization_checks

MU = Q(22096964222976, 21378414915091)
CUTOFF = Q(5, 8)


def divide(p, divisor):
    p, divisor = trim(p), trim(divisor)
    require(divisor != [0], 'nonzero divisor')
    quotient = [Q(0)] * max(1, len(p)-len(divisor)+1)
    while p != [0] and len(p) >= len(divisor):
        k = len(p)-len(divisor)
        v = p[-1]/divisor[-1]
        quotient[k] += v
        p = add(p, scale([Q(0)]*k+divisor, -v))
    return trim(quotient), p


def jet_product(p, q):
    """Literal Gaussian eps/t product, no derivative or Hessian formula."""
    out = {}
    for (e, k), z in p.items():
        for (f, l), w in q.items():
            if e+f > 2:
                continue
            key = (e+f, k+l)
            result = gaussian_mul(z, w)
            old = out.get(key, ([Q(0)], [Q(0)]))
            out[key] = tuple(add(u, v) for u, v in zip(old, result))
    return out


def literal_polar(direction):
    a, d = [Q(0), Q(1)], [Q(1), Q(-1)]
    gammas = [9]+[1]*7
    radial2_numerators = [scale(a, -Q(sum(v*v for v in direction[1:]), 2))]
    radial2_numerators += [scale(a, Q(v*v, 2)) for v in direction[1:]]
    product = {(0, 0): ([Q(1)], [Q(0)])}
    for g, radial2, v in zip(gammas, radial2_numerators, direction):
        q2_num = add(radial2, [Q(-g*v*v, 2)])
        # b q0 = g(1-a), b q1 = i g(1-a)v, b q2 = (1-a)q2_num.
        factor = {(0, 0): (a, [Q(0)]),
                  (0, 1): (scale(d, g), [Q(0)]),
                  (1, 1): ([Q(0)], scale(d, g*v)),
                  (2, 1): (mul(d, q2_num), [Q(0)])}
        product = jet_product(product, factor)
    re0 = add(*(scale(z[0], Q(1, k+1)) for (e, k), z in product.items() if e == 0))
    im1 = add(*(scale(z[1], Q(1, k+1)) for (e, k), z in product.items() if e == 1))
    re2 = add(*(scale(z[0], Q(1, k+1)) for (e, k), z in product.items() if e == 2))
    require(re0 == [Q(1)], 'complete polar coalesced equality')
    # Twice the full modulus phase coefficient, before division by b.
    return add(scale(re2, 2), power(im1, 2)), im1


def polar_checks(p):
    a, plus, d = [0, 1], [1, 1], [1, -1]
    basis = [[int(i == j) for j in range(8)] for i in range(8)]
    directions = list(basis)
    for i in range(8):
        for j in range(i+1, 8):
            directions += [[basis[i][k]+sign*basis[j][k] for k in range(8)] for sign in (1, -1)]
    rows = []
    for v in directions:
        expected = [Q(0)]
        for i in range(8):
            for j in range(8):
                name = 'polar_heavy_numerator' if i == j == 0 else 'polar_diagonal_numerator' if i == j \
                    else 'polar_cross_numerator' if i == 0 or j == 0 else 'polar_off_numerator'
                expected = add(expected, scale(p[name], v[i]*v[j]))
        direct, imaginary = literal_polar(v)
        quotient, remainder = divide(direct, d)
        require(remainder == [0], 'normalized literal polar jet is divisible by 1-a')
        require(mul(plus, quotient) == expected, 'full literal Gaussian polar phase identity')
        rows.append({'direction':v,'phase_numerator':list(map(str, expected)),
                     'modulus_unnormalized':list(map(str, direct)),
                     'imaginary_linear':list(map(str, imaginary))})
    require(len(rows) == 64, '64 full polar phase controls')
    return rows


def polar_integral(k, n):
    return [Q(factorial(n)*factorial(k+n-j), factorial(n-j)*factorial(k+n+1))
            for j in range(n+1)]


def regenerate(mu=Q(1)):
    a, plus, minus, b = [0, 1], [1, 1], [1, -1], [1, 0, -1]
    j1, j2, j3 = polar_integral(1, 7), polar_integral(2, 6), polar_integral(3, 5)
    js = add(j1, scale(mul(minus, j2), 8))
    jss = add(j2, scale(mul(minus, j3), 8))
    # All four entries of the normalized polar matrix have denominator2(1+a)^2.
    ph = add(scale(mul(plus, j1), -9), scale(mul(b, power(j1, 2)), 81))
    px = add(scale(mul(b, j2), -9), scale(mul(b, j1, js), 9))
    pd = add(scale(mul(plus, js), -1), scale(mul(a, minus, plus, j2), 8),
             mul(b, power(js, 2)))
    po = add(scale(mul(b, jss), -1), mul(b, power(js, 2)))
    p = formulas()
    o = {}
    for key in ('B_heavy', 'B_cross', 'B_diagonal', 'B_off'):
        poly = p[key]
        o[key] = mul(to_a(poly), power(plus, 15-(len(poly)-1)))
    # Common denominator18(1+a)^7 for the joint matrix.
    joint = {}
    for name, key, polar in (('heavy', 'B_heavy', ph), ('cross', 'B_cross', px),
                            ('diagonal', 'B_diagonal', pd), ('off', 'B_off', po)):
        joint[name] = add(o[key], scale(mul(power(plus, 5), polar), -9*mu))
    denominator = scale(power(plus, 7), 18)
    c = to_a(p['2ell_c'])
    # c_origin=2S/[7(1+a)^6], g=8(1-a)J2.
    slack = add(scale(c, Q(1, 2)), scale(mul(power(plus, 6), minus, j2), -8*mu))
    trans = add(joint['diagonal'], scale(joint['off'], -1))
    collective = add(joint['diagonal'], scale(joint['off'], 6))
    determinant = add(mul(joint['heavy'], collective), scale(power(joint['cross'], 2), -7))
    # Necessary slack/transverse compatibility at maximum admissible weight.
    # W= (1+a)^8 * (g*lambda_origin - c_origin*lambda_polar).
    g = scale(mul(minus, j2), 8)
    polar_trans = add(pd, scale(po, -1))
    origin_trans = add(o['B_diagonal'], scale(o['B_off'], -1))
    W = add(scale(mul(plus, g, origin_trans), Q(1, 18)),
            scale(mul(c, polar_trans), -Q(1, 4)))
    return {'j1': j1, 'j2': j2, 'j3': j3, 'g': g,
            'origin_slack_numerator':scale(c, Q(1,2)),
            'polar_heavy_numerator':ph,'polar_cross_numerator':px,
            'polar_diagonal_numerator':pd,'polar_off_numerator':po,
            'polar_trans_numerator': polar_trans,
            'joint_slack_numerator': slack,
            'matrix_denominator': denominator,
            'joint_transverse_numerator': trans,
            'joint_collective_numerator': collective,
            'joint_determinant_numerator': determinant,
            'compatibility_W_numerator': W, **{'joint_'+k+'_numerator':v for k,v in joint.items()}}


def sharp_controls(p):
    a, plus, d = [0, 1], [1, 1], [1, -1]
    require(Q(1) < MU < Q(2), 'weight interval')
    balanced = value(p['origin_slack_numerator'], CUTOFF)/(value(power(plus,6), CUTOFF)*value(p['g'], CUTOFF))
    require(balanced == MU, 'unique exact slack balance at cutoff')
    r = list(map(Q, ('1/2','71/42','115/42','39/14','11/6','31/42','1/7')))
    require(p['compatibility_W_numerator'] == mul(a,[-5,8],r), 'full dual compatibility factorization')
    require(all(c>0 for c in r), 'positive compatibility residual')
    require(p['polar_trans_numerator'][0]==0 and all(c<0 for c in p['polar_trans_numerator'][1:]), 'polar transverse strictly negative at every positive a')
    cuts = {}
    for name in ('joint_slack_numerator','joint_transverse_numerator'):
        quotient,remainder = divide(p[name],[-CUTOFF,1])
        require(remainder == [0], 'full exact cutoff division')
        cuts[name+'_quotient'] = quotient
    shift=Q(1,10000); den=p['matrix_denominator']
    heavy=add(p['joint_heavy_numerator'],scale(den,-shift))
    collective=add(p['joint_collective_numerator'],scale(den,-shift))
    determinant=add(mul(heavy,collective),scale(power(p['joint_cross_numerator'],2),-7))
    records = {}
    for name,poly in {**cuts,'shifted_heavy':heavy,'shifted_collective_determinant':determinant}.items():
        co=bernstein(poly,CUTOFF,Q(1))
        require(all(c>0 for c in co), 'every Bernstein coefficient positive on sharp cutoff interval')
        records[name]={'degree':len(poly)-1,'power':list(map(str,poly)),
                       'bernstein':list(map(str,co)),'minimum':str(min(co))}
    require(sum(len(r['bernstein']) for r in records.values())==85, '85 Bernstein coefficient coverage')
    require(Q(records['joint_slack_numerator_quotient']['minimum']) > 48, 'slack lower slope at least3/4')
    require(Q(records['joint_transverse_numerator_quotient']['minimum']) > Q(2304,3750), 'transverse lower slope at least1/3750')
    # H<=1 on[0,1]: its cleared excess is a^2(20+64a+90a^2+64a^3+20a^4-a^6).
    h_excess=add(scale(mul(a,power(plus,6)),8),scale(add(power(plus,8),[-1]),-1))
    require(h_excess==mul(power(a,2),[20,64,90,64,20,0,-1]), 'full heavy derivative upper bound identity')
    require(value(p['j1'],Q(1))==Q(1,2) and all(c>0 for c in p['j1']), 'J1 bounded by half on[0,1]')
    require(value(p['joint_transverse_numerator'],CUTOFF)==0 and value(p['joint_slack_numerator'],CUTOFF)==0, 'simultaneous exact cutoff degeneracy')
    return records


def literal_integral(k, n):
    """Expand each affine factor in t before integrating, in variable a."""
    return add(*(scale(mul(power([0, 1], n-j), power([1, -1], j)),
                       Q(comb(n, j), k+j+1)) for j in range(n+1)))


def affine_factor_integral(gammas, k):
    coefficients = [[Q(1)]]
    for gamma in gammas:
        nxt = [[Q(0)] for _ in range(len(coefficients)+1)]
        for j, coeff in enumerate(coefficients):
            nxt[j] = add(nxt[j], mul([0, 1], coeff))
            nxt[j+1] = add(nxt[j+1], scale(mul([1, -1], coeff), gamma))
        coefficients = nxt
    return add(*(scale(coeff, Q(1, k+j+1)) for j, coeff in enumerate(coefficients)))


def integral_checks(p):
    for key, k, n in (('j1', 1, 7), ('j2', 2, 6), ('j3', 3, 5)):
        require(literal_integral(k, n) == p[key], 'complete positive-coefficient integral identity')
    require(affine_factor_integral([1]*7, 1) == p['j1'], 'literal polar heavy derivative')
    small = affine_factor_integral([9]+[1]*6, 1)
    require(add(small, scale(p['j1'], -1)) == p['g'], 'literal seven polar slack derivatives')
    require(affine_factor_integral([1]*6, 2) == p['j2'], 'literal heavy-small mixed derivative')
    require(affine_factor_integral([9]+[1]*5, 2) == add(p['j2'], scale(mul([1,-1], p['j3']), 8)), 'literal distinct-small mixed derivative')
    original = formulas()
    h_numerator, remainder = divide(add(power([1,1],8), [-1]), [0,1])
    require(remainder == [0], 'closed heavy derivative numerator divisibility')
    require(to_a(original['ell_H']) == scale(h_numerator, Q(1,8)), 'complete closed origin heavy derivative')
    require(to_a(original['2ell_c']) == scale([-28,28,56,70,56,28,8,1], Q(4,7)), 'complete closed origin slack derivative')
    return 9


def reject(operation, message):
    try:
        operation()
    except ValueError:
        return message
    raise ValueError('mathematical damage accepted: '+message)


def regenerate_record():
    p = regenerate(MU)
    origin_controls = polarization_checks(formulas())
    polar_controls = polar_checks(p)
    intervals = sharp_controls(p)
    integral_count = integral_checks(p)
    damages = []
    bad = dict(p)
    bad['polar_heavy_numerator'] = add(p['polar_heavy_numerator'],
        scale(mul([1,0,-1], power(p['j1'],2)), -81))
    damages.append(reject(lambda: polar_checks(bad), 'omitted polar modulus rank-one term'))
    bad = dict(p); bad['polar_cross_numerator'] = add(p['polar_cross_numerator'], [0,1])
    damages.append(reject(lambda: polar_checks(bad), 'mixed polar phase coefficient'))
    bad_origin = formulas(); bad_origin['B_cross'] = add(bad_origin['B_cross'], [1])
    damages.append(reject(lambda: polarization_checks(bad_origin), 'mixed origin phase coefficient'))
    damages.append(reject(lambda: sharp_controls(regenerate(Q(1))), 'wrong fixed balancing weight'))
    bad = dict(p); bad['compatibility_W_numerator'] = add(p['compatibility_W_numerator'], [1])
    damages.append(reject(lambda: sharp_controls(bad), 'dual compatibility factor coefficient'))
    bad = dict(p); bad['joint_heavy_numerator'] = scale(p['joint_heavy_numerator'], -1)
    damages.append(reject(lambda: sharp_controls(bad), 'shifted collective block sign'))
    return {'status':'PASS; exact algebra with ordinary written nonlinear proof',
            'fixed_weight':str(MU),'cutoff':str(CUTOFF),
            'polynomials':{k:list(map(str,v)) for k,v in p.items()},
            'whole_interval_bounds':intervals,'bernstein_coefficient_count':85,
            'origin_phase_identity_count':len(origin_controls),
            'origin_phase_identity_digest':digest(origin_controls),
            'polar_phase_identity_count':len(polar_controls),
            'polar_phase_identity_digest':digest(polar_controls),
            'integral_polynomial_identity_count':integral_count,
            'mathematical_damage_rejections':damages,
            'trust_boundary':'Standalone stdlib Fraction polynomial identities and full Bernstein expansions; no grid, solver, floats, external data or imported campaign theorem. Uniform nonlinear neighborhoods, boundary applicability and the fixed-weight dual interpretation are ordinary written mathematics. Independently unreviewed joint certificate.'}
