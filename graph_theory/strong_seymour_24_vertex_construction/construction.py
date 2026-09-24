#!/usr/bin/env python3
"""Nine-fibre construction; exact integers and standard library only."""
from __future__ import annotations


def validate_quotient(out: list[list[int]]) -> None:
    q = len(out)
    if q == 0:
        raise ValueError('empty quotient')
    for i, row in enumerate(out):
        if len(set(row)) != len(row) or any(type(j) is not int or not 0 <= j < q or j == i for j in row):
            raise ValueError('invalid quotient row')
        for j in range(q):
            if i != j and ((j in row) + (i in out[j]) != 1):
                raise ValueError('quotient is not a tournament')


def hall_rows(out: list[list[int]], sources: list[list[int]]) -> tuple[list[list[int]], list[list[int]]]:
    validate_quotient(out)
    q = len(out)
    if len(sources) != q:
        raise ValueError('one Hall set per root required')
    rows, targets = [], []
    for p, source in enumerate(sources):
        if not source or len(set(source)) != len(source) or not set(source) <= set(out[p]):
            raise ValueError('invalid Hall source set')
        target = sorted(set().union(*(set(out[j]) for j in source)) - set(out[p]) - {p})
        rows.append([int(j in source) - int(j in target) for j in range(q)])
        targets.append(target)
    return rows, targets


def blowup(out: list[list[int]], weights: list[int], *, balanced: bool = False) -> tuple[list[list[int]], list[list[int]]]:
    """Transitive fibres by default; balanced=True uses cyclic odd fibres.

    For even fibres, delete one vertex from the cyclic tournament of order s+1.
    Thus this option is defined for every positive fibre size.
    """
    validate_quotient(out)
    if len(weights) != len(out) or any(type(s) is not int or s < 1 for s in weights):
        raise ValueError('positive integer weights required')
    fibres, labels = [], []
    for i, size in enumerate(weights):
        fibres.append(list(range(len(labels), len(labels) + size)))
        labels.extend([i] * size)
    n = len(labels)
    adj = [[0] * n for _ in range(n)]
    for i, vertices in enumerate(fibres):
        size = len(vertices)
        modulus = size if size % 2 else size + 1
        for a, u in enumerate(vertices):
            for b, v in enumerate(vertices):
                if a != b:
                    adj[u][v] = int(0 < (b - a) % modulus <= modulus // 2) if balanced else int(a < b)
            for j in out[i]:
                for v in fibres[j]:
                    adj[u][v] = 1
    return adj, fibres


def cyclic_data(a: int, b: int, c: int) -> tuple[list[list[int]], list[int], list[list[int]]]:
    """Labels A0,A1,A2,B0,B1,B2,C0,C1,C2; all parameters positive."""
    if any(type(x) is not int or x < 1 for x in (a, b, c)):
        raise ValueError('positive integer parameters required')
    out, sources = [[] for _ in range(9)], [[] for _ in range(9)]
    for i in range(3):
        j, k = (i + 1) % 3, (i + 2) % 3
        out[i] = sorted([j, 6 + j, 6 + k])
        out[3 + i] = sorted([0, 1, 2, 3 + j, 6 + i])
        out[6 + i] = sorted([i, 3 + j, 3 + k, 6 + j])
        sources[i] = [6 + j]
        sources[3 + i] = sorted([k, 3 + j, 6 + i])
        sources[6 + i] = out[6 + i][:]
    return out, [a] * 3 + [b] * 3 + [c] * 3, sources
