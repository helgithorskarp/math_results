#!/usr/bin/env python3
"""Independent exact checks for the order-23 radius-seven Gram result.

This program imports no module from the reviewed package.  It reconstructs
the record Gram and its automorphism factors, obtains the global edit-set
orbit count by Burnside, checks the new connected and 6+1 color quotients by
a different Burnside/dynamic-programming computation, evaluates every
survivor determinant, and repeats all 26 normalized sign-cube obstructions.
"""

from collections import Counter
from concurrent.futures import ProcessPoolExecutor
from functools import lru_cache
from fractions import Fraction
from hashlib import sha256
from itertools import combinations, permutations
from json import dumps, loads
from math import gcd, isqrt, lcm
from pathlib import Path
import os
import sys


ORDER = 23
RECORD_ROOT = 2_779_447_296_000_000
CAPACITIES = (1, 2, 2, 1, 2, 2, 1, 2, 2, 4, 4)
RADIUS7_SHA256 = "bd7cadcbb73a60ea694f8e5912a693716dbc3e8d226f6131394d2c16e95a9193"
OBSTRUCTION_SHA256 = "1379fb3f8a884f2f457b02d1507175fd1481981cfe54d4fafe9b7884fa287e87"
SURVIVOR_SHA256 = "33d26b9cad04217d60bd68206b850232347c8be676fbf07b2a47eab53a291b74"


def require(condition, message):
    if not condition:
        raise ValueError(message)


def read_record(path):
    rows = []
    for line in Path(path).read_text().splitlines():
        row = [1 if symbol == "+" else -1 for symbol in line if symbol in "+-"]
        if row:
            require(len(row) == ORDER, "record row has wrong length")
            rows.append(row)
    require(len(rows) == ORDER, "record has wrong order")
    return rows


def gram_matrix(record):
    return [
        [sum(record[i][k] * record[j][k] for k in range(ORDER))
         for j in range(ORDER)]
        for i in range(ORDER)
    ]


def bareiss(matrix):
    work = [row[:] for row in matrix]
    size = len(work)
    if size == 0:
        return 1
    sign = 1
    previous = 1
    for column in range(size - 1):
        pivot = next((row for row in range(column, size)
                      if work[row][column]), None)
        if pivot is None:
            return 0
        if pivot != column:
            work[column], work[pivot] = work[pivot], work[column]
            sign = -sign
        value = work[column][column]
        for row in range(column + 1, size):
            for other in range(column + 1, size):
                numerator = (
                    work[row][other] * value
                    - work[row][column] * work[column][other]
                )
                require(numerator % previous == 0, "non-exact Bareiss division")
                work[row][other] = numerator // previous
        previous = value
        for row in range(column + 1, size):
            work[row][column] = 0
    return sign * work[-1][-1]


def components(adjacency):
    unseen = set(range(len(adjacency)))
    result = []
    while unseen:
        root = min(unseen)
        component = {root}
        stack = [root]
        while stack:
            vertex = stack.pop()
            for other in adjacency[vertex]:
                if other not in component:
                    component.add(other)
                    stack.append(other)
        unseen -= component
        result.append(tuple(sorted(component)))
    return sorted(result, key=lambda item: (-len(item), item))


def structural_factors(gram):
    adjacency = [
        {j for j in range(ORDER) if i != j and gram[i][j] == 3}
        for i in range(ORDER)
    ]
    comps = components(adjacency)
    require([len(item) for item in comps] == [15, 4, 4],
            "wrong Gram-graph components")
    large, block_a, block_b = comps
    for block in (block_a, block_b):
        require(all(adjacency[v] == set(block) - {v} for v in block),
                "four-vertex component is not complete")
    cores = tuple(v for v in large if len(adjacency[v]) == 6)
    require(len(cores) == 3, "wrong core triangle")
    inactive = {}
    active = {}
    for missing in range(3):
        wanted = set(cores) - {cores[missing]}
        active[missing] = tuple(sorted(
            v for v in large
            if len(adjacency[v]) == 5 and adjacency[v] & set(cores) == wanted
        ))
        inactive[missing] = tuple(sorted(
            v for v in large
            if len(adjacency[v]) == 3 and set(active[missing]) <= adjacency[v]
        ))
        require(len(active[missing]) == len(inactive[missing]) == 2,
                "wrong twin-pair structure")

    first = []
    for core_image in permutations(range(3)):
        for swaps in range(64):
            image = list(range(ORDER))
            for source in range(3):
                target = core_image[source]
                image[cores[source]] = cores[target]
                for kind, pair_map in enumerate((inactive, active)):
                    for position in range(2):
                        flip = (swaps >> (2 * source + kind)) & 1
                        image[pair_map[source][position]] = pair_map[target][position ^ flip]
            first.append(tuple(image))
    second = []
    for exchange in range(2):
        for perm_a in permutations(range(4)):
            for perm_b in permutations(range(4)):
                image = list(range(ORDER))
                target_a, target_b = (block_b, block_a) if exchange else (block_a, block_b)
                for index in range(4):
                    image[block_a[index]] = target_a[perm_a[index]]
                    image[block_b[index]] = target_b[perm_b[index]]
                second.append(tuple(image))
    require(len(set(first)) == 384 and len(set(second)) == 1152,
            "wrong automorphism-factor orders")
    for image in first + second:
        require(all(gram[i][j] == gram[image[i]][image[j]]
                    for i in range(ORDER) for j in range(i)),
                "claimed factor does not preserve Gram")
    return comps, first, second


def cycle_lengths(items, image):
    unseen = set(items)
    result = []
    while unseen:
        start = next(iter(unseen))
        current = start
        length = 0
        while True:
            unseen.remove(current)
            current = image(current)
            length += 1
            if current == start:
                break
        result.append(length)
    return tuple(sorted(result))


def action_types(group, vertices):
    vertices = tuple(vertices)
    pairs = tuple(combinations(vertices, 2))
    result = Counter()
    for permutation in group:
        vertex_cycles = cycle_lengths(vertices, lambda vertex: permutation[vertex])
        pair_cycles = cycle_lengths(
            pairs,
            lambda pair: tuple(sorted((permutation[pair[0]], permutation[pair[1]]))),
        )
        result[(vertex_cycles, pair_cycles)] += 1
    return result


def fixed_subset_counts(cycles, degree):
    coefficients = [1] + [0] * degree
    for length in cycles:
        for size in range(degree, length - 1, -1):
            coefficients[size] += coefficients[size - length]
    return coefficients


def global_burnside(first_types, second_types, degree):
    totals = [0] * (degree + 1)
    group_order = 0
    for (vertices_a, pairs_a), multiplicity_a in first_types.items():
        for (vertices_b, pairs_b), multiplicity_b in second_types.items():
            cross = []
            for left in vertices_a:
                for right in vertices_b:
                    cross.extend([lcm(left, right)] * gcd(left, right))
            fixed = fixed_subset_counts(pairs_a + pairs_b + tuple(cross), degree)
            multiplicity = multiplicity_a * multiplicity_b
            group_order += multiplicity
            for size, value in enumerate(fixed):
                totals[size] += multiplicity * value
    require(group_order == 442_368, "wrong full group order")
    require(all(value % group_order == 0 for value in totals),
            "non-integral global Burnside average")
    return [value // group_order for value in totals]


def pair_bit(left, right):
    if left < right:
        left, right = right, left
    require(left != right, "loop in graph")
    return left * (left - 1) // 2 + right


@lru_cache(maxsize=None)
def vertex_permutations(size):
    return tuple(permutations(range(size)))


@lru_cache(maxsize=None)
def induced_edge_maps(size):
    maps = []
    pair_count = size * (size - 1) // 2
    for permutation in vertex_permutations(size):
        image = [0] * pair_count
        for left in range(size):
            for right in range(left):
                image[pair_bit(left, right)] = pair_bit(
                    permutation[left], permutation[right]
                )
        maps.append(tuple(image))
    return tuple(maps)


def permuted_graph(graph, edge_map):
    image = 0
    remaining = graph
    while remaining:
        bit = remaining & -remaining
        index = bit.bit_length() - 1
        image |= 1 << edge_map[index]
        remaining -= bit
    return image


@lru_cache(maxsize=None)
def canonical_graph(size, graph):
    return min(permuted_graph(graph, edge_map)
               for edge_map in induced_edge_maps(size))


def connected_shapes_through_seven():
    levels = {1: {(2, 1)}}
    for edge_count in range(1, 7):
        following = set()
        for size, graph in levels[edge_count]:
            for left in range(size):
                for right in range(left):
                    bit = 1 << pair_bit(left, right)
                    if not graph & bit:
                        candidate = graph | bit
                        following.add((size, canonical_graph(size, candidate)))
            for neighbor in range(size):
                candidate = graph | (1 << pair_bit(size, neighbor))
                following.add((size + 1, canonical_graph(size + 1, candidate)))
        levels[edge_count + 1] = following
    expected = {
        6: {4: 1, 5: 5, 6: 13, 7: 11},
        7: {5: 4, 6: 19, 7: 33, 8: 23},
    }
    for edge_count, census in expected.items():
        observed = Counter(size for size, _ in levels[edge_count])
        require(dict(sorted(observed.items())) == census,
                f"wrong connected {edge_count}-edge shape census")
    return levels


def automorphism_cycle_types(size, graph):
    result = Counter()
    for permutation, edge_map in zip(vertex_permutations(size), induced_edge_maps(size)):
        if permuted_graph(graph, edge_map) == graph:
            cycles = cycle_lengths(range(size), lambda vertex: permutation[vertex])
            result[cycles] += 1
    return result


def outer_color_actions():
    result = []
    for core_permutation in permutations(range(3)):
        for swap_blocks in range(2):
            action = [0] * 11
            for core in range(3):
                for kind in range(3):
                    action[3 * core + kind] = 3 * core_permutation[core] + kind
            action[9] = 9 + swap_blocks
            action[10] = 10 - swap_blocks
            result.append(tuple(action))
    require(len(set(result)) == 12, "wrong outer color group")
    return tuple(result)


@lru_cache(maxsize=None)
def fixed_capacity_colorings(vertex_cycles, color_action):
    zero = (0,) * 11
    states = {zero: 1}
    for length in vertex_cycles:
        options = Counter()
        for start in range(11):
            counts = [0] * 11
            color = start
            for _ in range(length):
                counts[color] += 1
                color = color_action[color]
            if color == start and all(counts[i] <= CAPACITIES[i] for i in range(11)):
                options[tuple(counts)] += 1
        following = {}
        for state, ways in states.items():
            for addition, multiplicity in options.items():
                total = tuple(state[i] + addition[i] for i in range(11))
                if all(total[i] <= CAPACITIES[i] for i in range(11)):
                    following[total] = following.get(total, 0) + ways * multiplicity
        states = following
    return sum(states.values())


def color_orbits(cycle_type_counts):
    actions = outer_color_actions()
    numerator = 0
    automorphism_order = sum(cycle_type_counts.values())
    for cycles, multiplicity in cycle_type_counts.items():
        for action in actions:
            numerator += multiplicity * fixed_capacity_colorings(cycles, action)
    denominator = automorphism_order * len(actions)
    require(numerator % denominator == 0, "non-integral color-orbit average")
    return numerator // denominator


def new_color_quotients(levels):
    connected_total = 0
    for size, graph in levels[7]:
        connected_total += color_orbits(automorphism_cycle_types(size, graph))
    six_plus_one_total = 0
    for size, graph in levels[6]:
        source = automorphism_cycle_types(size, graph)
        product_types = Counter()
        for cycles, multiplicity in source.items():
            product_types[tuple(sorted(cycles + (1, 1)))] += multiplicity
            product_types[tuple(sorted(cycles + (2,)))] += multiplicity
        six_plus_one_total += color_orbits(product_types)
    return connected_total, six_plus_one_total


def edited_gram(base, edge_list, indices):
    result = [row[:] for row in base]
    for index in indices:
        left, right = edge_list[index]
        result[left][right] = result[right][left] = 2 - base[left][right]
    return result


def scaled_inverse(matrix):
    size = len(matrix)
    augmented = [
        [Fraction(value) for value in matrix[row]]
        + [Fraction(row == column) for column in range(size)]
        for row in range(size)
    ]
    for column in range(size):
        pivot = next(row for row in range(column, size) if augmented[row][column])
        augmented[column], augmented[pivot] = augmented[pivot], augmented[column]
        divisor = augmented[column][column]
        augmented[column] = [value / divisor for value in augmented[column]]
        for row in range(size):
            if row == column:
                continue
            multiplier = augmented[row][column]
            if multiplier:
                augmented[row] = [
                    left - multiplier * right
                    for left, right in zip(augmented[row], augmented[column])
                ]
    inverse = [row[size:] for row in augmented]
    scale = lcm(*(value.denominator for row in inverse for value in row))
    numerator = [[int(value * scale) for value in row] for row in inverse]
    require(all(
        sum(matrix[i][k] * numerator[k][j] for k in range(size))
        == scale * (i == j)
        for i in range(size) for j in range(size)
    ), "scaled inverse identity failed")
    return scale, numerator


def admissible_columns(scale, numerator):
    vector = [1] * ORDER
    off_diagonal_sums = [
        sum(numerator[row][column] for column in range(ORDER) if row != column)
        for row in range(ORDER)
    ]
    quadratic = sum(map(sum, numerator))
    gray = 0
    masks = []
    for step in range(1 << 22):
        if quadratic == scale:
            masks.append(gray)
        if step + 1 == 1 << 22:
            break
        bit = ((step + 1) & -(step + 1)).bit_length() - 1
        coordinate = bit + 1
        old_sign = vector[coordinate]
        quadratic -= 4 * old_sign * off_diagonal_sums[coordinate]
        for row in range(ORDER):
            if row != coordinate:
                off_diagonal_sums[row] -= (
                    2 * numerator[row][coordinate] * old_sign
                )
        vector[coordinate] = -old_sign
        gray ^= 1 << bit
    return masks


def vector_from_mask(mask):
    return [1] + [-1 if mask >> bit & 1 else 1 for bit in range(22)]


def mask_hash(masks):
    return sha256("".join(f"{mask}\n" for mask in masks).encode("ascii")).hexdigest()


def verify_obstruction_task(task):
    matrix, entry = task
    root = entry["determinant_root"]
    require(bareiss(matrix) == root * root, "candidate determinant mismatch")
    require(all(bareiss([row[:size] for row in matrix[:size]]) > 0
                for size in range(1, ORDER + 1)),
            "candidate is not positive definite")
    scale, numerator = scaled_inverse(matrix)
    require(scale == entry["inverse_scale"], "inverse scale mismatch")
    masks = admissible_columns(scale, numerator)
    require(len(masks) == entry["normalized_column_count"],
            "normalized column count mismatch")
    require(mask_hash(masks) == entry["normalized_columns_sha256"],
            "normalized column hash mismatch")
    vectors = [vector_from_mask(mask) for mask in masks]
    obstruction = entry["obstruction"]
    kind = obstruction["type"]
    if kind == "no_admissible_column":
        require(not vectors, "claimed empty column set is nonempty")
    elif kind == "forced_pair_product":
        first, second = obstruction["rows_zero_based"]
        forced = obstruction["forced_product_per_column"]
        require(vectors and all(v[first] * v[second] == forced for v in vectors),
                "pair product is not forced")
        require(ORDER * forced != matrix[first][second],
                "pair product does not contradict Gram")
    elif kind == "forced_three_row_expression":
        first, second, third = obstruction["rows_zero_based"]
        forced = obstruction["forced_value_per_column"]
        values = [
            1 + v[first] * v[second] + v[first] * v[third]
            + v[second] * v[third]
            for v in vectors
        ]
        target = (
            ORDER + matrix[first][second] + matrix[first][third]
            + matrix[second][third]
        )
        require(vectors and all(value == forced for value in values),
                "three-row expression is not forced")
        require(ORDER * forced != target,
                "three-row expression does not contradict Gram")
    else:
        raise ValueError(f"unknown obstruction kind: {kind}")
    return {
        "edges": entry["edge_indices"],
        "root": root,
        "admissible_columns": len(masks),
        "obstruction": kind,
    }


def main():
    if len(sys.argv) not in (5, 6):
        raise SystemExit(
            "usage: independent_check.py RECORD RADIUS7 OBSTRUCTIONS EXPECTED [WORKERS]"
        )
    record_path, radius_path, obstruction_path, expected_path = sys.argv[1:5]
    workers = int(sys.argv[5]) if len(sys.argv) == 6 else min(8, os.cpu_count() or 1)
    require(workers >= 1, "workers must be positive")

    radius_bytes = Path(radius_path).read_bytes()
    obstruction_bytes = Path(obstruction_path).read_bytes()
    require(sha256(radius_bytes).hexdigest() == RADIUS7_SHA256,
            "radius-seven certificate hash mismatch")
    require(sha256(obstruction_bytes).hexdigest() == OBSTRUCTION_SHA256,
            "obstruction certificate hash mismatch")
    radius = loads(radius_bytes)
    obstruction = loads(obstruction_bytes)

    record = read_record(record_path)
    gram = gram_matrix(record)
    require(bareiss(gram) == RECORD_ROOT**2, "record determinant mismatch")
    require(sum(gram[i][j] == 3 for i in range(ORDER) for j in range(i)) == 45,
            "wrong number of Gram graph edges")
    comps, first, second = structural_factors(gram)
    first_types = action_types(first, comps[0])
    second_types = action_types(second, comps[1] + comps[2])
    global_orbits = global_burnside(first_types, second_types, 7)
    require(global_orbits == [1, 16, 380, 8887, 197931, 4132509,
                              81094402, 1503560419],
            "global Burnside orbit counts mismatch")

    levels = connected_shapes_through_seven()
    connected, six_plus_one = new_color_quotients(levels)
    require(connected == radius["connected"]["symmetry_classes"] == 75_778_019,
            "connected radius-seven quotient mismatch")
    require(six_plus_one == radius["six_plus_one"]["symmetry_classes"]
            == 158_015_168, "six-plus-one quotient mismatch")
    stored = global_orbits[7] - connected - six_plus_one
    require(stored == radius["stored_partition_symmetry_classes"]
            == 1_269_767_232,
            "stored-partition quotient does not match independent remainder")

    survivors = radius["survivor_edge_indices"]
    encoded_survivors = "".join(
        ",".join(map(str, row)) + "\n" for row in survivors
    ).encode("ascii")
    require(sha256(encoded_survivors).hexdigest() == SURVIVOR_SHA256,
            "survivor stream hash mismatch")
    edge_list = tuple((i, j) for i in range(ORDER) for j in range(i))
    roots = []
    exceptional = []
    matrices = {}
    for indices in survivors:
        require(indices == sorted(set(indices)) and len(indices) == 7,
                "malformed survivor")
        matrix = edited_gram(gram, edge_list, indices)
        determinant = bareiss(matrix)
        root = isqrt(determinant)
        require(root * root == determinant, "survivor determinant is not square")
        roots.append(root)
        if root > RECORD_ROOT:
            exceptional.append((tuple(indices), root))
            matrices[tuple(indices)] = matrix
    exceptional.sort(key=lambda item: (-item[1], item[0]))
    require(len(roots) == 2943 and len(set(roots)) == 2436,
            "square-survivor summary mismatch")
    require(sum(root == RECORD_ROOT for root in roots) == 0,
            "unexpected record-equality survivor")
    require(max(root for root in roots if root < RECORD_ROOT)
            == 2_777_874_432_000_000, "wrong largest subrecord root")
    require(len(exceptional) == 26 and exceptional[0][1] == 2_838_233_088_000_000,
            "record-beating survivor summary mismatch")

    entries = obstruction["candidates"]
    require([(tuple(entry["edge_indices"]), entry["determinant_root"])
             for entry in entries] == exceptional,
            "obstruction candidates do not match determinant census")
    tasks = [(matrices[tuple(entry["edge_indices"])], entry) for entry in entries]
    if workers == 1:
        checked = [verify_obstruction_task(task) for task in tasks]
    else:
        with ProcessPoolExecutor(max_workers=workers) as pool:
            checked = list(pool.map(verify_obstruction_task, tasks))
    kinds = Counter(item["obstruction"] for item in checked)
    require(kinds == {"no_admissible_column": 11,
                      "forced_pair_product": 14,
                      "forced_three_row_expression": 1},
            "obstruction-kind census mismatch")

    output = {
        "status": "PASS",
        "record_root": RECORD_ROOT,
        "automorphism_factor_orders": [len(first), len(second)],
        "global_edit_orbits_through_seven": global_orbits,
        "independent_shape_census": {
            "six_edges": dict(sorted(Counter(size for size, _ in levels[6]).items())),
            "seven_edges": dict(sorted(Counter(size for size, _ in levels[7]).items())),
        },
        "independent_color_burnside": {
            "connected": connected,
            "six_plus_one": six_plus_one,
            "stored_inherited": stored,
            "total": connected + six_plus_one + stored,
        },
        "certificate_sha256": sha256(radius_bytes).hexdigest(),
        "survivor_stream_sha256": sha256(encoded_survivors).hexdigest(),
        "square_survivors": {
            "orbits": len(roots),
            "distinct_roots": len(set(roots)),
            "record_equal": 0,
            "record_beating": len(exceptional),
            "largest_root": max(roots),
            "largest_below_record": max(root for root in roots if root < RECORD_ROOT),
        },
        "sign_column_obstructions": {
            "candidate_count": len(checked),
            "kind_counts": dict(sorted(kinds.items())),
            "admissible_column_counts": [item["admissible_columns"] for item in checked],
        },
        "trust_boundary": (
            "The checker independently validates the new connected and 6+1 quotient "
            "counts, compact survivor list, and sign-column contradictions. The "
            "streaming C++ generator remains the producer of the 2,943 survivors; "
            "stored disconnected partitions inherit the previously reviewed colored-"
            "component catalogue."
        ),
    }
    encoded = (dumps(output, indent=2, sort_keys=True) + "\n").encode()
    if expected_path == "-":
        sys.stdout.buffer.write(encoded)
        return
    require(encoded == Path(expected_path).read_bytes(),
            "output differs from expected JSON")
    print(dumps({"sha256": sha256(encoded).hexdigest(), "status": "PASS"},
                sort_keys=True))


if __name__ == "__main__":
    main()
