#!/usr/bin/env python3
"""Exact finite checks for the eventual branched-broom optimizer pattern."""

from __future__ import annotations

import hashlib
import json
import sys
from math import comb
from pathlib import Path


FIRST_PATTERN_ORDER = 91
LAST_CHECKED_ORDER = 500
EXPECTED_PATH = Path(__file__).with_name("expected_summary.json")

if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)


def potentials(d: int, e: int, t: int) -> tuple[int, int]:
    """Return the p-leaf and arm-leaf potentials."""
    return (
        d - 3 + (5 * e + 3) * 2**t,
        (d + 3) * 2 ** (t + 1) + 10 * e - 12,
    )


def exact_count(d: int, e: int, t: int) -> int:
    """Evaluate N(R(d,e,t)) from the sibling-leaf classification."""
    x_p, x_a = potentials(d, e, t)
    p_count = comb(x_p + d - 1, d - 1) if x_p >= x_a else 0
    arm_count = e if x_a >= x_p else 0
    return p_count + arm_count


def pattern_parameters(n: int) -> tuple[int, int, int]:
    """Return the 18-periodic parameter pattern from the theorem."""
    m = (n - 1) // 18
    d = 5 * m + 3
    e = 2 * m + 2
    return d, e, n - d - 2 * e - 1


def direct_optima(n: int) -> tuple[int, tuple[tuple[int, int, int], ...]]:
    """Enumerate all positive parameter triples of order n."""
    best = -1
    optima: list[tuple[int, int, int]] = []
    for d in range(1, n - 3):
        for e in range(1, (n - d - 1) // 2 + 1):
            t = n - d - 2 * e - 1
            if t < 1:
                continue
            value = exact_count(d, e, t)
            if value > best:
                best = value
                optima = [(d, e, t)]
            elif value == best:
                optima.append((d, e, t))
    assert best >= 0
    return best, tuple(optima)


def first_potential_e(d: int) -> int:
    """Return ceil((2d+4)/5), forced when d>=2 and the p class wins."""
    return (2 * d + 8) // 5


def formal_binomial_upper(n: int, d: int) -> tuple[int, int, int] | None:
    """Return the formal e_0 binomial upper bound for a fixed d."""
    e = first_potential_e(d)
    t = n - d - 2 * e - 1
    if t < 1:
        return None
    upper = (5 * e + 3) * 2**t + 2 * d - 4
    return comb(upper, d - 1), e, t


def verify_preperiod() -> tuple[int, str]:
    """Directly determine the last sub-91 exception to the pattern."""
    digest = hashlib.sha256()
    exceptions: list[int] = []
    for n in range(9, FIRST_PATTERN_ORDER):
        value, optima = direct_optima(n)
        expected = pattern_parameters(n)
        if optima != (expected,):
            exceptions.append(n)
        row = f"{n}:{value}:{','.join(map(str, optima))}\n"
        digest.update(row.encode("ascii"))
    assert exceptions
    return exceptions[-1], digest.hexdigest()


def verify_pattern_range() -> dict[str, int | str]:
    """Certify the formal upper reduction at every checked order."""
    digest = hashlib.sha256()
    narrowest_order = -1
    narrowest_floor_ratio: int | None = None
    final: tuple[int, int, int, int] | None = None

    for n in range(FIRST_PATTERN_ORDER, LAST_CHECKED_ORDER + 1):
        d_star, e_star, t_star = pattern_parameters(n)
        assert d_star + 2 * e_star + t_star + 1 == n
        x_p, x_a = potentials(d_star, e_star, t_star)
        assert x_p > x_a
        candidate = comb(x_p + d_star - 1, d_star - 1)

        runner_upper = n  # Covers d=1 and all arm-only rows.
        runner_parameters = (1, 1, n - 4)
        for d in range(2, n - 3):
            if d == d_star:
                continue
            formal = formal_binomial_upper(n, d)
            if formal is None:
                continue
            value, e, t = formal
            value += n  # Uniform additive upper bound for a possible tie.
            if value > runner_upper:
                runner_upper = value
                runner_parameters = (d, e, t)

        # For the same d, every e>e_star is bounded by the e_star+1 row.
        next_e = e_star + 1
        next_t = n - d_star - 2 * next_e - 1
        if next_t >= 1:
            next_upper = (5 * next_e + 3) * 2**next_t + 2 * d_star - 4
            same_d_upper = comb(next_upper, d_star - 1) + n
            if same_d_upper > runner_upper:
                runner_upper = same_d_upper
                runner_parameters = (d_star, next_e, next_t)

        assert candidate > runner_upper, (n, runner_parameters)
        floor_ratio = candidate // runner_upper
        if narrowest_floor_ratio is None or floor_ratio < narrowest_floor_ratio:
            narrowest_floor_ratio = floor_ratio
            narrowest_order = n

        record = (
            f"{n}:{d_star}:{e_star}:{t_star}:{candidate}:"
            f"{runner_parameters}:{runner_upper}\n"
        )
        digest.update(record.encode("ascii"))
        final = (d_star, e_star, t_star, candidate.bit_length())

    assert narrowest_floor_ratio is not None and final is not None
    return {
        "finite_first_order": FIRST_PATTERN_ORDER,
        "finite_last_order": LAST_CHECKED_ORDER,
        "finite_orders_checked": LAST_CHECKED_ORDER - FIRST_PATTERN_ORDER + 1,
        "narrowest_floor_ratio": narrowest_floor_ratio,
        "narrowest_order": narrowest_order,
        "order_500_d": final[0],
        "order_500_e": final[1],
        "order_500_t": final[2],
        "order_500_count_bits": final[3],
        "finite_record_sha256": digest.hexdigest(),
    }


def summarize() -> dict[str, int | str]:
    last_exception, preperiod_hash = verify_preperiod()
    result = verify_pattern_range()
    result["last_exception"] = last_exception
    result["preperiod_record_sha256"] = preperiod_hash
    return result


def main() -> None:
    summary = summarize()
    expected = json.loads(EXPECTED_PATH.read_text(encoding="utf-8"))
    assert summary == expected, (summary, expected)
    for key, value in summary.items():
        print(f"{key}={value}")
    print("EXACT ORDERS 91..500 VERIFIED")


if __name__ == "__main__":
    main()
