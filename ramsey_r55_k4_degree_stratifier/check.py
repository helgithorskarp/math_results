#!/usr/bin/env python3
"""Compact evidence and identity checker; no cache or solver required."""
from pathlib import Path
import hashlib
import json
import controls
import derive
import dimensions
import projection
import source

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
    evidence = json.loads((HERE / "EVIDENCE.json").read_text())
    theorem = json.loads((HERE / "THEOREM.json").read_text())
    control = json.loads((HERE / "CONTROLS.json").read_text())
    dims = json.loads((HERE / "DIMENSIONS.json").read_text())
    integration = json.loads((HERE / "INTEGRATION.json").read_text())
    observed = json.loads((HERE / "SIGNAL.json").read_text())
    formula = json.loads((HERE / "FORMULA_AUDIT.json").read_text())
    gate = json.loads((HERE / "GATE.json").read_text())
    need(theorem == derive.run(), "signature theorem")
    need(control == controls.run(), "propagation controls")
    need(dims == dimensions.run(), "generic dimensions")
    need(integration["status"] == "VERIFIED_ALL_MACRO_CLASS_INSTANTIATIONS" and
         integration["macro_classes"] == 18 and len(integration["rows"]) == 18,
         "macro-class integration")
    need(observed == projection.run(), "propagation signal")
    need(theorem["unconditional_minimum_contacts"] == 22, "contact floor")
    need([row["minimum_contacts"] for row in theorem["rows"]] ==
         [22, 24, 26, 28, 30, 32, 34], "degree strata")
    need(observed["new_unconditional_conflict_after_fixed_noncontacts"] == 18,
         "conflict boundary")
    need(formula["variables"] == 43622 and formula["clauses"] == 1051035 and
         formula["max_width"] == 8, "formula dimensions")
    need(formula["k4_expansion_clauses"] + formula["degree_counter_clauses"] +
         formula["degree_window_clauses"] + formula["degree_guard_clauses"] +
         formula["contact_stratum_clauses"] == formula["clauses"],
         "clause partition")
    need(formula["k4_expansion_variables"] + formula["degree_counter_variables"] +
         formula["degree_guard_variables"] == formula["variables"],
         "variable partition")
    for field, name in (("theorem_sha256", "THEOREM.json"),
                        ("controls_sha256", "CONTROLS.json"),
                        ("dimensions_sha256", "DIMENSIONS.json"),
                        ("integration_sha256", "INTEGRATION.json"),
                        ("signal_sha256", "SIGNAL.json"),
                        ("formula_audit_sha256", "FORMULA_AUDIT.json"),
                        ("gate_sha256", "GATE.json")):
        need(evidence[field] == digest(HERE / name), "evidence hash " + name)
    need(evidence["formula_sha256"] == formula["sha256"], "formula hash")
    need(evidence["physical_tasks"] == dims["physical_tasks"] == 2189178,
         "task coverage")
    need(not evidence["target43_found"] and evidence["tasks_decided"] == 0,
         "result scope")
    need(gate["physical_solver_calls"] == evidence["solver_calls"] == 0,
         "no solver")
    source.load()
    return {
        "status": "VERIFIED_COMPACT_K4_DEGREE_STRATIFIER",
        "package_manifest_entries": manifest(),
        "dependency_packages": 4,
        "macro_classes": 18,
        "physical_tasks": 2189178,
        "minimum_unconditional_contacts": 22,
        "solver_calls": 0,
        "tasks_decided": 0,
        "target43_found": False,
    }


if __name__ == "__main__":
    print(json.dumps(run(), sort_keys=True))
