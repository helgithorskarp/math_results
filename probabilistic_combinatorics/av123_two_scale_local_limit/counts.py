"""Exact counts from the prior two-corner formula; Python standard library."""

from math import comb


def choose(n, k):
    return comb(n, k) if n >= 0 and 0 <= k <= n else 0


def catalan(n):
    if n < 0:
        raise ValueError("negative size")
    return comb(2*n, n) // (n+1)


def ballot(length, height):
    if not 0 <= height <= length or (length-height) % 2:
        return 0
    j = (length-height)//2
    return choose(length, j) - choose(length, j-1)


def joint_count(n, d, x, y):
    """Number with distance d and the middle-strip subset sizes x,y."""
    if n < 2 or not 1 <= d <= n//2:
        return 0
    m, length = d-1, n-d-1
    if not (0 <= x <= m and 0 <= y <= m):
        return 0
    return (comb(m, x)*comb(m, y)*ballot(length, x+y)
            *ballot(length, 2*m-x-y))


def position_excedance_count(n, d, a, e):
    """Literal fixed positions a,a+d and the number e of excedances."""
    if not 1 <= a < a+d <= n:
        return 0
    m, length = d-1, n-d-1
    h, k = 2*a+d-n-1, 2*e-n+2
    if (m+k+h) % 2 or (m+k-h) % 2:
        return 0
    x, y = (m+k+h)//2, (m+k-h)//2
    return joint_count(n, d, x, y)


def distance_terms(n, d):
    """(s, binomial multiplicity, ballot product), including zero weights."""
    if n < 2 or not 1 <= d <= n//2:
        return []
    m, length = d-1, n-d-1
    return [(s, comb(2*m, s), ballot(length, s)*ballot(length, 2*m-s))
            for s in range(length % 2, 2*m+1, 2)]


def distance_count(n, d):
    return sum(b*g for _, b, g in distance_terms(n, d))


def two_fixed_count(n):
    return sum(distance_count(n, d) for d in range(1, n//2+1))
