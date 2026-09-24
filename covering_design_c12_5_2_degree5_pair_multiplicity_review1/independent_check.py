#!/usr/bin/env python3
"""Independent audit of the degree-five (12,5,2) link obstruction.

The local census is rebuilt without importing target code.  Nine multigraph
edges are chosen as a multiset from K_5, rather than by either target
recursion.  A generic exact set-cover search then proves directly, for each
isomorphism type, that four 5-subsets cannot cover its missed-pair graph.
The published sharpness and residual witnesses are checked from definitions.

Run from this directory with CPython 3.11+ and only the standard library.
"""

from __future__ import annotations

from copy import deepcopy
from functools import cache
from hashlib import sha256
from itertools import combinations, combinations_with_replacement, permutations
import json
from pathlib import Path
import sys


HERE = Path(__file__).resolve().parent
TARGET = HERE.parent / "covering_design_c12_5_2_degree5_pair_multiplicity"
PREDECESSOR = HERE.parent / "covering_design_c13_6_3_two_intersection_links"
EDGES5 = tuple(combinations(range(5), 2))
BLOCKS11 = tuple(combinations(range(11), 5))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def mask(points) -> int:
    return sum(1 << point for point in points)


def labelled_vectors() -> tuple[tuple[int, ...], ...]:
    """Enumerate edge multisets directly from C(10+9-1,9) choices."""
    vectors = []
    for chosen in combinations_with_replacement(range(len(EDGES5)), 9):
        counts = tuple(chosen.count(edge) for edge in range(len(EDGES5)))
        degrees = [
            sum(counts[index] for index, edge in enumerate(EDGES5) if vertex in edge)
            for vertex in range(5)
        ]
        if max(degrees) <= 4:
            vectors.append(counts)
    return tuple(sorted(vectors))


def permute_vector(vector: tuple[int, ...], permutation: tuple[int, ...]) -> tuple[int, ...]:
    image = {}
    for count, (u, v) in zip(vector, EDGES5):
        image[tuple(sorted((permutation[u], permutation[v])))] = count
    return tuple(image[edge] for edge in EDGES5)


PERMUTATIONS5 = tuple(permutations(range(5)))


def canonical(vector: tuple[int, ...]) -> tuple[int, ...]:
    return min(permute_vector(vector, permutation) for permutation in PERMUTATIONS5)


def columns(vector: tuple[int, ...]) -> tuple[frozenset[int], ...]:
    degrees = [
        sum(vector[index] for index, edge in enumerate(EDGES5) if vertex in edge)
        for vertex in range(5)
    ]
    result = [
        frozenset((vertex,))
        for vertex in range(5)
        for _ in range(4 - degrees[vertex])
    ]
    result.extend(
        frozenset(edge)
        for index, edge in enumerate(EDGES5)
        for _ in range(vector[index])
    )
    require(len(result) == 11, "incidence vector did not produce eleven columns")
    require(
        all(sum(vertex in support for support in result) == 4 for vertex in range(5)),
        "incidence row does not have size four",
    )
    return tuple(result)


def missed_edges(supports: tuple[frozenset[int], ...]) -> tuple[tuple[int, int], ...]:
    return tuple(
        (u, v)
        for u, v in combinations(range(11), 2)
        if supports[u].isdisjoint(supports[v])
    )


def exact_four_block_search(
    universe_edges: tuple[tuple[int, int], ...],
) -> tuple[bool, int, int]:
    """Decide whether at most four 5-subsets cover all universe edges.

    Candidate blocks are represented only by the universe edges they cover.
    Duplicate and dominated masks are discarded.  Branching on an uncovered
    edge is exhaustive. Reusing a candidate is allowed, so rejection also
    covers multisets of blocks.
    """
    edge_index = {edge: index for index, edge in enumerate(universe_edges)}
    universe = (1 << len(universe_edges)) - 1
    raw_masks = []
    for block in BLOCKS11:
        block_set = frozenset(block)
        covered = sum(
            1 << index
            for edge, index in edge_index.items()
            if edge[0] in block_set and edge[1] in block_set
        )
        if covered:
            raw_masks.append(covered)

    ordered = sorted(set(raw_masks), key=lambda value: (-value.bit_count(), value))
    candidates = []
    for value in ordered:
        if not any(value | kept == kept for kept in candidates):
            candidates.append(value)

    incident = [[] for _ in universe_edges]
    for candidate_index, value in enumerate(candidates):
        for edge_index_value in range(len(universe_edges)):
            if value >> edge_index_value & 1:
                incident[edge_index_value].append(candidate_index)

    @cache
    def search(uncovered: int, remaining: int) -> bool:
        if uncovered == 0:
            return True
        if remaining == 0:
            return False
        possible = [value & uncovered for value in candidates]
        if uncovered.bit_count() > remaining * max(value.bit_count() for value in possible):
            return False
        active_edges = [
            index for index in range(len(universe_edges)) if uncovered >> index & 1
        ]
        pivot = min(
            active_edges,
            key=lambda index: len(incident[index]),
        )
        for choice in incident[pivot]:
            if search(uncovered & ~candidates[choice], remaining - 1):
                return True
        return False

    result = search(universe, 4)
    return result, len(candidates), search.cache_info().misses


def pair_covered(blocks: list[frozenset[int]], pair: tuple[int, int]) -> bool:
    return any(pair[0] in block and pair[1] in block for block in blocks)


def validate_sharp(record: dict) -> list[int]:
    blocks = [frozenset(block) for block in record["blocks"]]
    h = record["distinguished_point"]
    require(len(blocks) == len(set(blocks)) == 9, "sharp witness block count")
    require(all(len(block) == 5 and block <= set(range(12)) for block in blocks),
            "sharp witness block domain")
    require(all(pair_covered(blocks, pair) for pair in combinations(range(12), 2)),
            "sharp witness misses a pair")
    require(sum(h in block for block in blocks) == 5, "sharp witness degree")
    codegrees = sorted(
        sum(h in block and point in block for block in blocks)
        for point in range(12)
        if point != h
    )
    require(codegrees == [1] * 3 + [2] * 7 + [3], "sharp witness codegrees")
    return codegrees


def sets_from_masks(rows: list[int], size: int) -> list[frozenset[int]]:
    require(all(type(row) is int and 0 <= row < 1 << 12 for row in rows),
            "row mask domain")
    result = [frozenset(point for point in range(12) if row >> point & 1) for row in rows]
    require(all(len(block) == size for block in result), "row block size")
    return result


def validate_link(record: dict) -> dict:
    a = sets_from_masks(record["rows"], 5)
    require(len(a) == len(set(a)) == 12, "through-family block count")
    require(all(sum(point in block for block in a) == 5 for point in range(12)),
            "through-family point degree")
    multiplicities = [
        sum(pair[0] in block and pair[1] in block for block in a)
        for pair in combinations(range(12), 2)
    ]
    require(set(multiplicities) <= {1, 2}, "through-family pair multiplicity")
    require(max(len(left & right) for left, right in combinations(a, 2)) <= 2,
            "through-family row intersection")

    all_triples = tuple(map(frozenset, combinations(range(12), 3)))
    missed = [triple for triple in all_triples if not any(triple <= block for block in a)]
    require(len(missed) == 100, "unexpected residual triple count")
    b = sets_from_masks(record["completion"], 6)
    require(len(b) == len(set(b)) and len(b) in (10, 11), "completion block count")
    require(all(any(triple <= block for block in b) for triple in missed),
            "completion misses a residual triple")
    degrees = [sum(point in block for block in b) for point in range(12)]
    require(min(degrees) >= 5, "completion violates residual degree bound")
    if len(b) == 10:
        require(set(degrees) == {5}, "ten-block completion is not five-regular")

    high = 12
    extended = [block | {high} for block in a] + b
    require(
        all(
            any(triple <= block for block in extended)
            for triple in map(frozenset, combinations(range(13), 3))
        ),
        "extended covering misses a triple",
    )
    return {
        "label": record["label"],
        "missing_triples": len(missed),
        "completion_blocks": len(b),
        "completion_degree_sequence": sorted(degrees),
        "extended_cover_blocks": len(extended),
    }


def expect_rejection(function, record: dict, label: str) -> None:
    try:
        function(record)
    except (KeyError, RuntimeError, TypeError, ValueError):
        return
    raise RuntimeError(f"negative control accepted: {label}")


def main() -> None:
    require(len(sys.argv) == 1, "usage: python3 independent_check.py")
    require(sys.version_info >= (3, 11), "CPython 3.11+ required")
    control_feasible, _, _ = exact_four_block_search(((0, 1),))
    require(control_feasible, "generic set-cover positive control failed")

    labelled = labelled_vectors()
    require(len(labelled) == len(set(labelled)) == 1430, "labelled census mismatch")
    orbit_counts = {}
    for vector in labelled:
        representative = canonical(vector)
        orbit_counts[representative] = orbit_counts.get(representative, 0) + 1
    require(len(orbit_counts) == 24 and sum(orbit_counts.values()) == 1430,
            "isomorphism census mismatch")

    search_records = []
    total_candidates = total_states = 0
    for index, (representative, orbit_size) in enumerate(sorted(orbit_counts.items())):
        universe = missed_edges(columns(representative))
        feasible, candidate_count, states = exact_four_block_search(universe)
        require(not feasible, f"four-block completion survives in type {index}")
        total_candidates += candidate_count
        total_states += states
        search_records.append(
            (index, orbit_size, len(universe), candidate_count, states, int(feasible))
        )

    sharp_record = json.loads((TARGET / "sharp_link.json").read_text())
    codegrees = validate_sharp(sharp_record)
    sharp_bad = deepcopy(sharp_record)
    sharp_bad["blocks"][0] = sharp_bad["blocks"][1]
    expect_rejection(validate_sharp, sharp_bad, "duplicate sharp block")

    links_record = json.loads((TARGET / "six_links.json").read_text())
    predecessor_bytes = (PREDECESSOR / "certificate.json").read_bytes()
    require(
        sha256(predecessor_bytes).hexdigest() == links_record["source_certificate_sha256"],
        "predecessor certificate hash mismatch",
    )
    predecessor = json.loads(predecessor_bytes)["cases"]
    require(len(predecessor) == len(links_record["classes"]) == 6,
            "copied representative count")
    for current, previous in zip(links_record["classes"], predecessor):
        require(current["rows"] == previous["rows"], "copied representative mismatch")
        require(current["label"].replace("+", "_") == previous["case"],
                "copied representative label mismatch")
    completion_records = [validate_link(record) for record in links_record["classes"]]
    links_bad = deepcopy(links_record["classes"][0])
    links_bad["completion"][0] = links_bad["completion"][1]
    expect_rejection(validate_link, links_bad, "duplicate completion block")

    encoded_vectors = json.dumps(labelled, separators=(",", ":")).encode()
    encoded_search = "\n".join(" ".join(map(str, row)) for row in search_records).encode()
    result = {
        "status": "INDEPENDENT_REVIEW_CHECK_PASSED",
        "labelled_incidence_types": len(labelled),
        "isomorphism_types": len(orbit_counts),
        "labelled_census_sha256": sha256(encoded_vectors).hexdigest(),
        "four_block_survivors": 0,
        "generic_search_candidates": total_candidates,
        "generic_search_states": total_states,
        "generic_search_record_sha256": sha256(encoded_search).hexdigest(),
        "sharp_link_codegrees": codegrees,
        "residual_completions": completion_records,
        "predecessor_certificate_sha256": sha256(predecessor_bytes).hexdigest(),
        "positive_controls_passed": 1,
        "negative_controls_rejected": 2,
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
