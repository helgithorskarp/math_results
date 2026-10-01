"""Classical GF16 sublines: independently regenerated prior-art baseline.

The68-block Steiner construction is prior art. Its regeneration is
baseline validation; no new unrestricted lower bound is asserted.
"""
from itertools import combinations
from collections import Counter
import json
import model as M


def multiply16(a, b):
    result = 0
    while b:
        if b & 1:
            result ^= a
        b >>= 1
        a <<= 1
        if a & 16:
            a ^= 19  # X^4+X+1.
    return result


def power16(a, n):
    result = 1
    while n:
        if n & 1:
            result = multiply16(result, a)
        a = multiply16(a, a)
        n >>= 1
    return result


def code():
    inverse = {a: power16(a, 14) for a in range(1, 16)}
    M.require(all(multiply16(a, inverse[a]) == 1 for a in inverse), 'GF16 inverse table')
    subfield = (0, 1, 6, 7)
    M.require(set(subfield) == {a for a in range(16) if power16(a, 4) == a}, 'GF4 subfield')
    coordinates = {subfield[x] ^ multiply16(subfield[y], 2): 4 * y + x
                   for x in range(4) for y in range(4)}
    M.require(len(coordinates) == 16, 'GF4 coordinate basis')
    base = (16,) + subfield
    blocks = set()
    for a in range(1, 16):
        for b in range(16):
            blocks.add(M.mask((16,) + tuple(coordinates[multiply16(a, z) ^ b] for z in subfield)))
    transformations = 240
    for a in range(16):
        for b in range(16):
            for d in range(16):
                if multiply16(a, d) == b:
                    continue
                image = [coordinates[a]]  # Image of infinity under (az+b)/(z+d).
                for z in subfield:
                    if z == d:
                        image.append(16)
                    else:
                        image.append(coordinates[multiply16(multiply16(a, z) ^ b, inverse[z ^ d])])
                blocks.add(M.mask(image))
                transformations += 1
    S = tuple(sorted(blocks))
    M.require(transformations == 4080 and len(S) == 68, 'subline orbit size')
    verify(S)
    M.require(set(M.affine_star()) <= set(S), 'derived AG(2,4) star')
    return S


def verify(S):
    M.check_code(S)
    M.require(len(S) == 68 and all(not w >> 17 & 1 for w in S), 'Steiner block domain')
    covered = Counter(t for w in S for t in M.triples(w))
    universe = {M.mask(t) for t in combinations(range(17), 3)}
    M.require(set(covered) == universe and set(covered.values()) == {1}, 'Steiner exact triple coverage')
