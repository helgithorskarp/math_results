#!/usr/bin/env python3
"""Clean-room checks for the disconnected Type-II branch of Dean k=5.

This script does not import the computational supplement.  It directly
implements the displayed definitions of the reduced 1+2 state and derives
the final 2+2 noncoverage conclusion from the projection table in Proposition
B.5 of the reviewed paper.
"""

from __future__ import annotations

from functools import lru_cache
from itertools import combinations, product


ONE_TWO_ORDERS = (7, 9, 11, 13, 17, 19, 21, 23, 27, 29, 31, 33)
TWO_TWO_ORDERS = ONE_TWO_ORDERS + (37, 39, 41, 43)


def mod5(value: int) -> int:
    return value % 5


def feet(n: int, start: int, kind: str) -> tuple[int, ...]:
    if kind == "S":
        return (start % n,)
    assert kind == "D"
    return tuple(dict.fromkeys((start % n, (start + 2) % n)))


@lru_cache(maxsize=None)
def arc(n: int, start: int, end: int, step: int) -> tuple[int, ...] | None:
    """The literal oriented simple arc; equality means the trivial arc."""
    assert step in (-1, 1)
    if start == end:
        return (start,) if step == 1 else None
    result = [start]
    current = start
    while current != end:
        current = (current + step) % n
        result.append(current)
    return tuple(result)


def good_triples() -> tuple[tuple[int, ...], ...]:
    rows = {
        tuple(sorted({a, mod5(a + d), mod5(a + 2 * d)}))
        for a in range(5)
        for d in (1, 2)
    }
    return tuple(sorted(rows))


PAIRS = tuple(combinations(range(5), 2))
GOOD_TRIPLES = good_triples()


def avoids_zero(*sets: tuple[int, ...] | frozenset[int]) -> bool:
    sums = {0}
    for values in sets:
        sums = {mod5(a + b) for a in sums for b in values}
    return 0 not in sums


@lru_cache(maxsize=None)
def closing_residues(
    n: int, left: tuple[int, ...], right: tuple[int, ...]
) -> frozenset[int]:
    """Residues of one ear's two attachment edges and a literal cycle arc."""
    out: set[int] = set()
    for x in left:
        for y in right:
            for step in (-1, 1):
                path = arc(n, x, y, step)
                if path is not None:
                    out.add(mod5(len(path) - 1 + 2))
    return frozenset(out)


@lru_cache(maxsize=None)
def cross_constants(
    n: int,
    probe_feet: tuple[int, ...],
    selected_pair: tuple[int, ...],
    landing_feet: tuple[int, ...],
) -> frozenset[int]:
    """Fixed residues of simple cycles using one ear from each component."""
    out: set[int] = set()
    for first, second in (
        (selected_pair, landing_feet),
        (landing_feet, selected_pair),
    ):
        for w in probe_feet:
            for x in first:
                for y in second:
                    for step1 in (-1, 1):
                        path1 = arc(n, w, x, step1)
                        if path1 is None:
                            continue
                        vertices1 = set(path1)
                        for step2 in (-1, 1):
                            path2 = arc(n, y, 0, step2)
                            if path2 is None or vertices1.intersection(path2):
                                continue
                            out.add(mod5(len(path1) + len(path2) + 2))
                            # The expression is (|P1|-1)+(|P2|-1)+4.
    return frozenset(out)


def has_two_probe_positions(
    rows: list[tuple[tuple[int, ...], tuple[int, ...]]]
) -> bool:
    """Two probe rows may repeat but must expose two positions besides zero."""
    for i, (feet1, _) in enumerate(rows):
        for feet2, _ in rows[i:]:
            if len({0, *feet1, *feet2}) >= 3:
                return True
    return False


def audit_one_two(n: int) -> tuple[int, int]:
    probe_rows: list[tuple[tuple[int, ...], tuple[int, ...]]] = []
    for kind in ("S", "D"):
        for w in range(n):
            probe_feet = feet(n, w, kind)
            outside = closing_residues(n, (0,), probe_feet)
            for residues in GOOD_TRIPLES:
                if avoids_zero(residues, outside):
                    probe_rows.append((probe_feet, residues))

    survivors = 0
    bad = 0
    for base in range(n):
        selected_pair = feet(n, base, "D")
        for kind in ("S", "D"):
            for landing in range(n):
                landing_feet = feet(n, landing, kind)
                if len(set(selected_pair).union(landing_feet)) < 3:
                    continue
                local = closing_residues(n, selected_pair, landing_feet)
                for pair in PAIRS:
                    if not avoids_zero(pair, local):
                        continue
                    compatible: list[tuple[tuple[int, ...], tuple[int, ...]]] = []
                    for probe_feet, triple in probe_rows:
                        constants = cross_constants(
                            n, probe_feet, selected_pair, landing_feet
                        )
                        if constants and avoids_zero(triple, pair, constants):
                            compatible.append((probe_feet, triple))
                    if has_two_probe_positions(compatible):
                        survivors += 1
                        if kind != "S" or landing != (base + 1) % n:
                            bad += 1
    return survivors, bad


def offset_allowed(n: int, offset: int) -> bool:
    """The exact Delta_n table in Proposition B.5."""
    q = n % 5
    offset %= n
    if q == 2:
        return False
    if q == 1:
        return offset in (0, 1, n - 1)
    if q == 3:
        return n != 13 and offset == 0
    assert q == 4
    return offset in (0, 1, n - 1) or offset % 5 == 2


def relative(n: int, position: int, origin: int) -> int:
    return (position - origin) % n


def selected_feet(n: int, base: int) -> set[int]:
    return {base, (base + 2) % n}


def base_cliques(n: int) -> list[tuple[int, ...]]:
    """All possible distinct selected-base sets, normalized to contain zero."""
    result: list[tuple[int, ...]] = []
    for size in range(1, 5):
        for rest in combinations(range(1, n), size - 1):
            bases = (0, *rest)
            if all(
                offset_allowed(n, (right - left) % n)
                for left, right in combinations(bases, 2)
            ):
                result.append(bases)
    # The table itself forces clique number at most three.
    assert not any(len(bases) == 4 for bases in result)
    return result


def audit_two_two_coverage(n: int) -> tuple[int, int]:
    """Exhaust the paper's global coverage deduction from Proposition B.5."""
    q = n % 5
    cases = 0
    full_cover_cases = 0

    for bases in base_cliques(n):
        # With a single base there are at least two exterior components, so
        # the zero offset must itself support a K_2,2 projection.
        if len(bases) == 1 and not offset_allowed(n, 0):
            continue

        broad = {
            base: set(range(n)).difference(selected_feet(n, base))
            for base in bases
        }
        adjacent_disjunctions: list[
            tuple[int, set[int], int, set[int]]
        ] = []

        if len(bases) == 1:
            base = bases[0]
            if q == 1:
                broad[base] &= {
                    z for z in range(n) if relative(n, z, base) % 5 != 2
                }
            elif q == 3:
                broad[base] &= {
                    z for z in range(n) if relative(n, z, base) % 5 in (1, 4)
                }
            elif q == 4:
                broad[base] &= {
                    z
                    for z in range(n)
                    if relative(n, z, base) == 1
                    or relative(n, z, base) % 5 == 3
                }

        for a, b in combinations(bases, 2):
            distance = relative(n, b, a)
            if distance == n - 1:
                left, right = b, a
                distance = 1
            else:
                left, right = a, b

            if distance == 1:
                if q == 1:
                    broad[left] &= {
                        z
                        for z in range(n)
                        if relative(n, z, left) in (1, 3)
                        or relative(n, z, left) % 5 == 4
                    }
                    broad[right] &= {
                        z
                        for z in range(n)
                        if relative(n, z, left) in (0, 2)
                        or relative(n, z, left) % 5 == 0
                    }
                elif q == 4:
                    broad[left] &= {
                        z
                        for z in range(n)
                        if relative(n, z, left) == 1
                        or relative(n, z, left) % 5 == 3
                    }
                    broad[right] &= {
                        z
                        for z in range(n)
                        if relative(n, z, left) in (0, 2)
                        or relative(n, z, left) % 5 == 4
                    }
                    adjacent_disjunctions.append(
                        (
                            left,
                            {(left + 1) % n, (left + 3) % n},
                            right,
                            {left, (left + 2) % n},
                        )
                    )
            elif q == 4:
                assert distance % 5 == 2
                exact = {(left + 1) % n, (right + 1) % n}
                broad[left] &= exact
                broad[right] &= exact
            else:
                raise AssertionError((n, bases, a, b, distance))

        for choices in product((0, 1), repeat=len(adjacent_disjunctions)):
            allowed = {base: set(values) for base, values in broad.items()}
            for choice, (left, left_narrow, right, right_narrow) in zip(
                choices, adjacent_disjunctions
            ):
                if choice == 0:
                    allowed[left] &= left_narrow
                else:
                    allowed[right] &= right_narrow

            possible_boundary: set[int] = set()
            for base in bases:
                possible_boundary.update(selected_feet(n, base))
                possible_boundary.update(allowed[base])
            cases += 1
            if len(possible_boundary) == n:
                full_cover_cases += 1

    return cases, full_cover_cases


def expected_representatives(maximum: int) -> tuple[int, ...]:
    return tuple(n for n in range(7, maximum + 1, 2) if n % 5)


def main() -> None:
    # Reducing at most six/eight positive marked gaps modulo five, followed
    # by one parity correction of five, yields these complete safe lists.
    assert ONE_TWO_ORDERS == expected_representatives(33)
    assert TWO_TWO_ORDERS == expected_representatives(43)

    one_two_total = 0
    one_two_bad = 0
    for n in ONE_TWO_ORDERS:
        survivors, bad = audit_one_two(n)
        one_two_total += survivors
        one_two_bad += bad
        print(f"1+2 n={n}: survivors={survivors}, nonmidpoint={bad}")
    assert one_two_bad == 0

    coverage_cases = 0
    fully_covered = 0
    for n in TWO_TWO_ORDERS:
        cases, bad = audit_two_two_coverage(n)
        coverage_cases += cases
        fully_covered += bad
        print(f"2+2 n={n}: base/branch cases={cases}, fully-covered={bad}")
    assert fully_covered == 0

    print("PASS Dean-5 disconnected Type-II audit")
    print(f"1+2 reduced survivors: {one_two_total}; nonmidpoint: {one_two_bad}")
    print(
        f"2+2 base/branch cases: {coverage_cases}; fully-covered: {fully_covered}"
    )


if __name__ == "__main__":
    main()
