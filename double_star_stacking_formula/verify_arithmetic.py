#!/usr/bin/env python3
"""Check the sharp arithmetic inequalities used in the double-star proof."""

from __future__ import annotations

import argparse


def sufficient(p: int, q: int, x: int, y: int) -> bool:
    """Return whether one of the three explicit stacking procedures applies."""
    if x >= p + 1 and y >= q + 1:
        return x + y >= p + q + 3
    if x <= p:
        deficit = p + 1 - x
        return y >= 2 * deficit + q + 2
    assert y <= q
    deficit = q + 1 - y
    return x >= 2 * deficit + p + 2


def check_pair_exhaustively(a: int, b: int) -> None:
    formula = 5 * a + 3 * b + 7
    for p in range(a + 1):
        for q in range(b + 1):
            # If 2x+2y+p+q reaches the formula, the proof says that one of
            # the constructive stacking cases must apply.  Values beyond the
            # displayed range are automatically sufficient by monotonicity.
            for x in range(formula + 1):
                for y in range(formula + 1):
                    envelope = 2 * x + 2 * y + p + q
                    if envelope >= formula:
                        assert sufficient(p, q, x, y), (a, b, p, q, x, y)



def check_pair_symbolically(a: int, b: int) -> None:
    """Evaluate the closed-form maxima from the three failed cases."""
    formula = 5 * a + 3 * b + 7
    assert 3 * a + 3 * b + 4 <= formula - 1
    assert 5 * a + 3 * b + 6 == formula - 1
    assert 3 * a + 5 * b + 6 <= formula - 1

    # Edge-flow bounds for the proposed critical configuration.
    heavy = 4 * a + 2 * b + 7
    heavy_leaf_contribution = (heavy - 3) // 2
    assert heavy_leaf_contribution == 2 * a + b + 2
    assert heavy_leaf_contribution - (b - 1) - (2 * a + 3) == 0
    assert heavy - 2 * (2 * a + b + 2) - 3 == 0


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--exhaustive-max-a", type=int, default=10)
    parser.add_argument("--identity-max-a", type=int, default=1000)
    args = parser.parse_args()
    exhaustive = 0
    for a in range(1, args.exhaustive_max_a + 1):
        for b in range(1, a + 1):
            check_pair_exhaustively(a, b)
            exhaustive += 1
    identities = 0
    for a in range(1, args.identity_max_a + 1):
        for b in range(1, a + 1):
            check_pair_symbolically(a, b)
            identities += 1
    print(f"exhaustive_parameter_pairs={exhaustive}")
    print(f"closed_form_parameter_pairs={identities}")
    print("upper_bound_case_partition=true")
    print("critical_edge_flow_identities=true")


if __name__ == "__main__":
    main()
