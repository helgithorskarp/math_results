#!/usr/bin/env python3
"""Clean-room arithmetic audit of the Dean-5 periodic split-apex closure.

This script does not import the claimed proof's computational supplement.  It
implements the definitions in equations (A.8)--(A.12) and Appendix B.9 of
version 1.0.1 directly, then checks several deductions used between the finite
tables and the graph-theoretic conclusion.
"""

from __future__ import annotations

from collections import deque


FORBIDDEN = frozenset({0, 3})
BAD_SEPARATIONS = {
    1: frozenset({1, 2}),
    5: frozenset({3, 4}),
    7: frozenset({4, 0}),
    9: frozenset({0, 1}),
}


def cycle_arc_lengths(order: int, start: int, end: int) -> frozenset[int]:
    """The two simple arc lengths, with only length zero at equal ends."""
    start %= order
    end %= order
    if start == end:
        return frozenset({0})
    return frozenset({(end - start) % order, (start - end) % order})


def safe_ear_starts(order: int, left_type: int, right_type: int) -> frozenset[int]:
    """Definition of E_d(i,j) in Appendix B.9."""
    arc_residues: set[int] = set()
    for left_attachment in (left_type - 1, left_type + 1):
        for right_attachment in (right_type - 1, right_type + 1):
            arc_residues.update(
                length % 10
                for length in cycle_arc_lengths(
                    order, left_attachment, right_attachment
                )
            )
    starts: set[int] = set()
    parity = (right_type - left_type) % 2
    for start in range(parity, 10, 2):
        if all(
            (ear_length + arc) % 10 not in FORBIDDEN
            for ear_length in (start, start + 2)
            for arc in arc_residues
        ):
            starts.add(start)
    return frozenset(starts)


def expected_ear_starts(order: int, separation: int) -> frozenset[int]:
    """The claimed tight-pair table (A.11)."""
    residue = order % 10
    if residue == 1:
        if separation % 10 == 4:
            return frozenset({0})
        if separation % 10 == 9:
            return frozenset({5})
    elif residue == 5:
        if separation == 0:
            return frozenset({2, 4})
        if separation % 10 == 1:
            return frozenset({3})
        if separation % 10 == 6:
            return frozenset({8})
    elif residue == 7:
        if separation == 0:
            return frozenset({2, 4})
        if separation == 1:
            return frozenset({1, 3})
        if separation % 10 == 2:
            return frozenset({2})
        if separation % 10 == 7:
            return frozenset({7})
    elif residue == 9:
        if separation == 0:
            return frozenset({2})
        if separation == 1:
            return frozenset({1})
        if separation == 2:
            return frozenset({2})
        if separation % 10 == 3:
            return frozenset({1})
        if separation % 10 == 8:
            return frozenset({6})
    return frozenset()


def safe_module_starts(order: int, separation: int) -> frozenset[int]:
    """Definition of P_d(t) in Appendix B.9, including path parity."""
    short_arc = min(separation, order - separation)
    starts: set[int] = set()
    for start in range(separation % 2, 10, 2):
        closures = {
            (start + 2 * shift + arc) % 10
            for shift in range(3)
            for arc in (short_arc, order - short_arc)
        }
        if closures.isdisjoint(FORBIDDEN):
            starts.add(start)
    return frozenset(starts)


def safe_module_starts_without_parity(order: int, separation: int) -> frozenset[int]:
    short_arc = min(separation, order - separation)
    return frozenset(
        start
        for start in range(10)
        if {
            (start + 2 * shift + arc) % 10
            for shift in range(3)
            for arc in (short_arc, order - short_arc)
        }.isdisjoint(FORBIDDEN)
    )


def verify_periodic_tables(max_order: int = 501) -> tuple[int, int]:
    """Check the exact tables well beyond the supplement's d <= 119 range."""
    tight_rows = 0
    module_rows = 0
    for order in range(9, max_order + 1, 2):
        if order % 10 not in BAD_SEPARATIONS:
            continue
        # Translation around the cycle makes E_d(i,j) depend on d and j-i.
        # We nevertheless count every Appendix-B.9 parameter row.
        for separation in range(order - 1):
            got = safe_ear_starts(order, 1, 1 + separation)
            want = expected_ear_starts(order, separation)
            assert got == want, (order, separation, got, want)
            tight_rows += order - 1 - separation
        for separation in range(1, order):
            got = safe_module_starts(order, separation)
            want_empty = separation % 5 in BAD_SEPARATIONS[order % 10]
            assert (not got) == want_empty, (order, separation, got)
            module_rows += 1
    return tight_rows, module_rows


def verify_published_row_counts() -> tuple[int, int]:
    tight_rows = 0
    module_rows = 0
    for order in range(9, 120, 2):
        if order % 10 not in BAD_SEPARATIONS:
            continue
        tight_rows += (order - 1) * order // 2
        module_rows += order - 1
    assert tight_rows == 115_173
    assert module_rows == 2_846
    return tight_rows, module_rows


def verify_support_shapes(max_order: int = 201) -> None:
    """Exhaust the pairwise-compatible support shapes in (A.13)."""
    for order in range(9, max_order + 1, 2):
        residue = order % 10
        if residue not in BAD_SEPARATIONS:
            continue
        types = range(1, order)
        neighbors = {
            i: {
                j
                for j in types
                if j != i and expected_ear_starts(order, abs(i - j))
            }
            for i in types
        }
        if residue == 1:
            assert all(not safe_ear_starts(order, i, i) for i in types)
            for i in types:
                for j in neighbors[i]:
                    assert not (neighbors[i] & neighbors[j]), (order, i, j)
        elif residue == 5:
            for i in types:
                for j in neighbors[i]:
                    assert abs(i - j) % 5 == 1
                    assert not (neighbors[i] & neighbors[j]), (order, i, j)
        elif residue in {7, 9}:
            local_width = 2 if residue == 7 else 3
            far_minimum = 7 if residue == 7 else 8
            far_modulus = 2 if residue == 7 else 3
            for i in types:
                for j in neighbors[i]:
                    separation = abs(i - j)
                    if separation > local_width:
                        assert separation >= far_minimum
                        assert separation % 5 == far_modulus
                        # A far pair is the entire distinct-type support.
                        assert not (neighbors[i] & neighbors[j]), (order, i, j)


def verify_bad_root_connectivity(max_order: int = 501) -> None:
    """Check connectivity of Gamma_d throughout and beyond the stated ranges."""
    starts = {1: 11, 5: 15, 7: 17, 9: 9}
    for residue, first_order in starts.items():
        for order in range(first_order, max_order + 1, 10):
            vertices = set(range(1, order))
            seen = {1}
            queue = deque([1])
            while queue:
                current = queue.popleft()
                for candidate in vertices - seen:
                    if abs(candidate - current) % 5 in BAD_SEPARATIONS[residue]:
                        seen.add(candidate)
                        queue.append(candidate)
            assert seen == vertices, (order, len(seen), len(vertices))


def verify_small_distances() -> None:
    assert safe_module_starts_without_parity(5, 1) == frozenset({1, 3})
    assert safe_module_starts_without_parity(5, 2) == frozenset({2})
    expected_five = {
        0: frozenset({2, 4}),
        1: frozenset({3}),
        2: frozenset(),
        3: frozenset(),
    }
    for separation, want in expected_five.items():
        assert safe_ear_starts(5, 1, 1 + separation) == want

    expected_seven_modules = {
        1: frozenset({1, 6}),
        2: frozenset({0, 2}),
        3: frozenset({1}),
    }
    for separation, want in expected_seven_modules.items():
        assert safe_module_starts_without_parity(7, separation) == want
    expected_seven_ears = {
        0: frozenset({2, 4}),
        1: frozenset({1, 3}),
        2: frozenset({2}),
        3: frozenset(),
        4: frozenset(),
        5: frozenset(),
    }
    for separation, want in expected_seven_ears.items():
        assert safe_ear_starts(7, 1, 1 + separation) == want


def verify_split_side_arithmetic(max_order: int = 501) -> None:
    """Check the exceptional equality and the remote bad-root choices."""
    avoidable_displacements = {0, 2, 8}
    for order in range(9, max_order + 1, 2):
        if order % 10 not in {5, 7}:
            continue
        for center in range(2, order - 1):
            first = (2 * center - order - 3) % 10
            second = (first + 6) % 10
            both_parities_can_avoid = (
                first in avoidable_displacements
                and second in avoidable_displacements
            )
            equality_case = (2 * center - order) % 10 == 5
            assert both_parities_can_avoid == equality_case
            if equality_case:
                remote_separation = 4 if order % 10 == 5 else 5
                assert center - remote_separation >= 1
                assert (
                    remote_separation % 5
                    in BAD_SEPARATIONS[order % 10]
                )


def main() -> None:
    published_counts = verify_published_row_counts()
    extended_counts = verify_periodic_tables()
    verify_support_shapes()
    verify_bad_root_connectivity()
    verify_small_distances()
    verify_split_side_arithmetic()
    print(
        "Appendix B.9 published-range row counts:",
        f"tight={published_counts[0]}, module={published_counts[1]}",
    )
    print(
        "Exact table formulas through d=501:",
        f"tight={extended_counts[0]}, module={extended_counts[1]}: OK",
    )
    print("Derived support shapes through d=201: OK")
    print("Bad-root graph connectivity through d=501: OK")
    print("Distance-five and distance-seven tables: OK")
    print("Split-side and remote-root arithmetic through d=501: OK")


if __name__ == "__main__":
    main()
