#!/usr/bin/env python3
"""Independent exact audit of the cap-auxiliary geometry.

No submitted module, certificate, or expected record is imported.  The
four-angle selector is checked by exhaustive rational vertex enumeration,
not by the submitted Farkas multipliers.  The icosahedral obstruction is
checked through the full cycle space of its face complex, not through the
submitted disk chain or row-space dual.  All arithmetic is integer or
Fraction arithmetic.
"""

import argparse
from fractions import Fraction as Q
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def add(*forms):
    return tuple(sum(values) for values in zip(*forms))


def scale(form, scalar):
    return tuple(scalar * value for value in form)


def evaluate(form, point):
    return form[0] + sum(c * x for c, x in zip(form[1:], point))


def matrix_rank(rows):
    if not rows:
        return 0
    work = [list(map(Q, row)) for row in rows]
    rank = 0
    for column in range(len(work[0])):
        pivot = next((i for i in range(rank, len(work)) if work[i][column]), None)
        if pivot is None:
            continue
        work[rank], work[pivot] = work[pivot], work[rank]
        value = work[rank][column]
        work[rank] = [x / value for x in work[rank]]
        for i in range(len(work)):
            if i != rank and work[i][column]:
                value = work[i][column]
                work[i] = [x - value * y for x, y in zip(work[i], work[rank])]
        rank += 1
    return rank


def solve_vertex(active_forms):
    """Solve five affine equalities in five variables, or return None."""
    matrix = [list(map(Q, form[1:])) + [Q(-form[0])] for form in active_forms]
    rank = 0
    for column in range(5):
        pivot = next((i for i in range(rank, 5) if matrix[i][column]), None)
        if pivot is None:
            continue
        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        value = matrix[rank][column]
        matrix[rank] = [x / value for x in matrix[rank]]
        for i in range(5):
            if i != rank and matrix[i][column]:
                value = matrix[i][column]
                matrix[i] = [x - value * y for x, y in zip(matrix[i], matrix[rank])]
        rank += 1
    if rank != 5:
        return None
    return tuple(matrix[i][5] for i in range(5))


def angle_polytope_audit():
    """Check every branch at every exact vertex of its bounded polytope."""
    one = (Q(1), 0, 0, 0, 0, 0)
    variables = tuple(tuple(Q(i == j) for i in range(6)) for j in range(1, 6))
    a, b, c, d, e = variables
    base = list(variables) + [add(one, scale(v, -1)) for v in variables]
    base += [add(one, scale(a, -1), scale(c, -1)),
             add(one, scale(b, -1), scale(d, -1)),
             add(scale(one, 2), scale(a, -1), scale(b, -1), scale(e, -1)),
             add(scale(one, 2), scale(c, -1), scale(d, -1), scale(e, -1))]
    branch_records = []
    total_vertices = 0
    active_systems = 0
    stream = sha256()
    for total_choice, first_choice in product((0, 1), repeat=2):
        totals = (e, add(a, b))
        total = totals[total_choice]
        firsts = (a, add(total, d, scale(one, -1)))
        first = firsts[first_choice]
        second = add(total, scale(first, -1))
        inequalities = base + [add(total, scale(totals[1 - total_choice], -1)),
                               add(first, scale(firsts[1 - first_choice], -1))]
        targets = [add(first, scale(a, -1)),
                   add(one, scale(c, -1), scale(first, -1)),
                   add(second, scale(b, -1)),
                   add(one, scale(d, -1), scale(second, -1)),
                   add(total, scale(e, -1)),
                   add(scale(one, 2), scale(e, -1), scale(total, -1))]
        vertices = set()
        for indices in combinations(range(len(inequalities)), 5):
            point = solve_vertex([inequalities[i] for i in indices])
            if point is None:
                continue
            active_systems += 1
            if all(evaluate(form, point) >= 0 for form in inequalities):
                vertices.add(point)
        require(vertices, "empty selector branch")
        minima = tuple(min(evaluate(target, point) for point in vertices)
                       for target in targets)
        require(all(value >= 0 for value in minima), "selector conclusion fails")
        total_vertices += len(vertices)
        record = {
            "branch": [total_choice, first_choice],
            "vertices": len(vertices),
            "target_minima": [str(value) for value in minima],
        }
        branch_records.append(record)
        for point in sorted(vertices):
            stream.update((f"{total_choice}:{first_choice}:"
                           + ",".join(map(str, point)) + "\n").encode())
    return branch_records, total_vertices, active_systems, stream.hexdigest()


# Z[phi], represented by a+b*phi and reduced with phi^2=phi+1.
def phi_mul(left, right):
    a, b = left
    c, d = right
    return a * c + b * d, a * d + b * c + b * d


def phi_dot(left, right):
    result = (0, 0)
    for x, y in zip(left, right):
        term = phi_mul(x, y)
        result = result[0] + term[0], result[1] + term[1]
    return result


def directed_edge_vector(a, b, edge_number):
    pair = tuple(sorted((a, b)))
    require(pair in edge_number, "triangle contains a nonedge")
    row = [0] * len(edge_number)
    row[edge_number[pair]] = 1 if a < b else -1
    return row


def icosahedral_cycle_space_audit():
    """Reconstruct the graph and prove that face boundaries span all cycles."""
    vertices = []
    for zero in range(3):
        for first, second in product((-1, 1), repeat=2):
            point = [[0, 0] for _ in range(3)]
            point[(zero + 1) % 3] = [first, 0]
            point[(zero + 2) % 3] = [0, second]
            vertices.append(tuple(tuple(x) for x in point))
    require(len(set(vertices)) == 12, "wrong icosahedral vertex count")
    require(all(phi_dot(v, v) == (2, 1) for v in vertices), "unequal norms")

    antipode = []
    for vertex in vertices:
        opposite = tuple((-a, -b) for a, b in vertex)
        matches = [i for i, candidate in enumerate(vertices) if candidate == opposite]
        require(len(matches) == 1, "antipode is not unique")
        antipode.append(matches[0])
    require(all(antipode[antipode[i]] == i and antipode[i] != i for i in range(12)),
            "antipodal map is not fixed-point-free")

    edges = [pair for pair in combinations(range(12), 2)
             if phi_dot(vertices[pair[0]], vertices[pair[1]]) == (0, 1)]
    require(len(edges) == 30, "wrong icosahedral edge count")
    edge_number = {edge: i for i, edge in enumerate(edges)}
    faces = [triple for triple in combinations(range(12), 3)
             if all(edge in edge_number for edge in combinations(triple, 2))]
    require(len(faces) == 20, "wrong icosahedral face count")
    require(all(tuple(sorted((antipode[a], antipode[b]))) in edge_number for a, b in edges),
            "antipode does not preserve edges")

    adjacency = {i: set() for i in range(12)}
    for a, b in edges:
        adjacency[a].add(b)
        adjacency[b].add(a)
    reached = {0}
    frontier = [0]
    while frontier:
        current = frontier.pop()
        for neighbor in adjacency[current] - reached:
            reached.add(neighbor)
            frontier.append(neighbor)
    require(len(reached) == 12 and all(len(adjacency[i]) == 5 for i in range(12)),
            "icosahedral graph connectivity or degree")

    face_rows = []
    edge_face_counts = [0] * len(edges)
    for a, b, c in faces:
        pieces = [directed_edge_vector(a, b, edge_number),
                  directed_edge_vector(b, c, edge_number),
                  directed_edge_vector(c, a, edge_number)]
        face_rows.append([sum(values) for values in zip(*pieces)])
        for edge in combinations((a, b, c), 2):
            edge_face_counts[edge_number[tuple(sorted(edge))]] += 1
    require(all(count == 2 for count in edge_face_counts), "not a closed triangulation")

    incidence = [[0] * len(edges) for _ in range(12)]
    for column, (a, b) in enumerate(edges):
        incidence[a][column] = -1
        incidence[b][column] = 1
    require(matrix_rank(incidence) == 11, "graph incidence rank")
    require(all(sum(incidence[v][e] * row[e] for e in range(len(edges))) == 0
                for row in face_rows for v in range(12)), "face is not a cycle")
    cycle_dimension = len(edges) - 12 + 1
    face_rank = matrix_rank(face_rows)
    require(cycle_dimension == face_rank == 19, "faces do not span the cycle space")
    require(12 - len(edges) + len(faces) == 2, "Euler characteristic")

    stream = sha256()
    for edge in edges:
        stream.update(f"E:{edge[0]}:{edge[1]}\n".encode())
    for face in faces:
        stream.update(f"F:{face[0]}:{face[1]}:{face[2]}\n".encode())
    return {
        "vertices": len(vertices),
        "edges": len(edges),
        "faces": len(faces),
        "antipodal_pairs": len(vertices) // 2,
        "graph_incidence_rank": 11,
        "cycle_space_dimension": cycle_dimension,
        "face_boundary_rank": face_rank,
        "euler_characteristic": 2,
        "complex_sha256": stream.hexdigest(),
    }


def motion_grid_audit():
    """Stress the exact cross-cap inequalities on a rational parameter grid."""
    checks = 0
    stream = sha256()
    values = tuple(Q(i, 8) for i in range(-8, 9))
    for a_num, b_num in product(range(1, 5), repeat=2):
        a, b = Q(a_num, 4), Q(b_num, 4)
        for normal_dot, auxiliary_dot in product(values, repeat=2):
            if auxiliary_dot > 1 + 2 * normal_dot:
                continue
            for ratio, excess in product((Q(1, 2), Q(1), Q(2)), (Q(1), Q(2))):
                h_i = a * ratio * excess
                h_j = b / ratio
                require(h_i * h_j >= a * b, "cap interval separation")
                energy = a * h_i + b * h_j + 2 * a * b * normal_dot
                delta = 2 * a * b * (normal_dot - auxiliary_dot)
                require(energy >= abs(delta), "motion energy domination")
                for lambda_num in range(9):
                    lam = Q(lambda_num, 8)
                    derivative_over_four = -energy + (1 - 2 * lam) * delta
                    require(derivative_over_four <= 0, "distance increased")
                    checks += 1
                    stream.update(
                        f"{a}:{b}:{normal_dot}:{auxiliary_dot}:{ratio}:{excess}:{lam}:"
                        f"{derivative_over_four}\n".encode()
                    )
    return checks, stream.hexdigest()


def rational_hemisphere_audit():
    """Check the projection construction on many exact rational sphere points."""
    points = {(Q(0), Q(0), Q(1))}
    for denominator in range(1, 9):
        for p, q in product(range(-denominator, denominator + 1), repeat=2):
            if p * p + q * q > denominator * denominator:
                continue
            u, v = Q(p, denominator), Q(q, denominator)
            scale_value = 1 + u * u + v * v
            point = (2 * u / scale_value, 2 * v / scale_value,
                     (1 - u * u - v * v) / scale_value)
            require(sum(x * x for x in point) == 1 and point[2] >= 0,
                    "rational hemisphere point")
            points.add(point)
    points = sorted(points)
    negative_pairs = 0
    for left, right in combinations(points, 2):
        normal_dot = sum(a * b for a, b in zip(left, right))
        if normal_dot >= 0:
            continue
        projected_dot = normal_dot - left[2] * right[2]
        projected_norm_product_squared = ((1 - left[2] ** 2) * (1 - right[2] ** 2))
        require(projected_dot < 0 and projected_norm_product_squared > 0,
                "negative pair projection signs")
        bound = 1 + 2 * normal_dot
        if bound < 0:
            require(projected_dot ** 2 >= bound ** 2 * projected_norm_product_squared,
                    "normalized projection inequality")
        negative_pairs += 1
    require(negative_pairs > 0, "hemisphere grid has no negative pair")
    return len(points), negative_pairs


def finite_controls():
    tetrahedron = ((1, 1, 1), (1, -1, -1), (-1, 1, -1), (-1, -1, 1))
    square = ((1, 0), (0, 1), (-1, 0), (0, -1))
    require(tuple(sum(v[i] for v in tetrahedron) for i in range(3)) == (0, 0, 0),
            "tetrahedron is not centered")
    gram = [[Q(sum(a * b for a, b in zip(x, y)), 3)
             for y in tetrahedron] for x in tetrahedron]
    require(matrix_rank(gram) == 3, "tetrahedral Gram rank")
    require(all(sum(square[i][k] * square[j][k] for k in range(2))
                <= 1 + 2 * gram[i][j] for i, j in combinations(range(4), 2)),
            "square auxiliary certificate")

    # Exact inequalities for disjoint icosahedral caps and their R4 control.
    require(5 * 31 ** 2 > 50 ** 2, "cap disjointness radical comparison")
    require(Q(19, 100) < Q(9, 20) ** 2, "cross-cap projection bound")
    require(Q(9, 2) - 1 >= 1 - (-1), "shallow-cap energy comparison")

    vertices = ((0, 0, 0), (-1, -1, 0), (-1, 0, 1), (0, -1, 1),
                (1, -2, 5), (-2, -5, -1), (-5, 1, 2), (-4, -10, 7))
    normals = ((1, 1, 1), (1, -1, -1), (-1, 1, -1), (1, -1, 0))
    offsets = (Q(0), Q(0), Q(0), Q(11, 2))
    witness = (1, 1, -1)
    require(tuple(sum(a * b for a, b in zip(normal, witness)) for normal in normals)
            == (1, 1, 1, 0), "fixture hemisphere witness")
    values = [[sum(a * b for a, b in zip(normal, vertex)) - offset
               for normal, offset in zip(normals, offsets)] for vertex in vertices]
    separators = ((0, 1, Q(2)), (1, 2, Q(2)), (2, 0, Q(2)),
                  (0, 3, Q(14)), (1, 3, Q(2)), (2, 3, Q(26)))
    require(all(row[i] + coefficient * row[j] <= 0
                for i, j, coefficient in separators for row in values),
            "fixture cap separator")
    labels = [tuple(i for i, value in enumerate(row) if value > 0) for row in values]
    require(all(len(label) <= 1 for label in labels), "fixture has overlapping cap")
    require({i for label in labels for i in label} == set(range(4)) and () in labels,
            "fixture does not activate every cap and the core")
    return {
        "tetrahedral_gram_rank": 3,
        "tetrahedral_square_certificate": "PASS",
        "shallow_cap_exact_controls": "PASS",
        "hemisphere_fixture_vertices": len(vertices),
        "hemisphere_fixture_separators": len(separators),
    }


def audit():
    branches, vertices, active_systems, angle_hash = angle_polytope_audit()
    topology = icosahedral_cycle_space_audit()
    motion_checks, motion_hash = motion_grid_audit()
    hemisphere_points, hemisphere_negative_pairs = rational_hemisphere_audit()
    return {
        "status": "INDEPENDENT_CAP_AUXILIARY_REVIEW_PASS",
        "imports_submitted_code_certificate_or_expected_output": False,
        "angle_selector_branches": branches,
        "angle_selector_total_vertices": vertices,
        "angle_selector_nonsingular_active_systems": active_systems,
        "angle_selector_vertex_stream_sha256": angle_hash,
        "icosahedral_topology": topology,
        "motion_rational_derivative_checks": motion_checks,
        "motion_stream_sha256": motion_hash,
        "hemisphere_rational_points": hemisphere_points,
        "hemisphere_negative_pair_checks": hemisphere_negative_pairs,
        "finite_controls": finite_controls(),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    result = audit()
    if args.check:
        expected = json.loads(Path(__file__).with_name("EXPECTED.json").read_text())
        require(result == expected, "result differs from EXPECTED.json")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
