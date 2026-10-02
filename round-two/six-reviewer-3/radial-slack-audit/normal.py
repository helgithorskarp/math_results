"""Actual anchored heavy-factor derivatives and four original-root normals."""
from prior import F, I, K, need, real, embedding, enclose, cx, convolution, power, derivative


def determinant2(a):
    return a[0][0] * a[1][1] - a[0][1] * a[1][0]


def square(x):
    return x.square() if isinstance(x, I) else x * x


def partials(eta, v):
    x, y, opening, _, _, _ = v
    a, r, s = 1 - eta, eta * x, eta * y
    small = power([-r, 1], 6)
    # Differentiate the actual two critical factors before integration.
    qy = cx.primitive(cx.scale(convolution(small, [-s, 1]), -18), a)
    qt = cx.primitive(cx.scale(small, 9), a)
    qv = cx.primitive(cx.scale(convolution(small, [-2 * s, 1]), -9), a)
    qm = cx.primitive(cx.scale(small, -9), a)
    p = cx.primitive(cx.scale(convolution(small, [s * s + eta * opening, -2 * s, 1]), 9), a)
    return p, [qy, qt, qv, qm]


def normal(eta, v, c):
    p, polys = partials(eta, v)
    phases = [-F(1, 2) + eta * v[3], -c + eta * v[4]]
    J, O, squared_sines, denominators, quotients = [], [], [], [], []
    zp = [0] + derivative(p)
    for tau in phases:
        sine2 = 1 - square(tau)
        if isinstance(sine2, I):
            need(sine2.lo > 0, 'positive original-root sine domain')
        den = cx.circle(zp, tau)
        row = [cx.ratio(cx.circle(q, tau), den, sine2) for q in polys]
        J.append([-q[0][0] for q in row[:2]])
        O.append([q[0][1] for q in row[2:]])
        squared_sines.append(sine2)
        denominators.append(row[0][1])
        quotients.append([q[0] for q in row])
    detJ, detO = determinant2(J), determinant2(O)
    if isinstance(detJ, I):
        need(detJ.lo > 0 and detO.hi < 0, 'oppositely signed normal blocks')
    else:
        need(detJ != 0 and detO != 0, 'regular exact initial normal blocks')
    D, W = 1 - eta * (1 + v[1]), 1 + eta * v[5]
    rhs = [-D / (W**3), 1 / (2 * W**3)]
    # Solve the TRANSPOSE: there are two individually counted roots per pair.
    mu = [(rhs[0] * J[1][1] - J[1][0] * rhs[1]) / detJ,
          (J[0][0] * rhs[1] - rhs[0] * J[0][1]) / detJ]
    naive_mu = mu
    # q_y/2 + D*q_T = integral 9*(z-r)^6*(a-z), eliminating s exactly.
    combo = cx.primitive(cx.scale(convolution(power([-eta * v[0], 1], 6), [1 - eta, -1]), 9), 1 - eta)
    combo_real = [cx.ratio(cx.circle(combo, tau), cx.circle(zp, tau), sine2)[0][0]
                  for tau, sine2 in zip(phases, squared_sines)]
    mu = [combo_real[1] / (W**3 * detJ), -combo_real[0] / (W**3 * detJ)]
    if not isinstance(detJ, I):
        need(mu == naive_mu, 'full exact cancellation equals individual transpose solve')
    return {'p': p, 'partials': polys, 'J': J, 'O': O, 'detJ': detJ,
            'detO': detO, 'mu': mu, 'rhs': rhs, 'sine2': squared_sines,
            'denominators': denominators, 'quotients': quotients, 'D': D, 'W': W,
            'naive_mu': naive_mu, 'cancelled_combo': combo, 'combo_real': combo_real}


def initial():
    values, _, _, _, _ = real.initial()
    c, _ = real.constants()
    n = normal(K(0), values, c)
    expectedJ = [[K(-F(3, 8)), K(F(3, 14))], [-(1 + c) / 4, (2 - 2 * c**2) / 7]]
    need(n['J'] == expectedJ, 'entire independently reconstructed initial even block')
    need(n['detJ'] == 3 * (c + 2 * c**2 - 1) / 56, 'initial even determinant')
    need(n['O'] == [[K(F(1, 8)), K(-F(1, 7))], [K(F(1, 8)), -2 * c / 7]], 'entire initial odd block')
    need(n['mu'] == [K((F(26, 9), -F(2, 9), -F(4, 9))), (2 * c - 1) / 3], 'credited individually normalized initial multipliers')
    return values, {key: [[x.record() for x in row] for row in n[key]] for key in ['J', 'O']} | {
        'even_determinant': n['detJ'].record(), 'odd_determinant': n['detO'].record(),
        'individual_root_multipliers': [x.record() for x in n['mu']],
        'individual_root_dual_rhs': [x.record() for x in n['rhs']]}


def certify(values, radius):
    c = embedding()
    box = [enclose(x, c) + I(-radius, radius) for x in values]
    eta = I(0, F(1, 65536))
    n = normal(eta, box, c)
    need(n['D'].lo > 0 and n['W'].lo > 0 and box[2].lo > 0, 'physical distance and heavy-opening domains')
    need(n['detJ'].lo > F(1, 16) and n['detO'].hi < -F(1, 100), 'original determinant margins')
    need(all(x.lo > F(1, 4) and x.hi < 3 for x in n['mu']), 'all individually normalized multiplier signs')
    sine_product = (n['sine2'][0] * n['sine2'][1]).sqrt()
    raw_determinant = 4 * sine_product * n['detJ'] * n['detO']
    need(raw_determinant.hi < -F(1, 6400), 'complete physical four-normal determinant')
    need(F(9, 100) < n['detJ'].lo <= n['detJ'].hi < F(3, 32), 'sharper even determinant interval')
    need(-F(1, 560) < raw_determinant.lo <= raw_determinant.hi < -F(1, 600), 'sharper full four-normal determinant interval')
    return {'parameter_radius': str(radius), 'eta_domain': ['0', '1/65536'],
        'parameter_box': [x.record() for x in box],
        'even_matrix': [[x.record() for x in row] for row in n['J']],
        'odd_matrix': [[x.record() for x in row] for row in n['O']],
        'even_determinant': n['detJ'].record(), 'odd_determinant': n['detO'].record(),
        'original_root_sine_squared': [x.record() for x in n['sine2']],
        'sine_product': sine_product.record(),
        'complete_normal_determinant_over_eta5': raw_determinant.record(),
        'physical_circle_denominators': [x.record() for x in n['denominators']],
        'all_four_complex_partial_quotients': [[[x.record() for x in q] for q in row] for row in n['quotients']],
        'individual_root_dual_rhs': [x.record() for x in n['rhs']],
        'individual_root_multipliers': [x.record() for x in n['mu']],
        'uncancelled_transpose_multiplier_enclosures': [x.record() for x in n['naive_mu']],
        'cancelled_root_integral_real_quotients': [x.record() for x in n['combo_real']],
        'positive_D_W': [n['D'].record(), n['W'].record()]}
