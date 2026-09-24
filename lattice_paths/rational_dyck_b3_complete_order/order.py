#!/usr/bin/env python3
"""Arithmetic matching ranks and covers on D(a,3). See PROOF.md.

Ranks start at zero at the greatest matching score. No score is evaluated.
Only Python's standard library and arbitrary-precision integers are used.
"""

from math import comb, isqrt


def endpoint(a):
    if type(a) is not int or a <= 3 or a % 3 == 0:
        raise ValueError("a must be an integer >3 coprime to 3")
    return divmod(a, 3)


def total(a):
    endpoint(a)
    return (a + 1) * (a + 2) // 6


def validate(runs):
    if not isinstance(runs, (tuple, list)) or len(runs) != 3:
        raise ValueError("a run triple is required")
    if any(type(x) is not int or x < 0 for x in runs):
        raise ValueError("run lengths must be nonnegative integers")
    r, s, t = runs
    a = r + s + t
    endpoint(a)
    if 3 * r < a or 3 * (r + s) < 2 * a:
        raise ValueError("run triple is not rational-Dyck")
    return a


def layer_start(a, z):
    return z * a - 3 * z * (z - 1) // 2


def rank(runs):
    """Descending matching rank, including all equal-run boundaries."""
    a = validate(runs)
    m, _ = endpoint(a)
    x, y, z = sorted(runs, reverse=True)
    runs = tuple(runs)
    if y == z:
        local = 0
    elif y <= m:
        local = y - z if runs == (x, z, y) else m + y - 2 * z
    elif x == y or runs == (y, x, z):
        local = 2 * (y - z) - 1
    else:
        local = 2 * (y - z)
    return layer_start(a, z) + local


def unrank(a, index):
    """Inverse of rank, using one integer square root and bounded correction."""
    m, _ = endpoint(a)
    if type(index) is not int or not 0 <= index < total(a):
        raise ValueError("rank outside the carrier")
    discriminant = (2 * a + 3) ** 2 - 24 * index
    z = min(m, (2 * a + 3 - isqrt(discriminant)) // 6)
    # Rounding the square root can cross an integer boundary by at most one.
    if layer_start(a, z) > index:
        z -= 1
    if z < m and layer_start(a, z + 1) <= index:
        z += 1
    q = index - layer_start(a, z)
    n = m - z
    if q == 0:
        return a - 2 * z, z, z
    if q <= n:
        y = z + q
        return a - y - z, z, y
    if q <= 2 * n:
        y = z + q - n
        return a - y - z, y, z
    y = z + (q + 1) // 2
    x = a - y - z
    return (y, x, z) if q % 2 else (x, y, z)


def chain(a):
    """Yield every path in strictly decreasing matching order."""
    m, _ = endpoint(a)
    for z in range(m + 1):
        yield a - 2 * z, z, z
        for y in range(z + 1, m + 1):
            yield a - y - z, z, y
        for y in range(z + 1, m + 1):
            yield a - y - z, y, z
        for y in range(m + 1, (a - z) // 2 + 1):
            x = a - y - z
            yield y, x, z
            if x != y:
                yield x, y, z


def covers(lower, upper):
    """True exactly when lower <_M upper is a cover."""
    if validate(lower) != validate(upper):
        raise ValueError("cover endpoints must have the same a")
    return rank(lower) == rank(upper) + 1


def lagrange_rank(runs):
    """Descending rank of the Lagrange SCORE LEVEL, not of an individual path.

    Uses the prior height-three Lagrange classification; see SOURCES.md.
    """
    a = validate(runs)
    _, y, z = sorted(runs, reverse=True)
    previous = a * a // 4 - (a - z) ** 2 // 4 - z * (z - 1) // 2 + z
    return previous + y - z


def statistics(a):
    m, epsilon = endpoint(a)
    size = total(a)
    floor_term = (m + epsilon - 1) ** 2 // 4
    tied_covers = 1 + floor_term
    return {
        "paths": size,
        "matching_levels": size,
        "lagrange_levels": size - m * (m + 1) // 2 - floor_term,
        "matching_covers": size - 1,
        "common_oriented_covers": size - tied_covers - m,
        "lagrange_tied_matching_covers": tied_covers,
        "oppositely_oriented_common_covers": int(m >= 2),
        "nonlocal_matching_covers": max(m - 2, 0),
        "max_lagrange_fibre_distance": max(m - 1, 1),
        "discordant_unequal_fibre_pairs": comb(m + 1, 3),
    }


if __name__ == "__main__":
    import argparse
    import json

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("a", type=int)
    parser.add_argument("--rank", nargs=3, type=int, metavar=("R", "S", "T"))
    parser.add_argument("--unrank", type=int)
    args = parser.parse_args()
    endpoint(args.a)
    if args.rank is not None:
        if validate(args.rank) != args.a:
            parser.error("run sum differs from a")
        print(rank(args.rank))
    elif args.unrank is not None:
        print(*unrank(args.a, args.unrank))
    else:
        print(json.dumps(statistics(args.a), sort_keys=True, indent=2))
