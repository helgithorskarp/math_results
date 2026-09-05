#!/usr/bin/env python3
"""Definition-level audit of the R55 intrinsic-anchor propagation sweep.

No module from the reviewed package is imported.  The checker reads the 34
externally regenerated bases/formulas and eight fresh reviewer proof replays.
"""
from itertools import combinations, product
from pathlib import Path
import argparse
import hashlib
import json
import re


EXCLUDED = (88, 102, 107, 138, 169, 172, 176, 196)
PARENT_HASH = "c8f355b256de55727b18efcbd47ef9e777ac2b3b4ae69e09676fcddd51afa05f"


def need(condition, message):
    if not condition:
        raise ValueError(message)


def digest(path):
    h = hashlib.sha256()
    with path.open("rb") as stream:
        while block := stream.read(1 << 20):
            h.update(block)
    return {"bytes": path.stat().st_size, "sha256": h.hexdigest()}


def pair_var(i, j, delta):
    if i > j:
        i, j, delta = j, i, -delta
    pairs = list(combinations(range(11), 2))
    return 1 + 3 * pairs.index((i, j)) + delta % 3


def link_var(cycle, fixed):
    return 211 + 11 * (fixed - 33) + cycle


def core_red_edges(bits):
    pairs = list(combinations(range(4), 2))
    red = set()
    for a, b in combinations(range(12), 2):
        i, s = divmod(a, 3)
        j, t = divmod(b, 3)
        if i == j or bits[3 * pairs.index((i, j)) + (t - s) % 3] == "1":
            red.add((a, b))
    return red


def applicable_complements(bits):
    red = core_red_edges(bits)
    for five in combinations(range(12), 5):
        colours = {edge in red for edge in combinations(five, 2)}
        need(colours == {False, True}, "locally monochromatic five-set")
    applicable = []
    for omitted in range(4):
        vertices = [v for v in range(12) if v // 3 != omitted]
        has_blue_triangle = any(
            all(edge not in red for edge in combinations(triple, 2))
            for triple in combinations(vertices, 3)
        )
        if not has_blue_triangle:
            applicable.append(omitted)
    return applicable


def core_units(bits):
    units = []
    for q, (i, j) in enumerate(combinations(range(4), 2)):
        for delta in range(3):
            variable = pair_var(i, j, delta)
            units.append(variable if bits[3 * q + delta] == "1" else -variable)
    return units


def propagation_clauses(indices):
    fresh = 34280
    clauses = []
    for omitted in indices:
        indicators = []
        for fixed in range(33, 43):
            fresh += 1
            indicator = fresh
            indicators.append(indicator)
            inputs = [link_var(cycle, fixed) for cycle in range(4) if cycle != omitted]
            clauses.extend([(-indicator, -variable) for variable in inputs])
            clauses.append(tuple([indicator] + inputs))
        for omitted_fixed in range(10):
            clauses.append(tuple(indicators[:omitted_fixed] + indicators[omitted_fixed + 1:]))
    return fresh, clauses


def check_truth_tables():
    for indicator, *links in product((False, True), repeat=4):
        clauses_hold = all((not indicator) or (not link) for link in links)
        clauses_hold &= indicator or any(links)
        need(clauses_hold == (indicator == (not any(links))), "indicator clauses")
    nine_subsets = list(combinations(range(10), 9))
    for values in product((False, True), repeat=10):
        clauses_hold = all(any(values[j] for j in subset) for subset in nine_subsets)
        need(clauses_hold == (sum(values) >= 2), "cardinality clauses")
    return {"indicator_assignments": 16, "cardinality_assignments": 1024}


def check_base(parent, base, bits):
    with parent.open() as source, base.open() as target:
        need(source.readline() == "p cnf 34280 615920\n", "parent header")
        need(target.readline() == "p cnf 34280 615938\n", "base header")
        for line in source:
            need(target.readline() == line, "parent prefix mismatch")
        for unit in core_units(bits):
            need(target.readline() == f"{unit} 0\n", "core unit mismatch")
        need(target.read() == "", "base suffix")


def check_formula(base, formula, indices):
    variables, clauses = propagation_clauses(indices)
    clause_count = 615938 + len(clauses)
    with base.open() as source, formula.open() as target:
        need(source.readline() == "p cnf 34280 615938\n", "base header")
        need(target.readline() == f"p cnf {variables} {clause_count}\n", "formula header")
        for line in source:
            need(target.readline() == line, "base prefix mismatch")
        for clause in clauses:
            need(target.readline() == " ".join(map(str, clause)) + " 0\n", "propagation clause mismatch")
        need(target.read() == "", "formula suffix")
    return {"applications": len(indices), "variables": variables, "clauses": clause_count,
            "new_variables": variables - 34280, "new_clauses": len(clauses)}


def replay_data(work, index, expected):
    proof = work / f"c{index}.review1.drat"
    log = work / f"c{index}.review1.replay.log"
    proof_info = digest(proof)
    need(proof_info == expected["proof"], f"proof identity c{index}")
    text = log.read_text(errors="replace")
    need("s VERIFIED" in text, f"DRAT verification c{index}")
    hit = re.search(r"(\d+) RAT lemmas in core", text)
    need(hit is not None, f"RAT count c{index}")
    rat = int(hit.group(1))
    need(rat == expected["replay"]["rat_core_lemmas"], f"RAT identity c{index}")
    return {"index": index, "proof": proof_info, "drat_trim_verified": True,
            "rat_core_lemmas": rat}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--work", type=Path, required=True)
    parser.add_argument("--kissat", type=Path, required=True)
    parser.add_argument("--drat-trim", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    args = parser.parse_args()
    source = args.source.resolve()
    work = args.work.resolve()
    parent = work / "parent.cnf"
    need(digest(parent)["sha256"] == PARENT_HASH, "parent identity")
    cases = json.loads((source / "cases.json").read_text())
    published_rows = json.loads((source / "result.json").read_text())["cases"]
    published = {row["index"]: row for row in published_rows}
    need(len(cases) == len(published) == 34, "case count")
    need([row["index"] for row in cases] == [row["index"] for row in published_rows], "case order")

    histogram = {}
    applications = 0
    formula_sizes = {}
    for case in cases:
        index = case["index"]
        indices = applicable_complements(case["bits"])
        need(indices == case["omitted"] == published[index]["omitted"], f"applications c{index}")
        need(all(case[key] == published[index][key] for key in ("bits", "labeled", "base")),
             f"published identity c{index}")
        base = work / f"c{index}.base.cnf"
        formula = work / f"c{index}.cnf"
        need(digest(base) == case["base"], f"base hash c{index}")
        need(digest(formula) == published[index]["formula"], f"formula hash c{index}")
        check_base(parent, base, case["bits"])
        audit = check_formula(base, formula, indices)
        need(audit["variables"] == published[index]["audit"]["variables"] and
             audit["clauses"] == published[index]["audit"]["clauses"], f"formula dimensions c{index}")
        applications += len(indices)
        histogram[str(len(indices))] = histogram.get(str(len(indices)), 0) + 1
        formula_sizes[str(len(indices))] = {"variables": audit["variables"], "clauses": audit["clauses"]}

    need(applications == 56 and histogram == {"1": 14, "2": 19, "4": 1}, "application totals")
    need(sum(row["labeled"] for row in cases) == 24057, "starting labeled total")
    need(tuple(json.loads((source / "result.json").read_text())["excluded"]) == EXCLUDED, "excluded list")
    newly_excluded_labeled = sum(published[index]["labeled"] for index in EXCLUDED)
    need(newly_excluded_labeled == 7452, "new excluded labeled count")
    replays = [replay_data(work, index, published[index]) for index in EXCLUDED]
    need(sum(row["rat_core_lemmas"] for row in replays) == 6077, "RAT total")

    report = {
        "format": "r55-order3-eleven-anchor-propagation-review1-v1",
        "all_checks_passed": True,
        "parent": digest(parent),
        "cases_checked": 34,
        "starting_labeled_cores": 24057,
        "applications_checked": applications,
        "application_histogram": histogram,
        "formula_dimensions": formula_sizes,
        "truth_tables": check_truth_tables(),
        "whole_core_exclusions": list(EXCLUDED),
        "newly_excluded_classes": len(EXCLUDED),
        "newly_excluded_labeled": newly_excluded_labeled,
        "fresh_replays": replays,
        "rat_core_lemmas": sum(row["rat_core_lemmas"] for row in replays),
        "reviewer_kissat": digest(args.kissat),
        "reviewer_drat_trim": digest(args.drat_trim),
        "inconclusive_cases_rerun": False,
        "target_graph_claimed": False,
    }
    args.report.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print("PASS 34 exact formulas, 56 applications, eight fresh full DRAT replays")


if __name__ == "__main__":
    main()
