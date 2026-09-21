#!/usr/bin/env python3
"""Independent exact audit of the vertex-inflation collapse criterion.

CPython 3.11+, standard library only.  This imports no target code, fixtures,
or expected output.  It uses frozenset faces, a global free-pair search, and a
separate mod-2 boundary calculation.  The program cannot decide whether an
arbitrary base complex is aspherical; that implication remains a human proof
obligation.
"""

from collections import Counter, defaultdict
from hashlib import sha256
from itertools import combinations, product
import argparse
import json
from pathlib import Path


def require(condition, message):
    if not condition:
        raise ValueError(message)


def downward_closure(facets):
    return {
        frozenset(face)
        for facet in facets
        for size in range(1, len(facet) + 1)
        for face in combinations(facet, size)
    }


def labelled_complexes(number_of_vertices):
    """All labelled complexes of dimension at most two on a fixed vertex set."""
    edges = tuple(combinations(range(number_of_vertices), 2))
    for edge_mask in range(1 << len(edges)):
        selected_edges = {
            frozenset(edge)
            for index, edge in enumerate(edges)
            if edge_mask & (1 << index)
        }
        supported_triangles = tuple(
            triangle
            for triangle in combinations(range(number_of_vertices), 3)
            if all(frozenset(edge) in selected_edges
                   for edge in combinations(triangle, 2))
        )
        one_skeleton = selected_edges | {
            frozenset((vertex,)) for vertex in range(number_of_vertices)
        }
        for triangle_mask in range(1 << len(supported_triangles)):
            yield one_skeleton | {
                frozenset(triangle)
                for index, triangle in enumerate(supported_triangles)
                if triangle_mask & (1 << index)
            }


def is_forest(vertices, edges):
    parent = {vertex: vertex for vertex in vertices}

    def representative(vertex):
        while parent[vertex] != vertex:
            parent[vertex] = parent[parent[vertex]]
            vertex = parent[vertex]
        return vertex

    for edge in edges:
        left, right = tuple(edge)
        left = representative(left)
        right = representative(right)
        if left == right:
            return False
        parent[left] = right
    return True


def local_conditions(complex_, multiplicities):
    duplicated = {
        vertex
        for vertex, multiplicity in enumerate(multiplicities)
        if multiplicity > 1
    }
    triangles = [face for face in complex_ if len(face) == 3]
    links_are_forests = True
    for apex in duplicated:
        link_edges = {
            face - {apex}
            for face in triangles
            if apex in face
        }
        link_vertices = {
            next(iter(face - {apex}))
            for face in complex_
            if len(face) == 2 and apex in face
        }
        links_are_forests &= is_forest(link_vertices, link_edges)
    thin_duplicated_edges = all(
        sum(edge <= triangle for triangle in triangles) <= 1
        for edge in complex_
        if len(edge) == 2 and edge <= duplicated
    )
    no_fully_duplicated_triangle = all(
        not triangle <= duplicated for triangle in triangles
    )
    return (
        bool(links_are_forests),
        bool(thin_duplicated_edges),
        bool(no_fully_duplicated_triangle),
    )


def graph_cycle_rank(vertices, edges):
    if not vertices:
        return 0
    adjacency = {vertex: set() for vertex in vertices}
    for edge in edges:
        left, right = tuple(edge)
        adjacency[left].add(right)
        adjacency[right].add(left)
    components = 0
    unseen = set(vertices)
    while unseen:
        components += 1
        frontier = {unseen.pop()}
        while frontier:
            point = frontier.pop()
            new_points = adjacency[point] & unseen
            unseen -= new_points
            frontier |= new_points
    return len(edges) - len(vertices) + components


def predicted_kernel_rank(complex_, multiplicities):
    """The local H2-kernel rank obtained from the classical wedge formula."""
    triangles = [face for face in complex_ if len(face) == 3]
    rank = 0
    for vertex, multiplicity in enumerate(multiplicities):
        link_edges = {face - {vertex} for face in triangles if vertex in face}
        link_vertices = {
            next(iter(face - {vertex}))
            for face in complex_
            if len(face) == 2 and vertex in face
        }
        rank += (multiplicity - 1) * graph_cycle_rank(link_vertices, link_edges)
    for edge in (face for face in complex_ if len(face) == 2):
        incident = sum(edge < triangle for triangle in triangles)
        factor = 1
        for vertex in edge:
            factor *= multiplicities[vertex] - 1
        rank += factor * max(incident - 1, 0)
    for triangle in triangles:
        factor = 1
        for vertex in triangle:
            factor *= multiplicities[vertex] - 1
        rank += factor
    return rank


def inflate(complex_, multiplicities):
    inflated = set()
    for face in complex_:
        originals = tuple(sorted(face))
        for colors in product(*(range(multiplicities[v]) for v in originals)):
            inflated.add(frozenset(zip(originals, colors)))
    return inflated


def original_copy(complex_):
    return {
        frozenset((vertex, 0) for vertex in face)
        for face in complex_
    }


def second_betti_mod_two(complex_):
    """Compute dim ker(partial_2) directly by sparse column elimination."""
    pivots = {}
    triangle_count = 0
    for triangle in sorted(
            (face for face in complex_ if len(face) == 3),
            key=lambda face: tuple(sorted(face))):
        triangle_count += 1
        column = frozenset(frozenset(edge) for edge in combinations(triangle, 2))
        while column:
            pivot = max(column, key=lambda face: tuple(sorted(face)))
            if pivot not in pivots:
                pivots[pivot] = column
                break
            column ^= pivots[pivot]
    return triangle_count - len(pivots)


def global_greedy_collapse(inflated, protected):
    """Find free pairs from all incidences; no copy-addition order is used."""
    remaining = set(inflated)
    schedule = []
    while True:
        new_triangles = {
            face for face in remaining if len(face) == 3 and face not in protected
        }
        if not new_triangles:
            break
        incidence = defaultdict(list)
        for triangle in (face for face in remaining if len(face) == 3):
            for edge in combinations(triangle, 2):
                incidence[frozenset(edge)].append(triangle)
        candidates = [
            (triangle, edge)
            for edge, cofaces in incidence.items()
            if edge not in protected and len(cofaces) == 1
            for triangle in cofaces
            if triangle in new_triangles
        ]
        require(candidates, "global free-pair search is stuck")
        triangle, edge = min(
            candidates,
            key=lambda pair: (tuple(sorted(pair[1])), tuple(sorted(pair[0]))),
        )
        remaining.remove(triangle)
        remaining.remove(edge)
        schedule.append((triangle, edge))
    require(protected <= remaining, "a protected face was removed")
    require(all(len(face) < 3 or face in protected for face in remaining),
            "a nonoriginal triangle remains")
    require(remaining == downward_closure(remaining), "collapse broke closure")
    return schedule


def replay_on_subcomplex(subcomplex, protected, schedule):
    remaining = set(subcomplex)
    for triangle, edge in schedule:
        if triangle not in remaining:
            continue
        require(edge in remaining, "top face present without scheduled edge")
        cofaces = {
            face for face in remaining
            if len(face) == 3 and edge < face
        }
        require(cofaces == {triangle}, "restricted edge is not free")
        require(edge not in protected and triangle not in protected,
                "restricted replay removed an original face")
        remaining.remove(triangle)
        remaining.remove(edge)
    require(all(len(face) < 3 or face in protected for face in remaining),
            "restricted replay left a nonoriginal triangle")
    require(remaining == downward_closure(remaining),
            "restricted replay broke closure")
    return remaining


def all_subcomplexes(complex_):
    faces = sorted(complex_, key=lambda face: (len(face), tuple(sorted(face))))

    def extend(position, selected):
        if position == len(faces):
            yield set(selected)
            return
        face = faces[position]
        yield from extend(position + 1, selected)
        codimension_one = {
            frozenset(subface) for subface in combinations(face, len(face) - 1)
        }
        if len(face) == 1 or codimension_one <= selected:
            selected.add(face)
            yield from extend(position + 1, selected)
            selected.remove(face)

    yield from extend(0, set())


def add_oriented(chain, vertices, coefficient):
    inversions = sum(
        vertices[i] > vertices[j]
        for i in range(len(vertices))
        for j in range(i + 1, len(vertices))
    )
    chain[tuple(sorted(vertices))] += coefficient * (-1 if inversions % 2 else 1)


def signed_join_of_pairs(pairs):
    chain = Counter()
    for choices in product((0, 1), repeat=3):
        add_oriented(
            chain,
            tuple(pairs[index][choice] for index, choice in enumerate(choices)),
            -1 if sum(choices) % 2 else 1,
        )
    return dict(chain)


def suspension_chain(apex_pair, cycle):
    chain = Counter()
    for left, right in zip(cycle, cycle[1:] + cycle[:1]):
        add_oriented(chain, (apex_pair[0], left, right), 1)
        add_oriented(chain, (apex_pair[1], left, right), -1)
    return dict(chain)


def audit_sphere(inflated, chain):
    require(chain and all(abs(value) == 1 for value in chain.values()),
            "sphere chain coefficients are not signed units")
    require(all(frozenset(face) in inflated for face in chain),
            "sphere contains a nonface")
    boundary = Counter()
    deflated = Counter()
    for triangle, coefficient in chain.items():
        for omitted in range(3):
            edge = triangle[:omitted] + triangle[omitted + 1:]
            boundary[edge] += (-1) ** omitted * coefficient
        originals = tuple(vertex for vertex, _ in triangle)
        add_oriented(deflated, originals, coefficient)
    require(all(value == 0 for value in boundary.values()),
            "sphere chain has nonzero boundary")
    require(all(value == 0 for value in deflated.values()),
            "sphere chain does not deflate to zero")

    support = downward_closure(frozenset(face) for face in chain)
    vertices = {face for face in support if len(face) == 1}
    edges = {face for face in support if len(face) == 2}
    triangles = {face for face in support if len(face) == 3}
    require(len(vertices) - len(edges) + len(triangles) == 2,
            "sphere support has wrong Euler characteristic")
    require(all(sum(edge < triangle for triangle in triangles) == 2
                for edge in edges), "sphere support has a nonmanifold edge")
    for singleton in vertices:
        vertex = next(iter(singleton))
        link_edges = {triangle - {vertex} for triangle in triangles if vertex in triangle}
        link_vertices = {
            next(iter(edge - {vertex})) for edge in edges if vertex in edge
        }
        degrees = Counter(point for edge in link_edges for point in edge)
        require(link_vertices and all(degrees[point] == 2 for point in link_vertices),
                "sphere support has a noncircular vertex link")
        adjacency = defaultdict(set)
        for edge in link_edges:
            left, right = tuple(edge)
            adjacency[left].add(right)
            adjacency[right].add(left)
        reached = {next(iter(link_vertices))}
        while True:
            expanded = reached | set().union(*(adjacency[p] for p in reached))
            if expanded == reached:
                break
            reached = expanded
        require(reached == link_vertices, "sphere vertex link is disconnected")
    return len(vertices), len(edges), len(triangles)


def criterion_enumeration():
    counts = Counter()
    digest = sha256()
    for number_of_vertices in range(1, 5):
        for complex_ in labelled_complexes(number_of_vertices):
            base_betti = second_betti_mod_two(complex_)
            for multiplicities in product((1, 2, 3), repeat=number_of_vertices):
                conditions = local_conditions(complex_, multiplicities)
                good = all(conditions)
                inflated = inflate(complex_, multiplicities)
                protected = original_copy(complex_)
                betti_jump = second_betti_mod_two(inflated) - base_betti
                require(betti_jump == predicted_kernel_rank(complex_, multiplicities),
                        "local quantitative kernel formula failed")
                require((betti_jump == 0) == good,
                        "criterion disagrees with the full boundary calculation")
                if good:
                    schedule = global_greedy_collapse(inflated, protected)
                    counts["admissible"] += 1
                    counts["greedy_pairs"] += len(schedule)
                    tag = "G"
                    witness = len(schedule)
                else:
                    require(betti_jump > 0, "failed condition lacks an H2 jump")
                    counts["obstructed"] += 1
                    counts["total_betti_jump"] += betti_jump
                    tag = "B"
                    witness = betti_jump
                counts["cases"] += 1
                counts["quantitative_formula_checks"] += 1
                digest.update(json.dumps([
                    number_of_vertices,
                    sorted(tuple(sorted(face)) for face in complex_),
                    multiplicities,
                    conditions,
                    tag,
                    witness,
                ], separators=(",", ":")).encode() + b"\n")
    return counts, digest.hexdigest()


def obstruction_and_boundary_controls():
    controls = []

    # A duplicated apex over a three-cycle; breaking one triangle gives a path.
    complex_ = downward_closure(((0, 1, 2), (0, 2, 3), (0, 3, 1)))
    multiplicities = (2, 1, 1, 1)
    require(local_conditions(complex_, multiplicities) == (False, True, True),
            "link-cycle control does not isolate condition 1")
    inflated = inflate(complex_, multiplicities)
    chain = suspension_chain(
        (((0, 0)), ((0, 1))),
        [((1, 0)), ((2, 0)), ((3, 0))],
    )
    controls.append(["link_cycle", list(audit_sphere(inflated, chain))])
    near = downward_closure(((0, 1, 2), (0, 2, 3)))
    require(all(local_conditions(near, multiplicities)), "link-path near miss rejected")
    global_greedy_collapse(inflate(near, multiplicities), original_copy(near))

    # Two triangles on one duplicated edge; duplicating only one endpoint is safe.
    complex_ = downward_closure(((0, 1, 2), (0, 1, 3)))
    multiplicities = (2, 2, 1, 1)
    require(local_conditions(complex_, multiplicities) == (True, False, True),
            "two-triangle control does not isolate condition 2")
    inflated = inflate(complex_, multiplicities)
    chain = signed_join_of_pairs((
        (((0, 0)), ((0, 1))),
        (((1, 0)), ((1, 1))),
        (((2, 0)), ((3, 0))),
    ))
    controls.append(["duplicated_edge", list(audit_sphere(inflated, chain))])
    near_multiplicities = (2, 1, 1, 1)
    require(all(local_conditions(complex_, near_multiplicities)),
            "single-endpoint near miss rejected")
    global_greedy_collapse(
        inflate(complex_, near_multiplicities), original_copy(complex_)
    )

    # A fully duplicated triangle; leaving exactly one vertex unduplicated is safe.
    complex_ = downward_closure(((0, 1, 2),))
    multiplicities = (2, 2, 2)
    require(local_conditions(complex_, multiplicities) == (True, True, False),
            "full-triangle control does not isolate condition 3")
    inflated = inflate(complex_, multiplicities)
    chain = signed_join_of_pairs(tuple(
        (((vertex, 0)), ((vertex, 1))) for vertex in range(3)
    ))
    controls.append(["duplicated_triangle", list(audit_sphere(inflated, chain))])
    near_multiplicities = (2, 2, 1)
    require(all(local_conditions(complex_, near_multiplicities)),
            "two-duplicated-vertices near miss rejected")
    global_greedy_collapse(
        inflate(complex_, near_multiplicities), original_copy(complex_)
    )
    return controls


def restriction_controls():
    fixtures = (
        (downward_closure(((0, 1, 2),)), (2, 2, 1)),
        (downward_closure(((0, 1, 2), (0, 1, 3))), (1, 1, 2, 2)),
    )
    counts = []
    digest = sha256()
    for complex_, multiplicities in fixtures:
        require(all(local_conditions(complex_, multiplicities)),
                "restriction fixture violates the criterion")
        inflated = inflate(complex_, multiplicities)
        protected = original_copy(complex_)
        schedule = global_greedy_collapse(inflated, protected)
        number = 0
        for subcomplex in all_subcomplexes(inflated):
            remainder = replay_on_subcomplex(subcomplex, protected, schedule)
            require(second_betti_mod_two(remainder)
                    == second_betti_mod_two(subcomplex),
                    "restricted elementary collapses changed H2")
            number += 1
            digest.update(json.dumps([
                sorted(tuple(sorted(face)) for face in subcomplex),
                sorted(tuple(sorted(face)) for face in remainder),
            ], separators=(",", ":")).encode() + b"\n")
        counts.append(number)
    return counts, digest.hexdigest()


def run():
    counts, criterion_digest = criterion_enumeration()
    obstruction_controls = obstruction_and_boundary_controls()
    restriction_counts, restriction_digest = restriction_controls()
    return {
        "status": "VERIFIED",
        "scope": "finite structural audit; base asphericity remains a human premise",
        "enumeration": "all labelled dim<=2 complexes on 1..4 vertices, m in {1,2,3}",
        "counts": dict(sorted(counts.items())),
        "criterion_digest": criterion_digest,
        "obstruction_sphere_f_vectors": obstruction_controls,
        "near_miss_controls": 3,
        "all_subcomplex_restriction_counts": restriction_counts,
        "restriction_digest": restriction_digest,
        "implementation": "global free-pair search; no target code or vertex-addition schedule",
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--emit", action="store_true",
                        help="print new output instead of checking expected.json")
    arguments = parser.parse_args()
    result = run()
    canonical = json.dumps(result, sort_keys=True, separators=(",", ":")).encode()
    result["evidence_sha256"] = sha256(canonical).hexdigest()
    if not arguments.emit:
        expected_path = Path(__file__).with_name("expected.json")
        require(result == json.loads(expected_path.read_text()),
                "result differs from expected.json")
    print(json.dumps(result, indent=2, sort_keys=True))
