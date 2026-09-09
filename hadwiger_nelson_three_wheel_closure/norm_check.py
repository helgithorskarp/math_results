"""Independent unit test via a degree-one/two algebraic norm, not matrices."""
from fractions import Fraction as F
from math import isqrt
from arithmetic import need, trim, fp_gcd


class NormBlock:
    def __init__(self, r, h, prime):
        self.p = prime
        need(prime in (1009, 1013, 1019) and all(prime % k for k in range(2, isqrt(prime)+1)), 'prime norm modulus')
        def residue(c):
            c = F(c)
            need(c.denominator % prime, 'good norm reduction denominator')
            return c.numerator*pow(c.denominator, -1, prime) % prime
        self.r = tuple(residue(c) for c in r)
        need(self.r[-1] == 1 and h[-1] == (1,), 'monic norm relations')
        self.h = [self.red(tuple(residue(c) for c in a)) for a in h]
        need(len(h) in (2, 3), 'linear or quadratic y algebra')

    def red(self, a):
        a = list(trim([c % self.p for c in a]))
        while len(a) >= len(self.r):
            c = a[-1]; shift = len(a)-len(self.r)
            for j, v in enumerate(self.r):
                a[shift+j] = (a[shift+j]-c*v) % self.p
            a = list(trim(a))
        return tuple(a)

    def add(self, a, b, sign=1):
        return self.red([(a[i] if i < len(a) else 0)+sign*(b[i] if i < len(b) else 0)
                         for i in range(max(len(a), len(b)))])

    def mul(self, a, b):
        if not a or not b:
            return ()
        out = [0]*(len(a)+len(b)-1)
        for i, c in enumerate(a):
            for j, d in enumerate(b):
                out[i+j] += c*d
        return self.red(out)

    def unit(self, coefficients):
        C, B, A = [self.red([coefficients[3*i+j] for i in range(3)]) for j in range(3)]
        if len(self.h) == 2:
            # y=-h0; evaluate A*y^2+B*y+C by Horner's rule.
            root = tuple(-c for c in self.h[0])
            value = self.add(self.mul(self.add(self.mul(A, root), B), root), C)
        else:
            # h=y^2+u*y+v. Reduce the event to C'+B'*y, whose norm is
            # C'^2-u*B'*C'+v*B'^2 over Fp[x]/r, even with repeated roots.
            v, u = self.h[:2]
            C = self.add(C, self.mul(A, v), -1)
            B = self.add(B, self.mul(A, u), -1)
            value = self.add(self.add(self.mul(C, C), self.mul(u, self.mul(B, C)), -1),
                             self.mul(v, self.mul(B, B)))
        return fp_gcd(self.r, value, self.p) == (1,)
