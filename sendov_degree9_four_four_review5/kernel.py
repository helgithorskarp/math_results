"""six-reviewer-5: fresh integer expansion of eight linear complex factors.

No researcher module is imported. The ring is Z[b,c,x,eta,d,y] modulo
d*d=1-c*c and y*y=1-x*x. Gaussian coefficients are pairs of integers.
"""
from collections import defaultdict
from fractions import Fraction as F
from math import comb


def require(ok, reason):
    if not ok:
        raise ArithmeticError(reason)


def add(*polys):
    r = defaultdict(int)
    for p in polys:
        for e, v in p.items():
            r[e] += v
    return {e: v for e, v in r.items() if v}


def scale(p, v):
    return {e: a*v for e, a in p.items() if a*v}


def multiply(p, q, circles=False):
    r = defaultdict(int)
    for e, a in p.items():
        for f, b in q.items():
            h = tuple(x+y for x, y in zip(e, f))
            if not circles:
                r[h] += a*b
                continue
            require(h[4] <= 2 and h[5] <= 2, 'Nonreduced circle input')
            d2, y2 = h[4]//2, h[5]//2
            for j in range(d2+1):
                for k in range(y2+1):
                    z = (h[0], h[1]+2*j, h[2]+2*k, h[3], h[4]%2, h[5]%2)
                    r[z] += a*b*(-1)**(j+k)
    return {e: v for e, v in r.items() if v}


def power(p, n, circles=False):
    r = {(0,)*len(next(iter(p))): 1}
    for _ in range(n):
        r = multiply(r, p, circles)
    return r


def variable(axis, n=4):
    e = [0]*n
    e[axis] = 1
    return {tuple(e): 1}


def origin_kernel(progress=lambda _: None):
    one = {(0,)*6: 1}
    b, c, x, eta, d, y = [variable(i, 6) for i in range(6)]
    mul = lambda p, q: multiply(p, q, True)
    # Re/Im of w(c+id) and w(c-id); expand the eight LINEAR factors.
    ur = add(mul(x, c), scale(mul(y, d), -1))
    ui = add(mul(x, d), mul(y, c))
    vr = add(mul(x, c), mul(y, d))
    vi = add(scale(mul(x, d), -1), mul(y, c))
    factors = []
    for r, i, s in [(ur, ui, 1)]*4 + [(vr, vi, -1)]*4:
        radius = add(one, scale(eta, s))
        factors.append((add(one, scale(mul(b, mul(radius, r)), -1)),
                        scale(mul(b, mul(radius, i)), -1)))
    real, imag = one, {}
    for fr, fi in factors:
        real, imag = add(mul(real, fr), scale(mul(imag, fi), -1)), add(mul(real, fi), mul(imag, fr))
    # 2520 is divisible by 1,...,9. Integration uses integer arithmetic.
    real = {e: v*(9*2520//(e[0]+1)) for e, v in real.items()}
    imag = {e: v*(9*2520//(e[0]+1)) for e, v in imag.items()}
    progress(('integrated-linear-factors', len(real), len(imag)))
    norm = add(mul(real, real), mul(imag, imag))
    even, odd = {}, {}
    for e, v in norm.items():
        if e[4:] == (0, 0) and e[3]%2 == 0:
            even[(e[0], e[1], e[2], e[3]//2)] = F(v, 2520**2)
        elif e[4:] == (1, 1) and e[3]%2 == 1:
            # lambda = -eta*d*y; remove that single signed factor.
            odd[(e[0], e[1], e[2], (e[3]-1)//2)] = F(-v, 2520**2)
        else:
            raise ArithmeticError('Forbidden norm parity')
    require((len(even), len(odd)) == (551, 295), 'Norm inventory')
    return even, odd


def weighted(even, odd):
    """Fresh explicit substitution b=t(cx+L), L^2=Q(1-c^2)(1-x^2)."""
    p, r = defaultdict(F), defaultdict(F)
    for offset, kernel in enumerate([even, odd]):
        for (b, c, x, q), coefficient in kernel.items():
            for ell in range(b+1):
                j = (ell+offset)//2
                output = r if (ell+offset)%2 else p
                for h in range(j+1):
                    for k in range(j+1):
                        e = (b, c+b-ell+2*h, x+b-ell+2*k, q+j)
                        output[e] += coefficient*comb(b, ell)*comb(j, h)*comb(j, k)*(-1)**(h+k)
    return add(p), add(r)


def parameters(p, eta=False, signed=False):
    """Q=q/4, or Q=z^2/4 and an extra eta=z/2."""
    r = defaultdict(F)
    for e, a in p.items():
        r[e[:3]+((2*e[3]+int(signed)) if eta else e[3],)] += a*F(1,4)**e[3]*(F(1,2) if signed else 1)
    return add(r)


def unweighted(p):
    r = defaultdict(F)
    for (b, c, x, q), a in p.items():
        r[(b, c+b, x+b, q)] += a
    return add(r)


def evaluate(p, coordinates):
    powers = [[v**k for k in range(1+max(e[i] for e in p))] for i, v in enumerate(coordinates)]
    return sum(a*powers[0][e[0]]*powers[1][e[1]]*powers[2][e[2]]*powers[3][e[3]] for e, a in p.items())


def canonical(p):
    return [[list(e), str(a)] for e, a in sorted(p.items())]
