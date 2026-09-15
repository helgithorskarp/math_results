#!/usr/bin/env python3
"""Independent physical audit using real/imaginary quadratic coordinates.

A tuple (a,b,c,d) means x=a+b*sqrt(13), y=sqrt(3)*(c+d*sqrt(13)).
This checker does not import verify.py and never implements its field product.
"""

from collections import Counter
from fractions import Fraction as F
from hashlib import sha256
from itertools import combinations
import json


ONE = (F(1), F(0), F(0), F(0))
THREE_WORD = (
    "0101120112121200111111101112201101122011201112201220220011101121100200110121122010111220010122220011112220022222001111121111220011121212212200111102210102200001111111220000010011111122010101212110121122010111222010100000211120022220221101101200111200011212001111211211111112201010112011212"
)
POINT_SHA = "764ab9a0e1de2441d4028c47c678b47a0a66852b4c2d5aa1c41541451689224f"
EDGE_SHA = "2c90fad7388ce64a4e7f3c2df6f210b479d211c9076bd6f3b8c76e838e25e659"


def require(condition, message):
    if not condition:
        raise ValueError(message)


def add(p, q):
    return tuple(a + b for a, b in zip(p, q))


def subtract(p, q):
    return tuple(a - b for a, b in zip(p, q))


def rotate60(p):
    a, b, c, d = p
    return (
        (a - 3 * c) / 2,
        (b - 3 * d) / 2,
        (a + c) / 2,
        (b + d) / 2,
    )


def squared_norm(p):
    a, b, c, d = p
    return (
        a * a + 13 * b * b + 3 * c * c + 39 * d * d,
        2 * a * b + 6 * c * d,
    )


def is_unit(p):
    return squared_norm(p) == (F(1), F(0))


def point_key(p):
    return tuple((q.numerator, q.denominator) for q in p)


def stream_sha(rows):
    digest = sha256()
    for row in rows:
        digest.update((" ".join(map(str, row)) + "\n").encode())
    return digest.hexdigest()


def main():
    phases = [
        ONE,
        (F(5, 8), F(0), F(0), F(1, 8)),
        (F(0), F(1, 4), F(1, 4), F(0)),
        (F(0), F(-1, 5), F(2, 5), F(0)),
    ]
    require(all(is_unit(p) for p in phases), "phase norm")
    directions = []
    for phase in phases:
        point = phase
        for _ in range(6):
            directions.append(point)
            point = rotate60(point)
        require(point == phase, "rotation order")
    require(len(set(directions)) == 24, "direction count")

    addresses = [add(a, b) for a in directions for b in directions]
    points = sorted(set(addresses), key=point_key)
    index = {point: i for i, point in enumerate(points)}
    multiplicities = Counter(index[point] for point in addresses)
    require(len(points) == 289, "point count")
    require(Counter(multiplicities.values()) == {1: 24, 2: 264, 24: 1}, "multiplicities")

    edges = [
        (u, v)
        for u, v in combinations(range(len(points)), 2)
        if is_unit(subtract(points[u], points[v]))
    ]
    require(len(edges) == 1032, "edge count")
    generator_edges = {
        tuple(sorted((index[p], index[add(p, direction)])))
        for p in points
        for direction in directions
        if add(p, direction) in index
    }
    require(set(edges) == generator_edges, "unaccounted unit contact")

    point_hash = stream_sha(
        tuple(q for x in p for q in (x.numerator, x.denominator))
        for p in points
    )
    edge_hash = stream_sha(edges)
    require(point_hash == POINT_SHA and edge_hash == EDGE_SHA, "stream hash")
    require(len(THREE_WORD) == 289, "word size")
    colours = tuple(map(int, THREE_WORD))
    require(all(colours[u] != colours[v] for u, v in edges), "three-colouring")

    adjacency = [set() for _ in points]
    degrees = [0] * len(points)
    for u, v in edges:
        adjacency[u].add(v)
        adjacency[v].add(u)
        degrees[u] += 1
        degrees[v] += 1
    triangle = next(
        (u, v, min(adjacency[u] & adjacency[v]))
        for u, v in edges
        if adjacency[u] & adjacency[v]
    )
    require(triangle == (0, 1, 62), "triangle")
    require(Counter(degrees) == {3: 24, 4: 24, 6: 216, 24: 25}, "degree histogram")
    print(
        json.dumps(
            {
                "checks": "all passed",
                "coordinates": "x=a+b*sqrt(13), y=sqrt(3)*(c+d*sqrt(13))",
                "directions": 24,
                "points": 289,
                "edges": 1032,
                "incidental_edges": 0,
                "triangle": list(triangle),
                "three_colouring": True,
                "chromatic_number": 3,
                "point_sha256": point_hash,
                "edge_sha256": edge_hash,
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
