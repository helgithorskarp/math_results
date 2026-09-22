"""Construct finite color-forcing certificates; no verification code is imported."""
from collections import Counter


def threshold(k, ell):
    return k * k + ((ell + 1) * (ell - 2) // 2 + 2) * k + ell * (ell - 2)


def step(*groups):
    """Each group is an iterable of (value, multiplicity) pairs."""
    c = Counter()
    for group in groups:
        for x, multiplicity in group:
            c[x] += multiplicity
    # Zero extra copies are permitted; negative counts remain for the auditor.
    return sorted((x, multiplicity) for x, multiplicity in c.items() if multiplicity)


def once(values):
    return [(x, 1) for x in values]


def certificate(k, ell, blue):
    """blue is the minority color in [1,2*ell-1]; colors are otherwise free.

    Yield sums. In a coloring avoiding the target, each sum forces the opposite
    color at its result. The independent auditor checks all arithmetic and stops
    at the first contradiction (which can be before this sequence ends).
    """
    if ell < 3 or k < 2 * ell + 1:
        raise ValueError('outside the proved parameter range')
    B = sorted(blue)
    if len(B) >= ell or len(set(B)) != len(B) or any(x < 1 or x >= 2 * ell for x in B):
        raise ValueError('invalid minority prefix')
    R = [x for x in range(1, 2 * ell) if x not in set(B)][:ell]
    u = k - ell
    if R == list(range(1, ell + 1)):
        T = k + (ell + 1) * (ell - 2) // 2
        for j in range(2 * ell - 1):
            e = min(j, ell - 1)
            f = j - e
            yield step(once(R), [(1, u - 2), (1 + e, 1), (1 + f, 1)])
        A = (k + 1) * T + 1
        yield step(once(range(T + 1, T + ell + 1)), [(T + 1, u)])
        shifts = [1, 4, 4] if ell == 3 else [1, 4, 4] + list(range(7, 2 * ell, 2))
        yield step(once(T + s for s in shifts), [(T + 2, u)])
        yield step(once(range(1, ell)), [(A, 1), (1, u)])
        return
    if R == list(range(1, 2 * ell, 2)):
        A = k + ell * ell - ell
        C = 3 * k + 2 * ell * ell - 4 * ell
        D = 4 * k + 3 * ell * ell - 7 * ell + 1
        yield step(once(R), [(1, u)])
        yield step(once(range(2, 2 * ell, 2)), [(A, 1), (2, u)])
        yield step(once(range(1, 2 * ell - 2, 2)), [(C, 1), (1, u)])
        yield step(once(range(2, 2 * ell, 2)), [(D, 1), (2, u)])
        yield step([(x, 2) for x in range(3, 2 * ell, 2)], [(C, 1), (3, k - 2 * ell + 1)])
        return
    if R == [1, 4, 5]:
        c = next(c for c in (1, 2, 3) if (c - 2 * k) % 3 == 0)
        b = (2 * k + 6 - 4 * c) // 3
        a = (k - 6 + c) // 3
        yield [(1, k - 2), (4, 1), (5, 1)]
        yield [(2, k - 2), (3, 1), (k + 7, 1)]
        yield [(1, a), (4, b), (5, c)]
        return
    if R == [1, 3, 4]:
        for a, b, c in [(k - 2, 1, 1), (k - 3, 2, 1), (k - 4, 3, 1), (k - 4, 2, 2)]:
            yield [(1, a), (3, b), (4, c)]
        yield [(2, k - 2), (k + 5, 1), (k + 7, 1)]
        yield [(2, k - 2), (k + 9, 1), (k + 10, 1)]
        yield [(1, k - 2), (3, 1), (4 * k + 8, 1)]
        yield [(3, 1), (4, k - 2), (4 * k + 15, 1)]
        yield [(2, k - 2), (k + 5, 1), (5 * k + 9, 1)]
        return
    a = next(R[i] for i in range(ell - 1) if R[i + 1] == R[i] + 1)
    v = min(B)
    q = ell - len(B)
    S = sum(R) + u * a
    for t in range(q):
        yield step(once(R), [(a, u - t), (a + 1, t)])
    V = sum(B) + q * S + q * (q - 1) // 2 + u * v
    yield step(once(B), once(range(S, S + q)), [(v, u)])
    yield step(once(B), once(range(S, S + q)), [(v, u - 1), (S, 1)])
    r = next(r for r in R if r > v and r not in (a, a + 1))
    t = r - v
    yield step(once(r0 for r0 in R if r0 != r), [(a, u - t), (a + 1, t), (V, 1)])
