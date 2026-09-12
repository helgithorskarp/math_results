#!/usr/bin/env python3
"""Definition-level checks for the even-length middle-quadratic theorem.

This deliberately uses Python arbitrary-precision integers and enumerates
every middle split on small complete SQN trees.  It does not call or parse the
C++ implementation.
"""

from __future__ import annotations

import argparse
import json
import subprocess


KNOWN_BINARY = {
    4: 1,
    6: 3,
    8: 8,
    10: 24,
    12: 81,
    14: 274,
    16: 927,
    18: 3160,
    20: 11272,
}

EXPECTED_CPP = {
    10: (24, 4, 10, 4),
    12: (81, 10, 31, 13),
    14: (274, 31, 142, 31),
    16: (927, 142, 967, 151),
    18: (3160, 967, 10723, 967),
    20: (11272, 10723, 192656, 11968),
    22: (40202, 192656, 6001931, 192656),
    24: (147312, 6001931, 321286030, 6706281),
}


def convolution_at(left: list[int], right: list[int], index: int) -> int:
    """Return sum(left[j]*right[index-1-j], j=0,...,index-1)."""
    return sum(left[j] * right[index - 1 - j] for j in range(index))


def condition_values(
    prefix_left: list[int], prefix_right: list[int], n: int
) -> list[int]:
    """Reimplement the published backwards upper-orientation condition."""
    conditions = [0] * n
    sides = [0] * n
    parameter = [[0] * (i + 1) for i in range((n + 1) // 2)]
    for i, row in enumerate(parameter):
        row[i] = 1

    for index in range(len(prefix_left)):
        for j in range(index):
            for k in range(j - 1, -1, -1):
                parameter[j][k] = sum(
                    (
                        prefix_right[j - ell - 1]
                        if sides[n - index + ell - 1]
                        else prefix_left[j - ell - 1]
                    )
                    * parameter[ell][k]
                    for ell in range(k, j)
                )

        position = n - index - 2
        value = prefix_right[index] - prefix_left[index]
        for j in range(index):
            inner = sum(
                parameter[j][ell]
                * (prefix_right[ell] - prefix_left[ell])
                for ell in range(j + 1)
            )
            factor = (
                prefix_right[index - j - 1]
                if sides[n - index + j - 1]
                else prefix_left[index - j - 1]
            )
            value += inner * factor
        conditions[position] = value
        sides[position] = int(value >= 0)
    return conditions


def complete_and_score(
    prefix_left: list[int], prefix_right: list[int], n: int, middle_left: int
) -> tuple[int, tuple[int, ...], tuple[int, ...]]:
    """Complete one middle split using the published optimal upper rule."""
    middle = n // 2
    left = prefix_left + [0] * (n - 1 - len(prefix_left))
    right = prefix_right + [0] * (n - 1 - len(prefix_right))
    conditions = condition_values(prefix_left, prefix_right, n)
    middle_total = convolution_at(left, right, middle - 1)
    assert 0 <= middle_left <= middle_total
    left[middle - 1] = middle_left
    right[middle - 1] = middle_total - middle_left

    for index in range(middle, n - 1):
        total = convolution_at(left, right, index)
        if conditions[index] > 0:
            left[index] = total
        else:
            right[index] = total
    return convolution_at(left, right, n - 1), tuple(left), tuple(right)


def vertex_candidates(total: int, value_zero: int, value_one: int) -> tuple[int, ...]:
    """Return all possible integer maximizers of -t^2+B*t+C on [0,total]."""
    assert total >= 1
    coefficient = value_one - value_zero + 1
    if coefficient <= 0:
        return (0,)
    if coefficient >= 2 * total:
        return (total,)
    lower = coefficient // 2
    upper = (coefficient + 1) // 2
    return tuple(sorted({lower, upper}))


def verify_even_length(n: int) -> dict[str, int]:
    """Exhaust the binary lower-prefix tree and every middle split."""
    assert n >= 4 and n % 2 == 0
    middle = n // 2
    best_original = -1
    best_compressed = -1
    prefixes = 0
    original_leaves = 0
    compressed_evaluations = 0
    quadratic_checks = 0

    def visit(left: list[int], right: list[int]) -> None:
        nonlocal best_original, best_compressed, prefixes
        nonlocal original_leaves, compressed_evaluations, quadratic_checks
        current_level = len(left)
        if current_level == middle - 1:
            prefixes += 1
            total = convolution_at(left, right, middle - 1)
            values = [
                complete_and_score(left, right, n, t)[0]
                for t in range(total + 1)
            ]
            original_leaves += len(values)
            for t in range(total - 1):
                assert values[t + 2] - 2 * values[t + 1] + values[t] == -2
                quadratic_checks += 1

            if total == 0:
                candidates = (0,)
            else:
                candidates = vertex_candidates(total, values[0], values[1])
            candidate_values = [values[t] for t in candidates]
            compressed_evaluations += len(candidates)
            assert max(candidate_values) == max(values)
            best_original = max(best_original, max(values))
            best_compressed = max(best_compressed, max(candidate_values))
            return

        total = 2 if current_level == 0 else convolution_at(
            left, right, current_level
        )
        minimum = 1 if current_level == 0 else 0
        maximum = total
        if all(a == b for a, b in zip(left, right)):
            maximum = total // 2
        for value in range(minimum, maximum + 1):
            visit(left + [value], right + [total - value])

    visit([], [])
    assert best_original == best_compressed == KNOWN_BINARY[n]
    return {
        "n": n,
        "best": best_original,
        "prefixes": prefixes,
        "original_middle_leaves": original_leaves,
        "compressed_middle_evaluations": compressed_evaluations,
        "quadratic_second_differences_checked": quadratic_checks,
    }


def verify_cpp(binary: str) -> list[dict[str, int]]:
    """Check deterministic C++ summaries and their displayed SQN witnesses."""
    records = []
    for n, expected in EXPECTED_CPP.items():
        completed = subprocess.run(
            [binary, str(n)], check=True, capture_output=True, text=True
        )
        fields: dict[str, str] = {}
        for line in completed.stdout.splitlines():
            key, _, value = line.partition(" ")
            fields[key] = value
        actual = tuple(
            int(fields[key])
            for key in (
                "best",
                "prefixes",
                "original_middle_leaves",
                "vertex_candidates",
            )
        )
        assert actual == expected, (n, actual, expected)
        assert int(fields["quadratic_leading_checks"]) == actual[1]

        left = tuple(map(int, fields["L"].split()))
        right = tuple(map(int, fields["R"].split()))
        assert len(left) == len(right) == n - 1
        assert left[0] + right[0] == 2
        assert left[0] > 0 and right[0] > 0
        for index in range(1, n - 1):
            total = sum(left[j] * right[index - 1 - j] for j in range(index))
            assert left[index] + right[index] == total
        objective = sum(left[j] * right[n - 2 - j] for j in range(n - 1))
        assert objective == actual[0]
        assert all(
            left[i] == 0 or right[i] == 0 for i in range(n // 2, n - 1)
        )
        records.append(
            {
                "n": n,
                "best": actual[0],
                "prefixes": actual[1],
                "original_middle_leaves": actual[2],
                "vertex_candidates": actual[3],
            }
        )
    return records


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--binary", help="also verify the compiled C++ enumerator")
    args = parser.parse_args()
    records = [verify_even_length(n) for n in sorted(KNOWN_BINARY)]
    result: dict[str, object] = {"status": "PASS", "reference_records": records}
    if args.binary:
        result["cpp_records"] = verify_cpp(args.binary)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
