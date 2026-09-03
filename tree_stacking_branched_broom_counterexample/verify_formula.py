#!/usr/bin/env python3
"""Exact closed-form audit for the 23-vertex branched-broom counterexample."""

from math import comb


def branched_broom_potentials(d: int, e: int, t: int) -> tuple[int, int]:
    """Return the symbolic p- and arm-parent potentials for R(d,e,t)."""
    x_p = d - 3 + (5 * e + 3) * 2**t
    x_a = (d + 3) * 2 ** (t + 1) + 10 * e - 12
    return x_p, x_a


def symmetric_double_broom_count(a: int, ell: int) -> int:
    """Return N(B(a,a,ell)) from the sibling-leaf classification."""
    return 2 * comb(2**ell * (a + 3) + 2 * a - 4, a - 1)


def main() -> None:
    d, e, t = 8, 4, 6
    order = d + 2 * e + t + 1
    x_p, x_a = branched_broom_potentials(d, e, t)
    assert order == 23
    assert (x_p, x_a) == (1477, 1436)
    assert x_p > x_a

    candidate = comb(x_p + d - 1, d - 1)
    assert candidate == 3_100_645_395_776_119_256

    rows: list[tuple[int, int, int, int]] = []
    for a in range(1, 11):
        ell = 22 - 2 * a
        upper = 2**ell * (a + 3) + 2 * a - 4
        value = symmetric_double_broom_count(a, ell)
        rows.append((a, ell, upper, value))

    best = max(rows, key=lambda row: row[3])
    assert best == (6, 10, 9224, 1_111_665_975_462_168_688)
    difference = candidate - best[3]
    assert difference == 1_988_979_420_313_950_568

    print("a ell binomial_upper N")
    for row in rows:
        print(*row)
    print(f"candidate_order={order}")
    print(f"candidate_X_p={x_p}")
    print(f"candidate_X_a={x_a}")
    print(f"candidate_N={candidate}")
    print(f"best_symmetric_parameters=({best[0]},{best[0]},{best[1]})")
    print(f"best_symmetric_N={best[3]}")
    print(f"difference={difference}")
    print("status=VERIFIED")


if __name__ == "__main__":
    main()
