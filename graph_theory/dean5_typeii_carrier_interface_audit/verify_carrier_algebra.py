#!/usr/bin/env python3
"""Clean-room finite checks for the Dean-5 Type-II carrier reductions.

The routines below implement the displayed mathematical definitions in the
paper rather than importing code or data from its computational supplement.
They check the phase table, both Watkins--Mesner coordinate systems, the
one-cap reduction, the serial-cap normalization, and the weak landing orders.
"""

from __future__ import annotations

from itertools import product


Z5 = range(5)
GOOD = {
    frozenset((0, 1, 3)),
    frozenset((0, 2, 3)),
    frozenset((0, 2, 4)),
    frozenset((1, 2, 4)),
    frozenset((1, 3, 4)),
}
OMEGA = {0, 1, 4}
EVEN_PATHS = {0, 2}


def audit_phase_table() -> None:
    expected = {
        (1, 3): frozenset((1, 2, 4)),
        (2, 0): frozenset((0, 2, 4)),
        (2, 2): frozenset((0, 2, 4)),
        (3, 0): frozenset((1, 2, 4)),
        (3, 3): frozenset((1, 2, 4)),
        (4, 2): frozenset((0, 2, 4)),
    }
    actual = {}
    for eta in range(1, 5):
        for h in Z5:
            excluded = {(-h - 2) % 5, (h - eta - 2) % 5, 3}
            allowed = frozenset(set(Z5) - excluded)
            if any(g <= allowed for g in GOOD):
                actual[(eta, h)] = allowed
    assert actual == expected, (actual, expected)


def carrier_paths(coords: tuple[int, ...], i: int, j: int, k: int) -> tuple[int, ...]:
    a = coords[:3]
    b = coords[3:]
    return (
        (a[i] + a[j]) % 5,
        (b[i] + b[j]) % 5,
        (a[i] + a[k] + b[k] + b[j]) % 5,
        (b[i] + a[k] + b[k] + a[j]) % 5,
    )


def carrier_pair_cycle(coords: tuple[int, ...], i: int, j: int) -> int:
    a = coords[:3]
    b = coords[3:]
    return (a[i] + b[i] + a[j] + b[j]) % 5


def audit_watkins_mesner_coordinates() -> None:
    cubic = []
    aligned = []
    aligned_spectra = {
        frozenset((0, 1)): {0, 2},
        frozenset((0, 2)): {1, 4},
        frozenset((1, 2)): {0, 1, 4},
    }
    for coords in product(Z5, repeat=6):
        cubic_ok = True
        aligned_ok = True
        for i, j in ((0, 1), (0, 2), (1, 2)):
            k = 3 - i - j
            paths = carrier_paths(coords, i, j, k)
            if not set(paths) <= EVEN_PATHS or carrier_pair_cycle(coords, i, j) == 0:
                cubic_ok = False
            if (
                not set(paths) <= aligned_spectra[frozenset((i, j))]
                or carrier_pair_cycle(coords, i, j) == 0
            ):
                aligned_ok = False
        if cubic_ok:
            cubic.append(coords)
        if aligned_ok:
            aligned.append(coords)
    assert cubic == [(0, 0, 0, 1, 1, 1), (1, 1, 1, 0, 0, 0)], cubic
    assert aligned == [], aligned


def adjacency(edges: list[tuple[str, str, int]]) -> dict[str, list[tuple[str, int]]]:
    result: dict[str, list[tuple[str, int]]] = {}
    for u, v, weight in edges:
        result.setdefault(u, []).append((v, weight % 5))
        result.setdefault(v, []).append((u, weight % 5))
    return result


def simple_path_residues(
    graph: dict[str, list[tuple[str, int]]], start: str, end: str
) -> set[int]:
    residues = set()

    def visit(vertex: str, used: frozenset[str], weight: int) -> None:
        if vertex == end:
            residues.add(weight % 5)
            return
        for nxt, edge_weight in graph[vertex]:
            if nxt not in used:
                visit(nxt, used | {nxt}, weight + edge_weight)

    visit(start, frozenset((start,)), 0)
    return residues


def has_zero_cycle(edges: list[tuple[str, str, int]]) -> bool:
    """Enumerate each vertex-simple cycle by fixing its least vertex."""
    graph = adjacency(edges)
    vertices = sorted(graph)
    for start in vertices:
        for first, first_weight in graph[start]:
            if first <= start:
                continue

            def visit(vertex: str, used: tuple[str, ...], weight: int) -> bool:
                for nxt, edge_weight in graph[vertex]:
                    if nxt == start and len(used) >= 3:
                        if (weight + edge_weight) % 5 == 0:
                            return True
                    elif nxt > start and nxt not in used:
                        if visit(nxt, used + (nxt,), weight + edge_weight):
                            return True
                return False

            if visit(first, (start, first), first_weight):
                return True
    return False


def one_cap_edges(q: int, t: int, alpha: int, beta: int) -> list[tuple[str, str, int]]:
    return [
        ("x0", "a", q),
        ("a", "b", t),
        ("b", "x1", 2 - q - t),
        ("x1", "x2", 0),
        ("x2", "x0", 0),
        ("a", "y", alpha),
        ("y", "b", beta),
    ]


def internally_admissible_cap(q: int, t: int, alpha: int, beta: int) -> bool:
    edges = one_cap_edges(q, t, alpha, beta)
    if has_zero_cycle(edges):
        return False
    graph = adjacency(edges)
    centers = ("x0", "x1", "x2")
    for x, z in combinations_of_two(centers):
        if not simple_path_residues(graph, x, z) <= EVEN_PATHS:
            return False
    for center in centers:
        if not simple_path_residues(graph, center, "y") <= OMEGA:
            return False
    return True


def combinations_of_two(items: tuple[str, ...]):
    for i in range(len(items)):
        for j in range(i + 1, len(items)):
            yield items[i], items[j]


def audit_one_cap_reduction() -> None:
    actual = {
        (q, t, alpha, beta)
        for q, t, alpha, beta in product(Z5, repeat=4)
        if internally_admissible_cap(q, t, alpha, beta)
    }
    expected = {
        (4, 2, 2, 0),
        (2, 4, 4, 0),
        (1, 2, 0, 2),
        (4, 4, 2, 2),
        (2, 1, 4, 2),
        (1, 4, 0, 4),
        (4, 1, 2, 4),
        (2, 3, 4, 4),
    }
    assert actual == expected, (actual, expected)


def audit_serial_normalization() -> None:
    """Two surviving sources on one serial cap force a zero-residue middle."""
    surviving_rows = {
        (2, 1): (4, 0),
        (1, 0): (0, 4),
        (2, 0): (4, 4),
    }
    survivors = []
    for phases, arms in surviving_rows.items():
        for left, middle, right in product(Z5, repeat=3):
            row_y = (left, (middle + right) % 5)
            row_z = ((left + middle) % 5, right)
            if row_y == arms and row_z == arms:
                survivors.append((phases, left, middle, right))
    assert survivors == [
        ((2, 1), 4, 0, 0),
        ((1, 0), 0, 0, 4),
        ((2, 0), 4, 0, 4),
    ], survivors


def audit_weak_orders() -> None:
    """Count all ordered partitions with Ly<Ry and Lz<Rz."""
    orders = set()
    for ranks in product(range(4), repeat=4):
        ly, ry, lz, rz = ranks
        used = set(ranks)
        if used != set(range(max(used) + 1)):
            continue
        if ly < ry and lz < rz:
            orders.add(ranks)
    assert len(orders) == 13, sorted(orders)


def main() -> None:
    audit_phase_table()
    audit_watkins_mesner_coordinates()
    audit_one_cap_reduction()
    audit_serial_normalization()
    audit_weak_orders()
    print("PASS Dean-5 Type-II carrier algebra")
    print("phase table survivors: 6")
    print("cubic Watkins-Mesner coordinate survivors: 2")
    print("aligned Watkins-Mesner coordinate survivors: 0")
    print("internally admissible one-cap tuples: 8 of 625")
    print("serial normalized rows: 3; every middle residue is 0")
    print("weak landing orders: 13")


if __name__ == "__main__":
    main()
