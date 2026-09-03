#!/usr/bin/env python3
"""Independent coefficient check for the Albertson r=27 Kempe states.

Unlike verify.py's closed binomial coefficient formula, this file multiplies
the two bivariate local-state polynomials by a direct dynamic program.
"""

from __future__ import annotations

import json
from pathlib import Path


P2 = {
    (0, 0): 1,
    (1, 0): 1,
    (1, 1): 2,
    (2, 0): 1,
    (2, 1): 2,
    (2, 2): 1,
    (3, 2): 1,
}

P3 = {
    (0, 0): 1,
    (1, 0): 2,
    (1, 1): 3,
    (2, 0): 3,
    (2, 1): 6,
    (2, 2): 3,
    (3, 0): 2,
    (3, 1): 5,
    (3, 2): 6,
    (3, 3): 1,
    (4, 1): 1,
    (4, 2): 3,
    (4, 3): 2,
    (5, 3): 1,
}


def multiply(
    distribution: list[list[int]],
    polynomial: dict[tuple[int, int], int],
    max_weight: int,
    max_excess: int,
) -> list[list[int]]:
    new = [[0] * (max_excess + 1) for _ in range(max_weight + 1)]
    for weight, row in enumerate(distribution):
        for excess, count in enumerate(row):
            if not count:
                continue
            for (dw, de), multiplicity in polynomial.items():
                if weight + dw <= max_weight and excess + de <= max_excess:
                    new[weight + dw][excess + de] += count * multiplicity
    return new


def main() -> None:
    expected = json.loads(Path(__file__).with_name("certificate.json").read_text())[
        "state_counts"
    ]

    # One direct 325-step multiplication supplies both the order-53 table
    # and, via the step-300 snapshot, the pair-pair factor for order 54.
    distribution = [[0] * 53 for _ in range(376)]
    distribution[0][0] = 1
    pair_300 = None
    for step in range(1, 326):
        distribution = multiply(distribution, P2, 375, 52)
        if step == 300:
            pair_300 = [row[:49] for row in distribution]
    assert pair_300 is not None
    pair_325 = distribution
    cases = ((53, 713, 362, 48), (53, 714, 363, 50), (53, 715, 364, 52))
    for n, m, weight, excess in cases:
        count = sum(pair_325[weight][: excess + 1])
        assert str(count) == expected[f"{n},{m}"]
        print(f"PASS independent DP n={n},m={m}: {count}")

    distribution = pair_300
    for _ in range(25):
        distribution = multiply(distribution, P3, 375, 48)
    count54 = sum(distribution[375])
    assert str(count54) == expected["54,726"]
    print(f"PASS independent DP n=54,m=726: {count54}")


if __name__ == "__main__":
    main()
