#!/usr/bin/env python3
"""Solver-free verifier for the union of all six exceptional Parts placements."""

from __future__ import annotations

import argparse
import base64
import hashlib
import importlib.util
import json
import subprocess
import sys
from pathlib import Path


L_SIZE = 374
TRIPLE_SIZE = 533
EXTENSION_SIZE = 159
ALL_SIZE = 692
EXPECTED_TRIPLE_CERTIFICATE_SHA256 = "46ee849ead7b3601e887cee2aa2d5a1d02d12cf083a673c9890e2d2552bef795"
EXPECTED_TRIPLE_VERIFIER_SHA256 = "e367ad5029146a764d4804b13b6e319f1ccc82e3def1b49d001c981bd35db6b9"
EXPECTED_EDGE_SHA256 = "ee9d50eed3d3ba28d5a687876311fdb23b02a88458eed0c769a04916d1018465"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_triple_verifier(path: Path):
    spec = importlib.util.spec_from_file_location("parts509_rotation_triple_verify", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load the triple verifier")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def run_triple_verifier(verifier_path: Path, certificate_path: Path) -> dict:
    completed = subprocess.run(
        [sys.executable, str(verifier_path), str(certificate_path)],
        check=True,
        capture_output=True,
        text=True,
    )
    lines = [line for line in completed.stdout.splitlines() if line]
    if len(lines) != 1:
        raise AssertionError("unexpected triple-verifier output")
    summary = json.loads(lines[0])
    expected = {
        "all_checks": True,
        "vertices": 533,
        "edges": 2607,
        "forced_vertices": 470,
        "free_vertices": 63,
        "minimal_killing_sets": 330,
        "transversal_number": 39,
        "transversal_search_nodes": 73946,
        "minimum_non_four_colorable_order": 509,
        "strict_edge_arrays_identical": True,
    }
    if any(summary.get(key) != value for key, value in expected.items()):
        raise AssertionError("unexpected triple-verifier summary")
    return summary


def scale_point(point, factor: int):
    return tuple(tuple(factor * coefficient for coefficient in coordinate) for coordinate in point)


def lift_colors(colors: dict[int, int]) -> dict[int, int]:
    """Duplicate one canonical 159-vertex extension while retaining common L."""
    lifted = {vertex: color for vertex, color in colors.items() if vertex < L_SIZE}
    for vertex, color in colors.items():
        if vertex >= L_SIZE:
            lifted[vertex] = color
            lifted[vertex + EXTENSION_SIZE] = color
    return lifted


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("certificate", nargs="?", type=Path, default=Path(__file__).with_name("certificate.json"))
    args = parser.parse_args()
    here = Path(__file__).resolve().parent
    root = here.parent
    triple_dir = root / "hadwiger_nelson_parts509_rotation_triple_minimum"
    triple_verifier_path = triple_dir / "verify.py"
    triple_certificate_path = triple_dir / "certificate.json"
    if sha256(triple_verifier_path) != EXPECTED_TRIPLE_VERIFIER_SHA256:
        raise ValueError("unexpected source triple verifier SHA-256")
    if sha256(triple_certificate_path) != EXPECTED_TRIPLE_CERTIFICATE_SHA256:
        raise ValueError("unexpected source triple certificate SHA-256")
    triple_summary = run_triple_verifier(triple_verifier_path, triple_certificate_path)
    triple = load_triple_verifier(triple_verifier_path)

    certificate = json.loads(args.certificate.read_text(encoding="utf-8"))
    expected_certificate_fields = {
        "format": "parts509-six-exceptional-placements-minimum-v1",
        "canonical_event_order": [108, 109, 789, 215, 216, 690],
        "vertices": ALL_SIZE,
        "edges": 3354,
        "edge_sha256": EXPECTED_EDGE_SHA256,
        "common_L_vertices": L_SIZE,
        "extension_copy_size": EXTENSION_SIZE,
        "paired_forced_extension_positions": 96,
        "projected_free_positions": 63,
        "projected_transversal_number": 39,
        "transversal_number_outside_L": 135,
        "minimum_non_four_colorable_order": 509,
        "source_triple_certificate_sha256": EXPECTED_TRIPLE_CERTIFICATE_SHA256,
        "source_triple_verifier_sha256": EXPECTED_TRIPLE_VERIFIER_SHA256,
    }
    if any(certificate.get(key) != value for key, value in expected_certificate_fields.items()):
        raise AssertionError("six-placement certificate metadata mismatch")

    points_path = root / "hadwiger_nelson_parts509_completion_census_degree9" / "points.tsv"
    first_points, first_edges, first_placements, first_multiplicity = triple.build_union(points_path)
    second_points, second_edges, second_placements, second_multiplicity = triple.build_equivalent_union(points_path)
    if first_edges != second_edges or first_multiplicity != second_multiplicity:
        raise AssertionError("source extension copies are not canonically identical")
    scaled_first = [scale_point(point, 32) for point in first_points]
    if scaled_first[:L_SIZE] != second_points[:L_SIZE]:
        raise AssertionError("the two extension copies do not share the same L coordinates")
    points = scaled_first + second_points[L_SIZE:]
    if len(points) != ALL_SIZE or len(set(points)) != ALL_SIZE:
        raise AssertionError("six-placement point census mismatch")
    edges = triple.strict_edges(points, 96 * 64)
    if len(edges) != 3354 or triple.edge_digest(edges) != EXPECTED_EDGE_SHA256:
        raise AssertionError("six-placement edge census mismatch")

    first_induced = [(u, v) for u, v in edges if v < TRIPLE_SIZE]
    if first_induced != first_edges:
        raise AssertionError("first extension copy has the wrong induced edge list")
    cross_edges = [
        (u, v) for u, v in edges
        if L_SIZE <= u < TRIPLE_SIZE and v >= TRIPLE_SIZE
    ]
    if cross_edges:
        raise AssertionError("an unexpected cross-extension unit edge exists")
    second_induced = []
    for u, v in edges:
        if (u < L_SIZE or u >= TRIPLE_SIZE) and (v < L_SIZE or v >= TRIPLE_SIZE):
            mapped_u = u if u < L_SIZE else u - EXTENSION_SIZE
            mapped_v = v if v < L_SIZE else v - EXTENSION_SIZE
            second_induced.append(tuple(sorted((mapped_u, mapped_v))))
    if sorted(second_induced) != second_edges:
        raise AssertionError("second extension copy has the wrong induced edge list")
    edge_partition = {
        "inside_L": sum(v < L_SIZE for _, v in edges),
        "first_extension_contribution": sum(v >= L_SIZE and v < TRIPLE_SIZE for _, v in edges),
        "second_extension_contribution": sum(v >= TRIPLE_SIZE for _, v in edges),
        "cross_extension": len(cross_edges),
    }
    if edge_partition != {
        "inside_L": 1860,
        "first_extension_contribution": 747,
        "second_extension_contribution": 747,
        "cross_extension": 0,
    }:
        raise AssertionError("unexpected edge partition")

    edge_set = set(edges)
    placement_counts = {}
    for event, labels in first_placements.items():
        count, _ = triple.placement_edge_digest(labels, edge_set)
        placement_counts[event] = count
    for event, labels in second_placements.items():
        mapped = [vertex if vertex < L_SIZE else vertex + EXTENSION_SIZE for vertex in labels]
        count, _ = triple.placement_edge_digest(mapped, edge_set)
        placement_counts[event] = count
    if set(placement_counts) != {108, 109, 215, 216, 690, 789} or set(placement_counts.values()) != {2442}:
        raise AssertionError("a constituent placement has the wrong strict-edge count")

    triple_certificate = json.loads(triple_certificate_path.read_text(encoding="utf-8"))
    forced = triple_certificate["forced_vertices"]
    free = triple_certificate["free_vertices"]
    forced_set = set(forced)
    free_set = set(free)
    if set(range(L_SIZE)) - forced_set:
        raise AssertionError("a common L vertex is not forced in the triple")
    forced_extension = sorted(forced_set - set(range(L_SIZE)))
    if len(forced_extension) != 96 or len(free) != 63 or any(vertex < L_SIZE for vertex in free):
        raise AssertionError("unexpected triple extension partition")

    coloring_checks = 0
    forced_payload = base64.b64decode(triple_certificate["forced_colorings_base64"], validate=True)
    row_bytes = ((TRIPLE_SIZE - 1) + 3) // 4
    if len(forced_payload) != row_bytes * len(forced):
        raise AssertionError("source forced-colouring payload length mismatch")
    for row_index, deleted in enumerate(forced):
        payload = forced_payload[row_index * row_bytes : (row_index + 1) * row_bytes]
        packed_colors = triple.unpack_colors(payload, TRIPLE_SIZE - 1)
        active = [vertex for vertex in range(TRIPLE_SIZE) if vertex != deleted]
        colors = dict(zip(active, packed_colors, strict=True))
        lifted = lift_colors(colors)
        if deleted < L_SIZE:
            expected_active = set(range(ALL_SIZE)) - {deleted}
        else:
            expected_active = set(range(ALL_SIZE)) - {deleted, deleted + EXTENSION_SIZE}
        if set(lifted) != expected_active:
            raise AssertionError("a lifted forced colouring has the wrong domain")
        coloring_checks += triple.check_coloring(lifted, edges)

    identity_extension = set(first_placements[789]) - set(range(L_SIZE))
    if len(identity_extension) != 135 or not set(forced_extension) <= identity_extension:
        raise AssertionError("the identity placement does not select all forced extension positions")
    identity_projected_free = identity_extension & free_set
    if len(identity_projected_free) != 39:
        raise AssertionError("identity placement has the wrong projected free part")

    for row in triple_certificate["killing_sets"]:
        deleted = set(row["deleted"])
        if not deleted <= free_set:
            raise AssertionError("a source killing set leaves the free universe")
        active = [vertex for vertex in range(TRIPLE_SIZE) if vertex not in deleted]
        packed_colors = triple.unpack_colors(
            base64.b64decode(row["coloring_base64"], validate=True), len(active)
        )
        colors = dict(zip(active, packed_colors, strict=True))
        lifted = lift_colors(colors)
        doubled_deleted = deleted | {vertex + EXTENSION_SIZE for vertex in deleted}
        if set(lifted) != set(range(ALL_SIZE)) - doubled_deleted:
            raise AssertionError("a lifted killing-set colouring has the wrong domain")
        coloring_checks += triple.check_coloring(lifted, edges)
        if not identity_projected_free & deleted:
            raise AssertionError("the identity placement misses a projected killing set")

    # Every non-4-colourable induced subgraph contains all 374 common L
    # vertices. Its remaining vertices must hit 96 disjoint forced-position
    # twin pairs, and their projection on the other 63 twin positions must hit
    # the source hypergraph, whose checked transversal number is 39.
    lower_bound_outside_L = len(forced_extension) + triple_summary["transversal_number"]
    if lower_bound_outside_L != 135:
        raise AssertionError("derived outside-L lower bound mismatch")
    if L_SIZE + lower_bound_outside_L != 509:
        raise AssertionError("derived total lower bound mismatch")

    summary = {
        "all_checks": True,
        "vertices": len(points),
        "edges": len(edges),
        "edge_partition": edge_partition,
        "common_forced_vertices": L_SIZE,
        "paired_forced_extension_positions": len(forced_extension),
        "projected_free_positions": len(free),
        "projected_transversal_number": triple_summary["transversal_number"],
        "transversal_number_outside_L": lower_bound_outside_L,
        "minimum_non_four_colorable_order": 509,
        "lifted_coloring_edge_checks": coloring_checks,
        "edge_sha256": triple.edge_digest(edges),
        "source_triple_certificate_sha256": sha256(triple_certificate_path),
    }
    print(json.dumps(summary, sort_keys=True))


if __name__ == "__main__":
    main()
