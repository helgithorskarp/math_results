#!/usr/bin/env python3
"""Verify a rational flip-threshold certificate using only Python integers."""

import argparse
import hashlib
import json
from pathlib import Path


def require(condition, message):
    if not condition:
        raise ValueError(message)


def build(c):
    require(c["schema"] == 1, "unsupported certificate schema")
    q = c["q"]
    denominator = c["weight_denominator"]
    h = c["potential"]
    v = c["subeigenvector"]
    require(q == 13 and denominator == 5_000_000, "unexpected tournament parameters")
    require(len(h) == len(v) == q, "wrong vector dimension")
    require(all(type(x) is int for x in h + v), "noninteger vector entry")
    require(min(v) == 10**16, "unexpected vector normalization")
    require(c["directed_prefix"] == 5600 and c["alternating_pairs"] == 1200,
            "unexpected path word")
    require(c["growth"] == [25_000_001, 25_000_000], "unexpected growth claim")
    require(c["padding_factor"] == [999, 1000], "unexpected padding claim")
    require(c["repetitions_at_least"] == 30_000, "unexpected length threshold")
    weights = []
    for i in range(q):
        row = []
        for j in range(q):
            sign = 0 if i == j else (1 if 0 < (j - i) % q <= q // 2 else -1)
            row.append(denominator // 2 + 2_497_500 * sign + h[i] - h[j])
        weights.append(row)
    require(all(0 < weights[i][j] < denominator for i in range(q) for j in range(q)),
            "matrix is not a strictly positive weighted tournament")
    require(all(weights[i][j] + weights[j][i] == denominator
                for i in range(q) for j in range(q)), "tournament identity fails")
    return weights, q * denominator // 2


def down_step(a, denominator, vector):
    """Componentwise lower bound for (a/denominator) times vector."""
    return [sum(x * y for x, y in zip(row, vector)) // denominator for row in a]


def direct_check(c, a, denominator):
    v = c["subeigenvector"]
    transpose = [list(row) for row in zip(*a)]
    image = v[:]
    for _ in range(c["alternating_pairs"]):
        image = down_step(transpose, denominator, image)
        image = down_step(a, denominator, image)
    for _ in range(c["directed_prefix"]):
        image = down_step(a, denominator, image)
    numerator, growth_denominator = c["growth"]
    slack = min(growth_denominator * y - numerator * x for x, y in zip(v, image))
    require(slack > 0, "subeigenvector inequality fails")

    period = c["directed_prefix"] + 2 * c["alternating_pairs"]
    padding_numerator, padding_denominator = c["padding_factor"]
    lower = [min(v)] * c["q"]
    padding_slack = None
    worst_padding = None
    for length in range(period):
        current = min(padding_denominator * y - padding_numerator * x
                      for x, y in zip(v, lower))
        if padding_slack is None or current < padding_slack:
            padding_slack, worst_padding = current, length
        require(current >= 0, "padding inequality fails")
        lower = down_step(a, denominator, lower)

    repetitions = c["repetitions_at_least"]
    # Bernoulli: g^t >= 1 + t(g-1).
    bernoulli_slack = (
        padding_numerator * (growth_denominator + repetitions * (numerator - growth_denominator))
        - padding_denominator * growth_denominator
    )
    require(bernoulli_slack > 0, "length threshold fails")
    return {
        "direct_min_growth_slack": slack,
        "direct_min_increment": min(y - x for x, y in zip(v, image)),
        "padding_min_slack": padding_slack,
        "worst_padding_length": worst_padding,
        "bernoulli_slack": bernoulli_slack,
        "all_lengths_at_least": period * repetitions,
        "flip_ratio_upper_bound": [2 * c["alternating_pairs"], period],
    }


def block_check(c, a, denominator):
    """Different decomposition: rounded matrix powers by repeated squaring.

    Every stored matrix divided by scale is an entrywise lower bound.
    Nonnegativity preserves that order through every multiplication.
    """
    q = c["q"]
    scale = 10**35

    def product(x, y):
        columns = list(zip(*y))
        return [[sum(p * r for p, r in zip(row, column)) // scale
                 for column in columns] for row in x]

    def power(x, exponent):
        answer = [[scale if i == j else 0 for j in range(q)] for i in range(q)]
        while exponent:
            if exponent & 1:
                answer = product(answer, x)
            exponent //= 2
            if exponent:
                x = product(x, x)
        return answer

    m = [[x * scale // denominator for x in row] for row in a]
    b = product(m, [list(row) for row in zip(*m)])
    lower = product(power(m, c["directed_prefix"]), power(b, c["alternating_pairs"]))
    v = c["subeigenvector"]
    image = [sum(x * y for x, y in zip(row, v)) // scale for row in lower]
    numerator, growth_denominator = c["growth"]
    slack = min(growth_denominator * y - numerator * x for x, y in zip(v, image))
    require(slack > 0, "block-power subeigenvector inequality fails")
    return {"block_min_growth_slack": slack, "block_scale": scale}


def verify(c):
    a, denominator = build(c)
    result = direct_check(c, a, denominator)
    result.update(block_check(c, a, denominator))
    result["status"] = "PASS"
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("certificate", nargs="?", type=Path,
                        default=Path(__file__).with_name("certificate.json"))
    args = parser.parse_args()
    raw = args.certificate.read_bytes()
    result = verify(json.loads(raw))
    result["certificate_sha256"] = hashlib.sha256(raw).hexdigest()
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
