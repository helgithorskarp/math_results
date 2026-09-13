#!/usr/bin/env python3
"""Exact positive audit and optional inherited DRAT check for Parts574."""
from __future__ import annotations

import argparse
import base64
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import tempfile

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
PARENT = REPO / "hadwiger_nelson_parts509_pool_obstruction574"
GEOMETRY = (REPO /
    "hadwiger_nelson_parts509_pool_shape6_review1/independent_check.py")


def need(condition, message):
    if not condition:
        raise ValueError(message)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def unpack(data, length):
    raw = base64.b64decode(data, validate=True)
    need(len(raw) == (length + 3) // 4, "packed length")
    word = "".join(str((raw[i // 4] >> (2 * (i % 4))) & 3)
                   for i in range(length))
    need(not (length % 4) or
         raw[-1] >> (2 * (length % 4)) == 0, "packed padding")
    return word


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def compute(certificate_path):
    certificate = json.loads(certificate_path.read_text())
    need(certificate["schema"] == "parts574-L-indispensability-v1",
         "certificate schema")
    pins = certificate["source_pins"]
    sources = {
        "parent_certificate.json": PARENT / "certificate.json",
        "parent_expected.json": PARENT / "expected.json",
        "parent_proof_manifest.json": PARENT / "proof_manifest.json",
        "exact_geometry_reader.py": GEOMETRY,
    }
    for name, path in sources.items():
        need(digest(path) == pins[name], f"source changed: {name}")

    parent_verify = load_module("parent_verify", PARENT / "verify.py")
    parent_facts, parent_cnf = parent_verify.compute()
    need(parent_facts["vertices"] == 574 and
         parent_facts["edges"] == 2707 and
         parent_facts["pool_deletion_colourings_verified"] == 200,
         "parent positive certificate changed")

    parent_certificate = json.loads((PARENT / "certificate.json").read_text())
    labels = list(range(374)) + parent_certificate["pool_labels"]
    label_set = set(labels)
    geometry = load_module("exact_geometry", GEOMETRY)
    _, points, _, _, all_edges = geometry.read_geometry()
    need(len(labels) == len(set(labels)) == 574, "graph label count")
    need(len({points[v] for v in labels}) == 574, "coordinate collision")
    edges = [(a, b) for a, b in all_edges
             if a in label_set and b in label_set]
    need(len(edges) == 2707, "strict unit-edge count")

    rows = certificate["L_deletion_colourings"]
    need([row["removed"] for row in rows] == list(range(374)),
         "L deletion coverage")
    edge_checks = 0
    for row in rows:
        removed = row["removed"]
        active = [v for v in labels if v != removed]
        word = unpack(row["colouring_2bit"], 573)
        colours = dict(zip(active, word))
        need(set(colours) == label_set - {removed}, "colour domain")
        for a, b in edges:
            if removed not in (a, b):
                edge_checks += 1
                need(colours[a] != colours[b],
                     f"monochromatic edge after deleting {removed}")

    proof_manifest = json.loads((PARENT / "proof_manifest.json").read_text())
    need(proof_manifest["cnf_sha256"] == hashlib.sha256(parent_cnf).hexdigest(),
         "parent CNF/proof link")
    need(proof_manifest["drat_verified"] is True and
         proof_manifest["status"] == "FULL GRAPH DRAT VERIFIED",
         "parent proof status")
    result = {
        "status": "ALL_574_SINGLE_VERTEX_DELETIONS_HAVE_CHECKED_4_COLOURINGS",
        "vertices": 574,
        "edges": 2707,
        "distinct_exact_points": 574,
        "L_deletion_colourings_verified": 374,
        "pool_deletion_colourings_in_parent_verified": 200,
        "all_single_vertex_deletions_verified": 574,
        "new_L_deletion_edge_checks": edge_checks,
        "parent_non_four_proof_manifest_linked": True,
        "parent_non_four_proof_rechecked_now": False,
        "conclusion": "with the inherited checked non-four proof, the graph is vertex-critical and has no proper non-four-colourable induced subgraph",
        "scope": "induced subgraphs of the exact 574-point Parts pool obstruction",
    }
    return result, parent_cnf


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--certificate", type=Path,
                        default=HERE / "certificate.json")
    parser.add_argument("--proof", type=Path)
    parser.add_argument("--drat-trim", type=Path)
    args = parser.parse_args()
    need(bool(args.proof) == bool(args.drat_trim),
         "supply both proof and drat-trim")
    result, parent_cnf = compute(args.certificate)
    if args.proof:
        with tempfile.TemporaryDirectory(prefix="parts574-L-proof-") as directory:
            cnf_path = Path(directory) / "parent.cnf"
            cnf_path.write_bytes(parent_cnf)
            check = subprocess.run(
                [str(args.drat_trim.resolve()), str(cnf_path),
                 str(args.proof.resolve())], capture_output=True, text=True)
        need(check.returncode == 0 and "s VERIFIED" in check.stdout,
             "parent DRAT did not verify")
        result["parent_non_four_proof_rechecked_now"] = True
        result["proof_sha256"] = digest(args.proof)
        result["status"] = "VERIFIED_574_VERTEX_CRITICAL_UNIT_DISTANCE_GRAPH"
    expected_path = HERE / "expected.json"
    if expected_path.exists() and not args.proof:
        need(result == json.loads(expected_path.read_text()),
             "result differs from expected.json")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    try:
        main()
    except (ValueError, KeyError, TypeError, json.JSONDecodeError) as error:
        print(f"verification failed: {error}")
        raise SystemExit(1)
