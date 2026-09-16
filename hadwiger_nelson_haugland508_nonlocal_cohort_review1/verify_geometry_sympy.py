#!/usr/bin/env python3
"""Exact union-geometry cross-check through the independent SymPy route."""

from __future__ import annotations

from hashlib import sha256
import importlib.util
import json
from pathlib import Path

import verify as review


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
STRICT = ROOT / "hadwiger_nelson_haugland2131_strict_edges" / "strict_edge_certificate.py"
RECON = ROOT / "hadwiger_nelson_haugland2131_exact_reproduction" / "reconstruct.py"
STRICT_SHA256 = "5f7cb15233f9cca0e422350f71e88293899077e729e6ceeeac4f276890b46447"
RECON_SHA256 = "220099937ab59881932e444f72ac4da1d3b00556321d512cb46f60ca45f45664"


def load_module(name: str, path: Path):
    review.require(sha256(path.read_bytes()).hexdigest() in (STRICT_SHA256, RECON_SHA256), f"pinned {name}")
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def main() -> None:
    cert = json.loads((HERE / "certificate.json").read_text())
    target = review.read_hashed(review.TARGET / "certificate.json", review.TARGET_CERT_SHA256)
    edges, adjacency = review.load_parent()
    supports = [review.frozen_support(r["seed"], r["orientation"], adjacency) for r in target["records"]]
    union = sorted(set().union(*map(set, supports)))
    review.require(len(union) == cert["union_vertices"], "union order")

    strict = load_module("hn_primary_strict", STRICT)
    reconstruct = strict.load_reconstruct()
    # Pin the file imported internally by strict.load_reconstruct().
    review.require(sha256(RECON.read_bytes()).hexdigest() == RECON_SHA256, "pinned reconstruction")
    payload = review.read_hashed(review.PARENT / "graph.json", review.GRAPH_SHA256)
    field = reconstruct.Cyclotomic84()
    vectors = field.unit_vectors()
    floats = field.float_vectors()
    g1, f1 = reconstruct.build_g1(payload["paths"], vectors, floats, field)
    g2, f2 = reconstruct.build_g2(g1, f1, field)
    g3, _ = reconstruct.build_g3(g2, f2, field)
    review.require((len(g1), len(g2), len(g3)) == (740, 1066, 2131), "reconstruction orders")
    review.require(len(set(g3)) == 2131, "distinct parent points")
    coordinate_sha = strict.coordinate_hash(g3, True)
    review.require(
        coordinate_sha == "fcdcba9dee3c2e0ea6044e17cb5f32bc9c989b8155d8c377863d41d357f72cab",
        "parent coordinate digest",
    )

    prime, zeta_image, sqrt5_image = 1009, 527, 244
    strict.check_specialization(field, prime, zeta_image)
    points = [g3[v] for v in union]
    images = strict.extended_images(points, prime, zeta_image, sqrt5_image)
    survivors = strict.sieve_candidates(images, prime)
    local_edges = strict.confirm_extended(reconstruct, points, survivors, field.zero, field.one)
    actual = [(union[u], union[v]) for u, v in local_edges]
    expected = review.induced(union, edges)
    review.require(actual == expected, "complete exact union edge set")
    result = {
        "status": "EXACT_SYMPY_UNION_GEOMETRY_VERIFIED",
        "arithmetic": "SymPy 1.14.0 algebraic field over Q(zeta_84)(sqrt(5))",
        "prime": prime,
        "zeta_image": zeta_image,
        "sqrt5_image": sqrt5_image,
        "parent_vertices": len(g3),
        "parent_coordinate_sha256": coordinate_sha,
        "union_vertices": len(union),
        "union_pairs_checked": len(union) * (len(union) - 1) // 2,
        "union_sieve_survivors": len(survivors),
        "union_unit_edges": len(actual),
        "union_global_edge_sha256": review.digest_edges(actual),
        "matches_parent_induced_edges": True,
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

