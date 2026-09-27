#!/usr/bin/env python3
"""Independent exact audit of the rational indecomposable input frontier."""

import argparse
from fractions import Fraction as F
from hashlib import sha256
from itertools import combinations
import json
from math import comb, isqrt
from pathlib import Path


HERE = Path(__file__).resolve().parent


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def pins():
    manifest = json.loads((HERE / "TARGET_INPUTS.json").read_text())
    require(manifest["schema"] == 1, "manifest schema")
    for relative, expected in manifest["files"].items():
        actual = sha256((HERE / relative).read_bytes()).hexdigest()
        require(actual == expected, f"changed target or dependency: {relative}")
    return manifest


def ceiling(q):
    return (q.numerator + q.denominator - 1) // q.denominator


def clog(integer):
    require(isinstance(integer, int) and not isinstance(integer, bool) and integer > 0,
            "positive integer required")
    return (integer - 1).bit_length()


def fraction_clog(q):
    require(q >= 1, "fractional logarithm domain")
    guess = max(0, q.numerator.bit_length() - q.denominator.bit_length())
    while F(1 << guess) < q:
        guess += 1
    while guess and F(1 << (guess - 1)) >= q:
        guess -= 1
    return guess


def height(q):
    q = F(q)
    return clog(max(abs(q.numerator), q.denominator))


def sub(first, second):
    return tuple(x - y for x, y in zip(first, second))


def dot(first, second):
    return sum((x * y for x, y in zip(first, second)), F(0))


def cross(first, second):
    return (first[1] * second[2] - first[2] * second[1],
            first[2] * second[0] - first[0] * second[2],
            first[0] * second[1] - first[1] * second[0])


def determinant(columns):
    return dot(columns[0], cross(columns[1], columns[2]))


def dist2(first, second):
    difference = sub(first, second)
    return dot(difference, difference)


def matrix_multiply(first, second):
    return tuple(tuple(sum(first[i][k] * second[k][j]
                           for k in range(len(second)))
                       for j in range(len(second[0])))
                 for i in range(len(first)))


def matrix_vector(matrix, vector):
    return tuple(dot(row, vector) for row in matrix)


def transpose(matrix):
    return tuple(zip(*matrix))


def identity(size):
    return tuple(tuple(F(i == j) for j in range(size)) for i in range(size))


def rotation(quaternion):
    """Rational orthogonal matrix from an integral quaternion."""
    a, b, c, d = map(F, quaternion)
    norm = a*a + b*b + c*c + d*d
    matrix = (
        (a*a+b*b-c*c-d*d, 2*(b*c-a*d), 2*(b*d+a*c)),
        (2*(b*c+a*d), a*a-b*b+c*c-d*d, 2*(c*d-a*b)),
        (2*(b*d-a*c), 2*(c*d+a*b), a*a-b*b-c*c+d*d),
    )
    result = tuple(tuple(entry / norm for entry in row) for row in matrix)
    require(matrix_multiply(transpose(result), result) == identity(3),
            "quaternion matrix is not orthogonal")
    return result


def affine_reflection(plane):
    normal, constant = plane[:3], plane[3]
    norm = dot(normal, normal)
    require(norm > 0, "zero reflection plane")
    return tuple(
        tuple(F(i == j) - 2 * normal[i] * normal[j] / norm for j in range(3))
        + (-2 * constant * normal[i] / norm,)
        for i in range(3)
    ) + ((F(0), F(0), F(0), F(1)),)


def plane_value(plane, point):
    return dot(plane[:3], point) + plane[3]


def concrete_repair_controls():
    scenarios = (
        ((1, 2, 3, 4), (F(1, 7), F(-2, 11), F(3, 13)),
         (F(2, 17), F(-3, 19), F(5, 23)),
         (F(-1, 5), F(2, 7), F(4, 9))),
        ((2, -1, 4, 3), (F(-2, 5), F(1, 13), F(7, 17)),
         (F(-3, 11), F(5, 29), F(2, 31)),
         (F(3, 8), F(-4, 15), F(1, 6))),
        ((3, 5, -2, 1), (F(4, 19), F(-5, 23), F(6, 31)),
         (F(1, 37), F(2, 41), F(-3, 43)),
         (F(-2, 9), F(5, 12), F(7, 20))),
    )
    facets = (
        (F(1), F(0), F(0), F(1)), (F(-1), F(0), F(0), F(1)),
        (F(0), F(1), F(0), F(1)), (F(0), F(-1), F(0), F(1)),
        (F(0), F(0), F(1), F(1)), (F(0), F(0), F(-1), F(1)),
    )
    stream = sha256()
    records = []
    for quaternion, shift, apex, image in scenarios:
        linear = rotation(quaternion)
        preimage = matrix_vector(transpose(linear), sub(image, shift))
        normal = sub(preimage, apex)
        require(dot(normal, normal) > 0, "vacuous repair scenario")
        constant = dot(preimage, preimage) - dot(apex, apex)
        bisector = tuple(2 * value for value in normal) + (-constant,)
        reflection = affine_reflection(bisector)
        affine = tuple(row + (translation,) for row, translation in zip(linear, shift)) \
            + ((F(0), F(0), F(0), F(1)),)
        repaired = matrix_multiply(affine, reflection)
        require(matrix_vector(repaired, apex + (F(1),))[:3] == image,
                "repair misses prescribed image")
        require(matrix_multiply(reflection, reflection) == identity(4),
                "repair reflection is not involutive")
        require(plane_value(bisector, apex) == -dot(normal, normal),
                "bisector sign identity")
        side_planes = []
        for facet in facets:
            side = tuple(plane_value(facet, apex) * h
                         - plane_value(bisector, apex) * f
                         for h, f in zip(bisector, facet))
            require(plane_value(side, apex) == 0, "cone side misses apex")
            side_planes.append(side)
        inputs = tuple(value for row in linear for value in row) + shift + apex + image
        input_height = max(1, max(map(height, inputs)))
        repaired_height = max(map(height, (value for row in repaired for value in row)))
        side_height = max(map(height, (value for plane in side_planes for value in plane)))
        require(repaired_height <= 1024 * input_height, "repaired-map height")
        require(side_height <= 1024 * input_height, "side-plane height")
        line = f"{quaternion}:{bisector}:{repaired}:{side_planes}\n".encode()
        stream.update(line)
        records.append({
            "input_height": input_height,
            "repaired_map_height": repaired_height,
            "maximum_side_height": side_height,
        })
    return {"scenarios": records, "stream_sha256": stream.hexdigest()}


def height_factor_controls():
    """Re-derive coefficient factors from the scalar height rules."""
    add = lambda first, second: first + second + 1
    multiply = lambda first, second: first + second
    divide = multiply
    sum_many = lambda values: sum(values) + len(values) - 1
    scale_two = lambda value: value + 1

    difference = add(1, 1)
    preimage = sum_many([multiply(1, difference)] * 3)
    normal = add(preimage, 1)
    preimage_norm = sum_many([multiply(preimage, preimage)] * 3)
    apex_norm = sum_many([multiply(1, 1)] * 3)
    constant = add(preimage_norm, apex_norm)
    normal_norm = sum_many([multiply(normal, normal)] * 3)
    bisector_normal = scale_two(normal)
    linear_reflection = add(0, divide(scale_two(multiply(normal, normal)), normal_norm))
    translation_reflection = divide(multiply(constant, normal), normal_norm)
    repaired_linear = sum_many([multiply(1, linear_reflection)] * 3)
    repaired_translation = add(
        sum_many([multiply(1, translation_reflection)] * 3), 1)
    facet_at_apex = add(sum_many([multiply(1, 1)] * 3), 1)
    bisector_at_apex = add(
        sum_many([multiply(bisector_normal, 1)] * 3), constant)
    side = add(multiply(facet_at_apex, max(bisector_normal, constant)),
               multiply(bisector_at_apex, 1))

    derived = {
        "difference": difference,
        "preimage": preimage,
        "normal": normal,
        "constant": constant,
        "normal_norm": normal_norm,
        "bisector": max(bisector_normal, constant),
        "reflection": max(linear_reflection, translation_reflection),
        "repaired_map": max(repaired_linear, repaired_translation),
        "cone_side": side,
    }
    advertised = {
        "difference": 3,
        "preimage": 14,
        "normal": 16,
        "constant": 95,
        "normal_norm": 98,
        "bisector": 128,
        "reflection": 256,
        "repaired_map": 1024,
        "cone_side": 1024,
    }
    require(all(derived[key] <= advertised[key] for key in advertised),
            "repair height factor not covered")

    # Three-point plane: differences cost 3, cross-product coordinates 13,
    # and the constant term 44.  Six determinant terms cost 18A+5.
    point_plane = max(13, sum_many([multiply(13, 1)] * 3))
    cramer_determinant_at_a_one = sum_many([3] * 6)
    cramer_coordinate_at_a_one = divide(cramer_determinant_at_a_one,
                                        cramer_determinant_at_a_one)
    generic_reflection_at_p_one = max(
        add(0, divide(scale_two(multiply(1, 1)), sum_many([2] * 3))),
        divide(scale_two(multiply(1, 1)), sum_many([2] * 3)),
    )
    require(point_plane == 44 <= 64, "three-point plane factor")
    require(cramer_determinant_at_a_one == 23, "determinant factor")
    require(cramer_coordinate_at_a_one == 46 <= 64, "Cramer factor")
    require(generic_reflection_at_p_one == 12, "face reflection factor")
    return {
        "repair_factors": derived,
        "three_point_plane_factor": point_plane,
        "cramer_determinant_factor_at_A_1": cramer_determinant_at_a_one,
        "cramer_coordinate_factor_at_A_1": cramer_coordinate_at_a_one,
        "face_reflection_factor_at_P_1": generic_reflection_at_p_one,
    }


def solve_columns(columns, target):
    """Exact Gauss-Jordan solution; columns form a nonsingular 3-by-3 matrix."""
    matrix = [[F(columns[column][row]) for column in range(3)] + [F(target[row])]
              for row in range(3)]
    for column in range(3):
        pivot = next((row for row in range(column, 3) if matrix[row][column]), None)
        require(pivot is not None, "singular affine frame")
        matrix[column], matrix[pivot] = matrix[pivot], matrix[column]
        value = matrix[column][column]
        matrix[column] = [entry / value for entry in matrix[column]]
        for row in range(3):
            if row != column and matrix[row][column]:
                value = matrix[row][column]
                matrix[row] = [entry - value * base
                               for entry, base in zip(matrix[row], matrix[column])]
    return tuple(matrix[row][3] for row in range(3))


def affine_transport(point, reference_tetrahedron, placed_tetrahedron):
    source_columns = tuple(sub(reference_tetrahedron[index], reference_tetrahedron[0])
                           for index in range(1, 4))
    coefficients = solve_columns(source_columns, sub(point, reference_tetrahedron[0]))
    target_columns = tuple(sub(placed_tetrahedron[index], placed_tetrahedron[0])
                           for index in range(1, 4))
    return tuple(placed_tetrahedron[0][coordinate]
                 + sum(coefficients[index] * target_columns[index][coordinate]
                       for index in range(3))
                 for coordinate in range(3))


def reflect_point(point, face):
    normal = cross(sub(face[1], face[0]), sub(face[2], face[0]))
    norm = dot(normal, normal)
    require(norm > 0, "degenerate reflection face")
    scale = 2 * dot(sub(point, face[0]), normal) / norm
    return tuple(value - scale * normal[index] for index, value in enumerate(point))


def distance_vector(points):
    return tuple(dist2(points[first], points[second])
                 for first, second in combinations(range(len(points)), 2))


def below(first, second):
    return all(x <= y for x, y in zip(first, second))


def framework_fixture(include_cycle):
    source = tuple(tuple(map(F, point)) for point in (
        (0, 0, 0), (2, 0, 0), (0, 3, 0), (0, 0, 5),
        (2, 3, 5), (-1, 4, 6), (3, -2, 7), (4, 5, -3),
    ))
    chain_cells = (
        (0, 1, 2, 3), (1, 2, 3, 4), (2, 3, 4, 5),
        (3, 4, 5, 6), (4, 5, 6, 7),
    )
    cycle_cell = (2, 4, 5, 7)
    cells = chain_cells + ((cycle_cell,) if include_cycle else ())
    for cell in cells:
        base = source[cell[0]]
        require(determinant(tuple(sub(source[index], base) for index in cell[1:])) != 0,
                "degenerate source tetrahedron")
    steps = (
        (chain_cells[0], chain_cells[1], (1, 2, 3), 0, 4),
        (chain_cells[1], chain_cells[2], (2, 3, 4), 1, 5),
        (chain_cells[2], chain_cells[3], (3, 4, 5), 2, 6),
        (chain_cells[3], chain_cells[4], (4, 5, 6), 3, 7),
    )
    partials = [{index: source[index] for index in chain_cells[0]}]
    pair_values = []
    for parent, child, face, opposite, new in steps:
        reference_parent = tuple(source[index] for index in parent)
        reflected_reference = reflect_point(source[new], tuple(source[index] for index in face))
        low, high = sorted((dist2(source[opposite], source[new]),
                            dist2(source[opposite], reflected_reference)))
        require(low < high, "collapsed binary distance")
        pair_values.append((opposite, new, low, high))
        next_partials = []
        for placed in partials:
            placed_parent = tuple(placed[index] for index in parent)
            continued = affine_transport(source[new], reference_parent, placed_parent)
            folded = reflect_point(continued, tuple(placed[index] for index in face))
            require(continued != folded, "child cell became degenerate")
            for candidate in (continued, folded):
                extended = dict(placed)
                extended[new] = candidate
                next_partials.append(extended)
        partials = next_partials

    mesh_edges = {tuple(sorted(edge)) for cell in cells for edge in combinations(cell, 2)}
    states = []
    for placed in partials:
        points = tuple(placed[index] for index in range(len(source)))
        if not all(dist2(points[first], points[second])
                   == dist2(source[first], source[second])
                   for first, second in mesh_edges):
            continue
        bits = []
        for first, second, low, high in pair_values:
            bit = (dist2(points[first], points[second]) - low) / (high - low)
            require(bit in (0, 1), "nonbinary selected distance")
            bits.append(int(bit))
        states.append((tuple(bits), distance_vector(points)))
    require(states and len(states) == len(set(states)), "duplicate or empty state set")
    require(len({bits for bits, _ in states}) == len(states), "encoding not injective")

    comparable = 0
    maximum_interval = maximum_height = maximum_rank = 0
    for lower_bits, lower_distance in states:
        for upper_bits, upper_distance in states:
            if not below(lower_distance, upper_distance):
                continue
            comparable += 1
            require(below(lower_bits, upper_bits), "selected bits are not monotone")
            rank = sum(upper_bits) - sum(lower_bits)
            interval = [(bits, distance) for bits, distance in states
                        if below(lower_distance, distance) and below(distance, upper_distance)]
            longest = {}
            for bits, distance in sorted(interval, key=lambda item: (sum(item[0]), item[0])):
                predecessors = [other_bits for other_bits, other_distance in interval
                                if other_distance != distance and below(other_distance, distance)]
                longest[bits] = 0 if not predecessors else 1 + max(
                    longest[other_bits] for other_bits in predecessors)
            chain_height = max(longest.values())
            require(chain_height <= rank, "chain height exceeds changing bits")
            require(len(interval) <= 1 << rank, "interval exceeds binary state budget")
            maximum_interval = max(maximum_interval, len(interval))
            maximum_height = max(maximum_height, chain_height)
            maximum_rank = max(maximum_rank, rank)
    stream = sha256()
    for bits, distances in sorted(states):
        stream.update(f"{bits}:{distances}\n".encode())
    return {
        "tetrahedra": len(cells),
        "labels": len(source),
        "framework_states": len(states),
        "comparable_endpoint_pairs": comparable,
        "maximum_interval_states": maximum_interval,
        "maximum_chain_height": maximum_height,
        "maximum_changing_bits": maximum_rank,
        "state_stream_sha256": stream.hexdigest(),
    }


def budget_controls():
    records = []
    inequalities = 0
    for labels in range(1, 13):
        for input_height in (1, 7, 19):
            planes = 512 * 2**labels * (labels + 6) + 3 * labels + comb(labels, 3) + 6
            tetrahedra = 12 * planes * sum(comb(planes, index) for index in range(4))
            repair_height = 2**(10 * labels) * (input_height + 4)
            arrangement_plane = 64 * repair_height
            vertex_height = 64 * arrangement_plane
            vertices = comb(planes, 3)
            mesh_height = vertices * (vertex_height + 2)
            total_height = 2**15 * tetrahedra * mesh_height
            face_height = 1024 * mesh_height
            word_bound = (13 * (tetrahedra - 1) * face_height + 4 * mesh_height
                          + 2 * (tetrahedra - 1))
            require(word_bound <= 2**14 * tetrahedra * mesh_height,
                    "cleared reflection-word budget")
            require(2**14 * tetrahedra * mesh_height + mesh_height + 1 <= total_height,
                    "root-translation budget")
            inequalities += 2
            if labels in (1, 4, 8, 12) and input_height == 7:
                records.append({
                    "prescribed_labels": labels,
                    "planes": planes,
                    "tetrahedra_bit_length": tetrahedra.bit_length(),
                    "mesh_height_bit_length": mesh_height.bit_length(),
                    "all_state_height_bit_length": total_height.bit_length(),
                })
    return inequalities, records


def frontier_controls():
    inputs = []
    mass_checks = endpoint_checks = 0
    for delta in (F(1), F(2, 3), F(1, 7), F(1, 25)):
        k = ceiling(F(9, 1) / delta)
        ell_k = clog(k)
        h_k = isqrt(ell_k + 1)
        n_k = ceiling(F(k, h_k))
        atoms = min(k**3 * (2 * comb(2 * ell_k + 6, 3) - 1),
                    n_k**3 * (2 * comb(4 * ell_k + 11, 3) - 1))
        coordinate_denominator = 256 * k**3
        coordinate_integer = 3 * k * coordinate_denominator
        input_height = clog(768 * k**4 + 1)
        require(coordinate_denominator <= 1 << input_height
                and coordinate_integer < 1 << input_height
                and 3 * k <= 1 << input_height,
                "rational producer height")
        weight_total = 4 * k * atoms
        for labels in (4, 7, 13):
            numerator, denominator = delta.numerator, delta.denominator
            common = 2 * (2 * denominator + numerator) * weight_total * labels
            original = [weight_total] + [0] * (labels - 1)
            masses = [F((4 * denominator + numerator) * count * labels
                        + numerator * weight_total, common) for count in original]
            minimum = delta / (2 * (2 + delta) * labels)
            require(sum(masses) == 1 and min(masses) == minimum,
                    "augmented common mass denominator")
            mass_checks += 1
            for coordinate_height, radius in ((1, 1), (3, 12), (11, 37)):
                mass_log = fraction_clog(1 / minimum)
                j0 = (145 + 2 * clog(labels) + 6 * clog(radius)
                      + (222 * labels + 30) * coordinate_height)
                expanded = (40 + 2 * clog(labels) + 6 * clog(radius)
                            + 7 * (6 * labels * coordinate_height)
                            + 5 * clog(6 * 5040)
                            + 30 * (1 + (6 * labels + 1) * coordinate_height))
                require(expanded == j0, "endpoint denominator exponent")
                require(minimum >= F(1, 1 << mass_log), "mass logarithm")
                source_floor = F(1, 1 << (12 * labels * coordinate_height))
                upper_exponent = mass_log + 12 * labels * coordinate_height + 4
                require(minimum * source_floor / (8 + source_floor)
                        >= F(1, 1 << upper_exponent), "source peak envelope")
                endpoint_checks += 1
        inputs.append({
            "delta": str(delta),
            "k": k,
            "atom_bound": atoms,
            "coordinate_denominator": coordinate_denominator,
            "input_height": input_height,
        })
    return mass_checks, endpoint_checks, inputs


def audit():
    manifest = pins()
    factors = height_factor_controls()
    repairs = concrete_repair_controls()
    tree = framework_fixture(False)
    cycle = framework_fixture(True)
    require(tree["framework_states"] == 16, "tree fixture should realize every bit word")
    require(cycle["framework_states"] < tree["framework_states"],
            "cycle fixture did not enforce consistency")
    budget_count, budgets = budget_controls()
    mass_count, endpoint_count, inputs = frontier_controls()
    return {
        "status": "INDEPENDENT_COORDINATE_FRONTIER_REVIEW_PASS",
        "target_commit": manifest["target_commit"],
        "target_graph_ref": manifest["target_graph_ref"],
        "pinned_files": len(manifest["files"]),
        "height_factor_controls": factors,
        "concrete_repair_controls": repairs,
        "placement_controls": {"stacked_tree": tree, "cycle_constrained": cycle},
        "global_budget_inequalities": budget_count,
        "budget_samples": budgets,
        "mass_denominator_checks": mass_count,
        "endpoint_exponent_checks": endpoint_count,
        "frontier_inputs": inputs,
        "verdict": "accept coordinate-height theorem and finite-input consequence; middle hinge remains open",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--expected", type=Path, default=HERE / "REVIEW_EXPECTED.json")
    args = parser.parse_args()
    record = audit()
    if args.check:
        require(record == json.loads(args.expected.read_text()), "review record differs")
        print(record["status"])
    else:
        print(json.dumps(record, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
