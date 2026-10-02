"""Independent original polynomial/phase calculations with Fraction endpoints."""
from parents import real, F, I, K, need, convolution, power, evaluate, derivative, chebyshev, embedding, enclose, up


def square(x):
    return x.square() if isinstance(x, I) else x * x


def primitive(raw, anchor):
    out = [raw[0] * 0] + [x / F(j + 1) for j, x in enumerate(raw)]
    out[0] -= evaluate(out, anchor)
    return out


def add_polys(*parts):
    out = [0] * max(map(len, parts))
    for p in parts:
        for j, x in enumerate(p):
            out[j] += x
    return out


def scale(poly, scalar):
    return [scalar * x for x in poly]


def circle(poly, tau):
    ts, us = chebyshev([0, 1]), chebyshev([0, 2])
    return (sum((x * evaluate(ts[j], tau) for j, x in enumerate(poly)), tau * 0),
            sum((x * evaluate(us[j - 1], tau) for j, x in enumerate(poly) if j), tau * 0))


def multiply(a, b, sine2):
    return (a[0] * b[0] - sine2 * a[1] * b[1], a[0] * b[1] + a[1] * b[0])


def ratio(a, b, sine2):
    den = square(b[0]) + sine2 * square(b[1])
    if isinstance(den, I):
        need(den.lo > 0, 'actual circle divisor has positive squared norm')
    else:
        need(den != 0, 'nonzero exact circle divisor')
    return ((a[0] * b[0] + sine2 * a[1] * b[1]) / den,
            (a[1] * b[0] - a[0] * b[1]) / den), den


def polynomials(eta, v):
    x, y, opening, _, _, _ = v
    r, s, a = eta * x, eta * y, 1 - eta
    small = power([-r, 1], 6)
    heavy = [s * s + eta * opening, -2 * s, 1]
    p = primitive(scale(convolution(small, heavy), 9), a)
    split = primitive(scale(convolution(power([-r, 1], 4), heavy), -9), a)
    qv = primitive(scale(convolution(small, [-2 * s, 1]), -9), a)
    qm = primitive(scale(small, -9), a)
    qd = primitive(scale(power([-r, 1], 5), -54 * (opening + eta * square(x - y))), a)
    return p, split, qv, qm, qd


def odd_response(eta, v, c):
    p, split, qv, qm, qd = polynomials(eta, v)
    phases = [-F(1, 2) + eta * v[3], -c + eta * v[4]]
    O, force, physical_denominators = [], [], []
    zp = [0] + derivative(p)
    for tau in phases:
        sine2 = 1 - square(tau)
        if isinstance(sine2, I):
            need(sine2.lo > 0, 'positive active sine domain')
        denominator = circle(zp, tau)
        quotients = [ratio(circle(q, tau), denominator, sine2) for q in [qv, qm, qd]]
        O.append([q[0][1] for q in quotients[:2]])
        force.append(quotients[2][0][1])
        physical_denominators.append(quotients[0][1])
    det = O[0][0] * O[1][1] - O[0][1] * O[1][0]
    if isinstance(det, I):
        need(det.hi < 0, 'negative odd radial determinant')
    else:
        need(det != 0, 'nonzero exact odd determinant')
    V = (-force[0] * O[1][1] + O[0][1] * force[1]) / det
    M = (-O[0][0] * force[1] + force[0] * O[1][0]) / det
    return {'O': O, 'force': force, 'det': det, 'V': V, 'M': M, 'p': p,
            'split': split, 'qv': qv, 'qm': qm, 'qd': qd, 'phases': phases,
            'physical_denominators': physical_denominators}


def common_second(eta, v, c, odd):
    x, y, opening, _, _, _ = v
    V, M = odd['V'], odd['M']
    r, s, a = eta * x, eta * y, 1 - eta
    n = (M - eta * V * y + 6 * (y - x)) / 2
    mean = eta * V / 2 - 3
    # Derive the reduced R as an anchored primitive of three coefficients
    # in X=z-r, rather than reading a producer polynomial or fixture.
    R = primitive(add_polys(scale(power([-r, 1], 6), -9 * (eta * square(V) / 2 + square(n) / opening)),
                           scale(power([-r, 1], 5), 6 * (54 * (x - y) - 9 * (V * (r - 2 * s) + M))),
                           scale(power([-r, 1], 4), -162 * (opening + eta * square(x - y)))), a)
    q = add_polys(odd['qd'], scale(odd['qv'], V), scale(odd['qm'], M))
    zp = [0] + derivative(odd['p'])
    z2pp = [0, 0] + derivative(derivative(odd['p']))
    zqp = [0] + derivative(q)
    reduced, phases_b, roots = [], [], []
    for tau in odd['phases']:
        sine2 = 1 - square(tau)
        den = circle(zp, tau)
        b = ratio(circle(q, tau), den, sine2)[0][0]
        term = circle(zqp, tau)
        acceleration = circle(add_polys(zp, z2pp), tau)
        Croot = tuple(b * term[j] - square(b) * acceleration[j] / 2 for j in range(2))
        raw = circle(R, tau)
        reduced.append(tuple(raw[j] + eta * Croot[j] for j in range(2)))
        phases_b.append(b)
        roots.append(Croot)
    forcing = [reduced[0][1], reduced[1][1], reduced[0][0], reduced[1][0], eta * 0]
    return {'R': R, 'q': q, 'm1': mean, 'n1': n, 'phase_b': phases_b,
            'moving_root_correction': roots, 'forcing': forcing}


def initial():
    values, Y, w0, w1, parent_record = real.initial()
    c, _ = real.constants()
    odd = odd_response(K(0), values, c)
    expected_O = [[K(F(1, 8)), K(-F(1, 7))], [K(F(1, 8)), -2 * c / 7]]
    need(odd['O'] == expected_O, 'all four initial odd physical rows')
    need(odd['det'] == (1 - 2 * c) / 56, 'initial odd determinant')
    need(odd['V'] == 8 * (2 * c + 1) * values[2] and odd['M'] == 7 * (2 * c + 1) * values[2], 'both initial common odd responses')
    second = common_second(K(0), values, c, odd)
    tstar = [-3 * w1[j] - sum((Y[j][i] * second['forcing'][i] for i in range(5)), K(0)) for j in range(5)]
    alpha, omega = 1 + values[0], values[5]
    centered = -3 * alpha - 2 * omega + 2 * w1[-1]
    Hodd = -second['n1']**2 / values[2] + 3 * (second['m1'] * values[2] - second['n1'])**2 / values[2]
    common = -9 * alpha - 6 * omega - 2 * tstar[-1] + Hodd
    need(centered == K((F(1099, 135), -F(6146, 135), F(1988, 45))), 'credited finite centered imaginary coefficient')
    need(common == K((F(9233, 18), -588, F(5810, 9))), 'credited finite common imaginary coefficient')
    return values, Y, w0, w1, tstar, {'parent_initial': parent_record,
        'odd_matrix': [[x.record() for x in row] for row in odd['O']],
        'odd_determinant': odd['det'].record(), 'odd_first_response': [odd['V'].record(), odd['M'].record()],
        'common_reduced_forcing': [x.record() for x in second['forcing']],
        'common_next_response': [x.record() for x in tstar],
        'centered_imaginary_coefficient': centered.record(), 'common_imaginary_coefficient': common.record()}


def certify(values, Yfield, w0field, w1field, tstarfield, radius):
    # The earlier own full seven-axis third tensor bounds exactly the same
    # necessary even five-block and removable difference quotients.
    parent = real.certify(values, Yfield, w0field, w1field, radius)
    unpack = lambda row: I(F(row[0]), F(row[1]))
    c = embedding()
    box = [enclose(x, c) + I(-radius, radius) for x in values]
    eta = I(0, F(1, 65536))
    odd = odd_response(eta, box, c)
    need(odd['det'].hi < -F(1, 100), 'whole-box odd determinant margin')
    second = common_second(eta, box, c, odd)
    B = [[unpack(x) for x in row] for row in parent['five_block_enclosure']]
    B1 = [[unpack(x) for x in row] for row in parent['five_block_eta_difference_quotient_enclosure']]
    U1 = [unpack(x) for x in parent['forcing_eta_difference_quotient_enclosure']]
    Y = [[enclose(x, c) for x in row] for row in Yfield]
    w0 = [enclose(x, c) for x in w0field]
    star = [enclose(x, c) for x in tstarfield]
    rhs = [3 * U1[j] + 3 * real.matvec(B1, w0)[j] - second['forcing'][j] for j in range(5)]
    residual = [rhs[j] - real.matvec(B, star)[j] for j in range(5)]
    pre = real.matvec(Y, residual)
    rabs = [up(x.absmax()) for x in pre]
    beta = F(parent['five_block_beta_upper'])
    scalar_error = up(max(rabs) / (1 - beta))
    resolvent = [[F(x) for x in row] for row in parent['nonnegative_componentwise_resolvent']]
    errors = [up(sum(a * b for a, b in zip(row, rabs))) for row in resolvent]
    need(all(e <= scalar_error for e in errors), 'componentwise common response refines scalar bound')
    t1 = [x + I(-e, e) for x, e in zip(star, errors)]
    w1 = [unpack(x) for x in parent['response_next_eta_coefficient_enclosure']]
    x, y, opening, _, _, omega = box
    alpha, A, D, W = 1 + x, 1 - eta * (1 + x), 1 - eta * (1 + y), 1 + eta * omega
    need(A.lo > 0 and D.lo > 0 and W.lo > 0 and opening.lo > 0, 'all physical distance/opening domains')
    deflated = alpha * (3 - 3 * eta * alpha + square(eta) * square(alpha)) / (A**3)
    omega_term = omega * (2 + eta * omega) / square(W)
    centered = -deflated - omega_term + 2 * w1[-1] / square(W)
    Hodd = -square(second['n1']) / (opening * W**3) + 3 * square(second['m1'] * opening - D * second['n1']) / (opening * W**5)
    common = -3 * deflated - 3 * omega_term - 2 * t1[-1] / square(W) + Hodd
    need(3 < centered.lo <= centered.hi < 6, 'whole-box centered imaginary eigenvalue')
    need(400 < common.lo <= common.hi < 650, 'whole-box common imaginary directional coefficient')
    return {'parameter_radius': str(radius), 'eta_domain': ['0', '1/65536'],
        'parent_real_certificate': parent,
        'odd_matrix': [[x.record() for x in row] for row in odd['O']],
        'odd_forcing': [x.record() for x in odd['force']], 'odd_determinant': odd['det'].record(),
        'physical_circle_denominators': [x.record() for x in odd['physical_denominators']],
        'common_odd_first_response': [odd['V'].record(), odd['M'].record()],
        'common_reduced_forcing': [x.record() for x in second['forcing']],
        'phase_first_normalized_response': [x.record() for x in second['phase_b']],
        'moving_root_correction': [[x.record() for x in row] for row in second['moving_root_correction']],
        'common_preconditioned_residual': [x.record() for x in pre],
        'common_scalar_response_error': str(scalar_error),
        'common_componentwise_response_errors': list(map(str, errors)),
        'common_next_response': [x.record() for x in t1],
        'centered_imaginary_eta2_eigenvalue': centered.record(),
        'common_imaginary_eta2_directional_coefficient': common.record(),
        'common_imaginary_eta2_eigenvalue': (common / 3).record()}
