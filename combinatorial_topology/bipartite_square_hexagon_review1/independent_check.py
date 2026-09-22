#!/usr/bin/env python3
"""Independent audit of hexagonal spheres in C4-free bipartite squares.

This checker exhausts the two labelled eight-vertex incidence rectangles
3-by-5 and 4-by-4, a frontier not covered by the producer's exhaustive run.
It represents faces as bit masks, validates both Morse matchings from their
transition digraphs, uses dense rational elimination for homology, and checks
the integral detector entry by entry.

Python 3.11+, standard library only.
"""

from __future__ import annotations

from collections import defaultdict, deque
from fractions import Fraction
import itertools
import json


def vertices(mask: int):
    while mask:
        bit = mask & -mask
        yield bit.bit_length() - 1
        mask ^= bit


def graph_from_rectangle(left: int, right: int, incidence: int):
    n = left + right
    adjacency = [0] * n
    edges = []
    for x in range(left):
        for j in range(right):
            if incidence & (1 << (x * right + j)):
                y = left + j
                adjacency[x] |= 1 << y
                adjacency[y] |= 1 << x
                edges.append((x, y))
    return tuple(adjacency), tuple(edges)


def connected(adjacency) -> bool:
    if not adjacency:
        return False
    reached = 1
    frontier = 1
    while frontier:
        new = 0
        for v in vertices(frontier):
            new |= adjacency[v]
        new &= ~reached
        reached |= new
        frontier = new
    return reached == (1 << len(adjacency)) - 1


def c4_free(adjacency, left: int) -> bool:
    return all(
        (adjacency[u] & adjacency[v]).bit_count() <= 1
        for u, v in itertools.combinations(range(left), 2)
    )


def square(adjacency):
    result = []
    for v, neighbors in enumerate(adjacency):
        mask = neighbors
        for w in vertices(neighbors):
            mask |= adjacency[w]
        result.append(mask & ~(1 << v))
    return tuple(result)


def clique_faces(adjacency):
    n = len(adjacency)
    faces = set()
    for mask in range(1, 1 << n):
        if all((mask & ~(1 << v)) & ~adjacency[v] == 0 for v in vertices(mask)):
            faces.add(mask)
    return faces


def bridge_faces(adjacency):
    faces = set()
    for v, neighbors in enumerate(adjacency):
        star = neighbors | (1 << v)
        sub = star
        while sub:
            faces.add(sub)
            sub = (sub - 1) & star
    return faces


def graph_faces(adjacency):
    faces = {1 << v for v in range(len(adjacency))}
    faces.update((1 << u) | (1 << v) for u in range(len(adjacency)) for v in vertices(adjacency[u]) if u < v)
    return faces


def audit_bridge_collapse(adjacency, bridge):
    remaining = set(bridge)
    pairs = []
    for center, neighbors in enumerate(adjacency):
        sub = neighbors
        while sub:
            if sub.bit_count() >= 2:
                pairs.append((sub, sub | (1 << center)))
            sub = (sub - 1) & neighbors
    pairs.sort(key=lambda pair: (-pair[0].bit_count(), pair[0], pair[1]))
    for lower, upper in pairs:
        if lower not in remaining or upper not in remaining:
            raise AssertionError("collapse pair missing")
        cofaces = {face for face in remaining if face != lower and face & lower == lower}
        if cofaces != {upper}:
            raise AssertionError("proposed bridge face is not free")
        remaining.remove(lower)
        remaining.remove(upper)
    if remaining != graph_faces(adjacency):
        raise AssertionError("bridge collapse has wrong endpoint")
    return len(pairs)


def common_neighbors(adjacency, mask: int) -> int:
    answer = (1 << len(adjacency)) - 1
    for v in vertices(mask):
        answer &= adjacency[v]
    return answer


def audit_dowker_matching(faces, adjacency, chosen_part: int):
    """Match faces toward the pure chosen part and detect every V-cycle."""
    n = len(adjacency)
    chosen_mask = chosen_part
    other_mask = ((1 << n) - 1) ^ chosen_mask
    lower_to_upper = {}
    uppers = set()
    for face in faces:
        other = face & other_mask
        if not other:
            continue
        candidates = common_neighbors(adjacency, other) & chosen_mask
        if not candidates:
            raise AssertionError("bridge face lost its common neighbor")
        pivot = (candidates & -candidates).bit_length() - 1
        if not (face & (1 << pivot)):
            upper = face | (1 << pivot)
            if upper not in faces or upper in uppers:
                raise AssertionError("invalid Dowker matching")
            lower_to_upper[face] = upper
            uppers.add(upper)
    critical = faces - set(lower_to_upper) - uppers
    expected = {face for face in faces if face & ~chosen_mask == 0}
    if critical != expected:
        raise AssertionError("wrong Dowker critical complex")

    transitions = {lower: set() for lower in lower_to_upper}
    for lower, upper in lower_to_upper.items():
        for v in vertices(upper):
            candidate = upper ^ (1 << v)
            if candidate != lower and candidate in lower_to_upper:
                transitions[lower].add(candidate)
    state = {}

    def visit(node):
        state[node] = 1
        for nxt in transitions[node]:
            if state.get(nxt) == 1:
                raise AssertionError("cyclic Dowker matching")
            if not state.get(nxt):
                visit(nxt)
        state[node] = 2

    for node in transitions:
        if not state.get(node):
            visit(node)
    return len(lower_to_upper)


def canonical_cycle(cycle):
    cycle = tuple(cycle)
    choices = []
    for direction in (cycle, cycle[::-1]):
        for i in range(6):
            choices.append(direction[i:] + direction[:i])
    return min(choices)


def six_cycles(adjacency):
    found = set()
    n = len(adjacency)

    def extend(path):
        if len(path) == 6:
            if adjacency[path[-1]] & (1 << path[0]):
                found.add(canonical_cycle(path))
            return
        for nxt in vertices(adjacency[path[-1]]):
            if nxt not in path:
                extend(path + (nxt,))

    for start in range(n):
        extend((start,))
    return sorted(found)


def edge_vector(path, edge_index):
    vector = [0] * len(edge_index)
    for u, v in zip(path, path[1:]):
        edge = (min(u, v), max(u, v))
        vector[edge_index[edge]] += 1 if u < v else -1
    return tuple(vector)


def cycle_vector(cycle, edge_index):
    return edge_vector(cycle + (cycle[0],), edge_index)


def two_step_path(u, v, adjacency):
    common = adjacency[u] & adjacency[v]
    if common.bit_count() != 1:
        raise AssertionError("same-part square edge lacks a unique center")
    center = (common & -common).bit_length() - 1
    return (u, center, v)


def add_vectors(*terms):
    if not terms:
        return ()
    return tuple(sum(values) for values in zip(*terms, strict=True))


def scale(vector, coefficient):
    return tuple(coefficient * x for x in vector)


def detector(face: int, left_mask: int, adjacency, edge_index):
    verts = tuple(vertices(face))
    if len(verts) != 3 or face & ~left_mask:
        return (0,) * len(edge_index)
    a, b, c = verts
    return add_vectors(
        edge_vector(two_step_path(a, b, adjacency), edge_index),
        edge_vector(two_step_path(b, c, adjacency), edge_index),
        edge_vector(two_step_path(c, a, adjacency), edge_index),
    )


def boundary(face: int):
    verts = tuple(vertices(face))
    for i, v in enumerate(verts):
        yield face ^ (1 << v), -1 if i % 2 else 1


def sphere_coefficients(facets, pure_left):
    edge_to_facets = defaultdict(list)
    for facet in facets:
        for edge, sign in boundary(facet):
            edge_to_facets[edge].append((facet, sign))
    if any(len(rows) != 2 for rows in edge_to_facets.values()):
        raise AssertionError("candidate octahedron is not a closed surface")
    coefficients = {pure_left: 1}
    queue = deque([pure_left])
    while queue:
        facet = queue.popleft()
        for edge, sign in boundary(facet):
            rows = edge_to_facets[edge]
            other, other_sign = rows[0] if rows[1][0] == facet else rows[1]
            wanted = -coefficients[facet] * sign * other_sign
            if other in coefficients and coefficients[other] != wanted:
                raise AssertionError("inconsistent sphere orientation")
            if other not in coefficients:
                coefficients[other] = wanted
                queue.append(other)
    if set(coefficients) != set(facets) or set(coefficients.values()) - {-1, 1}:
        raise AssertionError("incomplete sphere orientation")
    total = defaultdict(int)
    for facet, coefficient in coefficients.items():
        for edge, sign in boundary(facet):
            total[edge] += coefficient * sign
    if any(total.values()):
        raise AssertionError("oriented octahedron is not an integral cycle")
    return coefficients


def dense_rank(matrix):
    if not matrix:
        return 0
    work = [[Fraction(x) for x in row] for row in matrix]
    rows = len(work)
    cols = len(work[0]) if rows else 0
    pivot_row = 0
    for col in range(cols):
        pivot = next((r for r in range(pivot_row, rows) if work[r][col]), None)
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        value = work[pivot_row][col]
        work[pivot_row] = [x / value for x in work[pivot_row]]
        for r in range(rows):
            if r == pivot_row or not work[r][col]:
                continue
            value = work[r][col]
            work[r] = [x - value * y for x, y in zip(work[r], work[pivot_row], strict=True)]
        pivot_row += 1
        if pivot_row == rows:
            break
    return pivot_row


def vector_rank(vectors):
    if not vectors:
        return 0
    return dense_rank([list(row) for row in zip(*vectors, strict=True)])


def betti_numbers(faces):
    max_size = max((face.bit_count() for face in faces), default=0)
    levels = {size: sorted(face for face in faces if face.bit_count() == size) for size in range(1, max_size + 1)}
    ranks = {size: 0 for size in range(1, max_size + 2)}
    for size in range(2, max_size + 1):
        row_index = {face: i for i, face in enumerate(levels[size - 1])}
        matrix = [[0] * len(levels[size]) for _ in levels[size - 1]]
        for j, face in enumerate(levels[size]):
            for lower, sign in boundary(face):
                matrix[row_index[lower]][j] = sign
        ranks[size] = dense_rank(matrix)
    return [
        len(levels.get(size, ())) - ranks.get(size, 0) - ranks.get(size + 1, 0)
        for size in range(1, max_size + 1)
    ]


def pad(values, length):
    return values + [0] * (length - len(values))


def audit_graph(adjacency, edges, left):
    n = len(adjacency)
    left_mask = (1 << left) - 1
    right_mask = ((1 << n) - 1) ^ left_mask
    squared = square(adjacency)
    faces = clique_faces(squared)
    bridge = bridge_faces(adjacency)
    if not bridge <= faces:
        raise AssertionError("star bridge is not a subcomplex")
    bridge_pairs = audit_bridge_collapse(adjacency, bridge)
    dowker_x = audit_dowker_matching(bridge, adjacency, left_mask)
    dowker_y = audit_dowker_matching(bridge, adjacency, right_mask)

    edge_index = {edge: i for i, edge in enumerate(edges)}
    cycles = six_cycles(adjacency)
    cycle_vectors = [cycle_vector(cycle, edge_index) for cycle in cycles]
    cycle_vector_set = set(cycle_vectors) | {scale(vector, -1) for vector in cycle_vectors}
    phi = {face: detector(face, left_mask, adjacency, edge_index) for face in faces if face.bit_count() == 3}
    for face, image in phi.items():
        if any(image) and image not in cycle_vector_set:
            raise AssertionError("pure triangle does not expand to a six-cycle")
    for tetrahedron in (face for face in faces if face.bit_count() == 4):
        image = add_vectors(*(scale(phi[triangle], sign) for triangle, sign in boundary(tetrahedron)))
        if any(image):
            raise AssertionError("detector does not annihilate a tetrahedron boundary")

    sphere_count = 0
    for cycle, expected in zip(cycles, cycle_vectors, strict=True):
        support = sum(1 << v for v in cycle)
        induced = {face for face in faces if face & ~support == 0}
        counts = tuple(sum(face.bit_count() == size for face in induced) for size in (1, 2, 3, 4))
        if counts != (6, 12, 8, 0):
            raise AssertionError("six-cycle does not induce an octahedral boundary")
        facets = [face for face in induced if face.bit_count() == 3]
        pure_left = next(face for face in facets if face & ~left_mask == 0)
        coefficients = sphere_coefficients(facets, pure_left)
        image = add_vectors(*(scale(phi[face], coefficient) for face, coefficient in coefficients.items()))
        if image != expected and image != scale(expected, -1):
            raise AssertionError("integral sphere detector has wrong image")
        sphere_count += 1

    if not cycles and faces != bridge:
        raise AssertionError("hexagon-free square contains a face outside the bridge")

    half_x = {face for face in faces if face & ~left_mask == 0}
    half_y = {face for face in faces if face & ~right_mask == 0}
    b = betti_numbers(faces)
    bx = betti_numbers(half_x)
    by = betti_numbers(half_y)
    length = max(len(b), len(bx), len(by), 4)
    b, bx, by = pad(b, length), pad(bx, length), pad(by, length)
    lattice_rank = vector_rank(cycle_vectors)
    graph_cycle_rank = len(edges) - n + 1
    if b[1] != graph_cycle_rank - lattice_rank:
        raise AssertionError("wrong rational H1 quotient")
    if b[2] != bx[2] + by[2] + lattice_rank:
        raise AssertionError("wrong rational H2 exact-sequence rank")
    if any(b[j] != bx[j] + by[j] for j in range(3, length)):
        raise AssertionError("wrong higher rational homology split")
    return {
        "hexagons": len(cycles),
        "hexagon_lattice_rank": lattice_rank,
        "sphere_checks": sphere_count,
        "bridge_pairs": bridge_pairs,
        "dowker_pairs": dowker_x + dowker_y,
    }


def run_rectangle(left, right):
    possible = left * right
    accepted = 0
    totals = defaultdict(int)
    for incidence in range(1 << possible):
        adjacency, edges = graph_from_rectangle(left, right, incidence)
        if not connected(adjacency) or not c4_free(adjacency, left):
            continue
        row = audit_graph(adjacency, edges, left)
        accepted += 1
        for key, value in row.items():
            totals[key] += value
    return {"labelled_graphs": accepted, **dict(sorted(totals.items()))}


def fixture_subdivision_complete(order):
    base_edges = list(itertools.combinations(range(order), 2))
    n = order + len(base_edges)
    edges = []
    for j, (u, v) in enumerate(base_edges):
        center = order + j
        edges.extend(((u, center), (v, center)))
    adjacency = [0] * n
    for u, v in edges:
        adjacency[u] |= 1 << v
        adjacency[v] |= 1 << u
    return tuple(adjacency), tuple(sorted(edges)), order


def fixture_from_edges(n, edges):
    adjacency = [0] * n
    for u, v in edges:
        adjacency[u] |= 1 << v
        adjacency[v] |= 1 << u
    return tuple(adjacency), tuple(sorted(edges))


def basic_fixtures():
    examples = {
        "P4_no_hexagon": (
            4,
            ((0, 2), (1, 2), (1, 3)),
            2,
        ),
        "C6_one_sphere": (
            6,
            ((0, 3), (1, 3), (1, 4), (2, 4), (2, 5), (0, 5)),
            3,
        ),
        "C8_no_hexagon": (
            8,
            ((0, 4), (1, 4), (1, 5), (2, 5), (2, 6), (3, 6), (3, 7), (0, 7)),
            4,
        ),
    }
    result = {}
    for name, (n, edges, left) in examples.items():
        adjacency, canonical_edges = fixture_from_edges(n, edges)
        result[name] = audit_graph(adjacency, canonical_edges, left)
    return result


def c4_boundary_fixture():
    # The old C6 is retained, but adding vertex 6 adjacent to its three
    # left vertices makes 6 universal in the square.  The full clique
    # complex is therefore a cone, exactly where the detector's unique
    # two-step-path premise fails.
    edges = (
        (0, 3), (1, 3), (1, 4), (2, 4), (2, 5), (0, 5),
        (0, 6), (1, 6), (2, 6),
    )
    adjacency, _ = fixture_from_edges(7, edges)
    squared = square(adjacency)
    faces = clique_faces(squared)
    old_support = (1 << 6) - 1
    old_induced = {face for face in faces if face & ~old_support == 0}
    return {
        "contains_four_cycle": not c4_free(adjacency, 3),
        "old_C6_induced_f_vector": [
            sum(face.bit_count() == size for face in old_induced)
            for size in (1, 2, 3)
        ],
        "universal_square_vertices": [
            v for v, neighbors in enumerate(squared)
            if neighbors.bit_count() == 6
        ],
    }


def main():
    rectangles = {
        "3x5": run_rectangle(3, 5),
        "4x4": run_rectangle(4, 4),
    }
    k4_adjacency, k4_edges, k4_left = fixture_subdivision_complete(4)
    k4 = audit_graph(k4_adjacency, k4_edges, k4_left)
    result = {
        "adversarial_smallest_fixtures": basic_fixtures(),
        "complete_labelled_eight_vertex_rectangles": rectangles,
        "four_cycle_boundary_cone": c4_boundary_fixture(),
        "subdivision_K4_dependency_fixture": k4,
        "exact_arithmetic": "integer chains and Fraction Gaussian elimination",
        "trust_boundary": (
            "finite adversarial audit only; universal collapse, Mayer-Vietoris, "
            "fundamental-group, and asphericity claims rest on the written proof"
        ),
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
