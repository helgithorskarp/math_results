#!/usr/bin/env python3
"""Independent exact audit of the Parts-509 two-point closure certificate.

This checker deliberately does not import the contribution's Python modules and
does not use NumPy.  It treats the already reviewed Parts-509 base graph and Q3
completion-point census as inputs, then independently checks the load-bearing
new work:

* all Q3--Q3 unit distances, by integer arithmetic in
  Q(sqrt(3),sqrt(5),sqrt(11));
* every packed base, swap, and pair-certificate colouring against the base
  graph; and
* all 340,980,627 (deleted vertex, unordered Q3 pair) extension instances,
  using Python-integer bitsets rather than the contribution's Boolean matrices.

Run from any directory with the math_results checkout as the optional argument:

    python review_pair_closure.py /path/to/math_results
"""
from __future__ import annotations

import base64
import hashlib
import json
import math
import sys
from collections import Counter, defaultdict
from fractions import Fraction
from pathlib import Path


N = 509
NQ = 1158
ROW_BYTES = 127
RADICANDS = (3, 5, 11)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def edge_sha256(edges: list[tuple[int, int]]) -> str:
    body = "".join(f"{a} {b}\n" for a, b in edges).encode()
    return hashlib.sha256(body).hexdigest()


def decode(raw: bytes, deleted: int) -> list[int]:
    if len(raw) != ROW_BYTES:
        raise ValueError("wrong packed row length")
    colors = [(byte >> shift) & 3 for byte in raw for shift in (0, 2, 4, 6)]
    if len(colors) != N - 1:
        raise AssertionError("row decoder length error")
    it = iter(colors)
    return [-1 if v == deleted else next(it) for v in range(N)]


def payload(obj: dict, data_key: str, hash_key: str) -> bytes:
    raw = base64.b64decode(obj[data_key], validate=True)
    if hashlib.sha256(raw).hexdigest() != obj[hash_key]:
        raise ValueError(f"{data_key} payload hash mismatch")
    return raw


def scale_q3(points: list[dict]) -> tuple[list[tuple[tuple[int, ...], tuple[int, ...]]], int]:
    denominator = 1
    parsed = []
    for point in points:
        x = tuple(Fraction(c) for c in point["x"])
        y = tuple(Fraction(c) for c in point["y"])
        if len(x) != 8 or len(y) != 8:
            raise ValueError("unexpected radical-basis dimension")
        parsed.append((x, y))
        for c in x + y:
            denominator = math.lcm(denominator, c.denominator)
    scaled = [
        (
            tuple(int(c * denominator) for c in x),
            tuple(int(c * denominator) for c in y),
        )
        for x, y in parsed
    ]
    if len(set(scaled)) != len(scaled):
        raise ValueError("duplicate Q3 coordinates")
    return scaled, denominator


def radical_factor(mask: int) -> int:
    ans = 1
    for bit, radicand in enumerate(RADICANDS):
        if mask & (1 << bit):
            ans *= radicand
    return ans


RADICAL_FACTOR = tuple(radical_factor(mask) for mask in range(8))


def square(vector: tuple[int, ...]) -> list[int]:
    """Square one radical-basis vector, exploiting symmetry."""
    nz = [(i, a) for i, a in enumerate(vector) if a]
    out = [0] * 8
    for pos, (i, a) in enumerate(nz):
        out[0] += a * a * RADICAL_FACTOR[i]
        for j, b in nz[pos + 1 :]:
            out[i ^ j] += 2 * a * b * RADICAL_FACTOR[i & j]
    return out


def q3_unit_edges(points: list[dict]) -> tuple[list[tuple[int, int]], int]:
    scaled, denominator = scale_q3(points)
    target = denominator * denominator
    edges = []
    for a in range(len(scaled)):
        ax, ay = scaled[a]
        for b in range(a + 1, len(scaled)):
            bx, by = scaled[b]
            sx = square(tuple(x - y for x, y in zip(ax, bx)))
            sy = square(tuple(x - y for x, y in zip(ay, by)))
            if sx[0] + sy[0] == target and all(sx[i] + sy[i] == 0 for i in range(1, 8)):
                edges.append((a, b))
    return edges, denominator


def validate_row(row: list[int], deleted: int, edges: list[tuple[int, int]]) -> None:
    if row[deleted] != -1 or any(row[v] not in range(4) for v in range(N) if v != deleted):
        raise ValueError(f"malformed colouring after deleting {deleted}")
    for a, b in edges:
        if a != deleted and b != deleted and row[a] == row[b]:
            raise ValueError(f"monochromatic base edge {(a, b)} after deleting {deleted}")


def iter_set_bits(value: int):
    while value:
        low = value & -value
        yield low.bit_length() - 1
        value ^= low


def main() -> None:
    root = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path(__file__).resolve().parents[1]
    base_dir = root / "hadwiger_nelson_parts509_criticality"
    swap_dir = root / "hadwiger_nelson_parts509_swap_closure"
    pair_dir = root / "hadwiger_nelson_parts509_pair_closure"
    base_path = base_dir / "certificate.json"
    swap_path = swap_dir / "swap_certificate.json"
    completion_path = swap_dir / "completion_points.json"
    pair_path = pair_dir / "pair_certificate.json"
    ambient_path = pair_dir / "ambient_w3_edges.json"

    base = json.loads(base_path.read_text())
    swap = json.loads(swap_path.read_text())
    completion = json.loads(completion_path.read_text())
    cert = json.loads(pair_path.read_text())
    ambient = json.loads(ambient_path.read_text())

    expected_hashes = {
        "base_certificate_sha256": sha256(base_path),
        "swap_certificate_sha256": sha256(swap_path),
        "completion_points_sha256": sha256(completion_path),
    }
    for key, actual in expected_hashes.items():
        if cert[key] != actual:
            raise ValueError(f"pair certificate {key} mismatch")
    if swap["completion_points_sha256"] != expected_hashes["completion_points_sha256"]:
        raise ValueError("swap certificate uses a different Q3 census")
    if cert["q3_count"] != NQ or completion["q3_count"] != NQ or len(completion["points"]) != NQ:
        raise ValueError("unexpected Q3 size")

    ambient_edges = [tuple(edge) for edge in ambient["edges"]]
    if ambient_edges != sorted(set(ambient_edges)) or any(not (0 <= a < b < N + NQ) for a, b in ambient_edges):
        raise ValueError("ambient edge list is not canonical")
    vv = [(a, b) for a, b in ambient_edges if b < N]
    qv = [(a, b) for a, b in ambient_edges if a < N <= b]
    ambient_qq = [(a - N, b - N) for a, b in ambient_edges if N <= a < b]
    if edge_sha256(vv) != cert["edge_sha256"] or cert["edge_sha256"] != base["edge_sha256"]:
        raise ValueError("base edge-list digest mismatch")
    listed_qv = sorted((v, N + q) for q, point in enumerate(completion["points"]) for v in point["neighbors"])
    if sorted(qv) != listed_qv:
        raise ValueError("ambient Q3--base edges disagree with listed neighborhoods")

    qq, denominator = q3_unit_edges(completion["points"])
    if qq != ambient_qq or len(qq) != cert["q3q3_unit_pairs"]:
        raise ValueError("independently reconstructed Q3--Q3 edges disagree")
    q_neighbors = [tuple(point["neighbors"]) for point in completion["points"]]
    if any(neighbors != tuple(sorted(set(neighbors))) or len(neighbors) < 3 for neighbors in q_neighbors):
        raise ValueError("malformed Q3 neighborhood list")
    qq_masks = [0] * NQ
    for a, b in qq:
        qq_masks[a] |= 1 << b
        qq_masks[b] |= 1 << a

    base_raw = payload(base, "deletion_colorings_base64", "packed_deletion_colorings_sha256")
    swap_raw = payload(swap, "family_rows_base64", "packed_rows_sha256")
    pair_raw = payload(cert, "family_rows_base64", "packed_rows_sha256")
    if len(base_raw) != N * ROW_BYTES:
        raise ValueError("base payload length mismatch")
    if len(swap["family_sizes"]) != N or len(swap_raw) != sum(swap["family_sizes"]) * ROW_BYTES:
        raise ValueError("swap payload length mismatch")
    if len(cert["family_sizes"]) != N or len(pair_raw) != sum(cert["family_sizes"]) * ROW_BYTES:
        raise ValueError("pair payload length mismatch")

    base_rows = [decode(base_raw[u * ROW_BYTES : (u + 1) * ROW_BYTES], u) for u in range(N)]
    swap_offset = pair_offset = 0
    U: dict[tuple[int, int], list[int]] = defaultdict(list)
    total_rows = declared_instances = 0
    full_q_bits = (1 << NQ) - 1
    upper_masks = [full_q_bits ^ ((1 << (q + 1)) - 1) for q in range(NQ)]

    for u in range(N):
        rows = [base_rows[u]]
        for _ in range(swap["family_sizes"][u]):
            rows.append(decode(swap_raw[swap_offset : swap_offset + ROW_BYTES], u))
            swap_offset += ROW_BYTES
        for _ in range(cert["family_sizes"][u]):
            rows.append(decode(pair_raw[pair_offset : pair_offset + ROW_BYTES], u))
            pair_offset += ROW_BYTES
        total_rows += len(rows)

        uncovered = upper_masks.copy()
        for row in rows:
            validate_row(row, u, vv)
            free = []
            valid_bits = 0
            singleton_bits = {1: 0, 2: 0, 4: 0, 8: 0}
            for q, neighbors in enumerate(q_neighbors):
                used = 0
                for v in neighbors:
                    if v != u:
                        used |= 1 << row[v]
                mask = 15 ^ used
                free.append(mask)
                if mask:
                    valid_bits |= 1 << q
                    if mask in singleton_bits:
                        singleton_bits[mask] |= 1 << q
            for q, mask in enumerate(free):
                if not mask:
                    continue
                covered = valid_bits & upper_masks[q]
                if mask in singleton_bits:
                    covered &= ~(qq_masks[q] & singleton_bits[mask])
                uncovered[q] &= ~covered

        actual = {(q, r) for q, bits in enumerate(uncovered) for r in iter_set_bits(bits)}
        declared = {tuple(pair) for pair in cert["declared_pairs"][u]}
        if actual != declared:
            raise ValueError(f"declared-pair mismatch at deleted vertex {u}")
        declared_instances += len(actual)
        for pair in actual:
            U[pair].append(u)

    if swap_offset != len(swap_raw) or pair_offset != len(pair_raw):
        raise ValueError("not all packed rows were consumed")
    histogram = Counter(map(len, U.values()))
    expected_histogram = {int(k): v for k, v in cert["U_histogram"].items()}
    if dict(sorted(histogram.items())) != expected_histogram:
        raise ValueError("U(A) histogram mismatch")
    expected_two = {(tuple(item["A"]), tuple(item["U"])) for item in cert["pairs_with_U_eq2"]}
    actual_two = {(pair, tuple(vertices)) for pair, vertices in U.items() if len(vertices) == 2}
    if actual_two != expected_two:
        raise ValueError("pairs with |U(A)|=2 mismatch")
    if any(len(vertices) >= 3 for vertices in U.values()):
        raise ValueError("a Q3 pair fails for at least three deleted vertices")
    if cert["pairs_with_U_ge3"] or cert["candidates_508"]:
        raise ValueError("certificate unexpectedly declares a 508-vertex candidate")
    triple_raw = payload(cert, "triple_rows_base64", "packed_triple_rows_sha256")
    if triple_raw or cert["triple_witnesses"]:
        raise ValueError("unexpected triple-witness payload when no |U(A)| >= 3")

    result = {
        "all_checks": True,
        "method": "independent Python-integer exact geometry and bitset coverage replay",
        "q3_common_denominator": denominator,
        "base_edges": len(vv),
        "q3_base_edges": len(qv),
        "q3_q3_edges": len(qq),
        "q3_pairs": NQ * (NQ - 1) // 2,
        "pair_deletion_instances": N * NQ * (NQ - 1) // 2,
        "colourings_checked": total_rows,
        "declared_instances": declared_instances,
        "pairs_with_nonempty_U": len(U),
        "U_histogram": {str(k): v for k, v in sorted(histogram.items())},
        "pairs_with_U_ge3": 0,
        "pair_certificate_sha256": sha256(pair_path),
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
