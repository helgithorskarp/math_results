#!/usr/bin/env python3
"""Independent exact checker for the second order-23 record H-class.

The C++ checker separates the matrices by their complete 4-minor census.
This checker deliberately uses a different H-invariant: for every four-row
subset, it records the 23 column patterns modulo independent column signs,
then canonicalizes the eight-bin histogram under every signed permutation of
the four selected rows.  The multiset over all four-row subsets is preserved
by signed row and column permutations.
"""

from __future__ import annotations

import hashlib
import itertools
from collections import Counter
from pathlib import Path

from verify import bareiss_determinant, gram_matrix, read_record


HERE = Path(__file__).resolve().parent
ORDER = 23
RECORD = 2_779_447_296_000_000
BLOCKS = (
    ((7, 8), (9, 10)),
    ((3, 4), (5, 6)),
    ((11, 12), (13, 14)),
)
ROW_PERMUTATION = (
    0, 1, 2, 5, 6, 11, 12, 9, 10, 3, 4, 13,
    14, 7, 8, 15, 16, 17, 18, 19, 20, 21, 22,
)
ROW_SIGNS = (
    1, 1, 1, -1, -1, 1, 1, -1, -1, 1, 1, -1,
    -1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
)
COLUMN_PERMUTATION = (
    1, 2, 0, 5, 6, 11, 12, 9, 10, 3, 4, 13,
    14, 7, 8, 15, 16, 17, 18, 19, 20, 21, 22,
)
COLUMN_SIGNS = (
    1, 1, 1, 1, 1, -1, -1, 1, 1, -1, -1, 1,
    1, -1, -1, 1, 1, 1, 1, 1, 1, 1, 1,
)
PROFILE_HASHES = (
    "7c65ef560b5f9f212909c2bb8e982dfbee240ec989031fcbf4b752bff357c90b",
    "b5fd7c94de3fe7d27f7e9bf40054584a6710f8e322ac2237138586de8bc792c9",
)
DISTINGUISHING_SIGNATURE = (2, 3, 3, 2, 3, 3, 3, 4)


def read_second() -> list[list[int]]:
    lines = (HERE / "record23_class2.txt").read_text().splitlines()
    assert len(lines) == ORDER
    assert all(len(line) == ORDER and set(line) <= {"+", "-"} for line in lines)
    return [[1 if entry == "+" else -1 for entry in line] for line in lines]


def transpose(matrix: list[list[int]]) -> list[list[int]]:
    return [list(row) for row in zip(*matrix)]


def check_gram_map(
    source: list[list[int]],
    target: list[list[int]],
    permutation: tuple[int, ...],
    signs: tuple[int, ...],
) -> None:
    assert sorted(permutation) == list(range(ORDER))
    assert set(signs) <= {-1, 1}
    assert all(
        source[left][right]
        == signs[left]
        * signs[right]
        * target[permutation[left]][permutation[right]]
        for left in range(ORDER)
        for right in range(ORDER)
    )


def switched(
    base: list[list[int]], choices: tuple[tuple[int, int, int], ...]
) -> list[list[int]]:
    answer = [row[:] for row in base]
    for core, (block, column_kind, row_kind) in enumerate(choices):
        for column in BLOCKS[block][column_kind]:
            answer[core][column] *= -1
        for row in BLOCKS[block][row_kind]:
            answer[row][core] *= -1
    return answer


def pattern_actions() -> list[tuple[int, ...]]:
    actions = set()
    for permutation in itertools.permutations(range(4)):
        for sign_mask in range(16):
            image = []
            for word in range(16):
                transformed = sum(
                    (
                        ((word >> permutation[position]) & 1)
                        ^ ((sign_mask >> position) & 1)
                    )
                    << position
                    for position in range(4)
                )
                # A column negation complements all four signs, so its
                # projective pattern has the canonical label min(w,w xor 15).
                image.append(min(transformed, transformed ^ 15))
            actions.add(tuple(image))
    assert len(actions) == 192
    return sorted(actions)


def four_row_profile(matrix: list[list[int]]) -> Counter[tuple[int, ...]]:
    negative = [[entry < 0 for entry in row] for row in matrix]
    actions = pattern_actions()
    profile: Counter[tuple[int, ...]] = Counter()
    for rows in itertools.combinations(range(ORDER), 4):
        words = [
            sum(negative[rows[position]][column] << position for position in range(4))
            for column in range(ORDER)
        ]
        canonical = None
        for action in actions:
            histogram = [0] * 8
            for word in words:
                histogram[action[word]] += 1
            candidate = tuple(histogram)
            if canonical is None or candidate < canonical:
                canonical = candidate
        assert canonical is not None and sum(canonical) == ORDER
        profile[canonical] += 1
    assert sum(profile.values()) == 8_855
    return profile


def profile_hash(profile: Counter[tuple[int, ...]]) -> str:
    encoded = "".join(
        ",".join(map(str, signature)) + ":" + str(multiplicity) + "\n"
        for signature, multiplicity in sorted(profile.items())
    ).encode("ascii")
    return hashlib.sha256(encoded).hexdigest()


def main() -> None:
    base = read_record()
    second = read_second()
    assert abs(bareiss_determinant(base)) == RECORD
    assert abs(bareiss_determinant(second)) == RECORD
    assert sum(
        base[row][column] != second[row][column]
        for row in range(ORDER)
        for column in range(ORDER)
    ) == 12

    base_row_gram = gram_matrix(base)
    second_row_gram = gram_matrix(second)
    check_gram_map(second_row_gram, base_row_gram, ROW_PERMUTATION, ROW_SIGNS)
    check_gram_map(
        gram_matrix(transpose(second)),
        gram_matrix(transpose(base)),
        COLUMN_PERMUTATION,
        COLUMN_SIGNS,
    )

    stated_choice = ((1, 1, 0), (0, 1, 0), (2, 1, 0))
    assert switched(base, stated_choice) == second
    determinant_values = Counter()
    record_choices = []
    for encoded in itertools.product(range(12), repeat=3):
        choices = tuple(
            (value // 4, (value // 2) % 2, value % 2) for value in encoded
        )
        determinant = abs(bareiss_determinant(switched(base, choices)))
        determinant_values[determinant] += 1
        if determinant == RECORD:
            record_choices.append(choices)
    assert len(determinant_values) == 770
    assert max(determinant_values) == RECORD
    assert len(record_choices) == 2
    assert stated_choice in record_choices

    base_profile = four_row_profile(base)
    second_profile = four_row_profile(second)
    assert len(base_profile) == 29
    assert len(second_profile) == 31
    assert profile_hash(base_profile) == PROFILE_HASHES[0]
    assert profile_hash(second_profile) == PROFILE_HASHES[1]
    assert base_profile[DISTINGUISHING_SIGNATURE] == 2_508
    assert second_profile[DISTINGUISHING_SIGNATURE] == 2_460
    assert base_profile != second_profile

    print("exact determinants, 12-flip construction, and Gram maps verified")
    print("structured family: 1728 matrices, 770 determinant values, 2 records")
    print("four-row H-invariant multiplicity: 2508 versus 2460")
    print("the two record matrices are Hadamard-inequivalent")


if __name__ == "__main__":
    main()
