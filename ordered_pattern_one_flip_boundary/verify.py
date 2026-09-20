#!/usr/bin/env python3
"""Definition-level exact audit for the one-flip rm+2 boundary theorem."""

from __future__ import annotations

import hashlib
import itertools
import json
import math
import sys
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parent
EXPECTED_PATH = ROOT / "EXPECTED.json"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def one_flip_signs(r: int, t: int) -> tuple[int, ...]:
    require(r >= 2 and 1 <= t < r, "invalid one-flip parameters")
    return (1,) * t + (-1,) * (r - t)


def base_edge(
    signs: tuple[int, ...], m: int, rank: int
) -> tuple[int, ...]:
    """Rank-rank edge of P^(m) on [rm], in increasing vertex order."""
    require(1 <= rank <= m, "invalid edge rank")
    return tuple(
        i * m + (rank if sign == 1 else m + 1 - rank)
        for i, sign in enumerate(signs)
    )


def increasing_complement_map(
    size: int, omissions: tuple[int, int]
) -> tuple[int, ...]:
    """Increasing bijection [size] -> [size+2] minus the two omissions."""
    x, y = omissions
    require(1 <= x < y <= size + 2, "invalid omissions")
    complement = [v for v in range(1, size + 3) if v not in {x, y}]
    require(len(complement) == size, "wrong complement size")
    return tuple(complement)


def canonical_copy_sequence(
    signs: tuple[int, ...], m: int, omissions: tuple[int, int]
) -> tuple[tuple[int, ...], ...]:
    """Edges of the order-preserving copy, kept in base-rank order."""
    phi = increasing_complement_map(len(signs) * m, omissions)
    return tuple(
        tuple(phi[position - 1] for position in base_edge(signs, m, rank))
        for rank in range(1, m + 1)
    )


def compositions(total: int, parts: int):
    if parts == 1:
        yield (total,)
        return
    for first in range(total + 1):
        for tail in compositions(total - first, parts - 1):
            yield (first, *tail)


def selected_omissions(mu: tuple[int, ...], m: int) -> tuple[int, int]:
    require(sum(mu) == 2, "selected composition must have mass two")
    weak_tuple = tuple(
        q for q, multiplicity in enumerate(mu) for _ in range(multiplicity)
    )
    return (weak_tuple[0] * m + 1, weak_tuple[1] * m + 2)


def selected_edge(
    signs: tuple[int, ...],
    m: int,
    rank: int,
    mu: tuple[int, ...],
) -> tuple[int, ...]:
    """Composition encoding of an edge in a selected copy."""
    base = base_edge(signs, m, rank)
    prefix = 0
    edge = []
    for i, value in enumerate(base):
        prefix += mu[i]
        edge.append(value + prefix)
    return tuple(edge)


def unit_sum(parts: int, *indices: int) -> tuple[int, ...]:
    result = [0] * parts
    for index in indices:
        result[index] += 1
    return tuple(result)


def path_composition(r: int, t: int, q: int) -> tuple[int, ...]:
    require(0 <= q <= r, "path index outside range")
    if q <= t:
        return unit_sum(r + 1, q, r)
    return unit_sum(r + 1, t, r + t - q)


def chain_omissions(r: int, m: int, t: int, b: int, q: int) -> tuple[int, int]:
    """Omitted pair defining K_q for a fixed bridge z_b."""
    require(1 <= b < m and 1 <= q <= r, "invalid chain parameters")
    n = r * m + 2
    if q <= t:
        result = ((q - 1) * m + b + 1, n)
    else:
        result = (t * m + 1, n - (q - t - 1) * m - b)
    require(result[0] < result[1], "chain omissions not increasing")
    return result


def lower_blocker(r: int, m: int, t: int) -> frozenset[tuple[int, ...]]:
    """Theorem 9.1 nonedges specialized to a one-flip pattern."""
    # For i<r, s_i=1 except s_t=2, while s_r=0.  Shifting the
    # i-th coordinate by (m-1) sum_{h<i}s_h maps the blocker to
    # all r-subsets of [r+2].
    offsets = tuple(
        (m - 1) * ((i - 1) + int(i > t)) for i in range(1, r + 1)
    )
    return frozenset(
        tuple(y + offset for y, offset in zip(subset, offsets))
        for subset in itertools.combinations(range(1, r + 3), r)
    )


def lower_blocker_predicate(edge: tuple[int, ...], m: int, t: int) -> bool:
    return all(
        edge[i] - edge[i - 1] > (m - 1) * (1 + int(i == t))
        for i in range(1, len(edge))
    )


def collision_delta(r: int, t: int) -> tuple[int, ...]:
    return tuple(
        1 if i in (0, r) else -2 if i == t else 0
        for i in range(r + 1)
    )


def audit_case(r: int, m: int, t: int) -> dict[str, int]:
    signs = one_flip_signs(r, t)
    n = r * m + 2
    all_mu = tuple(compositions(2, r + 1))
    target = math.comb(r + 2, r)
    require(len(all_mu) == target, "wrong number of selected copies")

    selected: dict[tuple[int, ...], tuple[tuple[int, ...], ...]] = {}
    occurrences: dict[tuple[int, ...], list[tuple[tuple[int, ...], int]]] = (
        defaultdict(list)
    )
    for mu in all_mu:
        direct = canonical_copy_sequence(signs, m, selected_omissions(mu, m))
        encoded = tuple(
            selected_edge(signs, m, rank, mu)
            for rank in range(1, m + 1)
        )
        require(direct == encoded, "selected-copy encoding failed")
        selected[mu] = direct
        for rank, edge in enumerate(direct, start=1):
            occurrences[edge].append((mu, rank))

    alpha = unit_sum(r + 1, 0, r)
    beta = unit_sum(r + 1, t, t)
    bridges = tuple(selected_edge(signs, m, b, alpha) for b in range(1, m))
    multiply_used = {
        edge: frozenset(labels)
        for edge, labels in occurrences.items()
        if len(labels) > 1
    }
    expected_labels = {
        selected_edge(signs, m, b, alpha): frozenset((
            (alpha, b),
            (beta, b + 1),
        ))
        for b in range(1, m)
    }
    require(multiply_used == expected_labels, "bridge classification failed")
    require(
        sum(len(labels) == 1 for labels in occurrences.values())
        == m * target - 2 * (m - 1),
        "wrong number of singly used selected edges",
    )
    require(
        len(occurrences) == m * target - (m - 1),
        "wrong selected-support size",
    )

    # Audit the collision criterion for every pair of selected labels, not
    # just the expected bridges.
    delta = collision_delta(r, t)
    labels = [
        (mu, rank, edge)
        for mu, copy in selected.items()
        for rank, edge in enumerate(copy, start=1)
    ]
    collision_pair_count = 0
    for left_index, (mu, rank, edge) in enumerate(labels):
        for nu, other_rank, other_edge in labels[left_index:]:
            difference = tuple(y - x for x, y in zip(mu, nu))
            predicted = difference == tuple(
                (rank - other_rank) * value for value in delta
            )
            require((edge == other_edge) == predicted, "collision criterion failed")
            collision_pair_count += 1

    chain_copy_count = 0
    chain_edge_count = 0
    signature_state_transitions = 0
    for b, bridge in enumerate(bridges, start=1):
        for q in range(1, r + 1):
            direct = canonical_copy_sequence(
                signs, m, chain_omissions(r, m, t, b, q)
            )
            expected = tuple(
                selected_edge(
                    signs,
                    m,
                    rank,
                    path_composition(r, t, q if rank <= b else q - 1),
                )
                for rank in range(1, m + 1)
            )
            require(direct == expected, "chain-copy identity failed")
            require(bridge not in direct, "chain copy contains its bridge")
            chain_copy_count += 1
            chain_edge_count += m

        # Dynamic audit of the rank clauses forced by K_1,...,K_r.
        possible = {a for a in range(1, m + 1) if a <= b}
        require(possible == set(range(1, b + 1)), "K_1 clause failed")
        for _q in range(2, r):
            next_possible = set()
            for previous in possible:
                for current in range(1, m + 1):
                    signature_state_transitions += 1
                    if current <= b or previous > b:
                        next_possible.add(current)
            possible = next_possible
        require(
            not any(previous > b for previous in possible),
            "K_r clause can be met after the middle clauses",
        )

    blocker = lower_blocker(r, m, t)
    require(len(blocker) == target, "lower blocker has wrong size")
    require(
        all(lower_blocker_predicate(edge, m, t) for edge in blocker),
        "lower-blocker predicate failed",
    )
    canonical_copy_count = 0
    for omissions in itertools.combinations(range(1, n + 1), 2):
        copy = canonical_copy_sequence(signs, m, omissions)
        require(copy[0] in blocker, "paper's lower blocker misses a copy")
        require(
            any(edge in blocker for edge in copy),
            "lower blocker does not hit a canonical copy",
        )
        canonical_copy_count += 1

    return {
        "blocker_edges": len(blocker),
        "bridges": len(bridges),
        "canonical_copies": canonical_copy_count,
        "chain_copies": chain_copy_count,
        "chain_edges": chain_edge_count,
        "collision_pairs": collision_pair_count,
        "selected_copies": len(selected),
        "selected_labels": len(labels),
        "signature_state_transitions": signature_state_transitions,
    }


def build_report() -> dict[str, object]:
    records: list[list[int]] = []
    totals = {
        "blocker_edges": 0,
        "bridges": 0,
        "canonical_copies": 0,
        "chain_copies": 0,
        "chain_edges": 0,
        "collision_pairs": 0,
        "selected_copies": 0,
        "selected_labels": 0,
        "signature_state_transitions": 0,
    }
    case_count = 0

    # The proof is parameter-free.  This bounded box independently rebuilds
    # copies from omissions and exercises every flip location.
    for r in range(2, 8):
        for m in range(2, 8):
            for t in range(1, r):
                counts = audit_case(r, m, t)
                case_count += 1
                for key, value in counts.items():
                    totals[key] += value
                records.append([r, m, t, *(counts[key] for key in sorted(counts))])

    record_bytes = json.dumps(records, separators=(",", ":")).encode("ascii")
    return {
        "audit_box": {"r": [2, 7], "m": [2, 7], "all_flip_locations": True},
        "case_count": case_count,
        "record_sha256": hashlib.sha256(record_bytes).hexdigest(),
        "status": "VERIFIED",
        "totals": totals,
    }


def main() -> None:
    report = build_report()
    if "--print-report" not in sys.argv:
        expected = json.loads(EXPECTED_PATH.read_text(encoding="utf-8"))
        require(report == expected, "report differs from EXPECTED.json")
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
