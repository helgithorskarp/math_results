#!/usr/bin/env python3
"""Explicit 13-part tournament family; Python standard library only."""
from __future__ import annotations

LABELS = ('A0', 'A2', 'B0u', 'B0v', 'B1', 'B2u', 'B2v',
          'C0p', 'C0q', 'C1q', 'C1p', 'C2p', 'C2q')
OUT = (
    (7, 9, 10, 11, 12), (0, 7, 8, 9, 10),
    (0, 1, 3, 4, 7, 8), (0, 1, 4, 7, 8, 11),
    (0, 1, 5, 6, 9, 10, 11), (0, 1, 2, 3, 6, 11, 12),
    (0, 1, 2, 3, 7, 11, 12), (4, 5, 8, 9),
    (0, 4, 5, 6, 9, 10), (2, 3, 5, 6, 10, 11, 12),
    (2, 3, 5, 6, 7, 11, 12), (1, 2, 7, 8, 12),
    (1, 2, 3, 4, 7, 8),
)
TYPES = (0, 0, 0, 0, 1, 0, 0, 0, 2, 2, 0, 0, 2)
SOURCES = (
    (9, 10), (7, 8), (1, 3, 4, 7, 8), (1, 4, 7, 8),
    (0, 5, 6, 9, 10), (2, 3, 6, 11, 12), (2, 3, 11, 12),
    (8,), (0, 4, 5, 6, 9, 10), (2, 3, 5, 6, 10, 11, 12),
    (2, 3, 5, 6, 11, 12), (12,), (1, 2, 3, 4, 7, 8),
)


def weights(a: int, b: int, c: int) -> list[int]:
    if any(type(x) is not int or x <= 0 for x in (a, b, c)):
        raise ValueError('parameters must be positive integers')
    return [(a, b, c)[t] for t in TYPES]


def blowup(a: int = 1, b: int = 2, c: int = 4,
           internal: str = 'transitive') -> tuple[list[int], list[list[int]]]:
    """Bit j in row i means i -> j. Part order follows LABELS."""
    if internal not in ('transitive', 'reverse', 'balanced'):
        raise ValueError('unknown internal tournament rule')
    sizes = weights(a, b, c)
    parts: list[list[int]] = []
    start = 0
    for size in sizes:
        parts.append(list(range(start, start + size)))
        start += size
    graph = [0] * start
    for i, part in enumerate(parts):
        external = sum(1 << v for j in OUT[i] for v in parts[j])
        size = len(part)
        for u, vertex in enumerate(part):
            row = external
            for v, other in enumerate(part):
                if u == v:
                    continue
                if internal == 'transitive':
                    beats = u < v
                elif internal == 'reverse':
                    beats = u > v
                else:
                    distance = (v - u) % size
                    beats = 2 * distance < size or (2 * distance == size and u < v)
                if beats:
                    row |= 1 << other
            graph[vertex] = row
    return graph, parts


def matrix_text(graph: list[int]) -> str:
    return ''.join(''.join(str(row >> j & 1) for j in range(len(graph))) + '\n'
                   for row in graph)


if __name__ == '__main__':
    print(matrix_text(blowup()[0]), end='')
