#!/usr/bin/env python3
"""Corruption controls plus complementary-color and margin boundary checks."""
import argparse
from copy import deepcopy
from itertools import combinations
import json
from pathlib import Path
import kernel
import verify


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    args = parser.parse_args()
    read = lambda name: json.loads((args.source / (name + ".json")).read_text())
    fixtures, formula = read("fixtures"), read("small_kernel")
    doc = fixtures["positive"]["graph"]
    rejected = []

    def rejects(name, run):
        try:
            run()
        except ValueError:
            rejected.append(name)
        else:
            raise ValueError("accepted corruption: " + name)

    for name in ("deleted_clause", "flipped_color", "deleted_literal", "duplicated_literal",
                 "wrong_five_set", "missing_variable", "reordered_variables"):
        wrong = deepcopy(formula)
        if name == "deleted_clause":
            wrong["clauses"] = []
        elif name == "flipped_color":
            wrong["clauses"][0]["color"] = "red"
        elif name == "deleted_literal":
            wrong["clauses"][0]["variables"].pop()
        elif name == "duplicated_literal":
            wrong["clauses"][0]["variables"].append(3)
        elif name == "wrong_five_set":
            wrong["clauses"][0]["vertices"][0] = 0
        elif name == "missing_variable":
            wrong["variables"].pop()
        else:
            wrong["variables"].reverse()
        rejects(name, lambda wrong=wrong: verify.verify_kernel(doc, wrong))
    for name, full in (("empty_signature", False), ("full_signature", True)):
        wrong = deepcopy(doc)
        edges = {tuple(e) for e in wrong["red_edges"]}
        for e in range(3):
            edges.discard((e, 3))
            if full:
                edges.add((e, 3))
        wrong["red_edges"] = [list(e) for e in sorted(edges)]
        rejects(name, lambda wrong=wrong: verify.read_graph(wrong))
    for name in ("red_singleton_necessity", "blue_pair_necessity"):
        rejects("cannot_freeze_" + name,
                lambda name=name: verify.check(verify.preflight(fixtures[name])["passes"], "preflight gap"))
    rows = read("margin_certificates")
    infeasible = next(r for r in rows if "flow" in r["certificate"] and not r["certificate"]["feasible"])
    for name in ("false_feasible", "wrong_cut", "wrong_flow"):
        wrong = deepcopy(infeasible["certificate"])
        if name == "false_feasible":
            wrong["feasible"] = True
        elif name == "wrong_cut":
            wrong["cut_capacity"] += 1
        else:
            wrong["edges"] = []
        rejects(name, lambda wrong=wrong: verify.verify_margin(infeasible["left"], infeasible["right"], wrong))
    # Color complementation preserves free variables and flips every clause's color.
    for name, example in (("positive", doc), ("red", fixtures["red_singleton_necessity"]),
                          ("blue", fixtures["blue_pair_necessity"])):
        n, red, _ = verify.read_graph(example)
        complement = {"n": n, "red_edges": [list(e) for e in combinations(range(n), 2) if e not in red]}
        expected = deepcopy(verify.reconstruct(example))
        for r in expected["clauses"]:
            r["color"] = "blue" if r["color"] == "red" else "red"
        expected["clauses"].sort(key=lambda r: (r["vertices"], r["color"] == "blue"))
        verify.verify_kernel(complement, expected)
        verify.check(kernel.compile_kernel(kernel.decode(complement)) == expected, "producer complement")
    boundaries = [([], []), ([], [0, 0]), ([0, 0], []), ([-1, 0], [0, 0]),
                  ([3, 0], [1, 1]), ([3, 3, 0], [3, 3, 0])]
    for left, right in boundaries:
        verify.verify_margin(left, right, kernel.bipartite(left, right))
    for bad in (-1, 4096, True):
        rejects("assignment_" + str(bad), lambda bad=bad: kernel.satisfies(formula, bad))
    result = {"status": "PASSED", "rejected": rejected, "corruptions_rejected": len(rejected),
              "complement_fixtures": 3, "margin_boundaries": len(boundaries)}
    args.report.write_text(json.dumps(result, sort_keys=True, indent=2) + "\n")
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
