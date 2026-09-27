#!/usr/bin/env python3
"""Independent exact audit of loss-proportional paired Gaussian cubature."""

import argparse
from collections import Counter
from fractions import Fraction as F
from functools import lru_cache
from hashlib import sha256
from itertools import combinations_with_replacement
import json
from math import comb, factorial
from pathlib import Path


HERE = Path(__file__).resolve().parent


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def ceiling(q):
    return (q.numerator + q.denominator - 1) // q.denominator


def decimal_upper(q, places=18):
    """Compact outward decimal upper bound for a nonnegative rational."""
    require(q >= 0, "negative decimal bound")
    scale = 10 ** places
    numerator = ceiling(q * scale)
    return f"{numerator // scale}.{numerator % scale:0{places}d}"


def pins():
    manifest = json.loads((HERE / "TARGET_INPUTS.json").read_text())
    require(manifest["schema"] == 1, "manifest schema")
    for relative, expected in manifest["files"].items():
        actual = sha256((HERE / relative).read_bytes()).hexdigest()
        require(actual == expected, f"changed target or dependency: {relative}")
    return manifest


@lru_cache(maxsize=None)
def exp_neg(q, bits):
    """Dyadic enclosure of exp(-q) from a positive exp(q) series."""
    require(q >= 0 and bits >= 32, "invalid exponential request")
    scale = 1 << bits
    if q == 0:
        return scale, scale
    total = term = F(1)
    n = 0
    while True:
        n += 1
        term *= q / n
        total += term
        next_term = term * q / (n + 1)
        ratio = q / (n + 2)
        if ratio < 1:
            remainder = next_term / (1 - ratio)
            low = int(scale / (total + remainder))
            high = ceiling(F(scale, 1) / total)
            if high - low <= 2:
                return low, high


def sqrt_bounds(q, bits):
    scale = 1 << bits
    bound = q.numerator * scale * scale
    low, high = 0, 1
    while high * high * q.denominator <= bound:
        low, high = high, 2 * high
    while high - low > 1:
        middle = (low + high) // 2
        if middle * middle * q.denominator <= bound:
            low = middle
        else:
            high = middle
    lower = F(low, scale)
    upper = lower if lower * lower == q else F(high, scale)
    require(lower * lower <= q <= upper * upper, "square-root enclosure")
    return lower, upper


def scale_interval(interval, factor):
    low, high = interval
    return (low * factor, high * factor) if factor >= 0 else (high * factor, low * factor)


def add_intervals(first, second):
    return first[0] + second[0], first[1] + second[1]


def exp_linear(terms, bits=180):
    low = high = F(0)
    for value, coefficient in terms.items():
        if not coefficient:
            continue
        a, b = exp_neg(value, bits)
        interval = scale_interval((F(a, 1 << bits), F(b, 1 << bits)), coefficient)
        low += interval[0]
        high += interval[1]
    return low, high


def divide_by_sqrt(interval, integer, rational_factor):
    root_low, root_high = sqrt_bounds(F(integer), 180)
    denominators = (rational_factor * root_low, rational_factor * root_high)
    values = [numerator / denominator for numerator in interval for denominator in denominators]
    return min(values), max(values)


def taylor(value, degree):
    return sum(((-value) ** power / factorial(power)
                for power in range(degree + 1)), F(0))


def beta_width(row, half_degree, epsilon):
    values = []
    for index in range(row + 1):
        total = sum(comb(row - index, shift)
                    * (index + shift + 2) ** (half_degree - 2)
                    for shift in range(row - index + 1))
        values.append(comb(row, index) * total)
    return (F(row + 1, 4 * factorial(half_degree))
            * (epsilon / 2) ** half_degree * max(values))


def select_degree(row, epsilon, bits):
    target = F(1, 1 << bits)
    degree = max(2, ceiling(F(row + 2) * epsilon / 2))
    while beta_width(row, degree, epsilon) > target:
        degree += 1
    return degree


def feature(source, target, degree):
    return ((F(1),)
            + tuple(source ** power for power in range(1, degree + 1))
            + tuple(target ** power for power in range(1, degree + 1)))


def null_vector(vectors):
    """Exact null vector for columns, via an independently written RREF."""
    rows = len(vectors[0])
    columns = len(vectors)
    matrix = [[F(vectors[column][row]) for column in range(columns)]
              for row in range(rows)]
    pivot_columns = []
    pivot_row = 0
    for column in range(columns):
        pivot = next((row for row in range(pivot_row, rows)
                      if matrix[row][column]), None)
        if pivot is None:
            continue
        matrix[pivot_row], matrix[pivot] = matrix[pivot], matrix[pivot_row]
        value = matrix[pivot_row][column]
        matrix[pivot_row] = [entry / value for entry in matrix[pivot_row]]
        for row in range(rows):
            if row != pivot_row and matrix[row][column]:
                value = matrix[row][column]
                matrix[row] = [entry - value * base
                               for entry, base in zip(matrix[row], matrix[pivot_row])]
        pivot_columns.append(column)
        pivot_row += 1
        if pivot_row == rows:
            break
    free = next((column for column in range(columns)
                 if column not in pivot_columns), None)
    require(free is not None, "columns are independent")
    answer = [F(0)] * columns
    answer[free] = F(1)
    # The selected free column can lie to the left of later pivots.  Since the
    # matrix is in reduced row-echelon form, read every pivot coordinate
    # directly from that free column.
    for row, column in enumerate(pivot_columns):
        answer[column] = -matrix[row][free]
    require(any(answer) and all(sum(answer[column] * vectors[column][row]
                                    for column in range(columns)) == 0
                                for row in range(rows)), "null-vector reconstruction")
    return answer


def compress(sources, targets, weights, degree):
    vectors = [feature(source, target, degree)
               for source, target in zip(sources, targets)]
    active = [index for index, weight in enumerate(weights) if weight]
    current = list(weights)
    cap = len(vectors[0])
    while len(active) > cap:
        chosen = active[:cap + 1]
        direction = null_vector([vectors[index] for index in chosen])
        if not any(value > 0 for value in direction):
            direction = [-value for value in direction]
        step = min(current[index] / value
                   for index, value in zip(chosen, direction) if value > 0)
        for index, value in zip(chosen, direction):
            current[index] -= step * value
            require(current[index] >= 0, "negative cubature weight")
        active = [index for index in active if current[index]]
    retained = [current[index] for index in active]
    require(sum(retained) == 1 and len(active) <= cap, "cubature support")
    for power in range(degree + 1):
        require(sum(weight * source ** power for source, weight in zip(sources, weights))
                == sum(weight * sources[index] ** power
                       for index, weight in zip(active, retained)),
                "source moment")
        require(sum(weight * target ** power for target, weight in zip(targets, weights))
                == sum(weight * targets[index] ** power
                       for index, weight in zip(active, retained)),
                "target moment")
    return active, retained


def variance(sites, weights):
    mean = sum(weight * site for site, weight in zip(sites, weights))
    return sum(weight * site * site for site, weight in zip(sites, weights)) - mean * mean


def pair_loss(sources, targets, weights):
    direct = sum(weights[i] * weights[j]
                 * ((sources[i] - sources[j]) ** 2 - (targets[i] - targets[j]) ** 2)
                 for i in range(len(sources)) for j in range(len(sources)))
    covariance = 2 * (variance(sources, weights) - variance(targets, weights))
    require(direct == covariance >= 0, "loss normalization")
    return direct


def scatter_histogram(sites, weights, replicas):
    result = Counter()
    for indices in combinations_with_replacement(range(len(sites)), replicas):
        counts = Counter(indices)
        multiplicity = factorial(replicas)
        probability = F(1)
        for index, count in counts.items():
            multiplicity //= factorial(count)
            probability *= weights[index] ** count
        total = sum(sites[index] for index in indices)
        scatter = (sum(sites[index] ** 2 for index in indices)
                   - total * total / replicas) / 2
        result[scatter] += multiplicity * probability
    require(sum(result.values()) == 1 and min(result) >= 0, "scatter histogram")
    return result


def a_difference_interval(source_mu, target_mu, source_nu, target_nu, replicas):
    terms = Counter()
    for histogram, sign in ((target_mu, 1), (source_mu, -1),
                            (target_nu, -1), (source_nu, 1)):
        for value, probability in histogram.items():
            terms[value] += sign * probability
    numerator = exp_linear(terms)
    return divide_by_sqrt(numerator, replicas,
                          F(replicas ** 2 * (replicas - 1)))


def finite_law_controls():
    sources = [F(index, 10) for index in range(-9, 10)]
    weights = [F(index + 1, 190) for index in range(19)]
    epsilon = F(81, 100)
    half_degree = 2
    degree = 2 * half_degree
    rows = []
    stream = sha256()
    total_polynomial_checks = total_moment_checks = 0
    for contraction in (F(3, 4), F(1023, 1024), F((1 << 30) - 1, 1 << 30)):
        targets = [source if source >= 0 else contraction * source for source in sources]
        require(all(abs(targets[i] - targets[j]) <= abs(sources[i] - sources[j])
                    for i in range(19) for j in range(19)), "map contraction")
        active, retained = compress(sources, targets, weights, degree)
        source_nu = [sources[index] for index in active]
        target_nu = [targets[index] for index in active]
        loss_mu = pair_loss(sources, targets, weights)
        loss_nu = pair_loss(source_nu, target_nu, retained)
        require(loss_mu == loss_nu > 0, "cubature loss preservation")
        total_moment_checks += 2 * (degree + 1)

        a_intervals = {}
        maximum_ratio = F(0)
        for replicas in range(2, 5):
            source_mu_hist = scatter_histogram(sources, weights, replicas)
            target_mu_hist = scatter_histogram(targets, weights, replicas)
            source_nu_hist = scatter_histogram(source_nu, retained, replicas)
            target_nu_hist = scatter_histogram(target_nu, retained, replicas)
            for power in range(half_degree + 1):
                source_mu_moment = sum(probability * value ** power
                                       for value, probability in source_mu_hist.items())
                source_nu_moment = sum(probability * value ** power
                                       for value, probability in source_nu_hist.items())
                target_mu_moment = sum(probability * value ** power
                                       for value, probability in target_mu_hist.items())
                target_nu_moment = sum(probability * value ** power
                                       for value, probability in target_nu_hist.items())
                require(source_mu_moment == source_nu_moment
                        and target_mu_moment == target_nu_moment,
                        "replica polynomial moment")
                total_polynomial_checks += 2
            polynomial_difference = F(0)
            for histogram, sign in ((target_mu_hist, 1), (source_mu_hist, -1),
                                    (target_nu_hist, -1), (source_nu_hist, 1)):
                polynomial_difference += sign * sum(
                    probability * taylor(value, half_degree)
                    for value, probability in histogram.items())
            require(polynomial_difference == 0, "common Taylor polynomial part")
            interval = a_difference_interval(source_mu_hist, target_mu_hist,
                                             source_nu_hist, target_nu_hist, replicas)
            a_intervals[replicas - 2] = interval
            absolute_upper = max(abs(interval[0]), abs(interval[1]))
            root_upper = sqrt_bounds(F(replicas), 180)[1]
            theorem_lower = (loss_mu * (F(replicas) * epsilon / 2) ** half_degree
                             / (4 * replicas ** 2 * root_upper * factorial(half_degree)))
            require(absolute_upper <= theorem_lower, "loss-proportional moment error")
            maximum_ratio = max(maximum_ratio, absolute_upper / loss_mu)

        beta_maximum = F(0)
        row = 2
        for index in range(row + 1):
            interval = (F(0), F(0))
            for shift in range(row - index + 1):
                coefficient = ((row + 1) * comb(row, index)
                               * (-1) ** shift * comb(row - index, shift))
                interval = add_intervals(
                    interval, scale_interval(a_intervals[index + shift], coefficient))
            beta_maximum = max(beta_maximum,
                               max(abs(interval[0]), abs(interval[1])) / loss_mu)
            stream.update(f"{contraction}:{index}:{interval}\n".encode())
        theorem_beta = beta_width(row, half_degree, epsilon)
        require(beta_maximum <= theorem_beta, "loss-proportional beta error")
        rows.append({
            "negative_side_contraction": str(contraction),
            "loss": str(loss_mu),
            "retained_atoms": len(active),
            "maximum_normalized_a_error_upper_decimal": decimal_upper(maximum_ratio),
            "maximum_normalized_beta_error_upper_decimal": decimal_upper(beta_maximum),
            "theorem_normalized_beta_bound_decimal": decimal_upper(theorem_beta),
        })
    return {
        "original_atoms": len(sources),
        "feature_count": 2 * (degree + 1) - 1,
        "matched_moment_checks": total_moment_checks,
        "replica_polynomial_moment_checks": total_polynomial_checks,
        "interval_stream_sha256": stream.hexdigest(),
        "controls": rows,
    }


def scalar_and_budget_controls():
    scalar_checks = 0
    grid = [F(0), F(1, 32), F(1, 8), F(1, 2), F(1), F(3)]
    for degree in range(2, 10):
        for low in grid:
            for high in grid:
                if low > high:
                    continue
                terms = Counter()
                terms[low] += 1
                terms[high] -= 1
                remainder = exp_linear(terms)
                polynomial = taylor(high, degree) - taylor(low, degree)
                signed = scale_interval(add_intervals(remainder, (polynomial, polynomial)),
                                        (-1) ** degree)
                upper = (high - low) * high ** degree / factorial(degree)
                require(F(0) <= signed[0] <= signed[1] <= upper,
                        "signed Taylor remainder")
                scalar_checks += 1

    schedules = []
    for row, epsilon, bits, expected in (
        (8, F(1, 2), 10, 12),
        (32, F(1, 2), 10, 42),
        (64, F(1, 2), 20, 86),
        (8, F(4), 10, 59),
        (32, F(9), 10, 434),
    ):
        selected = select_degree(row, epsilon, bits)
        require(selected == expected, "degree schedule")
        schedules.append({
            "row": row,
            "radius_ratio": str(epsilon),
            "error_bits": bits,
            "selected_half_degree": selected,
            "atoms": 2 * comb(2 * selected + 3, 3) - 1,
            "relative_beta_bound_upper_decimal": decimal_upper(
                beta_width(row, selected, epsilon)),
        })

    ratio_checks = 0
    for row in range(9):
        for degree in range(2, 16):
            for epsilon in (F(0), F(1, 16), F(1, 2), F(2)):
                current = beta_width(row, degree, epsilon)
                following = beta_width(row, degree + 1, epsilon)
                factor = F(row + 2) * epsilon / (2 * (degree + 1))
                require(following <= factor * current, "degree monotonicity")
                ratio_checks += 1
    return scalar_checks, ratio_checks, schedules


def audit():
    manifest = pins()
    scalar_checks, ratio_checks, schedules = scalar_and_budget_controls()
    finite = finite_law_controls()
    dimensions = {
        str(degree): 2 * comb(2 * degree + 3, 3) - 1
        for degree in (2, 12, 42, 86)
    }
    require(dimensions == {"2": 69, "12": 5849, "42": 211989, "86": 1755949},
            "Caratheodory dimensions")
    return {
        "status": "INDEPENDENT_LOSS_CUBATURE_REVIEW_PASS",
        "target_commit": manifest["target_commit"],
        "target_graph_ref": manifest["target_graph_ref"],
        "pinned_files": len(manifest["files"]),
        "method": "independent RREF cubature, definition-level replica histograms, positive-series exponential enclosures, linear degree search",
        "signed_taylor_interval_checks": scalar_checks,
        "degree_ratio_checks": ratio_checks,
        "caratheodory_atom_counts": dimensions,
        "degree_schedules": schedules,
        "finite_law_controls": finite,
        "verdict": "accept the loss-proportional beta and conditional full-curve transfer bounds; no new universal hinge sign follows",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--expected", type=Path, default=HERE / "REVIEW_EXPECTED.json")
    args = parser.parse_args()
    record = audit()
    if args.check:
        require(record == json.loads(args.expected.read_text()), "review record differs")
        print(record["status"])
    else:
        print(json.dumps(record, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
