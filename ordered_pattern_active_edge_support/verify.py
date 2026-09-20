#!/usr/bin/env python3
"""Exact finite audit for the ordered-pattern active-edge theorem."""

from __future__ import annotations

import hashlib
import itertools
import json
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parent
EXPECTED_PATH = ROOT / "EXPECTED.json"
OMISSION_CAP = 20_000


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def choose0(n: int, k: int) -> int:
    return math.comb(n, k) if n >= k >= 0 else 0


def flip_count(signs: tuple[int, ...]) -> int:
    return sum(a != b for a, b in zip(signs, signs[1:]))


def delta(signs: tuple[int, ...]) -> tuple[int, ...]:
    return (
        signs[0],
        *(signs[i + 1] - signs[i] for i in range(len(signs) - 1)),
        -signs[-1],
    )


def compositions(total: int, parts: int):
    if parts == 1:
        yield (total,)
        return
    for first in range(total + 1):
        for tail in compositions(total - first, parts - 1):
            yield (first, *tail)


def base_edge(
    signs: tuple[int, ...], m: int, rank: int
) -> tuple[int, ...]:
    return tuple(
        i * m + (rank if sign == 1 else m + 1 - rank)
        for i, sign in enumerate(signs)
    )


def selected_edge(
    signs: tuple[int, ...],
    m: int,
    rank: int,
    mu: tuple[int, ...],
) -> tuple[int, ...]:
    base = base_edge(signs, m, rank)
    prefix = 0
    edge = []
    for i, value in enumerate(base):
        prefix += mu[i]
        edge.append(value + prefix)
    return tuple(edge)


def selected_omissions(mu: tuple[int, ...], m: int) -> tuple[int, ...]:
    weak_tuple = tuple(
        q for q, multiplicity in enumerate(mu) for _ in range(multiplicity)
    )
    return tuple(q * m + t for t, q in enumerate(weak_tuple, start=1))


def canonical_copy(
    signs: tuple[int, ...],
    m: int,
    omissions: tuple[int, ...],
) -> frozenset[tuple[int, ...]]:
    n = len(signs) * m + len(omissions)
    omitted = set(omissions)
    remaining = [v for v in range(1, n + 1) if v not in omitted]
    require(len(remaining) == len(signs) * m, "wrong complement size")
    return frozenset(
        tuple(remaining[position - 1] for position in base_edge(signs, m, rank))
        for rank in range(1, m + 1)
    )


def all_active_edges(
    signs: tuple[int, ...], m: int, s: int
) -> frozenset[tuple[int, ...]]:
    n = len(signs) * m + s
    active: set[tuple[int, ...]] = set()
    for omissions in itertools.combinations(range(1, n + 1), s):
        active.update(canonical_copy(signs, m, omissions))
    return frozenset(active)


def selected_data(signs: tuple[int, ...], m: int, s: int):
    d = delta(signs)
    copies: list[frozenset[tuple[int, ...]]] = []
    edge_to_lambda: dict[tuple[int, ...], tuple[int, ...]] = {}
    lambda_to_edge: dict[tuple[int, ...], tuple[int, ...]] = {}
    labels = 0

    for mu in compositions(s, len(signs) + 1):
        omissions = selected_omissions(mu, m)
        direct = canonical_copy(signs, m, omissions)
        encoded = frozenset(
            selected_edge(signs, m, rank, mu) for rank in range(1, m + 1)
        )
        require(direct == encoded, "selected omission encoding failed")
        copies.append(encoded)
        for rank, edge in (
            (rank, selected_edge(signs, m, rank, mu))
            for rank in range(1, m + 1)
        ):
            invariant = tuple(x + rank * y for x, y in zip(mu, d))
            if edge in edge_to_lambda:
                require(
                    edge_to_lambda[edge] == invariant,
                    "equal edges have different invariants",
                )
            if invariant in lambda_to_edge:
                require(
                    lambda_to_edge[invariant] == edge,
                    "equal invariants have different edges",
                )
            edge_to_lambda[edge] = invariant
            lambda_to_edge[invariant] = edge
            labels += 1

    require(
        len(edge_to_lambda) == len(lambda_to_edge),
        "invariant is not a bijection on selected edges",
    )
    return copies, frozenset(edge_to_lambda), frozenset(lambda_to_edge), labels


def translated_simplex_checks(
    signs: tuple[int, ...], m: int, s: int
) -> None:
    d = delta(signs)
    simplices = [
        {
            tuple(x + rank * y for x, y in zip(mu, d))
            for mu in compositions(s, len(signs) + 1)
        }
        for rank in range(1, m + 1)
    ]
    h = flip_count(signs) + 1
    expected_adjacent = choose0(len(signs) + s - h, len(signs))
    for rank in range(1, m):
        require(
            len(simplices[rank] & simplices[rank - 1])
            == expected_adjacent,
            "adjacent translate intersection has wrong size",
        )
        earlier = set().union(*simplices[:rank])
        require(
            simplices[rank] & earlier
            == simplices[rank] & simplices[rank - 1],
            "nonadjacent overlap is not absorbed by adjacent overlap",
        )


def formula(signs: tuple[int, ...], m: int, s: int) -> int:
    r = len(signs)
    f = flip_count(signs)
    return m * math.comb(r + s, r) - (m - 1) * choose0(
        r + s - f - 1, r
    )


def audit_case(
    signs: tuple[int, ...], m: int, s: int
) -> list[int | str]:
    r = len(signs)
    f = flip_count(signs)
    selected_copies, selected_edges, invariants, labels = selected_data(
        signs, m, s
    )
    translated_simplex_checks(signs, m, s)

    active = all_active_edges(signs, m, s)
    expected = formula(signs, m, s)
    require(active == selected_edges, "selected family misses an active edge")
    require(len(active) == expected, "active-support formula failed")
    require(len(invariants) == expected, "orbit-union formula failed")
    require(
        labels == m * math.comb(r + s, r),
        "selected label count failed",
    )

    desired = math.comb(r + s, r)
    overlap_deficit = (m - 1) * choose0(r + s - f - 1, r)
    packing_bound = expected // m
    require(
        packing_bound
        == desired - math.ceil(overlap_deficit / m),
        "packing-bound simplification failed",
    )
    selected_disjoint = sum(map(len, selected_copies)) == len(selected_edges)
    require(
        selected_disjoint == (s <= f),
        "selected packing has wrong flip threshold",
    )
    if s <= f:
        require(packing_bound == desired, "packing should attain target")
    else:
        require(packing_bound < desired, "packing obstruction should be strict")

    sign_word = "".join("+" if x == 1 else "-" for x in signs)
    return [
        r,
        m,
        s,
        sign_word,
        f,
        len(active),
        desired,
        packing_bound,
    ]


def audit_sharp_collisions() -> int:
    checked = 0
    for r in range(1, 8):
        for tail in itertools.product((1, -1), repeat=r - 1):
            signs = (1, *tail)
            d = delta(signs)
            h = flip_count(signs) + 1
            positive = tuple(max(x, 0) for x in d)
            negative = tuple(max(-x, 0) for x in d)
            require(sum(positive) == sum(negative) == h, "delta mass failed")
            for m in range(2, 7):
                for rank in range(1, m):
                    require(
                        selected_edge(signs, m, rank + 1, negative)
                        == selected_edge(signs, m, rank, positive),
                        "sharp collision witness failed",
                    )
                    checked += 1
    return checked


def build_report() -> dict[str, object]:
    records: list[list[int | str]] = []
    skipped = 0
    canonical_copies = 0
    selected_labels = 0

    for r in range(1, 6):
        for tail in itertools.product((1, -1), repeat=r - 1):
            signs = (1, *tail)
            for m in range(2, 6):
                for s in range(0, 5):
                    n = r * m + s
                    copy_count = math.comb(n, s)
                    if copy_count > OMISSION_CAP:
                        skipped += 1
                        continue
                    records.append(audit_case(signs, m, s))
                    canonical_copies += copy_count
                    selected_labels += m * math.comb(r + s, r)

    record_bytes = json.dumps(
        records, sort_keys=True, separators=(",", ":")
    ).encode()
    return {
        "case_count": len(records),
        "canonical_copy_count": canonical_copies,
        "selected_label_count": selected_labels,
        "sharp_collision_count": audit_sharp_collisions(),
        "skipped_by_omission_cap": skipped,
        "omission_cap": OMISSION_CAP,
        "record_sha256": hashlib.sha256(record_bytes).hexdigest(),
        "status": "VERIFIED",
    }


def main() -> None:
    report = build_report()
    expected = json.loads(EXPECTED_PATH.read_text(encoding="utf-8"))
    require(report == expected, "report differs from EXPECTED.json")
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
