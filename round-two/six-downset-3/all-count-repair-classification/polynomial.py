"""Dense exact polynomials over QQ[k]; no CAS, solver, or floating arithmetic."""
from fractions import Fraction as F
from math import comb


def clean(a):
    a = list(map(F, a))
    while a and not a[-1]:
        a.pop()
    return tuple(a)


def constant(x):
    return clean((x,))


K = clean((0, 1))
ONE = constant(1)


def add(*terms):
    out = [F(0)] * max(map(len, terms), default=0)
    for term in terms:
        for i, value in enumerate(term):
            out[i] += value
    return clean(out)


def scale(a, b):
    return clean([x * b for x in a])


def mul(*terms):
    out = ONE
    for b in terms:
        c = [F(0)] * max(0, len(out) + len(b) - 1)
        for i, x in enumerate(out):
            for j, y in enumerate(b):
                c[i+j] += x * y
        out = clean(c)
    return out


def divide(a, b):
    if not b:
        raise ValueError('zero polynomial divisor')
    rest = list(a)
    quotient = [F(0)] * max(0, len(a)-len(b)+1)
    while rest:
        i = len(rest)-len(b)
        if i < 0:
            raise ValueError('nonzero exact polynomial remainder')
        x = rest[-1]/b[-1]
        quotient[i] += x
        for j, y in enumerate(b):
            rest[i+j] -= x*y
        rest = list(clean(rest))
    out = clean(quotient)
    if mul(out, b) != a:
        raise ValueError('complete polynomial division multiply-back')
    return out


def choose(a, size):
    if size == 0:
        return ONE
    if size == 1:
        return a
    if size == 2:
        return scale(mul(a, add(a, constant(-1))), F(1, 2))
    raise ValueError('original orbit sizes are at most two')


def evaluate(a, k):
    out = F(0)
    for value in reversed(a):
        out = out*k + value
    return out


def shift(a, at):
    return clean([sum(a[j]*comb(j, i)*at**(j-i) for j in range(i, len(a)))
                  for i in range(len(a))])


def record(a):
    return [str(x) for x in a]
