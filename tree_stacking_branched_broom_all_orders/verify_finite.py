#!/usr/bin/env python3
"""Exact closed-form verification of the finite all-orders comparison."""

from __future__ import annotations

import hashlib
import json
import sys
from math import comb
from pathlib import Path


FIRST_ORDER = 23
LAST_FINITE_ORDER = 576
EXPECTED_PATH = Path(__file__).with_name("expected_summary.json")

# Exact record integers at the upper endpoint have more than 4,300 decimal
# digits.  Disable only CPython's display-conversion guard; arithmetic is
# unaffected.
if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)


def witness_parameters(n: int) -> tuple[int, int, int]:
    """Return the declared R(d,e,t) witness of order n."""
    if 23 <= n <= 32:
        d, e = 8, 4
        return d, e, n - d - 2 * e - 1
    if 33 <= n <= 36:
        d, e = 10, 5
        return d, e, n - d - 2 * e - 1
    if n >= 37:
        m = (n - 1) // 18
        d, e = 5 * m + 3, 2 * m + 2
        return d, e, n - d - 2 * e - 1
    raise ValueError(f"no witness declared for order {n}")


def branched_potentials(d: int, e: int, t: int) -> tuple[int, int]:
    """Return the two leaf-parent potentials in R(d,e,t)."""
    x_p = d - 3 + (5 * e + 3) * 2**t
    x_a = (d + 3) * 2 ** (t + 1) + 10 * e - 12
    return x_p, x_a


def symmetric_count(a: int, ell: int) -> int:
    """Return N(B(a,a,ell)) from the sibling-leaf count formula."""
    upper = 2**ell * (a + 3) + 2 * a - 4
    return 2 * comb(upper, a - 1)


def canonical_record(n: int) -> dict[str, int]:
    """Compute one exact comparison record at order n."""
    d, e, t = witness_parameters(n)
    assert d >= 2 and e >= 1 and t >= 1
    assert d + 2 * e + t + 1 == n

    x_p, x_a = branched_potentials(d, e, t)
    assert x_p > x_a
    candidate = comb(x_p + d - 1, d - 1)

    symmetric_rows = [
        (symmetric_count(a, n - 2 * a - 1), a, n - 2 * a - 1)
        for a in range(1, (n - 2) // 2 + 1)
    ]
    best_value, best_a, best_ell = max(symmetric_rows)
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
        "x_a": x_a,
        "x_p": x_p,
    }


def summarize() -> dict[str, int | str]:
    digest = hashlib.sha256()
    minimum: dict[str, int] | None = None
    final: dict[str, int] | None = None
    count = 0

    for n in range(FIRST_ORDER, LAST_FINITE_ORDER + 1):
        record = canonical_record(n)
        encoded = json.dumps(record, sort_keys=True, separators=(",", ":"))
        digest.update(encoded.encode("ascii") + b"\n")
        if minimum is None or record["margin"] < minimum["margin"]:
            minimum = record
        final = record
        count += 1

    assert minimum is not None and final is not None
    return {
        "finite_first_order": FIRST_ORDER,
        "finite_last_order": LAST_FINITE_ORDER,
        "finite_orders_checked": count,
        "minimum_margin": minimum["margin"],
        "minimum_margin_order": minimum["n"],
        "order_576_best_a": final["best_a"],
        "order_576_best_symmetric_bits": final["best_symmetric"].bit_length(),
        "order_576_candidate_bits": final["candidate"].bit_length(),
        "order_576_witness_d": final["d"],
        "order_576_witness_e": final["e"],
        "order_576_witness_t": final["t"],
        "record_sha256": digest.hexdigest(),
    }


def main() -> None:
    summary = summarize()
    expected = json.loads(EXPECTED_PATH.read_text(encoding="utf-8"))
    assert summary == expected
    for key, value in summary.items():
        print(f"{key}={value}")
    print("status=VERIFIED")


if __name__ == "__main__":
    main()
