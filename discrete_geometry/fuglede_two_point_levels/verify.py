"""Exact auxiliary checks for PROOF.md; Python 3.11+, standard library.

The universal claim is proved in prose, not by this finite audit. The tiny
spectral searches use only character orthogonality, not the claimed criterion.
Cyclotomic remainders and Ramanujan traces give separate exact zero tests.
Some elementary polynomial/clique routines are adapted from this repository's
discrete_geometry/fuglede_full_prime_fiber/verify.py.
"""
from collections import Counter
from functools import cache
from hashlib import sha256
from itertools import combinations, product
from math import gcd, isqrt
from pathlib import Path
import json
import sys


def require(ok, message):
    if not ok:
        raise ValueError(message)


def trim(a):
    while len(a) > 1 and a[-1] == 0:
        a.pop()
    return a


def divide(a, b):
    a = list(a)
    q = [0] * max(1, len(a) - len(b) + 1)
    while len(a) >= len(b):
        j, c = len(a) - len(b), a[-1]
        q[j] = c
        for k, v in enumerate(b):
            a[j + k] -= c * v
        trim(a)
    return trim(q), trim(a)


@cache
def phi(n):
    if n == 1:
        return (-1, 1)
    a = [-1] + [0] * (n - 1) + [1]
    for d in range(1, n):
        if n % d == 0:
            a, r = divide(a, phi(d))
            require(r == [0], "cyclotomic division")
    return tuple(a)


@cache
def cyclotomic_zero(n, exponents):
    common = n
    for e in exponents:
        common = gcd(common, e)
    if common > 1:
        return cyclotomic_zero(n // common, tuple(e // common for e in exponents))
    a = [0] * n
    for e in exponents:
        a[e % n] += 1
    return divide(trim(a), phi(n))[1] == [0]


def zero(n, exponents):
    return cyclotomic_zero(n, tuple(sorted(e % n for e in exponents)))


@cache
def mobius(n):
    sign, d = 1, 2
    while d * d <= n:
        if n % d == 0:
            n //= d
            sign = -sign
            if n % d == 0:
                return 0
        d += 1
    return -sign if n > 1 else sign


@cache
def ramanujan(n, t):
    g = gcd(n, t)
    return sum(d * mobius(n // d) for d in range(1, g + 1) if g % d == 0)


def trace_zero(n, exponents):
    # Tr(S*conj(S)) is a sum of nonnegative squared complex magnitudes;
    # it vanishes exactly when S does. The formula below uses only integers.
    c = Counter(e % n for e in exponents)
    trace = sum(a * b * ramanujan(n, (e - f) % n)
                for e, a in c.items() for f, b in c.items())
    require(trace >= 0, "trace positivity")
    return trace == 0


def characters(n, p, points, frequencies, checker=zero):
    if len(points) != len(frequencies) or len(set(points)) != len(points):
        return False
    if len(set(frequencies)) != len(frequencies):
        return False
    return all(checker(n * p, [p * a * (u - v) + n * j * (s - t)
                              for a, j in points])
               for (u, s), (v, t) in combinations(frequencies, 2))


def find_spectrum(n, points):
    """Exhaustive Fourier-zero-graph clique search, translated to include 0."""
    zeros = {d for d in range(1, n) if zero(n, [d * a for a in points])}
    adjacent = [sum(1 << j for j in range(n) if (j - i) % n in zeros)
                for i in range(n)]

    def extend(chosen, candidates):
        if len(chosen) == len(points):
            return chosen
        while len(chosen) + candidates.bit_count() >= len(points):
            bit = candidates & -candidates
            candidates ^= bit
            v = bit.bit_length() - 1
            found = extend(chosen + [v], candidates & adjacent[v])
            if found is not None:
                return found
        return None

    return extend([0], adjacent[0])


def prime(p):
    return p >= 2 and all(p % d for d in range(2, isqrt(p) + 1))


def v2(x):
    require(x > 0, "positive valuation argument")
    return (x & -x).bit_length() - 1


def levels(n, p, points):
    require(n >= 2 and prime(p) and gcd(n, p) == 1, "coprime prime parameters")
    require(len(points) == 2 * p and len(set(points)) == 2 * p, "distinct points")
    require(all(0 <= a < n and 0 <= j < p for a, j in points), "residue range")
    parts = [sorted(a for a, k in points if k == j) for j in range(p)]
    require(all(len(part) == 2 for part in parts), "two points per level")
    return parts


def binary_criterion(n, parts):
    if n % 2:
        return None
    vals = {v2((b - a) % n) for a, b in parts}
    return next(iter(vals)) if len(vals) == 1 and max(vals) < v2(n) else None


def canonical(n, p, t):
    spectrum = [(u, j) for u in (0, n // 2 ** (t + 1)) for j in range(p)]
    complement = [(a, 0) for a in range(n) if a % 2 ** (t + 1) < 2 ** t]
    return spectrum, complement


def tiles(n, p, points, complement):
    counts = Counter(((a + b) % n, (j + k) % p)
                     for a, j in points for b, k in complement)
    return len(counts) == n * p and set(counts.values()) == {1}


def audit_small():
    rows, digest = [], sha256()
    for n, p in ((2, 3), (3, 2), (3, 5), (4, 3), (4, 5), (5, 2), (5, 3), (8, 3)):
        # The base exclusion is independently searched, not inferred from n.
        base_count = sum(find_spectrum(n, a) is not None
                         for a in combinations(range(n), 2 * p))
        require(base_count == 0, "small-case base exclusion")
        tested = spectral = 0
        for parts in product(list(combinations(range(n), 2)), repeat=p):
            tested += 1
            points = [(a, j) for j, pair in enumerate(parts) for a in pair]
            encoded = [(p * a + n * j) % (n * p) for a, j in points]
            found = find_spectrum(n * p, encoded)
            t = binary_criterion(n, levels(n, p, points))
            require((found is not None) == (t is not None), "classification mismatch")
            if found is not None:
                spectral += 1
                frequencies = [(u % n, u % p) for u in found]
                require(characters(n, p, points, frequencies, trace_zero), "found spectrum trace")
                require(len({s for u, s in frequencies}) > 1, "base-excluded spectrum")
                antipodal = [d for d in range(1, n)
                             if all((d * (b - a)) % n == n // 2 for a, b in parts)]
                require(antipodal, "common antipodal character")
                canonical_spectrum, complement = canonical(n, p, t)
                require(characters(n, p, points, canonical_spectrum, trace_zero), "canonical spectrum")
                require(tiles(n, p, points, complement), "unique tiling")
                digest.update(repr((n, p, parts, t)).encode())
        rows.append(dict(n=n, p=p, candidate_sets=tested, spectral_sets=spectral,
                         base_spectral_sets_of_size_2p=base_count))
        cyclotomic_zero.cache_clear()
    return rows, digest.hexdigest()


def audit_pairing():
    tested = zeros = 0
    # Normalize R=T=1, S=x, U=y. After multiplication by y the equation is
    # k(x+y)+(p-k)(1+xy)=0. Its only solutions are {x,y}={1,-1}.
    for n in range(2, 21):
        for p in (2, 3, 5, 7):
            if n % p == 0:
                continue
            for k in range(1, p):
                for a, b in product(range(n), repeat=2):
                    exponents = [a, b] * k + [0, (a + b) % n] * (p - k)
                    c, r = zero(n, exponents), trace_zero(n, exponents)
                    require(c == r, "independent arithmetic disagreement")
                    expected = n % 2 == 0 and {a, b} == {0, n // 2}
                    require(c == expected, "weighted-pairing rigidity")
                    tested += 1
                    zeros += c
        cyclotomic_zero.cache_clear()
    # Failure when p divides n: x=zeta_6^2,y=zeta_6^4,k=2,p=3.
    require(zero(6, [2, 4, 2, 4, 0, 0]), "noncoprime pairing control")
    return dict(equations=tested, zero_equations=zeros, noncoprime_failure=True)


def audit_fixtures():
    out = []
    for n, p, offsets, differences, t in (
        (210, 11, list(range(0, 22, 2)), [1] * 11, 0),
        (24, 5, [0, 3, 8, 17, 23], [2, 6, 10, 14, 22], 1),
        (40, 3, [1, 8, 14], [4, 12, 20], 2),
    ):
        points = [(x, j) for j, (a, d) in enumerate(zip(offsets, differences))
                  for x in (a, (a + d) % n)]
        require(binary_criterion(n, levels(n, p, points)) == t, "fixture criterion")
        frequencies, complement = canonical(n, p, t)
        for test in (zero, trace_zero):
            require(characters(n, p, points, frequencies, test), "fixture orthogonality")
            require(characters(n, p, frequencies, points, test), "row orthogonality")
        require(tiles(n, p, points, complement), "fixture tiling")
        require(not characters(n, p, points, frequencies[:-1]), "missing frequency")
        require(not tiles(n, p, points, complement[:-1]), "missing translate")
        full_fibers = [a for a in range(n) if all((a, j) in points for j in range(p))]
        require(not full_fibers, "fixture outside full-fiber family")
        out.append(dict(n=n, p=p, valuation=t, points=points, spectrum=frequencies,
                        complement_size=len(complement), full_prime_fibers=0))
    points = [(0, 0), (4, 0), (0, 1), (1, 1), (1, 2), (3, 2)]
    frequencies = [(b, b % 3) for b in range(6)]
    complement = [(4 * k % 6, k) for k in range(3)]
    require(characters(6, 3, points, frequencies), "noncoprime spectrum")
    require(characters(6, 3, points, frequencies, trace_zero), "noncoprime trace")
    require(tiles(6, 3, points, complement), "noncoprime tile")
    require(binary_criterion(6, [[0, 4], [0, 1], [1, 3]]) is None, "binary branch fails")
    require(len({a for a, j in points}) < 6, "injective descent fails")
    counterexample = dict(n=6, p=3, points=points, spectrum=frequencies, complement=complement)
    invalid = 0
    for args in ((6, 3, points), (4, 4, []), (1, 3, []), (4, 3, [(0, 0)] * 6),
                 (4, 3, [(0, 0), (1, 0), (2, 0), (3, 0), (0, 1), (1, 1)]),
                 (4, 3, [(0, 0), (4, 0), (0, 1), (1, 1), (0, 2), (1, 2)])):
        try:
            levels(*args)
        except ValueError:
            invalid += 1
    require(invalid == 6, "invalid input rejection")
    return out, counterexample, invalid


def main():
    rows, digest = audit_small()
    pairing = audit_pairing()
    fixtures, boundary, invalid = audit_fixtures()
    result = dict(balanced_level_census=rows, spectral_set_digest=digest,
                  weighted_pairing_audit=pairing, positive_fixtures=fixtures,
                  coprimality_counterexample=boundary, invalid_inputs_rejected=invalid)
    encoded = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if sys.argv[1:] == ["--check"]:
        require(encoded == Path(__file__).with_name("expected.json").read_text(), "expected output")
        print("PASS: exact spectra, tilings, pairing equations, boundary, and expected output")
    else:
        require(not sys.argv[1:], "usage: verify.py [--check]")
        print(encoded, end="")


if __name__ == "__main__":
    main()
