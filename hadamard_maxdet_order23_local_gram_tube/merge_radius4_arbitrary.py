#!/usr/bin/env python3
"""Merge and exactly classify a complete radius-four arbitrary-value cover."""

from __future__ import annotations

import hashlib
import heapq
import json
import math
import re
import sys
import tempfile
from pathlib import Path

from verify import PRIMES, bareiss_determinant, gram_matrix, read_record


HERE = Path(__file__).resolve().parent
EXPECTED_INTERNAL = 1_886_683
EXPECTED_ORBITS = 197_931
EXPECTED_EVALUATIONS = 1_979_310_000
ASSIGNMENTS_PER_REPRESENTATIVE = 10_000
COVERED_LABELED_MATRICES = math.comb(253, 4) * 10_000
RECORD = 2_779_447_296_000_000
LEGAL_VALUES = tuple(range(-21, 20, 4))
EXPECTED_PARTITIONS = ("4", "3+1", "2+2", "2+1+1", "1+1+1+1")


def inverse_numerator() -> tuple[int, list[list[int]]]:
    """Read the production inverse, then verify its defining identity exactly."""
    text = (HERE / "order23_inverse.hpp").read_text()
    scale_match = re.search(r"kScale\s*=\s*(\d+)", text)
    assert scale_match is not None
    scale = int(scale_match.group(1))
    block = text.split("kInverseNumerator", 1)[1].split(
        "inline constexpr std::array", 1
    )[0]
    values = [int(item) for item in re.findall(r"-?\d+", block)]
    assert len(values) == 23 * 23
    numerator = [values[23 * row : 23 * (row + 1)] for row in range(23)]
    gram = gram_matrix(read_record())
    assert all(
        sum(gram[row][middle] * numerator[middle][column] for middle in range(23))
        == scale * int(row == column)
        for row in range(23)
        for column in range(23)
    )
    return scale, numerator


def encoding_key(edits: tuple[tuple[int, int], ...]) -> str:
    """Fixed-width key whose lexical order is the edit tuple order."""
    value_indices = {value: index for index, value in enumerate(LEGAL_VALUES)}
    edge_key = ",".join(f"{edge:03d}" for edge, _ in edits)
    value_key = ",".join(f"{value_indices[value]:02d}" for _, value in edits)
    return edge_key + "|" + value_key


def exact_determinant(
    edits: tuple[tuple[int, int], ...],
    edges: tuple[tuple[int, int, int], ...],
    scale: int,
    inverse: list[list[int]],
) -> int:
    vertices = sorted({vertex for edge, _ in edits for vertex in edges[edge][:2]})
    positions = {vertex: index for index, vertex in enumerate(vertices)}
    size = len(vertices)
    perturbation = [[0] * size for _ in range(size)]
    for edge_index, value in edits:
        left, right, old_value = edges[edge_index]
        delta = value - old_value
        left_position = positions[left]
        right_position = positions[right]
        perturbation[left_position][right_position] = delta
        perturbation[right_position][left_position] = delta
    update = [
        [
            scale * int(row == column)
            + sum(
                inverse[vertices[row]][vertices[middle]]
                * perturbation[middle][column]
                for middle in range(size)
            )
            for column in range(size)
        ]
        for row in range(size)
    ]
    numerator = bareiss_determinant(update)
    scaled = RECORD * RECORD * numerator
    denominator = scale**size
    assert scaled % denominator == 0
    return scaled // denominator


def positive_definiteness_witness(
    matrix: list[list[int]],
) -> tuple[bool, int | None, int | None]:
    """Return exact Sylvester status and the first nonpositive leading minor."""
    work = [row[:] for row in matrix]
    previous = 1
    for column in range(len(work)):
        pivot = work[column][column]
        if pivot <= 0:
            return False, column + 1, pivot
        if column + 1 == len(work):
            return True, None, None
        for row in range(column + 1, len(work)):
            for other in range(column + 1, len(work)):
                numerator = (
                    work[row][other] * pivot
                    - work[row][column] * work[column][other]
                )
                assert numerator % previous == 0
                work[row][other] = numerator // previous
        previous = pivot
    raise AssertionError("unreachable")


def candidate_matrix(
    gram: list[list[int]],
    edges: tuple[tuple[int, int, int], ...],
    edits: tuple[tuple[int, int], ...],
) -> list[list[int]]:
    answer = [row[:] for row in gram]
    for edge_index, value in edits:
        left, right, _ = edges[edge_index]
        answer[left][right] = answer[right][left] = value
    return answer


def normalized_edits(
    item: list[list[int]], edges: tuple[tuple[int, int, int], ...]
) -> tuple[tuple[int, int], ...]:
    edits = tuple((int(edge), int(value)) for edge, value in item)
    indices = tuple(edge for edge, _ in edits)
    assert len(edits) == 4
    assert indices == tuple(sorted(indices)) and len(set(indices)) == 4
    assert all(0 <= edge < 253 for edge in indices)
    assert all(value in LEGAL_VALUES for _, value in edits)
    assert all(value != edges[edge][2] for edge, value in edits)
    return edits


def main() -> None:
    if len(sys.argv) < 2:
        raise SystemExit(
            "usage: python3 merge_radius4_arbitrary.py [-o RESULT.json] "
            "PART.json [...]"
        )
    arguments = sys.argv[1:]
    output_path = None
    if arguments[:1] == ["-o"]:
        if len(arguments) < 3:
            raise SystemExit("-o requires an output path and shard paths")
        output_path = Path(arguments[1])
        arguments = arguments[2:]
    paths = [Path(argument) for argument in arguments]

    gram = gram_matrix(read_record())
    assert bareiss_determinant(gram) == RECORD**2
    edges = tuple(
        (left, right, gram[left][right])
        for left in range(23)
        for right in range(left)
    )
    scale, inverse = inverse_numerator()

    shard_count: int | None = None
    observed_shards: set[int] = set()
    fixed_metadata: tuple | None = None
    partition_totals = {
        name: {"internally_colored_graphs": 0, "underlying_edit_set_orbits": 0}
        for name in EXPECTED_PARTITIONS
    }
    total_internal = 0
    total_orbits = 0
    total_evaluations = 0
    witness_counts = [0] * len(PRIMES)
    modular_survivors = 0
    exact_negative = 0
    exact_nonsquare = 0
    square_below = 0
    square_equal = 0
    square_above = 0
    largest_below = 0
    positive_definite_above = []
    equal_record_edits = []
    above_record_edits = []
    classified = 0

    with tempfile.TemporaryDirectory(prefix="radius4-arbitrary-merge-") as temporary:
        temporary_path = Path(temporary)
        survivor_stream_paths = []
        square_stream_paths = []
        above_stream_paths = []

        for path in paths:
            part = json.loads(path.read_text())
            assert part["schema"] == "radius4-arbitrary-shard-v1"
            current_shard_count = int(part["shard_count"])
            if shard_count is None:
                shard_count = current_shard_count
            assert current_shard_count == shard_count
            shard = int(part["shard"])
            assert 0 <= shard < shard_count and shard not in observed_shards
            observed_shards.add(shard)
            metadata = (
                part["order"],
                part["radius"],
                part["expected_global_internally_colored"],
                part["expected_global_underlying_edit_set_orbits"],
                part["expected_global_normalized_cover_evaluations"],
                part["connected_shapes_through_four"],
                part["colored_connected_variants_through_four"],
                tuple(part["legal_values"]),
                part["value_assignments_per_representative"],
                part["covered_labeled_matrices"],
                tuple(part["witness_primes"]),
                part["record_threshold"],
            )
            if fixed_metadata is None:
                fixed_metadata = metadata
            assert metadata == fixed_metadata
            assert metadata == (
                23,
                4,
                EXPECTED_INTERNAL,
                EXPECTED_ORBITS,
                EXPECTED_EVALUATIONS,
                10,
                152_305,
                LEGAL_VALUES,
                ASSIGNMENTS_PER_REPRESENTATIVE,
                COVERED_LABELED_MATRICES,
                PRIMES,
                RECORD,
            )

            partitions = part["partitions"]
            assert tuple(item["partition"] for item in partitions) == EXPECTED_PARTITIONS
            part_internal = sum(item["internally_colored_graphs"] for item in partitions)
            part_orbits = sum(item["underlying_edit_set_orbits"] for item in partitions)
            assert part_internal == part["internally_colored_underlying_graphs"]
            assert part_orbits == part["underlying_edit_set_orbits"]
            assert part["normalized_cover_evaluations"] == (
                part_orbits * ASSIGNMENTS_PER_REPRESENTATIVE
            )
            for item in partitions:
                totals = partition_totals[item["partition"]]
                totals["internally_colored_graphs"] += item[
                    "internally_colored_graphs"
                ]
                totals["underlying_edit_set_orbits"] += item[
                    "underlying_edit_set_orbits"
                ]
            total_internal += part_internal
            total_orbits += part_orbits
            total_evaluations += part["normalized_cover_evaluations"]
            for index, count in enumerate(part["witness_counts"]):
                witness_counts[index] += count

            items = part["survivor_edits"]
            assert len(items) == part["survives_48_nonsquare_tests"]
            assert sum(part["witness_counts"]) + len(items) == part[
                "normalized_cover_evaluations"
            ]
            modular_survivors += len(items)
            survivor_path = temporary_path / f"survivors-{shard:06d}.txt"
            square_path = temporary_path / f"squares-{shard:06d}.txt"
            above_path = temporary_path / f"above-{shard:06d}.txt"
            survivor_stream_paths.append(survivor_path)
            square_stream_paths.append(square_path)
            above_stream_paths.append(above_path)
            previous_key = None
            with (
                survivor_path.open("w") as survivor_stream,
                square_path.open("w") as square_stream,
                above_path.open("w") as above_stream,
            ):
                for item in items:
                    edits = normalized_edits(item, edges)
                    key = encoding_key(edits)
                    assert previous_key is None or previous_key < key
                    previous_key = key
                    survivor_stream.write(key + "\n")
                    determinant = exact_determinant(edits, edges, scale, inverse)
                    classified += 1
                    if determinant < 0:
                        exact_negative += 1
                    else:
                        root = math.isqrt(determinant)
                        if root * root != determinant:
                            exact_nonsquare += 1
                        else:
                            square_stream.write(f"{key}|{root}\n")
                            if root < RECORD:
                                square_below += 1
                                largest_below = max(largest_below, root)
                            elif root == RECORD:
                                square_equal += 1
                                equal_record_edits.append(
                                    {
                                        "edits": [list(edit) for edit in edits],
                                        "square_root": root,
                                        "determinant": determinant,
                                    }
                                )
                            else:
                                square_above += 1
                                above_stream.write(f"{key}|{root}\n")
                                matrix = candidate_matrix(gram, edges, edits)
                                is_positive, failed_order, failed_minor = (
                                    positive_definiteness_witness(matrix)
                                )
                                threat = {
                                    "edits": [list(edit) for edit in edits],
                                    "square_root": root,
                                    "determinant": determinant,
                                    "positive_definite": is_positive,
                                }
                                if not is_positive:
                                    threat["first_nonpositive_leading_principal_order"] = (
                                        failed_order
                                    )
                                    threat["first_nonpositive_leading_principal_minor"] = (
                                        failed_minor
                                    )
                                above_record_edits.append(threat)
                                if is_positive:
                                    positive_definite_above.append(
                                        {
                                            "edits": [list(edit) for edit in edits],
                                            "square_root": root,
                                            "determinant": determinant,
                                        }
                                    )
                    if classified % 100_000 == 0:
                        print(
                            f"classified {classified:,} modular survivors",
                            file=sys.stderr,
                        )
            print(
                f"processed shard {shard}/{shard_count}: "
                f"{part_orbits:,} representatives, {len(items):,} survivors",
                file=sys.stderr,
            )
            del part, items

        assert shard_count is not None
        assert len(paths) == shard_count
        assert observed_shards == set(range(shard_count))
        assert total_internal == EXPECTED_INTERNAL
        assert total_orbits == EXPECTED_ORBITS
        assert total_evaluations == EXPECTED_EVALUATIONS
        assert sum(witness_counts) + modular_survivors == total_evaluations
        assert classified == modular_survivors

        survivor_digest = hashlib.sha256()
        square_digest = hashlib.sha256()
        above_digest = hashlib.sha256()
        for stream_paths, digest, expected_count in (
            (survivor_stream_paths, survivor_digest, modular_survivors),
            (square_stream_paths, square_digest, square_below + square_equal + square_above),
            (above_stream_paths, above_digest, square_above),
        ):
            streams = [path.open() for path in stream_paths]
            previous = None
            count = 0
            try:
                for line in heapq.merge(*streams):
                    assert previous is None or previous < line
                    previous = line
                    digest.update(line.encode("ascii"))
                    count += 1
            finally:
                for stream in streams:
                    stream.close()
            assert count == expected_count

    positive_definite_above.sort(
        key=lambda item: tuple(tuple(edit) for edit in item["edits"])
    )
    equal_record_edits.sort(
        key=lambda item: tuple(tuple(edit) for edit in item["edits"])
    )
    above_record_edits.sort(
        key=lambda item: tuple(tuple(edit) for edit in item["edits"])
    )
    result = {
        "schema": "radius4-arbitrary-certificate-v1",
        "order": 23,
        "radius": 4,
        "shard_count": shard_count,
        "legal_values": list(LEGAL_VALUES),
        "value_assignments_per_representative": ASSIGNMENTS_PER_REPRESENTATIVE,
        "covered_labeled_matrices": COVERED_LABELED_MATRICES,
        "connected_shapes_through_four": 10,
        "colored_connected_variants_through_four": 152_305,
        "partitions": [
            {"partition": name, **partition_totals[name]}
            for name in EXPECTED_PARTITIONS
        ],
        "internally_colored_underlying_graphs": total_internal,
        "underlying_edit_set_orbits": total_orbits,
        "normalized_cover_evaluations": total_evaluations,
        "witness_primes": list(PRIMES),
        "witness_counts": witness_counts,
        "survives_48_nonsquare_tests": modular_survivors,
        "survivor_encoding_sha256": survivor_digest.hexdigest(),
        "exact_negative_determinants": exact_negative,
        "exact_nonnegative_nonsquares": exact_nonsquare,
        "exact_squares_below_record": square_below,
        "largest_square_root_below_record": largest_below,
        "exact_squares_equal_record": square_equal,
        "record_equal_square_edits": equal_record_edits,
        "exact_squares_above_record": square_above,
        "square_encoding_and_root_sha256": square_digest.hexdigest(),
        "above_record_encoding_and_root_sha256": above_digest.hexdigest(),
        "record_threshold": RECORD,
        "above_record_square_edits": above_record_edits,
        "positive_definite_squares_above_record": len(positive_definite_above),
        "positive_definite_above_record_edits": positive_definite_above,
    }
    assert (
        exact_negative
        + exact_nonsquare
        + square_below
        + square_equal
        + square_above
        == modular_survivors
    )
    encoded = json.dumps(result, indent=2) + "\n"
    if output_path is None:
        sys.stdout.write(encoded)
    else:
        output_path.write_text(encoded)
        print(f"wrote {output_path}")


if __name__ == "__main__":
    main()
