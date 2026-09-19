#!/usr/bin/env python3
"""Exact finite audit of PROOF.md. CPython 3.11+, standard library only."""
from collections import Counter
from itertools import combinations, permutations, product
from math import comb, factorial
from pathlib import Path
import hashlib
import json


def require(condition, message):
    if not condition:
        raise ValueError(message)


def trim(p):
    p = list(p)
    while len(p) > 1 and p[-1] == 0:
        p.pop()
    return p


def multiply(a, b):
    c = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            c[i + j] += x * y
    return trim(c)


def power(a, k):
    c = [1]
    for _ in range(k):
        c = multiply(c, a)
    return c


def stretch(a, k):
    c = [0] * ((len(a) - 1) * k + 1)
    for i, x in enumerate(a):
        c[i * k] = x
    return c


def gamma(a, degree):
    require(len(a) <= degree + 1, "polynomial exceeds gamma center")
    a = list(a) + [0] * (degree + 1 - len(a))
    require(a == a[::-1], "gamma input is not palindromic")
    out = []
    for j in range(degree // 2 + 1):
        c = a[j]
        out.append(c)
        for k in range(degree - 2 * j + 1):
            a[j + k] -= c * comb(degree - 2 * j, k)
    require(not any(a), "gamma reconstruction failed")
    return out


def rational_series(numerator, denominator, bound):
    require(denominator[0] == 1, "nonunit series denominator")
    out = []
    for i in range(bound + 1):
        v = numerator[i] if i < len(numerator) else 0
        v -= sum(denominator[j] * out[i - j]
                 for j in range(1, min(i + 1, len(denominator))))
        out.append(v)
    return out


def cycles(g):
    require(sorted(g) == list(range(len(g))), "not a permutation")
    seen = set()
    out = []
    for v in range(len(g)):
        if v in seen:
            continue
        c = []
        while v not in seen:
            seen.add(v)
            c.append(v)
            v = g[v]
        out.append(tuple(c))
    return out


def posets(n):
    """All transitively closed strict orders compatible with labels 0,...,n-1.

    This is a finite fixture family, not an isomorphism-class enumeration.
    """
    pairs = list(combinations(range(n), 2))
    for mask in range(1 << len(pairs)):
        rel = {p for i, p in enumerate(pairs) if mask >> i & 1}
        if all((i, k) in rel for i, j in rel for jj, k in rel if j == jj):
            yield frozenset(rel)


def maximal_chains(n, rel):
    all_chains = []
    for mask in range(1, 1 << n):
        c = tuple(i for i in range(n) if mask >> i & 1)
        if all((i, j) in rel for i, j in combinations(c, 2)):
            all_chains.append(c)
    return [c for c in all_chains
            if not any(set(c) < set(d) for d in all_chains)]


def extensions(n, rel):
    out = []
    for w in permutations(range(n)):
        inverse = {v: i for i, v in enumerate(w)}
        if all(inverse[x] < inverse[y] for x, y in rel):
            out.append(w)
    return out


def desc(w):
    return sum(a > b for a, b in zip(w, w[1:]))


def descent_polynomial(words):
    counts = Counter(desc(w) for w in words)
    return [counts[i] for i in range(max(counts) + 1)]


def ordinal_rel(n, rel, k):
    out = {(a * n + x, a * n + y) for a in range(k) for x, y in rel}
    out.update((a * n + x, b * n + y) for a in range(k)
               for b in range(a + 1, k) for x in range(n) for y in range(n))
    return out


def direct_fixed_counts(n, rel, k, bound):
    """Enumerate full ambient vectors; test every maximal-chain inequality.

    Neither shell convolution nor a quotient-polytope formula is used.
    """
    chains = maximal_chains(n * k, ordinal_rel(n, rel, k))
    group = list(permutations(range(k)))
    result = {g: [] for g in group}
    tested = 0
    for m in range(bound + 1):
        count = {g: 0 for g in group}
        for x in product(range(m + 1), repeat=n * k):
            tested += 1
            if any(sum(x[i] for i in c) > m for c in chains):
                continue
            for g in group:
                if all(x[a * n + i] == x[g[a] * n + i]
                       for a in range(k) for i in range(n)):
                    count[g] += 1
        for g in group:
            result[g].append(count[g])
    return result, tested


def cycle_numerator(h, g):
    out = [1]
    for c in cycles(g):
        out = multiply(out, stretch(h, len(c)))
    return out


def determinant(n, g):
    out = [1, -1]  # Fixed homogenizing direction.
    for c in cycles(g):
        out = multiply(out, power([1] + [0] * (len(c) - 1) + [-1], n))
    return out


def gamma_characters(h, k):
    d = len(h) - 1
    identity = gamma(power(h, k), k * d)
    tau_value = gamma(multiply(stretch(h, 2), power(h, k - 2)), k * d)
    trivial = []
    sign = []
    for a, b in zip(identity, tau_value):
        require((a + b) % 2 == 0, "nonintegral C2 character")
        trivial.append((a + b) // 2)
        sign.append((a - b) // 2)
    return identity, tau_value, trivial, sign


def root_multiplicity(a):
    a = trim(a)
    order = 0
    while len(a) > 1 and sum(c * (-1) ** i for i, c in enumerate(a)) == 0:
        quotient = [a[0]]
        for c in a[1:-1]:
            quotient.append(c - quotient[-1])
        require(quotient[-1] == a[-1], "division by 1+t failed")
        a = trim(quotient)
        order += 1
    return order, a


def obstruction_check(h, k):
    s, b = root_multiplicity(h)
    require(s > 0, "obstruction hypothesis does not hold")
    d = len(h) - 1
    require((d - s) % 2 == 0, "invalid palindromic root parity")
    j = k * ((d - s) // 2) + s
    b_minus = sum(c * (-1) ** i for i, c in enumerate(b))
    expected = (-1) ** j * sum(h) * b_minus ** (k - 2)
    a, v, trivial, sign = gamma_characters(h, k)
    require(a[j] == 0 and v[j] == expected != 0, "root obstruction mismatch")
    require(min(trivial[j], sign[j]) < 0, "negative multiplicity missing")
    return j, expected


def multiset_descents(n, a):
    """Independent ideal-state recurrence for n chains of a elements."""
    states = {(tuple([0] * n), -1): [1]}
    for _ in range(n * a):
        next_states = {}
        for (counts, last), p in states.items():
            for letter in range(n):
                if counts[letter] == a:
                    continue
                new_counts = list(counts)
                new_counts[letter] += 1
                key = (tuple(new_counts), letter)
                v = ([0] + p) if last > letter else p
                old = next_states.setdefault(key, [0] * len(v))
                old.extend([0] * (len(v) - len(old)))
                for i, c in enumerate(v):
                    old[i] += c
        states = next_states
    out = [0] * (n * a + 1)
    for p in states.values():
        for i, c in enumerate(p):
            out[i] += c
    return trim(out)


def run():
    report = {"schema": 1, "posets_by_size": {}, "direct_coordinate_vectors": 0,
              "direct_fixed_comparisons": 0, "direct_module_comparisons": 0,
              "graded_posets": 0, "root_obstruction_checks": 0}
    digest = hashlib.sha256()
    for n in range(1, 5):
        fixtures = list(posets(n))
        report["posets_by_size"][str(n)] = len(fixtures)
        for rel in fixtures:
            words = extensions(n, rel)
            h = descent_polynomial(words)
            chains = maximal_chains(n, rel)
            graded = len({len(c) for c in chains}) == 1
            if graded:
                report["graded_posets"] += 1
                degree = n - len(chains[0])
                require(len(h) - 1 == degree, "graded degree formula fails")
                require(all(x >= 0 for x in gamma(h, degree)), "ordinary gamma")
                if root_multiplicity(h)[0]:
                    for k in range(2, 7):
                        obstruction_check(h, k)
                        report["root_obstruction_checks"] += 1
            for k in range(2, 5):
                if n * k > 9:
                    continue
                bound = 3 if n * k <= 6 else 2
                actual, tested = direct_fixed_counts(n, rel, k, bound)
                report["direct_coordinate_vectors"] += tested
                for g, counts in actual.items():
                    numerator = cycle_numerator(h, g)
                    predicted = rational_series(numerator, determinant(n, g), bound)
                    require(counts == predicted, "direct fixed-lattice count mismatch")
                    report["direct_fixed_comparisons"] += len(counts)
                    digest.update(json.dumps([n, sorted(rel), k, g, counts],
                                             separators=(",", ":")).encode())
                    if len(words) ** k <= 4096:
                        fixed = Counter()
                        for ws in product(words, repeat=k):
                            if all(ws[i] == ws[g[i]] for i in range(k)):
                                fixed[sum(desc(w) for w in ws)] += 1
                        decoded = trim([fixed[i] for i in range(k * n + 1)])
                        require(decoded == numerator, "graded permutation model mismatch")
                        report["direct_module_comparisons"] += 1
    require(report["posets_by_size"] == {"1": 1, "2": 2, "3": 7, "4": 40},
            "finite fixture generation count changed")

    # Product-of-simplices Ehrhart counts versus a separate multiset-word DP.
    families = []
    for n in range(2, 7):
        for a in range(1, 4):
            dimension = n * a
            counts = [comb(m + a, a) ** n for m in range(dimension + 1)]
            denominator = [(-1) ** j * comb(dimension + 1, j)
                           for j in range(dimension + 2)]
            h = trim(multiply(counts, denominator)[:dimension + 1])
            require(h == multiset_descents(n, a), "independent ordinary h mismatch")
            require(h == h[::-1] and len(h) - 1 == a * (n - 1), "family degree")
            e = factorial(dimension) // factorial(a) ** n
            require(sum(h) == e, "linear extension count mismatch")
            if n % 2 == 0 and a % 2 == 1:
                j, value = obstruction_check(h, 2)
                require(j == a * (n - 1) and value == -e, "family top coefficient")
                for k in range(3, 7):
                    obstruction_check(h, k)
                report["root_obstruction_checks"] += 5
                families.append({"n": n, "a": a, "top_gamma_index": j,
                                 "trivial_multiplicity": -e // 2,
                                 "sign_multiplicity": e // 2})
    report["product_simplex_vs_multiset_cases"] = 15
    report["named_odd_degree_families"] = families

    # Hand-checkable positive/negative controls, including even degree failure.
    c4 = gamma_characters([1, 1], 2)
    require(c4 == ([1, 0], [1, -2], [1, -1], [0, 1]), "C4 control")
    a3 = gamma_characters([1, 4, 1], 2)
    require(a3[2][-1] == 5 and a3[3][-1] == -1, "even-degree negative control")
    a5 = [1, 26, 66, 26, 1]
    require(all(v >= 0 for row in gamma_characters(a5, 2)[2:] for v in row),
            "positive C2 control for five-element antichain")
    chain = gamma_characters([1], 2)
    require(chain == ([1], [1], [1], [0]), "simplex control")
    # Removing the fixed homogenizing direction must change even degree-one counts.
    wrong = rational_series([1, 0, 1], power([1, 0, -1], 2), 2)
    require(wrong != [1, 1, 4], "missing-homogenizer control failed")
    for action in [lambda: gamma([1, 2], 1), lambda: cycles((0, 0)),
                   lambda: obstruction_check([1], 2)]:
        try:
            action()
        except ValueError:
            pass
        else:
            raise ValueError("malformed-input rejection failed")
    report["controls"] = 8
    report["direct_fixed_data_sha256"] = digest.hexdigest()
    report["c4_gamma_trivial"] = c4[2]
    report["c4_gamma_sign"] = c4[3]
    report["status"] = "all exact checks passed"
    return report


if __name__ == "__main__":
    result = run()
    expected_path = Path(__file__).with_name("EXPECTED.json")
    if expected_path.exists():
        require(json.loads(expected_path.read_text()) == result, "EXPECTED.json mismatch")
    print(json.dumps(result, indent=2, sort_keys=True))
