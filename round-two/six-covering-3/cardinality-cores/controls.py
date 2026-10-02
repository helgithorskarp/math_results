"""Damage controls and exhaustive Boolean cardinality boundary checks."""

import argparse
from copy import deepcopy
from itertools import product
import json
from pathlib import Path
import resource
import time

from audit import read_formula, model_for, satisfied
from check import audit, require
from encode import Formula
from model import evaluate


def rejected(function, argument):
    try:
        function(argument)
    except (ValueError, TypeError, KeyError, IndexError):
        return True
    return False


def run(single_path, full_path):
    root = Path(__file__).resolve().parent
    certificate = json.loads((root / "certificate.json").read_text())
    damages = []
    def damaged(name, edit):
        c = deepcopy(certificate)
        edit(c)
        require(rejected(audit, c), "certificate damage accepted: " + name)
        damages.append(name)
    damaged("wrong pool label", lambda c: c["D"].__setitem__(-1, 287))
    damaged("missing original predicate", lambda c: c["implications"].pop())
    damaged("duplicate target predicate", lambda c: c["implications"].__setitem__(0, c["implications"][1]))
    damaged("boolean target mask", lambda c: c["implications"][0].__setitem__(0, True))
    damaged("boolean witness index", lambda c: c["implications"][0].__setitem__(1, True))
    damaged("negative witness index", lambda c: c["implications"][0].__setitem__(1, -1))
    damaged("cloned original support resource", lambda c: c["frontier"][0]["pairs"][0].__setitem__(1, c["frontier"][0]["pairs"][0][0]))
    damaged("missing minimal support pair", lambda c: c["frontier"][0]["pairs"].pop(2))
    damaged("reversed implication", lambda c: c["implications"][0].__setitem__(1, 1))
    damaged("wrong threshold", lambda c: c["frontier"][0].__setitem__("required", 2))
    damaged("wrong prefix domain", lambda c: c["prefix"][-1].__setitem__(1, 4))
    damaged("missing shared base resource", lambda c: c["base_moduli"].pop())
    control = json.loads((root / "core-control.json").read_text())
    base = control["base_phases"]
    bad_inputs = [base[:-1], base + [base[0]], {str(d): a for d, a in base},
                  [[True, 0]] + base[1:], [[base[0][0], -1]] + base[1:],
                  [[base[0][0], base[0][0]]] + base[1:]]
    require(all(rejected(evaluate, p) for p in bad_inputs), "malformed base input accepted")

    truth_cases = 0
    for m in range(8):
        f = Formula()
        xs = [f.variable(("toy", i)) for i in range(m)]
        f.at_most_one(xs, ("toy",))
        auxiliary = len(f.names) - m
        for bits in product((False, True), repeat=m):
            possible = False
            for extra in product((False, True), repeat=auxiliary):
                values = (False,) + bits + extra
                if all(any(values[abs(v)] == (v > 0) for v in clause) for clause in f.clauses):
                    possible = True
                    break
            require(possible == (sum(bits) <= 1), "sequential counter truth table")
            truth_cases += 1
    full_names, full_clauses, full_meta = read_formula(full_path)
    cardinality_cases = 0
    for j, row in enumerate(full_meta["rows"]):
        zs = {i for i, name in enumerate(full_names, 1) if name[0] == "qualified" and name[1] == j}
        clauses = [c for c in full_clauses if c and all(v in zs for v in c)]
        ordered = sorted(zs)
        require(len(ordered) == 7, "lost labeled fibers")
        for bits in product((False, True), repeat=7):
            truth = {v for v, b in zip(ordered, bits) if b}
            require(satisfied(clauses, truth) == (sum(bits) >= row["required"]), "fiber cardinality truth table")
            cardinality_cases += 1
    names, clauses, meta = read_formula(single_path)
    lookup = {name: i for i, name in enumerate(names, 1)}
    original = model_for(names, control)
    require(satisfied(clauses, original), "positive control")
    def refresh(truth):
        truth = {v for v in truth if names[v - 1][0] != "counter"}
        first = {}
        for v in truth:
            name = names[v - 1]
            if name[0] in ("base", "witness"):
                first[name[:-1]] = min(first.get(name[:-1], name[-1]), name[-1])
        for name, v in lookup.items():
            if name[0] == "counter":
                key, end = name[1:-1], name[-1]
                if key in first and first[key] <= end:
                    truth.add(v)
        return truth
    model_damages = []
    def bad_model(name, add=(), remove=()):
        truth = set(original)
        truth.update(lookup[v] for v in add)
        truth.difference_update(lookup[v] for v in remove)
        require(not satisfied(clauses, refresh(truth)), "Boolean model damage accepted: " + name)
        model_damages.append(name)
    bad_model("duplicate original15 phase", add=(("base", 15, 0),))
    bad_model("missing original15 phase", remove=(("base", 15, 4),))
    bad_model("duplicate witness5 phase", add=(("witness", 0, 1, 5, 0),))
    bad_model("three distinct witness resources", add=(("resource", 0, 1, 7), ("witness", 0, 1, 7, 0)))
    bad_model("wrong literal cofactor phase", add=(("witness", 0, 1, 9, 4),), remove=(("witness", 0, 1, 9, 5),))
    bad_model("lost third selected fiber", remove=(("qualified", 0, 5),))
    return {"agent": "six-covering-3", "role": "researcher", "status": "CONTROLS PASSED",
            "certificate_damages": damages, "malformed_base_inputs": len(bad_inputs),
            "sequential_counter_truth_cases": truth_cases,
            "fiber_cardinality_truth_cases": cardinality_cases, "CNF_model_damages": model_damages}


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--full", type=Path, required=True)
    ap.add_argument("--B13", type=Path, required=True)
    args = ap.parse_args()
    start = time.monotonic()
    evidence = run(args.B13, args.full)
    print(json.dumps({"evidence": evidence, "seconds": round(time.monotonic() - start, 6),
                      "max_RSS_KiB": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}, sort_keys=True))
