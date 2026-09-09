#!/usr/bin/env python3
"""Exact fixed-prefix effect of the h4021 cut on all h3987 UNKNOWN tasks."""
from collections import Counter
from importlib.util import module_from_spec, spec_from_file_location
from itertools import combinations
from pathlib import Path
import hashlib
import json
import math
import sys

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
Q10 = REPO / "ramsey_r55_q10_recovered_cube_refutations"
CUT = REPO / "ramsey_r55_structural_cut_interface"

PINS = {
    Q10 / "TASKS.json": "349b2307a16696323b927a546ea6b365668fb09a01532f91480a0093950fb548",
    Q10 / "verify.py": "2601004d3959c20ad547920ec6705471e3b871926a78753c3a66c33d3f0e9f12",
    CUT / "TEMPLATE.json": "672c8fed249efca052b21ed7b4cb6a01364977d5074edf1f252e3b8d055d0d99",
    CUT / "interface.py": "bc5161252c0cae025f6b217d21440e39a989dc9d0189d0e2f5c0ff9ef4011dca",
}


def need(test, message):
    if not test:
        raise ValueError(message)


def load_module(name, path):
    spec = spec_from_file_location(name, path)
    need(spec is not None and spec.loader is not None, "module specification")
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def check_pins():
    for path, expected in PINS.items():
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        need(actual == expected, "dependency identity: " + str(path))


def physical_edges():
    edges = [edge for edge in combinations(range(43), 2)
             if edge[0] < 40 and edge[0] // 4 != edge[1] // 4]
    need(len(edges) == 840, "physical q10 variables")
    return {index + 2: edge for index, edge in enumerate(edges)}


def fixed_prefix(task, inverse):
    fixed = {}
    for block in range(10):
        for edge in combinations(range(4 * block, 4 * block + 4), 2):
            fixed[edge] = 1
    for edge in combinations((40, 41, 42), 2):
        fixed[edge] = 0
    literals = list(task["cube"])
    if task["forced_residual_literal"] is not None:
        literals.append(task["forced_residual_literal"])
    for literal in literals:
        edge = inverse[abs(literal)]
        color = int(literal > 0)
        need(edge not in fixed or fixed[edge] == color, "consistent prefix")
        fixed[edge] = color
    return fixed


def analyze():
    check_pins()
    q10 = load_module("h3987_verify", Q10 / "verify.py")
    cut = load_module("h4021_interface", CUT / "interface.py")
    tasks = json.loads((Q10 / "TASKS.json").read_text())
    need(tasks == q10.tasks(), "h3987 task generator and ledger agree")
    unknown = [task for task in tasks if task["status"] == "UNKNOWN"]
    need(len(tasks) == 260 and len(unknown) == 161, "h3987 ledger counts")

    template = json.loads((CUT / "TEMPLATE.json").read_text())
    fixed_template = template["fixed"]
    need(len(fixed_template) == 147, "h4021 cut width")
    need(len({tuple(sorted((u, v))) for u, v, color in fixed_template}) == 147,
         "distinct h4021 fixed pairs")
    root = template["root"]
    root_rows = [(u, v, color) for u, v, color in fixed_template
                 if root in (u, v)]
    need(len(root_rows) == 18 and all(color == 1 for u, v, color in root_rows),
         "h4021 monochromatic root star")
    for color in (0, 1):
        emitted = cut.instantiate(list(range(19)), color)
        need(len(emitted["physical_clause"]) == 147, "emitted cut width")
        root_truths = [truth for u, v, truth in emitted["physical_clause"]
                       if 0 in (u, v)]
        need(len(root_truths) == 18 and set(root_truths) == {1 - color},
             "emitted root-star polarity")

    inverse = physical_edges()
    histogram = Counter()
    branch_counts = Counter()
    fixed_counts = Counter()
    per_task = []
    eligible_pairs = 0
    for task in unknown:
        fixed = fixed_prefix(task, inverse)
        degrees = [[0, 0] for unused in range(43)]
        for (u, v), color in fixed.items():
            degrees[u][color] += 1
            degrees[v][color] += 1
        maximum_red = max(row[1] for row in degrees)
        maximum_blue = max(row[0] for row in degrees)
        eligible = sum(row[color] >= 18 for row in degrees for color in (0, 1))
        eligible_pairs += eligible
        key = (maximum_red, maximum_blue, len(fixed))
        histogram[key] += 1
        branch_counts[task["branch"]] += 1
        fixed_counts[len(fixed)] += 1
        per_task.append({
            "id": task["id"],
            "branch": task["branch"],
            "fixed_edges": len(fixed),
            "max_fixed_red_degree": maximum_red,
            "max_fixed_blue_degree": maximum_blue,
            "eligible_root_color_pairs": eligible,
            "forced_residual_literal": task["forced_residual_literal"],
        })

    maximum_red = max(row[0] for row in histogram)
    maximum_blue = max(row[1] for row in histogram)
    need(maximum_red == 6 and maximum_blue == 6, "exact degree maxima")
    need(eligible_pairs == 0, "zero eligible roots")
    need(branch_counts == {"d20-22": 67, "d22-20": 94}, "branch cover")
    need(fixed_counts == {76: 132, 77: 29}, "fixed-edge counts")
    ordered_embeddings = 2 * math.prod(range(43 - 19 + 1, 44))
    return {
        "status": "CERTIFIED_ZERO_DIRECT_H4021_Q10_PREFIX_CLOSURES",
        "scope": "all h3987 tasks whose ledger status is UNKNOWN",
        "interface": {
            "fixed_template_edges": len(fixed_template),
            "root_star_edges": len(root_rows),
            "necessary_fixed_same_color_root_degree_for_conflict": 18,
        },
        "carrier": {
            "all_tasks": len(tasks),
            "previously_certified_unsat": len(tasks) - len(unknown),
            "unknown_tasks_checked": len(unknown),
            "unknown_by_branch": dict(sorted(branch_counts.items())),
            "fixed_edge_count_histogram": {str(k): fixed_counts[k]
                                           for k in sorted(fixed_counts)},
            "root_color_pairs_checked": len(unknown) * 43 * 2,
            "eligible_root_color_pairs": eligible_pairs,
            "ordered_interface_embeddings_covered": ordered_embeddings,
            "direct_conflict_embeddings": 0,
            "new_task_closures": 0,
            "remaining_unknown_tasks": len(unknown),
            "maximum_fixed_red_degree": maximum_red,
            "maximum_fixed_blue_degree": maximum_blue,
        },
        "degree_histogram": [
            {"max_fixed_red_degree": red, "max_fixed_blue_degree": blue,
             "fixed_edges": count, "tasks": histogram[red, blue, count]}
            for red, blue, count in sorted(histogram)
        ],
        "carrier_task_digest_sha256": hashlib.sha256(
            json.dumps(per_task, separators=(",", ":"), sort_keys=True).encode()
        ).hexdigest(),
        "limitations": [
            "No h3987 UNKNOWN task is decided.",
            "The result concerns h4021 CONFLICT under the fixed q10 prefix only.",
            "Nonempty h4021 clauses may still prune later SAT search.",
            "No claim is made about templates completed by currently free edges.",
            "No good43 graph is produced.",
        ],
    }


if __name__ == "__main__":
    json.dump(analyze(), sys.stdout, indent=2, sort_keys=True)
    sys.stdout.write("\n")
