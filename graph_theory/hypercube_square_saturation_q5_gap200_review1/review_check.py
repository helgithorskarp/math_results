#!/usr/bin/env python3
"""Independent reviewer checks for the parity-free Q5 gap-200 theorem.

This standard-library program does not import either target engine.  It
exhausts all Q5 edge subsets of size at most three to locate the first odd
deficit, rebuilds the seven residual Q4 automorphism orbits, checks their
statistics and boundary profiles, generates every residual facet placement
from multiset multiplicities, closes all placements by exact edge overlap,
and checks the global rational algebra.  It is not a third complete Q4
low-slack census.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from itertools import combinations, permutations, product
import json
from math import factorial


def cube_edges(dimension: int) -> tuple[tuple[int, int], ...]:
    return tuple(
        tuple(sorted((vertex, vertex ^ (1 << coordinate))))
        for vertex in range(1 << dimension)
        for coordinate in range(dimension)
        if vertex < (vertex ^ (1 << coordinate))
    )


def cube_squares(dimension: int) -> tuple[tuple[tuple[int, int], ...], ...]:
    squares = []
    for first, second in combinations(range(dimension), 2):
        for base in range(1 << dimension):
            if (base >> first) & 1 or (base >> second) & 1:
                continue
            squares.append(
                tuple(
                    tuple(sorted(edge))
                    for edge in (
                        (base, base ^ (1 << first)),
                        (base, base ^ (1 << second)),
                        (
                            base ^ (1 << first),
                            base ^ (1 << first) ^ (1 << second),
                        ),
                        (
                            base ^ (1 << second),
                            base ^ (1 << first) ^ (1 << second),
                        ),
                    )
                )
            )
    return tuple(squares)


Q4_EDGES = cube_edges(4)
Q4_SQUARES = cube_squares(4)
Q5_EDGES = cube_edges(5)
Q5_SQUARES = cube_squares(5)
Q4_FACETS = tuple((coordinate, bit) for coordinate in range(4) for bit in (0, 1))
Q5_FACETS = tuple((coordinate, bit) for coordinate in range(5) for bit in (0, 1))


def q5_three_subcubes() -> tuple[tuple[tuple[tuple[int, int], ...], ...], ...]:
    result = []
    for varying in combinations(range(5), 3):
        fixed = tuple(coordinate for coordinate in range(5) if coordinate not in varying)
        for bits in product((0, 1), repeat=2):
            base = sum(bit << coordinate for bit, coordinate in zip(bits, fixed))
            vertices = {
                base
                ^ sum(((mask >> position) & 1) << coordinate for position, coordinate in enumerate(varying))
                for mask in range(8)
            }
            squares = tuple(
                square
                for square in Q5_SQUARES
                if all(vertex in vertices for edge in square for vertex in edge)
            )
            if len(squares) != 6:
                raise AssertionError("incorrect Q3 subcube")
            result.append(squares)
    if len(result) != 40:
        raise AssertionError("incorrect number of Q3 subcubes in Q5")
    return tuple(result)


Q5_Q3_SQUARES = q5_three_subcubes()


def q5_deficit(chosen_edges: tuple[tuple[int, int], ...]) -> tuple[int, int]:
    chosen = frozenset(chosen_edges)
    twice_slack_sum = 0
    for squares in Q5_Q3_SQUARES:
        missing = []
        inactive_incidences = 0
        for square in squares:
            present = [edge for edge in square if edge in chosen]
            if len(present) == 4:
                raise ValueError("chosen set contains a square")
            if len(present) == 3:
                missing.append(next(edge for edge in square if edge not in chosen))
            else:
                inactive_incidences += len(present)
        repeated = len(missing) - len(set(missing))
        twice_slack_sum += 2 * inactive_incidences + 4 * repeated - len(missing)
    return 17 * twice_slack_sum - 12 * len(chosen), twice_slack_sum


def small_parity_audit() -> tuple[dict[str, dict[str, int]], dict[str, object]]:
    spectra = {}
    first_odd = None
    for size in range(4):
        values = Counter()
        for chosen in combinations(Q5_EDGES, size):
            deficit, twice_slack = q5_deficit(chosen)
            values[deficit] += 1
            if deficit % 2 and first_odd is None:
                first_odd = (chosen, deficit, twice_slack)
        spectra[str(size)] = {str(key): value for key, value in sorted(values.items())}
    if first_odd is None:
        raise AssertionError("no odd deficit found")
    chosen, deficit, twice_slack = first_odd
    if (len(chosen), deficit, twice_slack) != (3, 831, 51):
        raise AssertionError("unexpected smallest odd-deficit example")
    if any(int(key) % 2 for size in ("0", "1", "2") for key in spectra[size]):
        raise AssertionError("odd deficit occurs below three edges")
    return spectra, {
        "edges": [list(edge) for edge in chosen],
        "edge_count": len(chosen),
        "twice_slack": twice_slack,
        "deficit": deficit,
    }


def mask_edges(mask: int) -> frozenset[tuple[int, int]]:
    return frozenset(edge for index, edge in enumerate(Q4_EDGES) if (mask >> index) & 1)


def permute_vertex(vertex: int, permutation: tuple[int, ...]) -> int:
    result = 0
    for old_coordinate, new_coordinate in enumerate(permutation):
        result |= ((vertex >> old_coordinate) & 1) << new_coordinate
    return result


def transform(
    pattern: frozenset[tuple[int, int]],
    translation: int,
    permutation: tuple[int, ...],
) -> frozenset[tuple[int, int]]:
    return frozenset(
        tuple(
            sorted(
                (
                    permute_vertex(first, permutation) ^ translation,
                    permute_vertex(second, permutation) ^ translation,
                )
            )
        )
        for first, second in pattern
    )


def orbit(mask: int) -> tuple[frozenset[tuple[int, int]], ...]:
    pattern = mask_edges(mask)
    return tuple(
        frozenset(
            transform(pattern, translation, permutation)
            for translation in range(16)
            for permutation in permutations(range(4))
        )
    )


def q4_statistics(pattern: frozenset[tuple[int, int]]) -> tuple[int, int, int, int]:
    witnesses = []
    for square in Q4_SQUARES:
        present = [edge for edge in square if edge in pattern]
        if len(present) == 4:
            raise AssertionError("residual orbit contains a square")
        if len(present) == 3:
            witnesses.append(next(edge for edge in square if edge not in present))
    multiplicities = Counter(witnesses)
    pairs = sum(value * (value - 1) // 2 for value in multiplicities.values())
    edges = len(pattern)
    slack = 6 * edges - 7 * len(witnesses) + 2 * pairs
    return edges, len(witnesses), slack, 17 * slack - 3 * edges


def delete_coordinate(vertex: int, coordinate: int) -> int:
    result = 0
    target = 0
    for source in range(4):
        if source == coordinate:
            continue
        result |= ((vertex >> source) & 1) << target
        target += 1
    return result


def facet_signature(
    pattern: frozenset[tuple[int, int]], facet: tuple[int, int]
) -> frozenset[tuple[int, int]]:
    coordinate, bit = facet
    return frozenset(
        tuple(
            sorted(
                (
                    delete_coordinate(first, coordinate),
                    delete_coordinate(second, coordinate),
                )
            )
        )
        for first, second in pattern
        if ((first >> coordinate) & 1) == bit
        and ((second >> coordinate) & 1) == bit
    )


def boundary_profile(
    catalog: tuple[frozenset[tuple[int, int]], ...],
    extendable: frozenset[frozenset[tuple[int, int]]],
) -> tuple[int, int]:
    profiles = set()
    for pattern in catalog:
        signatures = tuple(facet_signature(pattern, facet) for facet in Q4_FACETS)
        profiles.add(
            (
                sum(signature not in extendable for signature in signatures),
                sum(not signature for signature in signatures),
            )
        )
    if len(profiles) != 1:
        raise AssertionError("boundary profile is not orbit-invariant")
    return profiles.pop()


def embed_q4(
    pattern: frozenset[tuple[int, int]], facet: tuple[int, int]
) -> frozenset[tuple[int, int]]:
    coordinate, bit = facet
    free = tuple(index for index in range(5) if index != coordinate)

    def embed_vertex(local_vertex: int) -> int:
        result = bit << coordinate
        for local_coordinate, global_coordinate in enumerate(free):
            result |= ((local_vertex >> local_coordinate) & 1) << global_coordinate
        return result

    return frozenset(
        tuple(sorted((embed_vertex(first), embed_vertex(second))))
        for first, second in pattern
    )


Q5_FACET_EDGES = tuple(
    frozenset(
        edge
        for edge in Q5_EDGES
        if all(((vertex >> coordinate) & 1) == bit for vertex in edge)
    )
    for coordinate, bit in Q5_FACETS
)


REPRESENTATIVES = {
    "eq": 0x000DFFDD,
    "28": 0x00BDFFEC,
    "42": 0x0DFFE55A,
    "48": 0x001F7EFE,
    "71": 0x000D5FFE,
    "99": 0x00000001,
    "124": 0x0DFF753B,
}


ROW_DATA = {
    42: ({"42": 1, "eq": 8, "empty": 1}, "42"),
    84: ({"42": 2, "eq": 8}, "42"),
    132: ({"42": 2, "48": 1, "eq": 6, "empty": 1}, "48"),
    144: ({"48": 3, "eq": 6, "empty": 1}, "48"),
    161: ({"42": 1, "48": 1, "71": 1, "eq": 6, "empty": 1}, "71"),
    166: ({"42": 1, "124": 1, "eq": 7, "empty": 1}, "42"),
    174: ({"42": 3, "48": 1, "eq": 6}, "48"),
    186: ({"42": 1, "48": 3, "eq": 6}, "42"),
    188: ({"28": 5, "48": 1, "eq": 3, "empty": 1}, "48"),
    190: ({"48": 1, "71": 2, "eq": 6, "empty": 1}, "48"),
    195: ({"71": 1, "124": 1, "eq": 7, "empty": 1}, "71"),
    196: ({"28": 7, "eq": 3}, "28"),
    198: ({"99": 2, "eq": 6, "empty": 2}, "99"),
}


def multiset_words(counts: dict[str, int], prefix: tuple[str, ...] = ()):
    if sum(counts.values()) == 0:
        yield prefix
        return
    for label in sorted(counts):
        if counts[label]:
            next_counts = dict(counts)
            next_counts[label] -= 1
            yield from multiset_words(next_counts, prefix + (label,))


def gluing_solutions(
    labels: tuple[str, ...],
    fixed_pattern: frozenset[tuple[int, int]],
    embedded_catalogs: dict[str, tuple[tuple[frozenset[tuple[int, int]], ...], ...]],
) -> int:
    ones = embed_q4(fixed_pattern, Q5_FACETS[0])
    known = Q5_FACET_EDGES[0]

    def visit(
        selected: frozenset[tuple[int, int]],
        assigned: frozenset[tuple[int, int]],
        remaining: tuple[int, ...],
    ) -> int:
        if not remaining:
            return 1
        choices = []
        for facet in remaining:
            overlap = Q5_FACET_EDGES[facet] & assigned
            compatible = tuple(
                candidate
                for candidate in embedded_catalogs[labels[facet - 1]][facet]
                if (candidate & overlap) == (selected & overlap)
            )
            choices.append((len(compatible), facet, compatible))
        count, facet, compatible = min(choices, key=lambda item: item[0])
        if count == 0:
            return 0
        next_remaining = tuple(item for item in remaining if item != facet)
        return sum(
            visit(
                selected | candidate,
                assigned | Q5_FACET_EDGES[facet],
                next_remaining,
            )
            for candidate in compatible
        )

    return visit(ones, known, tuple(range(1, 10)))


def live_capacity_maxima() -> list[int]:
    edge_facets = []
    for first, second in Q5_EDGES:
        direction = (first ^ second).bit_length() - 1
        edge_facets.append(
            frozenset(
                (coordinate, (first >> coordinate) & 1)
                for coordinate in range(5)
                if coordinate != direction
            )
        )
    return [
        max(
            sum(containing <= frozenset(live) for containing in edge_facets)
            for live in combinations(Q5_FACETS, live_count)
        )
        for live_count in range(1, 11)
    ]


def check() -> dict[str, object]:
    if (len(Q4_EDGES), len(Q4_SQUARES), len(Q5_EDGES), len(Q5_SQUARES)) != (32, 24, 80, 80):
        raise AssertionError("incorrect cube incidence structure")
    parity_spectra, first_odd = small_parity_audit()

    catalogs = {name: orbit(mask) for name, mask in REPRESENTATIVES.items()}
    catalogs["empty"] = (frozenset(),)
    expected_sizes = {"eq": 64, "28": 192, "42": 32, "48": 192, "71": 192, "99": 32, "124": 192}
    if {name: len(catalogs[name]) for name in expected_sizes} != expected_sizes:
        raise AssertionError("unexpected residual orbit size")
    expected_statistics = {
        "eq": (17, 15, 3, 0),
        "28": (19, 17, 5, 28),
        "42": (20, 18, 6, 42),
        "48": (18, 16, 6, 48),
        "71": (16, 13, 7, 71),
        "99": (1, 0, 6, 99),
        "124": (21, 19, 11, 124),
    }
    for name in expected_sizes:
        if set(map(q4_statistics, catalogs[name])) != {expected_statistics[name]}:
            raise AssertionError(f"incorrect statistics in {name} orbit")

    extendable = frozenset(
        facet_signature(pattern, facet)
        for pattern in catalogs["eq"]
        for facet in Q4_FACETS
    )
    profiles = {name: boundary_profile(catalogs[name], extendable) for name in expected_sizes}
    expected_profiles = {
        "eq": (0, 1),
        "28": (6, 0),
        "42": (0, 0),
        "48": (3, 0),
        "71": (2, 1),
        "99": (3, 5),
        "124": (1, 0),
    }
    if profiles != expected_profiles:
        raise AssertionError("incorrect boundary profiles")

    embedded_catalogs = {
        name: tuple(
            tuple(embed_q4(pattern, facet) for pattern in catalog)
            for facet in Q5_FACETS
        )
        for name, catalog in catalogs.items()
    }
    residuals = {}
    for total, (counts, fixed_label) in ROW_DATA.items():
        remaining = dict(counts)
        remaining[fixed_label] -= 1
        expected_cases = factorial(9)
        for count in remaining.values():
            expected_cases //= factorial(count)
        cases = 0
        solutions = 0
        fixed_pattern = mask_edges(REPRESENTATIVES[fixed_label])
        for labels in multiset_words(remaining):
            cases += 1
            solutions += gluing_solutions(labels, fixed_pattern, embedded_catalogs)
        if cases != expected_cases or solutions:
            raise AssertionError(f"residual row {total} failed")
        residuals[str(total)] = {"cases": cases, "solutions": solutions}
    if sum(row["cases"] for row in residuals.values()) != 2430:
        raise AssertionError("incorrect total placement count")

    capacities = live_capacity_maxima()
    if capacities != [0, 0, 0, 1, 5, 9, 16, 28, 48, 80]:
        raise AssertionError("incorrect live-facet capacities")
    q5_ratio = Fraction(12 * 56 + 200, 34 * 56)
    global_coefficient = q5_ratio / 12
    new_constant = Fraction(4998, 2747)
    old_constant = Fraction(19992, 11005)
    if (q5_ratio, global_coefficient) != (Fraction(109, 238), Fraction(109, 2856)):
        raise AssertionError("incorrect local-to-global ratio")
    if new_constant - old_constant != Fraction(84966, 30230735):
        raise AssertionError("incorrect improvement")
    integer_bounds = {}
    for dimension in (7, 8):
        value = Fraction(4998 * dimension * 2**dimension, 2747 * dimension + 7249)
        integer_bounds[str(dimension)] = (value.numerator + value.denominator - 1) // value.denominator
    if integer_bounds != {"7": 170, "8": 351}:
        raise AssertionError("incorrect integer consequence")

    return {
        "small_edge_deficit_spectra": parity_spectra,
        "first_odd_deficit_example": first_odd,
        "residual_orbit_sizes": expected_sizes,
        "residual_statistics": expected_statistics,
        "residual_boundary_profiles": profiles,
        "residual_gluing": residuals,
        "total_residual_placements": 2430,
        "live_facet_capacity_maxima": capacities,
        "q5_slack_edge_ratio": str(q5_ratio),
        "global_slack_coefficient": str(global_coefficient),
        "asymptotic_constant": str(new_constant),
        "improvement_over_gap166": str(new_constant - old_constant),
        "integer_bounds": integer_bounds,
        "status": "PASS",
    }


if __name__ == "__main__":
    print(json.dumps(check(), indent=2, sort_keys=True))
