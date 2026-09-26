#!/usr/bin/env python3
"""Exact relative-divisor-complex Betti numbers. Python >= 3.11, stdlib only.

Faces are integer masks, vertex 0 is the smallest generator, and the empty
face is mask 0. Chain degree i here means simplicial degree i-1.
Characteristic 0 means Q; a positive characteristic must be prime.
"""
from __future__ import annotations

import argparse
from collections import defaultdict
from fractions import Fraction
from functools import lru_cache
from math import gcd, isqrt
import json


def check_characteristic(p: int) -> None:
    if p != 0 and (p < 2 or any(p % d == 0 for d in range(2, isqrt(p) + 1))):
        raise ValueError("characteristic must be 0 or a prime")


def orders(gens: tuple[int, ...], bound: int) -> list[int]:
    """Maximum lengths; -1 represents integers outside the semigroup."""
    out = [-1] * (bound + 1)
    out[0] = 0
    for s in range(1, bound + 1):
        lengths = [out[s - n] + 1 for n in gens if n <= s and out[s - n] >= 0]
        if lengths:
            out[s] = max(lengths)
    return out


def generators(values) -> tuple[int, ...]:
    g = tuple(values)
    if not g or any(type(n) is not int or n <= 0 for n in g):
        raise ValueError("generators must be positive integers")
    if g != tuple(sorted(set(g))) or gcd(*g) != 1:
        raise ValueError("generators must be strictly increasing with gcd 1")
    for i, n in enumerate(g):
        if i and orders(g[:i], n)[n] >= 0:
            raise ValueError(f"redundant generator {n}")
    return g


def support_bound(g: tuple[int, ...]) -> int:
    """All nonzero fine Betti degrees have s <= this proven bound."""
    return (g[0] - 1) * g[-1] + sum(g[1:])


def face_sums(g: tuple[int, ...]) -> tuple[int, ...]:
    out = [0] * (1 << len(g))
    for f in range(1, len(out)):
        v = f & -f
        out[f] = out[f ^ v] + g[v.bit_length() - 1]
    return tuple(out)


def weights(s: int, sums: tuple[int, ...], order: list[int]) -> dict[int, int]:
    """f -> ord(s-n_f)+|f| for the ordinary divisor faces only."""
    return {f: order[s - n] + f.bit_count()
            for f, n in enumerate(sums) if 0 <= s - n and order[s - n] >= 0}


def pair(w: dict[int, int], j: int) -> tuple[frozenset[int], frozenset[int]]:
    return (frozenset(f for f, h in w.items() if h >= j),
            frozenset(f for f, h in w.items() if h >= j + 1))


def absolute_complex(delta: frozenset[int], lam: frozenset[int], e: int):
    """Attach a cone on lam, using vertex e; leave delta alone if lam is void."""
    if not lam:
        return delta
    return frozenset(delta | lam | {f | (1 << e) for f in lam})


def is_complex(faces: frozenset[int]) -> bool:
    return all(f ^ (1 << v) in faces
               for f in faces for v in range(f.bit_length()) if (f >> v) & 1)


def boundary(faces: tuple[int, ...], i: int) -> list[list[int]]:
    """Augmented relative boundary C_i -> C_(i-1), omitted faces killed."""
    cols = [f for f in faces if f.bit_count() == i]
    rows = {f: r for r, f in enumerate(f for f in faces if f.bit_count() == i - 1)}
    a = [[0] * len(cols) for _ in rows]
    for c, f in enumerate(cols):
        pos = 0
        for v in range(f.bit_length()):
            if (f >> v) & 1:
                d = f ^ (1 << v)
                if d in rows:
                    a[rows[d]][c] = (-1) ** pos
                pos += 1
    return a


def rank(a: list[list[int]], p: int) -> int:
    """Exact Gaussian elimination, without floating point or modular guessing."""
    if not a or not a[0]:
        return 0
    m = [[Fraction(x) if p == 0 else x % p for x in row] for row in a]
    r = 0
    for col in range(len(m[0])):
        pivot = next((k for k in range(r, len(m)) if m[k][col]), None)
        if pivot is None:
            continue
        m[r], m[pivot] = m[pivot], m[r]
        inv = 1 / m[r][col] if p == 0 else pow(m[r][col], -1, p)
        m[r] = [x * inv if p == 0 else x * inv % p for x in m[r]]
        for k in range(r + 1, len(m)):
            t = m[k][col]
            if t:
                m[k] = [x - t * y if p == 0 else (x - t * y) % p
                        for x, y in zip(m[k], m[r])]
        r += 1
        if r == len(m):
            break
    return r


@lru_cache(maxsize=None)
def homology(faces: tuple[int, ...], e: int, p: int) -> tuple[int, ...]:
    """Betti dimensions indexed by shifted chain degree i=0,...,e."""
    sizes = [sum(f.bit_count() == i for f in faces) for i in range(e + 1)]
    ranks = [0] + [rank(boundary(faces, i), p) for i in range(1, e + 1)] + [0]
    answer = tuple(sizes[i] - ranks[i] - ranks[i + 1] for i in range(e + 1))
    if min(answer) < 0:
        raise ArithmeticError("negative homology dimension")
    return answer


def fine_betti(values, p: int = 0, extra: int = 0) -> dict[tuple[int, int, int], int]:
    """Map (homological i, exponent s, internal j) to positive dimension.

    extra optionally checks an additional interval above the proven cutoff.
    It never truncates the proven complete computation.
    """
    check_characteristic(p)
    g = generators(values)
    if extra < 0:
        raise ValueError("extra must be nonnegative")
    cap = support_bound(g)
    order = orders(g, cap + extra)
    sums = face_sums(g)
    out = {}
    for s in range(cap + extra + 1):
        w = weights(s, sums, order)
        strata = defaultdict(list)
        for f, j in w.items():
            strata[j].append(f)
        for j, faces in sorted(strata.items()):
            dims = homology(tuple(sorted(faces)), len(g), p)
            for i, dim in enumerate(dims):
                if dim:
                    if s > cap:
                        raise ArithmeticError("support bound violated")
                    out[i, s, j] = dim
    return out


def graded_betti(fine) -> dict[tuple[int, int], int]:
    out = defaultdict(int)
    for (i, _s, j), value in fine.items():
        out[i, j] += value
    return dict(sorted(out.items()))


def report(values, p: int = 0) -> dict:
    g = generators(values)
    fine = fine_betti(g, p)
    graded = graded_betti(fine)
    return {"generators": list(g), "characteristic": p,
            "support_bound": support_bound(g),
            "total_betti": [sum(v for (i, _j), v in graded.items() if i == h)
                            for h in range(len(g) + 1)],
            "graded_betti": [[i, j, v] for (i, j), v in graded.items()],
            "fine_betti": [[i, s, j, v] for (i, s, j), v in sorted(fine.items())]}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("generators", type=int, nargs="+")
    parser.add_argument("--characteristic", type=int, default=0)
    args = parser.parse_args()
    print(json.dumps(report(args.generators, args.characteristic), indent=2))


if __name__ == "__main__":
    main()
