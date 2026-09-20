#!/usr/bin/env python3
"""Definition-level checks for the compact order-12 census certificate."""

from __future__ import annotations

import csv
import hashlib
import sys
from fractions import Fraction
from pathlib import Path


HERE = Path(__file__).resolve().parent
PUBLISHED_G14 = "Ml_GGCHO??_@?@?C_"


def decode_graph6(record: str) -> tuple[int, list[tuple[int, int]]]:
    if record.startswith(">>graph6<<"):
        record = record[10:]
    if not record:
        raise ValueError("empty graph6 record")
    order = ord(record[0]) - 63
    expected = 1 + (order * (order - 1) // 2 + 5) // 6
    if not 0 <= order <= 62 or len(record) != expected:
        raise ValueError(f"invalid short graph6 record: {record!r}")
    bits: list[int] = []
    for character in record[1:]:
        value = ord(character) - 63
        if not 0 <= value <= 63:
            raise ValueError("invalid graph6 character")
        bits.extend((value >> shift) & 1 for shift in range(5, -1, -1))
    edges: list[tuple[int, int]] = []
    cursor = 0
    for j in range(1, order):
        for i in range(j):
            if bits[cursor]:
                edges.append((i, j))
            cursor += 1
    return order, edges


def symmetric_swap(matrix: list[list[Fraction]], a: int, b: int) -> None:
    if a == b:
        return
    matrix[a], matrix[b] = matrix[b], matrix[a]
    for row in matrix:
        row[a], row[b] = row[b], row[a]


def exact_inertia(matrix: list[list[int]]) -> tuple[int, int, int]:
    work = [[Fraction(value) for value in row] for row in matrix]
    positive = zero = negative = 0
    k = 0
    while k < len(work):
        pivot_index = next((i for i in range(k, len(work)) if work[i][i]), None)
        if pivot_index is not None:
            symmetric_swap(work, k, pivot_index)
            pivot = work[k][k]
            positive += pivot > 0
            negative += pivot < 0
            for i in range(k + 1, len(work)):
                for j in range(i, len(work)):
                    work[i][j] -= work[i][k] * work[k][j] / pivot
                    work[j][i] = work[i][j]
            k += 1
            continue
        off_diagonal = next(
            (
                (i, j)
                for i in range(k, len(work))
                for j in range(i + 1, len(work))
                if work[i][j]
            ),
            None,
        )
        if off_diagonal is None:
            zero += len(work) - k
            break
        row, column = off_diagonal
        symmetric_swap(work, k, row)
        if column == k:
            column = row
        symmetric_swap(work, k + 1, column)
        pivot = work[k][k + 1]
        if work[k][k] or work[k + 1][k + 1] or not pivot:
            raise AssertionError("invalid 2-by-2 pivot")
        positive += 1
        negative += 1
        for i in range(k + 2, len(work)):
            for j in range(i, len(work)):
                work[i][j] -= (
                    work[i][k] * work[k + 1][j]
                    + work[i][k + 1] * work[k][j]
                ) / pivot
                work[j][i] = work[i][j]
        k += 2
    return positive, zero, negative


def line_signature(record: str) -> tuple[int, int, tuple[int, int, int]]:
    order, edges = decode_graph6(record)
    matrix = [[0] * len(edges) for _ in edges]
    for i, first in enumerate(edges):
        for j in range(i):
            second = edges[j]
            if first[0] in second or first[1] in second:
                matrix[i][j] = matrix[j][i] = 1
    inertia = exact_inertia(matrix)
    return order, len(edges), (inertia[0] - inertia[2], *inertia)


def parse_manifest() -> list[dict[str, str]]:
    with (HERE / "SHARD_MANIFEST.tsv").open(encoding="ascii", newline="") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    if [int(row["edges"]) for row in rows] != list(range(12, 23)):
        raise AssertionError("manifest edge shards are not exactly 12 through 22")
    return rows


def check_aggregate(rows: list[dict[str, str]]) -> None:
    lines = (HERE / "EXPECTED_OUTPUT.txt").read_text(encoding="ascii").splitlines()
    header = dict(field.split("=") for field in lines[0].split())
    if header != {
        "graphs": "308913398",
        "fallbacks": "5354397",
        "counterexamples": "0",
    }:
        raise AssertionError("unexpected aggregate header")
    if sum(int(row["graphs"]) for row in rows) != int(header["graphs"]):
        raise AssertionError("manifest graph total mismatch")
    if sum(int(row["fallbacks"]) for row in rows) != int(header["fallbacks"]):
        raise AssertionError("manifest fallback total mismatch")
    signature_total = sum(
        int(line.rsplit("=", 1)[1])
        for line in lines
        if line.startswith("signature ")
    )
    if signature_total != int(header["graphs"]):
        raise AssertionError("signature histogram total mismatch")
    if lines[-1] != "maximum_signature=1 maximizers=39":
        raise AssertionError("unexpected aggregate maximum")


def check_shard_outputs(rows: list[dict[str, str]], directory: Path) -> None:
    for row in rows:
        path = directory / f"result_m{row['edges']}.txt"
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        if digest != row["sha256"]:
            raise AssertionError(f"hash mismatch for {path}")
    print(f"shard outputs: hashes valid in {directory}")


def main() -> None:
    rows = parse_manifest()
    check_aggregate(rows)
    for row in rows:
        order, edges, signature_inertia = line_signature(row["first_maximizer"])
        signature, positive, zero, negative = signature_inertia
        if (order, edges, signature) != (
            12,
            int(row["edges"]),
            int(row["maximum_signature"]),
        ):
            raise AssertionError(f"bad shard maximizer at m={row['edges']}")
        print(
            f"m={edges} witness={row['first_maximizer']} "
            f"line_inertia=({positive},{zero},{negative}) signature={signature}"
        )
    order, edges, signature_inertia = line_signature(PUBLISHED_G14)
    if (order, edges, signature_inertia) != (14, 16, (2, 9, 0, 7)):
        raise AssertionError("published order-14 witness check failed")
    print(f"published upper-bound witness: order={order} edges={edges} inertia=(9,0,7)")
    print("aggregate: graphs=308913398 maximum_signature=1 status=VERIFIED")

    if len(sys.argv) == 3 and sys.argv[1] == "--results-dir":
        check_shard_outputs(rows, Path(sys.argv[2]))
    elif len(sys.argv) != 1:
        raise SystemExit("usage: verify_certificate.py [--results-dir DIRECTORY]")


if __name__ == "__main__":
    main()
