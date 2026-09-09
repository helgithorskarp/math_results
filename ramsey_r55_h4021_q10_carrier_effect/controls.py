#!/usr/bin/env python3
"""Exercise the actual h4021 receiver and its three status outcomes."""
from importlib.util import module_from_spec, spec_from_file_location
from itertools import combinations
from pathlib import Path
import json
import sys

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
CUT = REPO / "ramsey_r55_structural_cut_interface"
Q10 = REPO / "ramsey_r55_q10_recovered_cube_refutations"


def need(test, message):
    if not test:
        raise ValueError(message)


def module(path):
    spec = spec_from_file_location("h4021_control_interface", path)
    need(spec is not None and spec.loader is not None, "interface module")
    result = module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


def complete_map(values):
    edges, variable = [], 10000
    for pair in combinations(range(43), 2):
        if pair in values:
            edges.append([*pair, "fixed", values[pair]])
        else:
            edges.append([*pair, "var", variable])
            variable += 1
    return {"edges": edges}


def q10_fixed(task):
    physical = [edge for edge in combinations(range(43), 2)
                if edge[0] < 40 and edge[0] // 4 != edge[1] // 4]
    inverse = {index + 2: edge for index, edge in enumerate(physical)}
    values = {}
    for start in range(0, 40, 4):
        for edge in combinations(range(start, start + 4), 2):
            values[edge] = 1
    for edge in combinations((40, 41, 42), 2):
        values[edge] = 0
    literals = task["cube"] + ([] if task["forced_residual_literal"] is None
                               else [task["forced_residual_literal"]])
    for literal in literals:
        values[inverse[abs(literal)]] = int(literal > 0)
    return values


def run():
    interface = module(CUT / "interface.py")
    statuses = {"CONFLICT": 0, "CLAUSE": 0, "TAUTOLOGY": 0}
    positive = {"CONFLICT": 0, "CLAUSE": 0, "TAUTOLOGY": 0}
    for color in (0, 1):
        cut = interface.instantiate(list(range(19)), color)
        desired = {(u, v): 1 - truth for u, v, truth in cut["physical_clause"]}
        mapping = complete_map(desired)
        answer = interface.receive(cut, mapping)
        need(answer["status"] == "CONFLICT", "positive conflict control")
        positive[answer["status"]] += 1

        root_pair = next((u, v) for u, v, truth in cut["physical_clause"]
                         if 0 in (u, v))
        partial = dict(desired)
        del partial[root_pair]
        answer = interface.receive(cut, complete_map(partial))
        need(answer["status"] == "CLAUSE" and len(answer["clause"]) == 1,
             "one-free-edge clause control")
        positive[answer["status"]] += 1

        blocked = dict(desired)
        blocked[root_pair] = 1 - blocked[root_pair]
        answer = interface.receive(cut, complete_map(blocked))
        need(answer["status"] == "TAUTOLOGY", "opposite-edge control")
        positive[answer["status"]] += 1

    tasks = [task for task in json.loads((Q10 / "TASKS.json").read_text())
             if task["status"] == "UNKNOWN"]
    need(len(tasks) == 161, "all UNKNOWN tasks")
    for task in tasks:
        mapping = complete_map(q10_fixed(task))
        for color in (0, 1):
            # This is one literal receiver call per color and task.  The
            # universal all-embedding conclusion is checked by the star lemma.
            answer = interface.receive(interface.instantiate(list(range(19)), color),
                                       mapping)
            need(answer["status"] != "CONFLICT", "q10 control conflict")
            statuses[answer["status"]] += 1
    result = {"status": "H4021_RECEIVER_CONTROLS_PASS",
              "positive_status_controls": positive,
              "q10_interface_calls": len(tasks) * 2,
              "q10_identity_embedding_statuses": statuses}
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    run()
