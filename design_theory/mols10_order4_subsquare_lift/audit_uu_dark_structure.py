#!/usr/bin/env python3
"""Exhaustive audits for the named dark-coordinate lemmas in type (U,U).

The first audit enumerates every simple 4-by-4 bipartite graph whose
degree sequence on both sides is (2,2,4,4).  The second enumerates every
labelled 6-by-6 zero-one matrix with all row and column sums two and
records the cycle partition of its bipartite support.
"""

from itertools import combinations, product


def audit_uu_intersection_graph() -> None:
    degrees = (2, 2, 4, 4)
    row_choices = [list(combinations(range(4), degree)) for degree in degrees]
    solutions = []
    for rows in product(*row_choices):
        column_degrees = tuple(sum(column in row for row in rows) for column in range(4))
        if column_degrees == degrees:
            solutions.append(rows)
    expected = ((2, 3), (2, 3), (0, 1, 2, 3), (0, 1, 2, 3))
    assert solutions == [expected]
    print("UU labelled dark-intersection graphs: 1")
    print("forced rows:", expected)


def cycle_partition(rows: list[tuple[int, int]]) -> tuple[int, ...]:
    adjacency = [[] for _ in range(12)]
    for row, columns in enumerate(rows):
        for column in columns:
            adjacency[row].append(6 + column)
            adjacency[6 + column].append(row)
    seen: set[int] = set()
    half_lengths = []
    for initial in range(12):
        if initial in seen:
            continue
        stack = [initial]
        seen.add(initial)
        size = 0
        while stack:
            vertex = stack.pop()
            size += 1
            for neighbour in adjacency[vertex]:
                if neighbour not in seen:
                    seen.add(neighbour)
                    stack.append(neighbour)
        assert size % 2 == 0
        half_lengths.append(size // 2)
    return tuple(sorted(half_lengths, reverse=True))


def audit_sigma_cycle_types() -> None:
    pairs = list(combinations(range(6), 2))
    column_degrees = [0] * 6
    rows: list[tuple[int, int]] = []
    counts: dict[tuple[int, ...], int] = {}

    def extend(row: int) -> None:
        if row == 6:
            if column_degrees == [2] * 6:
                kind = cycle_partition(rows)
                counts[kind] = counts.get(kind, 0) + 1
            return
        for pair in pairs:
            if all(column_degrees[column] < 2 for column in pair):
                rows.append(pair)
                for column in pair:
                    column_degrees[column] += 1
                extend(row + 1)
                for column in pair:
                    column_degrees[column] -= 1
                rows.pop()

    extend(0)
    expected = {(6,): 43200, (4, 2): 16200, (3, 3): 7200, (2, 2, 2): 1350}
    assert counts == expected
    assert sum(counts.values()) == 67950
    print("labelled Sigma supports:", sum(counts.values()))
    for kind in sorted(counts, reverse=True):
        print("cycle half-lengths", kind, "count", counts[kind])


def audit_first_column_matching_orbits() -> None:
    edges = [(p, q) for p in range(6, 10) for q in range(6, 10) if p >= 8 or q >= 8]
    matchings = {
        frozenset(pair)
        for pair in combinations(edges, 2)
        if pair[0][0] != pair[1][0] and pair[0][1] != pair[1][1]
    }

    actions = []
    for swap_pl, swap_ph, swap_ql, swap_qh in product(range(2), repeat=4):
        def action(edge, bits=(swap_pl, swap_ph, swap_ql, swap_qh)):
            p, q = edge
            if bits[0] and p in (6, 7):
                p = 13 - p
            if bits[1] and p in (8, 9):
                p = 17 - p
            if bits[2] and q in (6, 7):
                q = 13 - q
            if bits[3] and q in (8, 9):
                q = 17 - q
            return p, q
        actions.append(action)

    unseen = set(matchings)
    orbits = []
    while unseen:
        representative = min(unseen, key=lambda matching: sorted(matching))
        orbit = {
            frozenset(action(edge) for edge in representative)
            for action in actions
        }
        assert orbit <= matchings
        unseen -= orbit
        orbits.append((representative, orbit))

    expected_sizes = [2, 16, 8, 2, 8, 2]
    assert len(matchings) == 38
    assert sorted(len(orbit) for _, orbit in orbits) == sorted(expected_sizes)
    assert len(orbits) == 6
    print("column-0 dark matchings:", len(matchings))
    print("matching orbits:", len(orbits), "sizes", [len(orbit) for _, orbit in orbits])
    for index, (representative, _) in enumerate(orbits):
        print("orbit", index, "representative", tuple(sorted(representative)))


if __name__ == "__main__":
    audit_uu_intersection_graph()
    audit_sigma_cycle_types()
    audit_first_column_matching_orbits()
