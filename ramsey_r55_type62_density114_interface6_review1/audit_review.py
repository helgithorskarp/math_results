#!/usr/bin/env python3
"""Independent audit of the h3653 classification and interface-6 consumer.

The family-independent physical and literal-CNF routines are loaded from the
already published reviewer implementation used for interface 7, after an exact
source-hash check.  No module from the reviewed repository is imported.
"""

import argparse
import hashlib
import importlib.util
import itertools
import json
from pathlib import Path
import shutil


TARGET = "ramsey_r55_type62_density114_interface6"
UPSTREAM = "ramsey_r55_dense_degree23_hub_classification"
TARGET_SUMS_SHA256 = "da86f6dafaa912244a720e6ac5ea43e922c0d489c209a013b67cde71fc71b578"
INPUTS_SHA256 = "8e17676c21e4b9c5b03c21e6fdba25d9d9325b77d0f1ee4f2718681c7db2fca2"
CERTIFICATE_SHA256 = "39491fe6f15eb2ff887c0985cbbe50cced364a27047b7ead39427125f5b86cf8"
TUPLE_STREAM_SHA256 = "84f53e3e52093fd4a466251c12f3ae2e937f5f1166eeb372c08b52b9851fdec8"
TEMPLATE_STREAM_SHA256 = "a75d32a16ac21d8cda1b6e9ea8f9565692eae424d16208338fa0d73830bf24fa"
MANIFEST_SHA256 = "3834410d2a6bd7793f1306db96a34cd6501e6aa39b389e1fd925df31e70b2506"
COMMON_SHA256 = "d81fa53b8d3b97a710eba27714fbf38f61afbdec1760fa9001ff53a5a00d33ed"
SAMPLES = ((0, 0), (0, 1), (127, 0), (424, 1), (848, 0),
           (848, 1), (1272, 0), (1695, 1), (1696, 0), (1696, 1))


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def load_common():
    path = (Path(__file__).resolve().parents[1] /
            "ramsey_r55_type62_density114_interface7_review1" / "audit_review.py")
    if sha256(path.read_bytes()) != COMMON_SHA256:
        raise RuntimeError("pinned reviewer common implementation changed")
    spec = importlib.util.spec_from_file_location("type62_review_common", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def check_source(source, common):
    package = source / TARGET
    sums = package / "SHA256SUMS"
    common.require(sha256(sums.read_bytes()) == TARGET_SUMS_SHA256,
                   "target checksum list changed")
    names = []
    for line in sums.read_text().splitlines():
        expected, name = line.split("  ", 1)
        path = package / name
        common.require(path.is_file() and sha256(path.read_bytes()) == expected,
                       f"target source changed: {name}")
        names.append(name)
    common.require(len(names) == len(set(names)) == 18,
                   "unexpected target checksum scope")


def audit_replay(replay, expected_templates, common):
    cohort = replay / "cohort"
    manifest_raw = (cohort / "manifest.json").read_bytes()
    common.require(sha256(manifest_raw) == MANIFEST_SHA256, "manifest identity")
    manifest = json.loads(manifest_raw)
    runs = json.loads((cohort / "runs.json").read_bytes())
    result = json.loads((cohort / "result.json").read_bytes())
    keys = [[6, 62, j, k] for j in range(1697) for k in range(2)]
    common.require(len(manifest) == len(runs) == 3394 and
                   [row["key"] for row in manifest] ==
                   [row["key"] for row in runs] == keys,
                   "complete ordered replay cohort")
    common.require([{field: row[field] for field in
                     ("key", "variables", "clauses", "cnf_sha256", "matrix_sha256")}
                    for row in runs] == manifest, "run/manifest projection")
    common.require(result == {
        "complete_cases": 3394,
        "interface": 6,
        "kernel_edge_variables": 272,
        "kernel_vertices": 40,
        "manifest_sha256": MANIFEST_SHA256,
        "new_global_hub_deficiency_lower_bound": 9,
        "physical_free_edges": 389,
        "status": "VERIFIED_COMPLETE_INTERFACE6_TYPE62_DENSITY114_EXCLUSION",
        "unconstrained_outside_edges": 117,
    }, "terminal replay result")

    clause_counts = []
    matrix_hashes = set()
    cnf_hashes = set()
    proof_hashes = set()
    proof_bytes = 0
    for row, run, expected in zip(manifest, runs, expected_templates):
        key = tuple(row["key"])
        stem = "-".join(map(str, key))
        saved = (cohort / f"{stem}.matrix").read_bytes()
        common.require(saved == expected and sha256(expected) == row["matrix_sha256"],
                       f"matrix mismatch: {stem}")
        common.require(row["variables"] == 389 and 19126 <= row["clauses"] <= 19340,
                       f"formula dimensions: {stem}")
        common.require((cohort / f"{stem}.solver.log").read_text().rstrip().endswith(
            "c exit 20"), f"solver terminal status: {stem}")
        common.require("s VERIFIED" in (cohort / f"{stem}.check.log").read_text(),
                       f"checker terminal status: {stem}")
        common.require(run["proof_bytes"] > 0 and len(run["proof_sha256"]) == 64,
                       f"proof checkpoint: {stem}")
        clause_counts.append(row["clauses"])
        matrix_hashes.add(row["matrix_sha256"])
        cnf_hashes.add(row["cnf_sha256"])
        proof_hashes.add(run["proof_sha256"])
        proof_bytes += run["proof_bytes"]
    common.require(min(clause_counts) == 19126 and max(clause_counts) == 19340 and
                   sum(clause_counts) == 65215510, "clause census")
    common.require(len(matrix_hashes) == len(cnf_hashes) == 3394,
                   "matrix/formula distinctness census")
    common.require(len(proof_hashes) == 3374, "proof-hash census")
    common.require(proof_bytes == 152151217, "proof-byte census")
    return {tuple(row["key"]): row for row in manifest}, proof_bytes


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--replay", type=Path, required=True)
    parser.add_argument("--scratch", type=Path, required=True)
    parser.add_argument("--kissat", required=True)
    parser.add_argument("--drat-trim", required=True)
    args = parser.parse_args()
    common = load_common()
    source = args.source.resolve()
    replay = args.replay.resolve()
    scratch = args.scratch.resolve()
    common.require(not scratch.exists(), "scratch directory must be new")
    scratch.mkdir(parents=True)
    try:
        check_source(source, common)
        inputs = common.pinned_json(source / UPSTREAM / "inputs.json", INPUTS_SHA256)
        certificate = common.pinned_json(source / TARGET / "certificate.json",
                                         CERTIFICATE_SHA256)
        edges = common.graph6(inputs["interfaces"][6])
        marks = common.markings(edges)
        rows = common.classification_rows(certificate)

        expected_templates = []
        sample_fixed = {}
        stream = hashlib.sha256()
        for j, row in enumerate(rows):
            for k, mark in enumerate(marks):
                key = (6, 62, j, k)
                raw, fixed = common.template(edges, mark, row["columns"])
                expected_templates.append(raw)
                stream.update((" ".join(map(str, key)) + "\n").encode())
                stream.update(bytes(value - 48 for value in raw))
                if (j, k) in SAMPLES:
                    sample_fixed[key] = fixed
        common.require(len(set(expected_templates)) == 3394, "template distinctness")
        common.require(stream.hexdigest() == TEMPLATE_STREAM_SHA256,
                       "template stream identity")
        manifest, replay_proof_bytes = audit_replay(replay, expected_templates, common)

        sample_clauses = 0
        sample_proof_bytes = 0
        for j, k in SAMPLES:
            key = (6, 62, j, k)
            cnf, count = common.literal_cnf(sample_fixed[key])
            common.require(count == manifest[key]["clauses"] and
                           sha256(cnf) == manifest[key]["cnf_sha256"],
                           f"independent formula mismatch: {key}")
            sample_clauses += count
            sample_proof_bytes += common.prove(
                cnf, scratch, "-".join(map(str, key)), args.kissat, args.drat_trim)

        enumeration = json.loads((replay / "enumeration.json").read_bytes())
        classification = json.loads((replay / "classification.json").read_bytes())
        common.require(enumeration == {"type": 62, "columns": 7225,
                                      "outer_pairs": 793798,
                                      "c4_pairs": 194750300,
                                      "labeled_tuples": 461584},
                       "enumeration replay")
        common.require(classification.get("status") ==
                       "VERIFIED_COMPLETE_TYPE62_DENSITY114_CLASSIFICATION" and
                       classification.get("classes") == 1697 and
                       classification.get("labeled_tuples") == 461584 and
                       classification.get("full_tuple_sha256") == TUPLE_STREAM_SHA256 and
                       classification.get("paley_automorphisms") == 136 and
                       classification.get("s_automorphisms") == 2 and
                       classification.get("all_rigid") is True and
                       classification.get("all_unique_hub") is True,
                       "classification audit replay")

        report = {
            "status": "VERIFIED_REVIEW_CHECKPOINT_INTERFACE6_DENSITY114",
            "reviewed_source_commit": "607d56027ae008e1b02ee1d351e8f9cf9757b752",
            "reviewer_common_sha256": COMMON_SHA256,
            "classification": {
                "classes": 1697,
                "labeled_tuples": 461584,
                "orbit_size": 272,
                "all_representatives_directly_checked_R45_23": True,
                "complete_tuple_stream_sha256": TUPLE_STREAM_SHA256,
            },
            "interface": {"number": 6, "vertices": 22, "red_edges": 109,
                          "type62_markings": 2},
            "cohort": {
                "cases": 3394,
                "physical_free_edges": 389,
                "kernel_variables_used": 272,
                "outside_variables_unused": 117,
                "clauses_min": 19126,
                "clauses_max": 19340,
                "clauses_total": 65215510,
                "all_saved_matrices_reconstructed": True,
                "all_solver_logs_unsat": True,
                "all_checker_logs_verified": True,
                "full_replay_proof_bytes": replay_proof_bytes,
                "manifest_sha256": MANIFEST_SHA256,
                "template_stream_sha256": TEMPLATE_STREAM_SHA256,
            },
            "independent_cnf_sample": {
                "cases": len(SAMPLES),
                "keys": [[6, 62, j, k] for j, k in SAMPLES],
                "clauses_total": sample_clauses,
                "all_hashes_match": True,
                "all_new_drat_proofs_verified": True,
                "new_proof_bytes": sample_proof_bytes,
            },
            "scope": {
                "classification_and_interface6_density114_exclusion": "accepted",
                "interfaces6_7_8_density114_layer_independently_accepted": True,
                "ramsey_5_5_lower_bound_changed": False,
            },
        }
        print(json.dumps(report, indent=2, sort_keys=True))
    finally:
        shutil.rmtree(scratch, ignore_errors=True)


if __name__ == "__main__":
    main()
