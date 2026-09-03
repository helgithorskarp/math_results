#!/usr/bin/env python3
"""Independent direct finite checks of the optimizer certificate."""

from __future__ import annotations

import sys
from math import comb


if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)


def independent_count(d: int, e: int, t: int) -> int:
    """Evaluate both sibling classes without importing the main checker."""
    left = d - 3 + (5 * e + 3) * (1 << t)
    right = (d + 3) * (1 << (t + 1)) + 10 * e - 12
    total = 0
    if left >= right:
        total += comb(left + d - 1, d - 1)
    if right >= left:
        total += e
    return total


def brute_force(n: int) -> tuple[int, int, int]:
    """Scan every positive d,e,t with d+2e+t+1=n."""
    winner: tuple[int, int, int] | None = None
    best = -1
    ties = 0
    for d in range(1, n - 3):
        for e in range(1, (n - d - 1) // 2 + 1):
            t = n - d - 2 * e - 1
            if t < 1:
                continue
            value = independent_count(d, e, t)
            if value > best:
                best = value
                winner = (d, e, t)
                ties = 1
            elif value == best:
                ties += 1
    assert winner is not None and ties == 1
    return winner


def expected(n: int) -> tuple[int, int, int]:
    m = (n - 1) // 18
    d, e = 5 * m + 3, 2 * m + 2
    return d, e, n - d - 2 * e - 1


def check_residue_table() -> None:
    expected_a = (13, 11, 9, 12, 10)
    expected_five_q = (-30, -26, -22, -28, -24)
    for j in range(5):
        k = 17
        r = 5 * k + j
        d = r + 1
        e = (2 * d + 8) // 5
        a = 5 * e + 3 - 2 * r
        # t_0=n-(9/5)r+q, so 5q=5(t_0-n)+9r.
        n = 1000
        t = n - d - 2 * e - 1
        five_q = 5 * (t - n) + 9 * r
        assert a == expected_a[j]
        assert five_q == expected_five_q[j]


def main() -> None:
    check_residue_table()
    for n in range(91, 121):
        assert brute_force(n) == expected(n), n
    print("residue_table=VERIFIED")
    print("direct_first_order=91")
    print("direct_last_order=120")
    print("direct_orders_checked=30")
    print("INDEPENDENT DIRECT ENUMERATION THROUGH 120 PASSED")


if __name__ == "__main__":
    main()
