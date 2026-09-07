#!/usr/bin/env python3
"""Check the compact evidence for the all-row support-eight UNKNOWN boundary."""

from __future__ import annotations

from hashlib import sha256
import argparse
import json
from pathlib import Path


def digest(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("root", type=Path, nargs="?", default=Path(__file__).parent)
    parser.add_argument("--cover", type=Path)
    args = parser.parse_args()
    root = args.root.resolve()
    cover = args.cover or root.parent / "ramsey_r55_rank4_complete_task_cover" / "row_cover.tsv"
    frozen = json.loads((root / "frozen-run.json").read_text())
    evidence = json.loads((root / "EVIDENCE.json").read_text())
    result = json.loads((root / "RESULT.json").read_text())
    production = json.loads((root / "production-result.json").read_text())
    metadata = json.loads((root / "metadata.json").read_text())
    audit = json.loads((root / "audit.json").read_text())
    controls = json.loads((root / "controls.json").read_text())

    for name, expected in frozen["inputs"].items():
        if digest(root / name) != expected:
            raise AssertionError(("frozen input", name))
    if digest(root / "frozen-run.json") != evidence["frozen_run_sha256"]:
        raise AssertionError("frozen manifest hash")
    if digest(root / "production-result.json") != evidence["production_result_sha256"]:
        raise AssertionError("production record hash")
    if digest(root / "audit.json") != evidence["audit_sha256"]:
        raise AssertionError("audit hash")
    if digest(root / "controls.json") != evidence["controls_sha256"]:
        raise AssertionError("controls hash")
    if digest(cover) != frozen["row_cover_sha256"]:
        raise AssertionError("row-cover hash")

    formula = metadata["formula"]
    expected_formula = {
        "bytes": 138709891,
        "clauses": 2462655,
        "sha256": "e01a3aec66bf8d3bd0ce8aba611634abc3f5068ad6ad56511be00186d6832989",
        "variables": 147595,
    }
    for key, value in expected_formula.items():
        if formula[key] != value or audit["formula"][key] != value:
            raise AssertionError(("formula", key))
    if result["formula"]["sha256"] != expected_formula["sha256"]:
        raise AssertionError("result formula hash")
    if production["cnf_sha256"] != expected_formula["sha256"]:
        raise AssertionError("production formula hash")
    if production["status"] != "UNKNOWN" or production["solver_exit"] != 0:
        raise AssertionError("production verdict")
    if result["status"] != "AUDITED_ALL_ROW_SUPPORT8_FORMULA_UNKNOWN_AT_900_SECONDS":
        raise AssertionError("result status")
    if result["target43_found"] or result["whole_family_excluded"]:
        raise AssertionError("false mathematical verdict")
    if evidence["candidate_file_created"] or evidence["checker_run"]:
        raise AssertionError("unexpected candidate or checker")
    witness = evidence["witness"]["content"].encode()
    if len(witness) != evidence["witness"]["bytes"] or sha256(witness).hexdigest() != evidence["witness"]["sha256"]:
        raise AssertionError("witness record")
    if evidence["partial_drat"]["is_certificate"] or evidence["partial_drat"]["published"]:
        raise AssertionError("partial proof status")
    if controls["status"] != "VERIFIED_ALL_ROW_SUPPORT8_ENCODING_CONTROLS":
        raise AssertionError("controls status")
    if audit["status"] != "INDEPENDENT_AUDIT_ALL_ROW_SUPPORT8_PHYSICAL_FORMULA":
        raise AssertionError("audit status")
    print(json.dumps({
        "status": "VERIFIED_COMPACT_ALL_ROW_SUPPORT8_UNKNOWN_BOUNDARY",
        "canonical_row_tasks": result["scope"]["canonical_row_tasks"],
        "cnf_sha256": expected_formula["sha256"],
        "solver_status": production["status"],
        "target43_found": False,
        "whole_family_excluded": False,
    }, sort_keys=True))


if __name__ == "__main__":
    main()
