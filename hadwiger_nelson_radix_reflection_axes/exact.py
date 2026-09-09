"""Small exact polynomial checker routines; coefficients are low degree first."""
from fractions import Fraction
from math import isqrt
import hashlib
import json

PRIMES = (1000003, 1000033, 1000037, 1000039)
WEIGHTS = ((1,0,0,0,0), (1,0,0,0,1), (1,0,0,1,0), (1,0,0,1,1))


def need(condition, message):
    if not condition:
        raise ValueError(message)


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def trim(a):
    a = list(a)
    while a and a[-1] == 0:
        a.pop()
    return a


def add(a, b, scale=1):
    c = list(a) + [0] * max(0, len(b)-len(a))
    for i, x in enumerate(b):
        c[i] += scale*x
    return trim(c)


def mul(a, b):
    c = [0] * max(0, len(a)+len(b)-1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            c[i+j] += x*y
    return trim(c)


def rem(a, b, prime=None):
    a, b = trim(a), trim(b)
    need(b, 'polynomial division by zero')
    if prime is not None:
        a, b = trim([x % prime for x in a]), trim([x % prime for x in b])
        inverse = pow(b[-1], -1, prime)
    while a and len(a) >= len(b):
        scale = a[-1] * inverse % prime if prime else Fraction(a[-1]) / Fraction(b[-1])
        offset = len(a)-len(b)
        for i, x in enumerate(b):
            a[offset+i] -= scale*x
            if prime:
                a[offset+i] %= prime
        a = trim(a)
    return a


def gcd_is_one(a, b, prime):
    a, b = trim([x % prime for x in a]), trim([x % prime for x in b])
    while len(b) > 1:
        a, b = b, rem(a, b, prime)
    return len(b) == 1 or (not b and len(a) == 1)


def derivative(a):
    return [i*a[i] for i in range(1, len(a))]


def is_prime(p):
    return p >= 2 and all(p % d for d in range(2, isqrt(p)+1))


def root_count(poly, left=None, right=None):
    chain = [list(map(Fraction, poly)), list(map(Fraction, derivative(poly)))]
    while chain[-1]:
        r = rem(chain[-2], chain[-1])
        if not r:
            break
        r = [-x for x in r]
        scale = abs(r[-1])
        chain.append([x/scale for x in r])
    def variations(value, positive_infinity):
        signs = []
        for q in chain:
            if value is None:
                sign = 1 if q[-1] > 0 else -1
                if not positive_infinity and (len(q)-1) % 2:
                    sign = -sign
            else:
                v = Fraction(0)
                for x in reversed(q):
                    v = v*value+x
                if not v:
                    continue
                sign = 1 if v > 0 else -1
            signs.append(sign)
        return sum(a != b for a, b in zip(signs, signs[1:]))
    return variations(left, False)-variations(right, True)


def power_mod(a, exponent, modulus, prime):
    result = [1]
    while exponent:
        if exponent & 1:
            result = rem(mul(result, a), modulus, prime)
        exponent //= 2
        a = rem(mul(a, a), modulus, prime)
    return result


def irreducible_degree_seven_mod_five(poly):
    need(len(poly) == 8 and poly[-1] % 5 == 1, 'degree-seven monic polynomial')
    x = [0, 1]
    need(gcd_is_one(poly, add(power_mod(x, 5, poly, 5), x, -1), 5), 'no degree-one factor modulo five')
    value = x
    for _ in range(7):
        value = power_mod(value, 5, poly, 5)
    need(trim(value) == x, 'degree-seven Frobenius criterion')
