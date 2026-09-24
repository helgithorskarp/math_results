#!/usr/bin/env python3
"""The new minimum 51-vertex example, with transitive parts by default."""
from __future__ import annotations
Q = ((2,3),(4,5),(1,3,4),(1,5),(0,3,5),(0,2))
WEIGHTS = (3,8,16,3,7,14)


def construct(transitive: bool = True) -> list[list[int]]:
    labels = [i for i, size in enumerate(WEIGHTS) for _ in range(size)]
    return [[int(i < j and transitive if a == b else b in Q[a])
             for j, b in enumerate(labels)] for i, a in enumerate(labels)]


if __name__ == '__main__':
    for row in construct():
        print(''.join(map(str,row)))
