#!/usr/bin/env python3
"""Check the strict color-class capacity lower bounds used in the proof."""


CASES = [(16, 9), (17, 8), (19, 8), (22, 8)]


def capacity(n: int, colors: int) -> tuple[list[int], int]:
    # On 2n cyclic positions, occurrences of color i have gap at least 2i+1.
    bounds = [(2 * n) // (2 * color + 1) for color in range(1, colors + 1)]
    return bounds, sum(bounds)


def main() -> None:
    for n, colors in CASES:
        bounds, total = capacity(n, colors)
        assert total < 2 * n, (n, colors, bounds, total)
        print(f"C_{n}, k={colors}: capacities={bounds}, sum={total} < {2*n}")
    print(f"verified {len(CASES)} strict capacity lower bounds")


if __name__ == "__main__":
    main()
