#!/usr/bin/env python3
"""Build the frozen three-sqrt(3)-centre lens-orbit certificate."""

from __future__ import annotations

import argparse
import hashlib
import json
from itertools import combinations
from pathlib import Path


CENTRES = ((0, 0), (2, 0), (1, 3))
LENSES = (
    ((0, 1), ((1, -1), (1, 1))),
    ((0, 2), ((0, 2), (1, 1))),
    ((1, 2), ((1, 1), (2, 2))),
)


def rotate60(vector: tuple[int, int]) -> tuple[int, int]:
    """Rotate (s*sqrt(3)/2,t/2) counterclockwise by pi/3."""
    s, t = vector
    if (s - t) % 2 or (3 * s + t) % 2:
        raise ValueError("rotation left the integer coordinate lattice")
    return ((s - t) // 2, (3 * s + t) // 2)


def norm4(p: tuple[int, int], q: tuple[int, int]) -> int:
    """Four times squared Euclidean distance."""
    ds, dt = p[0] - q[0], p[1] - q[1]
    return 3 * ds * ds + dt * dt


def stream_hash(lines: list[str]) -> str:
    return hashlib.sha256("".join(lines).encode("ascii")).hexdigest()


def build_points() -> list[tuple[int, int]]:
    points = set(CENTRES)
    for owners, intersections in LENSES:
        for point in intersections:
            for owner_index in owners:
                owner = CENTRES[owner_index]
                vector = (point[0] - owner[0], point[1] - owner[1])
                for _ in range(6):
                    points.add((owner[0] + vector[0], owner[1] + vector[1]))
                    vector = rotate60(vector)
    return sorted(points)


def find_word(
    adjacency: list[set[int]], pins: dict[int, int], colours: int = 4
) -> str:
    word = [-1] * len(adjacency)
    for vertex, colour in pins.items():
        word[vertex] = colour
    for vertex, colour in pins.items():
        if any(word[other] == colour for other in adjacency[vertex]):
            raise ValueError("inconsistent pin request")

    def search(remaining: int) -> bool:
        if remaining == 0:
            return True
        uncoloured = [v for v, colour in enumerate(word) if colour < 0]
        vertex = max(
            uncoloured,
            key=lambda v: (
                len({word[w] for w in adjacency[v] if word[w] >= 0}),
                len(adjacency[v]),
                -v,
            ),
        )
        forbidden = {word[w] for w in adjacency[vertex] if word[w] >= 0}
        for colour in range(colours):
            if colour not in forbidden:
                word[vertex] = colour
                if search(remaining - 1):
                    return True
                word[vertex] = -1
        return False

    remaining = sum(colour < 0 for colour in word)
    if not search(remaining):
        raise ValueError("pin request unexpectedly has no four-colouring")
    return "".join(str(colour) for colour in word)


def build_certificate() -> dict[str, object]:
    points = build_points()
    edges = [
        (i, j)
        for i, j in combinations(range(len(points)), 2)
        if norm4(points[i], points[j]) == 4
    ]
    adjacency = [set() for _ in points]
    for left, right in edges:
        adjacency[left].add(right)
        adjacency[right].add(left)
    index = {point: i for i, point in enumerate(points)}
    centre_indices = [index[point] for point in CENTRES]
    patterns = ("000", "001", "010", "011", "012")
    witnesses = {
        pattern: find_word(
            adjacency,
            {centre_indices[i]: int(pattern[i]) for i in range(3)},
        )
        for pattern in patterns
    }
    point_hash = stream_hash([f"{s} {t}\n" for s, t in points])
    edge_hash = stream_hash([f"{i} {j}\n" for i, j in edges])
    return {
        "format": "hn-three-sqrt3-lens-orbit-v1",
        "coordinate_convention": "(s,t) means (s*sqrt(3)/2,t/2)",
        "centres": [list(point) for point in CENTRES],
        "lenses": [
            {
                "owners": list(owners),
                "intersections": [list(point) for point in intersections],
            }
            for owners, intersections in LENSES
        ],
        "points": [list(point) for point in points],
        "edges": [list(edge) for edge in edges],
        "centre_indices": centre_indices,
        "three_colouring": "".join(str(point[1] % 3) for point in points),
        "centre_relation_witnesses": witnesses,
        "unit_triangle": [index[(0, 0)], index[(0, 2)], index[(1, 1)]],
        "hashes": {"points": point_hash, "edges": edge_hash},
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", required=True, type=Path)
    args = parser.parse_args()
    if args.out.exists():
        raise SystemExit(f"refusing to overwrite {args.out}")
    data = build_certificate()
    args.out.write_text(
        json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()
