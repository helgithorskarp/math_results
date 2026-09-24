#!/usr/bin/env python3
"""Symmetry-compressed exact sign-column obstructions.

The exceptional candidate Grams have large, explicit row-permutation
subgroups.  Binary sign vectors modulo these subgroups are classified by the
signs on fixed vertices, the negative counts on interchangeable pairs, and
the unordered negative counts on two interchangeable four-vertex blocks.
"""

from __future__ import annotations

import hashlib
import itertools
import json
import math
from dataclasses import dataclass
from typing import Iterator

from candidate_obstructions import (
    CANDIDATES,
    ORDER,
    candidate_gram,
    gram_matrix,
    quadratic,
    read_record,
    scaled_inverse,
)


BLOCKS = ((15, 16, 17, 18), (19, 20, 21, 22))


@dataclass(frozen=True)
class SymmetryData:
    fixed_vertices: tuple[int, ...]
    interchangeable_pairs: tuple[tuple[int, int], ...]

    @property
    def subgroup_order(self) -> int:
        return (2 ** len(self.interchangeable_pairs)) * (24 * 24 * 2)


SYMMETRIES = (
    SymmetryData(
        fixed_vertices=(1, 2, 5, 6, 7, 8, 11, 12, 13, 14),
        interchangeable_pairs=((3, 4), (9, 10)),
    ),
    SymmetryData(
        fixed_vertices=(1, 2, 5, 6, 9, 10, 13, 14),
        interchangeable_pairs=((3, 4), (7, 8), (11, 12)),
    ),
)

EXPECTED_CENSUSES = {
    "candidate1_all": {
        "canonical_representatives": 138240,
        "represented_labeled_vectors": 4194304,
        "distinct_quadratic_values": 86326,
        "closest_nonzero_gap_to_scale": 13872,
        "solution_representatives": 0,
        "solution_labeled_vectors": 0,
        "solution_records": [],
        "census_sha256": "f1adaf219c10cf1cc3e6ea40dc9ab858bffb0a91347902b0d583ca6f80290ad5",
    },
    "candidate2_all": {
        "canonical_representatives": 103680,
        "represented_labeled_vectors": 4194304,
        "distinct_quadratic_values": 78705,
        "closest_nonzero_gap_to_scale": 896,
        "solution_representatives": 2,
        "solution_labeled_vectors": 48,
        "solution_records": [
            {"mask": 3679880, "orbit_size": 32},
            {"mask": 3671084, "orbit_size": 16},
        ],
        "census_sha256": "2d83ad3b68aed06f5844335c66c1ae5c62f80b1f8b4b1c0847d7c3c42020f94a",
    },
    "candidate2_forbidden": {
        "canonical_representatives": 51840,
        "represented_labeled_vectors": 2097152,
        "distinct_quadratic_values": 39360,
        "closest_nonzero_gap_to_scale": 2052,
        "solution_representatives": 0,
        "solution_labeled_vectors": 0,
        "solution_records": [],
        "census_sha256": "71491d5644dc929ea9759dbaeab1a9aafb7d7d818d5f0e00f51699353c528d3c",
    },
}


def permutation_matrix_action(
    matrix: list[list[int]], permutation: tuple[int, ...]
) -> list[list[int]]:
    return [
        [matrix[permutation[left]][permutation[right]] for right in range(ORDER)]
        for left in range(ORDER)
    ]


def symmetry_generators(data: SymmetryData) -> list[tuple[int, ...]]:
    generators: list[tuple[int, ...]] = []

    def transposition(left: int, right: int) -> tuple[int, ...]:
        answer = list(range(ORDER))
        answer[left], answer[right] = answer[right], answer[left]
        return tuple(answer)

    for pair in data.interchangeable_pairs:
        generators.append(transposition(*pair))
    for block in BLOCKS:
        generators.append(transposition(block[0], block[1]))
        cycle = list(range(ORDER))
        for source, target in zip(block, block[1:] + block[:1]):
            cycle[source] = target
        generators.append(tuple(cycle))
    swap_blocks = list(range(ORDER))
    for left, right in zip(*BLOCKS):
        swap_blocks[left], swap_blocks[right] = right, left
    generators.append(tuple(swap_blocks))
    return generators


def canonical_vectors(
    data: SymmetryData, forced_signs: dict[int, int]
) -> Iterator[tuple[list[int], int]]:
    free_fixed = tuple(
        vertex for vertex in data.fixed_vertices if vertex not in forced_signs
    )

    def generate():
        for fixed_signs in itertools.product((1, -1), repeat=len(free_fixed)):
            for pair_counts in itertools.product(
                range(3), repeat=len(data.interchangeable_pairs)
            ):
                for first_count in range(5):
                    for second_count in range(first_count, 5):
                        vector = [1] * ORDER
                        for vertex, sign in forced_signs.items():
                            vector[vertex] = sign
                        for vertex, sign in zip(free_fixed, fixed_signs):
                            vector[vertex] = sign

                        multiplicity = 1
                        for pair, count in zip(
                            data.interchangeable_pairs, pair_counts
                        ):
                            for vertex in pair[:count]:
                                vector[vertex] = -1
                            multiplicity *= math.comb(2, count)

                        for vertex in BLOCKS[0][:first_count]:
                            vector[vertex] = -1
                        for vertex in BLOCKS[1][:second_count]:
                            vector[vertex] = -1
                        block_multiplicity = (
                            math.comb(4, first_count) ** 2
                            if first_count == second_count
                            else 2
                            * math.comb(4, first_count)
                            * math.comb(4, second_count)
                        )
                        multiplicity *= block_multiplicity
                        yield vector, multiplicity

    return generate()


def census(
    numerator: list[list[int]],
    scale: int,
    data: SymmetryData,
    forced_signs: dict[int, int],
) -> dict[str, object]:
    digest = hashlib.sha256()
    representatives = 0
    labeled_vectors = 0
    solution_representatives = 0
    solution_vectors = 0
    solution_records: list[dict[str, int]] = []
    distinct_values: set[int] = set()
    closest_nonzero_gap: int | None = None

    for vector, multiplicity in canonical_vectors(data, forced_signs):
        value = quadratic(numerator, vector)
        mask = sum((sign < 0) << index for index, sign in enumerate(vector))
        digest.update(f"{mask}:{multiplicity}:{value}\n".encode("ascii"))
        representatives += 1
        labeled_vectors += multiplicity
        distinct_values.add(value)
        gap = abs(value - scale)
        if gap:
            closest_nonzero_gap = (
                gap
                if closest_nonzero_gap is None
                else min(closest_nonzero_gap, gap)
            )
        else:
            solution_representatives += 1
            solution_vectors += multiplicity
            solution_records.append({"mask": mask, "orbit_size": multiplicity})

    assert closest_nonzero_gap is not None
    return {
        "canonical_representatives": representatives,
        "represented_labeled_vectors": labeled_vectors,
        "distinct_quadratic_values": len(distinct_values),
        "closest_nonzero_gap_to_scale": closest_nonzero_gap,
        "solution_representatives": solution_representatives,
        "solution_labeled_vectors": solution_vectors,
        "solution_records": solution_records,
        "census_sha256": digest.hexdigest(),
    }


def main() -> None:
    base = gram_matrix(read_record())
    candidate_data = []
    numerators = []
    for index, (candidate, symmetry) in enumerate(zip(CANDIDATES, SYMMETRIES)):
        cells = (
            [(0,)]
            + [(vertex,) for vertex in symmetry.fixed_vertices]
            + list(symmetry.interchangeable_pairs)
            + list(BLOCKS)
        )
        assert len({vertex for cell in cells for vertex in cell}) == ORDER
        assert sorted(vertex for cell in cells for vertex in cell) == list(range(ORDER))
        matrix = candidate_gram(base, candidate["edges"])
        scale, numerator = scaled_inverse(matrix)
        assert scale == candidate["inverse_scale"]
        generators = symmetry_generators(symmetry)
        assert len(set(generators)) == len(generators)
        for permutation in generators:
            assert permutation[0] == 0 and permutation[1] == 1
            assert permutation_matrix_action(matrix, permutation) == matrix
            assert permutation_matrix_action(numerator, permutation) == numerator
        candidate_data.append(
            {
                "candidate_index": index + 1,
                "edges": list(candidate["edges"]),
                "inverse_scale": scale,
                "fixed_vertices": list(symmetry.fixed_vertices),
                "interchangeable_pairs": [list(pair) for pair in symmetry.interchangeable_pairs],
                "interchangeable_four_blocks": [list(block) for block in BLOCKS],
                "symmetry_subgroup_order": symmetry.subgroup_order,
            }
        )
        numerators.append(numerator)

    assert [item.subgroup_order for item in SYMMETRIES] == [4608, 9216]

    candidate1_all = census(
        numerators[0], CANDIDATES[0]["inverse_scale"], SYMMETRIES[0], {}
    )
    candidate2_all = census(
        numerators[1], CANDIDATES[1]["inverse_scale"], SYMMETRIES[1], {}
    )
    candidate2_forbidden = census(
        numerators[1], CANDIDATES[1]["inverse_scale"], SYMMETRIES[1], {1: -1}
    )
    assert candidate1_all == EXPECTED_CENSUSES["candidate1_all"]
    assert candidate2_all == EXPECTED_CENSUSES["candidate2_all"]
    assert candidate2_forbidden == EXPECTED_CENSUSES["candidate2_forbidden"]
    candidate_data[0]["all_normalized_columns"] = candidate1_all
    candidate_data[1]["all_normalized_columns"] = candidate2_all
    candidate_data[1]["forbidden_v0v1_minus_one"] = candidate2_forbidden

    result = {
        "order": ORDER,
        "normalization": "v_0=1",
        "candidate_data": candidate_data,
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
