"""Exact arithmetic in Q[a,x] and Gaussian rationals; no numeric dependencies."""
from fractions import Fraction as F
from math import comb

ONE = {(0, 0): F(1)}
A = {(1, 0): F(1)}
X = {(0, 1): F(1)}


def add(p, q):
    out = dict(p)
    for m, c in q.items():
        out[m] = out.get(m, F(0)) + c
        if not out[m]:
            del out[m]
    return out


def scale(p, s):
    return {m: c * s for m, c in p.items() if c * s}


def mul(p, q):
    out = {}
    for (i, j), c in p.items():
        for (k, l), d in q.items():
            out[i + k, j + l] = out.get((i + k, j + l), F(0)) + c * d
    return {m: c for m, c in out.items() if c}


def power(p, n):
    out = ONE
    for _ in range(n):
        out = mul(out, p)
    return out


def evaluate(p, a, x):
    return sum(c * a**i * x**j for (i, j), c in p.items())


def subx(p, lo, slope):
    """Substitute x=lo(a)+slope(a)y, retaining exponent order (a,y)."""
    out = {}
    mx = max((j for _, j in p), default=0)
    pl = [power(lo, k) for k in range(mx + 1)]
    ps = [power(slope, k) for k in range(mx + 1)]
    for (i, j), c in p.items():
        for k in range(j + 1):
            part = scale(mul(pl[j-k], ps[k]), c * comb(j, k))
            out = add(out, {(h+i, t+k): v for (h, t), v in part.items()})
    return out


def suba(p, lo, hi):
    out = {}
    for (i, j), c in p.items():
        for k in range(i + 1):
            out[k, j] = out.get((k, j), F(0)) + c*comb(i, k)*lo**(i-k)*(hi-lo)**k
    return {m: c for m, c in out.items() if c}


def bernstein(p):
    da = max((i for i, j in p), default=0)
    dy = max((j for i, j in p), default=0)
    arr = [[p.get((i, j), F(0)) for j in range(dy+1)] for i in range(da+1)]
    temp = [[sum(arr[i][j]*F(comb(k, i), comb(da, i)) for i in range(k+1))
             for j in range(dy+1)] for k in range(da+1)]
    vals = [[sum(temp[k][j]*F(comb(l, j), comb(dy, j)) for j in range(l+1))
             for l in range(dy+1)] for k in range(da+1)]
    return (da, dy), vals


def inverse_bernstein(vals):
    """Inverse via tensor finite differences, with no forward-transform reuse."""
    da, dy = len(vals)-1, len(vals[0])-1
    temp = [[comb(da, i)*sum(F((-1)**(i-k)*comb(i, k))*vals[k][l]
             for k in range(i+1)) for l in range(dy+1)] for i in range(da+1)]
    arr = [[comb(dy, j)*sum(F((-1)**(j-l)*comb(j, l))*temp[i][l]
            for l in range(j+1)) for j in range(dy+1)] for i in range(da+1)]
    return {(i, j): c for i, row in enumerate(arr) for j, c in enumerate(row) if c}


def coefficients():
    b = add(ONE, {(2, 0): F(-1)})
    oc = [{(k, 0): F(9*comb(8, k)*(-1)**k, k+1)} for k in range(9)]
    cc = [scale(mul(power(A, 8-k), power(b, k)), F(comb(8, k), k+1))
          for k in range(9)]
    return b, oc, cc


def chebyshev_norm(cs):
    ts = [ONE, X]
    for _ in range(2, 9):
        ts.append(add(scale(mul(X, ts[-1]), 2), scale(ts[-2], -1)))
    out = {}
    for j, c in enumerate(cs):
        out = add(out, mul(c, c))
        for k in range(j):
            out = add(out, scale(mul(mul(c, cs[k]), ts[j-k]), 2))
    return out


def quotient_norm(cs):
    """Independent reduction in Q[a,x,q]/(q^2-2xq+1).

    A pair represents P+Qq. For unit q, conjugation sends q to 2x-q;
    the resulting norm is P^2+2xPQ+Q^2.
    """
    qp = (ONE, {})
    p, q = {}, {}
    for c in cs:
        p, q = add(p, mul(c, qp[0])), add(q, mul(c, qp[1]))
        qp = (scale(qp[1], -1), add(qp[0], scale(mul(X, qp[1]), 2)))
    return add(add(mul(p, p), scale(mul(X, mul(p, q)), 2)), mul(q, q))


def phase_polynomials():
    b, oc, cc = coefficients()
    no, nc = chebyshev_norm(oc), chebyshev_norm(cc)
    r = add(ONE, scale(mul(b, add(no, scale(ONE, -1))), F(4, 3)))
    d = add(mul(r, r), scale(nc, -1))
    lo, slope = scale(A, F(1, 2)), add(ONE, scale(A, F(-1, 2)))
    return no, nc, subx(r, lo, slope), subx(d, lo, slope)


def gaussian_add(z, w):
    return z[0]+w[0], z[1]+w[1]


def gaussian_mul(z, w):
    return z[0]*w[0]-z[1]*w[1], z[0]*w[1]+z[1]*w[0]


def gaussian_power(z, n):
    out = F(1), F(0)
    for _ in range(n):
        out = gaussian_mul(out, z)
    return out


def gaussian_sum(cs, a, q):
    out = F(0), F(0)
    for k, c in enumerate(cs):
        v = evaluate(c, a, F(0))
        z = gaussian_power(q, k)
        out = gaussian_add(out, (v*z[0], v*z[1]))
    return out


def norm2(z):
    return z[0]**2 + z[1]**2


def polar_modulus_integral(a, x):
    """Integral [a^2+2abxt+b^2t^2]^4, |q|=1, exactly."""
    b = 1-a*a
    factor = [a*a, 2*a*b*x, b*b]
    cs = [F(1)]
    for _ in range(4):
        out = [F(0)]*(len(cs)+2)
        for i, c in enumerate(cs):
            for j, d in enumerate(factor):
                out[i+j] += c*d
        cs = out
    return sum(c/F(j+1) for j, c in enumerate(cs))
