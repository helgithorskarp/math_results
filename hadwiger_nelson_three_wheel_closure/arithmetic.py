"""Small exact elimination/quotient kernel. No CAS, solver or floats."""
from fractions import Fraction as F
from itertools import permutations
from math import gcd, lcm, isqrt
from functools import reduce


def need(ok, message):
    if not ok:
        raise ValueError(message)


def trim(a):
    a = list(a)
    while a and a[-1] == 0:
        a.pop()
    return tuple(a)


def add(a, b):
    return trim([(a[i] if i < len(a) else 0)+(b[i] if i < len(b) else 0)
                 for i in range(max(len(a), len(b)))])


def scale(a, c):
    return trim([x*c for x in a])


def mul(a, b):
    if not a or not b:
        return ()
    out = [0]*(len(a)+len(b)-1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i+j] += x*y
    return trim(out)


def divmod_q(a, b):
    need(b, 'division by zero polynomial')
    a = list(trim(a)); q = [F(0)]*max(0, len(a)-len(b)+1)
    while len(a) >= len(b):
        k = len(a)-len(b); c = F(a[-1])/b[-1]; q[k] += c
        for j, v in enumerate(b):
            a[k+j] -= c*v
        a = list(trim(a))
    return trim(q), tuple(a)


def gcd_q(a, b):
    while b:
        a, b = b, divmod_q(a, b)[1]
    return scale(a, F(1)/a[-1]) if a else ()


def primitive(a):
    need(a, 'zero elimination polynomial')
    den = reduce(lcm, (F(c).denominator for c in a), 1)
    nums = [int(c*den) for c in a]
    g = reduce(gcd, nums, 0)
    if nums[-1] < 0:
        g = -g
    return tuple(c//g for c in nums)


def ycoeffs(vector):
    need(len(vector) == 9, 'source coefficient order')
    return trim([trim(vector[3*i+j] for i in range(3)) for j in range(3)])


def trim_y(a):
    a = list(a)
    while a and not a[-1]:
        a.pop()
    return tuple(a)


def resultant_y(f, g):
    """Sylvester determinant in Z[x], degree in y at most two here."""
    f, g = trim_y(ycoeffs(f)), trim_y(ycoeffs(g))
    need(f and g, 'nonzero source factors')
    m, n = len(f)-1, len(g)-1
    if m == n == 0:
        need(gcd_q(f[0], g[0]) == (1,), 'univariate source factors coprime')
        return (1,)
    size = m+n; matrix = []
    for z, copies in ((f, n), (g, m)):
        for k in range(copies):
            row = [()] * size
            row[k:k+len(z)] = reversed(z)
            matrix.append(row)
    out = ()
    for perm in permutations(range(size)):
        sign = (-1)**sum(perm[i] > perm[j] for i in range(size) for j in range(i+1, size))
        term = (sign,)
        for i, j in enumerate(perm):
            term = mul(term, matrix[i][j])
        out = add(out, term)
    need(out, 'coprime finite input has nonzero resultant')
    return primitive(out)


class Quotient:
    """Q[x]/(r). We verify each inversion; irreducibility is not assumed."""
    def __init__(self, r):
        self.r = scale(tuple(map(F, r)), F(1)/r[-1])
        self.n = len(r)-1
        need(self.n > 0, 'nonconstant projection factor')
        self.inverses = {}

    def red(self, a):
        return divmod_q(a, self.r)[1]

    def times(self, a, b):
        return self.red(mul(a, b))

    def inverse(self, a):
        a = self.red(a)
        if a in self.inverses:
            return self.inverses[a]
        need(a, 'nonunit zero coefficient')
        old, cur = self.r, a
        u, v = (), (F(1),)
        while cur:
            q, rem = divmod_q(old, cur)
            old, cur = cur, rem
            u, v = v, add(u, scale(mul(q, v), -1))
        need(len(old) == 1, 'noninvertible leading coefficient in quotient')
        answer = self.red(scale(u, F(1)/old[0]))
        need(self.times(a, answer) == (1,), 'checked quotient inverse')
        self.inverses[a] = answer
        return answer

    def y_monic(self, a):
        a = trim_y(a)
        return tuple(self.times(c, self.inverse(a[-1])) for c in a) if a else ()

    def y_rem(self, a, b):
        need(b, 'nonzero y divisor')
        a = list(a); inv = self.inverse(b[-1])
        while len(a) >= len(b):
            k = len(a)-len(b); c = self.times(a[-1], inv)
            for j, v in enumerate(b):
                a[k+j] = add(a[k+j], scale(self.times(c, v), -1))
            a = list(trim_y(a))
        return tuple(a)

    def y_gcd(self, f, g):
        f = trim_y([self.red(a) for a in ycoeffs(f)])
        g = trim_y([self.red(a) for a in ycoeffs(g)])
        # Every remainder is a combination of its two predecessors modulo r.
        while g:
            f, g = g, self.y_rem(f, g)
        need(f, 'unexpected vertical common component')
        return self.y_monic(f)

    def y_mul(self, a, b):
        out = [()] * (len(a)+len(b)-1)
        for i, x in enumerate(a):
            for j, y in enumerate(b):
                out[i+j] = add(out[i+j], self.times(x, y))
        return trim_y(out)


def encode_h(h):
    return [[str(c) for c in a] for a in h]


def decode_h(h):
    return tuple(trim(tuple(F(c) for c in a)) for a in h)


def fp_gcd(a, b, p):
    a, b = trim([c % p for c in a]), trim([c % p for c in b])
    while b:
        r = list(a); inv = pow(b[-1], -1, p)
        while len(r) >= len(b):
            c = r[-1]*inv % p; k = len(r)-len(b)
            for j, v in enumerate(b):
                r[k+j] = (r[k+j]-c*v) % p
            r = list(trim(r))
        a, b = b, tuple(r)
    return tuple(c*pow(a[-1], -1, p) % p for c in a) if a else ()


class ModBlock:
    """Finite free quotient with basis x^i*y^j, i<deg r,j<deg_y h."""
    def __init__(self, r, h, prime):
        self.p = prime
        need(prime in (1009, 1013, 1019), 'declared prime')
        need(all(prime % k for k in range(2, isqrt(prime)+1)), 'prime modulus')
        def residue(c):
            c = F(c)
            need(c.denominator % prime != 0, 'good reduction denominator')
            return c.numerator*pow(c.denominator, -1, prime) % prime
        self.r = [residue(c) for c in r]
        self.n = len(r)-1; self.d = len(h)-1; self.N = self.n*self.d
        need(self.r[-1] == 1 and h[-1] == (1,), 'monic quotient relations')
        self.h = {(i, j): residue(c) for j, a in enumerate(h) for i, c in enumerate(a) if c}
        self.mons = [(i, j) for j in range(self.d) for i in range(self.n)]
        self.nine = [self.reduce({(i, j): 1}) for i in range(3) for j in range(3)]
        self.products = None
        if self.d > 1:
            self.products = [[self.reduce({(i+a, j+b): 1}) for a, b in self.mons]
                             for i in range(3) for j in range(3)]

    def reduce(self, z):
        p, n, d = self.p, self.n, self.d
        z = {ij: c % p for ij, c in z.items() if c % p}
        while any(j >= d for i, j in z):
            i, j = max(z, key=lambda ij: (ij[1], ij[0])); c = z.pop((i, j))
            for (a, b), v in self.h.items():
                if (a, b) == (0, d):
                    continue
                ij = i+a, j-d+b
                z[ij] = (z.get(ij, 0)-c*v) % p
                if not z[ij]:
                    del z[ij]
        while z and max(i for i, j in z) >= n:
            i, j = max(z); c = z.pop((i, j))
            for a, v in enumerate(self.r[:-1]):
                ij = i-n+a, j
                z[ij] = (z.get(ij, 0)-c*v) % p
                if not z[ij]:
                    del z[ij]
        return [z.get(ij, 0) for ij in self.mons]

    def unit(self, coefficients):
        p, N = self.p, self.N
        if self.d == 1:
            value = [sum(c*v[k] for c, v in zip(coefficients, self.nine)) % p for k in range(N)]
            return fp_gcd(self.r, value, p) == (1,)
        M = [[sum(c*T[j][i] for c, T in zip(coefficients, self.products)) % p
              for j in range(N)] for i in range(N)]
        for i in range(N):
            pivot = next((j for j in range(i, N) if M[j][i]), None)
            if pivot is None:
                return False
            M[i], M[pivot] = M[pivot], M[i]
            inv = pow(M[i][i], -1, p)
            for j in range(i+1, N):
                a = M[j][i]*inv % p
                if a:
                    for k in range(i+1, N):
                        M[j][k] = (M[j][k]-a*M[i][k]) % p
        return True
