#!/usr/bin/env python3
"""Complete finite base certificate and independent regression checks."""

from __future__ import annotations

from fractions import Fraction
from hashlib import sha256
import json

import direct
import layers


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ArithmeticError(message)


def audit_case(b: int, c: int) -> tuple[int, ...]:
    a = layers.comparison(b, c)
    z = direct.comparison(b, c)
    require(a == z, f"coefficient-level algorithm disagreement at {(b,c)}")
    g = layers.reference(b, c)
    require(g == direct.reference(b, c), f"reference disagreement at {(b,c)}")
    require(len(a) == b*c//2+1, "wrong coefficient vector length")
    require(a[:3] == (0, 0, 0) and a[3] == 1, "wrong initial Schur coefficients")
    require(all(x > 0 for x in a[3:]), f"nonpositive coefficient at {(b,c)}")
    require(all(960*x >= 31*y for x, y in zip(a, g)),
            f"quantitative Schur bound failed at {(b,c)}")
    return a


def record_bytes(b: int, c: int, values: tuple[int, ...]) -> bytes:
    return (f"{b}|{c}|"+','.join(map(str, values))+'\n').encode('ascii')


def run() -> dict[str, object]:
    budget = layers.tail_budget()
    base = [(b, c) for c in range(3, 11) for b in range(3, c+1) if b*c % 2 == 0]
    require(len(base) == 26, "incomplete finite base")
    digest = sha256()
    count = 0
    minimum_ratio = Fraction(2)
    for b, c in base:
        values = audit_case(b, c)
        count += len(values)
        digest.update(record_bytes(b, c, values))
        g = layers.reference(b, c)
        minimum_ratio = min(minimum_ratio, *(Fraction(x,y) for x,y in zip(values,g) if y))

    # These are regression audits of the already symbolic c>=11 theorem,
    # not a larger finite range presented as a proof of that theorem.
    regression = [(3,12), (4,11), (11,12), (12,12)]
    regression += [(b,16) for b in range(4,17)]
    regression += [(8,24), (12,24), (16,24)]
    regression_digest = sha256()
    regression_count = 0
    for b, c in regression:
        values = audit_case(b, c)
        regression_digest.update(record_bytes(b,c,values))
        regression_count += len(values)

    kernel_checks = 0
    for n in range(2, 385):
        f, prev = layers.lucas_schur(n), layers.lucas_schur(n-2)
        for r, coefficient in enumerate(f):
            rhs = 2*prev[r-1] if 1 <= r <= len(prev) else 0
            require(coefficient >= rhs, "Schur contraction kernel failed")
            kernel_checks += 1

    prefix_checks = absolute_checks = 0
    p = layers.partitions_through(192)
    for b in range(3,17):
        restricted = layers.partitions_through(11, smallest=2, largest=b)
        for c in range(max(b,11),25):
            if b*c % 2:
                continue
            rectangle = layers.gaussian(b+c,b)
            u = [rectangle[i]-(rectangle[i-1] if i else 0)-(i % 2 == 0)
                 for i in range(b*c//2+1)]
            for i in range(12):
                require(u[i] == restricted[i]-(i % 2 == 0), "stable prefix mismatch")
                prefix_checks += 1
            for i in range(2,len(u)):
                require(abs(u[i]) <= p[i], "partition envelope failure")
                absolute_checks += 1

    return {
        "schema": "lucas-a2-complete-schur-v1",
        "finite_base_cases": len(base),
        "finite_base_schur_coefficients": count,
        "finite_base_records_sha256": digest.hexdigest(),
        "finite_base_minimum_D_over_G": str(minimum_ratio),
        "finite_base_maximum_degree": 100,
        "regression_cases": len(regression),
        "regression_schur_coefficients": regression_count,
        "regression_records_sha256": regression_digest.hexdigest(),
        "kernel_coefficients_audited": kernel_checks,
        "stable_prefix_values_audited": prefix_checks,
        "absolute_layer_bounds_audited": absolute_checks,
        "tail_budget": budget,
        "all_checks": True,
    }


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, sort_keys=True))
