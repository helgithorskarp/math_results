#!/usr/bin/env python3
"""Exact incidence audit for the terminal triangle--kite reconstruction.

The Jordan-curve and face-tracing implications are proved in README.md.  This
checker verifies the resulting local plane-map incidence, forced endpoints,
K5 complement, crossing graph, profile arithmetic, and order-54 propagation.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from hashlib import sha256
from itertools import combinations
from json import dumps
from math import comb


Edge = frozenset[str]


def edge(left: str, right: str) -> Edge:
    if left == right:
        raise ValueError("loop")
    return frozenset((left, right))


def face_edges(face: tuple[str, str, str]) -> tuple[Edge, Edge, Edge]:
    return (
        edge(face[0], face[1]),
        edge(face[1], face[2]),
        edge(face[2], face[0]),
    )


def union_boundary(faces: tuple[tuple[str, str, str], ...]) -> set[Edge]:
    incidences = Counter(side for face in faces for side in face_edges(face))
    if set(incidences.values()) != {1, 2}:
        raise AssertionError(incidences)
    return {side for side, count in incidences.items() if count == 1}


def chord_crosses(left: Edge, right: Edge, boundary: tuple[str, ...]) -> bool:
    if not left.isdisjoint(right):
        return False
    position = {vertex: index for index, vertex in enumerate(boundary)}
    i, j = sorted(position[vertex] for vertex in left)
    k, ell = (position[vertex] for vertex in right)
    return (i < k < j) != (i < ell < j)


def local_map_certificate() -> dict[str, object]:
    # x is the planarization vertex of the crossing pair d,f.  The first
    # face is on the non-kite side of shared edge zw; the other four are the
    # complete star of x in the terminal triangulation.
    faces = (
        ("u", "z", "w"),
        ("z", "w", "x"),
        ("w", "r", "x"),
        ("r", "t", "x"),
        ("t", "z", "x"),
    )
    boundary = union_boundary(faces)
    expected_boundary = {
        edge("u", "z"),
        edge("z", "t"),
        edge("t", "r"),
        edge("r", "w"),
        edge("w", "u"),
    }
    if boundary != expected_boundary:
        raise AssertionError((boundary, expected_boundary))

    # An endpoint reached without another crossing must be the third real
    # vertex of the exit face.  It cannot be a crossing vertex or an endpoint
    # of the edge just crossed.
    c_before = set(faces[0]) - {"z", "w"}
    c_after = set(faces[4]) - {"z", "x"}
    b_before = set(faces[0]) - {"z", "w"}
    b_after = set(faces[2]) - {"w", "x"}
    if (c_before, c_after, b_before, b_after) != (
        {"u"},
        {"t"},
        {"u"},
        {"r"},
    ):
        raise AssertionError((c_before, c_after, b_before, b_after))

    crossed = {
        edge("z", "w"),  # a
        edge("u", "r"),  # b
        edge("u", "t"),  # c
        edge("z", "r"),  # d
        edge("w", "t"),  # f
    }
    vertices = ("u", "z", "t", "r", "w")
    complete = {edge(left, right) for left, right in combinations(vertices, 2)}
    if crossed & boundary or crossed | boundary != complete:
        raise AssertionError((crossed, boundary, complete))

    crossing_pairs = {
        frozenset((left, right))
        for left, right in combinations(crossed, 2)
        if chord_crosses(left, right, vertices)
    }
    crossing_degrees = Counter(item for pair in crossing_pairs for item in pair)
    if len(crossing_pairs) != 5 or set(crossing_degrees.values()) != {2}:
        raise AssertionError((crossing_pairs, crossing_degrees))

    return {
        "faces": faces,
        "outer_boundary": sorted(sorted(item) for item in boundary),
        "restored_b": ["u", "r"],
        "restored_c": ["u", "t"],
        "diagonals": sorted(sorted(item) for item in crossed),
        "crossing_degrees": sorted(crossing_degrees.values()),
    }


def profile_certificate() -> tuple[dict[str, int | str], ...]:
    rows = (("A", 103, 57, 9), ("B", 106, 64, 11))
    result: list[dict[str, int | str]] = []
    for name, edges, crossings, full in rows:
        c5_numerator = 2 * edges - 8 * (24 - 2)
        if c5_numerator % 3:
            raise AssertionError((name, c5_numerator))
        c5 = c5_numerator // 3
        terminal_edges = edges - 2 * c5
        terminal_crossings = crossings - 4 * c5
        vertices_planarized = 24 + terminal_crossings
        edges_planarized = terminal_edges + 2 * terminal_crossings
        if edges_planarized != 3 * vertices_planarized - 6:
            raise AssertionError(name)
        if c5 != full + 1:
            raise AssertionError((name, c5, full))
        result.append(
            {
                "name": name,
                "c5": c5,
                "reported_full": full,
                "terminal_edges": terminal_edges,
                "terminal_crossings": terminal_crossings,
                "planar_vertices": vertices_planarized,
                "planar_edges": edges_planarized,
            }
        )
    return tuple(result)


def order54_sampling() -> Fraction:
    bound = Fraction(
        5 * 726 * comb(52, 22) - 495 * comb(54, 24),
        comb(50, 20),
    )
    if bound != Fraction(1965795, 322) or not bound > 6084:
        raise AssertionError(bound)
    return bound


def main() -> None:
    certificate = {
        "local_map": local_map_certificate(),
        "profiles": profile_certificate(),
        "order54_sampling": str(order54_sampling()),
    }
    digest = sha256(dumps(certificate, sort_keys=True).encode("ascii")).hexdigest()
    print("PASS terminal triangle--kite incidence forces the full K5 pentagon")
    print("forced restored edges: b=ur, c=ut")
    for row in certificate["profiles"]:
        print(
            f"profile {row['name']}: C5={row['c5']}, "
            f"reported_full={row['reported_full']}, "
            f"terminal=(e={row['terminal_edges']},x={row['terminal_crossings']})"
        )
    print(f"order54_sampling={certificate['order54_sampling']}")
    print(f"certificate_sha256={digest}")


if __name__ == "__main__":
    main()
