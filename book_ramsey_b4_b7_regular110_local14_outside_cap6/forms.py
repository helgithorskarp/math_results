"""Exact helpers copied from six-books-3's d00a13612475ea701786203b280200c11a105106.
The original helper was attributed there to source5ac6c693382a19253fa867f91d74f112e015a3a1.
Only weighted slack enumeration and exact integer-form recovery are reused.
"""
from fractions import Fraction
from math import gcd,lcm

def need(ok, message):
    if not ok:
        raise RuntimeError(message)

def weighted_stars(degrees, capacities):
    """Decide a vertex's entire remaining star before processing the next."""
    remaining = list(degrees)
    edges = []

    def visit():
        i = next((i for i, d in enumerate(remaining) if d), None)
        if i is None:
            yield tuple(edges)
            return
        amount = remaining[i]
        neighbors = [j for j in range(i + 1, len(degrees))
                     if remaining[j] and capacities[i][j] > 0]
        if sum(min(remaining[j], capacities[i][j]) for j in neighbors) < amount:
            return
        remaining[i] = 0

        def distribute(k, left):
            if k == len(neighbors):
                if left == 0:
                    yield from visit()
                return
            j = neighbors[k]
            future = sum(min(remaining[v], capacities[i][v]) for v in neighbors[k + 1:])
            for weight in range(max(0, left - future), min(left, remaining[j], capacities[i][j]) + 1):
                remaining[j] -= weight
                if weight:
                    edges.append((i, j, weight))
                yield from distribute(k + 1, left - weight)
                if weight:
                    edges.pop()
                remaining[j] += weight
        yield from distribute(0, amount)
        remaining[i] = amount
    yield from visit()

def primitive(vector):
    scale = lcm(*(x.denominator for x in vector))
    out = [int(x * scale) for x in vector]
    divisor = gcd(*out)
    need(divisor > 0, 'zero vector')
    out = [x // divisor for x in out]
    if next(x for x in out if x) < 0:
        out = [-x for x in out]
    return out

def quadratic(a, vector):
    return sum(a[i][j] * vector[i] * vector[j]
               for i in range(len(a)) for j in range(len(a)))

def negative_vector(original):
    n = len(original)
    a = [[Fraction(x) for x in row] for row in original]
    columns = [[Fraction(i == j) for i in range(n)] for j in range(n)]
    for k in range(n):
        pivot = a[k][k]
        if pivot < 0:
            out = primitive(columns[k])
            need(quadratic(original, out) < 0, 'invalid negative pivot witness')
            return out
        if pivot == 0:
            j = next((j for j in range(k + 1, n) if a[k][j]), None)
            if j is not None:
                cross = a[k][j]
                multiple = -(1 if cross > 0 else -1) * (int(abs(a[j][j]) / (2 * abs(cross))) + 1)
                out = primitive([multiple * x + y for x, y in zip(columns[k], columns[j])])
                need(quadratic(original, out) < 0, 'invalid zero pivot witness')
                return out
            continue
        multipliers = {j: a[k][j] / pivot for j in range(k + 1, n)}
        for j, multiplier in multipliers.items():
            columns[j] = [x - multiplier * y for x, y in zip(columns[j], columns[k])]
        for i in range(k + 1, n):
            for j in range(i, n):
                a[i][j] -= a[k][i] * multipliers[j]
                a[j][i] = a[i][j]
    raise RuntimeError('unexpected positive semidefinite survivor')
