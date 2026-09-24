#!/usr/bin/env python3
"""Independent finite audit for the upper-seven hypercube construction.

This file imports no reviewed source.  It reconstructs the initial graph from
the mathematical definition, stores cube edges by direction, and checks all
faces and all nonexceptional missing edges.  In particular, the 18-dimensional
case is beyond the reviewed constructor's expansion cap.
"""

from __future__ import annotations

import json
from fractions import Fraction


A = frozenset((0, 1, 2))


def syndrome_table(length: int) -> list[int]:
    """Syndrome of every word; coordinate labels are 1,...,length."""
    answer = [0] * (1 << length)
    for word in range(1, 1 << length):
        low = word & -word
        answer[word] = answer[word ^ low] ^ low.bit_length()
    return answer


def quotient_edge(u: int, v: int) -> bool:
    """The graph R, expressed without using the reviewed implementation."""
    if u == v:
        return False
    pair = frozenset((u, v))
    if 0 in pair or pair == frozenset((1, 3)):
        return True
    for hub, outer in ((u, v), (v, u)):
        if hub in (1, 2) and outer not in (0, 1, 2, 3):
            chi = ((outer & 1) ^ ((outer >> 1) & 1))
            return hub == (1 if chi == 0 else 2)
    return False


def audit_quotient(q: int) -> dict[str, int | str]:
    edges = {
        frozenset((u, v))
        for u in range(q)
        for v in range(u + 1, q)
        if quotient_edge(u, v)
    }
    affine_squares = 0
    boundary_missing_edges: set[frozenset[int]] = set()
    for u in range(q):
        for v in range(u + 1, q):
            for w in range(v + 1, q):
                x = u ^ v ^ w
                if x <= w:
                    continue
                affine_squares += 1
                cycle_sets = (
                    ((u, v), (v, w), (w, x), (x, u)),
                    ((u, v), (v, x), (x, w), (w, u)),
                    ((u, w), (w, v), (v, x), (x, u)),
                )
                for cycle in cycle_sets:
                    assert sum(frozenset(e) in edges for e in cycle) < 4
    for u in A:
        for v in range(q):
            if u == v or frozenset((u, v)) in edges:
                continue
            boundary_missing_edges.add(frozenset((u, v)))
            label = u ^ v
            witnessed = False
            for second in range(1, q):
                if second == label:
                    continue
                cycle = ((u, u ^ second), (u ^ second, v ^ second),
                         (v ^ second, v))
                if all(quotient_edge(x, y) for x, y in cycle):
                    witnessed = True
                    break
            assert witnessed
    assert len(edges) == 2 * q - 4
    assert len(boundary_missing_edges) == q - 2
    for dominating in ({0}, {1, 2}):
        assert all(
            v in dominating
            or any(quotient_edge(v, d) for d in dominating)
            for v in range(q)
        )
        assert not any(quotient_edge(u, v) for u in dominating for v in dominating)
    return {
        "affine_square_cycles_checked": 3 * affine_squares,
        "boundary_missing_edges_checked": len(boundary_missing_edges),
        "edges": len(edges),
        "q": q,
        "status": "VERIFIED",
    }


def audit_blocks(a: int, b: int, r: int) -> dict[str, int | list[int] | str]:
    """Check the initial graph, before greedy completion, by full enumeration."""
    assert a + 1 >= 4 and (a + 1) & a == 0
    assert b + 1 >= 4 and (b + 1) & b == 0
    assert r >= 0
    n = a + b + r
    vertices = 1 << n
    mask_a = (1 << a) - 1
    mask_b0 = (1 << b) - 1
    mask_b = mask_b0 << a
    syn_a = syndrome_table(a)
    syn_b = syndrome_table(b)

    def syndromes(vertex: int) -> tuple[int, int]:
        return syn_a[vertex & mask_a], syn_b[(vertex & mask_b) >> a]

    def exceptional(vertex: int) -> bool:
        sx, sy = syndromes(vertex)
        return sx in A and sy in A

    present = [bytearray(vertices) for _ in range(n)]
    initial_edges = 0
    for direction in range(n):
        bit = 1 << direction
        row = present[direction]
        for lower in range(vertices):
            if lower & bit:
                continue
            sx, sy = syndromes(lower)
            chosen = False
            if direction < a:
                chosen = quotient_edge(sx, sx ^ (direction + 1))
            elif direction < a + b:
                chosen = quotient_edge(sy, sy ^ (direction - a + 1))
            if direction >= a and sx in A:
                want = 0 if sx == 0 else 1
                chosen |= ((lower & ~mask_a).bit_count() & 1) == want
            if not a <= direction < a + b and sy in A:
                want = 0 if sy == 0 else 1
                chosen |= ((lower & ~mask_b).bit_count() & 1) == want
            if chosen and not exceptional(lower) and not exceptional(lower ^ bit):
                row[lower] = 1
                initial_edges += 1

    faces_checked = 0
    for i in range(n):
        bi = 1 << i
        for j in range(i + 1, n):
            bj = 1 << j
            for base in range(vertices):
                if base & (bi | bj):
                    continue
                faces_checked += 1
                count = (present[i][base] + present[i][base ^ bj]
                         + present[j][base] + present[j][base ^ bi])
                assert count < 4

    missing_away = 0
    witnessed_away = 0
    incident_exceptional = 0
    for i in range(n):
        bi = 1 << i
        for lower in range(vertices):
            if lower & bi or present[i][lower]:
                continue
            if exceptional(lower) or exceptional(lower ^ bi):
                incident_exceptional += 1
                continue
            missing_away += 1
            found = False
            for j in range(n):
                if j == i:
                    continue
                bj = 1 << j
                base = lower & ~bj
                opposite = base ^ bj
                if lower == base:
                    other_parallel = present[i][opposite]
                else:
                    other_parallel = present[i][base]
                if other_parallel and present[j][base] and present[j][base ^ bi]:
                    found = True
                    break
            assert found, (a, b, r, lower, i)
            witnessed_away += 1

    exceptional_vertices = sum(exceptional(v) for v in range(vertices))
    assert exceptional_vertices == 9 * vertices // ((a + 1) * (b + 1))
    p, q = a + 1, b + 1
    coefficient = (Fraction(5, 2)
                   + Fraction(3 * n - 13, 4) * (Fraction(1, p) + Fraction(1, q))
                   + Fraction(9 * n, p * q))
    assert initial_edges + n * exceptional_vertices <= coefficient * vertices
    return {
        "blocks": [a, b, r],
        "dimension": n,
        "exceptional_incident_missing_edges": incident_exceptional,
        "exceptional_vertices": exceptional_vertices,
        "faces_checked": faces_checked,
        "initial_edges": initial_edges,
        "missing_edges_away_from_exceptional_set": missing_away,
        "proved_edge_bound_coefficient": str(coefficient),
        "status": "VERIFIED",
        "witnessed_missing_edges_away_from_exceptional_set": witnessed_away,
    }


def audit_arithmetic() -> dict[str, int | str]:
    cases = 0
    for n in range(6, 10001):
        q = 1 << (((n + 2) // 2).bit_length() - 1)
        p = q if n + 2 < 3 * q else 2 * q
        assert p + q - 2 <= n
        value = (Fraction(5, 2)
                 + Fraction(3 * n - 13, 4) * (Fraction(1, p) + Fraction(1, q))
                 + Fraction(9 * n, p * q))
        assert value < 7 + Fraction(48, n + 2)
        cases += 1
    for exponent in range(2, 101):
        q = 1 << exponent
        n = 2 * q - 2
        value = (Fraction(5, 2) + Fraction(3 * n - 13, 2 * q)
                 + Fraction(9 * n, q * q))
        assert value == Fraction(11, 2) + Fraction(17, 2 * q) - Fraction(18, q * q)
        cases += 1
    return {"exact_cases": cases, "status": "VERIFIED"}


def main() -> None:
    report = {
        "arithmetic": audit_arithmetic(),
        "block_audits": [
            audit_blocks(3, 3, 4),
            audit_blocks(7, 7, 1),
            audit_blocks(15, 3, 0),
        ],
        "quotient_audits": [audit_quotient(q) for q in (4, 8, 16, 32, 64)],
        "status": "INDEPENDENT_AUDIT_VERIFIED",
    }
    print(json.dumps(report, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
