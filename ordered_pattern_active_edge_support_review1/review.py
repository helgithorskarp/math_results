#!/usr/bin/env python3
"""Independent finite audit of the active-edge support theorem.

The primary enumeration starts from rm-subsets of [rm+s], constructs the
ordered clique directly from its selected vertices, and only afterwards
compares the result with the claimed support formula and selected family.
"""

from __future__ import annotations

import hashlib
import itertools
import json
import math
from functools import lru_cache
from pathlib import Path


ROOT = Path(__file__).resolve().parent
EXPECTED = ROOT / "EXPECTED.json"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def choose0(n: int, k: int) -> int:
    return math.comb(n, k) if n >= k >= 0 else 0


def flips(signs: tuple[int, ...]) -> int:
    return sum(x != y for x, y in zip(signs, signs[1:]))


def base_positions(
    signs: tuple[int, ...], m: int, rank: int
) -> tuple[int, ...]:
    """One-based positions of the rank edge in an rm-vertex clique."""
    return tuple(
        block * m + (rank if sign == 1 else m + 1 - rank)
        for block, sign in enumerate(signs)
    )


def clique_from_vertices(
    signs: tuple[int, ...], m: int, vertices: tuple[int, ...]
) -> frozenset[tuple[int, ...]]:
    """Construct a canonical clique directly from its increasing vertices."""
    require(len(vertices) == len(signs) * m, "wrong vertex-set size")
    return frozenset(
        tuple(vertices[p - 1] for p in base_positions(signs, m, rank))
        for rank in range(1, m + 1)
    )


def all_cliques(
    signs: tuple[int, ...], m: int, s: int
) -> list[frozenset[tuple[int, ...]]]:
    n = len(signs) * m + s
    return [
        clique_from_vertices(signs, m, vertices)
        for vertices in itertools.combinations(range(1, n + 1), len(signs) * m)
    ]


def weak_tuples(length: int, maximum: int):
    yield from itertools.combinations_with_replacement(
        range(maximum + 1), length
    )


def selected_cliques(
    signs: tuple[int, ...], m: int, s: int
) -> list[frozenset[tuple[int, ...]]]:
    n = len(signs) * m + s
    answer = []
    for q in weak_tuples(s, len(signs)):
        omitted = {value * m + index for index, value in enumerate(q, 1)}
        require(len(omitted) == s, "selected omissions are not distinct")
        require(min(omitted, default=1) >= 1, "omission below ground set")
        require(max(omitted, default=n) <= n, "omission above ground set")
        vertices = tuple(v for v in range(1, n + 1) if v not in omitted)
        answer.append(clique_from_vertices(signs, m, vertices))
    return answer


def formula(signs: tuple[int, ...], m: int, s: int) -> int:
    r = len(signs)
    return m * math.comb(r + s, r) - (m - 1) * choose0(
        r + s - flips(signs) - 1, r
    )


def insertion_completeness(
    signs: tuple[int, ...], m: int, s: int
) -> int:
    """Check the arbitrary-copy to selected-copy reduction edge by edge."""
    r = len(signs)
    n = r * m + s
    checked = 0
    for vertices in itertools.combinations(range(1, n + 1), r * m):
        for rank in range(1, m + 1):
            base = base_positions(signs, m, rank)
            edge = tuple(vertices[p - 1] for p in base)
            counts = tuple(x - p for x, p in zip(edge, base))
            require(
                0 <= counts[0]
                and counts[-1] <= s
                and all(a <= b for a, b in zip(counts, counts[1:])),
                "insertion counts are not a bounded weakly increasing tuple",
            )
            multiplicities = (
                counts[0],
                *(counts[i + 1] - counts[i] for i in range(r - 1)),
                s - counts[-1],
            )
            q = tuple(
                value
                for value, count in enumerate(multiplicities)
                for _ in range(count)
            )
            omitted = {value * m + index for index, value in enumerate(q, 1)}
            selected_vertices = tuple(
                v for v in range(1, n + 1) if v not in omitted
            )
            reconstructed = tuple(selected_vertices[p - 1] for p in base)
            require(reconstructed == edge, "insertion reduction lost an edge")
            checked += 1
    return checked


def maximum_packing(
    cliques: list[frozenset[tuple[int, ...]]]
) -> tuple[int, int]:
    """Exact maximum set packing via a memoized conflict-graph recurrence."""
    size = len(cliques)
    closed_conflict = []
    for i, left in enumerate(cliques):
        mask = 1 << i
        for j, right in enumerate(cliques):
            if i != j and not left.isdisjoint(right):
                mask |= 1 << j
        closed_conflict.append(mask)

    states = 0

    @lru_cache(maxsize=None)
    def solve(candidates: int) -> int:
        nonlocal states
        states += 1
        if not candidates:
            return 0
        members = [i for i in range(size) if candidates >> i & 1]
        pivot = max(
            members,
            key=lambda i: (candidates & closed_conflict[i]).bit_count(),
        )
        without = solve(candidates & ~(1 << pivot))
        with_pivot = 1 + solve(candidates & ~closed_conflict[pivot])
        return max(without, with_pivot)

    return solve((1 << size) - 1), states


def audit_case(
    signs: tuple[int, ...], m: int, s: int
) -> tuple[list[int | str], int]:
    r = len(signs)
    direct = all_cliques(signs, m, s)
    selected = selected_cliques(signs, m, s)
    require(len(direct) == math.comb(r * m + s, s), "copy count failed")
    require(len(selected) == math.comb(r + s, r), "selected count failed")
    require(
        all(len(copy) == m for copy in direct),
        "a canonical clique has repeated edges",
    )
    support = frozenset().union(*direct)
    selected_support = frozenset().union(*selected)
    require(support == selected_support, "selected family misses active edges")
    require(len(support) == formula(signs, m, s), "support formula failed")

    labels = sum(map(len, selected))
    selected_disjoint = labels == len(selected_support)
    require(
        selected_disjoint == (s <= flips(signs)),
        "selected-family threshold failed",
    )
    target = math.comb(r + s, r)
    upper = len(support) // m
    require(
        upper
        == target
        - math.ceil(
            (m - 1)
            * choose0(r + s - flips(signs) - 1, r)
            / m
        ),
        "packing-bound identity failed",
    )
    if s <= flips(signs):
        require(selected_disjoint and upper == target, "positive direction failed")
    else:
        require(upper < target, "support does not obstruct the target packing")

    insertion_edges = insertion_completeness(signs, m, s)
    word = "".join("+" if x == 1 else "-" for x in signs)
    return [r, m, s, word, len(direct), len(support), target, upper], insertion_edges


def build_report() -> dict[str, object]:
    records: list[list[int | str]] = []
    insertion_edges = 0
    direct_cliques = 0
    for r in range(1, 5):
        for tail in itertools.product((1, -1), repeat=r - 1):
            signs = (1, *tail)
            for m in range(2, 5):
                for s in range(0, 4):
                    record, checked = audit_case(signs, m, s)
                    records.append(record)
                    insertion_edges += checked
                    direct_cliques += record[4]

    # Boundary probes omitted by the rectangular box: long translate chains,
    # several-rank overlaps, and the first failure beyond maximum flip depth.
    for signs, m, s in (
        ((1,), 2, 6),
        ((1, 1), 2, 5),
        ((1, -1, 1), 2, 5),
        ((1, -1, 1, -1), 2, 4),
        ((1, -1, 1, -1), 3, 4),
    ):
        record, checked = audit_case(signs, m, s)
        records.append(record)
        insertion_edges += checked
        direct_cliques += record[4]

    exact_specs = (
        ((1,), 2, 0),
        ((1,), 2, 1),
        ((1,), 2, 2),
        ((1, 1), 2, 1),
        ((1, 1), 2, 2),
        ((1, -1), 2, 1),
        ((1, -1), 2, 2),
        ((1, 1), 3, 1),
        ((1, -1), 3, 2),
        ((1, 1, 1), 2, 1),
        ((1, 1, -1), 2, 2),
    )
    exact_packings = []
    search_states = 0
    for signs, m, s in exact_specs:
        cliques = all_cliques(signs, m, s)
        optimum, states = maximum_packing(cliques)
        support = frozenset().union(*cliques)
        upper = len(support) // m
        target = math.comb(len(signs) + s, len(signs))
        require(optimum <= upper, "exact packing exceeds support bound")
        require((optimum == target) == (s <= flips(signs)), "exact iff failed")
        exact_packings.append(
            [
                "".join("+" if x == 1 else "-" for x in signs),
                m,
                s,
                len(cliques),
                optimum,
                upper,
                target,
            ]
        )
        search_states += states

    encoded = json.dumps(records, separators=(",", ":")).encode("ascii")
    return {
        "case_count": len(records),
        "direct_clique_count": direct_cliques,
        "insertion_edge_count": insertion_edges,
        "exact_packing_cases": exact_packings,
        "packing_search_states": search_states,
        "record_sha256": hashlib.sha256(encoded).hexdigest(),
        "status": "VERIFIED",
    }


def main() -> None:
    report = build_report()
    expected = json.loads(EXPECTED.read_text(encoding="utf-8"))
    require(report == expected, "report differs from EXPECTED.json")
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
