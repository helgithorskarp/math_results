#!/usr/bin/env python3
"""Exact corroboration of PROOF.md; CPython 3.11+, standard library only."""
from collections import Counter
from fractions import Fraction
from itertools import combinations, combinations_with_replacement, permutations, product
from math import comb, factorial
from pathlib import Path
import hashlib
import json


def check(ok, message):
    if not ok:
        raise ValueError(message)


def trim(p):
    p = list(p)
    while len(p) > 1 and p[-1] == 0:
        p.pop()
    return p


def mul(p, q):
    out = [0] * (len(p) + len(q) - 1)
    for i, a in enumerate(p):
        for j, b in enumerate(q):
            out[i + j] += a * b
    return trim(out)


def power(p, n):
    out = [1]
    for _ in range(n):
        out = mul(out, p)
    return out


def dilate(p, n):
    out = [0] * (n * (len(p) - 1) + 1)
    for i, a in enumerate(p):
        out[n * i] = a
    return out


def gammas(p, degree):
    check(len(p) <= degree + 1, "degree mismatch")
    p = list(p) + [0] * (degree + 1 - len(p))
    check(p == p[::-1], "nonpalindromic gamma input")
    out = []
    for j in range(degree // 2 + 1):
        a = p[j]
        out.append(a)
        for i in range(degree - 2 * j + 1):
            p[j + i] -= a * comb(degree - 2 * j, i)
    check(not any(p), "gamma reconstruction failed")
    return out


def series(num, den, bound):
    check(den[0] == 1, "denominator must have constant term one")
    out = []
    for i in range(bound + 1):
        a = num[i] if i < len(num) else 0
        out.append(a - sum(den[j] * out[i - j]
                           for j in range(1, min(len(den), i + 1))))
    return out


def cycle_type(g):
    check(sorted(g) == list(range(len(g))), "not a permutation")
    seen = set()
    out = []
    for i in range(len(g)):
        if i in seen:
            continue
        length = 0
        while i not in seen:
            seen.add(i)
            length += 1
            i = g[i]
        out.append(length)
    return tuple(sorted(out, reverse=True))


def partitions(n, cap=None):
    if n == 0:
        yield ()
        return
    for a in range(min(n, n if cap is None else cap), 0, -1):
        for rest in partitions(n - a, a):
            yield (a,) + rest


def centralizer(mu):
    z = 1
    for length, count in Counter(mu).items():
        z *= length ** count * factorial(count)
    return z


def numerator(h, mu):
    out = [1]
    for length in mu:
        out = mul(out, dilate(h, length))
    return out


def determinant(n, mu):
    out = [1, -1]
    for length in mu:
        out = mul(out, power([1] + [0] * (length - 1) + [-1], n))
    return out


def eulerian(n):
    p = [1]
    for size in range(2, n + 1):
        q = [0] * size
        for j in range(size):
            q[j] = ((j + 1) * p[j] if j < len(p) else 0)
            q[j] += (size - j) * p[j - 1] if j > 0 else 0
        p = q
    return p


def desc(w):
    return sum(a > b for a, b in zip(w, w[1:]))


def from_counts(counts):
    return trim([counts[i] for i in range(max(counts, default=0) + 1)])


def direct_points(n, k, bound):
    """Actual coordinate vectors, all maximal-clique inequalities, all g in S_k."""
    cliques = list(product(*[range(i * n, (i + 1) * n) for i in range(k)]))
    group = list(permutations(range(k)))
    counts = {g: [] for g in group}
    examined = 0
    for m in range(bound + 1):
        current = dict.fromkeys(group, 0)
        for x in product(range(m + 1), repeat=n * k):
            examined += 1
            if any(sum(x[v] for v in clique) > m for clique in cliques):
                continue
            for g in group:
                if all(x[i * n + j] == x[g[i] * n + j]
                       for i in range(k) for j in range(n)):
                    current[g] += 1
        for g in group:
            counts[g].append(current[g])
    return counts, examined


def invariants(h):
    d = len(h) - 1
    check(d % 2 == 0 and h == h[::-1], "even palindromic degree required")
    b = (-1) ** (d // 2) * sum((-1) ** i * a for i, a in enumerate(h))
    e = sum(h)
    check(b > 0, "positive top ordinary gamma coefficient required")
    check(e >= b and (e - b) % 2 == 0, "invalid signed alphabet")
    return b, e


def run():
    h = eulerian(5)
    check(h == [1, 26, 66, 26, 1], "Eulerian recurrence control")
    words = list(permutations(range(5)))
    degrees = [desc(w) for w in words]
    direct_h = from_counts(Counter(degrees))
    cube_counts = [(m + 1) ** 5 for m in range(7)]
    cube_h = trim(mul(cube_counts, [(-1) ** j * comb(6, j) for j in range(7)])[:7])
    check(h == direct_h == cube_h, "three ordinary numerator routes disagree")
    check(gammas(h, 4) == [1, 22, 16], "ordinary gamma control")

    point_checks = 0
    vectors = 0
    point_data = []
    for n, k, bound in [(5, 2, 2), (5, 3, 1), (3, 3, 2)]:
        actual, tested = direct_points(n, k, bound)
        vectors += tested
        for g, counts in actual.items():
            mu = cycle_type(g)
            predicted = series(numerator(eulerian(n), mu), determinant(n, mu), bound)
            check(predicted == counts, "definition-level fixed-point mismatch")
            point_checks += len(counts)
            point_data.append([n, k, g, counts])

    # S2: independent symmetric/exterior bases, compared with character projections.
    symmetric = Counter(sum(degrees[i] for i in pair)
                        for pair in combinations_with_replacement(range(120), 2))
    exterior2 = Counter(sum(degrees[i] for i in pair)
                        for pair in combinations(range(120), 2))
    id2, swap = power(h, 2), dilate(h, 2)
    projected_trivial = [(a + b) // 2 for a, b in zip(id2, swap)]
    projected_sign = [(a - b) // 2 for a, b in zip(id2, swap)]
    check(from_counts(symmetric) == trim(projected_trivial), "symmetric square mismatch")
    check(from_counts(exterior2) == trim(projected_sign), "exterior square mismatch")
    trivial_gamma = gammas(from_counts(symmetric), 8)
    sign_gamma = gammas(from_counts(exterior2), 8)
    check(trivial_gamma == [1, 18, 281, 292, 188], "S2 trivial gamma certificate")
    check(sign_gamma == [0, 26, 235, 412, 68], "S2 sign gamma certificate")
    check(min(trivial_gamma + sign_gamma) >= 0, "S2 is not effective")

    # S3: count actual three-element subsets of linear extensions, without characters.
    exterior3 = Counter(sum(degrees[i] for i in triple)
                        for triple in combinations(range(120), 3))
    exterior_poly = from_counts(exterior3)
    exterior_gamma = gammas(exterior_poly, 12)
    g_id = gammas(power(h, 3), 12)
    g_trans = gammas(mul(dilate(h, 2), h), 12)
    g_cycle = gammas(dilate(h, 3), 12)
    character_sign = []
    for a, b, c in zip(g_id, g_trans, g_cycle):
        value = Fraction(a - 3 * b + 2 * c, 6)
        check(value.denominator == 1, "nonintegral S3 sign multiplicity")
        character_sign.append(int(value))
    check(exterior_gamma == character_sign, "exterior and character routes disagree")
    check(exterior_gamma[-1] == -272, "S3 obstruction missing")
    b, e = invariants(h)
    check((b, e) == (16, 120), "base invariants")
    top_s3 = [Fraction(b * (b * b + 3 * e + 2), 6),
              Fraction(b ** 3 - b, 3),
              Fraction(b * (b * b - 3 * e + 2), 6)]
    check(top_s3 == [1648, 1360, -272], "S3 top decomposition")

    # Subgroup persistence: direct polynomial reconstruction in ten finite controls.
    persistence = []
    for k in range(3, 13):
        base = power(h, k - 3)
        values = [gammas(mul(base, numerator(h, mu)), 4 * k)[-1]
                  for mu in [(1, 1, 1), (2, 1), (3,)]]
        actual = Fraction(values[0] - 3 * values[1] + 2 * values[2], 6)
        expected = -272 * 16 ** (k - 3)
        check(actual == expected, "restriction persistence mismatch")
        persistence.append([k, expected])

    # General sign formula checked via the conjugacy-class cycle index.
    parity_checks = 0
    sign_checks = 0
    first_checks = 0
    for n in [1, 3, 5, 7]:
        base_h = eulerian(n)
        base_b, base_e = invariants(base_h)
        u, v = (base_e + base_b) // 2, (base_e - base_b) // 2
        for k in range(1, 8):
            sign_inner = Fraction(0)
            first_inner = Fraction(0)
            for mu in partitions(k):
                g = gammas(numerator(base_h, mu), (n - 1) * k)
                top = base_b ** sum(l % 2 for l in mu) * base_e ** sum(l % 2 == 0 for l in mu)
                check(g[-1] == top, "cycle-parity formula mismatch")
                parity_checks += 1
                sign_inner += Fraction((-1) ** (k - len(mu)) * top, centralizer(mu))
                if n > 1 and k >= 2:
                    a, d = base_h[1], n - 1
                    check(g[1] == a * mu.count(1) - k * d, "first character value")
                    first_inner += Fraction(g[1], centralizer(mu))
            coefficient = sum((-1) ** j * comb(v, j) * comb(u, k - j)
                              for j in range(k + 1) if j <= v and k - j <= u)
            check(sign_inner == coefficient, "sign generating polynomial mismatch")
            sign_checks += 1
            if n > 1 and k >= 2:
                check(first_inner == base_h[1] - k * (n - 1), "first trivial multiplicity")
                first_checks += 1
    check(26 - 4 * 6 == 2 and 26 - 4 * 7 == -2, "eventual bound boundary")

    # Guard against overgeneralizing either necessary/sufficient condition.
    check(Fraction(2 ** 2 - 6, 2) == -1, "A3 already fails at two copies")
    b7, e7 = invariants(eulerian(7))
    check(b7 * (b7 * b7 - 3 * e7 + 2) > 0, "A7 must not be ruled out by S3 test")
    check(gammas([1], 0) == [1], "chain control")
    for action in [lambda: invariants([1, 1]),
                   lambda: invariants([1, 2, 1]),
                   lambda: cycle_type((0, 0))]:
        try:
            action()
        except ValueError:
            pass
        else:
            raise ValueError("invalid-input rejection failed")

    return {
        "schema": 1, "status": "all exact checks passed",
        "base_numerator": h, "base_gamma": [1, 22, 16],
        "base_even_odd_descents": [sum(d % 2 == 0 for d in degrees),
                                   sum(d % 2 == 1 for d in degrees)],
        "ordinary_linear_extensions": len(words),
        "direct_coordinate_vectors": vectors,
        "direct_fixed_count_comparisons": point_checks,
        "direct_fixed_data_sha256": hashlib.sha256(json.dumps(point_data, separators=(",", ":")).encode()).hexdigest(),
        "symmetric_pairs": sum(symmetric.values()),
        "exterior_pairs": sum(exterior2.values()),
        "exterior_triples": sum(exterior3.values()),
        "s2_gamma_trivial": trivial_gamma, "s2_gamma_sign": sign_gamma,
        "s3_gamma_sign": exterior_gamma,
        "s3_top_decomposition_trivial_standard_sign": [int(x) for x in top_s3],
        "restriction_controls": persistence,
        "cycle_parity_checks": parity_checks,
        "sign_cycle_index_checks": sign_checks,
        "first_trivial_multiplicity_checks": first_checks,
        "controls": 7,
    }


if __name__ == "__main__":
    result = run()
    expected = Path(__file__).with_name("EXPECTED.json")
    if expected.exists():
        check(result == json.loads(expected.read_text()), "EXPECTED.json mismatch")
    print(json.dumps(result, indent=2, sort_keys=True))
