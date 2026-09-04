#!/usr/bin/env python3
"""Independent exact checks for modular residue-slab composition.

Standard-library CPython only.  Small rectangle bases are found by a generic
exact-cover search; this file does not import the submitted cyclic constructor.
The universal proof is in README.md.
"""

from __future__ import annotations

import itertools
import math
from functools import lru_cache
from typing import Sequence


Cell = tuple[int, ...]
Part = tuple[Cell, ...]


def is_line(part: Sequence[Cell]) -> bool:
    """Return whether a nonempty set of cells lies in one coordinate line."""
    if not part or len(set(part)) != len(part):
        return False
    dimension = len(part[0])
    if any(len(cell) != dimension for cell in part):
        return False
    varying = sum(len({cell[i] for cell in part}) > 1 for i in range(dimension))
    return varying <= 1


def validate_partition(
    parts: Sequence[Part], dimensions: Sequence[int], s: int
) -> None:
    expected = set(itertools.product(*(range(side) for side in dimensions)))
    seen: set[Cell] = set()
    for part in parts:
        assert len(part) >= s
        assert is_line(part)
        assert seen.isdisjoint(part)
        seen.update(part)
    assert seen == expected
    assert len(parts) == math.prod(dimensions) // s


@lru_cache(maxsize=None)
def exact_rectangle_partition(m: int, n: int, s: int) -> tuple[Part, ...]:
    """Find an optimal small rectangle partition by deterministic Algorithm X.

    An optimal Q-part partition has total excess tau=mn-sQ, so it suffices to
    enumerate line subsets of sizes s through s+tau.  This search is wholly
    independent of the submitted cyclic formula.
    """
    assert 2 <= s <= min(m, n)
    total = m * n
    quotient, excess = divmod(total, s)
    candidates: list[int] = []

    for row in range(m):
        line = [row * n + column for column in range(n)]
        for size in range(s, min(len(line), s + excess) + 1):
            for subset in itertools.combinations(line, size):
                candidates.append(sum(1 << cell for cell in subset))
    for column in range(n):
        line = [row * n + column for row in range(m)]
        for size in range(s, min(len(line), s + excess) + 1):
            for subset in itertools.combinations(line, size):
                candidates.append(sum(1 << cell for cell in subset))

    through_cell: list[list[int]] = [[] for _ in range(total)]
    for index, mask in enumerate(candidates):
        bits = mask
        while bits:
            low = bits & -bits
            through_cell[low.bit_length() - 1].append(index)
            bits ^= low

    @lru_cache(maxsize=None)
    def search(uncovered: int, parts_left: int) -> tuple[int, ...] | None:
        cells_left = uncovered.bit_count()
        extra_left = cells_left - s * parts_left
        if parts_left == 0:
            return () if uncovered == 0 else None
        if extra_left < 0 or extra_left > excess:
            return None

        best_options: list[int] | None = None
        bits = uncovered
        while bits:
            low = bits & -bits
            cell = low.bit_length() - 1
            bits ^= low
            options = [
                index
                for index in through_cell[cell]
                if candidates[index] & uncovered == candidates[index]
                and candidates[index].bit_count() - s <= extra_left
            ]
            if not options:
                return None
            if best_options is None or len(options) < len(best_options):
                best_options = options

        assert best_options is not None
        best_options.sort(key=lambda index: (-candidates[index].bit_count(), index))
        for index in best_options:
            mask = candidates[index]
            suffix = search(uncovered ^ mask, parts_left - 1)
            if suffix is not None:
                return (mask,) + suffix
        return None

    masks = search((1 << total) - 1, quotient)
    assert masks is not None
    parts: list[Part] = []
    for mask in masks:
        part = tuple(
            divmod(index, n) for index in range(total) if (mask >> index) & 1
        )
        parts.append(part)
    validate_partition(parts, (m, n), s)
    return tuple(parts)


def compose(
    base_parts: Sequence[Part],
    base_dimensions: Sequence[int],
    p: int,
    s: int,
) -> tuple[Part, ...]:
    """Apply the residue-slab construction to a checked optimal base."""
    validate_partition(base_parts, base_dimensions, s)
    base_volume = math.prod(base_dimensions)
    slab_count, c = divmod(p, s)
    base_quotient, tau = divmod(base_volume, s)
    assert len(base_parts) == base_quotient
    if c * tau >= s:
        raise ValueError("residue-slab criterion fails")

    result: list[Part] = []
    for base_cell in itertools.product(*(range(side) for side in base_dimensions)):
        for block in range(slab_count):
            result.append(
                tuple(base_cell + (last,) for last in range(block * s, (block + 1) * s))
            )
    cutoff = slab_count * s
    for last in range(cutoff, p):
        for base_part in base_parts:
            result.append(tuple(cell + (last,) for cell in base_part))

    assert len(result) == slab_count * base_volume + c * base_quotient
    validate_partition(result, tuple(base_dimensions) + (p,), s)
    return tuple(result)


def audit_floor_identity(max_s: int = 80) -> int:
    checked = 0
    for s in range(2, max_s + 1):
        for volume in range(s, 4 * s + 6):
            quotient, tau = divmod(volume, s)
            for p in range(1, 4 * s + 6):
                slabs, c = divmod(p, s)
                if c * tau >= s:
                    continue
                assert slabs * volume + c * quotient == volume * p // s
                checked += 1
    return checked


def audit_small_compositions() -> tuple[int, int, int, int]:
    rectangles = 0
    compositions = 0
    composed_parts = 0
    beyond_old = 0
    for s in range(2, 6):
        for m in range(s, s + 4):
            for n in range(m, s + 4):
                base = exact_rectangle_partition(m, n, s)
                rectangles += 1
                tau = (m * n) % s
                for p in range(1, 2 * s + 4):
                    if (p % s) * tau >= s:
                        continue
                    parts = compose(base, (m, n), p, s)
                    compositions += 1
                    composed_parts += len(parts)
                    if p * tau >= s:
                        beyond_old += 1
    return rectangles, compositions, composed_parts, beyond_old


def audit_iterated_compositions() -> int:
    """Check the compact product criterion for two appended coordinates."""
    checked = 0
    for s in range(2, 6):
        dimensions = (s + 1, s + 2)
        base = exact_rectangle_partition(*dimensions, s)
        tau = math.prod(dimensions) % s
        for p in range(1, s + 3):
            for q in range(1, s + 3):
                if tau * (p % s) * (q % s) >= s:
                    continue
                appendages = [p, q]
                appendages.sort(key=lambda side: (side % s != 0, side))
                parts: tuple[Part, ...] = base
                current_dimensions = dimensions
                for side in appendages:
                    parts = compose(parts, current_dimensions, side, s)
                    current_dimensions += (side,)
                validate_partition(parts, current_dimensions, s)
                assert math.prod(current_dimensions) % s == (
                    tau * (p % s) * (q % s)
                )
                checked += 1
    return checked


def previous_criterion(sides: Sequence[int], s: int) -> bool:
    residues = [side % s for side in sides]
    residue_volume = math.prod(residues)
    if residue_volume < s:
        return True
    if residue_volume < 2 * s and sum(residues) >= s + 2:
        return True
    return s == 3 and residues == [2, 2, 2]


def qualifying_old_layering(sides: Sequence[int], s: int) -> bool:
    for first, second in itertools.combinations(range(3), 2):
        remaining = 3 - first - second
        pair_remainder = sides[first] * sides[second] % s
        if sides[remaining] * pair_remainder < s:
            return True
    return False


def family_arithmetic(max_k: int = 10_000) -> int:
    checked = 0
    for k in range(2, max_k + 1):
        orders = (3 * k + 6, 3 * k + 2, 2 * k + 3, 2 * k + 3)
        deficits = tuple(order - 1 for order in orders)
        h = (sum(deficits) + 1) // 2
        s = h - deficits[0] + 1
        sides = orders[1:]
        residues = tuple(side % s for side in sides)
        assert orders == tuple(sorted(orders, reverse=True))
        assert h == 5 * k + 5 and s == 2 * k + 1
        assert residues == (k + 1, 2, 2)
        assert (sides[0] * sides[1]) % s == 1
        assert (sides[2] % s) * ((sides[0] * sides[1]) % s) == 2 < s
        quotient = 6 * k * k + 19 * k + 16
        assert math.prod(sides) == s * quotient + 2
        assert all(residue != 0 for residue in residues)
        assert all(
            (residues[i] * residues[j]) % s != 0
            for i, j in itertools.combinations(range(3), 2)
        )
        assert math.prod(residues) == 2 * s + 2
        assert not previous_criterion(sides, s)
        assert not qualifying_old_layering(sides, s)
        checked += 1
    return checked


def explicit_hamming_witness() -> tuple[int, int, int, int]:
    """Construct and directly audit the k=2 colouring on all 4,704 vertices."""
    n1, n2, n3, n4 = (12, 8, 7, 7)
    s, h = (5, 15)
    base = exact_rectangle_partition(n2, n3, s)
    minor_parts = compose(base, (n2, n3), n4, s)
    assert len(minor_parts) == 78

    colour_of: dict[Cell, int] = {}
    for colour, part in enumerate(minor_parts):
        for cell in part:
            assert cell not in colour_of
            colour_of[cell] = colour
    assert len(colour_of) == n2 * n3 * n4

    minimum = n1 + n2 + n3 + n4
    maximum = 0
    vertices = 0
    for first in range(n1):
        for minor in itertools.product(range(n2), range(n3), range(n4)):
            colour = colour_of[minor]
            same = n1 - 1
            for direction, side in enumerate((n2, n3, n4)):
                for value in range(side):
                    if value == minor[direction]:
                        continue
                    neighbour = list(minor)
                    neighbour[direction] = value
                    same += colour_of[tuple(neighbour)] == colour
            assert same >= h
            minimum = min(minimum, same)
            maximum = max(maximum, same)
            vertices += 1
    assert vertices == n1 * n2 * n3 * n4
    return vertices, len(minor_parts), minimum, maximum


def main() -> None:
    identities = audit_floor_identity()
    rectangles, compositions, parts, beyond_old = audit_small_compositions()
    iterated = audit_iterated_compositions()
    family = family_arithmetic()
    vertices, colours, minimum, maximum = explicit_hamming_witness()
    print(f"floor identities checked: {identities}")
    print(f"independent exact-cover rectangle bases: {rectangles}")
    print(f"small modular compositions checked: {compositions}")
    print(f"composed line parts checked: {parts}")
    print(f"small compositions beyond old full-side test: {beyond_old}")
    print(f"iterated two-coordinate compositions checked: {iterated}")
    print(f"infinite-family indices checked: {family}")
    print(f"K12xK8xK7xK7 vertices checked: {vertices}")
    print(f"K12xK8xK7xK7 colours: {colours}")
    print(f"same-colour neighbour range: {minimum}..{maximum}")
    print("all independent checks passed")


if __name__ == "__main__":
    main()
