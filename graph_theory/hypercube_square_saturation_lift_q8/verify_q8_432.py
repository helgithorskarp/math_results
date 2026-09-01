#!/usr/bin/env python3
"""Definition-level verifier for a 432-edge square-saturated subgraph of Q_8."""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
CERTIFICATE = ROOT / "q8_hamming_layer_lift_432.json"
Edge = tuple[int, int]


def edge_key(x: int, y: int) -> Edge:
    difference = x ^ y
    assert difference and not difference & (difference - 1)
    coordinate = difference.bit_length() - 1
    return min(x, y), coordinate


def syndrome7(word: int) -> int:
    result = 0
    for coordinate in range(7):
        if word & (1 << coordinate):
            result ^= coordinate + 1
    return result


def edges(dimension: int) -> set[Edge]:
    return {
        (word, coordinate)
        for word in range(1 << dimension)
        for coordinate in range(dimension)
        if not word & (1 << coordinate)
    }


def squares(dimension: int) -> set[frozenset[Edge]]:
    result: set[frozenset[Edge]] = set()
    for word in range(1 << dimension):
        for first, second in itertools.combinations(range(dimension), 2):
            if word & (1 << first) or word & (1 << second):
                continue
            result.add(
                frozenset(
                    {
                        (word, first),
                        (word, second),
                        (word ^ (1 << first), second),
                        (word ^ (1 << second), first),
                    }
                )
            )
    expected = dimension * (dimension - 1) * (1 << (dimension - 3))
    assert len(result) == expected
    return result


def verify_saturated(
    dimension: int, selected: set[Edge], host_edges: set[Edge], square_faces: set[frozenset[Edge]]
) -> int:
    assert selected <= host_edges
    assert not any(face <= selected for face in square_faces)
    missing = host_edges - selected
    for omitted in missing:
        assert any(face - {omitted} <= selected for face in square_faces if omitted in face), omitted
    return len(missing)


def canonical_bytes(selected: set[Edge]) -> bytes:
    return "\n".join(f"{lower} {coordinate}" for lower, coordinate in sorted(selected)).encode("ascii")


def main() -> None:
    payload = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
    assert payload["base_dimension"] == 7
    assert payload["lift_dimension"] == 8
    vertical_syndrome = payload["vertical_matching_syndrome"]
    quotient_edges = {tuple(sorted(item)) for item in payload["base_quotient_selected_edges"]}
    assert len(quotient_edges) == 13

    host7 = edges(7)
    faces7 = squares(7)
    selected7 = {
        host_edge
        for host_edge in host7
        if tuple(
            sorted(
                (
                    syndrome7(host_edge[0]),
                    syndrome7(host_edge[0]) ^ (host_edge[1] + 1),
                )
            )
        )
        in quotient_edges
    }
    assert len(selected7) == 208
    missing7 = verify_saturated(7, selected7, host7, faces7)
    assert missing7 == 240

    dominating_coset = {word for word in range(128) if syndrome7(word) == vertical_syndrome}
    assert len(dominating_coset) == 16
    assert all(
        edge_key(x, y) not in selected7 for x, y in itertools.combinations(dominating_coset, 2)
        if (x ^ y).bit_count() == 1
    )
    for word in set(range(128)) - dominating_coset:
        neighbors_in_coset = [
            word ^ (1 << coordinate)
            for coordinate in range(7)
            if word ^ (1 << coordinate) in dominating_coset
            and edge_key(word, word ^ (1 << coordinate)) in selected7
        ]
        assert len(neighbors_in_coset) == 1

    selected8: set[Edge] = set()
    for lower, coordinate in selected7:
        selected8.add((lower, coordinate))
        selected8.add((lower | 128, coordinate))
    selected8.update((word, 7) for word in dominating_coset)
    assert len(selected8) == 2 * 208 + 16 == 432

    host8 = edges(8)
    faces8 = squares(8)
    missing8 = verify_saturated(8, selected8, host8, faces8)
    assert len(host8) == 1024
    assert len(faces8) == 1792
    assert missing8 == 592

    code = {word for word in range(128) if syndrome7(word) == 0}
    assert len(code) == 16
    for lower, coordinate in selected8:
        for translation in code:
            x = lower ^ translation
            y = x ^ (1 << coordinate)
            assert edge_key(x, y) in selected8

    print(
        json.dumps(
            {
                "base_omitted_edges_with_witness": missing7,
                "base_selected_edges": len(selected7),
                "dominating_coset_size": len(dominating_coset),
                "lift_host_edges": len(host8),
                "lift_omitted_edges_with_witness": missing8,
                "lift_selected_edge_sha256": hashlib.sha256(canonical_bytes(selected8)).hexdigest(),
                "lift_selected_edges": len(selected8),
                "lift_square_faces": len(faces8),
                "status": "VERIFIED",
                "translation_group_order": len(code),
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
