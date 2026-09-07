#!/usr/bin/env python3
"""Independent structural audit of the all-row support-at-most-eight CNF."""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
from itertools import combinations
import argparse
import json
from pathlib import Path


N = 43
A_SIZE = 20
B_SIZE = 23
TASKS = 10959
FIVE_SETS = 962598
COVER_HASH = "bd1161b4261eb1ee3f8bc2cd0104a062c858bf38d596cf725acbfb195b158bac"


def file_sha256(path: Path) -> str:
    digest = sha256()
    with path.open("rb") as handle:
        while chunk := handle.read(1024 * 1024):
            digest.update(chunk)
    return digest.hexdigest()


def rank(values: list[int]) -> int:
    pivots: dict[int, int] = {}
    for value in values:
        while value:
            pivot = value.bit_length() - 1
            if pivot in pivots:
                value ^= pivots[pivot]
            else:
                pivots[pivot] = value
                break
    return len(pivots)


def cover_audit(path: Path) -> dict:
    if file_sha256(path) != COVER_HASH:
        raise AssertionError("cover hash")
    lines = path.read_text(encoding="ascii").splitlines()
    if lines[0] != "code\tzero\torbit_size\tsupport\ttriples" or len(lines) != TASKS + 1:
        raise AssertionError("cover shape")
    previous = -1
    mass = 0
    equal_pairs = 0
    zero_tasks = 0
    row_windows = {(first, first + distance)
                   for distance in (1, 2) for first in range(A_SIZE - distance)}
    codes = []
    for line in lines[1:]:
        code, zero, orbit_size, support, triples = map(int, line.split("\t"))
        counts = [(code >> (2 * value)) & 3 for value in range(15)]
        inferred_zero = 20 - sum(counts)
        rows = [0] * inferred_zero + [
            value for value in range(1, 16) for _ in range(counts[value - 1])
        ]
        populations = Counter(rows)
        if not (
            previous < code < 2**30
            and inferred_zero in (0, 1)
            and zero == inferred_zero
            and len(rows) == A_SIZE
            and rows == sorted(rows)
            and rank(rows) == 4
            and max(populations.values()) <= 3
            and support == sum(count > 0 for count in counts)
            and triples == sum(count == 3 for count in counts)
            and orbit_size > 0
            and 20160 % orbit_size == 0
        ):
            raise AssertionError(f"cover row {code}")
        for first, second in combinations(range(A_SIZE), 2):
            if rows[first] == rows[second]:
                equal_pairs += 1
                if (first, second) not in row_windows:
                    raise AssertionError("row window misses equal pair")
        previous = code
        mass += orbit_size
        zero_tasks += zero
        codes.append(code)
    if mass != 154847637 or zero_tasks != 5109:
        raise AssertionError("cover aggregates")
    return {
        "sha256": COVER_HASH,
        "tasks": TASKS,
        "covered_row_profiles": mass,
        "zero_tasks": zero_tasks,
        "equal_row_pairs_across_tasks": equal_pairs,
        "codes": codes,
    }


def sinz_variables(n: int, bound: int) -> int:
    if bound >= n or bound <= 0:
        return 0
    return (n - 1) * bound


def sinz_clauses(n: int, bound: int) -> int:
    if bound >= n:
        return 0
    if bound < 0:
        return 1
    if bound == 0:
        return n
    return bound + (n - 2) * (2 * bound) + (n - 1)


def expected_dimensions() -> tuple[dict[str, dict[str, int]], int, int]:
    row_pairs = sum(A_SIZE - distance for distance in (1, 2))
    column_pairs = sum(B_SIZE - distance for distance in (1, 2, 3, 4))
    blocks = {
        "canonical_row_selector": {
            "variables": TASKS + sinz_variables(TASKS, 1) + A_SIZE * 16,
            "clauses": 1 + sinz_clauses(TASKS, 1)
                       + A_SIZE * (16 * 15 // 2) + TASKS * A_SIZE,
        },
        "physical_edges": {"variables": 43 * 42 // 2, "clauses": 0},
        "column_labels_caps_support_span": {
            "variables": B_SIZE * 16 + 16 + sinz_variables(16, 8),
            "clauses": B_SIZE * (1 + 16 * 15 // 2)
                       + (B_SIZE - 1) * (16 * 15 // 2)
                       + (B_SIZE - 2) + 15 * (B_SIZE - 5)
                       + 16 * (B_SIZE + 1) + sinz_clauses(16, 8)
                       + 1 + 15,
        },
        "dot_product_cross_edges": {
            "variables": 15 * B_SIZE,
            "clauses": 15 * B_SIZE * 16 + A_SIZE * B_SIZE * (1 + 2 * 15),
        },
        "complement_rank_four": {"variables": 0, "clauses": 15 * 8},
        "tripled_row_contacts": {
            "variables": 15 * ((A_SIZE - 2) + 1
                               + 2 * sinz_variables(B_SIZE, 13)),
            "clauses": 15 * ((A_SIZE - 2) * 3 + (A_SIZE - 2 + 1)
                             + 2 * sinz_clauses(B_SIZE, 13)),
        },
        "equal_label_pair_distances": {
            "variables": row_pairs * (1 + (A_SIZE - 2)
                                      + sinz_variables(A_SIZE - 2, A_SIZE - 2 - 8))
                         + column_pairs * (1 + (B_SIZE - 2)
                                         + sinz_variables(B_SIZE - 2, B_SIZE - 2 - 8)),
            "clauses": row_pairs * (16 + 4 * (A_SIZE - 2)
                                    + sinz_clauses(A_SIZE - 2, A_SIZE - 2 - 8))
                       + column_pairs * (16 + 4 * (B_SIZE - 2)
                                       + sinz_clauses(B_SIZE - 2, B_SIZE - 2 - 8)),
        },
        "degree_18_24": {
            "variables": N * (sinz_variables(N - 1, (N - 1) - 18)
                              + sinz_variables(N - 1, 24)),
            "clauses": N * (sinz_clauses(N - 1, (N - 1) - 18)
                            + sinz_clauses(N - 1, 24)),
        },
        "physical_five_sets": {"variables": 0, "clauses": 2 * FIVE_SETS},
    }
    variables = sum(block["variables"] for block in blocks.values())
    clauses = sum(block["clauses"] for block in blocks.values())
    return blocks, variables, clauses


def physical_map(metadata: dict) -> dict[tuple[int, int], int]:
    result = {}
    for category in ("internal_variables", "cross_variables"):
        for key, variable in metadata["maps"][category].items():
            edge = tuple(map(int, key.split(",")))
            if len(edge) != 2 or not 0 <= edge[0] < edge[1] < N or edge in result:
                raise AssertionError("physical edge map")
            result[edge] = variable
    if set(result) != set(combinations(range(N), 2)) or len(set(result.values())) != 903:
        raise AssertionError("physical map coverage")
    return result


def dimacs_audit(path: Path, metadata: dict, expected_clauses: int,
                 edge_variables: dict[tuple[int, int], int]) -> dict:
    digest = file_sha256(path)
    if digest != metadata["formula"]["sha256"]:
        raise AssertionError("CNF hash")
    histogram: Counter[int] = Counter()
    five_iterator = iter(combinations(range(N), 5))
    current_edges = None
    target_start = expected_clauses - 2 * FIVE_SETS
    with path.open("r", encoding="ascii") as handle:
        header = handle.readline().split()
        if header[:2] != ["p", "cnf"] or len(header) != 4:
            raise AssertionError("DIMACS header")
        variables, declared_clauses = map(int, header[2:])
        if variables != metadata["formula"]["variables"] or declared_clauses != expected_clauses:
            raise AssertionError("DIMACS dimensions")
        seen_clauses = 0
        for line in handle:
            tokens = list(map(int, line.split()))
            if not tokens or tokens[-1] != 0 or any(value == 0 for value in tokens[:-1]):
                raise AssertionError("DIMACS clause syntax")
            clause = tuple(tokens[:-1])
            if len(set(clause)) != len(clause) or any(-literal in clause for literal in clause):
                raise AssertionError("noncanonical clause")
            if any(not 1 <= abs(literal) <= variables for literal in clause):
                raise AssertionError("literal range")
            histogram[len(clause)] += 1
            if seen_clauses >= target_start:
                offset = seen_clauses - target_start
                if offset % 2 == 0:
                    vertices = next(five_iterator)
                    current_edges = tuple(edge_variables[edge]
                                          for edge in combinations(vertices, 2))
                    expected = current_edges
                else:
                    expected = tuple(-edge for edge in current_edges)
                if clause != expected:
                    raise AssertionError(("physical five-set clause", offset, clause, expected))
            seen_clauses += 1
        if seen_clauses != expected_clauses:
            raise AssertionError("clause count")
        try:
            next(five_iterator)
            raise AssertionError("unread five-set")
        except StopIteration:
            pass
    stored_histogram = {int(length): count
                        for length, count in metadata["formula"]["clause_length_histogram"].items()}
    if dict(histogram) != stored_histogram:
        raise AssertionError("clause histogram")
    return {
        "sha256": digest,
        "bytes": path.stat().st_size,
        "variables": variables,
        "clauses": seen_clauses,
        "literal_five_set_clauses": 2 * FIVE_SETS,
        "clause_length_histogram": dict(sorted(histogram.items())),
    }


def metadata_audit(metadata: dict, cover: dict) -> dict:
    blocks, variables, clauses = expected_dimensions()
    if metadata["blocks"] != blocks:
        raise AssertionError(("block dimensions", metadata["blocks"], blocks))
    if metadata["formula"]["variables"] != variables or metadata["formula"]["clauses"] != clauses:
        raise AssertionError("formula aggregate dimensions")
    if metadata["cover"]["sha256"] != COVER_HASH:
        raise AssertionError("metadata cover hash")
    if metadata["cover"]["row_codes"] != cover["codes"]:
        raise AssertionError("metadata row codes")
    selectors = metadata["cover"]["selector_variables"]
    if len(selectors) != TASKS or len(set(selectors)) != TASKS:
        raise AssertionError("selector map")
    row_labels = metadata["maps"]["row_label_variables"]
    column_labels = metadata["maps"]["column_label_variables"]
    if len(row_labels) != A_SIZE or any(len(row) != 16 for row in row_labels):
        raise AssertionError("row-label map")
    if len(column_labels) != B_SIZE or any(len(row) != 16 for row in column_labels):
        raise AssertionError("column-label map")
    if len(metadata["maps"]["support_variables"]) != 16:
        raise AssertionError("support map")
    if metadata["rank_guard_pairs"] != 120:
        raise AssertionError("rank guard")
    row_pairs = {tuple(pair) for pair in metadata["optimized_pair_windows"]["row_pairs"]}
    column_pairs = {tuple(pair) for pair in metadata["optimized_pair_windows"]["column_pairs"]}
    if row_pairs != {(first, first + distance)
                     for distance in (1, 2) for first in range(A_SIZE - distance)}:
        raise AssertionError("row pair windows")
    if column_pairs != {(first, first + distance)
                        for distance in (1, 2, 3, 4)
                        for first in range(B_SIZE - distance)}:
        raise AssertionError("column pair windows")
    return {"blocks": blocks, "variables": variables, "clauses": clauses}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cover", type=Path, required=True)
    parser.add_argument("--cnf", type=Path, required=True)
    parser.add_argument("--metadata", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    metadata = json.loads(args.metadata.read_text())
    cover = cover_audit(args.cover)
    dimensions = metadata_audit(metadata, cover)
    edges = physical_map(metadata)
    formula = dimacs_audit(args.cnf, metadata, dimensions["clauses"], edges)
    result = {
        "status": "INDEPENDENT_AUDIT_ALL_ROW_SUPPORT8_PHYSICAL_FORMULA",
        "cover": {key: value for key, value in cover.items() if key != "codes"},
        "dimensions": dimensions,
        "formula": formula,
        "physical_edges": len(edges),
        "physical_five_sets": FIVE_SETS,
    }
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
