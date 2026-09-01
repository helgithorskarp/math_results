#!/usr/bin/env python3
"""Independent solver-free replay of the degree-10 replacement certificate.

This checker intentionally imports none of pair_replacement.py.  It trusts the
committed edge and neighbor manifests; pair_replacement.py supplies the separate
exact-geometry bridge from algebraic coordinates to those manifests.
"""

import argparse
import base64
import hashlib
import json
import struct
from pathlib import Path


HERE = Path(__file__).resolve().parent
BASE_CERT = HERE.parent / "hadwiger_nelson_parts509_criticality" / "certificate.json"
N, K, X = 509, 4, 509
ROW_BYTES = 128
MAGIC = b"HN509RP1"


def unpack_base_rows():
    document = json.loads(BASE_CERT.read_text())
    payload = base64.b64decode(document["deletion_colorings_base64"], validate=True)
    if hashlib.sha256(payload).hexdigest() != document["packed_deletion_colorings_sha256"]:
        raise ValueError("base certificate payload hash mismatch")
    row_bytes = (N - 1 + 3) // 4
    if len(payload) != N * row_bytes:
        raise ValueError("base certificate payload length mismatch")
    rows = []
    for deleted in range(N):
        raw = payload[deleted * row_bytes : (deleted + 1) * row_bytes]
        compact = [(raw[i // 4] >> (2 * (i % 4))) & 3 for i in range(N - 1)]
        row = []
        cursor = 0
        for vertex in range(N):
            if vertex == deleted:
                row.append(-1)
            else:
                row.append(compact[cursor])
                cursor += 1
        rows.append(row)
    return rows


def unpack_witness(raw):
    if len(raw) != ROW_BYTES or raw[-1] & 0xF0:
        raise ValueError("invalid packed witness")
    return [(raw[i // 4] >> (2 * (i % 4))) & 3 for i in range(N + 1)]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("certificate", type=Path)
    args = parser.parse_args()
    edges = [tuple(edge) for edge in json.loads((HERE / "edges.json").read_text())]
    neighbors = [tuple(row) for row in json.loads((HERE / "candidate_neighbors.json").read_text())]
    if len(edges) != 2442 or len(neighbors) != 4 or any(len(row) != 10 for row in neighbors):
        raise ValueError("manifest dimensions differ")
    rows = unpack_base_rows()
    for deleted, colors in enumerate(rows):
        for u, v in edges:
            if deleted not in (u, v) and colors[u] == colors[v]:
                raise ValueError(f"bad base deletion row {deleted}")

    remaining = set()
    precovered = 0
    for candidate, neighborhood in enumerate(neighbors):
        for u in range(N):
            for v in range(u + 1, N):
                usable = False
                for row_deleted, extra_deleted in ((u, v), (v, u)):
                    used = {
                        rows[row_deleted][w]
                        for w in neighborhood
                        if w not in (row_deleted, extra_deleted)
                    }
                    usable |= used != set(range(K))
                if usable:
                    precovered += 1
                else:
                    remaining.add((candidate, u, v))

    data = args.certificate.read_bytes()
    if len(data) < 16:
        raise ValueError("truncated certificate")
    magic, vertices, candidate_count, count = struct.unpack_from("<8sHHI", data)
    if (magic, vertices, candidate_count) != (MAGIC, N, 4):
        raise ValueError("certificate header mismatch")
    if len(data) != 16 + count * 132:
        raise ValueError("certificate record count mismatch")
    offset = 16
    edge_checks = 0
    useful = 0
    for _ in range(count):
        u, v = struct.unpack_from("<HH", data, offset)
        raw = data[offset + 4 : offset + 132]
        offset += 132
        if not 0 <= u < v < N:
            raise ValueError("invalid deleted pair")
        colors = unpack_witness(raw)
        for a, b in edges:
            if a not in (u, v) and b not in (u, v):
                edge_checks += 1
                if colors[a] == colors[b]:
                    raise ValueError(f"monochromatic edge {(a, b)}")
        newly = 0
        for candidate, neighborhood in enumerate(neighbors):
            if all(w in (u, v) or colors[w] != colors[X] for w in neighborhood):
                key = (candidate, u, v)
                if key in remaining:
                    remaining.remove(key)
                    newly += 1
        if newly:
            useful += 1
    if remaining:
        raise ValueError(f"{len(remaining)} instances remain uncovered")
    if useful != count:
        raise ValueError(f"{count - useful} certificate records are redundant")
    print(
        json.dumps(
            {
                "all_checks": True,
                "instances": 4 * N * (N - 1) // 2,
                "prior_rows_cover": precovered,
                "residual_instances": 4 * N * (N - 1) // 2 - precovered,
                "certificate_records": count,
                "retained_edge_inequality_checks": edge_checks,
                "certificate_sha256": hashlib.sha256(data).hexdigest(),
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
