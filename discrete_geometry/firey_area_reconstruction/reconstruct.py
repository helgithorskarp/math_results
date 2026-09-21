"""Exact reconstruction from a Firey area jet of a rational symmetric polygon.

Only standard-library rational arithmetic. Input jet[d][j] is the coefficient
of x**j*y**(d-j); absent odd degrees are zero. The decoder receives no geometry.
This rational-root implementation is a certificate-quality prototype, not a
complexity or numerical-stability claim for general real data.
"""
from fractions import Fraction as F
from math import comb, gcd, isqrt, lcm


def require(ok, message):
    if not ok:
        raise ValueError(message)


def rref(matrix):
    a = [[F(x) for x in row] for row in matrix]
    if not a:
        return a, []
    row, pivots = 0, []
    for col in range(len(a[0])):
        pivot = next((i for i in range(row, len(a)) if a[i][col]), None)
        if pivot is None:
            continue
        a[row], a[pivot] = a[pivot], a[row]
        q = a[row][col]
        a[row] = [x/q for x in a[row]]
        for i in range(len(a)):
            if i != row and a[i][col]:
                q = a[i][col]
                a[i] = [x-q*y for x, y in zip(a[i], a[row])]
        pivots.append(col)
        row += 1
        if row == len(a):
            break
    return a, pivots


def multiply(a, b):
    """Homogeneous binary forms, indexed by exponent of the first variable."""
    c = [F(0)] * (len(a)+len(b)-1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            c[i+j] += x*y
    return c


def evaluate(a, u):
    d = len(a)-1
    return sum((x*u[0]**i*u[1]**(d-i) for i, x in enumerate(a)), F(0))


def moments(jet, d):
    require(d > 0 and d % 2 == 0 and d in jet, 'missing positive even degree')
    require(len(jet[d]) == d+1, 'bad homogeneous coefficient count')
    scale = (-1)**(d//2-1)*(d-1)
    return [F(c)*scale/comb(d, i) for i, c in enumerate(jet[d])]


def gram(jet, k):
    m = moments(jet, 2*k)
    return [[m[i+j] for j in range(k+1)] for i in range(k+1)]


def divisors(n):
    require(n > 0, 'positive integer required')
    factors, q = [], 2
    while q*q <= n:
        e = 0
        while n % q == 0:
            n //= q
            e += 1
        if e:
            factors.append((q, e))
        q = 3 if q == 2 else q+2
    if n > 1:
        factors.append((n, 1))
    ds = [1]
    for p, e in factors:
        ds = [d*p**a for d in ds for a in range(e+1)]
    return ds


def primitive(a):
    den = lcm(*(x.denominator for x in a))
    ints = [int(x*den) for x in a]
    g = gcd(*ints)
    return [x//g for x in ints]


def rational_projective_roots(poly):
    """All distinct roots, including infinity; reject non-rational/multiple roots."""
    r = len(poly)-1
    a = list(poly)
    roots = []
    if a[-1] == 0:
        roots.append((F(1), F(0)))
        a.pop()
        require(a[-1] != 0, 'multiple root at infinity')
    while len(a) > 1:
        if a[0] == 0:
            root = F(0)
        else:
            ints = primitive(a)
            candidates = {F(s*n, d) for n in divisors(abs(ints[0]))
                          for d in divisors(abs(ints[-1])) for s in [-1, 1]}
            root = next((x for x in sorted(candidates)
                         if evaluate(a, (x, F(1))) == 0), None)
            require(root is not None, 'kernel does not split over the rationals')
        v = (root, F(1))
        require(v not in roots, 'multiple projective root')
        roots.append(v)
        # Exact synthetic division by X-root in the chart Y=1.
        b = [F(0)]*(len(a)-1)
        b[-1] = a[-1]
        for i in range(len(b)-2, -1, -1):
            b[i] = a[i+1]+root*b[i+1]
        require(a[0]+root*b[0] == 0, 'nonzero division remainder')
        a = b
    require(len(roots) == r, 'incomplete projective factorization')
    return sorted(roots)


def rational_sqrt(x):
    require(x > 0, 'nonpositive radial square')
    a, b = isqrt(x.numerator), isqrt(x.denominator)
    require(a*a == x.numerator and b*b == x.denominator,
            'radial endpoint is not rational')
    return F(a, b)


def decode(jet):
    """Return (facet-pair count, polar endpoints, kernel) using the jet alone."""
    maximum = max(jet)//2
    found = None
    for k in range(1, maximum+1):
        reduced, pivots = rref(gram(jet, k))
        if len(pivots) < k+1:
            found = (k, reduced, pivots)
            break
    require(found is not None, 'no finite facet-support certificate in supplied jet')
    r, reduced, pivots = found
    require(r >= 2 and len(pivots) == r, 'not a full-dimensional polygon certificate')
    free = next(i for i in range(r+1) if i not in pivots)
    kernel = [F(0)]*(r+1)
    kernel[free] = F(1)
    for i, col in enumerate(pivots):
        kernel[col] = -reduced[i][free]
    directions = rational_projective_roots(kernel)
    linear_factors = [[-v[0], v[1]] for v in directions]
    low, high = moments(jet, 2*r-2), moments(jet, 2*r)
    polar = []
    for j, v in enumerate(directions):
        q = [F(1)]
        for i, ell in enumerate(linear_factors):
            if i != j:
                q = multiply(q, ell)
        a = [F(1)/v[1], F(0)] if v[1] else [F(0), F(1)/v[0]]
        q2 = multiply(q, q)
        aq2 = multiply(multiply(a, a), q2)
        denominator = sum(x*y for x, y in zip(q2, low))
        numerator = sum(x*y for x, y in zip(aq2, high))
        require(denominator > 0, 'nonpositive isolated moment')
        alpha = rational_sqrt(numerator/denominator)
        u = tuple(alpha*x for x in v)
        polar.extend([u, tuple(-x for x in u)])
    return r, tuple(sorted(polar)), tuple(kernel)
