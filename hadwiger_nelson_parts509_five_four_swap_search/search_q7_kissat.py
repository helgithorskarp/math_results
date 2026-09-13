#!/usr/bin/env python3
"""Kissat-driven CEGAR search for exact q=7 sealed-Parts selections.

The outer formula is the canonical solver-independent binary-counter selector
used by the certificate layer.  Kissat proposes a 134-point pool set with
exactly seven Q5 points which hits every recorded killing set.  The proposal
is then checked against all twenty exact fixed-L colouring interfaces.  Every
compatible colouring is grown and deletion-minimised to a new disjoint
killing set before the next outer formula is built.

Search answers are not proof evidence.  A candidate is merely a trigger for a
separate exact physical and chromatic certificate; an outer UNSAT answer must
receive an independently checked proof trace.
"""
from __future__ import annotations

import argparse
import json
import math
import random
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
PARENT = HERE.parent
SOURCE = PARENT / "hadwiger_nelson_parts509_s_replacement_budget"
sys.path.insert(0, str(SOURCE))
from sgadget import SGadget  # noqa: E402

from certlib import selector_exact_q_cnf  # noqa: E402


def load_rows(path):
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text().splitlines()
            if line.strip()]


def witness_row(gadget, killing, pattern, colouring):
    vertices = sorted(set(gadget.L) | (gadget.Uset - set(killing)))
    assert gadget.check(colouring, gadget.Uset - set(killing))
    return {
        "D": sorted(killing),
        "class_index": pattern,
        "colouring_L_plus_U_minus_D": "".join(
            str(colouring[v]) for v in vertices),
    }


def append_jsonl(path, row):
    with path.open("a") as stream:
        stream.write(json.dumps(row, separators=(",", ":")) + "\n")


def write_json(path, value):
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")


def kissat_model(output, selector_variables):
    values = {}
    for line in output.splitlines():
        if not line.startswith("v "):
            continue
        for literal in map(int, line.split()[1:]):
            if literal:
                values[abs(literal)] = literal > 0
    if len([v for v in values if v <= selector_variables]) != selector_variables:
        raise ValueError("Kissat did not return every selector variable")
    return values


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--import-jsonl", type=Path, action="append", default=[])
    parser.add_argument("--kissat", type=Path, required=True)
    parser.add_argument("--seconds", type=float, default=3600.0)
    parser.add_argument("--max-models", type=int, default=24)
    parser.add_argument("--seed", type=int, default=20260914)
    args = parser.parse_args()

    args.out.mkdir(parents=True, exist_ok=True)
    rows_path = args.out / "new_killing_sets.jsonl"
    models_path = args.out / "models.jsonl"
    state_path = args.out / "state.json"
    candidate_path = args.out / "candidate.json"
    cnf_path = args.out / "selector_q7.cnf"
    certificate = json.loads((HERE / "certificate.json").read_text())
    pool = certificate["pool"]
    q5 = set(certificate["Q5"])
    base_cuts = [row["D"] for row in certificate["killing_sets"]]
    rows = []
    for path in args.import_jsonl:
        rows.extend(load_rows(path))
    rows.extend(load_rows(rows_path))
    seen = {frozenset(d) for d in base_cuts}
    unique_rows = []
    for row in rows:
        d = frozenset(row["D"])
        if d not in seen:
            seen.add(d)
            unique_rows.append(row)
    rows = unique_rows

    gadget = SGadget()
    rng = random.Random(args.seed)
    started = time.time()
    prior_models = len(load_rows(models_path))
    print(json.dumps({
        "event": "start",
        "base_cuts": len(base_cuts),
        "imported_unique_rows": len(rows),
        "prior_models": prior_models,
        "q_count": 7,
    }, sort_keys=True), flush=True)

    for local_model in range(1, args.max_models + 1):
        cuts = base_cuts + [row["D"] for row in rows]
        cnf = selector_exact_q_cnf(pool, sorted(q5), cuts, 7,
                                   certificate["target_pool_order"])
        cnf_path.write_bytes(cnf.dimacs())
        remaining = max(1, math.ceil(args.seconds - (time.time() - started)))
        solve_started = time.time()
        proc = subprocess.run(
            [str(args.kissat), "-q", f"--time={remaining}", str(cnf_path)],
            text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        solve_seconds = time.time() - solve_started
        if proc.returncode == 20:
            state = {
                "status": "outer_unsat_requires_checked_proof",
                "q_count": 7,
                "models_tested_this_run": local_model - 1,
                "models_tested_total": prior_models + local_model - 1,
                "killing_sets": len(cuts),
                "variables": cnf.nvars,
                "clauses": len(cnf.clauses),
                "last_outer_seconds": solve_seconds,
                "elapsed_seconds": time.time() - started,
            }
            write_json(state_path, state)
            print(json.dumps(state, sort_keys=True), flush=True)
            return
        if proc.returncode != 10:
            state = {
                "status": "outer_timeout_or_error",
                "returncode": proc.returncode,
                "q_count": 7,
                "models_tested_this_run": local_model - 1,
                "models_tested_total": prior_models + local_model - 1,
                "killing_sets": len(cuts),
                "last_outer_seconds": solve_seconds,
                "elapsed_seconds": time.time() - started,
            }
            write_json(state_path, state)
            print(json.dumps(state, sort_keys=True), flush=True)
            return

        model = kissat_model(proc.stdout, len(pool))
        selected = {pool[i] for i in range(len(pool)) if model[i + 1]}
        if len(selected) != 134 or len(selected & q5) != 7:
            raise AssertionError("decoded selector has wrong cardinalities")
        if not all(selected & set(d) for d in cuts):
            raise AssertionError("decoded selector misses a killing set")
        sat_patterns = [p for p in range(gadget.np)
                        if gadget.sat_p(selected, p)]
        summary = {
            "model_number_this_run": local_model,
            "model_number_total": prior_models + local_model,
            "S_deleted": sorted(set(gadget.S135) - selected),
            "Q5_added": sorted(selected & q5),
            "sat_patterns": sat_patterns,
            "outer_seconds": solve_seconds,
            "killing_sets_hit": len(cuts),
        }
        append_jsonl(models_path, summary)
        if not sat_patterns:
            result = {
                "status": "candidate_requires_independent_certification",
                "q_count": 7,
                "vertices_total": 508,
                "selected": sorted(selected),
                **summary,
            }
            write_json(candidate_path, result)
            print(json.dumps(result, sort_keys=True), flush=True)
            return

        rng.shuffle(sat_patterns)
        new_rows = []
        for pattern in sat_patterns:
            killing, colouring = gadget.minimal_killing(
                gadget.Uset - selected, pattern, rng=rng, grow=True)
            d = frozenset(killing)
            if d & selected:
                raise AssertionError("new killing set meets its selector")
            if d in seen:
                raise AssertionError("selector violates an existing killing set")
            row = witness_row(gadget, killing, pattern, colouring)
            append_jsonl(rows_path, row)
            rows.append(row)
            new_rows.append(row)
            seen.add(d)
        state = {
            "status": "searching",
            "q_count": 7,
            **summary,
            "cuts_added_this_model": len(new_rows),
            "new_unique_rows_total": len(rows),
            "elapsed_seconds": time.time() - started,
            "interface_sat_calls": gadget.calls,
            "interface_sat_seconds": gadget.time,
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
