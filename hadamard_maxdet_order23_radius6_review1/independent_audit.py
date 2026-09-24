#!/usr/bin/env python3
"""Independent exact audit for the order-23 radius-six local Gram result.

The script does not import the author's Python modules.  It reconstructs the
record Gram graph, its forced automorphism factors, the Burnside orbit count,
all exact survivor determinants, the two exceptional orbit sizes, and the
sign-column obstructions.
"""

from collections import Counter
from fractions import Fraction
from hashlib import sha256
from itertools import combinations, permutations
import json
import math
from pathlib import Path
import sys


ORDER = 23
RECORD_ROOT = 2779447296000000
EXPECTED_RESULT_SHA256 = (
    "8145a2fdf28d61be0abb24813385c9b4f28f358668875be5f40ef9bc2c8e46e2"
)


def read_record(path):
    rows = []
    for line in Path(path).read_text().splitlines():
        row = [1 if symbol == "+" else -1 for symbol in line if symbol in "+-"]
        if row:
            assert len(row) == ORDER
            rows.append(row)
    assert len(rows) == ORDER
    return rows


def gram_matrix(record):
    return [
        [sum(record[i][k] * record[j][k] for k in range(ORDER))
         for j in range(ORDER)]
        for i in range(ORDER)
    ]


def bareiss(matrix):
    a = [row[:] for row in matrix]
    n = len(a)
    sign = 1
    previous = 1
    for column in range(n - 1):
        pivot = next((r for r in range(column, n) if a[r][column]), None)
        if pivot is None:
            return 0
        if pivot != column:
            a[column], a[pivot] = a[pivot], a[column]
            sign = -sign
        value = a[column][column]
        for i in range(column + 1, n):
            for j in range(column + 1, n):
                numerator = a[i][j] * value - a[i][column] * a[column][j]
                assert numerator % previous == 0
                a[i][j] = numerator // previous
        previous = value
        for i in range(column + 1, n):
            a[i][column] = 0
    return sign * a[-1][-1]


def components(adjacency):
    unseen = set(range(len(adjacency)))
    answer = []
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
        answer.append(tuple(sorted(component)))
    return sorted(answer, key=lambda item: (-len(item), item))


def structural_factors(gram):
    adjacency = [
        {j for j in range(ORDER) if j != i and gram[i][j] == 3}
        for i in range(ORDER)
    ]
    comps = components(adjacency)
    assert [len(item) for item in comps] == [15, 4, 4]
    large, block_a, block_b = comps
    assert all(adjacency[v] == set(block_a) - {v} for v in block_a)
    assert all(adjacency[v] == set(block_b) - {v} for v in block_b)

    cores = tuple(v for v in large if len(adjacency[v]) == 6)
    assert len(cores) == 3 and all(
        set(cores) - {v} <= adjacency[v] for v in cores
    )
    inactive = {}
    active = {}
    for missing in range(3):
        wanted = set(cores) - {cores[missing]}
        active[missing] = tuple(sorted(
            v for v in large
            if len(adjacency[v]) == 5 and adjacency[v] & set(cores) == wanted
        ))
        assert len(active[missing]) == 2
        inactive[missing] = tuple(sorted(
            v for v in large
            if len(adjacency[v]) == 3
            and set(active[missing]) <= adjacency[v]
        ))
        assert len(inactive[missing]) == 2

    first = []
    for core_image in permutations(range(3)):
        for swaps in range(64):
            image = list(range(ORDER))
            for source in range(3):
                target = core_image[source]
                image[cores[source]] = cores[target]
                for kind, pair_map in enumerate((inactive, active)):
                    source_pair = pair_map[source]
                    target_pair = pair_map[target]
                    flip = (swaps >> (2 * source + kind)) & 1
                    for position in range(2):
                        image[source_pair[position]] = target_pair[position ^ flip]
            first.append(tuple(image))
    assert len(set(first)) == 384

    second = []
    a = tuple(block_a)
    b = tuple(block_b)
    for exchange in range(2):
        for perm_a in permutations(range(4)):
            for perm_b in permutations(range(4)):
                image = list(range(ORDER))
                target_a, target_b = (b, a) if exchange else (a, b)
                for i in range(4):
                    image[a[i]] = target_a[perm_a[i]]
                    image[b[i]] = target_b[perm_b[i]]
                second.append(tuple(image))
    assert len(set(second)) == 1152

    edges = tuple((i, j) for i in range(ORDER) for j in range(i))
    for image in first + second:
        assert all(gram[i][j] == gram[image[i]][image[j]] for i, j in edges)
    return adjacency, comps, first, second


def cycle_lengths(items, image):
    unseen = set(items)
    lengths = []
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
        lengths.append(length)
    return tuple(sorted(lengths))


def action_type_counts(group, vertices):
    vertices = tuple(vertices)
    pairs = tuple(combinations(vertices, 2))
    pair_set = set(pairs)
    counts = Counter()
    for permutation in group:
        vertex_cycles = cycle_lengths(vertices, lambda v: permutation[v])
        pair_cycles = cycle_lengths(
            pairs,
            lambda pair: tuple(sorted((permutation[pair[0]], permutation[pair[1]]))),
        )
        assert all(pair in pair_set for pair in pairs)
        counts[(vertex_cycles, pair_cycles)] += 1
    return counts


def fixed_subset_counts(cycles, degree):
    coefficients = [1] + [0] * degree
    for length in cycles:
        for k in range(degree, length - 1, -1):
            coefficients[k] += coefficients[k - length]
    return coefficients


def burnside_through_six(first_types, second_types):
    totals = [0] * 7
    group_order = 0
    for (vertex_a, pairs_a), count_a in first_types.items():
        for (vertex_b, pairs_b), count_b in second_types.items():
            cross = []
            for a in vertex_a:
                for b in vertex_b:
                    cross.extend([math.lcm(a, b)] * math.gcd(a, b))
            fixed = fixed_subset_counts(pairs_a + pairs_b + tuple(cross), 6)
            multiplicity = count_a * count_b
            group_order += multiplicity
            for k, value in enumerate(fixed):
                totals[k] += multiplicity * value
    assert group_order == 442368
    assert all(value % group_order == 0 for value in totals)
    return [value // group_order for value in totals]


def edited_gram(base, edge_list, indices):
    result = [row[:] for row in base]
    for index in indices:
        i, j = edge_list[index]
        result[i][j] = result[j][i] = 2 - base[i][j]
    return result


def combined_image(first, second):
    # The factors have disjoint supports and commute.
    return tuple(second[first[v]] for v in range(ORDER))


def exceptional_orbit_size(indices, first, second, edge_list, edge_index):
    seed = frozenset(indices)
    stabilizer = 0
    for left in first:
        for right in second:
            image = combined_image(left, right)
            mapped = frozenset(
                edge_index[tuple(sorted((image[edge_list[i][0]], image[edge_list[i][1]])))]
                for i in seed
            )
            stabilizer += mapped == seed
    assert 442368 % stabilizer == 0
    return 442368 // stabilizer


def scaled_inverse(matrix):
    size = len(matrix)
    augmented = [
        [Fraction(value) for value in matrix[i]]
        + [Fraction(i == j) for j in range(size)]
        for i in range(size)
    ]
    for column in range(size):
        pivot = next(i for i in range(column, size) if augmented[i][column])
        augmented[column], augmented[pivot] = augmented[pivot], augmented[column]
        value = augmented[column][column]
        augmented[column] = [entry / value for entry in augmented[column]]
        for i in range(size):
            if i == column:
                continue
            multiplier = augmented[i][column]
            if multiplier:
                augmented[i] = [
                    a - multiplier * b
                    for a, b in zip(augmented[i], augmented[column])
                ]
    inverse = [row[size:] for row in augmented]
    scale = math.lcm(*(value.denominator for row in inverse for value in row))
    numerator = [[int(value * scale) for value in row] for row in inverse]
    assert all(
        sum(matrix[i][k] * numerator[k][j] for k in range(size))
        == scale * (i == j)
        for i in range(size) for j in range(size)
    )
    return scale, numerator


def admissible_columns(matrix):
    scale, numerator = scaled_inverse(matrix)
    vector = [1] * ORDER
    row_sums = [
        sum(numerator[i][j] for j in range(ORDER) if j != i)
        for i in range(ORDER)
    ]
    value = sum(sum(row) for row in numerator)
    masks = []
    gray = 0
    for step in range(1 << 22):
        if value == scale:
            masks.append(gray)
        if step + 1 == 1 << 22:
            break
        bit = ((step + 1) & -(step + 1)).bit_length() - 1
        coordinate = bit + 1
        old = vector[coordinate]
        value -= 4 * old * row_sums[coordinate]
        for i in range(ORDER):
            if i != coordinate:
                row_sums[i] -= 2 * numerator[i][coordinate] * old
        vector[coordinate] = -old
        gray ^= 1 << bit
    return scale, masks


def main():
    if len(sys.argv) != 3:
        raise SystemExit("usage: independent_audit.py record23.txt radius6_result.json")
    record_path, result_path = sys.argv[1:]
    result_bytes = Path(result_path).read_bytes()
    assert sha256(result_bytes).hexdigest() == EXPECTED_RESULT_SHA256
    result = json.loads(result_bytes)

    record = read_record(record_path)
    gram = gram_matrix(record)
    assert bareiss(gram) == RECORD_ROOT**2
    assert sum(gram[i][j] == 3 for i in range(ORDER) for j in range(i)) == 45

    adjacency, comps, first, second = structural_factors(gram)
    first_types = action_type_counts(first, comps[0])
    second_vertices = comps[1] + comps[2]
    second_types = action_type_counts(second, second_vertices)
    orbit_counts = burnside_through_six(first_types, second_types)
    assert orbit_counts == [1, 16, 380, 8887, 197931, 4132509, 81094402]

    radius = result["radius_six"]
    assert radius["symmetry_classes"] == orbit_counts[6]
    assert sum(radius["witness_counts"]) + radius["survives_48_nonsquare_tests"] == orbit_counts[6]
    survivors = radius["survivor_edge_indices"]
    assert len(survivors) == 359 == len({tuple(item) for item in survivors})

    edge_list = tuple((i, j) for i in range(ORDER) for j in range(i))
    edge_index = {tuple(sorted(pair)): i for i, pair in enumerate(edge_list)}
    roots = []
    exceptional_records = []
    for indices in survivors:
        assert len(indices) == 6 and indices == sorted(set(indices))
        matrix = edited_gram(gram, edge_list, indices)
        determinant = bareiss(matrix)
        root = math.isqrt(determinant)
        assert root * root == determinant
        roots.append(root)
        if root > RECORD_ROOT:
            exceptional_records.append((root, tuple(indices), matrix))
    exceptional_records.sort(reverse=True, key=lambda item: (item[0], item[1]))
    exceptional = [(root, indices) for root, indices, _ in exceptional_records]
    exceptional_matrices = [matrix for _, _, matrix in exceptional_records]
    assert len(set(roots)) == 298
    assert max(root for root in roots if root < RECORD_ROOT) == 2771425689600000
    assert exceptional == [
        (2823605452800000, (10, 22, 38, 47, 89, 92)),
        (2783182848000000, (2, 11, 36, 38, 46, 78)),
    ]

    orbit_sizes = [
        exceptional_orbit_size(indices, first, second, edge_list, edge_index)
        for _, indices in exceptional
    ]
    assert orbit_sizes == [96, 48]
    for matrix in exceptional_matrices:
        assert all(bareiss([row[:size] for row in matrix[:size]]) > 0
                   for size in range(1, ORDER + 1))

    column_counts = []
    first_two_products = []
    inverse_scales = []
    for matrix in exceptional_matrices:
        scale, masks = admissible_columns(matrix)
        inverse_scales.append(scale)
        column_counts.append(len(masks))
        first_two_products.append(sorted({1 if not (mask & 1) else -1 for mask in masks}))
    assert inverse_scales == [51563888640, 18035310240]
    assert column_counts == [0, 48]
    assert first_two_products == [[], [1]]
    assert exceptional_matrices[1][0][1] == 3

    output = {
        "status": "independent radius-six audit passed",
        "record_root": RECORD_ROOT,
        "gram_components": [list(item) for item in comps],
        "automorphism_factors": [len(first), len(second)],
        "factor_action_types": [len(first_types), len(second_types)],
        "burnside_orbits_through_six": orbit_counts,
        "generated_result_sha256": sha256(result_bytes).hexdigest(),
        "sieve_accounting": {
            "classes": radius["symmetry_classes"],
            "rejected": sum(radius["witness_counts"]),
            "survivors": len(survivors),
        },
        "square_survivors": {
            "orbits": len(roots),
            "distinct_roots": len(set(roots)),
            "largest_below_record": max(root for root in roots if root < RECORD_ROOT),
        },
        "exceptional_candidates": [
            {
                "root": root,
                "edges": list(indices),
                "orbit_size": orbit_size,
                "inverse_scale": scale,
                "admissible_normalized_columns": count,
                "possible_v0_v1": products,
            }
            for (root, indices), orbit_size, scale, count, products
            in zip(exceptional, orbit_sizes, inverse_scales, column_counts,
                   first_two_products)
        ],
    }
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
