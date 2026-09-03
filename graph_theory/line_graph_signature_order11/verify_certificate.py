#!/usr/bin/env python3
"""Definition-level checks for compact order-10/11 line-graph certificates."""

from __future__ import annotations

import hashlib
import sys
from fractions import Fraction
from pathlib import Path


HERE = Path(__file__).resolve().parent

EXPECTED_HASHES = {
    "expected_n3_n9.txt": "dcee24d8a53c3c5df474dc046dd21545c754acab5e0c8d155f91220104fc7139",
    "expected_n10.txt": "5567d30204ddee6550712ffe6693afb9ed73dc9da5212fc556ae8ce6af224aab",
    "expected_n11.txt": "32b42a4bb2b16f94a7140c48143a947dd1cc9ebc63ec1814ddbcc05dd1b11eaf",
}

WITNESSES = {
    "order10_maximizer": ("I?AA@ow}?", 1, 3),
    "order11_maximizer": ("J??E@owpDo?", 1, 4),
    "published_G14_counterexample": ("Ml_GGCHO??_@?@?C_", 2, 0),
}


def decode_graph6(record: str) -> list[tuple[int, int]]:
    """Decode the short graph6 format (orders at most 62)."""
    if record.startswith(">>graph6<<"):
        record = record[10:]
    if not record:
        raise ValueError("empty graph6 record")
    n = ord(record[0]) - 63
    expected = 1 + (n * (n - 1) // 2 + 5) // 6
    if not (0 <= n <= 62 and len(record) == expected):
        raise ValueError("invalid short graph6 record")
    bits = []
    for character in record[1:]:
        value = ord(character) - 63
        if not 0 <= value <= 63:
            raise ValueError("invalid graph6 character")
        bits.extend((value >> shift) & 1 for shift in range(5, -1, -1))
    edges = []
    cursor = 0
    for j in range(1, n):
        for i in range(j):
            if bits[cursor]:
                edges.append((i, j))
            cursor += 1
    return edges


def swap_symmetric(matrix: list[list[Fraction]], a: int, b: int) -> None:
    if a == b:
        return
    matrix[a], matrix[b] = matrix[b], matrix[a]
    for row in matrix:
        row[a], row[b] = row[b], row[a]


def exact_inertia(matrix: list[list[int]]) -> tuple[int, int, int]:
    """Exact rational congruence reduction with 1x1 and 2x2 pivots."""
    work = [[Fraction(value) for value in row] for row in matrix]
    n = len(work)
    positive = zero = negative = 0
    k = 0
    while k < n:
        pivot_index = next((i for i in range(k, n) if work[i][i]), None)
        if pivot_index is not None:
            swap_symmetric(work, k, pivot_index)
            pivot = work[k][k]
            if pivot > 0:
                positive += 1
            else:
                negative += 1
            for i in range(k + 1, n):
                for j in range(i, n):
                    work[i][j] -= work[i][k] * work[k][j] / pivot
                    work[j][i] = work[i][j]
            k += 1
            continue

        off_diagonal = next(
            ((i, j) for i in range(k, n) for j in range(i + 1, n) if work[i][j]),
            None,
        )
        if off_diagonal is None:
            zero += n - k
            break
        row, column = off_diagonal
        swap_symmetric(work, k, row)
        if column == k:
            column = row
        swap_symmetric(work, k + 1, column)
        pivot = work[k][k + 1]
        if work[k][k] or work[k + 1][k + 1] or not pivot:
            raise AssertionError("bad 2x2 pivot")
        positive += 1
        negative += 1
        for i in range(k + 2, n):
            for j in range(i, n):
                work[i][j] -= (
                    work[i][k] * work[k + 1][j]
                    + work[i][k + 1] * work[k][j]
                ) / pivot
                work[j][i] = work[i][j]
        k += 2
    return positive, zero, negative


def line_graph_matrix(edges: list[tuple[int, int]]) -> list[list[int]]:
    order = len(edges)
    matrix = [[0] * order for _ in range(order)]
    for i, first in enumerate(edges):
        for j in range(i):
            second = edges[j]
            if first[0] in second or first[1] in second:
                matrix[i][j] = matrix[j][i] = 1
    return matrix


def parse_summary(path: Path) -> None:
    lines = path.read_text(encoding="ascii").splitlines()
    header = dict(field.split("=") for field in lines[0].split())
    if header["counterexamples"] != "0":
        raise AssertionError(f"nonzero counterexample count in {path.name}")
    if header["sharp_bound_violations"] != "0":
        raise AssertionError(f"sharp-bound violation in {path.name}")
    graphs = int(header["graphs"])
    edge_total = sum(
        int(line.rsplit("=", 1)[1]) for line in lines if line.startswith("order_edges ")
    )
    signature_total = sum(
        int(line.rsplit("=", 1)[1]) for line in lines if line.startswith("signature ")
    )
    if edge_total != graphs or signature_total != graphs:
        raise AssertionError(f"inconsistent totals in {path.name}")
    if not lines[-1].startswith("maximum_signature=1 "):
        raise AssertionError(f"unexpected maximum in {path.name}")
    for line in lines:
        if line.startswith("cyclomatic ") and int(line.rsplit("=", 1)[1]) < 0:
            raise AssertionError(f"negative sharp-bound slack in {path.name}")


def main() -> None:
    if sys.argv[1:] == ["--stream"]:
        for raw_record in sys.stdin:
            graph6 = raw_record.strip()
            if not graph6:
                continue
            edges = decode_graph6(graph6)
            inertia = exact_inertia(line_graph_matrix(edges))
            print(f"{graph6}\t{inertia[0] - inertia[2]}")
        return
    if sys.argv[1:]:
        raise SystemExit("usage: verify_certificate.py [--stream]")

    for filename, expected_hash in EXPECTED_HASHES.items():
        path = HERE / filename
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        if digest != expected_hash:
            raise AssertionError(f"hash mismatch for {filename}: {digest}")
        parse_summary(path)
        print(f"summary {filename}: sha256={digest} totals=valid maximum=1")

    for name, (graph6, expected_signature, expected_slack) in WITNESSES.items():
        edges = decode_graph6(graph6)
        inertia = exact_inertia(line_graph_matrix(edges))
        signature = inertia[0] - inertia[2]
        order = ord(graph6[0]) - 63
        cyclomatic = len(edges) - order + 1
        slack = cyclomatic + 1 - 2 * signature
        if signature != expected_signature:
            raise AssertionError(f"wrong signature for {name}")
        if slack != expected_slack:
            raise AssertionError(f"wrong sharp-bound slack for {name}")
        print(
            f"witness {name}: graph6={graph6} edges={len(edges)} "
            f"line_inertia={inertia} signature={signature} sharp_slack={slack}"
        )


if __name__ == "__main__":
    main()
