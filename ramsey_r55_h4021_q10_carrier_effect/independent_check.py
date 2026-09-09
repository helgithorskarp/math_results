#!/usr/bin/env python3
"""Independent reconstruction and audit of the zero direct-closure result."""
from collections import Counter
from itertools import combinations, permutations
from pathlib import Path
import hashlib
import json
import math
import sys

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
Q10 = REPO / "ramsey_r55_q10_recovered_cube_refutations"
CUT = REPO / "ramsey_r55_structural_cut_interface"


def need(test, message):
    if not test:
        raise ValueError(message)


def canonical_words():
    """Brute-force the full S4 x S3 orbit, unlike h3987's sorted-row code."""
    answer = []
    row_actions = list(permutations(range(4)))
    column_actions = list(permutations(range(3)))
    for word in range(1 << 12):
        matrix = [[(word >> (3 * row + column)) & 1 for column in range(3)]
                  for row in range(4)]
        if any(all(matrix[row][column] for row in range(4))
               for column in range(3)):
            continue
        orbit_minimum = 1 << 12
        for rows in row_actions:
            for columns in column_actions:
                image = 0
                for new_row, old_row in enumerate(rows):
                    for new_column, old_column in enumerate(columns):
                        image |= matrix[old_row][old_column] << (3 * new_row + new_column)
                orbit_minimum = min(orbit_minimum, image)
        if word == orbit_minimum:
            answer.append(word)
    need(len(answer) == 65, "independent 65-word orbit transversal")
    return answer


def physical_maps():
    edges = [edge for edge in combinations(range(43), 2)
             if edge[0] < 40 and edge[0] // 4 != edge[1] // 4]
    need(len(edges) == 840, "840 physical variables")
    forward = {edge: index + 2 for index, edge in enumerate(edges)}
    inverse = {value: key for key, value in forward.items()}
    return forward, inverse


def reconstruct_tasks():
    forward, unused = physical_maps()
    core = [forward[row, column] for row in range(4)
            for column in (40, 41, 42)]
    clauses = {"d20-22": (139, 156), "d22-20": (121, 155)}
    output = []
    for branch, (pivot, core_literal) in clauses.items():
        for index, word in enumerate(canonical_words()):
            contacts = [variable if word >> bit & 1 else -variable
                        for bit, variable in enumerate(core)]
            for pivot_bit in (0, 1):
                cube = contacts + [pivot if pivot_bit else -pivot]
                closed = not pivot_bit and -core_literal in cube
                output.append({
                    "id": f"{branch}-w{index:02d}-p{pivot_bit}",
                    "branch": branch,
                    "word": word,
                    "cube": cube,
                    "status": "CERTIFIED_UNSAT" if closed else "UNKNOWN",
                    "certificate": (("d20-22-strong" if branch == "d20-22"
                                     else "d22-20-corezero") if closed else None),
                    "forced_residual_literal": (148 if branch == "d22-20"
                                                  and not pivot_bit and not closed
                                                  else None),
                })
    return output


def fixed_prefix(task, inverse):
    fixed = {}
    for block_start in range(0, 40, 4):
        for edge in combinations(range(block_start, block_start + 4), 2):
            fixed[edge] = 1
    for edge in combinations(range(40, 43), 2):
        fixed[edge] = 0
    literals = task["cube"] + ([] if task["forced_residual_literal"] is None
                               else [task["forced_residual_literal"]])
    for literal in literals:
        edge = inverse[abs(literal)]
        value = int(literal > 0)
        need(edge not in fixed or fixed[edge] == value, "consistent assignment")
        fixed[edge] = value
    return fixed


def expected_result(tasks, template):
    root = template["root"]
    fixed_template = template["fixed"]
    pairs = [tuple(sorted((u, v))) for u, v, color in fixed_template]
    need(len(fixed_template) == 147 and len(set(pairs)) == 147,
         "147 distinct template pairs")
    root_rows = [row for row in fixed_template if root in row[:2]]
    need(len(root_rows) == 18 and all(row[2] == 1 for row in root_rows),
         "18-edge chosen-color star")
    unused, inverse = physical_maps()
    unknown = [task for task in tasks if task["status"] == "UNKNOWN"]
    rows = []
    histogram = Counter()
    branches = Counter()
    fixed_counts = Counter()
    eligible_total = 0
    for task in unknown:
        fixed = fixed_prefix(task, inverse)
        degree = [[0, 0] for unused_vertex in range(43)]
        for (u, v), color in fixed.items():
            degree[u][color] += 1
            degree[v][color] += 1
        red = max(row[1] for row in degree)
        blue = max(row[0] for row in degree)
        eligible = sum(row[color] >= 18 for row in degree for color in (0, 1))
        eligible_total += eligible
        histogram[red, blue, len(fixed)] += 1
        branches[task["branch"]] += 1
        fixed_counts[len(fixed)] += 1
        rows.append({
            "id": task["id"], "branch": task["branch"],
            "fixed_edges": len(fixed), "max_fixed_red_degree": red,
            "max_fixed_blue_degree": blue,
            "eligible_root_color_pairs": eligible,
            "forced_residual_literal": task["forced_residual_literal"],
        })
    need(len(tasks) == 260 and len(unknown) == 161, "complete UNKNOWN carrier")
    need(eligible_total == 0, "star obstruction")
    return {
        "status": "CERTIFIED_ZERO_DIRECT_H4021_Q10_PREFIX_CLOSURES",
        "scope": "all h3987 tasks whose ledger status is UNKNOWN",
        "interface": {"fixed_template_edges": 147, "root_star_edges": 18,
                      "necessary_fixed_same_color_root_degree_for_conflict": 18},
        "carrier": {
            "all_tasks": len(tasks), "previously_certified_unsat": 99,
            "unknown_tasks_checked": len(unknown),
            "unknown_by_branch": dict(sorted(branches.items())),
            "fixed_edge_count_histogram": {str(k): fixed_counts[k]
                                           for k in sorted(fixed_counts)},
            "root_color_pairs_checked": len(unknown) * 86,
            "eligible_root_color_pairs": eligible_total,
            "ordered_interface_embeddings_covered": 2 * math.prod(range(25, 44)),
            "direct_conflict_embeddings": 0, "new_task_closures": 0,
            "remaining_unknown_tasks": len(unknown),
            "maximum_fixed_red_degree": max(row[0] for row in histogram),
            "maximum_fixed_blue_degree": max(row[1] for row in histogram),
        },
        "degree_histogram": [
            {"max_fixed_red_degree": red, "max_fixed_blue_degree": blue,
             "fixed_edges": count, "tasks": histogram[red, blue, count]}
            for red, blue, count in sorted(histogram)
        ],
        "carrier_task_digest_sha256": hashlib.sha256(
            json.dumps(rows, separators=(",", ":"), sort_keys=True).encode()
        ).hexdigest(),
        "limitations": [
            "No h3987 UNKNOWN task is decided.",
            "The result concerns h4021 CONFLICT under the fixed q10 prefix only.",
            "Nonempty h4021 clauses may still prune later SAT search.",
            "No claim is made about templates completed by currently free edges.",
            "No good43 graph is produced.",
        ],
    }


def check(path):
    tasks_path = Q10 / "TASKS.json"
    template_path = CUT / "TEMPLATE.json"
    need(hashlib.sha256(tasks_path.read_bytes()).hexdigest() ==
         "349b2307a16696323b927a546ea6b365668fb09a01532f91480a0093950fb548",
         "task ledger pin")
    need(hashlib.sha256(template_path.read_bytes()).hexdigest() ==
         "672c8fed249efca052b21ed7b4cb6a01364977d5074edf1f252e3b8d055d0d99",
         "template pin")
    tasks = json.loads(tasks_path.read_text())
    need(tasks == reconstruct_tasks(), "independent task reconstruction")
    expected = expected_result(tasks, json.loads(template_path.read_text()))
    actual = json.loads(Path(path).read_text())
    need(actual == expected, "result differs from independent reconstruction")
    answer = {"status": "INDEPENDENT_ZERO_EFFECT_CHECK_PASS",
              "tasks": 161, "root_color_pairs": 13846,
              "ordered_embeddings": expected["carrier"]["ordered_interface_embeddings_covered"],
              "maximum_fixed_monochromatic_degree": 6,
              "direct_conflict_embeddings": 0, "task_closures": 0}
    print(json.dumps(answer, sort_keys=True))


if __name__ == "__main__":
    need(len(sys.argv) == 2, "usage: independent_check.py RESULT.json")
    check(sys.argv[1])
