#!/usr/bin/env python3
"""Incremental exact search of the first open sealed-Parts stratum.

At q=7 an order-508 pool selection deletes exactly eight vertices of S and
adds exactly seven vertices of Q5.  Use deletion variables for S and addition
variables for Q5.  A killing set D is missed precisely when all of D intersect
S is deleted and none of D intersect Q5 is added, so its selector clause is

    OR_{s in D intersect S} not delete_s  OR  OR_{q in D intersect Q5} add_q.

If D contains more than eight S vertices the clause is automatically true and
is omitted.  Unlike search_cegar.py, the outer SAT solver is kept alive across
rounds, preserving all learned clauses when new killing sets are added.

This is candidate-generation code, not a proof checker.  Any non-four-colour
signal still requires a clean exact realization and a replayable chromatic
certificate.
"""
from __future__ import annotations

import argparse
import json
import random
import sys
import time
from pathlib import Path

from pysat.card import CardEnc, EncType
from pysat.solvers import Solver

HERE = Path(__file__).resolve().parent
PARENT = HERE.parent
SOURCE = PARENT / "hadwiger_nelson_parts509_s_replacement_budget"
sys.path.insert(0, str(SOURCE))
from sgadget import SGadget  # noqa: E402


ENCODINGS = {
    "seqcounter": EncType.seqcounter,
    "totalizer": EncType.totalizer,
    "mtotalizer": EncType.mtotalizer,
    "kmtotalizer": EncType.kmtotalizer,
    "cardnetwrk": EncType.cardnetwrk,
}


def source_cuts():
    cuts = []
    for name in ("general_pool_dual_certificate.json", "certificate.json"):
        data = json.loads((SOURCE / name).read_text())
        cuts.extend(frozenset(row["D"]) for row in data["killing_sets"])
    return cuts


def load_rows(path):
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text().splitlines()
            if line.strip()]


def minimal_family(cuts):
    ordered = sorted(set(cuts), key=lambda d: (len(d), tuple(sorted(d))))
    kept = []
    for d in ordered:
        if not any(e <= d for e in kept):
            kept.append(d)
    return kept


class IncrementalOuter:
    def __init__(self, gadget, cuts, encoding, solver_name):
        self.gadget = gadget
        self.S = set(gadget.S135)
        self.Q = set(gadget.Q5)
        self.dvar = {v: i + 1 for i, v in enumerate(gadget.S135)}
        offset = len(self.dvar)
        self.avar = {v: offset + i + 1 for i, v in enumerate(gadget.Q5)}
        top = len(gadget.U)
        clauses = []
        for lits, bound in ((list(self.dvar.values()), 8),
                            (list(self.avar.values()), 7)):
            card = CardEnc.equals(lits=lits, bound=bound, top_id=top,
                                  encoding=ENCODINGS[encoding])
            clauses.extend(card.clauses)
            top = card.nv
        self.variables = top
        self.cardinality_clauses = len(clauses)
        self.active_cuts = 0
        self.tautological_cuts = 0
        for d in cuts:
            clause = self.cut_clause(d)
            if clause is None:
                self.tautological_cuts += 1
            else:
                clauses.append(clause)
                self.active_cuts += 1
        self.solver = Solver(name=solver_name, bootstrap_with=clauses)
        self.total_clauses = len(clauses)
        self.solve_calls = 0
        self.solve_seconds = 0.0

    def cut_clause(self, d):
        ds = sorted(set(d) & self.S)
        if len(ds) > 8:
            return None
        dq = sorted(set(d) & self.Q)
        clause = [-self.dvar[v] for v in ds]
        clause.extend(self.avar[v] for v in dq)
        if not clause:
            raise AssertionError("empty killing clause")
        return clause

    def add_cut(self, d):
        clause = self.cut_clause(d)
        if clause is None:
            self.tautological_cuts += 1
            return False
        self.solver.add_clause(clause)
        self.active_cuts += 1
        self.total_clauses += 1
        return True

    def candidate(self):
        started = time.time()
        sat = self.solver.solve()
        elapsed = time.time() - started
        self.solve_calls += 1
        self.solve_seconds += elapsed
        if not sat:
            return None, elapsed
        model = set(x for x in self.solver.get_model() if x > 0)
        deleted = {v for v, x in self.dvar.items() if x in model}
        added = {v for v, x in self.avar.items() if x in model}
        assert len(deleted) == 8
        assert len(added) == 7
        selected = (self.S - deleted) | added
        assert len(selected) == 134
        return sorted(selected), elapsed

    def stats(self):
        result = {
            "variables": self.variables,
            "cardinality_clauses": self.cardinality_clauses,
            "active_cut_clauses": self.active_cuts,
            "tautological_cuts_omitted": self.tautological_cuts,
            "total_clauses": self.total_clauses,
            "outer_solve_calls": self.solve_calls,
            "outer_solve_seconds": self.solve_seconds,
        }
        try:
            result["solver_stats"] = self.solver.accum_stats()
        except (AttributeError, NotImplementedError):
            pass
        return result


def witness_row(gadget, killing, pattern, colouring):
    vertices = sorted(set(gadget.L) | (gadget.Uset - set(killing)))
    assert gadget.check(colouring, gadget.Uset - set(killing))
    return {
        "D": sorted(killing),
        "class_index": pattern,
        "colouring_L_plus_U_minus_D": "".join(
            str(colouring[v]) for v in vertices),
    }


def write_json(path, value):
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--import-jsonl", type=Path, action="append", default=[])
    parser.add_argument("--seconds", type=float, default=3600.0)
    parser.add_argument("--max-models", type=int, default=24)
    parser.add_argument("--seed", type=int, default=20260914)
    parser.add_argument("--encoding", choices=sorted(ENCODINGS),
                        default="kmtotalizer")
    parser.add_argument("--outer-solver", default="cadical195")
    args = parser.parse_args()

    args.out.mkdir(parents=True, exist_ok=True)
    rows_path = args.out / "new_killing_sets.jsonl"
    state_path = args.out / "state.json"
    candidate_path = args.out / "candidate.json"
    rng = random.Random(args.seed)
    gadget = SGadget()

    cuts = source_cuts()
    seen = set(cuts)
    imported_rows = 0
    for path in args.import_jsonl:
        for row in load_rows(path):
            d = frozenset(row["D"])
            if d not in seen:
                cuts.append(d)
                seen.add(d)
            imported_rows += 1
    resumed = load_rows(rows_path)
    for row in resumed:
        d = frozenset(row["D"])
        if d not in seen:
            cuts.append(d)
            seen.add(d)

    family = minimal_family(cuts)
    build_started = time.time()
    outer = IncrementalOuter(gadget, family, args.encoding, args.outer_solver)
    build_seconds = time.time() - build_started
    started = time.time()
    start = {
        "event": "start",
        "q_count": 7,
        "source_cut_rows": len(source_cuts()),
        "imported_rows": imported_rows,
        "resumed_rows": len(resumed),
        "distinct_cuts": len(seen),
        "minimal_cuts": len(family),
        "encoding": args.encoding,
        "outer_solver": args.outer_solver,
        "outer_build_seconds": build_seconds,
        **outer.stats(),
    }
    print(json.dumps(start, sort_keys=True), flush=True)

    for model_number in range(1, args.max_models + 1):
        selected, outer_seconds = outer.candidate()
        if selected is None:
            state = {
                "status": "outer_unsat_discovery_only",
                "q_count": 7,
                "models_tested": model_number - 1,
                "new_killing_sets": len(resumed),
                "elapsed_seconds": time.time() - started,
                "last_outer_seconds": outer_seconds,
                **outer.stats(),
            }
            write_json(state_path, state)
            print(json.dumps(state, sort_keys=True), flush=True)
            return

        sat_patterns = [p for p in range(gadget.np)
                        if gadget.sat_p(selected, p)]
        if not sat_patterns:
            result = {
                "status": "candidate_requires_independent_certification",
                "q_count": 7,
                "vertices_total": 508,
                "selected": selected,
                "S_selected": sorted(set(selected) & set(gadget.S135)),
                "S_deleted": sorted(set(gadget.S135) - set(selected)),
                "Q5_selected": sorted(set(selected) & set(gadget.Q5)),
                "models_tested": model_number,
                "new_killing_sets": len(resumed),
                "elapsed_seconds": time.time() - started,
                "interface_sat_calls": gadget.calls,
                "interface_sat_seconds": gadget.time,
                **outer.stats(),
            }
            write_json(candidate_path, result)
            print(json.dumps(result, sort_keys=True), flush=True)
            return

        rng.shuffle(sat_patterns)
        added_count = 0
        for pattern in sat_patterns:
            killing, colouring = gadget.minimal_killing(
                gadget.Uset - set(selected), pattern, rng=rng, grow=True)
            d = frozenset(killing)
            if d & set(selected):
                raise AssertionError("new killing set meets current candidate")
            if d in seen:
                raise AssertionError("current candidate violates an existing cut")
            row = witness_row(gadget, killing, pattern, colouring)
            with rows_path.open("a") as stream:
                stream.write(json.dumps(row, separators=(",", ":")) + "\n")
            cuts.append(d)
            seen.add(d)
            resumed.append(row)
            if not outer.add_cut(d):
                raise AssertionError("a disjoint q=7 killing set became tautological")
            added_count += 1

        state = {
            "status": "searching",
            "q_count": 7,
            "model_number": model_number,
            "S_deleted": sorted(set(gadget.S135) - set(selected)),
            "Q5_added": sorted(set(selected) & set(gadget.Q5)),
            "sat_patterns": len(sat_patterns),
            "cuts_added_this_model": added_count,
            "new_killing_sets": len(resumed),
            "distinct_cuts": len(seen),
            "last_outer_seconds": outer_seconds,
            "elapsed_seconds": time.time() - started,
            "interface_sat_calls": gadget.calls,
            "interface_sat_seconds": gadget.time,
            **outer.stats(),
        }
        write_json(state_path, state)
        print(json.dumps(state, sort_keys=True), flush=True)
        if time.time() - started >= args.seconds:
            state["status"] = "time_limit"
            write_json(state_path, state)
            print(json.dumps(state, sort_keys=True), flush=True)
            return

    state["status"] = "model_limit"
    write_json(state_path, state)
    print(json.dumps(state, sort_keys=True), flush=True)


if __name__ == "__main__":
    main()
