"""Set partitions and triangular span inversion, separate from counts.py."""
from functools import lru_cache
from math import comb, factorial, prod


@lru_cache(None)
def partitions(m, k, cap):
    if m == 0:
        return int(k == 0)
    if k <= 0 or m < k or m > k*cap:
        return 0
    return sum(comb(m-1, t-1)*partitions(m-t, k-1, cap)
               for t in range(1, min(m, cap)+1))


@lru_cache(None)
def words(m, letters, cap):
    return sum(partitions(m, k, cap)*factorial(letters)//factorial(letters-k)
               for k in range(min(m, letters)+1))


@lru_cache(None)
def subspaces(r, k):
    if k == 0 or k == r:
        return 1
    if k < 0 or k > r:
        return 0
    return subspaces(r-1, k-1) + 2**k*subspaces(r-1, k)


@lru_cache(None)
def spanning(m, r, cap):
    return words(m, 2**r-1, cap) - sum(subspaces(r, k)*spanning(m, k, cap) for k in range(r))


@lru_cache(None)
def affine(m, d, cap):
    return words(m, 2**d, cap) - sum(2**(d-k)*subspaces(d, k)*affine(m, k, cap) for k in range(d))


def stage(m, n, r, acap, bcap, azero, bzero):
    z = 0
    for a in range(azero+1):
        for b in range(bzero+1):
            if a and b:
                continue
            z += comb(m, a)*comb(n, b)*spanning(m-a, r, acap)*spanning(n-b, r, bcap)
    low = (2**r-1)*2**(r-1)*affine(m, r-1, acap)*affine(n, r-1, bcap)
    gl = prod(2**r-2**i for i in range(r))
    if z % gl or low % gl:
        raise ArithmeticError("bad quotient")
    return z//gl, low//gl
