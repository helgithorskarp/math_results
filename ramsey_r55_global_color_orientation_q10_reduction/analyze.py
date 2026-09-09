#!/usr/bin/env python3
"""Compute the exact color-orientation effect on the h3987 UNKNOWN ledger."""
from collections import Counter
from pathlib import Path
import hashlib
import json

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def need(condition, message):
    if not condition:
        raise ValueError(message)


def load_inputs():
    dependencies = json.loads((HERE / "DEPENDENCIES.json").read_text())
    for relative, metadata in dependencies.items():
        path = ROOT / relative
        need(path.is_file(), "missing dependency: " + relative)
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        need(actual == metadata["sha256"], "dependency identity: " + relative)
    tasks = json.loads((ROOT / "ramsey_r55_q10_recovered_cube_refutations" /
                        "TASKS.json").read_text())
    reduction = json.loads((ROOT / "ramsey_r55_q10_recovered_cube_refutations" /
                            "REDUCTION.json").read_text())
    regular = json.loads((ROOT / "ramsey_r55_q10_regular_cnf_reduction" /
                          "REDUCTION.json").read_text())
    return tasks, reduction, regular


def id_digest(ids):
    payload = "".join(identifier + "\n" for identifier in sorted(ids)).encode()
    return hashlib.sha256(payload).hexdigest()


def analyze():
    tasks, reduction, regular = load_inputs()
    need(len(tasks) == 260, "physical task count")
    need(len({row["id"] for row in tasks}) == len(tasks), "unique task ids")

    degree = {row["branch"]: row["red_degree"] for row in regular["rows"]
              if row["branch"] in ("d20-22", "d22-20")}
    need(degree == {"d20-22": 20, "d22-20": 22}, "branch degrees")

    order = 43
    total_edges = order * (order - 1) // 2
    cutoff = (total_edges - 1) // 2
    need(total_edges == 903 and cutoff == 451, "orientation arithmetic")

    status_counts = Counter(row["status"] for row in tasks)
    branch_counts = Counter(row["branch"] for row in tasks)
    need(status_counts == {"CERTIFIED_UNSAT": 99, "UNKNOWN": 161},
         "literal statuses")
    need(branch_counts == {"d20-22": 130, "d22-20": 130},
         "branch sizes")

    unknown = [row for row in tasks if row["status"] == "UNKNOWN"]
    active = []
    redirected = []
    detail = {}
    for branch in sorted(degree):
        red_degree = degree[branch]
        degree_sum = order * red_degree
        need(degree_sum % 2 == 0, "handshaking parity: " + branch)
        red_edges = degree_sum // 2
        complement_edges = total_edges - red_edges
        rows = [row for row in unknown if row["branch"] == branch]
        if red_edges <= cutoff:
            disposition = "TARGET_ACTIVE_ORIENTATION"
            active.extend(row["id"] for row in rows)
        else:
            disposition = "COLOR_COMPLEMENT_REDIRECT"
            redirected.extend(row["id"] for row in rows)
        detail[branch] = {
            "complement_red_degree": order - 1 - red_degree,
            "complement_red_edges": complement_edges,
            "disposition_of_unknown_children": disposition,
            "red_degree": red_degree,
            "red_edges": red_edges,
            "unknown_children": len(rows),
        }

    need(len(active) == 67 and len(redirected) == 94, "94/67 gate")
    need(reduction["unknown_physical_subtasks"] == 161, "reduction total")
    need(reduction["certified_closed_physical_subtasks"] == 99,
         "certified total")
    need(reduction["all_h3887_tasks"] == 2189178, "complete carrier count")

    return {
        "color_orbit": {
            "canonical_rule": "retain the representative with red_edges <= 451",
            "cutoff": cutoff,
            "fixed_orbits_possible": False,
            "order": order,
            "total_edges": total_edges,
        },
        "coverage": {
            "complete_carrier": "h3873 maximal-K4/Ramsey(4,4) carrier",
            "complete_carrier_physical_tasks": reduction["all_h3887_tasks"],
            "dependency_status": "INDEPENDENTLY_ACCEPTED",
            "redirect_destination": "some normalized task in the complete h3873 carrier; no same-child transport is claimed",
        },
        "literal_h3987_state": {
            "certified_unsat": status_counts["CERTIFIED_UNSAT"],
            "parent_formulas": reduction["parent_formulas"],
            "unknown": status_counts["UNKNOWN"],
            "whole_h3887_tasks_decided_here": 0,
        },
        "oriented_q10_unknown_queue": {
            "active_ids_sha256": id_digest(active),
            "by_branch": detail,
            "color_complement_redirect": len(redirected),
            "redirect_ids_sha256": id_digest(redirected),
            "redirected_fraction": {
                "decimal_percent": "58.385093167702",
                "denominator": len(unknown),
                "numerator": len(redirected),
            },
            "source_unknown": len(unknown),
            "target_active_orientation": len(active),
        },
        "ramsey_lower_bound_changed": False,
        "solver_calls": 0,
        "status": "CERTIFIED_GLOBAL_COLOR_ORIENTATION_EFFECT_ON_H3987_UNKNOWN_LEDGER",
        "status_separation": "94 redirects are neither SAT nor UNSAT decisions; the literal h3987 ledger remains 99 CERTIFIED_UNSAT / 161 UNKNOWN",
        "target43_found": False,
    }


if __name__ == "__main__":
    print(json.dumps(analyze(), indent=2, sort_keys=True))
