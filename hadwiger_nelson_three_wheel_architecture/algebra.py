"""Small exact polynomial and modular coprimality checker; no CAS imports."""
from functools import reduce
from math import gcd, isqrt
from itertools import combinations
import hashlib


def need(ok, message):
    if not ok:
        raise ValueError(message)


def add(*polys):
    out = {}
    for p in polys:
        for ij, c in p.items():
            out[ij] = out.get(ij, 0)+c
    return {ij: c for ij, c in out.items() if c}


def scale(p, n):
    return {ij: c*n for ij, c in p.items() if c*n}


def mul(p, q):
    out = {}
    for (i, j), c in p.items():
        for (k, l), d in q.items():
            ij = i+k, j+l
            out[ij] = out.get(ij, 0)+c*d
    return {ij: c for ij, c in out.items() if c}


ONE = {(0, 0): 1}
DX = {(0, 0): 1, (2, 0): 3}
DY = {(0, 0): 1, (0, 2): 3}
CX = {(0, 0): 1, (2, 0): -3}
CY = {(0, 0): 1, (0, 2): -3}
SX = {(1, 0): 2}
SY = {(0, 1): 2}


def vector(c):
    need(len(c) == 9 and all(type(a) is int for a in c), 'polynomial coefficients')
    return {(i, j): c[3*i+j] for i in range(3) for j in range(3) if c[3*i+j]}


def primitive(p):
    need(all(i <= 2 and j <= 2 for i, j in p), 'polynomial bidegree')
    cs = tuple(p.get((i, j), 0) for i in range(3) for j in range(3))
    g = reduce(gcd, cs)
    if not g:
        return cs
    if next(c for c in reversed(cs) if c) < 0:
        g = -g
    return tuple(c//g for c in cs)


def divide_exact(p, q):
    """Integer-coefficient lexicographic long division, with zero remainder."""
    p = dict(p); out = {}; ij = max(q); lc = q[ij]
    while p:
        kl = max(p)
        need(kl[0] >= ij[0] and kl[1] >= ij[1], 'nonzero polynomial remainder')
        need(p[kl] % lc == 0, 'nonintegral quotient')
        monomial = kl[0]-ij[0], kl[1]-ij[1]
        coeff = p[kl]//lc
        out[monomial] = coeff
        p = add(p, scale(mul({monomial: coeff}, q), -1))
    return out


def unit_polynomial(ds):
    """Expand the actual squared distance, not the producer's dot formula."""
    (a, b), (c, d), (e, f) = [(2*a+b, b) for a, b in ds]
    den = mul(DX, DY)
    real = add(scale(den, a), mul(add(scale(CX, c), scale(SX, -3*d)), DY),
               mul(add(scale(CY, e), scale(SY, -3*f)), DX))
    imag = add(scale(den, b), mul(add(scale(CX, d), scale(SX, c)), DY),
               mul(add(scale(CY, f), scale(SY, e)), DX))
    numerator = add(mul(real, real), scale(mul(imag, imag), 3), scale(mul(den, den), -4))
    quotient = divide_exact(numerator, scale(den, 4))
    need(mul(scale(den, 4), quotient) == numerator, 'distance identity')
    return primitive(quotient)


def trim(a):
    while a and a[-1] == 0:
        a.pop()
    return a


def ugcd(a, b, prime):
    a = trim([c % prime for c in a]); b = trim([c % prime for c in b])
    while b:
        r = a[:]; inv = pow(b[-1], -1, prime)
        while len(r) >= len(b):
            t = r[-1]*inv % prime; offset = len(r)-len(b)
            for i, c in enumerate(b):
                r[i+offset] = (r[i+offset]-t*c) % prime
            trim(r)
        a, b = b, r
    if a:
        inv = pow(a[-1], -1, prime)
        a = [c*inv % prime for c in a]
    return a


def degree(p):
    return max(i+j for (i, j), c in p.items() if c)


def modular_data(p, prime):
    q = {ij: c % prime for ij, c in p.items() if c % prime}
    if not q or degree(q) != degree(p):
        return None
    dy = max(j for i, j in q)
    content = []
    for j in range(dy+1):
        coeff = [q.get((i, j), 0) for i in range(3)]
        content = ugcd(content, coeff, prime)
    evaluations = []
    for a in range(17):
        row = [sum(c*pow(a, i, prime) for (i, k), c in q.items() if k == j) % prime
               for j in range(dy+1)]
        evaluations.append(row if row[-1] else None)
    return content, dy, evaluations


def witness(pdata, qdata, prime):
    if pdata is None or qdata is None:
        return None
    pc, pd, pe = pdata; qc, qd, qe = qdata
    if ugcd(pc, qc, prime) != [1]:
        return None
    if min(pd, qd) == 0:
        return -1
    for a, (p, q) in enumerate(zip(pe, qe)):
        if p is not None and q is not None and ugcd(p, q, prime) == [1]:
            return a
    return None


def audit_coprime(factors, active):
    # These primes are fixed protocol choices, checked by trial division.
    primes = (101, 103, 107)
    for p in primes:
        need(all(p % d for d in range(2, isqrt(p)+1)), 'prime modulus')
    data = {p: {i: modular_data(factors[i], p) for i in active} for p in primes}
    h = hashlib.sha256(); histogram = {}; total = 0
    for i, j in combinations(active, 2):
        found = False
        for p in primes:
            a = witness(data[p][i], data[p][j], p)
            if a is not None:
                histogram[str(p)] = histogram.get(str(p), 0)+1
                h.update(f'{i},{j},{p},{a}\n'.encode()); total += 1; found = True
                break
        need(found, f'no modular coprimality certificate for {i},{j}')
    return {'pairs_checked': total, 'prime_histogram': histogram, 'witness_stream_sha256': h.hexdigest()}


def controls():
    # A shared curve must be rejected, including after accidental specialization.
    x = {(1, 0): 1}; y = {(0, 1): 1}
    cases = [
        ('shared line', mul(add(x, y), add(x, scale(y, -1))), add(x, y), False),
        ('vertical versus primitive', x, add(mul(x, y), ONE), True),
        ('bad specialization at zero', add(x, y), add(x, scale(y, -1)), True),
        ('bad first prime', add(mul(x, x), mul(y, y)), add(mul(x, x), mul(y, y), scale(ONE, 101)), True),
    ]
    for name, p, q, expected in cases:
        actual = any(witness(modular_data(p, r), modular_data(q, r), r) is not None for r in (101, 103, 107))
        need(actual == expected, 'coprimality control: '+name)
    return [c[0] for c in cases]
