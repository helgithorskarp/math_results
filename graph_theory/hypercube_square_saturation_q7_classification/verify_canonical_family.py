#!/usr/bin/env python3
"""Independent direct checker for the canonical quotient and its 224 images."""

from __future__ import annotations

import hashlib
import itertools
import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parent
CERTIFICATE = ROOT / "canonical_affine_quotient.json"
Edge = tuple[int, int]


def edge(x: int, y: int) -> Edge:
    assert x != y
    return min(x, y), max(x, y)


def syndrome(word: int) -> int:
    result = 0
    for coordinate in range(7):
        if word & (1 << coordinate):
            result ^= coordinate + 1
    return result


def quotient_cycles() -> set[frozenset[Edge]]:
    cycles: set[frozenset[Edge]] = set()
    for start in range(8):
        for first, second in itertools.combinations(range(1, 8), 2):
            vertices = (start, start ^ first, start ^ first ^ second, start ^ second)
            cycles.add(
                frozenset(edge(vertices[index], vertices[(index + 1) % 4]) for index in range(4))
            )
    assert len(cycles) == 42
    return cycles


def quotient_is_saturated(selected: frozenset[Edge]) -> bool:
    cycles = quotient_cycles()
    all_edges = frozenset(edge(x, y) for x in range(8) for y in range(x + 1, 8))
    if any(cycle <= selected for cycle in cycles):
        return False
    return all(
        any(candidate - {missing} <= selected for candidate in cycles if missing in candidate)
        for missing in all_edges - selected
    )


def independent(a: int, b: int, c: int) -> bool:
    return len({0, a, b, c, a ^ b, a ^ c, b ^ c, a ^ b ^ c}) == 8


def family_member(pendant: int, universal: int, basis: tuple[int, int, int]) -> frozenset[Edge]:
    assert pendant != universal
    assert independent(*basis)
    assert basis[0] ^ basis[1] ^ basis[2] == pendant ^ universal
    selected = {edge(universal, vertex) for vertex in range(8) if vertex != universal}
    leaves = [pendant ^ vector for vector in basis]
    triangle = [universal ^ vector for vector in basis]
    selected.update(edge(leaves[index], triangle[index]) for index in range(3))
    selected.update(edge(x, y) for x, y in itertools.combinations(triangle, 2))
    assert len(selected) == 13
    return frozenset(selected)


def explicit_family() -> set[frozenset[Edge]]:
    result: set[frozenset[Edge]] = set()
    for pendant in range(8):
        for universal in range(8):
            if pendant == universal:
                continue
            for basis in itertools.combinations(range(1, 8), 3):
                if independent(*basis) and basis[0] ^ basis[1] ^ basis[2] == pendant ^ universal:
                    result.add(family_member(pendant, universal, basis))
    assert len(result) == 224
    return result


def affine_maps() -> list[tuple[int, ...]]:
    linear = set()
    for columns in itertools.permutations(range(1, 8), 3):
        if not independent(*columns):
            continue
        linear.add(
            tuple(
                (columns[0] if value & 1 else 0)
                ^ (columns[1] if value & 2 else 0)
                ^ (columns[2] if value & 4 else 0)
                for value in range(8)
            )
        )
    assert len(linear) == 168
    result = [tuple(image ^ shift for image in mapping) for mapping in linear for shift in range(8)]
    assert len(set(result)) == 1344
    return result


def transform(selected: frozenset[Edge], mapping: tuple[int, ...]) -> frozenset[Edge]:
    return frozenset(edge(mapping[x], mapping[y]) for x, y in selected)


def canonical_bytes(selected: set[Edge] | frozenset[Edge]) -> bytes:
    return "\n".join(f"{x} {y}" for x, y in sorted(selected)).encode("ascii")


def main() -> None:
    payload = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
    selected_quotient = frozenset(edge(*item) for item in payload["selected_edges"])
    basis = tuple(payload["basis"])
    canonical = family_member(
        payload["distinguished_pendant_vertex"],
        payload["distinguished_universal_vertex"],
        basis,
    )
    assert selected_quotient == canonical
    assert quotient_is_saturated(selected_quotient)

    family = explicit_family()
    assert all(quotient_is_saturated(member) for member in family)
    maps = affine_maps()
    orbit = {transform(canonical, mapping) for mapping in maps}
    stabilizer_order = sum(transform(canonical, mapping) == canonical for mapping in maps)
    assert orbit == family
    assert stabilizer_order == 6

    code = {word for word in range(128) if syndrome(word) == 0}
    assert len(code) == 16
    assert min((x ^ y).bit_count() for x in code for y in code if x != y) == 3
    host_edges = {
        (word, coordinate)
        for word in range(128)
        for coordinate in range(7)
        if not word & (1 << coordinate)
    }
    selected_q7 = {
        host_edge
        for host_edge in host_edges
        if edge(syndrome(host_edge[0]), syndrome(host_edge[0]) ^ (host_edge[1] + 1))
        in selected_quotient
    }
    assert len(host_edges) == 448
    assert len(selected_q7) == 208

    squares: set[frozenset[tuple[int, int]]] = set()
    for word in range(128):
        for first, second in itertools.combinations(range(7), 2):
            if word & (1 << first) or word & (1 << second):
                continue
            squares.add(
                frozenset(
                    {
                        (word, first),
                        (word, second),
                        (word ^ (1 << first), second),
                        (word ^ (1 << second), first),
                    }
                )
            )
    assert len(squares) == 672
    assert not any(square <= selected_q7 for square in squares)
    missing_q7 = host_edges - selected_q7
    assert all(
        any(candidate - {missing} <= selected_q7 for candidate in squares if missing in candidate)
        for missing in missing_q7
    )
    for translation in code:
        for lower, coordinate in selected_q7:
            x = lower ^ translation
            y = x ^ (1 << coordinate)
            translated = (min(x, y), coordinate)
            assert translated in selected_q7

    degrees = Counter(vertex for quotient_edge in selected_quotient for vertex in quotient_edge)
    planes = {
        frozenset((start, start ^ first, start ^ second, start ^ first ^ second))
        for start in range(8)
        for first, second in itertools.combinations(range(1, 8), 2)
    }
    assert len(planes) == 14
    plane_profile = Counter(
        sum(edge(x, y) in selected_quotient for x, y in itertools.combinations(plane, 2))
        for plane in planes
    )
    expanded_bytes = "\n".join(f"{lower} {coordinate}" for lower, coordinate in sorted(selected_q7)).encode(
        "ascii"
    )
    print(
        json.dumps(
            {
                "affine_group_order": len(maps),
                "affine_orbit_size": len(orbit),
                "affine_stabilizer_order": stabilizer_order,
                "explicit_family_size": len(family),
                "hamming_codewords": len(code),
                "omitted_q7_edges_with_witness": len(missing_q7),
                "q7_selected_edge_sha256": hashlib.sha256(expanded_bytes).hexdigest(),
                "q7_selected_edges": len(selected_q7),
                "q7_square_faces": len(squares),
                "quotient_degree_sequence": sorted(degrees.values()),
                "quotient_edge_sha256": hashlib.sha256(canonical_bytes(selected_quotient)).hexdigest(),
                "quotient_plane_profile": dict(sorted(plane_profile.items())),
                "status": "VERIFIED",
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
