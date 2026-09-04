#!/usr/bin/env python3
"""Exact arithmetic audit for the Albertson r=27 h=19 incidence pruning."""

from hashlib import sha256
from itertools import combinations
from math import comb


K = 27
H = 19
LOW_ORDER = 34


def clique(edges: set[tuple[int, int]], vertices: tuple[int, ...]) -> None:
    for u, v in combinations(vertices, 2):
        edges.add((min(u, v), max(u, v)))


def low_form(name: str) -> tuple[set[tuple[int, int]], tuple[int, ...]]:
    edges: set[tuple[int, int]] = set()
    if name in {"A0", "A1"}:
        blocks = (tuple(range(18)), tuple(range(18, 26)), tuple(range(26, 34)))
        for block in blocks:
            clique(edges, block)
        if name == "A1":
            edges.add((18, 26))
        big = blocks[0]
    elif name == "B":
        big = tuple(range(19))
        clique(edges, big)
        clique(edges, tuple(range(19, 27)))
        clique(edges, (19, *range(27, 34)))
    elif name == "C":
        big = tuple(range(18))
        clique(edges, big)
        clique(edges, tuple(range(18, 26)))
        clique(edges, (18, *range(26, 34)))
    else:
        raise ValueError(name)
    return edges, big


def core_threshold(c: int) -> int:
    """Minimum handshake bound for a c-critical core of order at least c+1."""
    return ((c - 1) * (c + 1) + 1) // 2


def main() -> None:
    data = {
        "A0": {"low_edges": 209, "high_edges": 38, "c": 9, "big": 18},
        "A1": {"low_edges": 210, "high_edges": 39, "c": 9, "big": 18},
        "B": {"low_edges": 227, "high_edges": 56, "c": 11, "big": 19},
        "C": {"low_edges": 217, "high_edges": 46, "c": 10, "big": 18},
    }

    records: list[tuple[object, ...]] = []
    for name, row in data.items():
        edges, big = low_form(name)
        assert len(big) == row["big"]
        assert len(edges) == row["low_edges"]
        assert len({v for edge in edges for v in edge} | set(range(LOW_ORDER))) == LOW_ORDER

        degrees = [0] * LOW_ORDER
        for u, v in edges:
            degrees[u] += 1
            degrees[v] += 1
        assert max(degrees[v] for v in big) == len(big) - 1

        c = row["c"]
        high_edges = row["high_edges"]
        threshold = core_threshold(c)
        assert high_edges < threshold
        residual = high_edges - comb(c, 2)
        assert residual >= 0
        records.append((name, len(edges), tuple(sorted(degrees)), threshold, residual))

    # In either A case, one colour contains a K9 vertex and two outsiders.
    # Its three high-degree sum is at most 8+2r, where r is the number of
    # edges outside the forced K9.  The other low vertices number 16.
    a_margins = {}
    for name in ("A0", "A1"):
        row = data[name]
        residual = row["high_edges"] - comb(9, 2)
        max_high_degree_sum = 8 + 2 * residual
        forced_big_incidence = 3 * K - 3 * (LOW_ORDER - row["big"]) - max_high_degree_sum
        rigid_capacity = row["big"]
        margin = forced_big_incidence - rigid_capacity
        assert margin > 0
        a_margins[name] = margin

    # In B,c=11 and C,c=10, a core colour outside F has no neighbour in B.
    # At most one residual high edge meets it.
    endpoint_degrees = {}
    for name in ("B", "C"):
        row = data[name]
        c = row["c"]
        residual = row["high_edges"] - comb(c, 2)
        assert residual == 1
        max_degree = (c - 1) + residual + (LOW_ORDER - row["big"])
        assert max_degree == K - 1
        endpoint_degrees[name] = max_degree

    record = repr((records, sorted(a_margins.items()), sorted(endpoint_degrees.items())))
    digest = sha256(record.encode("ascii")).hexdigest()
    assert digest == "34e557c7105ce427a60a0076852033f334c19231c97f5905ea45a48a99d05ffc"

    print("PASS Albertson r=27 h=19 incidence pruning")
    thresholds = {name: core_threshold(row["c"]) for name, row in data.items()}
    print(f"core_thresholds={thresholds}")
    print(f"A_form_incidence_margins={a_margins}")
    print(f"outside_F_degree_caps={endpoint_degrees}")
    print("survivors=B with c in {8,9,10}; C with c=9")
    print(f"result_sha256={digest}")


if __name__ == "__main__":
    main()
