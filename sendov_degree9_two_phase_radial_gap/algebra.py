"""Exact polynomials in Q[a,c,x]; Python standard library only."""
from fractions import Fraction as F
from math import comb, factorial

ONE = {(0, 0, 0): F(1)}
A = {(1, 0, 0): F(1)}
C = {(0, 1, 0): F(1)}
X = {(0, 0, 1): F(1)}
B = {(0, 0, 0): F(1), (2, 0, 0): F(-1)}


def add(p, q):
    out = dict(p)
    for m, z in q.items():
        out[m] = out.get(m, F(0)) + z
        if not out[m]:
            del out[m]
    return out


def scale(p, z):
    return {m: t*z for m, t in p.items() if t*z}


def mul(p, q):
    out = {}
    for (i, j, k), z in p.items():
        for (h, l, m), t in q.items():
            key = (i+h, j+l, k+m)
            out[key] = out.get(key, F(0)) + z*t
    return {m: z for m, z in out.items() if z}


def power(p, n):
    out = ONE
    for _ in range(n):
        out = mul(out, p)
    return out


def degrees(p):
    return tuple(max((m[j] for m in p), default=0) for j in range(3))


def coefficient_lists():
    # First construction: four ordinary convolutions of (1-2ct+t^2).
    hs = [ONE]
    for _ in range(4):
        out = [{} for _ in range(len(hs)+2)]
        for j, z in enumerate(hs):
            for k, t in enumerate([ONE, scale(C, -2), ONE]):
                out[j+k] = add(out[j+k], mul(z, t))
        hs = out
    oc = [scale(mul(hs[k], power(A, k)), F(9, k+1)) for k in range(9)]
    cc = [scale(mul(mul(hs[k], power(A, 8-k)), power(B, k)),
                F((-1)**k, k+1)) for k in range(9)]
    return hs, oc, cc


def multinomial_coefficients():
    # Independent closed coefficient formula, not the convolution above.
    hs = [{} for _ in range(9)]
    for n1 in range(5):
        for n2 in range(5-n1):
            n0 = 4-n1-n2
            k = n1+2*n2
            z = F(factorial(4)*(-2)**n1,
                  factorial(n0)*factorial(n1)*factorial(n2))
            hs[k] = add(hs[k], {(0, n1, 0): z})
    return hs


def chebyshev_norm(cs):
    ts = [ONE, X]
    for _ in range(2, 9):
        ts.append(add(scale(mul(X, ts[-1]), 2), scale(ts[-2], -1)))
    out = {}
    for j, z in enumerate(cs):
        out = add(out, mul(z, z))
        for k in range(j):
            out = add(out, scale(mul(mul(z, cs[k]), ts[j-k]), 2))
    return out


def quotient_norm(cs):
    """Independent reduction modulo w^2-2xw+1; no Chebyshev recurrence.

    A pair represents P+Qw. Conjugation w -> 2x-w gives the norm
    P^2+2xPQ+Q^2. All polynomial coefficients are compared exactly.
    """
    wp = (ONE, {})
    p, q = {}, {}
    for z in cs:
        p, q = add(p, mul(z, wp[0])), add(q, mul(z, wp[1]))
        wp = (scale(wp[1], -1), add(wp[0], scale(mul(X, wp[1]), 2)))
    return add(add(mul(p, p), scale(mul(X, mul(p, q)), 2)), mul(q, q))


def divide_by_b(p):
    da, dc, dx = degrees(p)
    out = {}
    for j in range(dc+1):
        for k in range(dx+1):
            row = [p.get((i, j, k), F(0)) for i in range(da+1)]
            quo = [F(0)]*(da-1)
            for i in range(da-1):
                quo[i] = row[i] + (quo[i-2] if i >= 2 else F(0))
            if row[-2] != -quo[-2] or row[-1] != -quo[-1]:
                raise ArithmeticError('nonzero b-division remainder')
            for i, z in enumerate(quo):
                if z:
                    out[i, j, k] = z
    if mul(B, out) != p:
        raise ArithmeticError('complete b-factor identity')
    return out


def phase_polynomials():
    hs, oc, cc = coefficient_lists()
    no, nc = chebyshev_norm(oc), chebyshev_norm(cc)
    r = add(ONE, scale(mul(B, add(no, scale(ONE, -1))), F(4, 3)))
    h = divide_by_b(add(mul(r, r), scale(nc, -1)))
    delta2 = {(0, 0, 0): F(1), (1, 0, 0): F(-2), (2, 0, 0): F(1)}
    angular = add(ONE, {(0, 1, 1): F(-1)})
    k = add(add(h, scale(delta2, F(-1, 100))), scale(angular, F(-1, 1000)))
    return hs, oc, cc, no, nc, r, h, k


def coupled_axis(p, axis):
    """Selected cosine = a/2+(1-a/2)y, by a closed monomial formula."""
    out = {}
    for m, z in p.items():
        n = m[axis]
        for k in range(n+1):
            for h in range(k+1):
                mm = list(m)
                mm[axis] = k
                mm[0] += n-k+h
                mm = tuple(mm)
                factor = F(comb(n, k)*comb(k, h)*(-1)**h, 2**(n-k+h))
                out[mm] = out.get(mm, F(0)) + z*factor
    return {m: z for m, z in out.items() if z}


def coupled_horner(p, axis):
    """Independent affine substitution by grouped Horner evaluation."""
    groups = {}
    for m, z in p.items():
        key = list(m)
        key[axis] = 0
        groups.setdefault(tuple(key), {})[m[axis]] = z
    y = tuple(1 if j == axis else 0 for j in range(3))
    affine = add(scale(A, F(1, 2)), {y: F(1),
                 tuple(u+v for u, v in zip(y, (1, 0, 0))): F(-1, 2)})
    out = {}
    for key, row in groups.items():
        local = {}
        for n in range(max(row), -1, -1):
            local = add(mul(local, affine), scale(ONE, row.get(n, F(0))))
        out = add(out, {tuple(i+j for i, j in zip(key, m)): z
                        for m, z in local.items()})
    return out


def affine_axis(p, axis, lo, hi):
    out = {}
    for m, z in p.items():
        n = m[axis]
        for k in range(n+1):
            mm = list(m)
            mm[axis] = k
            mm = tuple(mm)
            out[mm] = out.get(mm, F(0)) + z*comb(n, k)*lo**(n-k)*(hi-lo)**k
    return {m: z for m, z in out.items() if z}


def bernstein(p):
    ds = degrees(p)
    out = dict(p)
    for axis, degree in enumerate(ds):
        groups = {}
        for m, z in out.items():
            key = m[:axis]+m[axis+1:]
            groups.setdefault(key, {})[m[axis]] = z
        ratios = [[F(comb(k, j), comb(degree, j)) for j in range(k+1)]
                  for k in range(degree+1)]
        nxt = {}
        for key, row in groups.items():
            for k in range(degree+1):
                z = sum(row.get(j, F(0))*ratios[k][j] for j in range(k+1))
                if z:
                    nxt[key[:axis]+(k,)+key[axis:]] = z
        out = nxt
    return ds, out


def inverse_bernstein(ds, vals):
    """Full tensor finite differences, independent of the forward ratios."""
    out = dict(vals)
    for axis, degree in enumerate(ds):
        groups = {}
        for m, z in out.items():
            key = m[:axis]+m[axis+1:]
            groups.setdefault(key, {})[m[axis]] = z
        factors = [[(-1)**(i-k)*comb(i, k)*comb(degree, i)
                    for k in range(i+1)] for i in range(degree+1)]
        nxt = {}
        for key, row in groups.items():
            for i in range(degree+1):
                z = sum(row.get(k, F(0))*factors[i][k] for k in range(i+1))
                if z:
                    nxt[key[:axis]+(i,)+key[axis:]] = z
        out = nxt
    return out
