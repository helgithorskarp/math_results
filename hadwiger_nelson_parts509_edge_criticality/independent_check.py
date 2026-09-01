#!/usr/bin/env python3
"""Independent, solver-free check of the packed H-e coloring witnesses."""

from __future__ import annotations

import base64
import hashlib
import json
import sys
from pathlib import Path


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def main() -> None:
    edge_path = Path(sys.argv[1])
    certificate_path = Path(sys.argv[2])
    edge_bytes = edge_path.read_bytes()
    edges = [tuple(pair) for pair in json.loads(edge_bytes)["edges"]]
    certificate_bytes = certificate_path.read_bytes()
    certificate = json.loads(certificate_bytes)

    assert len(edges) == 2259
    assert edges == sorted(set(edges))
    assert all(0 <= u < v < 509 for u, v in edges)
    assert sha256(edge_bytes) == certificate["edge_file_sha256"]
    canonical_edges = "".join(f"{u} {v}\n" for u, v in edges).encode()
    assert sha256(canonical_edges) == certificate["edge_sha256"]

    payload = base64.b64decode(certificate["rows_base64"], validate=True)
    assert len(payload) == 2259 * 128
    assert sha256(payload) == certificate["packed_edge_deletion_colorings_sha256"]

    retained_checks = 0
    for deleted_index, deleted_edge in enumerate(edges):
        row = payload[128 * deleted_index : 128 * (deleted_index + 1)]
        assert row[-1] < 4  # six padding bits must be zero
        colors = tuple(
            (row[vertex >> 2] >> ((vertex & 3) << 1)) & 3
            for vertex in range(509)
        )
        assert set(colors) == {0, 1, 2, 3}
        assert colors[deleted_edge[0]] == colors[deleted_edge[1]]
        monochromatic = [
            edge_index
            for edge_index, (u, v) in enumerate(edges)
            if colors[u] == colors[v]
        ]
        assert monochromatic == [deleted_index]
        retained_checks += len(edges) - 1

    print(
        json.dumps(
            {
                "all_checks": True,
                "certificate_sha256": sha256(certificate_bytes),
                "edge_deletion_rows": len(edges),
                "endpoint_equalities": len(edges),
                "retained_edge_inequalities": retained_checks,
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
