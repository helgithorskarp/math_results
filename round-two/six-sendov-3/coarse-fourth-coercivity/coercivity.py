"""Exact corroboration of the moving-jet absorption proof.

Same-author arithmetic reuse; not independent review or analytic formalization.
All comparisons use whole sparse rational/ninth-field coefficient maps.
"""
from math import comb
from arithmetic import (F, N0, N1, NW, ZERO, need, canonical, sha256,
                        constant, variable, add, scale, multiply, power,
                        encoded, na, ns, nm, np, ni, nc, pc, pv, pa, ps,
                        pm, pconj)


def radd(*items):
    out = {}
    for p in items:
        for key, value in p.items():
            out[key] = add(out.get(key, {}), value)
    return {key: value for key, value in out.items() if value}


def rscale(p, scalar):
    return {key: scale(value, scalar) for key, value in p.items()
            if scale(value, scalar)}


def rtimes(p, q):
    out = {}
    for (r, j), a in p.items():
        for (s, k), b in q.items():
            if r+s <= 3:
                out[r+s, j+k] = add(out.get((r+s, j+k), {}), multiply(a, b))
    return {key: value for key, value in out.items() if value}


def moving_primitive(damage=None):
    # U0,H,W,D,J21,J4,U3,J22,J41,J6: ten independent formal moments.
    U, H, W, D, J21, J4, U3, J22, J41, J6 = [variable(i) for i in range(10)]
    powers = [{}, {(1, 0): U, (2, 0): W},
              {(1, 0): scale(H, -1), (2, 0): D},
              {(2, 0): scale(J21, -3), (3, 0): U3},
              {(2, 0): J4, (3, 0): scale(J22, -6)},
              {(3, 0): scale(J41, 5)},
              {(3, 0): scale(J6, 1 if damage == 'sixth_sign' else -1)}, {}, {}]
    elementary = [{(0, 0): constant(1)}]
    for m in range(1, 9):
        elementary.append(rscale(radd(*(
            rscale(rtimes(elementary[m-i], powers[i]), (-1)**(i-1))
            for i in range(1, m+1))), F(1, m)))
    derivative = radd(*({(r, 8-m): scale(p, 9*(-1)**m)
                         for (r, _), p in e.items()}
                        for m, e in enumerate(elementary)))
    primitive = {(r, j+1): scale(p, F(1, j+1))
                 for (r, j), p in derivative.items()}
    anchored = dict(primitive)
    for (r, j), p in primitive.items():
        for s in range(min(3-r, j)+1):
            anchored = radd(anchored, {(r+s, 0): scale(p, -comb(j, s)*(-1)**s)})
    return anchored


def field_normal(c, a, b=0, d=0):
    return na(ns(N1, F(a)), ns(c, F(b)), ns(np(c, 2), F(d)))


def serial(p):
    return [encoded(a) for a in p]


def evaluate(p, values):
    out = N0
    for j, a in enumerate(p):
        for exponents, coefficient in a.items():
            item = ns(np(NW, j), coefficient)
            for k, degree in enumerate(exponents):
                if degree:
                    need(k in values, 'every formal evaluation variable defined')
                    item = nm(item, np(values[k], degree))
            out = na(out, item)
    return out


def specialize(p, U, H):
    out = pc(N0)
    for exponents, coefficient in p.items():
        value = ns(nm(np(U, exponents[0]), np(H, exponents[1])), coefficient)
        residual = list(exponents)
        residual[0] = residual[1] = 0
        out = pa(out, tuple({tuple(residual): a} if a else {} for a in value))
    return out


def times_series(a, b, n):
    out = [pc(N0) for _ in range(n+1)]
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            if i+j <= n:
                out[i+j] = pa(out[i+j], pm(x, y))
    return out


def root_equation(blocks, root, n):
    powers = [[pc(N1)]+[pc(N0) for _ in range(n)]]
    for _ in range(9):
        powers.append(times_series(powers[-1], root, n))
    out = [pc(N0) for _ in range(n+1)]
    for r, block in enumerate(blocks):
        for j, value in enumerate(block):
            for s in range(n-r+1):
                out[r+s] = pa(out[r+s], pm(value, powers[j][s]))
    return out


def interval(poly, lo, hi):
    low = high = F(0)
    for coefficient in reversed(poly):
        values = (low*lo, low*hi, high*lo, high*hi)
        low, high = min(values)+coefficient, max(values)+coefficient
    return low, high


def build(baseline, damage=None):
    checks = []

    def equality(name, lhs, rhs):
        need(lhs == rhs, 'whole identity: '+name)
        checks.append({'name': name, 'whole_maps_compared': True})

    c = ns(na(np(NW, 4), np(NW, 5)), F(-1, 2))
    equality('physical cubic', na(ns(np(c, 3), 8), ns(c, -6), ns(N1, -1)), N0)
    y = ns(ni(na(N1, c)), F(1, 3))
    x = na(ns(N1, F(2, 3)), ns(y, -1))
    H, U = ns(y, 14), ns(x, -8)
    rho = ns(na(c, ns(N1, -5)), F(1, 3))
    k = ns(na(N1, ns(c, 2)), F(-7, 18))
    alpha = field_normal(c, F(-527, 360), F(41, 90), F(13, 90))
    tau = ns(np(na(k, rho), 2), F(1, 2))
    kappa = na(tau, ns(alpha, F(10, 27)))
    sigma = na(alpha, ns(np(rho, 2), F(1, 2)))
    uz = ns(na(U, nm(rho, H)), F(1, 8))
    up = na(uz, ns(nm(rho, H), F(-1, 2)))
    W = field_normal(c, F(2512, 27), F(5840, 9), F(-21392, 27))
    D = field_normal(c, F(-4270, 27), F(-29492, 27), F(4012, 3))
    Bstar = field_normal(c, F(2311, 108), F(4934, 27), F(-1976, 9))
    Tstar = field_normal(c, F(-60800959, 17496), F(-307083769, 17496), F(10980067, 486))
    K0 = na(Bstar, ns(np(uz, 2), -4), ns(nm(alpha, np(H, 2)), F(-1, 2)))
    U2 = na(ns(np(uz, 2), 6), ns(np(up, 2), 2))
    U3 = na(ns(np(uz, 3), 6), ns(np(up, 3), 2))
    target = {2: W, 3: D, 4: nm(H, up), 5: ns(np(H, 2), F(1, 2)),
              6: U3, 7: nm(H, np(up, 2)),
              8: ns(nm(np(H, 2), up), F(1, 2)), 9: ns(np(H, 3), F(1, 4)),
              16: U2, 17: U, 18: H}
    generic = moving_primitive(damage)
    generic_record = [[list(key), encoded(value)] for key, value in sorted(generic.items())]
    equality('ENTIRE credited10152 ten-moment primitive', generic_record,
             baseline['generic_real_primitive_through_eta3'])
    blocks = [[specialize(generic.get((r, j), {}), U, H)
               for j in range(10)] for r in range(4)]
    w4 = ni(na(c, ns(np(c, 2), 2), ns(N1, -1)))
    w3 = ns(na(ns(N1, 7), ns(nm(na(ns(N1, 2), ns(np(c, 2), -2)), w4), -1)), F(2, 3))
    A3, A4 = ns(N1, F(3, 2)), na(N1, c)
    B3, B4 = A3, na(ns(N1, 2), ns(np(c, 2), -2))
    equality('first positive dual row', na(nm(w3, A3), nm(w4, A4)), ns(N1, 8))
    equality('second positive dual row', na(nm(w3, B3), nm(w4, B4)), ns(N1, 7))
    moving_normals = {}
    for j in (3, 4, 5, 6):
        omega = np(NW, j)
        root = [pc(omega)]+[pc(N0) for _ in range(3)]
        for order in range(1, 4):
            root[order] = ps(pm(root_equation(blocks, root, order)[order], pc(omega)), F(-1, 9))
            equality('complete active root equation '+str(j)+'/'+str(order),
                     root_equation(blocks, root, order), [pc(N0) for _ in range(order+1)])
        normal = [ps(p, F(1, 2)) for p in
                  times_series(root, [pconj(t) for t in root], 3)]
        normal[0] = pa(normal[0], pc(ns(N1, F(-1, 2))))
        equality('whole active first normal '+str(j), normal[1], pc(N0))
        moving_normals[j] = normal
    radial_T = {}
    for j in (3, 4):
        equality('whole reflected active normal '+str(j), moving_normals[j], moving_normals[9-j])
        omega = np(NW, j)
        cosine = lambda m: ns(na(np(omega, m), nc(np(omega, m))), F(1, 2))
        a, b2 = na(N1, ns(cosine(1), -1)), na(N1, ns(cosine(2), -1))
        sixth, fifth = na(N1, ns(cosine(6), -1)), na(N1, ns(cosine(5), -1))
        q, s2 = (ns(N1, -1), ns(N1, F(3, 4))) if j == 3 else (ns(c, -2), na(N1, ns(np(c, 2), -1)))
        curvature = nm(ns(na(ns(np(x, 2), F(7, 2)), ns(nm(nm(x, y), q), 6),
                           ns(nm(np(y, 2), np(q, 2)), F(5, 2))), -1), s2)
        fixed = na(ns(N1, 4), U, ns(H, F(-1, 2)), ns(nm(b2, np(U, 2)), F(1, 14)),
                   ns(nm(sixth, nm(U, H)), F(-1, 12)), ns(nm(fifth, np(H, 2)), F(1, 40)), curvature)
        direct = pa(pc(fixed), pm(pc(ns(sixth, F(1, 6))), pv(variable(4))),
                    pm(pc(ns(fifth, F(-1, 20))), pv(variable(5))),
                    pm(pc(ns(a, F(-1, 8))), pv(variable(2))),
                    pm(pc(ns(b2, F(-1, 14))), pv(variable(3))))
        equality('ENTIRE moving second radial row '+str(j), moving_normals[j][2], direct)
        radial_T[j] = pa(direct, pm(pc(ns(a, F(1, 8))), pv(variable(2))),
                         pm(pc(ns(b2, F(1, 14))), pv(variable(3))))
    eliminated_second_cost = pa(pm(pc(w3), radial_T[3]), pm(pc(w4), radial_T[4]),
                                pv(scale(variable(16), F(1, 2))),
                                pc(na(ns(N1, 8), ns(U, 2), ns(H, F(-3, 2)))),
                                pv(add(scale(variable(4), F(-3, 2)),
                                       scale(variable(5), F(3, 8)))))
    stated_second_cost = pa(pc(K0), pv(scale(variable(16), F(1, 2))),
                            pm(pc(rho), pv(variable(4))), pm(pc(sigma), pv(variable(5))))
    equality('ENTIRE scalar plus positive-dual second cost', eliminated_second_cost, stated_second_cost)
    scalar = pv(add(constant(8), scale(variable(17), 3), scale(variable(16), F(3, 2)),
                    variable(6), scale(variable(18), -3), scale(variable(4), -6),
                    scale(variable(7), -3), scale(variable(5), F(15, 8)),
                    scale(variable(8), F(15, 8)), scale(variable(9), F(-5, 16)),
                    scale(variable(2), 2), scale(variable(3), F(3, 2))))
    phi = pa(scalar, pm(pc(w3), moving_normals[3][3]), pm(pc(w4), moving_normals[4][3]))
    if damage == 'frozen_moving_phi':
        phi = pc(evaluate(phi, target))
    normalization = na(nm(uz, W), nm(na(nm(rho, up), nm(sigma, H)), na(U2, ns(D, -1))))
    if damage == 'missing_norm_payment':
        normalization = nm(uz, W)
    equality('both normalization payments and complete stationary Tstar',
             na(evaluate(phi, target), normalization), Tstar)
    equality('stationary real gradient pair', na(up, ns(nm(rho, H), F(1, 2))), uz)
    equality('stationary real mean', na(ns(uz, 6), ns(up, 2)), U)
    # Whole invariant signed projection, BEFORE balance/norm/mean constraints.
    V1, V2, V3, V4, US, U2v, HU, H2U = [pv(variable(j)) for j in range(8)]
    a = pm(pc(nm(na(k, rho), ni(H))), V3)
    minimum_norm = pa(pc(ns(np(uz, 2), 8)), pm(pc(np(rho, 2)), V4), pm(pm(a, a), V2),
                      pm(pc(ns(nm(uz, rho), -2)), V2), pm(pc(ns(uz, 2)), pm(a, V1)),
                      pm(pc(ns(rho, -2)), pm(a, V3)))
    dot_minimum = pa(pm(pc(uz), US), pm(pc(ns(rho, -1)), H2U), pm(a, HU))
    residual = pa(U2v, ps(dot_minimum, -2), minimum_norm)
    original = pa(pc(K0), ps(U2v, F(1, 2)), pm(pc(rho), H2U), pm(pc(sigma), V4))
    constrained_K = pa(pc(na(Bstar, ns(nm(alpha, np(H, 2)), F(-1, 2)))),
                       pm(pc(alpha), V4), pm(pc(nm(tau, ni(H))), pm(V3, V3)))
    projected = pa(constrained_K, ps(residual, F(1, 2)), pm(a, pa(HU, pm(pc(ns(k, -1)), V3))))
    defect = pa(pm(pc(uz), pa(US, pc(ns(U, -1)), pm(pc(rho), pa(V2, pc(ns(H, -1)))))),
                ps(pm(pc(uz), pm(a, V1)), -1), ps(pm(pm(a, a), pa(V2, pc(ns(H, -1)))), F(-1, 2)))
    equality('ENTIRE unconstrained invariant projection defect', pa(original, ps(projected, -1)), defect)
    # Exact balanced chart: formal r,R2,R3,R4, weights 1,2,3,4.
    r, R2, R3, R4 = [pv(variable(j)) for j in range(10, 14)]
    q2 = pa(pc(ns(H, F(1, 2))), ps(R2, F(-1, 2)), ps(pm(r, r), -1))
    pair3 = pa(ps(pm(pm(r, r), r), 2), ps(pm(r, q2), 6), R3)
    pair4 = pa(ps(pm(pm(r, r), pm(r, r)), 2), ps(pm(pm(r, r), q2), 12), ps(pm(q2, q2), 2), R4)
    cubic = pa(pm(pc(ns(H, 3)), r), ps(pm(r, R2), -3), ps(pm(pm(r, r), r), -4), R3)
    quartic_deviation = pa(pm(pc(ns(H, -1)), R2), pm(pc(ns(H, 4)), pm(r, r)), R4,
                            ps(pm(R2, R2), F(1, 2)), ps(pm(pm(r, r), R2), -4),
                            ps(pm(pm(r, r), pm(r, r)), -8))
    equality('ENTIRE balanced cubic chart', pair3, cubic)
    equality('ENTIRE balanced quartic chart', pa(pair4, pc(ns(np(H, 2), F(-1, 2)))), quartic_deviation)
    local_K = pa(pm(pc(alpha), quartic_deviation), pm(pc(nm(tau, ni(H))), pm(cubic, cubic)))
    weights = {10: 1, 11: 2, 12: 3, 13: 4}
    homogeneous2 = tuple({m: a for m, a in p.items() if sum(weights.get(j, 0)*n for j, n in enumerate(m)) == 2}
                         for p in local_K)
    paid2 = pa(pm(pc(ns(nm(alpha, H), -1)), R2),
               pm(pc(nm(H, na(ns(alpha, 4), ns(tau, 9)))), pm(r, r)))
    if damage == 'quadratic_skew_sign':
        paid2 = pa(pm(pc(ns(nm(alpha, H), -1)), R2),
                   pm(pc(nm(H, na(ns(alpha, 4), ns(tau, -9)))), pm(r, r)))
    equality('ENTIRE weighted homogeneous quadratic part', homogeneous2, paid2)
    square_form = pa(pm(pc(ns(nm(H, kappa), 9)), pm(r, r)),
                     pm(pc(ns(nm(alpha, H), -1)), pa(R2, ps(pm(r, r), F(-2, 3)))))
    equality('ENTIRE positive quadratic decomposition', homogeneous2, square_form)
    remainder = pa(local_K, ps(homogeneous2, -1))
    need(all(sum(weights.get(j, 0)*n for j, n in enumerate(m)) >= 4
             for p in remainder for m in p), 'every omitted chart degree at least four')
    checks.append({'name': 'entire chart remainder has weighted degrees four and six', 'whole_maps_compared': True})
    lo, hi = F(15, 16), F(47, 50)
    f = lambda t: 8*t**3-6*t-1
    need(f(lo) < 0 < f(hi) and 24*lo*lo-6 > 0, 'unique physical cosine bracket')
    for _ in range(48):
        mid = (lo+hi)/2
        if f(mid) < 0:
            lo = mid
        else:
            hi = mid
    signs = []
    for name, value in [('H', H), ('minus_alpha', ns(alpha, -1)), ('kappa', kappa),
                        ('w3', w3), ('w4', w4), ('minus_radial_determinant', ns(nm(na(c, ns(np(c, 2), 2), ns(N1, -1)), N1), F(3, 224)))]:
        cc = (value[0]-2*value[1], -2*value[4], 4*value[1])
        equality('whole cubic sign coordinates '+name, value, field_normal(c, *cc))
        lower, upper = interval(cc, lo, hi)
        need(lower > 0, 'physical positive sign: '+name)
        signs.append({'name': name, 'cubic_coordinates': [str(t) for t in cc],
                      'lower': str(lower), 'upper': str(upper)})
    return {'agent': 'six-sendov-3', 'role': 'researcher', 'schema': 'coarse-fourth-v1',
            'analytic_bridges_unformalized': True, 'independent_review': False,
            'generic_ten_moment_primitive': generic_record,
            'moving_second_normals': {str(j): serial(moving_normals[j][2]) for j in (3, 4)},
            'moving_third_normals': {str(j): serial(moving_normals[j][3]) for j in (3, 4)},
            'moving_phi_exact_sum_mean_norm': serial(phi),
            'complete_unconstrained_projection_defect': serial(defect),
            'balanced_cubic': serial(cubic), 'balanced_quartic_deviation': serial(quartic_deviation),
            'balanced_cost': serial(local_K), 'positive_quadratic_part': serial(homogeneous2),
            'chart_remainder': serial(remainder),
            'stationary_normalization': [str(t) for t in normalization],
            'stationary_Tstar': [str(t) for t in Tstar],
            'whole_identities': checks, 'rational_positive_signs': signs,
            'physical_cosine_interval': [str(lo), str(hi)]}
