#!/usr/bin/env python3
"""Generate a direct CNF for a packing total coloring of a cycle."""

from __future__ import annotations

import argparse
from pathlib import Path


def variable(position: int, color: int, colors: int) -> int:
    """DIMACS variable for zero-based position and one-based color."""
    return position * colors + color


def cyclic_distance(a: int, b: int, order: int) -> int:
    delta = abs(a - b)
    return min(delta, order - delta)


def clauses(order: int, colors: int, symmetry: bool):
    """Yield the complete direct encoding, one clause as a list of ints."""
    for position in range(order):
        yield [variable(position, color, colors) for color in range(1, colors + 1)]

    for position in range(order):
        for color_a in range(1, colors + 1):
            for color_b in range(color_a + 1, colors + 1):
                yield [-variable(position, color_a, colors), -variable(position, color_b, colors)]

    for color in range(1, colors + 1):
        for a in range(order):
            for b in range(a + 1, order):
                if cyclic_distance(a, b, order) <= 2 * color:
                    yield [-variable(a, color, colors), -variable(b, color, colors)]

    if symmetry:
        yield [variable(0, 1, colors)]

        # T(C_n) = C_(2n)^2 has diameter ceil(n/2).
        diameter = (order // 2 + 1) // 2
        for color in range(diameter + 1, colors + 1):
            for position in range(order):
                yield [
                    -variable(position, color, colors),
                    *[
                        variable(earlier, color - 1, colors)
                        for earlier in range(position)
                    ],
                ]


def write_cnf(n: int, colors: int, output: Path, symmetry: bool) -> tuple[int, int]:
    if n < 3 or colors < 1:
        raise ValueError("require n >= 3 and colors >= 1")
    order = 2 * n
    encoded = list(clauses(order, colors, symmetry))
    with output.open("w", encoding="ascii") as handle:
        handle.write(f"p cnf {order * colors} {len(encoded)}\n")
        for clause in encoded:
            handle.write(" ".join(map(str, clause)) + " 0\n")
    return order * colors, len(encoded)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("n", type=int, help="order of the original cycle C_n")
    parser.add_argument("colors", type=int)
    parser.add_argument("output", type=Path)
    parser.add_argument("--symmetry", action="store_true")
    args = parser.parse_args()
    variables, clause_count = write_cnf(args.n, args.colors, args.output, args.symmetry)
    print(f"wrote {variables} variables and {clause_count} clauses to {args.output}")


if __name__ == "__main__":
    main()
