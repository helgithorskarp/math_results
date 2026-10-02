"""Literal original-residue/point-incidence/model audit of generated CNF."""

import argparse
from hashlib import sha256
import json
from pathlib import Path
import resource
import time

from check import require, local_supports
from model import evaluate, constraints, evaluate_fibers


def read_formula(path):
    metadata = json.loads(path.with_suffix(path.suffix + ".json").read_text())
    names = [tuple(v) for v in metadata["names"]]
    require(len(set(names)) == len(names) == metadata["variables"], "bad variable map")
    clauses = []
    digest = sha256()
    with path.open() as stream:
        header = stream.readline().split()
        require(header == ["p", "cnf", str(len(names)), str(metadata["clauses"])], "CNF header")
        for line in stream:
            digest.update(line.encode())
            values = list(map(int, line.split()))
            require(values and values[-1] == 0 and all(0 < abs(v) <= len(names) for v in values[:-1]), "bad clause")
            clauses.append(tuple(values[:-1]))
    require(len(clauses) == metadata["clauses"] and digest.hexdigest() == metadata["clause_body_sha256"], "CNF body")
    return names, clauses, metadata


def incidence_audit(path):
    names, clauses, meta = read_formula(path)
    prefix = ((8, 0), (9, 0), (10, 1), (14, 1), (12, 10))
    base = tuple(n for n in range(8, 2521) if 2520 % n == 0 and n not in {d for d, a in prefix})
    initial = {x for x in range(2520) if all(x % d != a for d, a in prefix)}
    seen = set()
    for clause in clauses:
        negative_qualifiers = [names[-v - 1] for v in clause if v < 0 and names[-v - 1][0] == "qualified"]
        if not negative_qualifiers:
            continue
        require(len(negative_qualifiers) == 1, "multiple target selectors in point clause")
        _, j, r = negative_qualifiers[0]
        positives = {names[v - 1] for v in clause if v > 0}
        large = [n for n in positives if n[:2] == ("base", 2520)]
        require(len(large) == 1, "point clause lost its original2520 phase")
        x = large[0][2]
        require(x in initial and x % 8 == r, "wrong or independently normalized physical parent")
        row = meta["rows"][j]
        allowed = {d for p in row["pairs"] for d in p}
        expected = {("base", d, x % d) for d in base}
        expected.update(("witness", j, r, d, x % d) for d in allowed)
        require(positives == expected and len(clause) == len(expected) + 1, "wrong original-resource incidence")
        require((j, x) not in seen, "duplicate point clause")
        seen.add((j, x))
    require(seen == {(j, x) for j in range(len(meta["rows"])) for x in initial}, "incomplete point-clause reduction")
    return {"variables": len(names), "clauses": len(clauses),
            "checked_point_clauses": len(seen), "clause_body_sha256": meta["clause_body_sha256"]}


def model_for(names, control):
    lookup = {name: i for i, name in enumerate(names, 1)}
    truth = set()
    for d, a in control["base_phases"]:
        truth.add(lookup[("base", d, a)])
    for r, classes in control["B13_witnesses"]:
        truth.add(lookup[("qualified", 0, r)])
        for d, a in classes:
            truth.add(lookup[("resource", 0, r, d)])
            truth.add(lookup[("witness", 0, r, d, a)])
    # Counter_i is true precisely when a selected phase has index<=i.
    first = {}
    for name, v in lookup.items():
        if v in truth and name[0] in ("base", "witness"):
            first[name[:-1]] = min(first.get(name[:-1], name[-1]), name[-1])
    for name, v in lookup.items():
        if name[0] == "counter":
            key, end = name[1:-1], name[-1]
            if key in first and first[key] <= end:
                truth.add(v)
    return truth


def satisfied(clauses, truth):
    return all(any((abs(v) in truth) == (v > 0) for v in clause) for clause in clauses)


def run(full_path, single_path, control):
    base = control["base_phases"]
    prefix = ((8, 0), (9, 0), (10, 1), (14, 1), (12, 10))
    chosen = prefix + tuple(map(tuple, base))
    physical = {x for x in range(10080) if all(x % d != a for d, a in chosen)}
    fibers = [sorted({x % 315 for x in physical if x % 8 == r}) for r in range(1, 8)]
    require(len(physical) == 4 * sum(map(len, fibers)), "lost physical copies")
    require(control["expected_sizes"] == list(map(len, fibers)), "literal size control")
    evaluated = evaluate(base)
    require(evaluated["fibers"] == fibers, "base adapter differs on original10080 residues")
    labels = tuple(d for d in range(1, 316) if 315 % d == 0)
    ss = [local_supports(f, labels) for f in fibers]
    all_values = {row["B"]: sum(any(not(set(row["B"]) & support) for support in v) for v in ss)
                  for row in constraints()}
    for row in evaluated["predicates"]:
        require(row["Q"] == all_values[tuple(row["B"])], "shape classifier differs from literal phase-set unions")
        for r, witness in enumerate(row["witnesses"], 1):
            if witness is None:
                continue
            classes = witness["classes"]
            require(len(classes) <= 2 and len({d for d, a in classes}) == len(classes), "cloned witness")
            require(all(d in labels and d not in row["B"] and type(a) is int and 0 <= a < d for d, a in classes), "illegal witness phase")
            require(all(any(x % d == a for d, a in classes) for x in fibers[r - 1]), "false literal containment witness")
    require(not evaluated["passed"] and control["expected_failed_B"] == [r["B"] for r in evaluated["predicates"] if not r["passed"]], "full cut control")
    require(all((all_values[row["B"]] >= row["required"]) ==
                evaluate_fibers(fibers, [row])[0]["passed"] for row in constraints()), "all638 classifications differ")
    for r, classes in control["B13_witnesses"]:
        require(len(classes) <= 2 and len(set(d for d, a in classes)) == len(classes), "positive control resource cloning")
        require(all(d in labels and d not in (1, 3) and 0 <= a < d for d, a in classes), "positive control bad phase")
        require(all(any(x % d == a for d, a in classes) for x in fibers[r - 1]), "positive control lost containment")
    require(len({r for r, c in control["B13_witnesses"]}) >= 3, "positive control lost distinct fibers")
    full = incidence_audit(full_path)
    single = incidence_audit(single_path)
    names, clauses, meta = read_formula(single_path)
    require(len(meta["rows"]) == 1 and meta["rows"][0]["B"] == [1, 3], "wrong single-core formula")
    truth = model_for(names, control)
    require(satisfied(clauses, truth), "literal positive control fails generated CNF")
    return {"agent": "six-covering-3", "role": "researcher", "status": "LITERAL CORE AND CNF AUDIT PASSED",
            "original_physical_residues_checked": 10080, "physical_holes": len(physical),
            "base_sizes": list(map(len, fibers)), "B13_qualifying_fibers": [r for r, c in control["B13_witnesses"]],
            "original_predicates_checked": len(all_values),
            "violated_original_predicates": sum(all_values[row["B"]] < row["required"] for row in constraints()),
            "violated_frontier_predicates": len(control["expected_failed_B"]),
            "full_formula": full, "B13_formula": single,
            "scope": "Literal feasible single necessary core; seven compressed cuts reject this same assignment. No tail completion or root exclusion."}


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--full", type=Path, required=True)
    ap.add_argument("--B13", type=Path, required=True)
    ap.add_argument("--control", type=Path, default=Path(__file__).with_name("core-control.json"))
    args = ap.parse_args()
    start = time.monotonic()
    evidence = run(args.full, args.B13, json.loads(args.control.read_text()))
    print(json.dumps({"evidence": evidence, "seconds": round(time.monotonic() - start, 6),
                      "max_RSS_KiB": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}, sort_keys=True))
