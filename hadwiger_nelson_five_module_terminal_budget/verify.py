#!/usr/bin/env python3
"""Verify the five-module/eight-terminal obstruction and finite evidence."""

from copy import deepcopy
from itertools import combinations, product
from pathlib import Path
import argparse
import hashlib
import json
import math

import audit
import kernel


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def require(condition, message):
    if not condition:
        raise ValueError(message)


def normalized_edge(edge, n):
    require(
        type(edge) is list
        and len(edge) == 2
        and all(type(v) is int and 0 <= v < n for v in edge),
        "malformed edge",
    )
    a, b = sorted(edge)
    require(a != b, "loop edge")
    return a, b


def adjacency_from_edges(n, edges):
    adjacency = [0] * n
    for a, b in edges:
        adjacency[a] |= 1 << b
        adjacency[b] |= 1 << a
    return tuple(adjacency)


def check_instance(instance):
    require(type(instance) is dict and set(instance) == {"name", "terminal_sets", "unit_edges"}, "instance keys")
    terminal_sets = instance["terminal_sets"]
    require(type(terminal_sets) is list and len(terminal_sets) == 5, "exactly five terminal sets")
    require(
        all(type(block) is list and len(block) >= 2 and len(block) == len(set(block)) for block in terminal_sets),
        "terminal set",
    )
    vertices = sorted({v for block in terminal_sets for v in block})
    require(vertices == list(range(len(vertices))) and len(vertices) <= 8, "canonical union of at most eight terminals")
    n = len(vertices)
    require(all(type(v) is int for block in terminal_sets for v in block), "terminal label")
    blocks = [set(block) for block in terminal_sets]
    unit_list = [normalized_edge(edge, n) for edge in instance["unit_edges"]]
    unit = set(unit_list)
    require(len(unit) == len(unit_list), "duplicate unit edge")
    require(all(not ({a, b} <= block) for a, b in unit for block in blocks), "unit edge inside a separated terminal set")
    unit_neighbours = [set() for _ in range(n)]
    for a, b in unit:
        unit_neighbours[a].add(b)
        unit_neighbours[b].add(a)
    for v in range(n):
        for block in blocks:
            require(
                len(unit_neighbours[v] & block) <= int(v not in block),
                "two unit neighbours in one foreign terminal set",
            )

    choice_lists = [list(combinations(sorted(block), 2)) for block in blocks]
    receipt = hashlib.sha256()
    maximum_degree = 0
    minimum_colours = 4
    for chosen_tuple in product(*choice_lists):
        chosen = {tuple(sorted(edge)) for edge in chosen_tuple}
        require(not (unit & chosen), "selected long pair is a unit edge")
        auxiliary = adjacency_from_edges(n, unit | chosen)
        degree = max((row.bit_count() for row in auxiliary), default=0)
        maximum_degree = max(maximum_degree, degree)
        require(degree <= 5, "auxiliary maximum degree")
        require(not kernel.contains_k5(auxiliary), "five long edges created K5")
        word = kernel.four_colouring(auxiliary)
        require(word is not None, "uncolourable auxiliary graph")
        require(all(word[a] != word[b] for a, b in unit), "unit edge colouring")
        require(all(len({word[v] for v in block}) > 1 for block in blocks), "monochromatic terminal set")
        minimum_colours = min(minimum_colours, 1 + max(word, default=-1))
        receipt.update(
            (",".join(f"{a}-{b}" for a, b in sorted(chosen)) + ":" + "".join(map(str, word)) + "\n").encode()
        )
    return {
        "name": instance["name"],
        "terminals": n,
        "unit_edges": len(unit),
        "pair_choices_checked": math.prod(map(len, choice_lists)),
        "maximum_auxiliary_degree": maximum_degree,
        "minimum_colours_in_returned_words": minimum_colours,
        "receipt_sha256": receipt.hexdigest(),
    }


def upstream_check():
    dependencies = json.loads((HERE / "DEPENDENCIES.json").read_text())
    for relative, expected in dependencies["source_files_sha256"].items():
        require(hashlib.sha256((ROOT / relative).read_bytes()).hexdigest() == expected, "upstream hash: " + relative)
    expected = json.loads((ROOT / "hadwiger_nelson_four_module_synthesis/EXPECTED.json").read_text())
    require(expected["status"] == "AT_MOST_FOUR_SEPARATED_TERMINAL_MODULES_ARE_FOUR_COLOURABLE", "upstream status")
    require(expected["full_A159_B214_nonfour_order_lower_bound"] == 783, "upstream full-module bound")
    require(expected["at_most508_nonfour_assembly_requires_some_private_size_at_most"] == 101, "upstream replacement-module bound")
    related = dependencies["related_A159_compression"]
    for relative, expected_hash in related["files_sha256"].items():
        require(hashlib.sha256((ROOT / relative).read_bytes()).hexdigest() == expected_hash, "related hash: " + relative)
    compression = json.loads((ROOT / "hadwiger_nelson_a159_module_compression/EXPECTED.json").read_text())
    require(compression["status"] == "EVERY_PROPER_TERMINAL_PRESERVING_A159_REDUCTION_EXTENDS_ALL_64_BOUNDARIES", "A159 compression status")
    return {
        "source_contribution_ref": dependencies["source_contribution_ref"],
        "source_commit": dependencies["source_commit"],
        "source_hashes_checked": len(dependencies["source_files_sha256"]),
        "prior_full_module_bound": 783,
        "prior_private_vertex_threshold": 101,
        "related_A159_compression_ref": related["contribution_ref"],
        "related_A159_compression_commit": related["commit"],
        "related_hashes_checked": len(related["files_sha256"]),
        "A159_reductions_already_closed_independently": True,
    }


def rejected_controls(fixtures):
    controls = []

    def reject(name, instance):
        try:
            check_instance(instance)
        except ValueError:
            controls.append(name)
        else:
            raise RuntimeError("accepted corruption: " + name)

    x = deepcopy(fixtures[0]); x["terminal_sets"].append([0, 1]); reject("six_terminal_sets", x)
    x = deepcopy(fixtures[1]); x["terminal_sets"][-1].append(8); reject("nine_terminal_vertices", x)
    x = deepcopy(fixtures[1]); x["unit_edges"].append([0, 0]); reject("loop_unit_edge", x)
    x = deepcopy(fixtures[1]); x["unit_edges"].append([0, 1]); reject("unit_edge_inside_terminal_set", x)
    x = deepcopy(fixtures[2]); x["unit_edges"].append([0, 5]); reject("two_neighbours_in_foreign_set", x)
    x = deepcopy(fixtures[1]); x["unit_edges"].append([0, 9]); reject("out_of_range_endpoint", x)
    x = deepcopy(fixtures[1]); x["unit_edges"].append(x["unit_edges"][0]); reject("duplicate_unit_edge", x)
    x = deepcopy(fixtures[0]); x["terminal_sets"][0] = [0]; reject("singleton_terminal_set", x)
    return controls


def run(include_controls=False):
    primary = kernel.run()
    independent = audit.run()
    require(
        [row["labelled_min4_max5_graphs"] for row in primary["kernels"]]
        == list(independent["degree_polynomial_counts"].values()),
        "independent graph counts disagree",
    )
    fixtures = json.loads((HERE / "fixtures.json").read_text())
    fixture_reports = [check_instance(instance) for instance in fixtures]
    full_bounds = []
    for b_copies in range(6):
        private = (5 - b_copies) * 156 + b_copies * 212
        full_bounds.append(
            {
                "A159_copies": 5 - b_copies,
                "B214_copies": b_copies,
                "private_vertices": private,
                "nonfour_terminal_union_lower_bound": 9,
                "total_order_lower_bound": private + 9,
            }
        )
    require([row["total_order_lower_bound"] for row in full_bounds] == [789, 845, 901, 957, 1013, 1069], "full-module bounds")
    require(5 * 100 + 9 == 509 and 499 // 5 == 99, "target-budget arithmetic")
    result = {
        "status": "FIVE_SEPARATED_TERMINAL_MODULES_WITH_AT_MOST_EIGHT_TERMINALS_ARE_FOUR_COLOURABLE",
        "record_improvement": False,
        "solver_calls": 0,
        "theorem": {
            "modules": 5,
            "terminal_union_upper_bound": 8,
            "pair_selection_quantifier": "every choice of one pair per terminal set works",
            "nonfour_terminal_union_lower_bound": 9,
            "at_most508_nonfour_requires_some_private_order_at_most": 99,
        },
        "upstream": upstream_check(),
        "finite_kernel_enumeration": primary,
        "independent_audit": independent,
        "interface_fixtures": fixture_reports,
        "full_A159_B214_five_module_order_lower_bounds": full_bounds,
        "trust_boundary": "written reduction using Tutte's one-factor theorem plus exact standard-library Python enumeration; no SAT, floating point, coordinates, or omitted certificate",
    }
    canonical = json.dumps(result, sort_keys=True, separators=(",", ":")).encode()
    result["receipt_sha256"] = hashlib.sha256(canonical).hexdigest()
    result["rejected_controls"] = rejected_controls(fixtures)
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--check-expected", action="store_true")
    parser.add_argument("--controls", action="store_true")
    args = parser.parse_args()
    output = run(args.controls)
    if args.check_expected:
        require(output == json.loads((HERE / "EXPECTED.json").read_text()), "expected result")
    print(json.dumps(output, indent=2, sort_keys=True))
