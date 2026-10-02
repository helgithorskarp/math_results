"""Separate Gaussian Taylor products retain both individual heavy roots."""
from math import comb
from parents import F, need, convolution, power, evaluate, derivative, K, I
from complex_sector import polynomials, common_second, add_polys, scale, primitive


class G:
    def __init__(self, re=0, im=0):
        if isinstance(re, G):
            self.re, self.im = re.re, re.im
        else:
            need(not isinstance(re, float) and not isinstance(im, float), 'exact Gaussian inputs')
            self.re, self.im = F(re), F(im)
    def __add__(self, b):
        b = G(b)
        return G(self.re + b.re, self.im + b.im)
    __radd__ = __add__
    def __neg__(self):
        return G(-self.re, -self.im)
    def __sub__(self, b):
        return self + -G(b)
    def __rsub__(self, b):
        return G(b) + -self
    def __mul__(self, b):
        b = G(b)
        return G(self.re * b.re - self.im * b.im, self.re * b.im + self.im * b.re)
    __rmul__ = __mul__
    def __truediv__(self, b):
        b = G(b)
        d = b.re**2 + b.im**2
        need(d != 0, 'nonzero Gaussian divisor')
        return G((self.re * b.re + self.im * b.im) / d, (self.im * b.re - self.re * b.im) / d)
    def __pow__(self, n):
        out = G(1)
        for _ in range(n):
            out *= self
        return out
    def conjugate(self):
        return G(self.re, -self.im)
    def __eq__(self, b):
        b = G(b)
        return (self.re, self.im) == (b.re, b.im)
    def record(self):
        return [str(self.re), str(self.im)]


class J:
    """Three literal delta coefficients; no derivative factorial convention."""
    def __init__(self, values=(0, 0, 0)):
        self.v = tuple(map(G, values)) if isinstance(values, (tuple, list)) else (G(values), G(0), G(0))
        need(len(self.v) == 3, 'three Taylor coefficients')
    def __add__(self, b):
        b = b if isinstance(b, J) else J(b)
        return J([a + x for a, x in zip(self.v, b.v)])
    __radd__ = __add__
    def __neg__(self):
        return J([-x for x in self.v])
    def __sub__(self, b):
        return self + -(b if isinstance(b, J) else J(b))
    def __rsub__(self, b):
        return J(b) + -self
    def __mul__(self, b):
        b = b if isinstance(b, J) else J(b)
        return J([sum((self.v[k] * b.v[j - k] for k in range(j + 1)), G(0)) for j in range(3)])
    __rmul__ = __mul__
    def __truediv__(self, b):
        need(not isinstance(b, J), 'Taylor division only by constant')
        return J([x / b for x in self.v])
    def __pow__(self, n):
        out = J(1)
        for _ in range(n):
            out *= self
        return out
    def conjugate(self):
        return J([x.conjugate() for x in self.v])


def actual_roots(b, us, hs, y, q0, V, M):
    eta = b * b
    m1 = (eta * V - sum(hs)) / 2
    n1 = (M - sum(h * u for h, u in zip(hs, us)) - 2 * m1 * y) / 2
    roots = [J([eta * u, G(0, b * h), 0]) for u, h in zip(us, hs)]
    for sign in (1, -1):
        roots.append(J([G(eta * y, sign * b * q0), G(sign * eta * n1 / q0, b * m1), G(0, -sign * b * m1**2 / (2 * q0))]))
    return roots, m1, n1


def actual_primitive(roots, anchor):
    raw = [J(1)]
    for root in roots:
        raw = convolution(raw, [-root, J(1)])
    out = [J(0)] + [9 * x / F(j + 1) for j, x in enumerate(raw)]
    out[0] -= evaluate(out, anchor)
    return out


def run():
    checks = 0
    damages = []
    records = []
    def check(ok, label):
        nonlocal checks
        need(ok, label)
        checks += 1
    def reject(name, predicate):
        try:
            need(predicate, 'damaged object ' + name)
        except ValueError:
            damages.append(name)
            return
        raise ValueError('damage accepted ' + name)
    # This multiplication oracle directly expands monomials and compares
    # every Gaussian coefficient with the independently truncated jet.
    for j in range(5):
        for k in range(5):
            a, b = G(F(j + 1, 7), F(k - 2, 11)), G(F(2 - j, 13), F(k + 3, 17))
            check((a * b).re == a.re * b.re - a.im * b.im and (a * b).im == a.re * b.im + a.im * b.re, 'Gaussian literal component products')
            if b != 0:
                check((a / b) * b == a, 'both Gaussian exact inverse components')
    for b in (F(1, 8), F(1, 16), F(1, 32)):
        eta, q0 = b * b, F(3)
        D, W = 4 * b, 5 * b
        y = (1 - D) / eta - 1
        x, V, M = F(-2, 3), F(7, 5), F(-4, 7)
        opening = q0**2
        v = [x, y, opening, F(2, 7), F(-1, 6), (W - 1) / eta]
        p, split, qv, qm, qd = polynomials(eta, v)
        literal_cases = []
        for name, hs, vv, mm in [('common', [1] * 6, V, M), ('V', [0] * 6, F(1), F(0)), ('M', [0] * 6, F(0), F(1)), ('centered', [1, -1, 0, 0, 0, 0], F(0), F(0))]:
            roots, m1, n1 = actual_roots(b, [x] * 6, hs, y, q0, vv, mm)
            primitive_all = actual_primitive(roots, 1 - eta)
            for j in range(10):
                check(primitive_all[j].v[0] == p[j], 'whole baseline coefficient')
            check(all(t == 0 for t in evaluate(primitive_all, 1 - eta).v), 'all marked-anchor coefficients')
            if name == 'common':
                odd = {'V': V, 'M': M, 'p': p, 'split': split, 'qv': qv, 'qm': qm, 'qd': qd, 'phases': [F(3, 5), F(5, 13)]}
                second = common_second(eta, v, F(15, 16), odd)
                first = add_polys(qd, scale(qv, V), scale(qm, M))
                p2 = add_polys(scale(split, -3 * eta), scale(second['R'], eta**2))
                for j in range(10):
                    check(primitive_all[j].v[1] == G(0, eta * b * (first[j] if j < len(first) else 0)), 'every cancelled common first coefficient')
                    check(primitive_all[j].v[2] == (p2[j] if j < len(p2) else 0), 'every actual common second coefficient')
                # Recover real/imaginary heavy coordinates literally from
                # each root and independently verify the four moments.
                hs_all = [J([q.im / b for q in root.v]) for root in roots]
                us_all = [J([q.re / eta for q in root.v]) for root in roots]
                check(sum(hs_all, J(0)).v == J([0, eta * V, 0]).v, 'actual complete imaginary first moment')
                check(sum((h * u for h, u in zip(hs_all, us_all)), J(0)).v == J([0, M, 0]).v, 'actual complete mixed moment')
                check(sum(us_all, J(0)).v == J(6 * x + 2 * y).v, 'actual complete real sum')
                check(sum((h * h for h in hs_all), J(0)).v == J([2 * opening, 0, 6]).v, 'actual complete imaginary square moment')
                check(second['m1'] == m1 and second['n1'] == n1, 'literal response coefficients')
                actual_distance_rows = []
                heavy_coefficients = []
                for sign, root in zip((1, -1), roots[-2:]):
                    distance = J(1 - eta) - root
                    squared = distance * distance.conjugate()
                    first_squared = sign * 2 * eta * (m1 * opening - D * n1) / q0
                    second_squared = eta**2 * n1**2 / opening
                    check(squared.v == J([W**2, first_squared, second_squared]).v, 'all actual heavy squared-distance coefficients')
                    reciprocal_second = -second_squared / (2 * W**3) + 3 * first_squared**2 / (8 * W**5)
                    heavy_coefficients.append(reciprocal_second)
                    actual_distance_rows.append([q.record() for q in squared.v])
                Hodd = -n1**2 / (opening * W**3) + 3 * (m1 * opening - D * n1)**2 / (opening * W**5)
                check(sum(heavy_coefficients) == eta**2 * Hodd, 'literal two-heavy reciprocal coefficient')
                literal_cases.append({'case': name, 'whole_primitive_coefficients': [[q.record() for q in z.v] for z in primitive_all], 'heavy_squared_distances': actual_distance_rows})
                reject('lost-heavy-asymmetry-square', sum(heavy_coefficients) == -eta**2 * n1**2 / (opening * W**3))
                reject('lost-common-integration-factor', primitive_all[6].v[2] == G(p2[6] + 1))
                wrong = add_polys(scale(split, -3 * eta), scale(second['R'], eta))
                reject('lost-common-second-eta', all(primitive_all[j].v[2] == (wrong[j] if j < len(wrong) else 0) for j in range(10)))
                reject('lost-common-first-eta', all(primitive_all[j].v[1] == G(0, b * (first[j] if j < len(first) else 0)) for j in range(10)))
                changed_roots = roots[:6] + [J([root.v[0], root.v[1], G(0)]) for root in roots[-2:]]
                changed_h = [J([q.im / b for q in root.v]) for root in changed_roots]
                reject('lost-heavy-square-root-second-term', sum((h * h for h in changed_h), J(0)).v == J([2 * opening, 0, 6]).v)
                changed_anchor = primitive_all[:];changed_anchor[0] += 1
                reject('lost-original-marked-anchor', all(q == 0 for q in evaluate(changed_anchor, 1 - eta).v))
            elif name in ('V', 'M'):
                partial = qv if name == 'V' else qm
                for j in range(10):
                    check(primitive_all[j].v[1] == G(0, eta * b * (partial[j] if j < len(partial) else 0)), 'every original odd partial coefficient')
            else:
                for j in range(10):
                    check(primitive_all[j].v[1] == 0, 'all centered first coefficients vanish')
                    check(primitive_all[j].v[2] == -eta * (split[j] if j < len(split) else 0), 'all centered imaginary split coefficients')
        # Compose the full moving unit root by direct powers. Include an
        # arbitrary second tangential phase, rather than assuming it zero.
        q = add_polys(qd, scale(qv, V), scale(qm, M))
        P2 = add_polys(scale(split, -3 * eta), scale(second['R'], eta**2))
        for co, si in [(F(3, 5), F(4, 5)), (F(5, 13), F(12, 13))]:
            z, bb, theta2 = G(co, si), F(7, 11), F(-5, 17)
            theta1 = -eta * b * bb
            moving = J([z, z * G(0, theta1), z * G(-theta1**2 / 2, theta2)])
            full = [J([p[j], G(0, eta * b * (q[j] if j < len(q) else 0)), P2[j] if j < len(P2) else 0]) for j in range(10)]
            composition = evaluate(full, moving)
            correction = bb * z * evaluate(derivative(q), z) - bb**2 * (z * evaluate(derivative(p), z) + z**2 * evaluate(derivative(derivative(p)), z)) / 2
            predicted = evaluate(P2, z) + eta**3 * correction + G(0, theta2) * z * evaluate(derivative(p), z)
            check(composition.v[2] == predicted, 'entire moving unit-root Taylor composition')
            check((moving * moving.conjugate()).v == J(1).v, 'all moving unit-modulus coefficients')
            omitted = predicted + eta**3 * bb**2 * z * evaluate(derivative(p), z) / 2
            reject('omitted-radial-acceleration', composition.v[2] == omitted)
        records.append({'sqrt_eta': str(b), 'eta': str(eta), 'literal_cases': literal_cases})
    # Two-sector norms and a full arbitrary twelve-coordinate quadratic form
    # distinguish directional coefficients from Hessian eigenvalues.
    a, bb, c, d = F(7, 3), F(2, 9), F(11, 5), F(-1, 8)
    H = [[(a * int(i == j) + bb) if i < 6 and j < 6 else (c * int(i == j) + d) if i >= 6 and j >= 6 else F(0) for j in range(12)] for i in range(12)]
    for which, eig in [('real', a), ('imag', c)]:
        offset = 0 if which == 'real' else 6
        centered = [0] * 12;centered[offset:offset + 2] = [1, -1]
        common = [int(offset <= j < offset + 6) for j in range(12)]
        energy = lambda z: sum(z[i] * H[i][j] * z[j] for i in range(12) for j in range(12))
        check(sum(x*x for x in centered) == 2 and energy(centered) / 2 == eig, 'literal centered metric and Rayleigh factor')
        reject('lost-centered-metric-factor-two', energy(centered) == eig)
        common_eig = eig + 6 * (bb if which == 'real' else d)
        check(sum(x*x for x in common) == 6 and energy(common) / 6 == common_eig, 'literal common metric and Rayleigh factor')
        reject('common-direction-factor-three', energy(common) / 2 == common_eig)
    invalid = 0
    for action in [lambda: G(0.5), lambda: G(1) / G(0), lambda: J([1, 2]), lambda: J(1) / J(1)]:
        try:
            action()
        except ValueError:
            invalid += 1
    check(invalid == 4, 'all four exact/domain rejections')
    return {'checks': checks, 'positive_eta_whole_coefficients': records,
            'mathematical_damage_rejections': damages, 'invalid_domains_rejected': invalid,
            'literal_centered_squared_norm': 2, 'literal_common_squared_norm': 6}
