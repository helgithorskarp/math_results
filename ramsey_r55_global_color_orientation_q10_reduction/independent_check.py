#!/usr/bin/env python3
"""Independent reader for an analyzer result; imports no producer code."""
from collections import Counter
from itertools import combinations
from pathlib import Path
import hashlib
import json
import re
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def need(condition, message):
    if not condition:
        raise ValueError(message)


def digest(strings):
    return hashlib.sha256("".join(x + "\n" for x in sorted(strings)).encode()).hexdigest()


def independently_rederive():
    dependencies = json.loads((HERE / "DEPENDENCIES.json").read_text())
    for relative, metadata in dependencies.items():
        need(hashlib.sha256((ROOT / relative).read_bytes()).hexdigest() ==
             metadata["sha256"], "dependency identity: " + relative)

    ledger = json.loads((ROOT / "ramsey_r55_q10_recovered_cube_refutations" /
                         "TASKS.json").read_text())
    historical = json.loads((ROOT / "ramsey_r55_q10_recovered_cube_refutations" /
                             "REDUCTION.json").read_text())
    degree_source = json.loads((ROOT / "ramsey_r55_q10_regular_cnf_reduction" /
                                "REDUCTION.json").read_text())

    need(len(ledger) == 260, "260 rows")
    need(len({row["id"] for row in ledger}) == 260, "unique ids")
    pattern = re.compile(r"^(d(?:20-22|22-20))-w(\d{2})-p([01])$")
    coordinates = set()
    for row in ledger:
        match = pattern.fullmatch(row["id"])
        need(match is not None, "task id grammar")
        need(match.group(1) == row["branch"], "task id branch")
        coordinate = (row["branch"], int(match.group(2)), int(match.group(3)))
        need(coordinate not in coordinates, "duplicate coordinate")
        coordinates.add(coordinate)
    expected_coordinates = {(branch, word_index, polarity)
                            for branch in ("d20-22", "d22-20")
                            for word_index in range(65) for polarity in range(2)}
    need(coordinates == expected_coordinates, "complete 2*65*2 coordinate grid")

    status = Counter(row["status"] for row in ledger)
    need(status == {"CERTIFIED_UNSAT": 99, "UNKNOWN": 161}, "status census")
    degree = {row["branch"]: int(row["red_degree"])
              for row in degree_source["rows"]
              if row["branch"] in ("d20-22", "d22-20")}
    need(degree == {"d20-22": 20, "d22-20": 22}, "degree interface")

    n = 43
    universe = len(tuple(combinations(range(n), 2)))
    need(universe == 903 and universe % 2 == 1, "odd edge universe")
    cutoff = universe // 2
    active, redirected = [], []
    branch_report = {}
    for branch in ("d20-22", "d22-20"):
        d = degree[branch]
        need((n * d) % 2 == 0, "handshake parity")
        edges = n * d // 2
        complement_degree = (n - 1) - d
        complement_edges = n * complement_degree // 2
        need(edges + complement_edges == universe, "complement handshake")
        ids = [row["id"] for row in ledger
               if row["status"] == "UNKNOWN" and row["branch"] == branch]
        if edges <= cutoff:
            active.extend(ids)
            disposition = "TARGET_ACTIVE_ORIENTATION"
        else:
            redirected.extend(ids)
            disposition = "COLOR_COMPLEMENT_REDIRECT"
        branch_report[branch] = (d, edges, complement_degree,
                                 complement_edges, disposition, len(ids))

    need(len(active) == 67, "active count")
    need(len(redirected) == 94, "redirect count")
    need(set(active).isdisjoint(redirected), "disjoint disposition sets")
    need(len(active) + len(redirected) == 161, "complete UNKNOWN partition")
    need(historical["physical_cover"] == {
        "d20-22": {"certified_unsat": 63, "physical_tasks": 130, "unknown": 67},
        "d22-20": {"certified_unsat": 36, "physical_tasks": 130, "unknown": 94},
    }, "historical branch totals")

    proof = (ROOT / "ramsey_r55_global_maximal_packing" / "PROOF.md").read_text()
    review = (ROOT / "ramsey_r55_global_maximal_packing_review1" /
              "README.md").read_text()
    need("Every good43 has a labeling in this family" in proof or
         "disjunction" in proof, "complete-carrier theorem text")
    need("**ACCEPT**" in review and "if a good43 graph exists" in review,
         "independent acceptance text")

    return {
        "active_ids_sha256": digest(active),
        "branch_report": {branch: {
            "complement_degree": values[2], "complement_edges": values[3],
            "disposition": values[4], "red_degree": values[0],
            "red_edges": values[1], "unknown": values[5],
        } for branch, values in branch_report.items()},
        "certified_unsat_unchanged": status["CERTIFIED_UNSAT"],
        "complete_unknown_partition": True,
        "redirect_ids_sha256": digest(redirected),
        "redirected": len(redirected),
        "retained": len(active),
        "source_unknown_unchanged": status["UNKNOWN"],
    }


def check(result_path):
    result = json.loads(Path(result_path).read_text())
    audit = independently_rederive()
    queue = result["oriented_q10_unknown_queue"]
    need(result["status"] ==
         "CERTIFIED_GLOBAL_COLOR_ORIENTATION_EFFECT_ON_H3987_UNKNOWN_LEDGER",
         "result status")
    need(result["color_orbit"] == {
        "canonical_rule": "retain the representative with red_edges <= 451",
        "cutoff": 451, "fixed_orbits_possible": False,
        "order": 43, "total_edges": 903,
    }, "orbit data")
    need(queue["target_active_orientation"] == audit["retained"], "retained result")
    need(queue["color_complement_redirect"] == audit["redirected"], "redirect result")
    need(queue["source_unknown"] == audit["source_unknown_unchanged"], "source total")
    need(queue["active_ids_sha256"] == audit["active_ids_sha256"], "active identity")
    need(queue["redirect_ids_sha256"] == audit["redirect_ids_sha256"], "redirect identity")
    expected_branches = {
        branch: {
            "complement_red_degree": values["complement_degree"],
            "complement_red_edges": values["complement_edges"],
            "disposition_of_unknown_children": values["disposition"],
            "red_degree": values["red_degree"],
            "red_edges": values["red_edges"],
            "unknown_children": values["unknown"],
        }
        for branch, values in audit["branch_report"].items()
    }
    need(queue["by_branch"] == expected_branches, "branch detail")
    need(queue["redirected_fraction"] == {
        "decimal_percent": "58.385093167702",
        "denominator": 161,
        "numerator": 94,
    }, "redirected fraction")
    need(result["literal_h3987_state"] == {
        "certified_unsat": 99,
        "parent_formulas": {"d20-22": "UNKNOWN", "d22-20": "UNKNOWN"},
        "unknown": 161,
        "whole_h3887_tasks_decided_here": 0,
    }, "literal-status separation")
    need(result["coverage"] == {
        "complete_carrier": "h3873 maximal-K4/Ramsey(4,4) carrier",
        "complete_carrier_physical_tasks": 2189178,
        "dependency_status": "INDEPENDENTLY_ACCEPTED",
        "redirect_destination": "some normalized task in the complete h3873 carrier; no same-child transport is claimed",
    }, "coverage boundary")
    need(result["target43_found"] is False and
         result["ramsey_lower_bound_changed"] is False and
         result["solver_calls"] == 0, "scope")
    return {"status": "INDEPENDENT_CHECK_ACCEPT", **audit}


if __name__ == "__main__":
    need(len(sys.argv) == 2, "usage: independent_check.py RESULT.json")
    print(json.dumps(check(sys.argv[1]), indent=2, sort_keys=True))
