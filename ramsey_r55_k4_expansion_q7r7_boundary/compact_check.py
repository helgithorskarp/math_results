#!/usr/bin/env python3
"""Check the compact identities and exact UNKNOWN boundary without solving."""
from pathlib import Path
import hashlib
import json

HERE = Path(__file__).resolve().parent


def need(ok, message):
    if not ok:
        raise ValueError(message)


def digest(path):
    value = hashlib.sha256()
    with Path(path).open("rb") as stream:
        while chunk := stream.read(1024 * 1024):
            value.update(chunk)
    return value.hexdigest()


def manifest():
    count = 0
    for line in (HERE / "SHA256SUMS").read_text().splitlines():
        wanted, name = line.split("  ", 1)
        need(digest(HERE / name) == wanted, "package identity " + name)
        count += 1
    return count


def run():
    result = json.loads((HERE / "RESULT.json").read_text())
    gate = json.loads((HERE / "GATE.json").read_text())
    frozen = json.loads((HERE / "FROZEN.json").read_text())
    formula = json.loads((HERE / "FORMULA_AUDIT.json").read_text())
    comparison = json.loads((HERE / "COMPARISON.json").read_text())
    controls = json.loads((HERE / "CONTROLS.json").read_text())
    evidence = json.loads((HERE / "EVIDENCE.json").read_text())
    need(result["status"] == "AUDITED_K4_EXPANSION_Q7R7_UNKNOWN_BOUNDARY", "result status")
    need(result["task"] == formula["task"] == gate["task"] == frozen["task"] ==
         "bo1-q7-r7-c000000", "task identity")
    need(result["solver_status"] == frozen["outcome"] == "UNKNOWN", "outcome")
    need(result["solver"]["exit_code"] == 0 and result["solver_calls"] ==
         gate["solver_calls_max"] == frozen["solver_calls"] == 1, "single solver call")
    need(result["solver"]["seconds_limit"] == gate["solver_wall_seconds_max"] ==
         frozen["seconds_limit"] == 1800, "time boundary")
    need(not result["candidate_found"] and not result["target43_found"], "no target")
    need(not result["branch_excluded"] and result["tasks_decided"] == 0, "no exclusion")
    need(result["tasks_remaining"] == 2189178, "remaining tasks")
    need(result["witness"]["content"] == "c UNKNOWN\n", "witness content")
    need(result["witness"]["bytes"] == 10 and result["witness"]["sha256"] ==
         hashlib.sha256(b"c UNKNOWN\n").hexdigest(), "witness identity")
    need(not result["partial_drat"]["is_certificate"] and
         not result["partial_drat"]["checked"] and
         not result["partial_drat"]["published"], "partial proof scope")
    for key in ("variables", "clauses", "max_width", "bytes", "sha256"):
        need(result["cnf"][key] == formula[key], "formula " + key)
    need(result["cnf"]["sha256"] == gate["input_formula_sha256"] ==
         frozen["formula_sha256"], "formula identity")
    need(result["solver"]["sha256"] == gate["solver_sha256"], "solver identity")
    need(digest(HERE / "run_decision.py") == frozen["runner_sha256"], "runner identity")
    base, expanded = comparison["base_h3893"], comparison["expanded"]
    diagnostics = result["diagnostics"]
    for key in ("conflicts", "decisions", "propagations"):
        need(expanded[key] == diagnostics[key], "expanded diagnostic " + key)
        need(comparison["expanded_minus_base"][key] == expanded[key] - base[key],
             "diagnostic delta " + key)
        expected = (expanded[key] / base[key] - 1) * 100
        need(comparison["expanded_percent_change"][key] == expected,
             "diagnostic percentage " + key)
    need(base["solver_status"] == expanded["solver_status"] == "UNKNOWN", "comparison outcomes")
    need(comparison["monolithic_tractability_gate_passed"] is False, "tractability scope")
    need(controls == {"cases": 6, "status": "VERIFIED_FAIL_CLOSED_RESULT_CLASSIFIER"},
         "classifier controls")
    need(evidence["formula_audit_sha256"] == digest(HERE / "FORMULA_AUDIT.json"), "formula audit hash")
    need(evidence["comparison_sha256"] == digest(HERE / "COMPARISON.json"), "comparison hash")
    need(evidence["gate_sha256"] == digest(HERE / "GATE.json"), "gate hash")
    need(evidence["frozen_sha256"] == digest(HERE / "FROZEN.json"), "frozen hash")
    need(evidence["runner_sha256"] == digest(HERE / "run_decision.py"), "runner hash")
    need(evidence["result_sha256"] == digest(HERE / "RESULT.json"), "result hash")
    need(evidence["controls_sha256"] == digest(HERE / "CONTROLS.json"), "controls hash")
    return {
        "status": "VERIFIED_K4_EXPANSION_Q7R7_UNKNOWN_BOUNDARY",
        "manifest_entries": manifest(),
        "solver_status": "UNKNOWN",
        "solver_calls_replayed": 0,
        "target43_found": False,
        "task_excluded": False,
        "monolithic_tractability_gate_passed": False
    }


if __name__ == "__main__":
    print(json.dumps(run(), sort_keys=True))
