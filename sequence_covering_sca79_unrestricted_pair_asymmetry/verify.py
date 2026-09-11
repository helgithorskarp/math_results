#!/usr/bin/env python3
"""Exact checker for unrestricted named-coordinate pair-link asymmetry."""

from __future__ import annotations

from math import comb, factorial, lcm
from pathlib import Path


U = (1, -7, 21, -35, 35, -21, 7, -1, 0)
V = (0, 1, -7, 21, -35, 35, -21, 7, -1)


def multinomial(parts: tuple[int, ...]) -> int:
    result = factorial(sum(parts))
    for part in parts:
        result //= factorial(part)
    return result


def positional_lcms() -> tuple[tuple[int, ...], tuple[int, ...]]:
    outgoing = []
    incoming = []
    for i in range(9):
        values = [
            multinomial((i, j - i - 1, 8 - j))
            for j in range(i + 1, 9)
        ]
        outgoing.append(lcm(*values) if values else 1)
    for j in range(9):
        values = [
            multinomial((i, j - i - 1, 8 - j))
            for i in range(j)
        ]
        incoming.append(lcm(*values) if values else 1)
    return tuple(outgoing), tuple(incoming)


def affine_add(
    left: tuple[int, int, int], right: tuple[int, int, int]
) -> tuple[int, int, int]:
    return tuple(a + b for a, b in zip(left, right, strict=True))


def affine_scale(
    scalar: int, value: tuple[int, int, int]
) -> tuple[int, int, int]:
    return tuple(scalar * entry for entry in value)


def symbolic_certificate() -> None:
    # Expressions are stored as coefficients of (1,k,l).
    a = (-35, 105, 0)
    b = (35, 315, 420)
    one = (1, 0, 0)
    d = []
    for i in range(9):
        value = affine_scale(560, one)
        value = affine_add(value, affine_scale(U[i], a))
        value = affine_add(value, affine_scale(V[i], b))
        d.append(value)
    assert d[1] == (840, -420, 420)
    assert d[2] == (-420, 0, -2940)
    assert d[3] == (2520, 2940, 8820)

    # d2 >= 0 forces l <= -1.  Then d3 >= 0 forces k >= -3l,
    # whereas d1 >= 0 forces k <= l+2.  For every integer l <= -1,
    # -3l > l+2, since -4l >= 4 > 2.
    assert -4 * (-1) > 2


def load_position_types() -> list[tuple[int, int]]:
    path = (
        Path(__file__).resolve().parents[1]
        / "sequence_covering_sca79_point_link_flow"
        / "RESULTS.tsv"
    )
    types = []
    active = False
    for line in path.read_text(encoding="ascii").splitlines():
        if line == "[position_types]":
            active = True
            continue
        if line.startswith("["):
            active = False
        elif active and line:
            types.append(tuple(map(int, line.split("\t"))))
    return types


def main() -> None:
    for power in range(7):
        assert sum((i**power) * U[i] for i in range(9)) == 0
        assert sum((i**power) * V[i] for i in range(9)) == 0

    outgoing, incoming = positional_lcms()
    assert outgoing == (105, 420, 210, 420, 105, 42, 7, 1, 1)
    assert incoming == (1, 1, 7, 42, 105, 420, 210, 420, 105)
    symbolic_certificate()

    # Independent audit against the complete earlier point-position census.
    position_types = load_position_types()
    outgoing_survivors = 0
    incoming_survivors = 0
    for a, b in position_types:
        d = tuple(560 + a * U[i] + b * V[i] for i in range(9))
        assert min(d) >= 0 and sum(d) == 5040
        outgoing_survivors += int(
            all(d[i] % outgoing[i] == 0 for i in range(8))
        )
        incoming_survivors += int(
            all(d[i] % incoming[i] == 0 for i in range(1, 9))
        )
    assert len(position_types) == 1695
    assert outgoing_survivors == incoming_survivors == 0

    excluded_small_supports = sum(comb(72, r) for r in range(9))

    print("outgoing positional lcms:", " ".join(map(str, outgoing)))
    print("incoming positional lcms:", " ".join(map(str, incoming)))
    print("symbolic nonnegativity contradiction: verified")
    print("point-position types audited: 1695")
    print("all-outgoing-symmetric types: 0")
    print("all-incoming-symmetric types: 0")
    print("minimum asymmetric ordered-pair links: 9")
    print("supports of size at most 8 excluded:", excluded_small_supports)
    print("all checks passed")


if __name__ == "__main__":
    main()
