#!/usr/bin/env python3
"""Independent arithmetic, family-enumeration and colouring controls."""

from itertools import combinations, product
import copy
import json

import verify as v


def generic_square(axis):
    output = [0] * 8
    for left, a in enumerate(axis):
        for right, b in enumerate(axis):
            repeated = left & right
            factor = 1
            for bit, prime in enumerate(v.PRIMES):
                if repeated & (1 << bit):
                    factor *= prime
            output[left ^ right] += a * b * factor
    return tuple(output)


def recursive_words(mask):
    edges = [pair for bit, pair in enumerate(v.LOCAL_PAIRS) if mask & (1 << bit)]
    earlier = [[] for _ in range(5)]
    for a, b in edges:
        earlier[b].append(a)
    word = [-1] * 5
    output = []

    def extend(vertex):
        if vertex == 5:
            output.append(tuple(word))
            return
        for colour in range(4):
            if all(word[other] != colour for other in earlier[vertex]):
                word[vertex] = colour
                extend(vertex + 1)
        word[vertex] = -1

    extend(0)
    return output


def cases_by_centres(pool_adjacency):
    cases = set()
    for centre in range(len(pool_adjacency)):
        opposite_edges = [
            (a, b)
            for a, b in combinations(sorted(pool_adjacency[centre]), 2)
            if b in pool_adjacency[a]
        ]
        for first, second in combinations(opposite_edges, 2):
            if not set(first) & set(second):
                cases.add(tuple(sorted((centre,) + first + second)))
    return cases


def main():
    certificate = json.loads((v.BASE / "certificate.json").read_text())
    expected = json.loads((v.BASE / "EXPECTED.json").read_text())
    v.require(v.audit(v.BASE.parent, certificate) == expected, "valid baseline")

    arithmetic_cases = 0
    zero = (0,) * 16
    for axis in product((-1, 0, 1), repeat=8):
        point = tuple(axis) + (0,) * 8
        v.require(v.norm_coefficients(point, zero) == generic_square(axis), "square oracle")
        arithmetic_cases += 1

    colouring_masks = 0
    cache = {}
    for mask in range(1 << len(v.LOCAL_PAIRS)):
        v.require(v.all_proper_five_words(mask, cache) == recursive_words(mask), "five-word oracle")
        colouring_masks += 1

    parent, pool, _, imported_edges = v.load_inputs(v.BASE.parent)
    pool_adjacency = [set() for _ in pool]
    for a, b in imported_edges:
        if a >= 509:
            a -= 509
            b -= 509
            pool_adjacency[a].add(b)
            pool_adjacency[b].add(a)
    triangles, pair_cases = v.enumerate_cases(pool_adjacency)
    centre_cases = cases_by_centres(pool_adjacency)
    v.require(set(pair_cases) == centre_cases, "two complete family enumerators")

    selected_global = list(v.HOST) + [509 + index for index in certificate["selected_q3_indices"]]
    selected_index = {vertex: index for index, vertex in enumerate(selected_global)}
    selected_edges = [
        (selected_index[a], selected_index[b])
        for a, b in imported_edges
        if a in selected_index and b in selected_index
    ]
    damaged = list(certificate["fresh_word"])
    a, b = selected_edges[0]
    damaged[b] = damaged[a]
    try:
        v.proper_word("".join(damaged), selected_edges, 508)
    except ValueError:
        colour_corruption_rejected = True
    else:
        raise ValueError("colour corruption accepted")

    input_name = next(iter(v.INPUT_HASHES))
    saved_hash = v.INPUT_HASHES[input_name]
    v.INPUT_HASHES[input_name] = "0" * 64
    try:
        v.load_inputs(v.BASE.parent)
    except ValueError:
        input_hash_corruption_rejected = True
    else:
        raise ValueError("input hash corruption accepted")
    finally:
        v.INPUT_HASHES[input_name] = saved_hash

    print(
        json.dumps(
            {
                "valid_baseline_passed": True,
                "quartic_square_oracle_cases": arithmetic_cases,
                "five_vertex_edge_masks_checked": colouring_masks,
                "pool_unit_triangles": len(triangles),
                "double_triangle_supports": len(pair_cases),
                "independent_family_enumerators_agree": True,
                "colour_corruption_rejected": colour_corruption_rejected,
                "input_hash_corruption_rejected": input_hash_corruption_rejected,
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
