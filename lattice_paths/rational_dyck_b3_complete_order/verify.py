#!/usr/bin/env python3
"""Definition-level audit of the complete height-three order.

The carrier, literal continued-fraction digits, scalar continuants, and every
cyclic Lagrange cut are reconstructed without using the proposed rank to
select, prune, or sort paths. Finite checks corroborate PROOF.md.
"""

import argparse
from collections import Counter, defaultdict
from fractions import Fraction
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path

import identities
import order


def ensure(condition, message):
    if not condition:
        raise ArithmeticError(message)


def carrier(a):
    # Independent enumeration: positions of the three U steps in a literal word.
    # The last U is forced to be last by the diagonal inequality.
    for first, second in combinations(range(a + 2), 2):
        word = ["R"] * (a + 3)
        word[first] = word[second] = word[-1] = "U"
        right = up = 0
        for letter in word:
            right += letter == "R"
            up += letter == "U"
            if a * up > 3 * right:
                break
        else:
            yield (first, second - first - 1, a + 1 - second), "".join(word)


def digits(word):
    result = []
    for a, b in zip(word, word[1:]):
        result.extend((1, 1) if a == b else (2,))
    return result


def convergents(coefficients):
    p0, p1, q0, q1 = 0, 1, 1, 0
    for digit in coefficients:
        p0, p1 = p1, digit * p1 + p0
        q0, q1 = q1, digit * q1 + q0
    return p1, p0, q1, q0


def lagrange_squared(coefficients):
    period = [2] + coefficients
    candidates = []
    trace = None
    for j in range(len(period)):
        p, r, q, s = convergents(period[j:] + period[:j])
        ensure(p * s - r * q == 1, "period determinant")
        if trace is None:
            trace = p + s
        ensure(p + s == trace and q > 0, "cyclic trace/denominator")
        candidates.append(Fraction((p - s) ** 2 + 4 * r * q, q * q))
    return max(candidates)


def fib_table(limit):
    values = [0, 1]
    for _ in range(limit - 1):
        values.append(values[-1] + values[-2])
    return values


def run_matrix_score(runs, fs):
    matrix = [[1, 0], [0, 1]]
    for n in runs:
        k = [[fs[2 * n + 3], fs[2 * n + 1]],
             [fs[2 * n + 1], fs[2 * n - 1] if n else 1]]
        matrix = [[sum(matrix[i][ell] * k[ell][j] for ell in range(2))
                   for j in range(2)] for i in range(2)]
    return matrix[1][0]


def check_chain(candidate, actual):
    ensure(candidate == actual, "proposed chain differs from literal-score sort")


def reject(call):
    try:
        call()
    except (ValueError, ArithmeticError):
        return
    raise ArithmeticError("malformed input/certificate accepted")


def audit(max_a=120, lagrange_max_a=40):
    if max_a < 11 or not 5 <= lagrange_max_a <= max_a:
        raise ValueError("need max_a>=11 and 5<=lagrange_max_a<=max_a")
    result = {"matching_max_a": max_a, "lagrange_max_a": lagrange_max_a,
              "endpoints": 0, "paths": 0, "matching_covers": 0,
              "lagrange_paths": 0, "cyclic_digit_cuts": 0,
              "lagrange_levels": 0, "fully_checked_cover_comparisons": 0,
              "fully_checked_discordant_pairs": 0}
    match_hash, lag_hash = sha256(), sha256()
    examples = []
    for a in range(4, max_a + 1):
        if a % 3 == 0:
            continue
        rows = []
        fs = fib_table(2 * a + 3)
        lag = {}
        for runs, word in carrier(a):
            coefficients = digits(word)
            score = convergents(coefficients)[0]
            ensure(score == run_matrix_score(runs, fs), (a, runs, "matrix bridge"))
            rows.append((score, runs))
            if a <= lagrange_max_a:
                lag[runs] = lagrange_squared(coefficients)
                result["cyclic_digit_cuts"] += len(coefficients) + 1
        rows.sort(reverse=True)
        actual = [runs for score, runs in rows]
        ensure(len({score for score, _ in rows}) == len(rows), (a, "matching tie"))
        check_chain(list(order.chain(a)), actual)
        ensure(len(rows) == order.total(a), (a, "carrier count"))
        for j, (score, runs) in enumerate(rows):
            ensure(order.rank(runs) == j and order.unrank(a, j) == runs, (a, runs, "rank"))
            ensure(j == 0 or order.covers(runs, rows[j - 1][1]), (a, runs, "cover"))
            match_hash.update(json.dumps([a, j, list(runs), score], separators=(",", ":")).encode() + b"\n")
        result["endpoints"] += 1
        result["paths"] += len(rows)
        result["matching_covers"] += len(rows) - 1

        if lag:
            unique = sorted(set(lag.values()), reverse=True)
            level = {score: i for i, score in enumerate(unique)}
            ranks = [level[lag[runs]] for runs in actual]
            fibres = defaultdict(list)
            for runs, j in zip(actual, ranks):
                ensure(order.lagrange_rank(runs) == j, (a, runs, "Lagrange rank"))
                fibres[j].append(runs)
            for paths in fibres.values():
                ensure(len({tuple(sorted(r, reverse=True)) for r in paths}) == 1,
                       (a, "Lagrange fibre mismatch"))
            deltas = Counter(right - left for left, right in zip(ranks, ranks[1:]))
            stats = order.statistics(a)
            m, epsilon = divmod(a, 3)
            expected = Counter({0: stats["lagrange_tied_matching_covers"],
                                1: stats["common_oriented_covers"]})
            expected.update({-distance: 1 for distance in range(1, m)})
            ensure(deltas == expected, (a, deltas, expected))
            crossed = sum(left > right for i, left in enumerate(ranks) for right in ranks[i + 1:])
            ensure(crossed == stats["discordant_unequal_fibre_pairs"], (a, "all-pair count"))
            ensure(len(unique) == stats["lagrange_levels"], (a, "level count"))
            nonlocal_pairs = []
            for j, (left, right) in enumerate(zip(ranks, ranks[1:])):
                if abs(right - left) > 1:
                    nonlocal_pairs.append((actual[j + 1], actual[j], left - right))
            predicted = [((a - 1 - 2 * z, z + 1, z),
                          (2 * m + epsilon - z, z, m), m - z - 1)
                         for z in range(max(m - 2, 0))]
            ensure(nonlocal_pairs == predicted, (a, "nonlocal completeness"))
            # Test the predicted distance distribution for ALL two-path Lagrange fibres.
            fibre_gaps = Counter(abs(order.rank(paths[0]) - order.rank(paths[1]))
                                 for paths in fibres.values() if len(paths) == 2)
            gap_expected = Counter({1: stats["lagrange_tied_matching_covers"]})
            gap_expected.update({distance: distance for distance in range(2, m + 1)})
            ensure(fibre_gaps == gap_expected, (a, "within-fibre gap distribution"))
            for runs in actual:
                value = lag[runs]
                record = [a, list(runs), value.numerator, value.denominator, level[value]]
                lag_hash.update(json.dumps(record, separators=(",", ":")).encode() + b"\n")
            result["lagrange_paths"] += len(actual)
            result["lagrange_levels"] += len(unique)
            result["fully_checked_cover_comparisons"] += len(actual) - 1
            result["fully_checked_discordant_pairs"] += crossed
        if a in (4, 5, 7, 8, 10, 11, 31):
            examples.append({"a": a, **order.statistics(a)})

    # These huge endpoints test the arithmetic formula, not mathematical universality.
    large_round_trips = 0
    for a in (10**30 + 1, 10**100 + 1, 10**1000 + 1):
        m, _ = order.endpoint(a)
        candidates = {0, 1, order.total(a) - 1, order.total(a) // 2}
        for z in (0, 1, m // 2, m - 1, m):
            start = order.layer_start(a, z)
            candidates.update((start, start + a - 3 * z - 1))
        for j in sorted(candidates):
            ensure(order.rank(order.unrank(a, j)) == j, "large arithmetic round trip")
            large_round_trips += 1
    bad_calls = [lambda: order.endpoint(3), lambda: order.endpoint(6),
                 lambda: order.endpoint(True), lambda: order.rank((0, 1, 3)),
                 lambda: order.rank((4, -1, 1)), lambda: order.rank((4, 0)),
                 lambda: order.rank((4.0, 0, 0)), lambda: order.unrank(4, -1),
                 lambda: order.unrank(4, 5), lambda: order.covers((4, 0, 0), (5, 0, 0))]
    reference = list(order.chain(8))
    for mutated in (reference[:-1], reference + reference[:1],
                    [reference[1], reference[0]] + reference[2:]):
        reject(lambda mutated=mutated: check_chain(mutated, reference))
    for call in bad_calls:
        reject(call)
    result.update(matching_records_sha256=match_hash.hexdigest(),
                  lagrange_records_sha256=lag_hash.hexdigest(),
                  large_integer_round_trips=large_round_trips,
                  rejected_malformed_cases=len(bad_calls) + 3,
                  symbolic=identities.audit(), examples=examples)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-a", type=int, default=120)
    parser.add_argument("--lagrange-max-a", type=int, default=40)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    result = audit(args.max_a, args.lagrange_max_a)
    if args.check:
        expected = json.loads(Path(__file__).with_name("EXPECTED.json").read_text())
        ensure(result == expected, "expected results differ")
    print(json.dumps(result, indent=2, sort_keys=True))
    print("PASS: complete order, arithmetic ranks, all covers, exact Lagrange comparisons, and universal identities")


if __name__ == "__main__":
    main()
