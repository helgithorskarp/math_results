#!/usr/bin/env python3
"""Independent core-distance and product-recurrence finite verifier."""

from __future__ import annotations

import hashlib
import json
import sys
from math import factorial, prod
from pathlib import Path


FIRST_ORDER = 23
LAST_FINITE_ORDER = 576
EXPECTED_PATH = Path(__file__).with_name("expected_summary.json")

if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)


def choose_witness(n: int) -> tuple[int, int, int]:
    if n < 23:
        raise ValueError("the theorem begins at order 23")
    if n < 33:
        d, e = 8, 4
    elif n < 37:
        d, e = 10, 5
    else:
        quotient = (n - 1) // 18
        d, e = 5 * quotient + 3, 2 * quotient + 2
    return d, e, n - d - 2 * e - 1


def weak_compositions(total: int, parts: int) -> int:
    """Count weak compositions without math.comb."""
    assert total >= 0 and parts >= 1
    r = parts - 1
    numerator = prod(range(total + 1, total + r + 1))
    denominator = factorial(r)
    assert numerator % denominator == 0
    return numerator // denominator


def branched_core_potentials(d: int, e: int, t: int) -> tuple[int, int]:
    """Sum full-tree degrees by core distance, without closed potentials."""
    assert d >= 1 and e >= 1 and t >= 1

    # Core path p=v_0,...,v_t=q, plus e arm parents adjacent to q.
    path_degrees = [d + 1] + [2] * (t - 1) + [e + 1]
    arm_degrees = [2] * e

    x_p = sum(degree * 2**j for j, degree in enumerate(path_degrees))
    x_p += sum(degree * 2 ** (t + 1) for degree in arm_degrees)

    # Use the first arm parent as the target.  Its distance to v_j is
    # t-j+1, its distance to itself is zero, and to every other arm is two.
    x_arm = sum(
        degree * 2 ** (t - j + 1)
        for j, degree in enumerate(path_degrees)
    )
    x_arm += arm_degrees[0]
    x_arm += sum(degree * 2**2 for degree in arm_degrees[1:])
    return x_p, x_arm


def double_broom_count_from_core(a: int, ell: int) -> int:
    """Evaluate one symmetric double broom from its weighted core path."""
    assert a >= 1 and ell >= 1
    degrees = [a + 1] + [2] * (ell - 1) + [a + 1]
    potential = sum(degree * 2**j for j, degree in enumerate(degrees))
    one_side = weak_compositions(potential, a)
    return 2 * one_side


def make_record(n: int) -> dict[str, int]:
    d, e, t = choose_witness(n)
    assert d + 2 * e + t + 1 == n
    x_p, x_arm = branched_core_potentials(d, e, t)
    assert x_p > x_arm
    candidate = weak_compositions(x_p, d)

    alternatives: list[tuple[int, int, int]] = []
    for a in range(1, (n - 2) // 2 + 1):
        ell = n - 2 * a - 1
        alternatives.append((double_broom_count_from_core(a, ell), a, ell))
    best_value, best_a, best_ell = max(alternatives)
    margin = candidate - best_value
    assert margin > 0

    return {
        "best_a": best_a,
        "best_ell": best_ell,
        "best_symmetric": best_value,
        "candidate": candidate,
        "d": d,
        "e": e,
        "margin": margin,
        "n": n,
        "t": t,
        "x_a": x_arm,
        "x_p": x_p,
    }


def main() -> None:
    expected = json.loads(EXPECTED_PATH.read_text(encoding="utf-8"))
    digest = hashlib.sha256()
    minimum: dict[str, int] | None = None
    last: dict[str, int] | None = None
    checked = 0

    for n in range(FIRST_ORDER, LAST_FINITE_ORDER + 1):
        record = make_record(n)
        line = json.dumps(record, sort_keys=True, separators=(",", ":"))
        digest.update(line.encode("ascii") + b"\n")
        if minimum is None or record["margin"] < minimum["margin"]:
            minimum = record
        last = record
        checked += 1

    assert minimum is not None and last is not None
    summary: dict[str, int | str] = {
        "finite_first_order": FIRST_ORDER,
        "finite_last_order": LAST_FINITE_ORDER,
        "finite_orders_checked": checked,
        "minimum_margin": minimum["margin"],
        "minimum_margin_order": minimum["n"],
        "order_576_best_a": last["best_a"],
        "order_576_best_symmetric_bits": last["best_symmetric"].bit_length(),
        "order_576_candidate_bits": last["candidate"].bit_length(),
        "order_576_witness_d": last["d"],
        "order_576_witness_e": last["e"],
        "order_576_witness_t": last["t"],
        "record_sha256": digest.hexdigest(),
    }
    assert summary == expected
    for key, value in summary.items():
        print(f"{key}={value}")
    print("status=VERIFIED")


if __name__ == "__main__":
    main()
