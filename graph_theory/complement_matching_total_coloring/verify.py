#!/usr/bin/env python3
"""Definition-level audit for complement-matching total colourings."""

from __future__ import annotations

import hashlib
import json
from itertools import combinations


def vertices(r: int) -> tuple[int, ...]:
    """Use q=2r-1 as the symbol infinity and 0,...,q-1 as residues."""
    if r < 2:
        raise ValueError("r must be at least two")
    q = 2 * r - 1
    return tuple(range(q + 1))


def edge(u: int, v: int) -> tuple[int, int]:
    if u == v:
        raise ValueError("loops are not edges")
    return (u, v) if u < v else (v, u)


def cyclic_color(r: int, u: int, v: int) -> int:
    q = 2 * r - 1
    infinity = q
    if u == v or u not in range(q + 1) or v not in range(q + 1):
        raise ValueError("invalid K_(2r) edge")
    if u == infinity:
        return v
    if v == infinity:
        return u
    return ((u + v) * pow(2, -1, q)) % q


def rainbow_matching(r: int) -> tuple[tuple[int, int], ...]:
    """The explicit matching in THEOREM.md; valid and rainbow for r>=3."""
    if r < 3:
        raise ValueError("the uniform rainbow construction starts at r=3")
    q = 2 * r - 1
    pairs: list[tuple[int, int]] = [(q, 0)]
    if r % 2 == 1:
        m = (r - 1) // 2
        pairs.extend((2 * k - 1, 2 * k) for k in range(1, 2 * m + 1))
    elif r == 4:
        pairs.extend(((1, 3), (2, 6), (4, 5)))
    else:
        m = r // 2
        pairs.extend((2 * k - 1, 2 * k) for k in range(1, m))
        pairs.append((2 * m - 1, 2 * m + 1))
        pairs.extend(
            (2 * m + 2 * t, 2 * m + 3 + 2 * t)
            for t in range(0, m - 3)
        )
        pairs.extend(((4 * m - 6, 4 * m - 2), (4 * m - 4, 4 * m - 3)))
    return tuple(edge(u, v) for u, v in pairs)


def complete_edges(r: int) -> tuple[tuple[int, int], ...]:
    return tuple(combinations(vertices(r), 2))


def verify_one_factorization(r: int) -> None:
    q = 2 * r - 1
    for u in vertices(r):
        seen = {
            cyclic_color(r, u, v)
            for v in vertices(r)
            if v != u
        }
        assert seen == set(range(q))


def verify_rainbow_matching(r: int) -> None:
    q = 2 * r - 1
    matching = rainbow_matching(r)
    assert len(matching) == r
    flat = [u for pair in matching for u in pair]
    assert len(set(flat)) == 2 * r
    assert set(flat) == set(vertices(r))
    colors = [cyclic_color(r, *pair) for pair in matching]
    assert len(set(colors)) == r
    assert all(0 <= color < q for color in colors)


def transferred_coloring(
    r: int, graph_edges: tuple[tuple[int, int], ...]
) -> tuple[dict[int, int], dict[tuple[int, int], int]]:
    matching = rainbow_matching(r)
    mate_color: dict[int, int] = {}
    for u, v in matching:
        color = cyclic_color(r, u, v)
        mate_color[u] = color
        mate_color[v] = color
    edge_colors = {
        edge(u, v): cyclic_color(r, u, v) for u, v in graph_edges
    }
    return mate_color, edge_colors


def check_total_coloring(
    graph_vertices: tuple[int, ...],
    graph_edges: tuple[tuple[int, int], ...],
    vertex_colors: dict[int, int],
    edge_colors: dict[tuple[int, int], int],
) -> bool:
    normalized = tuple(edge(u, v) for u, v in graph_edges)
    if len(set(normalized)) != len(normalized):
        return False
    if set(vertex_colors) != set(graph_vertices):
        return False
    if set(edge_colors) != set(normalized):
        return False
    incident: dict[int, list[tuple[int, int]]] = {v: [] for v in graph_vertices}
    for e in normalized:
        u, v = e
        if u not in incident or v not in incident:
            return False
        if vertex_colors[u] == vertex_colors[v]:
            return False
        if edge_colors[e] in (vertex_colors[u], vertex_colors[v]):
            return False
        incident[u].append(e)
        incident[v].append(e)
    for v in graph_vertices:
        colors = [edge_colors[e] for e in incident[v]]
        if len(colors) != len(set(colors)):
            return False
    return True


def allowed_edges(r: int) -> tuple[tuple[int, int], ...]:
    matching = set(rainbow_matching(r))
    return tuple(e for e in complete_edges(r) if e not in matching)


def thick_spider_edges(r: int) -> tuple[tuple[int, int], ...]:
    matching = rainbow_matching(r)
    left = {u for u, _ in matching}
    right = {v for _, v in matching}
    answer = []
    for e in allowed_edges(r):
        u, v = e
        if u in left and v in left:
            answer.append(e)
        elif (u in left and v in right) or (u in right and v in left):
            answer.append(e)
    return tuple(answer)


def degrees(graph_vertices: tuple[int, ...], graph_edges: tuple[tuple[int, int], ...]) -> dict[int, int]:
    result = {v: 0 for v in graph_vertices}
    for u, v in graph_edges:
        result[u] += 1
        result[v] += 1
    return result


def check_rank_two_boundary() -> None:
    # S_2 has edges x0-x1, x0-y1, x1-y0, represented by 0-1, 0-3, 1-2.
    verts = (0, 1, 2, 3)
    graph_edges = ((0, 1), (0, 3), (1, 2))
    vertex_colors = {0: 0, 1: 1, 2: 2, 3: 2}
    edge_colors = {(0, 1): 2, (0, 3): 1, (1, 2): 0}
    assert check_total_coloring(verts, graph_edges, vertex_colors, edge_colors)
    assert max(degrees(verts, graph_edges).values()) == 2


def main() -> None:
    profile = hashlib.sha256()
    for r in range(3, 101):
        verify_one_factorization(r)
        verify_rainbow_matching(r)
        matching = rainbow_matching(r)
        colors = tuple(cyclic_color(r, *pair) for pair in matching)
        profile.update(f"{r}:{matching}:{colors}\n".encode())

        dense_edges = allowed_edges(r)
        vertex_colors, edge_colors = transferred_coloring(r, dense_edges)
        assert check_total_coloring(vertices(r), dense_edges, vertex_colors, edge_colors)

        spider_edges = thick_spider_edges(r)
        vertex_colors, edge_colors = transferred_coloring(r, spider_edges)
        assert check_total_coloring(vertices(r), spider_edges, vertex_colors, edge_colors)
        degree_values = degrees(vertices(r), spider_edges).values()
        assert max(degree_values) == 2 * r - 2

    check_rank_two_boundary()

    base_edges = allowed_edges(3)
    assert len(base_edges) == 12
    sharp = 0
    for mask in range(1 << len(base_edges)):
        chosen = tuple(e for i, e in enumerate(base_edges) if mask & (1 << i))
        vertex_colors, edge_colors = transferred_coloring(3, chosen)
        assert check_total_coloring(vertices(3), chosen, vertex_colors, edge_colors)
        if max(degrees(vertices(3), chosen).values()) == 4:
            sharp += 1

    print(json.dumps({
        "claim": "complement perfect matching gives an (n-1)-total-colouring for even n>=6",
        "cyclic_factorizations_checked_r": [3, 100],
        "exhaustive_n6_spanning_subgraphs": 1 << len(base_edges),
        "exhaustive_n6_subgraphs_with_delta_4": sharp,
        "rainbow_profile_sha256": profile.hexdigest(),
        "thick_spiders_checked_r": [2, 100],
        "trust_boundary": "universal statement rests on THEOREM.md; code is a definition-level audit",
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
