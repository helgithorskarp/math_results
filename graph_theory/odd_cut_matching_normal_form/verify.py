#!/usr/bin/env python3
"""Definition-level audit for the component-parity normal form.

Python 3.11+, standard library only.  This is finite corroboration of the
written proof, not evidence for the universal quantifier by enumeration.
"""

from __future__ import annotations

from itertools import combinations


Edge = tuple[int, int]


def edge(u: int, v: int) -> Edge:
    assert u != v
    return (u, v) if u < v else (v, u)


def check_cubic(n: int, edges: frozenset[Edge]) -> None:
    degrees = [0] * n
    adjacency = [[] for _ in range(n)]
    for u, v in edges:
        assert 0 <= u < v < n
        degrees[u] += 1
        degrees[v] += 1
        adjacency[u].append(v)
        adjacency[v].append(u)
    assert degrees == [3] * n
    seen = {0}
    stack = [0]
    while stack:
        u = stack.pop()
        for v in adjacency[u]:
            if v not in seen:
                seen.add(v)
                stack.append(v)
    assert len(seen) == n


def perfect_matchings(n: int, edges: frozenset[Edge]) -> list[frozenset[Edge]]:
    incident = [[] for _ in range(n)]
    for e in edges:
        u, v = e
        incident[u].append(e)
        incident[v].append(e)

    answer: list[frozenset[Edge]] = []

    def visit(unmatched: frozenset[int], chosen: tuple[Edge, ...]) -> None:
        if not unmatched:
            answer.append(frozenset(chosen))
            return
        u = min(unmatched)
        for e in sorted(incident[u]):
            v = e[1] if e[0] == u else e[0]
            if v in unmatched:
                visit(unmatched - {u, v}, chosen + (e,))

    visit(frozenset(range(n)), ())
    return sorted(answer, key=lambda matching: sorted(matching))


def components(n: int, edges: frozenset[Edge]) -> tuple[list[int], list[list[int]]]:
    adjacency = [[] for _ in range(n)]
    for u, v in edges:
        adjacency[u].append(v)
        adjacency[v].append(u)
    label = [-1] * n
    blocks: list[list[int]] = []
    for start in range(n):
        if label[start] != -1:
            continue
        index = len(blocks)
        block: list[int] = []
        label[start] = index
        stack = [start]
        while stack:
            u = stack.pop()
            block.append(u)
            for v in adjacency[u]:
                if label[v] == -1:
                    label[v] = index
                    stack.append(v)
        blocks.append(sorted(block))
    return label, blocks


def contains_odd_cut_direct(
    n: int, edges: frozenset[Edge], intersection: frozenset[Edge]
) -> bool:
    # Fix vertex 0 on one side to inspect each unordered cut once.
    for mask in range(0, 1 << (n - 1)):
        side = {0}
        side.update(v for v in range(1, n) if mask & (1 << (v - 1)))
        if len(side) == n:
            continue
        cut = frozenset(e for e in edges if ((e[0] in side) != (e[1] in side)))
        if len(cut) % 2 == 1 and cut <= intersection:
            return True
    return False


def quotient_even_odd_cycle_components(
    n: int, edges: frozenset[Edge], m: frozenset[Edge], other: frozenset[Edge]
) -> bool:
    f_edges = edges - m
    cycle_of, cycles = components(n, f_edges)
    assert all(len(cycle) >= 3 for cycle in cycles)
    assert all(
        sum(1 for e in f_edges if vertex in e) == 2
        for vertex in range(n)
    )

    # Q_M[A], A=M-other.  Quotient loops deliberately do not merge blocks.
    q_edges = m - other
    q_adjacency = [set() for _ in cycles]
    for u, v in q_edges:
        i, j = cycle_of[u], cycle_of[v]
        if i != j:
            q_adjacency[i].add(j)
            q_adjacency[j].add(i)

    seen: set[int] = set()
    for start in range(len(cycles)):
        if start in seen:
            continue
        block: list[int] = []
        seen.add(start)
        stack = [start]
        while stack:
            i = stack.pop()
            block.append(i)
            for j in q_adjacency[i]:
                if j not in seen:
                    seen.add(j)
                    stack.append(j)
        odd_cycles = sum(len(cycles[i]) % 2 for i in block)
        if odd_cycles % 2:
            return False
    return True


def alternating_transversal(
    n: int, edges: frozenset[Edge], m: frozenset[Edge], other: frozenset[Edge]
) -> bool:
    difference = m ^ other
    if not difference:
        return False
    active = {v for e in difference for v in e}
    if any(sum(v in e for e in difference) != 2 for v in active):
        raise AssertionError("symmetric difference is not a cycle packing")
    _, difference_blocks = components(n, difference)
    nontrivial = [set(block) for block in difference_blocks if set(block) <= active]
    # components() also returns isolated vertices; retain only edge-components.
    nontrivial = [
        block for block in nontrivial
        if any(u in block and v in block for u, v in difference)
    ]
    if len(nontrivial) != 1:
        return False

    _, f_cycles = components(n, edges - m)
    return all(set(cycle) & nontrivial[0] for cycle in f_cycles if len(cycle) % 2)


def fixtures() -> list[tuple[str, int, frozenset[Edge]]]:
    k4 = frozenset(edge(u, v) for u, v in combinations(range(4), 2))
    k33 = frozenset(edge(u, v) for u in range(3) for v in range(3, 6))
    prism = frozenset(
        [edge(0, 1), edge(1, 2), edge(2, 0),
         edge(3, 4), edge(4, 5), edge(5, 3)]
        + [edge(i, i + 3) for i in range(3)]
    )
    cube = frozenset(
        edge(u, u ^ (1 << bit))
        for u in range(8)
        for bit in range(3)
        if u < (u ^ (1 << bit))
    )
    petersen = frozenset(
        [edge(i, (i + 1) % 5) for i in range(5)]
        + [edge(5 + i, 5 + ((i + 2) % 5)) for i in range(5)]
        + [edge(i, 5 + i) for i in range(5)]
    )
    return [
        ("K4", 4, k4),
        ("K3,3", 6, k33),
        ("triangular_prism", 6, prism),
        ("cube", 8, cube),
        ("Petersen", 10, petersen),
    ]


def main() -> None:
    total_pairs = 0
    total_valid = 0
    total_transversal = 0
    for name, n, edges in fixtures():
        check_cubic(n, edges)
        matchings = perfect_matchings(n, edges)
        valid = 0
        transversal = 0
        for m in matchings:
            for other in matchings:
                direct = not contains_odd_cut_direct(n, edges, m & other)
                quotient = quotient_even_odd_cycle_components(
                    n, edges, m, other
                )
                assert direct == quotient, (name, sorted(m), sorted(other))
                valid += direct
                if alternating_transversal(n, edges, m, other):
                    assert quotient
                    transversal += 1
        pairs = len(matchings) ** 2
        total_pairs += pairs
        total_valid += valid
        total_transversal += transversal
        print(
            f"{name}: perfect_matchings={len(matchings)} "
            f"ordered_pairs={pairs} valid_pairs={valid} "
            f"single_transversal_pairs={transversal}"
        )
    print(
        f"TOTAL: ordered_pairs={total_pairs} valid_pairs={total_valid} "
        f"single_transversal_pairs={total_transversal}"
    )
    print("all direct cut tests agree with the component-parity criterion")


if __name__ == "__main__":
    main()
