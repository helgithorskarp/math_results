"""Exact rational closed entries for the complement-plus-disjoint-pairs family.

Actual author: six-downset-3, researcher. The all-real reduction is in PROOF.md.
This module constructs rational instances; positivity is a verifier obligation.
"""
from fractions import Fraction as Q
from math import comb
import re


def require(condition, message):
    if not condition:
        raise ValueError(message)


def rational(value):
    if isinstance(value, Q):
        return value
    if type(value) is int:
        return Q(value)
    require(type(value) is str and re.fullmatch(r'-?\d+(?:/[1-9]\d*)?', value),
            'coefficient must be an integer or exact rational string')
    return Q(value)


def parameters(n, z, epsilon):
    require(type(n) is int and n >= 6, 'integer n>=6 required')
    require(type(z) is dict, 'complement weights must be a mapping')
    converted = {}
    for key, value in z.items():
        require(type(key) is int or (type(key) is str and key.isdigit()), 'invalid layer key')
        k = int(key)
        require(k not in converted, 'duplicate layer key')
        converted[k] = rational(value)
    require(set(converted) == set(range(2, n//2+1)), 'incomplete or excessive layer coverage')
    return {k: converted[min(k, n-k)] for k in range(2, n-1)}, rational(epsilon)


def construct(n, z, epsilon):
    """Return canonical vertices and L=(N-s)M+sI, without presuming PSD."""
    z, epsilon = parameters(n, z, epsilon)
    N, s = 2**n-n-1, 2**(n-1)-n
    full = (1 << n)-1
    members = [a for a in range(1 << n) if a.bit_count() <= n-2]
    singleton_pair = s-sum(comb(n-2, k-1)*z[k] for k in z)+(n-2)*(n-3)*epsilon
    empty_singleton = (N-n*s+sum((k-1)*comb(n-1, k)*z[k] for k in z)
                       -Q((n-1)*(n-2)*(n-3), 2)*epsilon)
    empty_middle = {k: N-2*s-(n-k-1)*z[k]
                       +(comb(n-2, 2)*epsilon if k == 2 else 0) for k in z}
    empty_diagonal = N-n*empty_singleton-sum(comb(n, k)*empty_middle[k] for k in z)
    matrix = []
    for a in members:
        row = []
        for b in members:
            ka, kb = a.bit_count(), b.bit_count()
            if a == b:
                value = empty_diagonal if a == 0 else Q(s)
            elif not a or not b:
                k = max(ka, kb)
                value = empty_singleton if k == 1 else empty_middle[k]
            elif a & b:
                value = Q(0)
            elif ka == kb == 1:
                value = singleton_pair
            elif min(ka, kb) == 1:
                k = max(ka, kb)
                value = z[k]-((n-3)*epsilon if k == 2 else 0)
            elif a | b == full:
                value = s-z[ka]
            elif ka == kb == 2:
                value = epsilon
            else:
                value = Q(0)
            row.append(value)
        matrix.append(row)
    return members, matrix
