#!/usr/bin/env python3
"""Definition-level audit of the forced U,U white graph and joint orbits."""

from collections import defaultdict
from itertools import combinations, permutations, product


N = 10
WHITE_DEGREES = (1,) * 6 + (2,) * 2 + (3,) * 2
DARK_EDGES = frozenset(
    (p, q)
    for p in range(6, N)
    for q in range(6, N)
    if p >= 8 or q >= 8
)
OMEGAS = (
    ((0, 1, 2, 3), (1, 2, 3, 0), (2, 3, 0, 1), (3, 0, 1, 2)),
    ((0, 1, 2, 3), (1, 0, 3, 2), (2, 3, 0, 1), (3, 2, 1, 0)),
)


def enumerate_white_graphs():
    """Enumerate all simple bipartite degree realizations avoiding DARK_EDGES."""
    row_order = (8, 9, 6, 7, 0, 1, 2, 3, 4, 5)
    remaining = list(WHITE_DEGREES)
    chosen = []
    graphs = []

    def search(depth):
        if depth == len(row_order):
            if remaining == [0] * N:
                graphs.append(frozenset(chosen))
            return
        p = row_order[depth]
        degree = WHITE_DEGREES[p]
        candidates = [
            q for q in range(N)
            if remaining[q] and (p, q) not in DARK_EDGES
        ]
        for neighbours in combinations(candidates, degree):
            for q in neighbours:
                remaining[q] -= 1
                chosen.append((p, q))
            if all(value >= 0 for value in remaining):
                search(depth + 1)
            for q in reversed(neighbours):
                assert chosen.pop() == (p, q)
                remaining[q] += 1

    search(0)
    return graphs


def expected_white_shape(graph):
    low_square = {(p, q) for p in (6, 7) for q in (6, 7)}
    if not low_square <= graph:
        return False
    if any(q >= 6 for p, q in graph if p >= 8):
        return False
    if any(p >= 6 for p, q in graph if q >= 8):
        return False
    return True


def swap(value, a, b):
    if value == a:
        return b
    if value == b:
        return a
    return value


def joint_orbits():
    dark_matchings = [
        frozenset(pair)
        for pair in combinations(DARK_EDGES, 2)
        if pair[0][0] != pair[1][0] and pair[0][1] != pair[1][1]
    ]
    group = tuple(product((0, 1), repeat=4))

    def act(state, element):
        matching, bit = state
        swap_plow, swap_phigh, swap_qlow, swap_qhigh = element
        image = []
        for p, q in matching:
            if swap_plow:
                p = swap(p, 6, 7)
            if swap_phigh:
                p = swap(p, 8, 9)
            if swap_qlow:
                q = swap(q, 6, 7)
            if swap_qhigh:
                q = swap(q, 8, 9)
            image.append((p, q))
        return frozenset(image), bit ^ swap_qhigh

    def state_key(state):
        matching, bit = state
        return tuple(sorted(matching)), bit

    states = {(matching, bit) for matching in dark_matchings for bit in (0, 1)}
    orbits = []
    while states:
        representative = min(states, key=state_key)
        orbit = {act(representative, element) for element in group}
        assert orbit <= states | set().union(*orbits)
        orbits.append(orbit)
        states -= orbit
    representatives = [state_key(min(orbit, key=state_key)) for orbit in orbits]
    return len(dark_matchings), representatives, [len(orbit) for orbit in orbits]


def cell_attributes(omega, cell):
    column, lrow = divmod(cell, 4)
    return column, lrow, omega[lrow][column]


def compatible_cells(omega, first, second):
    return all(
        a != b
        for a, b in zip(
            cell_attributes(omega, first), cell_attributes(omega, second)
        )
    )


def component_patterns(omega, kind, fixed_lrow=None):
    """Count labelled valid cell assignments by their 16-bit support."""
    size = 3 if kind == "star" else 4
    fixed_cell = fixed_lrow  # column zero, with source row fixed_lrow
    if fixed_lrow is not None:
        sequences = (
            (fixed_cell,) + tail
            for tail in permutations(
                [cell for cell in range(16) if cell != fixed_cell], size - 1
            )
        )
    else:
        sequences = permutations(range(16), size)
    patterns = defaultdict(int)
    for sequence in sequences:
        if kind == "star":
            required_pairs = combinations(range(3), 2)
        else:
            required_pairs = ((i, (i + 1) % 4) for i in range(4))
        if all(
            compatible_cells(omega, sequence[i], sequence[j])
            for i, j in required_pairs
        ):
            patterns[sum(1 << cell for cell in sequence)] += 1
    return patterns


def convolve_disjoint(first, second):
    result = defaultdict(int)
    for first_mask, first_count in first.items():
        for second_mask, second_count in second.items():
            if not first_mask & second_mask:
                result[first_mask | second_mask] += first_count * second_count
    return result


def white_cell_embedding_count(omega, fixed_lrow):
    """Count all anchored coordinate labellings of the five white components."""
    star = component_patterns(omega, "star")
    fixed_star = component_patterns(omega, "star", fixed_lrow=fixed_lrow)
    four_cycle = component_patterns(omega, "cycle")
    state = {0: 1}
    for component in (fixed_star, star, star, star, four_cycle):
        state = convolve_disjoint(state, component)
    return state.get((1 << 16) - 1, 0)


def fixed_star_pairs(omega, fixed_lrow):
    fixed_cell = fixed_lrow
    cells = [
        cell
        for cell in range(16)
        if cell != fixed_cell and compatible_cells(omega, fixed_cell, cell)
    ]
    result = []
    for first, second in combinations(cells, 2):
        if compatible_cells(omega, first, second):
            result.append(
                tuple((cell // 4, cell % 4) for cell in (first, second))
            )
    return result


def main():
    graphs = enumerate_white_graphs()
    assert len(graphs) == 400
    assert len(set(graphs)) == 400
    assert all(len(graph) == 16 for graph in graphs)
    assert all(expected_white_shape(graph) for graph in graphs)

    # The only labelled choices are the two complementary 3+3 partitions.
    assert {
        frozenset(q for p, q in graph if p == 8)
        for graph in graphs
    } == set(map(frozenset, combinations(range(6), 3)))
    assert {
        frozenset(p for p, q in graph if q == 8)
        for graph in graphs
    } == set(map(frozenset, combinations(range(6), 3)))

    matching_count, representatives, sizes = joint_orbits()
    expected_representatives = [
        (((6, 8), (7, 9)), 0),
        (((6, 8), (8, 6)), 0),
        (((6, 8), (8, 6)), 1),
        (((6, 8), (8, 9)), 0),
        (((6, 8), (8, 9)), 1),
        (((8, 6), (9, 7)), 0),
        (((8, 6), (9, 8)), 0),
        (((8, 6), (9, 8)), 1),
        (((8, 8), (9, 9)), 0),
    ]
    assert matching_count == 38
    assert representatives == expected_representatives
    assert sizes == [4, 16, 16, 8, 8, 4, 8, 8, 4]
    assert sum(sizes) == 2 * matching_count

    expected_fixedstar_pairs = [
        [
            ((1, 0), (2, 2)), ((1, 0), (3, 1)),
            ((1, 1), (2, 2)), ((1, 1), (3, 2)),
            ((2, 0), (3, 1)), ((2, 0), (3, 2)),
        ],
        [
            ((1, 0), (2, 2)), ((1, 0), (3, 1)),
            ((1, 1), (2, 0)), ((1, 1), (3, 2)),
            ((2, 0), (3, 2)), ((2, 2), (3, 1)),
        ],
    ]
    assert [fixed_star_pairs(omega, 3) for omega in OMEGAS] == expected_fixedstar_pairs
    assert all(
        len(fixed_star_pairs(omega, fixed_lrow)) == 6
        for omega in OMEGAS
        for fixed_lrow in (1, 2, 3)
    )
    embedding_counts = [
        [white_cell_embedding_count(omega, fixed_lrow) for fixed_lrow in (1, 2, 3)]
        for omega in OMEGAS
    ]
    assert embedding_counts == [[373248] * 3, [2985984] * 3]

    print("white_graphs=400")
    print("all_white_graphs_have_forced_shape=True")
    print("dark_matchings=38")
    print("joint_orbits=9")
    print("joint_orbit_sizes=" + ",".join(map(str, sizes)))
    print("fixed_star_cases_per_omega=6")
    print(
        "anchored_white_cell_embeddings="
        + ";".join(",".join(map(str, row)) for row in embedding_counts)
    )


if __name__ == "__main__":
    main()
