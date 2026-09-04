#!/usr/bin/env python3
"""Exact audit for the Albertson r=27 local equality-C5 closure.

The topology is proved in README.md.  This checker verifies the defect
arithmetic, terminal equality identities, forced endpoint reconstruction,
and the contradiction in both previously certified residual profiles.
"""

from hashlib import sha256
from itertools import combinations
from json import dumps


N = 24
S = N - 2

# (name, e(D2), x(D2), number of full F^2_5 configurations)
PROFILES = (
    ("A", 103, 57, 9),
    ("B", 106, 64, 11),
)


def defect(edges: int, crossings: int, empty_triangles: int) -> int:
    """Three times the slack in PRTT Lemma 3.2."""
    return 3 * crossings - 7 * edges + 25 * S - 2 * empty_triangles


def edge(*vertices: str) -> frozenset[str]:
    assert len(vertices) == 2 and vertices[0] != vertices[1]
    return frozenset(vertices)


def convex_chords_cross(
    left: frozenset[str], right: frozenset[str], boundary_order: tuple[str, ...]
) -> bool:
    """Whether two endpoint-disjoint chords alternate on a cyclic boundary."""
    if not left.isdisjoint(right):
        return False
    positions = {vertex: index for index, vertex in enumerate(boundary_order)}
    i, j = sorted(positions[vertex] for vertex in left)
    k, ell = (positions[vertex] for vertex in right)
    return (i < k < j) != (i < ell < j)


def triangle_kite_reconstruction() -> dict[str, object]:
    """Enumerate the endpoint choices at the equality triangle--kite.

    The triangle is u-z-w and the quadrilateral is z-w-r-t.  The shared edge
    a=zw is crossed by each restored edge.  Edge c also crosses diagonal
    d=zr, while b also crosses diagonal f=wt.  In a good drawing a restored
    edge cannot use an endpoint of an edge it crosses.
    """
    vertices = ("u", "z", "w", "r", "t")
    a = edge("z", "w")
    d = edge("z", "r")
    f = edge("w", "t")
    triangle_side = {"u", "z", "w"}
    kite_side = {"z", "w", "r", "t"}

    candidates = {edge(x, y) for x in triangle_side for y in kite_side if x != y}
    c_choices = sorted(
        candidates,
        key=lambda item: tuple(sorted(item)),
    )
    c_choices = [candidate for candidate in c_choices if candidate.isdisjoint(a | d)]
    b_choices = [candidate for candidate in candidates if candidate.isdisjoint(a | f)]
    assert c_choices == [edge("u", "t")]
    assert b_choices == [edge("u", "r")]

    c = c_choices[0]
    b = b_choices[0]
    crossed = {a, b, c, d, f}
    boundary = {
        edge("u", "z"),
        edge("z", "t"),
        edge("t", "r"),
        edge("r", "w"),
        edge("w", "u"),
    }
    complete = {edge(x, y) for x, y in combinations(vertices, 2)}
    assert crossed.isdisjoint(boundary)
    assert crossed | boundary == complete

    expected_crossing_pairs = {
        frozenset((a, b)),
        frozenset((a, c)),
        frozenset((c, d)),
        frozenset((d, f)),
        frozenset((f, b)),
    }
    boundary_order = ("u", "z", "t", "r", "w")
    crossing_pairs = {
        frozenset((left, right))
        for left, right in combinations(crossed, 2)
        if convex_chords_cross(left, right, boundary_order)
    }
    assert crossing_pairs == expected_crossing_pairs
    degrees = {crossed_edge: 0 for crossed_edge in crossed}
    for pair in crossing_pairs:
        left, right = tuple(pair)
        degrees[left] += 1
        degrees[right] += 1
    assert len(crossing_pairs) == 5
    assert set(degrees.values()) == {2}

    return {
        "c_choice": sorted(c),
        "b_choice": sorted(b),
        "crossed_edges": sorted(sorted(item) for item in crossed),
        "boundary_edges": sorted(sorted(item) for item in boundary),
        "crossing_degrees": sorted(degrees.values()),
    }


def audit_profile(name: str, edges: int, crossings: int, full: int) -> dict[str, object]:
    assert defect(edges, crossings, 0) == 0

    numerator = 2 * edges - 8 * S
    assert numerator % 3 == 0
    c5 = numerator // 3
    assert c5 == full + 1

    # Each equality C5 reduction deletes two edges and four crossings and
    # creates exactly one empty triangle.
    terminal_edges = edges - 2 * c5
    terminal_crossings = crossings - 4 * c5
    terminal_triangles = c5
    assert defect(terminal_edges, terminal_crossings, terminal_triangles) == 0

    # The two nonnegative slacks in the 1-planar branch both vanish.
    twice_density_slack = 8 * S - terminal_triangles - 2 * terminal_edges
    planarization_slack = terminal_crossings - terminal_edges + 3 * S
    assert twice_density_slack == 0
    assert planarization_slack == 0

    # The equality C5 lemma forces every cycle to be full, contradicting the
    # exact number of full configurations in the certified profile.
    forced_full = c5
    assert forced_full > full

    return {
        "name": name,
        "edges": edges,
        "crossings": crossings,
        "full_reported": full,
        "c5": c5,
        "terminal_edges": terminal_edges,
        "terminal_crossings": terminal_crossings,
        "terminal_empty_triangles": terminal_triangles,
        "forced_full": forced_full,
    }


def main() -> None:
    interface = triangle_kite_reconstruction()
    rows = [audit_profile(*profile) for profile in PROFILES]
    certificate = {"interface": interface, "profiles": rows}
    digest = sha256(dumps(certificate, sort_keys=True).encode("ascii")).hexdigest()

    print("PASS unique triangle-kite restoration is a full pentagon")
    print(f"forced c={interface['c_choice']}, b={interface['b_choice']}")
    for row in rows:
        print(
            f"profile {row['name']}: delta=0, C5={row['c5']}, "
            f"reported_full={row['full_reported']}, "
            f"terminal=(e={row['terminal_edges']},x={row['terminal_crossings']},"
            f"Delta={row['terminal_empty_triangles']})"
        )
    print(f"certificate_sha256={digest}")
    print("PASS both equality profiles contradict the equality C5 lemma")


if __name__ == "__main__":
    main()
