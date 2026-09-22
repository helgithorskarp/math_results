#!/usr/bin/env python3
"""Exact corroboration of the proof; CPython 3.11+, standard library only.

No solver, floating point, network, randomness, or imported research data.
The all-length theorem is proved in PROOF.md, not by these finite checks.
"""
from collections import Counter
from functools import lru_cache
from itertools import product
import json
from math import comb
from pathlib import Path
import sys


def require(ok, message):
    if not ok:
        raise AssertionError(message)


def path_count(v, n):
    """Dynamic programming by the last coordinate of a path word."""
    require(v >= 2 and n >= 0, "invalid path parameters")
    row = [1] * (n + 1)
    for _ in range(v - 1):
        total, prefix = 0, []
        for value in row:
            total += value
            prefix.append(total)
        row = prefix[::-1]
    return sum(row)


@lru_cache(None)
def cycle_count(m, n):
    """Closed-walk DP, with a separately specified initial coordinate."""
    require(m >= 1 and m % 2 == 1 and n >= 0, "invalid cycle parameters")
    count = 0
    for first in range(n + 1):
        row = [int(i == first) for i in range(n + 1)]
        for _ in range(m):
            total, prefix = 0, []
            for value in row:
                total += value
                prefix.append(total)
            row = prefix[::-1]
        count += row[first]
    return count


def brute_count(v, n, cyclic):
    """Definition-level tuples, independent of either DP."""
    return sum(all(word[i] + word[i + 1] <= n for i in range(v - 1))
               and (not cyclic or word[-1] + word[0] <= n)
               for word in product(range(n + 1), repeat=v))


def gamma(poly):
    """Triangular conversion of a palindromic polynomial, no Lagrange formula."""
    require(poly and poly == poly[::-1], "polynomial is not palindromic")
    d, residual, answer = len(poly) - 1, list(poly), []
    for j in range(d // 2 + 1):
        value = residual[j]
        answer.append(value)
        for k in range(d - 2 * j + 1):
            residual[j + k] -= value * comb(d - 2 * j, k)
    require(not any(residual), "incomplete gamma conversion")
    return answer


def get(poly, j):
    return poly[j] if 0 <= j < len(poly) else 0


@lru_cache(None)
def path_gamma(q):
    require(q >= 1, "invalid fence size")
    v = 2 * q
    counts = [path_count(v, n) for n in range(v + 3)]
    h = [sum((-1) ** i * comb(v + 1, i) * counts[k - i]
             for i in range(min(k, v + 1) + 1)) for k in range(v + 3)]
    require(not any(h[v - 1:]), "path numerator has unexpected degree")
    return tuple(gamma(h[:v - 1]))


@lru_cache(None)
def cycle_gamma(q):
    require(q >= 0, "invalid odd-cycle size")
    m = 2 * q + 1
    counts = [cycle_count(m, n) for n in range(m + 4)]
    difference = [sum((-1) ** i * comb(m + 1, i) * counts[k - i]
                      for i in range(min(k, m + 1) + 1))
                  for k in range(m + 4)]
    r = [value + (difference[k - 1] if k else 0)
         for k, value in enumerate(difference)]
    require(not any(r[m:]), "reduced cycle numerator has unexpected degree")
    return tuple(gamma(r[:m]))


def fence(q):
    """The path is -1,+1,-2,+2,...,-q,+q, with negative elements minimal."""
    order = tuple(x for i in range(1, q + 1) for x in (-i, i))
    predecessors = {x: set() for x in order}
    for a, b in zip(order, order[1:]):
        if a < 0:
            predecessors[b].add(a)
        else:
            predecessors[a].add(b)
    return order, predecessors


def linear_extensions(labels, predecessors):
    def visit(word, used):
        if len(word) == len(labels):
            yield tuple(word)
            return
        for x in labels:
            if x not in used and predecessors[x] <= used:
                word.append(x)
                used.add(x)
                yield from visit(word, used)
                used.remove(x)
                word.pop()
    yield from visit([], set())


def no_double_descent(word):
    extended = (0,) + tuple(word) + (0,)
    return all(not (a > b > c) for a, b, c in zip(extended, extended[1:], extended[2:]))


def descents(word):
    return sum(a > b for a, b in zip(word, word[1:]))


def is_extension(word, labels, predecessors):
    if len(word) != len(labels) or set(word) != set(labels):
        return False
    seen = set()
    for x in word:
        if not predecessors[x] <= seen:
            return False
        seen.add(x)
    return True


def run_checks():
    brute_checks = 0
    for m in (1, 3, 5, 7):
        for n in range(4):
            require(cycle_count(m, n) == brute_count(m, n, True), "cycle DP mismatch")
            brute_checks += 1
    for v in (2, 4, 6):
        for n in range(4):
            require(path_count(v, n) == brute_count(v, n, False), "path DP mismatch")
            brute_checks += 1

    bridge_checks = 0
    for m in range(3, 32, 2):
        for n in range(11):
            require(4 * cycle_count(m, n) ==
                    (2 * n + 3) * path_count(m - 1, n) + cycle_count(m - 2, n),
                    "cycle-path trace identity failed")
            bridge_checks += 1

    recurrence_checks = growth_checks = sign_checks = upper_checks = 0
    for q in range(1, 17):
        a, b = path_gamma(q), path_gamma(q + 1)
        g, previous = cycle_gamma(q), cycle_gamma(q - 1)
        require(a[0] == g[0] == 1, "constant normalization failed")
        for j in range(q + 1):
            rhs = ((2 * j + 3) * get(a, j) + 8 * (q - j) * get(a, j - 1)
                   + get(previous, j) - 4 * get(previous, j - 1))
            require(4 * g[j] == rhs, "gamma recurrence failed")
            recurrence_checks += 1
            require(get(b, j) >= (j + 1) * get(a, j) + (2 * q - 2 * j + 1) * get(a, j - 1),
                    "fence growth inequality failed")
            growth_checks += 1
            require(g[j] <= b[j], "simultaneous upper bound failed")
            upper_checks += 1
            require(g[j] > 0 if j < q else g[j] == (-1) ** q, "sign theorem failed")
            sign_checks += 1
        require(all(x > 0 for x in a), "fence strict positivity failed")

    extension_count = representative_count = insertion_count = 0
    class_checks = 0
    for q in range(1, 6):
        labels, predecessors = fence(q)
        new_labels, new_predecessors = fence(q + 1)
        u, w = -(q + 1), q + 1
        counts, images = Counter(), set()
        for word in linear_extensions(labels, predecessors):
            extension_count += 1
            if not no_double_descent(word):
                continue
            representative_count += 1
            k = descents(word)
            counts[k] += 1
            local = Counter()
            # Eligible positions are defined from the old word; append is extra.
            positions = [i for i in range(len(word) - 1) if word[i] < word[i + 1]]
            positions.append(len(word))
            for i in positions:
                image = (u,) + word[:i] + (w,) + word[i:]
                require(is_extension(image, new_labels, new_predecessors), "insertion violates order")
                require(no_double_descent(image), "insertion creates a double descent")
                require(tuple(x for x in image if x not in (u, w)) == word, "deletion is not inverse")
                require(image not in images, "insertion collision")
                images.add(image)
                local[descents(image)] += 1
                insertion_count += 1
            require(local == Counter({k: k + 1, k + 1: 2 * q - 2 * k - 1}),
                    "incorrect insertion multiplicities")
        require(tuple(counts[j] for j in range(q)) == path_gamma(q),
                "canonical representatives disagree with independent Ehrhart gamma")
        class_checks += 1

    # Full fixed-denominator H conversion checks the otherwise easy-to-miss zeros.
    h_checks = 0
    for q in range(1, 7):
        m = 2 * q + 1
        counts = [cycle_count(m, n) for n in range(2 * m + 3)]
        h = [sum((-1) ** i * comb(m + 1, i) * counts[k - 2 * i]
                 for i in range(min(k // 2, m + 1) + 1))
             for k in range(2 * m + 3)]
        require(not any(h[2 * m:]), "fixed numerator degree mismatch")
        gh = gamma(h[:2 * m])
        require(gh == list(cycle_gamma(q)) + [0] * (m - q - 1),
                "fixed-degree gamma normalization mismatch")
        h_checks += 1

    rejected = 0
    bad_calls = (lambda: path_count(1, 0), lambda: path_count(2, -1),
                 lambda: cycle_count(2, 0), lambda: cycle_count(3, -1),
                 lambda: gamma([1, 2]), lambda: path_gamma(0))
    for call in bad_calls:
        try:
            call()
        except AssertionError:
            rejected += 1
        else:
            raise AssertionError("invalid input was accepted")
    require(not no_double_descent((-1, -2, 1, 2)), "left boundary was ignored")
    require(not no_double_descent((-2, -1, 2, 1)), "right boundary was ignored")

    return {
        "status": "PASS",
        "arithmetic": "exact Python integers",
        "definition_level_count_checks": brute_checks,
        "cycle_path_identity_checks": bridge_checks,
        "gamma_recurrence_checks": recurrence_checks,
        "fence_growth_checks": growth_checks,
        "simultaneous_upper_bound_checks": upper_checks,
        "sign_coefficient_checks": sign_checks,
        "finite_sign_scope": "odd cycle lengths 3 through 33; universal scope is from PROOF.md",
        "canonical_extension_classes_checked": class_checks,
        "linear_extensions_visited": extension_count,
        "canonical_representatives_checked": representative_count,
        "distinct_insertion_images_checked": insertion_count,
        "fixed_denominator_gamma_checks": h_checks,
        "invalid_inputs_rejected": rejected,
        "boundary_negative_controls": 2,
        "small_cycle_gamma_vectors": {str(2 * q + 1): list(cycle_gamma(q)) for q in range(1, 5)},
    }


if __name__ == "__main__":
    require(sys.argv[1:] in ([], ["--check"]), "usage: python3 verify.py [--check]")
    result = run_checks()
    if sys.argv[1:] == ["--check"]:
        expected = json.loads(Path(__file__).with_name("EXPECTED.json").read_text())
        require(result == expected, "output differs from EXPECTED.json")
    print(json.dumps(result, indent=2, sort_keys=True))
