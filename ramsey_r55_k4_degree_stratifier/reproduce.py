#!/usr/bin/env python3
"""Rebuild and independently audit the degree-stratified formula; no solver."""
from pathlib import Path
import argparse
import hashlib
import json
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent
TASK = "bo1-q7-r7-c000000"


def need(ok, message):
    if not ok:
        raise ValueError(message)


def digest(path):
    value = hashlib.sha256()
    with Path(path).open("rb") as stream:
        while chunk := stream.read(1024 * 1024):
            value.update(chunk)
    return value.hexdigest()


def package_identity():
    rows = (HERE / "SHA256SUMS").read_text().splitlines()
    for row in rows:
        wanted, name = row.split("  ", 1)
        need(digest(HERE / name) == wanted, "package identity " + name)
    return len(rows)


def command(optimized, script, *arguments):
    result = [sys.executable]
    if optimized:
        result.append("-O")
    result.extend(["-B", str(script), *map(str, arguments)])
    return result


def output(optimized, script, *arguments):
    return subprocess.run(command(optimized, script, *arguments), check=True,
                          text=True, stdout=subprocess.PIPE).stdout


def run(cache):
    theorem = json.loads((HERE / "THEOREM.json").read_text())
    controls = json.loads((HERE / "CONTROLS.json").read_text())
    dimensions = json.loads((HERE / "DIMENSIONS.json").read_text())
    expected_integration = json.loads((HERE / "INTEGRATION.json").read_text())
    signal = json.loads((HERE / "SIGNAL.json").read_text())
    expected_formula = json.loads((HERE / "FORMULA_AUDIT.json").read_text())
    for optimized in (False, True):
        need(json.loads(output(optimized, HERE / "derive.py")) == theorem,
             "theorem reproduction")
        need(json.loads(output(optimized, HERE / "controls.py")) == controls,
             "control reproduction")
        need(json.loads(output(optimized, HERE / "dimensions.py")) == dimensions,
             "dimension reproduction")
        need(json.loads(output(optimized, HERE / "projection.py")) == signal,
             "signal reproduction")
    with tempfile.TemporaryDirectory(prefix="r55-k4-degree-") as raw:
        cnf = Path(raw) / "formula.cnf"
        produced = json.loads(output(False, HERE / "stratify.py", cache,
                              "--task", TASK, "--triangles", "--cnf", cnf))
        for key in ("variables", "clauses", "physical_variables",
                    "k4_expansion_variables", "k4_expansion_clauses",
                    "degree_counter_variables", "degree_counter_clauses",
                    "degree_window_clauses", "degree_guard_variables",
                    "degree_guard_clauses", "contact_stratum_clauses",
                    "max_width", "bytes", "sha256"):
            need(produced[key] == expected_formula[key], "producer field " + key)
        audits = []
        for optimized in (False, True):
            audits.append(json.loads(output(optimized, HERE / "audit.py",
                          "--cache", cache, "--task", TASK, "--triangles",
                          "--cnf", cnf)))
        need(audits[0] == audits[1] == expected_formula,
             "independent literal audits")
    integration = []
    compact = []
    for optimized in (False, True):
        integration.append(json.loads(output(optimized, HERE / "integration.py", cache)))
        compact.append(json.loads(output(optimized, HERE / "check.py")))
    need(integration[0] == integration[1] == expected_integration,
         "macro-class integration modes")
    need(integration[0]["macro_classes"] == 18, "macro-class integration")
    need(compact[0] == compact[1], "compact check modes")
    return {
        "status": "REPRODUCED_K4_DEGREE_STRATIFIER",
        "package_manifest_entries": package_identity(),
        "theorem_modes": 2,
        "control_modes": 2,
        "literal_audit_modes": 2,
        "macro_class_integration_modes": 2,
        "compact_check_modes": 2,
        "formula_sha256": expected_formula["sha256"],
        "formula_variables": expected_formula["variables"],
        "formula_clauses": expected_formula["clauses"],
        "minimum_unconditional_contacts": 22,
        "solver_calls": 0,
        "tasks_decided": 0,
        "target43_found": False,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("cache", type=Path)
    args = parser.parse_args()
    print(json.dumps(run(args.cache), sort_keys=True))
