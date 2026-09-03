#!/usr/bin/env python3
"""Exact finite checks for the n=rm+1 ordered pattern-clique theorem.

The implementation deliberately reconstructs every object from the defining
ordered vertex set.  It uses no solver, randomness, floating point, or third-
party package.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from collections import defaultdict
from collections.abc import Iterable, Sequence


Edge = tuple[int, ...]
SignVector = tuple[int, ...]


def normalized_signs(r: int) -> Iterable[SignVector]:
    """All block orientations, normalized to have first sign +1."""
    if r == 0:
        return
    for tail in itertools.product((1, -1), repeat=r - 1):
        yield (1, *tail)


def base_position(i: int, j: int, m: int, signs: SignVector) -> int:
    """One-based position of edge j in one-based block i."""
    local = j if signs[i - 1] == 1 else m + 1 - j
    return (i - 1) * m + local


def canonical_copy(r: int, m: int, signs: SignVector, omitted: int) -> tuple[Edge, ...]:
    """The P-clique on [rm+1] with one vertex omitted."""
    n = r * m + 1
    assert 1 <= omitted <= n

    # This increasing list implements the order-preserving embedding from
    # [rm] to [rm+1] minus {omitted}, without using the proof's shift formula.
    remaining = [v for v in range(1, n + 1) if v != omitted]
    edges: list[Edge] = []
    for j in range(1, m + 1):
        edge = tuple(
            remaining[base_position(i, j, m, signs) - 1]
            for i in range(1, r + 1)
        )
        edges.append(edge)
    return tuple(edges)


def two_edge_pattern(r: int, signs: SignVector) -> tuple[Edge, Edge]:
    """Construct the normalized r-partite pattern P on [2r]."""
    first = tuple(base_position(i, 1, 2, signs) for i in range(1, r + 1))
    second = tuple(base_position(i, 2, 2, signs) for i in range(1, r + 1))
    return first, second


def lower_bound_parameters(r: int, signs: SignVector) -> tuple[int, ...]:
    """Derive the gap parameters s_i directly from P's two edges."""
    first, second = two_edge_pattern(r, signs)
    assert first[0] < second[0]
    parameters: list[int] = []
    for i in range(r - 1):
        parameters.append(sum(first[i] < v < first[i + 1] for v in second))
    parameters.append(sum(v > first[-1] for v in second))
    assert sum(parameters) == r
    return tuple(parameters)


def is_lower_construction_edge(edge: Edge, m: int, parameters: Sequence[int]) -> bool:
    """Membership in the Anastos--Jin--Kwan--Sudakov lower construction."""
    r = len(edge)
    n = r * m + 1
    close_gap = any(
        edge[i + 1] - edge[i] <= parameters[i] * (m - 1)
        for i in range(r - 1)
    )
    terminal = edge[-1] >= n - parameters[-1] * (m - 1) + 1
    return close_gap or terminal


def check_pattern(r: int, m: int, signs: SignVector) -> dict[str, object]:
    n = r * m + 1
    copies = {
        x: set(canonical_copy(r, m, signs, x))
        for x in range(1, n + 1)
    }

    # Definition-level checks for every canonical matching.
    expected_vertices = set(range(1, n + 1))
    for x, edges in copies.items():
        assert len(edges) == m
        assert all(len(edge) == r and tuple(sorted(edge)) == edge for edge in edges)
        flattened = [v for edge in edges for v in edge]
        assert len(flattened) == len(set(flattened)) == r * m
        assert set(flattened) == expected_vertices - {x}

    # Enumerate the published lower construction from its gap definition.
    parameters = lower_bound_parameters(r, signs)
    missing = {
        edge
        for edge in itertools.combinations(range(1, n + 1), r)
        if not is_lower_construction_edge(edge, m, parameters)
    }
    assert len(missing) == r + 1
    assert all(copies[x] & missing for x in copies)

    occurrences: defaultdict[Edge, set[int]] = defaultdict(set)
    for x, edges in copies.items():
        for edge in edges:
            occurrences[edge].add(x)

    if all(sign == 1 for sign in signs):
        maximum_occurrence = max(map(len, occurrences.values()))
        assert maximum_occurrence <= m
        mechanism = "all_forward_occurrence_bound"
    else:
        boundary = [q * m + 1 for q in range(r + 1)]
        for x, y in itertools.combinations(boundary, 2):
            assert copies[x].isdisjoint(copies[y])
        maximum_occurrence = max(map(len, occurrences.values()))
        mechanism = "boundary_edge_set_disjointness"

    return {
        "r": r,
        "m": m,
        "signs": "".join("+" if sign == 1 else "-" for sign in signs),
        "n": n,
        "gap_parameters": parameters,
        "canonical_edge_union_size": len(occurrences),
        "maximum_copy_occurrence": maximum_occurrence,
        "missing_edges": sorted(missing),
        "mechanism": mechanism,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-r", type=int, default=5)
    parser.add_argument("--max-m", type=int, default=5)
    args = parser.parse_args()
    if args.max_r < 1 or args.max_m < 1:
        parser.error("--max-r and --max-m must be positive")

    records: list[dict[str, object]] = []
    for r in range(1, args.max_r + 1):
        for m in range(1, args.max_m + 1):
            for signs in normalized_signs(r):
                records.append(check_pattern(r, m, signs))

    encoded = json.dumps(records, sort_keys=True, separators=(",", ":")).encode()
    digest = hashlib.sha256(encoded).hexdigest()
    expected_patterns = args.max_m * (2**args.max_r - 1)
    assert len(records) == expected_patterns

    print(f"checked_parameter_pairs={args.max_r * args.max_m}")
    print(f"checked_normalized_patterns={len(records)}")
    print(f"max_r={args.max_r} max_m={args.max_m}")
    print(f"record_sha256={digest}")
    print("status=VERIFIED")


if __name__ == "__main__":
    main()
