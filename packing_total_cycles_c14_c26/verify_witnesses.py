#!/usr/bin/env python3
"""Check coloring certificates directly in the definition of T(C_n)."""

from __future__ import annotations

import json
from collections import deque
from pathlib import Path


HERE = Path(__file__).resolve().parent


def total_graph(n: int) -> list[set[int]]:
    """Return T(C_n), indexed v_0,e_0,v_1,e_1,... ."""
    graph = [set() for _ in range(2 * n)]

    def connect(a: int, b: int) -> None:
        graph[a].add(b)
        graph[b].add(a)

    for j in range(n):
        nxt = (j + 1) % n
        prv = (j - 1) % n
        vertex = 2 * j
        edge = 2 * j + 1
        connect(vertex, 2 * nxt)       # adjacent vertices
        connect(edge, 2 * nxt + 1)    # incident edges
        connect(vertex, edge)          # v_j incident with e_j
        connect(vertex, 2 * prv + 1)  # v_j incident with e_(j-1)
    return graph


def distances(graph: list[set[int]]) -> list[list[int]]:
    answer: list[list[int]] = []
    for source in range(len(graph)):
        row = [-1] * len(graph)
        row[source] = 0
        queue = deque([source])
        while queue:
            current = queue.popleft()
            for neighbor in graph[current]:
                if row[neighbor] == -1:
                    row[neighbor] = row[current] + 1
                    queue.append(neighbor)
        if any(value < 0 for value in row):
            raise AssertionError("total graph unexpectedly disconnected")
        answer.append(row)
    return answer


def verify_witness(n: int, claimed: int, word: list[int]) -> None:
    if len(word) != 2 * n:
        raise AssertionError(f"C_{n}: expected {2*n} entries, got {len(word)}")
    if min(word) < 1 or max(word) > claimed:
        raise AssertionError(f"C_{n}: color outside 1,...,{claimed}")
    metric = distances(total_graph(n))
    for a in range(2 * n):
        for b in range(a + 1, 2 * n):
            if word[a] == word[b] and metric[a][b] <= word[a]:
                raise AssertionError(
                    f"C_{n}: positions {a},{b} repeat color {word[a]} "
                    f"at total-graph distance {metric[a][b]}"
                )


def load_witnesses(path: Path = HERE / "witnesses.json") -> dict[str, dict[str, object]]:
    with path.open(encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise AssertionError("witness file must contain an object")
    return data


def main() -> None:
    data = load_witnesses()
    expected_orders = list(range(14, 27))
    actual_orders = sorted(map(int, data))
    if actual_orders != expected_orders:
        raise AssertionError(f"unexpected order set: {actual_orders}")
    for n in expected_orders:
        item = data[str(n)]
        verify_witness(n, int(item["claimed_chi"]), list(map(int, item["word"])))
    print("verified 13 packing total coloring witnesses for C_14 through C_26")


if __name__ == "__main__":
    main()
