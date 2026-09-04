#!/usr/bin/env python3
"""Independent exact audit of the Parts-509 tie-union certificates.

This checker deliberately does not import any code from the contribution.  It
enumerates *all* pairs in the largest (level-2) ambient graph using rational
arithmetic in Q(sqrt(3),sqrt(5),sqrt(11)), restricts that edge set to the two
smaller nested pools, replays every forced-vertex and killing-set colouring,
and reconstructs the three pseudo-Boolean decision instances.

The regenerated .opb instances can be passed to RoundingSat and VeriPB using
the commands in README.md.  Large proof logs are intentionally not committed.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import time
from fractions import Fraction
from pathlib import Path


POOLS = ("P25", "P44", "L2")
RADICANDS = (3, 5, 11)
ONE = (Fraction(1),) + (Fraction(0),) * 7

EXPECTED = {
    "P25": {
        "certificate_sha256": "edab40766c065fbbf9474ef55f2bccb704edbc79413a9761e8af41916d2f418c",
        "vertices": 534,
        "edges": 2620,
        "forced": 483,
        "free": 51,
        "family": 67,
        "minimal": 54,
        "pool": 25,
        "minimum": 26,
        "opb_sha256": "7c90e4b5f4f06b4a06944a373d587c1bef1766ef15426a90ee3b5514af903b6d",
        "proof_sha256": "49ffe96e4cb50bcdf603595c7231745a80609746cf9521cfac110de9931d54a6",
        "proof_bytes": 4532,
    },
    "P44": {
        "certificate_sha256": "51cefb3a66ab5e13d01f474208d81f5ab34e869c61d06b5142eceeddaf09f29a",
        "vertices": 553,
        "edges": 2754,
        "forced": 475,
        "free": 78,
        "family": 170,
        "minimal": 133,
        "pool": 44,
        "minimum": 34,
        "opb_sha256": "9ccfdbb0766e181018efa20eb68165eff11aaec88b9b06acda7b5c192fb27471",
        "proof_sha256": "39b13eabd38950e21b85fdd07d4d6514513f5445e5888ef31ada2f0ca4108690",
        "proof_bytes": 262815,
    },
    "L2": {
        "certificate_sha256": "5d49a0885fc89d095caeba3a5e9eb7ab320842714929682f4e02e2b0943d8fa9",
        "vertices": 648,
        "edges": 3119,
        "forced": 475,
        "free": 173,
        "family": 659,
        "minimal": 540,
        "pool": 139,
        "minimum": 34,
        "opb_sha256": "b09f17c663c76350a6ff8b63019203299c0e6e950b4ea1d437640276ae9c37af",
        "proof_sha256": "a7642baa7edc8a1dea3fea5526cee9cf208ebf3e0341776a03bc09c0b6c32869",
        "proof_bytes": 122264591,
    },
}


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def parse_field(values: list[str]) -> tuple[Fraction, ...]:
    assert len(values) == 8
    return tuple(Fraction(value) for value in values)


def square_field(value: tuple[Fraction, ...]) -> tuple[Fraction, ...]:
    """Square an element in the square-free subset basis, without floats."""

    answer = [Fraction(0)] * 8
    nonzero = [(mask, coefficient) for mask, coefficient in enumerate(value) if coefficient]
    for position, (left_mask, left) in enumerate(nonzero):
        diagonal_factor = 1
        for bit, radicand in enumerate(RADICANDS):
            if left_mask & (1 << bit):
                diagonal_factor *= radicand
        answer[0] += left * left * diagonal_factor
        for right_mask, right in nonzero[position + 1 :]:
            common_factor = 1
            for bit, radicand in enumerate(RADICANDS):
                if (left_mask & right_mask) & (1 << bit):
                    common_factor *= radicand
            answer[left_mask ^ right_mask] += 2 * left * right * common_factor
    return tuple(answer)


def is_unit_distance(
    left: tuple[tuple[Fraction, ...], tuple[Fraction, ...]],
    right: tuple[tuple[Fraction, ...], tuple[Fraction, ...]],
) -> bool:
    dx = tuple(a - b for a, b in zip(left[0], right[0]))
    dy = tuple(a - b for a, b in zip(left[1], right[1]))
    dx2 = square_field(dx)
    dy2 = square_field(dy)
    return tuple(a + b for a, b in zip(dx2, dy2)) == ONE


def proper_colouring(
    colouring: str,
    vertices: list[int],
    relevant_edges: list[tuple[int, int]],
) -> bool:
    if len(colouring) != len(vertices) or set(colouring) - set("0123"):
        return False
    colour = dict(zip(vertices, colouring, strict=True))
    return all(colour[a] != colour[b] for a, b in relevant_edges if a in colour and b in colour)


def minimal_family(rows: list[list[int]]) -> list[list[int]]:
    sets = [frozenset(row) for row in rows]
    assert len(set(sets)) == len(sets)
    return [row for row, item in zip(rows, sets, strict=True) if not any(other < item for other in sets)]


def decision_opb(cert: dict, minimal: list[list[int]]) -> bytes:
    """Independent transcription of the certified constrained hitting set."""

    free = cert["free"]
    variable = {vertex: index + 1 for index, vertex in enumerate(free)}
    lines = [
        " ".join(f"+1 x{variable[vertex]}" for vertex in sorted(row)) + " >= 1 ;"
        for row in minimal
    ]
    min_points = cert["min_points"]
    pool = cert["pool_free"]
    lines.append(" ".join(f"+1 x{variable[vertex]}" for vertex in pool) + f" >= {min_points} ;")
    bound = cert["minimum_hitting_set"] - 1
    lines.append(" ".join(f"-1 x{variable[vertex]}" for vertex in free) + f" >= {-bound} ;")
    header = f"* #variable= {len(free)} #constraint= {len(lines)} #equal= 0 intsize= 8\n"
    return (header + "\n".join(lines) + "\n").encode()


def load_certificates(source: Path) -> dict[str, dict]:
    certificates = {}
    for name in POOLS:
        path = source / f"certificate_{name}.json"
        raw = path.read_bytes()
        assert sha256_bytes(raw) == EXPECTED[name]["certificate_sha256"]
        certificates[name] = json.loads(raw)
    return certificates


def main() -> None:
    parser = argparse.ArgumentParser()
    default_source = Path(__file__).resolve().parent.parent / "hadwiger_nelson_parts509_tie_union_minimum"
    parser.add_argument("--source", type=Path, default=default_source)
    parser.add_argument("--write-opb", type=Path)
    parser.add_argument("--proof-dir", type=Path, help="optional directory containing P25/P44/L2.pbp")
    args = parser.parse_args()

    started = time.monotonic()
    certificates = load_certificates(args.source)

    for smaller, larger in zip(POOLS, POOLS[1:]):
        small = certificates[smaller]
        large = certificates[larger]
        assert set(small["vertices"]) <= set(large["vertices"])
        assert all(
            small["coordinates"][str(vertex)] == large["coordinates"][str(vertex)]
            for vertex in small["vertices"]
        )

    largest = certificates["L2"]
    vertices = largest["vertices"]
    assert vertices == sorted(vertices) and len(vertices) == len(set(vertices))
    points = {
        vertex: (
            parse_field(largest["coordinates"][str(vertex)][0]),
            parse_field(largest["coordinates"][str(vertex)][1]),
        )
        for vertex in vertices
    }
    assert len(set(points.values())) == len(points), "duplicate geometric points"

    edges = []
    for left_index, left_vertex in enumerate(vertices):
        for right_vertex in vertices[left_index + 1 :]:
            if is_unit_distance(points[left_vertex], points[right_vertex]):
                edges.append((left_vertex, right_vertex))
    print(
        f"exact_all_pairs: vertices={len(vertices)} pairs={len(vertices)*(len(vertices)-1)//2} "
        f"unit_edges={len(edges)} seconds={time.monotonic()-started:.3f}"
    )

    if args.write_opb:
        args.write_opb.mkdir(parents=True, exist_ok=True)

    total_witnesses = 0
    for name in POOLS:
        cert = certificates[name]
        expected = EXPECTED[name]
        star = cert["vertices"]
        star_set = set(star)
        relevant_edges = [(a, b) for a, b in edges if a in star_set and b in star_set]
        assert len(star) == expected["vertices"]
        assert len(relevant_edges) == expected["edges"]
        assert len(cert["forced"]) == expected["forced"]
        assert len(cert["free"]) == expected["free"]
        assert set(cert["forced"]).isdisjoint(cert["free"])
        assert sorted(cert["forced"] + cert["free"]) == star
        assert cert["pool"] == sorted(vertex for vertex in star if vertex >= 509)
        assert cert["pool_free"] == sorted(vertex for vertex in cert["free"] if vertex >= 509)
        assert len(cert["pool_free"]) == expected["pool"]

        for removed in cert["forced"]:
            surviving = [vertex for vertex in star if vertex != removed]
            assert proper_colouring(cert["forced_witness"][str(removed)], surviving, relevant_edges)

        family = []
        for item in cert["family"]:
            row = item["D"]
            assert row == sorted(row) and row and len(row) == len(set(row))
            assert set(row) <= set(cert["free"])
            surviving = [vertex for vertex in star if vertex not in set(row)]
            assert proper_colouring(item["witness"], surviving, relevant_edges)
            family.append(row)
        assert len(family) == expected["family"]
        minimal = minimal_family(family)
        assert len(minimal) == expected["minimal"]
        assert all(any(set(core) <= set(row) for core in minimal) for row in family)

        assert cert["min_points"] == 4
        assert cert["minimum_hitting_set"] == expected["minimum"]
        assert len(cert["forced"]) + cert["minimum_hitting_set"] == 509
        opb = decision_opb(cert, minimal)
        assert sha256_bytes(opb) == expected["opb_sha256"]
        if args.write_opb:
            (args.write_opb / f"{name}.opb").write_bytes(opb)
        if args.proof_dir:
            proof = (args.proof_dir / f"{name}.pbp").read_bytes()
            assert len(proof) == expected["proof_bytes"]
            assert sha256_bytes(proof) == expected["proof_sha256"]

        witnesses = len(cert["forced"]) + len(family)
        total_witnesses += witnesses
        edge_hash = sha256_bytes("".join(f"{a} {b}\n" for a, b in relevant_edges).encode())
        print(
            f"{name}: edges={len(relevant_edges)} edge_sha256={edge_hash} "
            f"witnesses={witnesses} minimal_killing_sets={len(minimal)} "
            f"opb_sha256={sha256_bytes(opb)}"
        )

    print(f"all_checks=true total_witnesses={total_witnesses} seconds={time.monotonic()-started:.3f}")


if __name__ == "__main__":
    main()
