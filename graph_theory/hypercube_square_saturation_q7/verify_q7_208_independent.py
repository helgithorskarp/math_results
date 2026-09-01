#!/usr/bin/env python3
"""Independent checker for the compact 208-edge Q_7 construction.

This deliberately does not import the SAT generator.  It expands the Hamming-code
translation orbits, reconstructs all edges and all 2-faces from endpoint pairs,
and checks square-freeness, saturation, and translation invariance directly.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
CERTIFICATE = ROOT / "q7_hamming_translation_208.json"


def canonical_edge(a: int, b: int) -> tuple[int, int]:
    difference = a ^ b
    assert difference and not difference & (difference - 1)
    coordinate = difference.bit_length() - 1
    return (min(a, b), coordinate)


def syndrome(word: int) -> int:
    value = 0
    for coordinate in range(7):
        if word & (1 << coordinate):
            value ^= coordinate + 1
    return value


def main() -> None:
    payload = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
    assert payload["dimension"] == 7
    assert payload["translation_code"] == "hamming7"
    representatives = [tuple(item) for item in payload["selected_orbit_representatives"]]

    code = {word for word in range(128) if syndrome(word) == 0}
    assert len(code) == 16
    assert min((a ^ b).bit_count() for a in code for b in code if a != b) == 3

    selected: set[tuple[int, int]] = set()
    for lower, coordinate in representatives:
        assert not lower & (1 << coordinate)
        for translation in code:
            selected.add(canonical_edge(lower ^ translation, (lower ^ (1 << coordinate)) ^ translation))

    host_edges = {
        canonical_edge(vertex, vertex ^ (1 << coordinate))
        for vertex in range(128)
        for coordinate in range(7)
        if not vertex & (1 << coordinate)
    }
    assert selected <= host_edges
    assert len(selected) == 208

    faces: list[frozenset[tuple[int, int]]] = []
    for base in range(128):
        for first in range(7):
            if base & (1 << first):
                continue
            for second in range(first + 1, 7):
                if base & (1 << second):
                    continue
                opposite = base ^ (1 << first) ^ (1 << second)
                face = frozenset(
                    {
                        canonical_edge(base, base ^ (1 << first)),
                        canonical_edge(base, base ^ (1 << second)),
                        canonical_edge(opposite, opposite ^ (1 << first)),
                        canonical_edge(opposite, opposite ^ (1 << second)),
                    }
                )
                assert len(face) == 4
                faces.append(face)
    assert len(faces) == 672
    assert len(set(faces)) == 672
    assert not any(face <= selected for face in faces)

    omitted = host_edges - selected
    witness_count = 0
    for edge in omitted:
        witnesses = [face for face in faces if edge in face and len((face - {edge}) & selected) == 3]
        assert witnesses, f"unsaturated omitted edge {edge}"
        witness_count += 1
    assert witness_count == 240

    for edge in selected:
        lower, coordinate = edge
        for translation in code:
            translated = canonical_edge(lower ^ translation, (lower ^ (1 << coordinate)) ^ translation)
            assert translated in selected

    canonical_bytes = "\n".join(f"{edge[0]} {edge[1]}" for edge in sorted(selected)).encode("ascii")
    print(
        json.dumps(
            {
                "hamming_codewords": len(code),
                "host_edges": len(host_edges),
                "omitted_edges_with_witness": witness_count,
                "selected_edge_sha256": hashlib.sha256(canonical_bytes).hexdigest(),
                "selected_edges": len(selected),
                "square_faces": len(faces),
                "status": "VERIFIED",
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
