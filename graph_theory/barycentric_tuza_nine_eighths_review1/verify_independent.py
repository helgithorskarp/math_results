#!/usr/bin/env python3
"""Independent exact audit of the barycentric 9/8 Tuza bound.

CPython 3.11+, standard library only.  This file imports no target code or
output.  Unlike the submitted switch-mask/gluing checker, it computes both
frustration parameters from their deletion definitions, exhausts boundary
parity on small labelled triangle complexes, and implements vertex-link
normalization while transporting oriented facets explicitly.
"""

from collections import Counter, defaultdict, deque
from hashlib import sha256
from itertools import combinations
import argparse
import json
from pathlib import Path


def require(condition, message):
    if not condition:
        raise ValueError(message)


# Each signed edge is (u,v,p), where p=1 means that coherent labels differ.
# These five tables are a direct reading of Figure 1 in arXiv:2511.15226v1.
EXCEPTIONS = {
    "Gamma1": (4, (
        (2, 3, 0), (1, 3, 0), (0, 1, 0), (0, 2, 0),
        (1, 2, 1), (0, 3, 1))),
    "Gamma2": (5, (
        (2, 3, 0), (1, 3, 0), (0, 1, 0), (0, 2, 0), (2, 4, 0),
        (1, 4, 1), (0, 3, 1))),
    "Gamma3": (8, (
        (1, 2, 0), (2, 3, 0), (3, 4, 0), (4, 5, 0), (1, 6, 0),
        (0, 2, 0), (0, 6, 0), (3, 7, 0), (5, 7, 0),
        (5, 6, 1), (0, 1, 1), (4, 7, 1))),
    "Gamma4": (8, (
        (1, 2, 0), (2, 3, 0), (4, 5, 0), (1, 5, 0), (3, 6, 0),
        (4, 6, 0), (0, 1, 0), (0, 7, 0), (6, 7, 0),
        (0, 2, 1), (3, 4, 1), (5, 7, 1))),
    "Gamma5": (8, (
        (0, 1, 0), (1, 2, 0), (2, 3, 0),
        (4, 5, 0), (5, 6, 0), (4, 7, 0),
        (0, 4, 0), (2, 6, 0), (3, 7, 0),
        (0, 3, 1), (6, 7, 1), (1, 5, 1))),
}

TETRAHEDRON = tuple(combinations(range(4), 3))
MOBIUS_FIVE = (
    (0, 1, 2), (0, 1, 3), (0, 2, 4), (1, 3, 4), (2, 3, 4),
)
PROJECTIVE_PLANE = (
    (0, 1, 2), (0, 1, 3), (0, 2, 4), (0, 3, 5), (0, 4, 5),
    (1, 2, 5), (1, 3, 4), (1, 4, 5), (2, 3, 4), (2, 3, 5),
)


def normalized_signed_edges(number, edges):
    result = []
    seen = set()
    for u, v, parity in edges:
        require(0 <= u < number and 0 <= v < number and u != v,
                "invalid signed edge endpoint")
        u, v = sorted((u, v))
        require((u, v) not in seen and parity in (0, 1),
                "signed graph is not simple")
        seen.add((u, v))
        result.append((u, v, parity))
    return tuple(sorted(result))


def is_balanced(number, edges, removed_vertices=frozenset(),
                removed_edges=frozenset()):
    adjacency = [[] for _ in range(number)]
    for index, (u, v, parity) in enumerate(edges):
        if index in removed_edges or u in removed_vertices or v in removed_vertices:
            continue
        adjacency[u].append((v, parity))
        adjacency[v].append((u, parity))
    labels = {}
    for start in range(number):
        if start in removed_vertices or start in labels:
            continue
        labels[start] = 0
        queue = deque([start])
        while queue:
            u = queue.popleft()
            for v, parity in adjacency[u]:
                expected = labels[u] ^ parity
                if v in labels:
                    if labels[v] != expected:
                        return False
                else:
                    labels[v] = expected
                    queue.append(v)
    return True


def edge_frustration_by_deletion(number, edges):
    for size in range(len(edges) + 1):
        for deleted in combinations(range(len(edges)), size):
            if is_balanced(number, edges, removed_edges=frozenset(deleted)):
                return size
    raise ValueError("edge deletion search did not terminate")


def vertex_frustration_by_deletion(number, edges):
    for size in range(number + 1):
        for deleted in combinations(range(number), size):
            if is_balanced(number, edges, removed_vertices=frozenset(deleted)):
                return size
    raise ValueError("vertex deletion search did not terminate")


def degree_sequence(number, edges):
    degrees = [0] * number
    for u, v, _ in edges:
        degrees[u] += 1
        degrees[v] += 1
    return tuple(sorted(degrees, reverse=True))


def connected(number, unsigned_edges, omitted=None):
    adjacency = [set() for _ in range(number)]
    for edge in unsigned_edges:
        if edge == omitted:
            continue
        u, v = edge
        adjacency[u].add(v)
        adjacency[v].add(u)
    seen = {0}
    stack = [0]
    while stack:
        u = stack.pop()
        for v in adjacency[u] - seen:
            seen.add(v)
            stack.append(v)
    return len(seen) == number


def is_two_edge_connected(number, edges):
    unsigned = {tuple(sorted((u, v))) for u, v, _ in edges}
    return connected(number, unsigned) and all(
        connected(number, unsigned, edge) for edge in unsigned
    )


def oriented_facet_data(oriented_facets):
    oriented_facets = tuple(tuple(facet) for facet in oriented_facets)
    require(oriented_facets, "empty facet family")
    require(all(len(facet) == 3 and len(set(facet)) == 3
                for facet in oriented_facets), "invalid triangular facet")
    require(len({frozenset(facet) for facet in oriented_facets}) ==
            len(oriented_facets), "duplicate facet")
    incidence = defaultdict(list)
    for index, (a, b, c) in enumerate(oriented_facets):
        for start, end in ((a, b), (b, c), (c, a)):
            incidence[tuple(sorted((start, end)))].append((index, start, end))
    require(max(map(len, incidence.values())) <= 2,
            "an edge lies in more than two facets")
    signed_edges = []
    boundary = []
    for edge, entries in incidence.items():
        if len(entries) == 1:
            boundary.append(edge)
            continue
        (left, a, b), (right, c, d) = entries
        require({a, b} == {c, d}, "shared-edge endpoints changed")
        parity = int((a, b) == (c, d))
        signed_edges.append((left, right, parity))
    return (normalized_signed_edges(len(oriented_facets), signed_edges),
            tuple(sorted(boundary)))


def link_components(oriented_facets, vertex):
    adjacency = defaultdict(set)
    for facet in oriented_facets:
        if vertex not in facet:
            continue
        other = [item for item in facet if item != vertex]
        adjacency[other[0]].add(other[1])
        adjacency[other[1]].add(other[0])
    require(adjacency, "unused vertex in normalization")
    unseen = set(adjacency)
    components = []
    while unseen:
        start = min(unseen)
        component = {start}
        stack = [start]
        while stack:
            u = stack.pop()
            for v in adjacency[u] - component:
                component.add(v)
                stack.append(v)
        unseen -= component
        components.append(frozenset(component))
    return tuple(components), adjacency


def normalize_closed_complex(oriented_facets):
    _, boundary = oriented_facet_data(oriented_facets)
    require(not boundary, "normalization fixture is not closed")
    vertices = sorted({v for facet in oriented_facets for v in facet})
    component_at = {}
    new_vertex = {}
    next_vertex = 0
    split_count = 0
    for vertex in vertices:
        components, adjacency = link_components(oriented_facets, vertex)
        require(all(len(adjacency[v]) == 2 for v in adjacency),
                "closed link is not 2-regular")
        split_count += len(components) - 1
        for component_index, component in enumerate(components):
            new_vertex[(vertex, component_index)] = next_vertex
            next_vertex += 1
            for neighbor in component:
                require((vertex, neighbor) not in component_at,
                        "link components overlap")
                component_at[(vertex, neighbor)] = component_index
    normalized = []
    for facet in oriented_facets:
        mapped = []
        for index, vertex in enumerate(facet):
            neighbor = facet[(index + 1) % 3]
            component_index = component_at[(vertex, neighbor)]
            mapped.append(new_vertex[(vertex, component_index)])
        normalized.append(tuple(mapped))
    normalized_edges, normalized_boundary = oriented_facet_data(normalized)
    require(not normalized_boundary, "normalization created a boundary")
    for vertex in sorted({v for facet in normalized for v in facet}):
        components, adjacency = link_components(normalized, vertex)
        require(len(components) == 1 and all(len(adjacency[v]) == 2
                                            for v in adjacency),
                "normalized vertex link is not one cycle")
    return tuple(normalized), normalized_edges, split_count


def boundary_degree_data(facets):
    _, boundary = oriented_facet_data(tuple(tuple(sorted(facet)) for facet in facets))
    degrees = Counter(v for edge in boundary for v in edge)
    return boundary, degrees


def audit_boundary_parity(max_labels=5):
    valid = 0
    histogram = Counter()
    digest = sha256()
    for labels in range(3, max_labels + 1):
        triangles = tuple(combinations(range(labels), 3))
        for mask in range(1, 1 << len(triangles)):
            facets = tuple(triangles[i] for i in range(len(triangles))
                           if mask & (1 << i))
            edge_counts = Counter(tuple(sorted(edge)) for facet in facets
                                  for edge in combinations(facet, 2))
            if max(edge_counts.values()) > 2:
                continue
            boundary, degrees = boundary_degree_data(facets)
            require(all(degree % 2 == 0 for degree in degrees.values()),
                    "boundary parity failed")
            require(len(boundary) not in (1, 2),
                    "nonempty Eulerian simple boundary has fewer than 3 edges")
            valid += 1
            histogram[len(boundary)] += 1
            digest.update(json.dumps([labels, mask, len(boundary)],
                                     separators=(",", ":")).encode())
    return {
        "label_orders": [3, max_labels],
        "valid_facet_families": valid,
        "boundary_edge_histogram": dict(sorted(histogram.items())),
        "record_digest": digest.hexdigest(),
    }


def minimum_nonorientable_surface_facets():
    feasible = []
    for vertices in range(2, 40):
        for characteristic in range(-30, 2):
            facets = 2 * (vertices - characteristic)
            edges = 3 * (vertices - characteristic)
            if edges <= vertices * (vertices - 1) // 2:
                feasible.append((facets, vertices, characteristic))
    return min(feasible)


def audit_exceptions():
    expected = {"Gamma1": 2, "Gamma2": 2, "Gamma3": 3,
                "Gamma4": 3, "Gamma5": 3}
    result = {}
    for name, (number, raw_edges) in EXCEPTIONS.items():
        edges = normalized_signed_edges(number, raw_edges)
        require(is_two_edge_connected(number, edges),
                f"{name} is not 2-edge-connected")
        edge_value = edge_frustration_by_deletion(number, edges)
        vertex_value = vertex_frustration_by_deletion(number, edges)
        require(edge_value == vertex_value == expected[name],
                f"{name} frustration mismatch")
        degrees = degree_sequence(number, edges)
        forced_boundary = 3 * number - 2 * len(edges)
        if name == "Gamma2":
            require(degrees == (3, 3, 3, 3, 2) and forced_boundary == 1,
                    "Gamma2 boundary obstruction mismatch")
            obstruction = "one_boundary_edge"
        else:
            require(set(degrees) == {3} and number < 10 and edge_value > 0,
                    f"{name} closed nonorientable obstruction mismatch")
            obstruction = "closed_unbalanced_below_ten_facets"
        result[name] = {
            "vertices": number,
            "edges": len(edges),
            "degrees": degrees,
            "edge_frustration": edge_value,
            "vertex_frustration": vertex_value,
            "forced_boundary_edges": forced_boundary,
            "obstruction": obstruction,
        }
    return result


def audit_controls():
    controls = {}
    for name, facets, expected in (
            ("tetrahedron", TETRAHEDRON, 0),
            ("mobius_five", MOBIUS_FIVE, 1),
            ("projective_plane", PROJECTIVE_PLANE, 3)):
        oriented = tuple(tuple(sorted(facet)) for facet in facets)
        signed_edges, boundary = oriented_facet_data(oriented)
        edge_value = edge_frustration_by_deletion(len(oriented), signed_edges)
        vertex_value = vertex_frustration_by_deletion(len(oriented), signed_edges)
        require(edge_value == vertex_value == expected,
                f"{name} frustration mismatch")
        require(is_two_edge_connected(len(oriented), signed_edges),
                f"{name} dual is not 2-edge-connected")
        if not boundary:
            normalized, transported_edges, splits = normalize_closed_complex(oriented)
            require(transported_edges == signed_edges,
                    f"{name} normalization changed the oriented signed dual")
            normalized_vertices = len({v for facet in normalized for v in facet})
        else:
            splits = None
            normalized_vertices = None
        controls[name] = {
            "facets": len(oriented),
            "dual_edges": len(signed_edges),
            "boundary_edges": len(boundary),
            "edge_frustration": edge_value,
            "vertex_frustration": vertex_value,
            "normalization_splits": splits,
            "normalized_vertices": normalized_vertices,
        }

    # Two tetrahedral spheres meeting only at a vertex test genuine splitting.
    pinched = tuple(tuple(facet) for facet in TETRAHEDRON) + tuple(
        tuple(0 if vertex == 4 else vertex for vertex in facet)
        for facet in combinations((4, 5, 6, 7), 3)
    )
    original_edges, boundary = oriented_facet_data(pinched)
    require(not boundary, "pinched-sphere fixture is not closed")
    normalized, transported_edges, splits = normalize_closed_complex(pinched)
    require(splits == 1 and transported_edges == original_edges,
            "pinched-sphere normalization failed")
    controls["pinched_two_spheres"] = {
        "facets": len(pinched),
        "original_vertices": len({v for facet in pinched for v in facet}),
        "normalized_vertices": len({v for facet in normalized for v in facet}),
        "normalization_splits": splits,
        "signed_dual_preserved": True,
    }
    return controls


def run():
    minimum = minimum_nonorientable_surface_facets()
    require(minimum == (10, 6, 1), "surface lower bound mismatch")
    return {
        "status": "VERIFIED",
        "primary_exception_audit": audit_exceptions(),
        "boundary_parity_audit": audit_boundary_parity(),
        "normalization_and_control_audit": audit_controls(),
        "surface_numerical_boundary": {
            "minimum_facets": minimum[0],
            "vertices": minimum[1],
            "euler_characteristic": minimum[2],
        },
        "trust_boundary": (
            "finite exact corroboration only; primary-source transcription, "
            "universal normalization, orientability, and imported theorem "
            "alignment are audited in REVIEW.md"
        ),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--emit", action="store_true",
                        help="emit output without checking expected.json")
    arguments = parser.parse_args()
    result = run()
    encoded = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if not arguments.emit:
        expected = json.loads(Path(__file__).with_name("expected.json").read_text())
        require(json.loads(encoded) == expected, "expected output mismatch")
    print(encoded, end="")


if __name__ == "__main__":
    main()
