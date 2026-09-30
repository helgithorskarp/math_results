"""Explicit classical 68-circle design; standard-library exact arithmetic."""
from collections import Counter
from itertools import combinations


def require(condition, message):
    if not condition:
        raise ValueError(message)


def mul(a, b):
    """GF(16) bit basis, modulus z^4+z+1 (integer19)."""
    out = 0
    while b:
        if b & 1:
            out ^= a
        b >>= 1
        a <<= 1
        if a & 16:
            a ^= 19
    return out


def power(a, n):
    out = 1
    while n:
        if n & 1:
            out = mul(out, a)
        a = mul(a, a)
        n >>= 1
    return out


def points(mask):
    return tuple(p for p in range(17) if mask >> p & 1)


def mask(pts):
    return sum(1 << p for p in pts)


def move(word, permutation):
    return mask(permutation[p] for p in points(word))


def generators():
    translation = tuple(p ^ 1 for p in range(16)) + (16,)
    primitive = tuple(mul(2, p) for p in range(16)) + (16,)
    subfield = tuple(mul(6, p) for p in range(16)) + (16,)
    inversion = (16,) + tuple(power(p, 14) for p in range(1, 16)) + (0,)
    frobenius = tuple(mul(p, p) for p in range(16)) + (16,)
    return (translation, primitive, inversion), (translation, subfield, inversion, frobenius)


def classical_design():
    global_gens, gap_gens = generators()
    require(all(sorted(g) == list(range(17)) for g in global_gens + gap_gens),
            'a generator is not a permutation')
    require(all(mul(p, power(p, 14)) == 1 for p in range(1, 16)),
            'incorrect field inversion')
    line = tuple(p for p in range(16) if power(p, 4) == p) + (16,)
    require(line == (0, 1, 6, 7, 16), 'incorrect subfield line')
    gap = mask(line)
    circles = [gap]
    seen = {gap}
    for c in circles:
        for g in global_gens:
            image = move(c, g)
            if image not in seen:
                seen.add(image)
                circles.append(image)
    circles.sort()
    require(len(circles) == 68 and all(c.bit_count() == 5 for c in circles),
            'incorrect circle orbit')
    require(all((c & d).bit_count() <= 2 for c, d in combinations(circles, 2)),
            'design circles have a repeated triple')
    incidence = Counter(mask(t) for c in circles for t in combinations(points(c), 3))
    require(len(incidence) == 680 and set(incidence.values()) == {1},
            'circles do not cover every old triple exactly once')
    for g in global_gens + gap_gens:
        require({move(c, g) for c in circles} == seen, 'generator does not preserve design')
    require(all(move(gap, g) == gap for g in gap_gens), 'gap generator moves the gap')
    return tuple(circles), gap
