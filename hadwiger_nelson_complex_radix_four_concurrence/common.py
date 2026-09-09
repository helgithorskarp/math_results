#!/usr/bin/env python3
"""Exact finite-field resultant machinery for the four-curve concurrence gate."""
from collections import Counter
from itertools import product
from math import comb
import hashlib
import json
import multiprocessing


WORKER_PRIME = None
WORKER_CURVES = None
WORKER_K = None


def need(condition, message):
    if not condition:
        raise ValueError(message)


def digest(value):
    return hashlib.sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


def is_prime(value):
    if value < 2:
        return False
    divisor = 2
    while divisor * divisor <= value:
        if value % divisor == 0:
            return False
        divisor += 1 if divisor == 2 else 2
    return True


def trim(poly):
    while poly and poly[-1] == 0:
        poly.pop()
    return poly


def divrem(left, right, prime):
    left, right = trim(left[:]), trim(right[:])
    need(right, "polynomial division by zero")
    inverse = pow(right[-1], -1, prime)
    while len(left) >= len(right) and left:
        scale = left[-1] * inverse % prime
        shift = len(left) - len(right)
        for i, value in enumerate(right):
            left[i + shift] = (left[i + shift] - scale * value) % prime
        trim(left)
    return left


def resultant_value(left, right, prime):
    """A nonzero scalar multiple convention for the univariate resultant."""
    left, right = trim(left[:]), trim(right[:])
    if not left or not right:
        return 0
    m, n = len(left) - 1, len(right) - 1
    if n == 0:
        return pow(right[0], m, prime)
    if m < n:
        sign = prime - 1 if (m * n) & 1 else 1
        return sign * resultant_value(right, left, prime) % prime
    remainder = divrem(left, right, prime)
    if not remainder:
        return 0
    degree = len(remainder) - 1
    sign = prime - 1 if ((m - degree) * n) & 1 else 1
    return (
        sign
        * pow(right[-1], m - degree, prime)
        * resultant_value(remainder, right, prime)
        % prime
    )


def evaluate_curve(curve, value, slope, prime):
    """Coefficients in y after x=value-slope*y, low degree first."""
    maximum = max(i + j for i, j, _ in curve)
    output = [0] * (maximum + 1)
    for i, j, coefficient in curve:
        for r in range(i + 1):
            output[j + r] += (
                coefficient
                * comb(i, r)
                * pow(value, i - r, prime)
                * pow(-slope, r, prime)
            )
    return trim([entry % prime for entry in output])


def interpolate_consecutive(values, prime):
    """Recover P from P(0),...,P(d) by Newton forward differences."""
    differences = [entry % prime for entry in values]
    deltas = []
    while differences:
        deltas.append(differences[0])
        differences = [
            (differences[i + 1] - differences[i]) % prime
            for i in range(len(differences) - 1)
        ]
    output = [0] * len(values)
    basis = [1]
    for k, delta in enumerate(deltas):
        for i, coefficient in enumerate(basis):
            output[i] = (output[i] + delta * coefficient) % prime
        if k + 1 < len(deltas):
            inverse = pow(k + 1, -1, prime)
            new = [0] * (len(basis) + 1)
            for i, coefficient in enumerate(basis):
                new[i] = (new[i] - k * coefficient * inverse) % prime
                new[i + 1] = (new[i + 1] + coefficient * inverse) % prime
            basis = new
    return trim(output)


def worker_init(curves, curve_k, prime):
    global WORKER_CURVES, WORKER_K, WORKER_PRIME
    WORKER_CURVES = curves
    WORKER_K = curve_k
    WORKER_PRIME = prime


def projected_resultant(pair, slope):
    """Monic Res_y(f(t-slope*y,y),g(t-slope*y,y)) modulo WORKER_PRIME."""
    bound = 2 * WORKER_K[pair[0]] * WORKER_K[pair[1]]
    values = []
    for value in range(bound + 1):
        left = evaluate_curve(WORKER_CURVES[pair[0]], value, slope, WORKER_PRIME)
        right = evaluate_curve(WORKER_CURVES[pair[1]], value, slope, WORKER_PRIME)
        need(len(left) - 1 == 2 * WORKER_K[pair[0]], "first eliminated-variable degree dropped")
        need(len(right) - 1 == 2 * WORKER_K[pair[1]], "second eliminated-variable degree dropped")
        values.append(resultant_value(left, right, WORKER_PRIME))
    result = interpolate_consecutive(values, WORKER_PRIME)
    need(
        len(result) - 1 == bound,
        f"projected resultant does not attain 2*k*l bound: {pair}, slope={slope}",
    )
    inverse = pow(result[-1], -1, WORKER_PRIME)
    return tuple(coefficient * inverse % WORKER_PRIME for coefficient in result)


def gcd_degree(left, right):
    left, right = list(left), list(right)
    while right:
        left, right = right, divrem(left, right, WORKER_PRIME)
    return len(left) - 1


def scan_normal(task):
    normal, left_pairs, right_pairs = task
    left = {pair: projected_resultant(pair, 2) for pair in left_pairs}
    right = {pair: projected_resultant(pair, 2) for pair in right_pairs}
    candidates = []
    histogram = Counter()
    for left_pair, right_pair in product(left_pairs, right_pairs):
        degree = gcd_degree(left[left_pair], right[right_pair])
        histogram[degree] += 1
        if degree:
            candidates.append(tuple(sorted(left_pair + right_pair)))
    evaluations = sum(len(poly) for poly in left.values()) + sum(
        len(poly) for poly in right.values()
    )
    return normal, tuple(candidates), dict(sorted(histogram.items())), evaluations


def build_tasks(buckets):
    tasks = []
    raw_quartets = 0
    for normal in sorted(buckets):
        sections = buckets[normal]
        if set(sections) != {0, 1, 2, 3}:
            continue
        left = tuple(product(sections[0], sections[1]))
        right = tuple(product(sections[2], sections[3]))
        raw_quartets += len(left) * len(right)
        tasks.append((normal, left, right))
    return tasks, raw_quartets


def run_sieve(factors, curve_k, curve_constant, buckets, prime, processes):
    need(is_prime(prime) and prime > 32, "modulus must be a prime larger than every interpolation degree")
    need(processes >= 1, "process count")
    tasks, raw_quartets = build_tasks(buckets)
    pair_inventory = [
        (normal, side, pair)
        for normal, left, right in tasks
        for side, pairs in enumerate((left, right))
        for pair in pairs
    ]
    if processes == 1:
        worker_init(factors, curve_k, prime)
        results = list(map(scan_normal, tasks))
    else:
        context = multiprocessing.get_context("spawn")
        with context.Pool(
            processes,
            initializer=worker_init,
            initargs=(factors, curve_k, prime),
        ) as pool:
            results = list(pool.imap_unordered(scan_normal, tasks))

    candidates = [
        list(quartet)
        for quartet in sorted({quartet for _, quartets, _, _ in results for quartet in quartets})
    ]
    primary_histogram = Counter()
    for _, _, histogram, _ in results:
        primary_histogram.update({int(key): value for key, value in histogram.items()})

    worker_init(factors, curve_k, prime)
    secondary = []
    active = candidates
    cache = {}
    for slope in (3, 4):
        survivors = []
        local_histogram = Counter()
        before = len(cache)
        evaluations = 0
        for quartet in active:
            sections = {constant: [] for constant in range(4)}
            for curve in quartet:
                sections[curve_constant[curve]].append(curve)
            need(
                all(len(section) == 1 for section in sections.values()),
                f"quartet does not have four signature sections: {quartet}",
            )
            pairs = (
                (sections[0][0], sections[1][0]),
                (sections[2][0], sections[3][0]),
            )
            projected = []
            for pair in pairs:
                key = slope, pair
                if key not in cache:
                    cache[key] = projected_resultant(pair, slope)
                    evaluations += len(cache[key])
                projected.append(cache[key])
            degree = gcd_degree(projected[0], projected[1])
            local_histogram[degree] += 1
            if degree:
                survivors.append(quartet)
        secondary.append(
            {
                "slope": slope,
                "input_count": len(active),
                "distinct_pair_resultants": len(cache) - before,
                "interpolation_evaluations": evaluations,
                "gcd_degree_histogram": {
                    str(key): value for key, value in sorted(local_histogram.items())
                },
                "survivors": survivors,
                "survivor_sha256": digest(survivors),
            }
        )
        active = survivors
        if not active:
            break

    bucket_serialization = [
        [list(normal), constant, curves]
        for normal in sorted(buckets)
        for constant, curves in sorted(buckets[normal].items())
    ]
    return {
        "prime": prime,
        "projection_slopes": [2, 3, 4],
        "covering_signature_normals": len(tasks),
        "eligible_no_circle_quartets": raw_quartets,
        "curve_bucket_sha256": digest(bucket_serialization),
        "primary": {
            "slope": 2,
            "distinct_pair_resultants": len(pair_inventory),
            "pair_inventory_sha256": digest(pair_inventory),
            "interpolation_evaluations": sum(item[3] for item in results),
            "gcd_degree_histogram": {
                str(key): value for key, value in sorted(primary_histogram.items())
            },
            "survivors": candidates,
            "survivor_sha256": digest(candidates),
        },
        "secondary": secondary,
        "final_survivors": active,
        "all_eligible_quartets_excluded": not active,
    }
