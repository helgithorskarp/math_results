#!/usr/bin/env python3
"""Independent checks for the quadratic-box upper-bound certificate."""

from __future__ import annotations

import argparse
from itertools import product
import json
import subprocess

from run_shards import merge, run_one


KNOWN = {16: 927, 18: 3160}
PYTHON_BOUNDS = {(16, 3): 1135, (18, 3): 3862, (20, 4): 15157}
CPP_BOUNDS = {
    (16, 3): (1135, 10, 40),
    (18, 3): (3862, 31, 124),
    (20, 4): (15157, 31, 248),
    (22, 4): (51006, 142, 1136),
    (24, 4): (180421, 967, 7736),
    (26, 5): (713229, 967, 15472),
    (28, 5): (2538272, 10723, 171568),
}


def conv(left: list[int], right: list[int], index: int) -> int:
    return sum(left[j] * right[index - 1 - j] for j in range(index))


def condition_values(left: list[int], right: list[int], n: int) -> list[int]:
    values = [0] * n
    sides = [0] * n
    parameter = [[0] * (i + 1) for i in range((n + 1) // 2)]
    for i in range(len(parameter)):
        parameter[i][i] = 1
    for index in range(len(left)):
        for j in range(index):
            for k in range(j - 1, -1, -1):
                parameter[j][k] = sum(
                    (right[j - ell - 1] if sides[n - index + ell - 1]
                     else left[j - ell - 1]) * parameter[ell][k]
                    for ell in range(k, j)
                )
        position = n - index - 2
        value = right[index] - left[index]
        for j in range(index):
            inner = sum(
                parameter[j][ell] * (right[ell] - left[ell])
                for ell in range(j + 1)
            )
            factor = (right[index - j - 1]
                      if sides[n - index + j - 1]
                      else left[index - j - 1])
            value += inner * factor
        values[position] = value
        sides[position] = int(value >= 0)
    return values


def extend_lower(prefix_l: list[int], prefix_r: list[int], n: int,
                 free_layers: int, values: list[int]) -> tuple[list[int], list[int]]:
    m = n // 2
    start = m - free_layers + 1
    assert len(prefix_l) == len(prefix_r) == start - 1
    left = prefix_l.copy()
    right = prefix_r.copy()
    for value in values:
        index = len(left)
        total = conv(left, right, index)
        left.append(value)
        right.append(total - value)
    return left, right


def forced_score(prefix_l: list[int], prefix_r: list[int], n: int,
                 free_layers: int, values: list[int], mask: int) -> int:
    m = n // 2
    left, right = extend_lower(prefix_l, prefix_r, n, free_layers, values)
    assert len(left) == m
    fixed_conditions = condition_values(prefix_l, prefix_r, n)
    left += [0] * (n - 1 - len(left))
    right += [0] * (n - 1 - len(right))
    for index in range(m, n - 1):
        total = conv(left, right, index)
        bit = index - m
        choose_left = ((mask >> bit) & 1) != 0 if bit < free_layers - 1 \
            else fixed_conditions[index] > 0
        if choose_left:
            left[index] = total
        else:
            right[index] = total
    return conv(left, right, n - 1)


def actual_score(lower_l: list[int], lower_r: list[int], n: int) -> int:
    m = n // 2
    assert len(lower_l) == len(lower_r) == m
    conditions = condition_values(lower_l, lower_r, n)
    left = lower_l + [0] * (n - 1 - m)
    right = lower_r + [0] * (n - 1 - m)
    for index in range(m, n - 1):
        total = conv(left, right, index)
        if conditions[index] > 0:
            left[index] = total
        else:
            right[index] = total
    return conv(left, right, n - 1)


def interpolate(prefix_l: list[int], prefix_r: list[int], n: int,
                free_layers: int, mask: int) -> dict[str, object]:
    zero = [0] * free_layers
    constant = forced_score(prefix_l, prefix_r, n, free_layers, zero, mask)
    linear = [0] * free_layers
    diagonal = [0] * free_layers
    first = [0] * free_layers
    for i in range(free_layers):
        one = zero.copy()
        one[i] = 1
        two = zero.copy()
        two[i] = 2
        f1 = forced_score(prefix_l, prefix_r, n, free_layers, one, mask)
        f2 = forced_score(prefix_l, prefix_r, n, free_layers, two, mask)
        numerator = f2 - 2 * f1 + constant
        assert numerator % 2 == 0
        diagonal[i] = numerator // 2
        linear[i] = f1 - constant - diagonal[i]
        first[i] = f1
    cross = [[0] * free_layers for _ in range(free_layers)]
    for i in range(free_layers):
        cross[i][i] = diagonal[i]
        for j in range(i + 1, free_layers):
            pair = zero.copy()
            pair[i] = pair[j] = 1
            fij = forced_score(prefix_l, prefix_r, n, free_layers, pair, mask)
            cross[i][j] = fij - first[i] - first[j] + constant
    return {"constant": constant, "linear": linear, "quadratic": cross}


def evaluate_poly(poly: dict[str, object], values: list[int]) -> int:
    linear = poly["linear"]
    quadratic = poly["quadratic"]
    assert isinstance(linear, list) and isinstance(quadratic, list)
    answer = int(poly["constant"])
    for i, value in enumerate(values):
        answer += int(linear[i]) * value
        for j in range(i, len(values)):
            answer += int(quadratic[i][j]) * value * values[j]
    return answer


def free_highs(prefix_l: list[int], prefix_r: list[int], n: int,
               free_layers: int) -> list[int]:
    highs: list[int] = []
    for variable in range(free_layers):
        zero = [0] * variable
        constant = conv(*extend_lower(
            prefix_l, prefix_r, n, free_layers, zero
        ), len(prefix_l) + variable)
        coefficients = []
        for j in range(variable):
            unit = zero.copy()
            unit[j] = 1
            total = conv(*extend_lower(
                prefix_l, prefix_r, n, free_layers, unit
            ), len(prefix_l) + variable)
            coefficients.append(total - constant)
        high = constant + sum(max(0, a * h) for a, h in zip(coefficients, highs))
        assert high >= 0
        highs.append(high)
    return highs


def floor_div(a: int, b: int) -> int:
    return a // b


def univariate_max(a: int, b: int, high: int) -> int:
    values = [0, a * high * high + b * high]
    if a < 0:
        below = floor_div(-b, 2 * a)
        for point in (below, below + 1):
            point = max(0, min(high, point))
            values.append(a * point * point + b * point)
    return max(values)


def box_upper(poly: dict[str, object], highs: list[int]) -> int:
    linear = poly["linear"]
    quadratic = poly["quadratic"]
    assert isinstance(linear, list) and isinstance(quadratic, list)
    answer = int(poly["constant"])
    for i, high in enumerate(highs):
        answer += univariate_max(int(quadratic[i][i]), int(linear[i]), high)
        for j in range(i + 1, len(highs)):
            answer += max(0, int(quadratic[i][j]) * high * highs[j])
    return answer


def enumerate_prefixes(n: int, free_layers: int):
    m = n // 2
    stop = m - free_layers

    def visit(left: list[int], right: list[int]):
        level = len(left)
        if level == stop:
            yield left, right
            return
        total = 2 if level == 0 else conv(left, right, level)
        minimum = 1 if level == 0 else 0
        maximum = total
        if all(a == b for a, b in zip(left, right)):
            maximum //= 2
        for value in range(minimum, maximum + 1):
            yield from visit(left + [value], right + [total - value])

    yield from visit([], [])


def enumerate_free(prefix_l: list[int], prefix_r: list[int], n: int,
                   free_layers: int):
    def visit(values: list[int]):
        if len(values) == free_layers:
            yield values
            return
        left, right = extend_lower(prefix_l, prefix_r, n, free_layers, values)
        total = conv(left, right, len(left))
        for value in range(total + 1):
            yield from visit(values + [value])
    yield from visit([])


def python_bound(n: int, free_layers: int,
                 exhaustive_grid: bool) -> dict[str, int]:
    best_upper = -1
    best_actual = -1
    prefix_count = 0
    polynomial_count = 0
    grid_points = 0
    for prefix_l, prefix_r in enumerate_prefixes(n, free_layers):
        prefix_count += 1
        highs = free_highs(prefix_l, prefix_r, n, free_layers)
        polynomials = []
        local_upper = -1
        for mask in range(1 << (free_layers - 1)):
            poly = interpolate(prefix_l, prefix_r, n, free_layers, mask)
            polynomials.append(poly)
            local_upper = max(local_upper, box_upper(poly, highs))
            polynomial_count += 1
        best_upper = max(best_upper, local_upper)

        if exhaustive_grid:
            for values in enumerate_free(prefix_l, prefix_r, n, free_layers):
                grid_points += 1
                assert all(0 <= value <= high for value, high in zip(values, highs))
                lower_l, lower_r = extend_lower(
                    prefix_l, prefix_r, n, free_layers, values
                )
                actual = actual_score(lower_l, lower_r, n)
                best_actual = max(best_actual, actual)
                assert actual <= local_upper
                for mask, poly in enumerate(polynomials):
                    assert evaluate_poly(poly, values) == forced_score(
                        prefix_l, prefix_r, n, free_layers, values, mask
                    )
    expected = PYTHON_BOUNDS[n, free_layers]
    assert best_upper == expected
    if exhaustive_grid:
        assert best_actual == KNOWN[n]
    return {
        "n": n,
        "free_layers": free_layers,
        "upper_bound": best_upper,
        "prefixes": prefix_count,
        "polynomials": polynomial_count,
        "feasible_grid_points": grid_points,
        "exact_value": best_actual,
    }


def generic_box_checks() -> int:
    checked = 0
    for h0, h1 in product(range(5), repeat=2):
        for l0, l1 in product(range(-3, 4), repeat=2):
            for q0, q1 in product(range(-3, 3), repeat=2):
                for cross in range(-3, 4):
                    poly = {
                        "constant": 7,
                        "linear": [l0, l1],
                        "quadratic": [[q0, cross], [0, q1]],
                    }
                    upper = box_upper(poly, [h0, h1])
                    assert all(
                        evaluate_poly(poly, [x, y]) <= upper
                        for x in range(h0 + 1) for y in range(h1 + 1)
                    )
                    checked += 1
    assert checked == 308700
    return checked


def parse_cpp(binary: str, n: int, free_layers: int) -> dict[str, int]:
    completed = subprocess.run(
        [binary, str(n), str(free_layers)],
        check=True,
        capture_output=True,
        text=True,
    )
    fields: dict[str, int] = {}
    for line in completed.stdout.splitlines():
        key, _, value = line.partition(" ")
        if key in {
            "n", "free_layers", "start_level", "upper_bound", "shard",
            "shards", "prefixes_seen", "prefixes_evaluated",
            "orientation_polynomials", "positive_cross_terms",
            "maximizing_mask",
        }:
            fields[key] = int(value)
    return fields


def verify_cpp(binary: str) -> list[dict[str, int]]:
    records = []
    for (n, free_layers), expected in CPP_BOUNDS.items():
        fields = parse_cpp(binary, n, free_layers)
        bound, prefixes, polynomials = expected
        assert fields["upper_bound"] == bound
        assert fields["prefixes_seen"] == fields["prefixes_evaluated"] == prefixes
        assert fields["orientation_polynomials"] == polynomials
        assert fields["positive_cross_terms"] == 0
        records.append(fields)

    mono = run_one(binary, 18, 3, 0, 1)
    shards = [run_one(binary, 18, 3, shard, 3) for shard in range(3)]
    merged = merge(shards, 18, 3, 3)
    assert merged["upper_bound"] == mono["upper_bound"] == 3862
    assert merged["prefixes_evaluated"] == mono["prefixes_evaluated"] == 31
    assert merged["orientation_polynomials"] == mono["orientation_polynomials"] == 124
    return records


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--binary")
    args = parser.parse_args()
    result: dict[str, object] = {
        "status": "PASS",
        "generic_boxes_checked": generic_box_checks(),
        "python_records": [
            python_bound(16, 3, True),
            python_bound(18, 3, True),
            python_bound(20, 4, False),
        ],
    }
    if args.binary:
        result["cpp_records"] = verify_cpp(args.binary)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
