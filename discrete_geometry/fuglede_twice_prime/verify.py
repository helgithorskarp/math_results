"""Exact corroboration of PROOF.md; Python 3.11+, standard library.

The universal theorem is the written proof, not an inference from this audit.
Polynomial and Ramanujan routines follow the earlier fuglede_two_point_levels
checker; this package is self-contained. The Fourier-zero clique oracle never
uses the binary criterion, the profile restriction, or a divisibility theorem.
"""
from collections import Counter
from functools import cache
from hashlib import sha256
from itertools import combinations, product
from math import comb, gcd, isqrt
from pathlib import Path
import json
import sys


def require(condition, message):
    if not condition:
        raise ValueError(message)


def prime(p):
    return p >= 2 and all(p % d for d in range(2, isqrt(p) + 1))


def trim(a):
    while len(a) > 1 and a[-1] == 0:
        a.pop()
    return a


def divide(a, b):
    require(b[-1] == 1 and len(b) >= 2, "monic nonconstant divisor")
    a = list(a)
    q = [0] * max(1, len(a) - len(b) + 1)
    while len(a) >= len(b):
        d, c = len(a) - len(b), a[-1]
        q[d] = c
        for j, coefficient in enumerate(b):
            a[d + j] -= c * coefficient
        trim(a)
    return trim(q), trim(a)


@cache
def phi(n):
    require(n >= 1, "positive cyclotomic order")
    if n == 1:
        return (-1, 1)
    a = [-1] + [0] * (n - 1) + [1]
    for d in range(1, n):
        if n % d == 0:
            a, remainder = divide(a, phi(d))
            require(remainder == [0], "cyclotomic factorization")
    return tuple(a)


@cache
def root(n, e):
    """Coordinates of zeta_n^e in Q[X]/Phi_n, with exact integer entries."""
    e %= n
    remainder = divide([0] * e + [1], phi(n))[1]
    return tuple(remainder + [0] * (len(phi(n)) - 1 - len(remainder)))


def sum_roots(n, exponents):
    coefficients = [0] * (len(phi(n)) - 1)
    for e in exponents:
        for i, a in enumerate(root(n, e % n)):
            coefficients[i] += a
    return tuple(coefficients)


def zero(n, exponents):
    exponents = tuple(e % n for e in exponents)
    common = n
    for e in exponents:
        common = gcd(common, e)
    if common > 1:
        return zero(n // common, (e // common for e in exponents))
    return not any(sum_roots(n, exponents))


@cache
def mobius(n):
    d, sign = 2, 1
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
    """Independent Tr(S conjugate(S)) test, entirely in Z."""
    counts = Counter(e % n for e in exponents)
    trace = sum(c * d * ramanujan(n, a - b)
                for a, c in counts.items() for b, d in counts.items())
    require(trace >= 0, "negative squared trace")
    return trace == 0


def spectral_pair(n, points, frequencies, checker=zero):
    if len(points) != len(frequencies):
        return False
    if len(set(points)) != len(points) or len(set(frequencies)) != len(frequencies):
        return False
    return all(checker(n, ((u - v) * a for a in points))
               for u, v in combinations(frequencies, 2))


def product_pair(n, p, points, frequencies, checker=zero):
    if len(points) != len(frequencies):
        return False
    if len(set(points)) != len(points) or len(set(frequencies)) != len(frequencies):
        return False
    return all(checker(n * p, (p * a * (u - v) + n * j * (s - t)
                              for a, j in points))
               for (u, s), (v, t) in combinations(frequencies, 2))


@cache
def zero_graph_spectrum(n, size, orders):
    """Exact clique search. Spectrum translation permits fixing frequency 0."""
    allowed = {d for d in range(1, n) if n // gcd(n, d) in orders}
    neighbors = [sum(1 << j for j in range(n) if (j - i) % n in allowed)
                 for i in range(n)]

    def search(chosen, available):
        if len(chosen) == size:
            return tuple(chosen)
        while len(chosen) + available.bit_count() >= size:
            bit = available & -available
            available ^= bit
            v = bit.bit_length() - 1
            result = search(chosen + [v], available & neighbors[v])
            if result is not None:
                return result
        return None

    return search([0], neighbors[0])


def find_spectrum(n, points):
    if not points or len(points) > n or len(set(points)) != len(points):
        return None
    # Galois conjugacy: vanishing at a root depends only on its order.
    orders = tuple(d for d in range(2, n + 1) if n % d == 0
                   and not any(sum_roots(d, points)))
    return zero_graph_spectrum(n, len(points), orders)


def v2(a):
    require(a > 0, "positive valuation argument")
    return (a & -a).bit_length() - 1


def parts(n, p, points):
    require(n >= 2 and prime(p) and p >= 3 and gcd(n, p) == 1,
            "odd coprime prime parameters")
    require(len(points) == 2 * p and len(set(points)) == 2 * p,
            "2p distinct points required")
    require(all(0 <= a < n and 0 <= j < p for a, j in points), "residue range")
    return [sorted(a for a, k in points if k == j) for j in range(p)]


def binary_valuation(n, levels):
    if n % 2 or any(len(level) != 2 for level in levels):
        return None
    values = {v2((b - a) % n) for a, b in levels}
    return next(iter(values)) if len(values) == 1 and max(values) < v2(n) else None


def canonical(n, p, t):
    spectrum = [(u, j) for u in (0, n // 2 ** (t + 1)) for j in range(p)]
    complement = [(a, 0) for a in range(n) if a % 2 ** (t + 1) < 2 ** t]
    return spectrum, complement


def tiles(n, p, points, complement):
    counts = Counter(((a + b) % n, (j + k) % p)
                     for a, j in points for b, k in complement)
    return len(counts) == n * p and set(counts.values()) == {1}


def normalized_subsets(n, size):
    if size <= n:
        for tail in combinations(range(1, n), size - 1):
            yield (0,) + tail


def audit_subsets():
    rows, digest = [], sha256()
    for n, p in ((2, 3), (4, 3), (5, 3), (7, 3), (8, 3),
                 (2, 5), (3, 5), (4, 5)):
        base_tests = {}
        for k in (p, 2 * p):
            count = 0
            for a in normalized_subsets(n, k):
                require(find_spectrum(n, a) is None, "base exclusion failed")
                count += 1
            base_tests[str(k)] = count
        tested = positive = unbalanced = 0
        inv_p, inv_n = pow(p, -1, n), pow(n, -1, p)
        for encoded in normalized_subsets(n * p, 2 * p):
            # encoded = p*a+n*j, a nonstandard but bijective CRT labeling.
            points = [(inv_p * e % n, inv_n * e % p) for e in encoded]
            levels = parts(n, p, points)
            t = binary_valuation(n, levels)
            found = find_spectrum(n * p, encoded)
            require((found is not None) == (t is not None),
                    "definition/criterion mismatch")
            tested += 1
            unbalanced += any(len(part) != 2 for part in levels)
            if found is not None:
                positive += 1
                frequencies = [(u % n, u % p) for u in found]
                require(product_pair(n, p, points, frequencies, trace_zero),
                        "independent found-spectrum check")
                require(all(len(part) == 2 for part in parts(n, p, frequencies)),
                        "spectrum is not balanced")
                explicit, complement = canonical(n, p, t)
                require(product_pair(n, p, points, explicit, trace_zero),
                        "canonical spectrum")
                require(tiles(n, p, points, complement), "unique tiling")
                digest.update(repr((n, p, encoded, t, found)).encode())
        require(tested == comb(n * p - 1, 2 * p - 1), "enumeration completeness")
        expected = 0 if n % 2 else sum(
            (n // 2 ** (t + 1)) * (n * n // 2 ** (t + 2)) ** (p - 1)
            for t in range(v2(n)))
        require(positive == expected, "independent subset-count formula")
        rows.append(dict(n=n, p=p, normalized_subsets=tested,
                         unbalanced_subsets=unbalanced, spectral_subsets=positive,
                         base_exclusion_tests=base_tests))
    return rows, digest.hexdigest()


def extract_paired(n, p, pairs, frequencies):
    """Check the algebra AFTER |N|<=2; may be tested without coprimality.

    This routine does not certify the universal reduction argument in Section 1.
    It treats constancy, row orthogonality, and pairwise orthogonality on N as
    independently checked hypotheses and checks the extracted spectrum directly.
    """
    require(len(pairs) == p and len(frequencies) == p + 1, "extraction sizes")
    require(len(set(frequencies)) == p + 1, "distinct extraction frequencies")
    require(all(x != y for x, y in pairs), "distinct pair entries")
    totals = {u: [sum_roots(n, (u * x, u * y)) for x, y in pairs]
              for u in frequencies}
    require(all(len(set(values)) == 1 for values in totals.values()),
            "nonconstant pair sums")
    require(all(zero(n, ((u - v) * a for pair in pairs for a in pair))
                for u, v in combinations(frequencies, 2)), "nonorthogonal rows")
    z = [u for u in frequencies if not any(totals[u][0])]
    nonzero = [u for u in frequencies if u not in z]
    require(1 <= len(nonzero) <= 2, "nonzero pair-sum count")
    require(all(zero(n, ((u - v) * x, (u - v) * y))
                for u, v in combinations(nonzero, 2) for x, y in pairs),
            "pairwise N orthogonality")
    if len(nonzero) == 1:
        selected = [x for x, y in pairs]
        spectrum = z
    else:
        u = nonzero[0]
        first, second = pairs[0]
        require((u * (first - second)) % n != 0, "equal nonzero pair values")
        chosen_value = u * first % n
        selected = []
        for x, y in pairs:
            eligible = [a for a in (x, y) if u * a % n == chosen_value]
            require(len(eligible) == 1, "pair-value orientation")
            selected.append(eligible[0])
        spectrum = z + [0]
    require(spectral_pair(n, selected, spectrum, trace_zero), "extracted spectrum")
    return dict(n=n, p=p, nonzero_pair_sums=len(nonzero),
                points=selected, spectrum=spectrum)


def audit_extraction():
    results = []
    for p in (3, 5, 7, 11):
        # Deliberately noncoprime fixtures make both extraction branches
        # nonvacuous. They test only the conditional vector algebra, not the
        # coprime spectral-pair theorem or realization of its mixed profile.
        pairs = [(2 * j, (2 * j + p) % (2 * p)) for j in range(p)]
        results.append(extract_paired(2 * p, p, pairs, [0] + list(range(1, 2 * p, 2))))
        pairs = [(4 * j, (4 * j + p) % (4 * p)) for j in range(p)]
        z = [u for u in range(2, 4 * p, 4) if u != 2 * p]
        results.append(extract_paired(4 * p, p, pairs, z + [p, 3 * p]))
    return results


def audit_pairing():
    tested = zeros = 0
    for n in range(2, 17):
        for p in (3, 5, 7):
            if n % p == 0:
                continue
            for k in range(1, p):
                for a, b in product(range(n), repeat=2):
                    exponents = [a, b] * k + [0, (a + b) % n] * (p - k)
                    found = zero(n, exponents)
                    require(found == trace_zero(n, exponents), "root arithmetic mismatch")
                    expected = n % 2 == 0 and {a, b} == {0, n // 2}
                    require(found == expected, "weighted-pairing consequence")
                    tested += 1
                    zeros += found
    require(zero(6, [2, 4, 2, 4, 0, 0]), "noncoprime control")
    return dict(equations=tested, zero_equations=zeros, noncoprime_control=True)


def partitions(total, length, lower=1):
    if length == 1:
        if total >= lower:
            yield (total,)
    else:
        for first in range(lower, total // length + 1):
            for tail in partitions(total - first, length - 1, first):
                yield (first,) + tail


def audit_profiles():
    rows = []
    for p in (3, 5, 7, 11, 13, 17):
        profiles = list(partitions(2 * p, p))
        survivors = [a for a in profiles if not (1 in a and any(2 <= x < p for x in a))]
        require(survivors == [(1,) * (p - 1) + (p + 1,), (2,) * p], "profile gap")
        r = p + 1
        gram = [[r if i == j else -(p - 1) for j in range(r)] for i in range(r)]
        value = sum(map(sum, gram))
        require(value == (p + 1) * (-p * p + 2 * p + 1) < 0, "Gram witness")
        rows.append(dict(p=p, profiles=len(profiles), survivors=survivors,
                         principal_gram_quadratic=value))
    return rows


def audit_fixtures():
    results = []
    for n, p, t, offsets, differences in (
        (210, 11, 0, list(range(0, 22, 2)), [1] * 11),
        (24, 5, 1, [0, 3, 8, 17, 23], [2, 6, 10, 14, 22]),
        (40, 3, 2, [1, 8, 14], [4, 12, 20]),
    ):
        points = [(x, j) for j, (a, d) in enumerate(zip(offsets, differences))
                  for x in (a, (a + d) % n)]
        require(binary_valuation(n, parts(n, p, points)) == t, "fixture criterion")
        frequencies, complement = canonical(n, p, t)
        for checker in (zero, trace_zero):
            require(product_pair(n, p, points, frequencies, checker), "fixture spectrum")
            require(product_pair(n, p, frequencies, points, checker), "fixture duality")
        require(tiles(n, p, points, complement), "fixture tiling")
        require(not tiles(n, p, points, complement[:-1]), "incomplete complement")
        require(not product_pair(n, p, points, frequencies[:-1]), "short spectrum")
        results.append(dict(n=n, p=p, valuation=t, complement_size=len(complement)))
    # Empty-level projection is tested at other cardinalities, where examples
    # exist without contradicting the twice-prime base-exclusion hypotheses.
    a = [(0, 0), (3, 0), (6, 1), (9, 1)]
    b = [(0, 0), (1, 0), (2, 0), (3, 0)]
    require(product_pair(12, 5, a, b, trace_zero), "empty-level fixture")
    require(spectral_pair(12, [x for x, j in a], [u for u, s in b], trace_zero),
            "empty-level projected spectrum")
    # In ordinary cyclic coordinates, the claimed fixed subgroup works.
    a2310 = [r + 22 * ((r * r + 17 * r) % 105) for r in range(22)]
    s2310 = [105 * j for j in range(22)]
    require(spectral_pair(2310, a2310, s2310, trace_zero), "cyclic 2310 spectrum")
    counts = Counter((a + 22 * j) % 2310 for a in a2310 for j in range(105))
    require(len(counts) == 2310 and set(counts.values()) == {1}, "cyclic 2310 tiling")
    return dict(binary_fixtures=results, empty_level_projection=True,
                cyclic_2310=True, total_2310_sets=str(105 ** 22))


def audit_bad_inputs():
    good = [(a, j) for a in (0, 1) for j in range(3)]
    bad = [(4, 2, good), (6, 3, good), (4, 9, good),
           (4, 3, good[:-1]), (4, 3, good[:-1] + [good[0]]),
           (4, 3, good[:-1] + [(4, 2)])]
    for args in bad:
        try:
            parts(*args)
        except ValueError:
            continue
        raise ValueError("malformed input accepted")
    return len(bad)


def main():
    require(sys.argv[1:] in ([], ["--check"]), "usage: python3 verify.py [--check]")
    rows, digest = audit_subsets()
    result = dict(scope="finite corroboration, not the universal proof",
                  subsets=rows, positive_record_sha256=digest,
                  extraction=audit_extraction(), pairing=audit_pairing(),
                  profiles=audit_profiles(), fixtures=audit_fixtures(),
                  rejected_inputs=audit_bad_inputs())
    if sys.argv[1:] == ["--check"]:
        expected = json.loads(Path(__file__).with_name("expected.json").read_text())
        # JSON normalizes tuples to lists.
        require(json.loads(json.dumps(result)) == expected, "expected output mismatch")
        print("PASS: all-subset classification, paired extraction, exact spectra, and tilings")
    else:
        print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
