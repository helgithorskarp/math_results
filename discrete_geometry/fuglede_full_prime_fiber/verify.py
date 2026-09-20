"""Exact definition-level checks for the full-prime-fiber theorem.

Python 3.11+, standard library. Small censuses corroborate the written
universal proof; they are not a search for all 22-point spectral sets.
"""
from collections import Counter
from functools import cache
from hashlib import sha256
from itertools import combinations, product
from math import gcd
import json


def require(condition, message):
    if not condition:
        raise ValueError(message)


def trim(poly):
    while len(poly) > 1 and poly[-1] == 0:
        poly.pop()
    return poly


def divide_monic(poly, divisor):
    poly = list(poly)
    quotient = [0] * max(1, len(poly)-len(divisor)+1)
    while len(poly) >= len(divisor):
        offset, factor = len(poly)-len(divisor), poly[-1]
        quotient[offset] = factor
        for j, c in enumerate(divisor):
            poly[offset+j] -= factor*c
        trim(poly)
    return trim(quotient), trim(poly)


@cache
def cyclotomic(n):
    if n == 1:
        return (-1, 1)
    poly = [-1] + [0]*(n-1) + [1]
    for d in range(1, n):
        if n % d == 0:
            poly, rem = divide_monic(poly, cyclotomic(d))
            require(rem == [0], "exact cyclotomic division")
    return tuple(poly)


@cache
def zero_sum(n, exponents):
    """An exact zero test in Q(zeta_n), with no complex floating point."""
    if not exponents:
        return True
    common = n
    for e in exponents:
        common = gcd(common, e)
    if common > 1:
        return zero_sum(n//common, tuple(e//common for e in exponents))
    coeff = [0]*n
    for e in exponents:
        coeff[e % n] += 1
    _, rem = divide_monic(trim(coeff), cyclotomic(n))
    return rem == [0]


def phases_zero(n, exponents):
    return zero_sum(n, tuple(sorted(e % n for e in exponents)))


def spectral_pair(n, p, points, frequencies):
    """Literal character inner products for Zn x Zp."""
    if (len(set(points)) != len(points) or len(frequencies) != len(points)
            or len(set(frequencies)) != len(frequencies)):
        return False
    for (b, u), (c, v) in combinations(frequencies, 2):
        if not phases_zero(n*p, (p*a*(b-c) + n*t*(u-v) for a, t in points)):
            return False
    return True


def find_spectrum(modulus, encoded_points):
    """Exact maximum-clique backtracking on the Fourier zero graph.

Every possible spectrum can be translated to contain frequency zero.
No fiber profile, valuation criterion, or predicted spectrum is used.
"""
    k = len(encoded_points)
    zeros = {d for d in range(1, modulus)
             if phases_zero(modulus, (d*a for a in encoded_points))}
    adjacent = [sum(1 << j for j in range(modulus)
                    if (j-i) % modulus in zeros) for i in range(modulus)]

    def extend(chosen, candidates):
        if len(chosen) == k:
            return chosen
        while len(chosen) + candidates.bit_count() >= k:
            bit = candidates & -candidates
            candidates ^= bit
            vertex = bit.bit_length()-1
            result = extend(chosen + [vertex], candidates & adjacent[vertex])
            if result is not None:
                return result
        return None

    return extend([0], adjacent[0])


def valuation_two(a):
    require(a > 0, "positive representative needed")
    return (a & -a).bit_length()-1


def classify(n, p, points):
    """The proposed normal form, independent of spectral clique search."""
    fiber = {(0, j) for j in range(p)}
    require(len(points) == 2*p and fiber <= set(points), "full fiber and size")
    rest = set(points) - fiber
    if n % 2 or Counter(j for a, j in rest) != Counter(range(p)):
        return None
    valuations = {valuation_two(a) for a, j in rest}
    if len(valuations) != 1:
        return None
    t = next(iter(valuations))
    return t if t < valuation_two(n) else None


def canonical_data(n, p, t):
    delta = n // (2**(t+1))
    frequencies = [(b, j) for b in (0, delta) for j in range(p)]
    complement = [(x, 0) for x in range(n) if x % (2**(t+1)) < 2**t]
    return frequencies, complement


def tiles(n, p, points, complement):
    counts = Counter(((a+b) % n, (j+k) % p)
                     for a, j in points for b, k in complement)
    return len(counts) == n*p and set(counts.values()) == {1}


def audit_full_fibers():
    rows, digest = [], sha256()
    for n, p in ((2, 3), (3, 5), (4, 3), (4, 5), (5, 3), (8, 3)):
        require(gcd(n, p) == 1, "coprime census parameters")
        # Verify the local base hypothesis directly in these tiny groups.
        base_count = 0
        for base in combinations(range(n), p):
            base_count += find_spectrum(n, base) is not None
        require(base_count == 0, "no p-point base spectral set")
        fiber = [(0, j) for j in range(p)]
        other = [(a, j) for a in range(1, n) for j in range(p)]
        candidates = spectral = strip_checks = 0
        for rest in combinations(other, p):
            candidates += 1
            points = fiber + list(rest)
            # a,j -> p*a+n*j is a group isomorphism to Z/(np).
            encoded = [(p*a+n*j) % (n*p) for a, j in points]
            found = find_spectrum(n*p, encoded)
            t = classify(n, p, points)
            require((found is not None) == (t is not None), "classification mismatch")
            if found is not None:
                spectral += 1
                frequencies = [(b % n, b % p) for b in found]
                require(spectral_pair(n, p, points, frequencies), "found spectrum")
                sections = [[b for b, u in frequencies if u == j] for j in range(p)]
                require(all(len(s) == 2 for s in sections), "two frequencies per level")
                # Test every way of selecting one of the two frequencies.
                for selected in product(*sections):
                    gamma = list(zip(selected, range(p)))
                    require(spectral_pair(n, p, list(rest), gamma), "fiber deletion")
                    strip_checks += 1
                canonical, complement = canonical_data(n, p, t)
                require(spectral_pair(n, p, points, canonical), "canonical spectrum")
                require(tiles(n, p, points, complement), "unique translations")
                digest.update(repr((n, p, rest, t)).encode())
        rows.append({"n": n, "p": p, "candidate_sets": candidates,
                     "spectral_sets": spectral, "spectrum_selections": strip_checks,
                     "base_spectral_sets_of_size_p": base_count})
        zero_sum.cache_clear()
    return rows, digest.hexdigest()


def audit_graph_dichotomy():
    tested = accepted = 0
    for n, p in ((2, 3), (3, 2), (4, 3)):
        universe = list(product(range(n), range(p)))
        for first in product(range(n), repeat=p):
            graph_spectrum = list(zip(first, range(p)))
            for points in combinations(universe, p):
                tested += 1
                if spectral_pair(n, p, points, graph_spectrum):
                    accepted += 1
                    levels = [j for a, j in points]
                    require(len(set(levels)) in (1, p), "graph-spectrum dichotomy")
        zero_sum.cache_clear()
    # Coprimality is essential: this spectral pair has level profile (2,1,0).
    points = [(0, 0), (1, 0), (1, 1)]
    frequencies = [(j, j) for j in range(3)]
    require(spectral_pair(3, 3, points, frequencies), "noncoprime counterexample")
    return {"candidate_pairs": tested, "spectral_pairs": accepted,
            "noncoprime_counterexample_levels": [2, 1, 0]}


def audit_fixtures():
    rows = []
    for n, p, t in ((12, 5, 0), (12, 5, 1), (24, 5, 2), (210, 11, 0)):
        offsets = [(2**t * (2*j+1)) % n for j in range(p)]
        points = [(0, j) for j in range(p)] + list(zip(offsets, range(p)))
        frequencies, complement = canonical_data(n, p, t)
        require(classify(n, p, points) == t, "fixture classification")
        require(spectral_pair(n, p, points, frequencies), "fixture orthogonality")
        require(tiles(n, p, points, complement), "fixture tiling")
        for h, k in ((1, 0), (0, 1), (n-1, p-1)):
            shifted = [((a+h) % n, (j+k) % p) for a, j in points]
            require(spectral_pair(n, p, shifted, frequencies), "translated spectrum")
            require(tiles(n, p, shifted, complement), "translated tiling")
        rows.append({"n": n, "p": p, "valuation": t,
                     "offsets": offsets, "complement_size": len(complement),
                     "translation_checks": 3})
    # Mixed valuations fail even though each individual offset is nonzero.
    points = [(0, j) for j in range(3)] + [(1, 0), (2, 1), (3, 2)]
    require(classify(4, 3, points) is None, "mixed valuation control")
    encoded = [(3*a+4*j) % 12 for a, j in points]
    require(find_spectrum(12, encoded) is None, "mixed valuation nonspectral")
    # A constant valuation at v2(n), rather than below it, is insufficient.
    points = [(0, j) for j in range(5)] + [(4, j) for j in range(5)]
    require(classify(12, 5, points) is None, "valuation upper boundary")
    encoded = [(5*a+12*j) % 60 for a, j in points]
    require(find_spectrum(60, encoded) is None, "upper boundary nonspectral")
    frequencies, complement = canonical_data(12, 5, 1)
    points = [(0, j) for j in range(5)] + [(2*(2*j+1) % 12, j) for j in range(5)]
    require(not spectral_pair(12, 5, points, frequencies[:-1]), "missing frequency")
    require(not tiles(12, 5, points, complement[:-1]), "missing translate")
    return rows


def main():
    # Familiar exact zero/nonzero controls for the arithmetic implementation.
    require(phases_zero(3, [0, 1, 2]), "third roots")
    require(phases_zero(8, [0, 4]), "antipodal roots")
    require(not phases_zero(5, [0, 1, 2]), "nonzero root sum")
    require(not phases_zero(1, [0]), "trivial character")
    rows, digest = audit_full_fibers()
    result = {"full_fiber_census": rows, "spectral_set_digest": digest,
              "graph_spectrum_dichotomy": audit_graph_dichotomy(),
              "explicit_fixtures": audit_fixtures(),
              "controls": ["root sums", "mixed valuations", "valuation upper boundary",
                           "missing frequency",
                           "missing translate", "noncoprime dichotomy counterexample"]}
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
