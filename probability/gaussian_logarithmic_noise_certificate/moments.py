"""Exact marginal-moment producer for the signed theorem in PROOF.md.

No replica-tuple enumeration in production. Python >=3.11, standard library.
The general Taylor remainder is the explicitly pinned R3 written theorem.
"""
from fractions import Fraction as F
from math import comb, factorial, isqrt


def need(condition, message):
    if not condition:
        raise ValueError(message)


def interval_scale(interval, scalar):
    a, b = interval
    need(a <= b, "ordered interval")
    vals = (a * scalar, b * scalar)
    return min(vals), max(vals)


def weighted_degree(key):
    return sum(key[:3]) + 2 * key[3]


def moment_keys(q):
    for k in range(q + 1):
        d = 2 * q - 2 * k
        for a in range(d + 1):
            for b in range(d - a + 1):
                for c in range(d - a - b + 1):
                    yield a, b, c, k


def egf(points, weights, q):
    out = {}
    for key in moment_keys(q):
        a, b, c, k = key
        moment = sum(w * x[0] ** a * x[1] ** b * x[2] ** c
                     * sum(v * v for v in x) ** k
                     for x, w in zip(points, weights))
        if moment:
            out[key] = moment / (factorial(a) * factorial(b) * factorial(c) * factorial(k))
    return out


def egf_multiply(a, b, q):
    out = {}
    graded_b = [(key, v, weighted_degree(key)) for key, v in b.items()]
    for ka, va in a.items():
        da = weighted_degree(ka)
        for kb, vb, db in graded_b:
            if da + db <= 2 * q:
                key = tuple(x + y for x, y in zip(ka, kb))
                out[key] = out.get(key, F(0)) + va * vb
    return {key: v for key, v in out.items() if v}


def scatter_moment(generating, m, r):
    total = F(0)
    for k in range(r + 1):
        for a in range(k + 1):
            for b in range(k - a + 1):
                c = k - a - b
                key = (2 * a, 2 * b, 2 * c, r - k)
                raw = generating.get(key, F(0))
                for v in key:
                    raw *= factorial(v)
                coeff = comb(r, k) * F(-1, m) ** k
                coeff *= F(factorial(k), factorial(a) * factorial(b) * factorial(c))
                total += coeff * raw
    return total / 2 ** r


def scatter_table(points, weights, q, max_m):
    """Exact moments of iid scatter; polynomial state space, no tuples."""
    base = egf(points, weights, q)
    g = {(0, 0, 0, 0): F(1)}
    rows = {}
    for m in range(1, max_m + 1):
        g = egf_multiply(g, base, q)
        if m >= 2:
            rows[m] = [scatter_moment(g, m, r) for r in range(q + 1)]
    return rows


def inverse_radical_interval(coefficient, m, bits=96):
    need(m >= 2 and bits >= 8, "radical precision")
    scale_factor = 2 ** bits
    radicand = m * scale_factor ** 2
    r = isqrt(radicand)
    lo = F(r, scale_factor)
    hi = lo if r * r == radicand else F(r + 1, scale_factor)
    return interval_scale((1 / hi, 1 / lo), F(coefficient))


def finite_input(source, target, weights, epsilon):
    x = [tuple(map(F, row)) for row in source]
    y = [tuple(map(F, row)) for row in target]
    w = list(map(F, weights))
    need(len(x) == len(y) == len(w) > 0, "matching finite input lengths")
    need(all(len(v) == 3 for v in x + y), "three coordinates per site")
    need(all(v >= 0 for v in w) and sum(w) == 1, "probability weights")
    epsilon = F(epsilon)
    need(0 < epsilon <= F(1, 2), "small-radius input")
    need(all(sum(t * t for t in row) <= epsilon for row in x + y), "both radius bounds")
    loss = F(0)
    for i in range(len(x)):
        for j in range(len(x)):
            gap = sum((a - b) ** 2 for a, b in zip(x[i], x[j]))
            gap -= sum((a - b) ** 2 for a, b in zip(y[i], y[j]))
            need(gap >= 0, "pairwise contraction")
            loss += w[i] * w[j] * gap
    return x, y, w, loss


def finite_taylor_moments(source, target, weights, epsilon, q, max_m, bits=96):
    """Return L_m intervals and exact rational coefficients L_m*sqrt(m)."""
    need(q >= 2 and max_m >= 2, "moment degrees")
    x, y, w, loss = finite_input(source, target, weights, epsilon)
    xx = scatter_table(x, w, q, max_m)
    yy = scatter_table(y, w, q, max_m)
    coefficients, intervals = [], []
    for m in range(2, max_m + 1):
        paired = sum(F((-1) ** r, factorial(r)) * (yy[m][r] - xx[m][r])
                     for r in range(q + 1))
        c = paired / (m ** 2 * (m - 1))
        coefficients.append(c)
        intervals.append(inverse_radical_interval(c, m, bits))
    return {"loss": loss, "coefficients": coefficients, "intervals": intervals,
            "source_scatters": xx, "target_scatters": yy}
