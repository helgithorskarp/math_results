#!/usr/bin/env python3
"""Small deterministic DSATUR routine; solver output is checked explicitly."""

import sys

sys.setrecursionlimit(10000)


def colour_graph(vertices, edges, colours=4):
    adjacency = [set() for _ in range(vertices)]
    for left, right in edges:
        adjacency[left].add(right)
        adjacency[right].add(left)
    row = [-1] * vertices
    nodes = 0

    def search(depth):
        nonlocal nodes
        nodes += 1
        if depth == vertices:
            return True
        candidates = []
        for vertex in range(vertices):
            if row[vertex] >= 0:
                continue
            used = {row[neighbor] for neighbor in adjacency[vertex]
                    if row[neighbor] >= 0}
            candidates.append((len(used), len(adjacency[vertex]), -vertex,
                               vertex, used))
        _sat, _degree, _minus_vertex, vertex, used = max(candidates)
        for colour in range(colours):
            if colour not in used:
                row[vertex] = colour
                if search(depth + 1):
                    return True
        row[vertex] = -1
        return False

    return (tuple(row) if search(0) else None), nodes


def valid_colouring(vertices, edges, row, colours=4):
    return (row is not None and len(row) == vertices
            and all(isinstance(value, int) and 0 <= value < colours for value in row)
            and all(row[left] != row[right] for left, right in edges))
