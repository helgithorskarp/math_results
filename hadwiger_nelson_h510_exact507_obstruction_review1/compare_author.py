#!/usr/bin/env python3
"""Optional entry-level comparison with the submitted candidate generator.

The primary checker is clean-room and never imports the submission.  This
secondary regression check intentionally imports it and confirms equality of
the three complete, canonical candidate-partition lists, not merely totals.
"""

from __future__ import annotations

from hashlib import sha256
import importlib.util
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent / "hadwiger_nelson_h510_exact507_obstruction" / "verify.py"


def require(condition, message):
    if not condition:
        raise ValueError(message)


def load_source():
    expected_hash = json.loads((HERE / "inputs.json").read_text())["../hadwiger_nelson_h510_exact507_obstruction/verify.py"]
    require(sha256(SOURCE.read_bytes()).hexdigest() == expected_hash, "submitted verifier hash")
    spec = importlib.util.spec_from_file_location("submitted_h510_exact507", SOURCE)
    require(spec is not None and spec.loader is not None, "submitted verifier import")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def partition_hash(partitions):
    digest = sha256()
    for groups in sorted(partitions):
        digest.update((json.dumps(groups, separators=(",", ":")) + "\n").encode())
    return digest.hexdigest()


def main():
    source = load_source()
    edges, certificate, parent_hash = source.load_parent()
    adjacency, rhombi, opposite_row = source.graph_data(edges)
    masks = source.row_masks(certificate, rhombi)
    covers = source.covering_row_triples(masks)
    three_pairs = source.three_pair_partitions(adjacency, rhombi, masks, covers, certificate)
    triple_pair, full_triples = source.triple_pair_partitions(adjacency, rhombi, opposite_row, masks)
    quadruples, dense_count = source.quadruple_partitions(
        adjacency, rhombi, opposite_row, masks, covers, full_triples, certificate
    )

    expected = json.loads((HERE / "expected.json").read_text())
    families = {
        "three_pairs": three_pairs,
        "triple_pair": triple_pair,
        "quadruple": quadruples,
    }
    result = {
        "status": "AUTHOR_AND_REVIEW_CANDIDATE_LISTS_IDENTICAL",
        "parent_certificate_sha256": parent_hash,
        "dense_quadruples_examined": dense_count,
        "families": {},
    }
    for name, partitions in families.items():
        digest = partition_hash(partitions)
        expected_family = expected["rank_defect_families"][name]
        require(len(partitions) == expected_family["candidates"], name + " count")
        require(digest == expected_family["partition_sha256"], name + " partition hash")
        result["families"][name] = {"candidates": len(partitions), "partition_sha256": digest}
    require(dense_count == expected["dense_quadruples_examined"], "dense quadruple count")

    expected_comparison_path = HERE / "comparison_expected.json"
    if expected_comparison_path.exists():
        require(result == json.loads(expected_comparison_path.read_text()), "comparison expected output")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
