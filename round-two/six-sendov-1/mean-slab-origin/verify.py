#!/usr/bin/env python3
"""Complete exact checks for origin coercivity on a real mean interval.

CPython3.10+, standard library. Analytic arguments and the inherited radial
theorem remain ordinary proof obligations. --emit writes expected.json;
default invocations only read it. No floating-point proof input.
"""
from fractions import Fraction as F
from hashlib import sha256
from itertools import combinations
from math import comb
from pathlib import Path
from copy import deepcopy
import argparse
import json


def need(ok, message):
    if not ok:
        raise ValueError(message)


# Sparse real polynomials in seven independent u and seven independent v.
NV = 14
ZERO = (0,) * NV


def const(c):
    return {ZERO: F(c)} if c else {}


def var(i):
    x = list(ZERO)
    x[i] = 1
    return {tuple(x): F(1)}


def add(*polys):
    out = {}
    for poly in polys:
        for key, value in poly.items():
            out[key] = out.get(key, F(0)) + value
            if not out[key]:
                del out[key]
    return out


def scale(poly, c):
    return {key: value*c for key, value in poly.items() if value*c}


def mul(p, q):
    out = {}
    for x, cx in p.items():
        for y, cy in q.items():
            key = tuple(a+b for a, b in zip(x, y))
            out[key] = out.get(key, F(0)) + cx*cy
    return {key: value for key, value in out.items() if value}


def power(p, n):
    out = const(1)
    for _ in range(n):
        out = mul(out, p)
    return out


def gadd(x, y):
    return add(x[0], y[0]), add(x[1], y[1])


def gmul(x, y):
    return add(mul(x[0], y[0]), scale(mul(x[1], y[1]), -1)), add(mul(x[0], y[1]), mul(x[1], y[0]))


def elementary(items, degree):
    out = [(const(1), {})] + [({}, {}) for _ in range(degree)]
    for item in items:
        for k in reversed(range(1, degree+1)):
            out[k] = gadd(out[k], gmul(item, out[k-1]))
    return out


def check_poly(lhs, rhs, label):
    need(lhs == rhs, label + ': full sparse coefficient mismatch')


def symbolic_checks():
    u = [var(i) for i in range(7)]
    v = [var(i+7) for i in range(7)]
    u.append(scale(add(*u), -1))
    v.append(scale(add(*v), -1))
    need(not add(*u) and not add(*v), 'complete balance identities')
    U = add(*(power(x, 2) for x in u))
    V = add(*(power(x, 2) for x in v))
    T = add(*(mul(x, y) for x, y in zip(u, v)))
    E = elementary(list(zip(u, v)), 4)
    Eu = elementary([(x, {}) for x in u], 4)
    real2 = scale(add(scale(U, -1), V), F(1, 2))
    imag2 = scale(T, -1)
    real3 = add(Eu[3][0], scale(add(*(mul(x, power(y, 2)) for x, y in zip(u, v))), -1))
    imag3 = add(add(*(mul(power(x, 2), y) for x, y in zip(u, v))), scale(add(*(power(y, 3) for y in v)), F(-1, 3)))
    real4 = add(Eu[4][0], scale(mul(U, V), F(-1, 4)), scale(power(V, 2), F(1, 8)),
                scale(power(T, 2), F(-1, 2)),
                scale(add(*(mul(power(x, 2), power(y, 2)) for x, y in zip(u, v))), F(3, 2)),
                scale(add(*(power(y, 4) for y in v)), F(-1, 4)))
    imag4 = add(scale(mul(add(U, scale(V, -1)), T), F(1, 2)),
                scale(add(*(mul(power(x, 3), y) for x, y in zip(u, v))), -1),
                add(*(mul(x, power(y, 3)) for x, y in zip(u, v))))
    targets = [(2, 0, real2), (2, 1, imag2), (3, 0, real3),
               (3, 1, imag3), (4, 0, real4), (4, 1, imag4)]
    records = []
    for k, component, rhs in targets:
        lhs = E[k][component]
        check_poly(lhs, rhs, 'e'+str(k)+' component'+str(component))
        canonical = json.dumps([[list(key), str(value)] for key, value in sorted(lhs.items())],
                               separators=(',', ':')).encode()
        records.append({'degree': k, 'component': ['real', 'imaginary'][component],
                        'all_monomials': len(lhs), 'sha256': sha256(canonical).hexdigest()})
    # Separate Newton power-sum route, including the balanced e4 denominator.
    P2 = ({}, {})
    P3 = ({}, {})
    P4 = ({}, {})
    for item in zip(u, v):
        square = gmul(item, item)
        P2 = gadd(P2, square)
        P3 = gadd(P3, gmul(square, item))
        P4 = gadd(P4, gmul(square, square))
    for component in range(2):
        check_poly(E[2][component], scale(P2[component], F(-1, 2)), 'Newton e2')
        check_poly(E[3][component], scale(P3[component], F(1, 3)), 'Newton e3')
        check_poly(E[4][component], add(scale(gmul(P2, P2)[component], F(1, 8)),
                                      scale(P4[component], F(-1, 4))), 'Newton e4')
    damaged_terms = [power(var(0), 2), mul(var(0), var(7)),
                     mul(var(0), power(var(7), 2)), mul(power(var(0), 2), var(7))]
    for target, damaged_term in zip(targets[:4], damaged_terms):
        k, component, rhs = target
        damage = add(rhs, damaged_term)
        try:
            check_poly(E[k][component], damage, 'damaged identity')
        except ValueError:
            continue
        raise ValueError('damaged symbolic identity accepted')
    return records


# Univariate rational polynomial engine, distinct from the sparse ring.
def umul(p, q):
    out = [F(0)] * (len(p)+len(q)-1)
    for i, x in enumerate(p):
        for j, y in enumerate(q):
            out[i+j] += x*y
    return out


def upower(p, n):
    out = [F(1)]
    for _ in range(n):
        out = umul(out, p)
    return out


def uevaluate(p, x):
    out = F(0)
    for value in reversed(p):
        out = out*x+value
    return out


def primitive_checks():
    Bs = []
    for k in range(9):
        integrand = [F(0)]*k + [9*(-1)**k*x for x in upower([F(1), F(-1)], 8-k)]
        route1 = [F(0)] + [x/F(i+1) for i, x in enumerate(integrand)]
        route2 = [F(0)]*10
        for j in range(9-k):
            route2[k+j+1] = F(9*(-1)**(k+j)*comb(8-k, j), k+j+1)
        need(route1 == route2, 'all B coefficients: convolution and binomial routes')
        need([i*route1[i] for i in range(1, 10)] == integrand, 'complete B derivative')
        need(uevaluate(route1, 1) == F((-1)**k, comb(8, k)), 'B endpoint')
        Bs.append(route1)
    b0 = [F(0)]*10
    b0[0] = 1
    for i, x in enumerate(upower([F(1), F(-1)], 9)):
        b0[i] -= x
    need(Bs[0] == b0, 'complete B0 identity')
    return Bs


def support_counts():
    records = []
    indices = set(range(8))
    for k in range(2, 9):
        for p in range(k+1):
            count = sum(1 for I in combinations(range(8), p)
                        for _ in combinations(sorted(indices-set(I)), k-p))
            direct = comb(8, p)*comb(8-p, k-p)
            alternate = comb(8, k)*comb(k, p)
            need(count == direct == alternate, 'complete mixed-support census')
            records.append([k, p, count])
    return records


def constants():
    h, nu, gamma, dmax = F(1, 4), F(1, 4000), F(1, 100000), F(1, 200000)
    umax, p, c, M = 8*h*h, (1-h*h)**4, F(27, 56), F(9, 8)
    d = {k: F((-1)**k, comb(8, k))-1 for k in range(2, 9)}
    need(max(abs(x) for x in d.values()) == M, 'all signed endpoint coefficients')
    L = h/3+F(5, 4)*h*h+sum(F(comb(8, k), 8)*h**(k-2) for k in range(5, 9))
    M0, Kh = F(1, 2)+L, (c+M*L)/p
    r2, r4 = {4: F(9, 4)}, {4: F(3, 8)}
    for k in range(5, 9):
        r2[k] = F(7, 12)*comb(6, k-2)*h**(k-4)
        r4[k] = sum(F(comb(8, j)*comb(8-j, k-j), 8)*h**(k-j)*nu**((j-4)//2)
                    for j in range(4, k+1, 2))
    Ap, Bp = sum(r2.values()), sum(r4.values())
    Ad = sum(abs(d[k])*r2[k] for k in r2)
    Bd = sum(abs(d[k])*r4[k] for k in r4)
    Ca = F(1, 2)+3*h+Ap*umax+Bp*nu
    Ai = 1+h+5*h*h+F(3, 2)*nu+sum(F(8, 7)*comb(7, k-1)*h**(k-2) for k in range(5, 9))
    Bi = F(1, 3)+sum(F(comb(8, j)*comb(8-j, k-j), 8)*h**(k-j)*nu**((j-3)//2)
                    for k in range(5, 9) for j in range(3, k+1, 2))
    A = abs(d[3])/p
    B = (c*M0+Ad+Kh*Ca)/p+2*(M+Kh*umax)*Ai*Ai/(p*p)
    C = Bd/p+2*(M+Kh*umax)*Bi*Bi*nu/(p*p)
    s, H = F(1, 128), F(1, 3)
    ell = {2: F(1, 2), 3: H/3, 4: F(5, 4)*H*H}
    ell.update({k: F(comb(8, k), 8)*H**(k-2) for k in range(5, 9)})
    tk = {k: 9*(1+s)**k*s**(9-k)/(9-k) for k in range(2, 9)}
    flat = sum(tk[k]*ell[k] for k in ell)/p
    vcap = 20*gamma/(1-gamma)+64*gamma*gamma/(1-gamma)**2
    lambda_low, young = F(9, 8)*(1-18*gamma), F(3, 125)
    au = F(3, 40)-F(1, 5000)-100*nu-young
    av = lambda_low-F(27, 28)-F(1, 5000)-(F(483, 8)+F(41, 8)**2/(4*young))*nu
    variance_cap = (1+24*gamma+37500*gamma*gamma)/(1-30*gamma)
    e2_lower = 28*(1-3*gamma)**2-16*variance_cap
    spread = F(1, 32)-(F(288, 5)+F(1, 16))*dmax
    radius_gap, phase = F(17, 1024)*spread, F(44112, 595)*dmax
    checks = {
        'A<2': A < 2, 'B<50': B < 50, 'C<30': C < 30,
        'positive_real_denominator': Ca*nu < p,
        'flat<1/10000': flat < F(1, 10000), 'inverse_P0<2': 1/p < 2,
        'radial_reference>3/80': 5*(2-umax/7)/256 > F(3, 80),
        'sqrt_U<3h': umax < (3*h)**2,
        'transverse_cap<nu': vcap < nu,
        'eta_H': h*h+vcap < H*H, 'z_s': 2*gamma < s*s,
        'young_coefficient': F(41, 8)**2/(4*young) == F(210125, 768),
        'young_square': (F(41, 8)/2)**2 == young*F(210125, 768),
        'U_cost>1/40': au > F(1, 40), 'V_cost>1/16': av > F(1, 16),
        'R18>1/2': 1-18*gamma > F(1, 2),
        'a_inverse_square<2': (1-gamma)**(-2) < 2,
        'origin_scalar_margin': 2*gamma**3 < 1,
        'variance_denominator_positive': 1-30*gamma > 0,
        'e2>119/10': e2_lower > F(119, 10),
        'Newton_coefficient': F(119, 10)/14 == F(17, 20),
        'epsilon<3/125': F(512, 5)*dmax < F(3, 125)**2,
        'phase_Hessian_cap': F(6, 5)/(1-2*F(3, 125)) == F(150, 119),
        'phase_coupling': (F(3, 2)+F(1200, 119))*F(32, 5) == F(44112, 595),
        'annulus_gap': radius_gap > phase, 'annulus_inside_slab': dmax <= gamma,
    }
    for name, ok in checks.items():
        need(ok, 'exact comparison '+name)
    values = {name: str(value) for name, value in locals().copy().items()
              if name in ['h', 'nu', 'gamma', 'dmax', 'umax', 'p', 'c', 'M', 'L', 'M0', 'Kh',
                          'Ap', 'Bp', 'Ad', 'Bd', 'Ca', 'Ai', 'Bi', 'A', 'B', 'C', 's', 'H',
                          'flat', 'vcap', 'lambda_low', 'young', 'au', 'av', 'variance_cap',
                          'e2_lower', 'spread', 'radius_gap', 'phase']}
    values['annulus_slack'] = str(radius_gap-phase)
    return {'values': values, 'all_dk': {str(k): str(x) for k, x in d.items()},
            'real_mixed_coefficients': {str(k): [str(r2[k]), str(r4[k])] for k in r2},
            'flatness_coefficients': {str(k): [str(ell[k]), str(tk[k])] for k in ell},
            'comparisons': sorted(checks)}


# Exact Gaussian-rational controls: independent direct-origin integration.
def ga(x, y):
    return x[0]+y[0], x[1]+y[1]


def gs(x, c):
    return x[0]*c, x[1]*c


def gm(x, y):
    return x[0]*y[0]-x[1]*y[1], x[0]*y[1]+x[1]*y[0]


def gn(x):
    return x[0]*x[0]+x[1]*x[1]


def gd(x, y):
    denominator = gn(y)
    need(denominator != 0, 'Gaussian denominator')
    return gs(gm(x, (y[0], -y[1])), 1/denominator)


def geval(p, x):
    out = (F(0), F(0))
    for value in reversed(p):
        out = ga(gm(out, x), (value, F(0)))
    return out


def exact_controls(Bs):
    cases = []
    a = F(99999, 100000)
    for size in [F(0), F(1, 32), F(1, 8), F(1, 4)]:
        for transverse in [F(0), F(1, 10000)]:
            u = [size]*4+[-size]*4
            v = [transverse]*4+[-transverse]*4
            m = (a, F(1, 2000))
            U, V = sum(x*x for x in u), sum(x*x for x in v)
            need(gn(m)*(1+V/12)**2 <= 1, 'control modulus mean upper bound')
            eta = list(zip(u, v))
            q = [gm(m, (1+x, y)) for x, y in eta]
            need(gs(tuple(map(sum, zip(*q))), F(1, 8)) == m, 'control mean')
            factors = [(F(1), F(0))]
            product_norm = F(1)
            for coordinate in q:
                product_norm *= gn(coordinate)
                out = [(F(0), F(0))]*(len(factors)+1)
                for k, value in enumerate(factors):
                    out[k] = ga(out[k], value)
                    out[k+1] = ga(out[k+1], gs(gm(value, coordinate), -a))
                factors = out
            O = (F(0), F(0))
            for k, value in enumerate(factors):
                O = ga(O, gs(value, F(9, k+1)))
            N = gn(O)/product_norm
            need(N >= 1+(1-a)+U/40+V/16, 'control coercivity')
            second_moment = sum(gn(x) for x in q)/8
            if size == F(1, 4) and transverse == 0:
                need(second_moment > 1, 'control outside second-moment premise')
            elementary_eta = [(F(1), F(0))]+[(F(0), F(0))]*8
            P = (F(1), F(0))
            for coordinate in eta:
                P = gm(P, ga((F(1), F(0)), coordinate))
                for k in reversed(range(1, 9)):
                    elementary_eta[k] = ga(elementary_eta[k], gm(coordinate, elementary_eta[k-1]))
            z = gs(m, a)
            numerator = (F(0), F(0))
            for k in range(9):
                numerator = ga(numerator, gm(geval(Bs[k], z), elementary_eta[k]))
            K = gd(numerator, P)
            need(gn(K)/(a*a*gn(m)**9) == N, 'exact full normalization bridge')
            cases.append({'u_size': str(size), 'v_size': str(transverse),
                          'mean_abs_q_squared': str(second_moment),
                          'N_minus_lower_bound': str(N-(1+(1-a)+U/40+V/16))})
    return cases


def generate():
    identities = symbolic_checks()
    Bs = primitive_checks()
    supports = support_counts()
    consts = constants()
    controls = exact_controls(Bs)
    return {'status': 'ordinary author proof: exact finite certificate',
            'symbolic_identities': identities, 'all_B_coefficients': [[str(x) for x in p] for p in Bs],
            'mixed_support_counts': supports, 'constants': consts, 'exact_controls': controls,
            'summary': {'full_symbolic_component_identities': 6, 'Newton_component_identities': 6,
                        'balanced_real_variables': 14, 'primitive_polynomials': 9,
                        'primitive_coefficients': 90, 'complete_support_counts': len(supports),
                        'rational_comparisons': len(consts['comparisons']),
                        'exact_control_profiles': len(controls), 'damaged_symbolic_identities_rejected': 4}}


def check_fixture(actual, fixture):
    need(actual == fixture, 'complete rational fixture mismatch')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--emit', action='store_true')
    args = parser.parse_args()
    path = Path(__file__).with_name('expected.json')
    actual = generate()
    if args.emit:
        path.write_text(json.dumps(actual, indent=2)+'\n')
    check_fixture(actual, json.loads(path.read_text()))
    damages = []
    for key in ['A', 'B', 'flat', 'av', 'annulus_slack']:
        damage = deepcopy(actual)
        damage['constants']['values'][key] = '999'
        damages.append(damage)
    damage = deepcopy(actual)
    damage['all_B_coefficients'][2][3] = '0'
    damages.append(damage)
    for damage in damages:
        try:
            check_fixture(actual, damage)
        except ValueError:
            continue
        raise ValueError('damaged fixture accepted')
    canonical = json.dumps(actual, sort_keys=True, separators=(',', ':')).encode()
    print(json.dumps({'status': 'PASS: mean interval finite checks',
                      **actual['summary'], 'damaged_fixtures_rejected': len(damages),
                      'canonical_sha256': sha256(canonical).hexdigest(),
                      'annulus_slack': actual['constants']['values']['annulus_slack']}, sort_keys=True))


if __name__ == '__main__':
    main()
