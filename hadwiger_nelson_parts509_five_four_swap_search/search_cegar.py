#!/usr/bin/env python3
"""Search the first open Parts sealed-pool record stratum.

Select 130 of the 135 S vertices and four of the 168 Q5 completion points.
Together with the fixed 374-point L block this is an exact 508-point graph.
The outer SAT problem hits every known killing set.  A four-colouring of an
outer candidate is grown to a new, disjoint, inclusion-minimal killing set,
which becomes another outer clause.  A candidate accepted by all twenty
interface UNSAT tests is written immediately for independent certification.

This is discovery code: SAT answers guide the search.  A positive record still
requires a separately checked exact graph and a replayable four-colour UNSAT
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
from pysat.solvers import Cadical195

HERE = Path(__file__).resolve().parent
PARENT = HERE.parent
SOURCE = PARENT / "hadwiger_nelson_parts509_s_replacement_budget"
sys.path.insert(0, str(SOURCE))
from sgadget import SGadget  # noqa: E402


def initial_cuts():
    cuts = []
    for name in ("general_pool_dual_certificate.json", "certificate.json"):
        data = json.loads((SOURCE / name).read_text())
        cuts.extend(frozenset(row["D"]) for row in data["killing_sets"])
    return cuts


def minimal_family(cuts):
    ordered = sorted(set(cuts), key=lambda d: (len(d), tuple(sorted(d))))
    kept = []
    for d in ordered:
        if not any(e <= d for e in kept):
            kept.append(d)
    return kept


def outer_candidate(gadget, cuts, q_count):
    index = {v: i + 1 for i, v in enumerate(gadget.U)}
    clauses = []
    top = len(gadget.U)
    for vertices, bound in ((gadget.S135, 134 - q_count),
                            (gadget.Q5, q_count)):
        card = CardEnc.equals(
            lits=[index[v] for v in vertices], bound=bound,
            top_id=top, encoding=EncType.totalizer)
        clauses.extend(card.clauses)
        top = card.nv
    clauses.extend([index[v] for v in d] for d in cuts)
    with Cadical195(bootstrap_with=clauses) as solver:
        if not solver.solve():
            return None, {"variables": top, "clauses": len(clauses)}
        model = set(solver.get_model())
    selected = sorted(v for v in gadget.U if index[v] in model)
    assert len(selected) == 134
    return selected, {"variables": top, "clauses": len(clauses)}


def witness_row(gadget, killing, pattern, colouring):
    vertices = sorted(set(gadget.L) | (gadget.Uset - set(killing)))
    assert gadget.check(colouring, gadget.Uset - set(killing))
    return {
        "D": sorted(killing),
        "class_index": pattern,
        "colouring_L_plus_U_minus_D": "".join(str(colouring[v]) for v in vertices),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--q-count", type=int, default=4)
    parser.add_argument("--seed", type=int, default=20260913)
    parser.add_argument("--seconds", type=float, default=900.0)
    parser.add_argument("--max-rounds", type=int, default=1000000)
    parser.add_argument("--cuts-per-pattern", type=int, default=1)
    parser.add_argument("--import-jsonl", type=Path, action="append", default=[],
                        help="additional valid killing-set rows from another stratum")
    args = parser.parse_args()
    if not 0 <= args.q_count <= 134:
        raise ValueError("q-count must lie in 0..134")

    args.out.mkdir(parents=True, exist_ok=True)
    rows_path = args.out / "new_killing_sets.jsonl"
    result_path = args.out / "candidate.json"
    state_path = args.out / "state.json"
    rng = random.Random(args.seed)
    gadget = SGadget()

    cuts = initial_cuts()
    seen = set(cuts)
    imported = 0
    for imported_path in args.import_jsonl:
        if not imported_path.exists():
            continue
        for line in imported_path.read_text().splitlines():
            if line.strip():
                d = frozenset(json.loads(line)["D"])
                if d not in seen:
                    cuts.append(d)
                    seen.add(d)
                    imported += 1
    resumed = []
    if rows_path.exists():
        for line in rows_path.read_text().splitlines():
            if line.strip():
                row = json.loads(line)
                d = frozenset(row["D"])
                resumed.append(row)
                if d not in seen:
                    cuts.append(d)
                    seen.add(d)

    started = time.time()
    print(json.dumps({"event": "start", "initial_cuts": len(initial_cuts()),
                      "imported_cuts": imported, "resumed_cuts": len(resumed),
                      "q_count": args.q_count}),
          flush=True)
    for round_number in range(1, args.max_rounds + 1):
        family = minimal_family(cuts)
        t = time.time()
        selected, outer = outer_candidate(gadget, family, args.q_count)
        outer_seconds = time.time() - t
        if selected is None:
            state = {
                "status": "outer_unsat_discovery_only",
                "round": round_number,
                "q_count": args.q_count,
                "cuts": len(cuts),
                "minimal_cuts": len(family),
                "elapsed_seconds": time.time() - started,
                **outer,
            }
            state_path.write_text(json.dumps(state, indent=2, sort_keys=True) + "\n")
            print(json.dumps(state), flush=True)
            return

        sat_patterns = [p for p in range(gadget.np)
                        if gadget.sat_p(selected, p)]
        if not sat_patterns:
            result = {
                "status": "candidate_requires_independent_certification",
                "q_count": args.q_count,
                "vertices_total": 374 + len(selected),
                "selected": selected,
                "S_selected": sorted(set(selected) & set(gadget.S135)),
                "S_deleted": sorted(set(gadget.S135) - set(selected)),
                "Q5_selected": sorted(set(selected) & set(gadget.Q5)),
                "round": round_number,
                "cuts": len(cuts),
                "minimal_cuts": len(family),
                "elapsed_seconds": time.time() - started,
                "interface_sat_calls": gadget.calls,
                "interface_sat_seconds": gadget.time,
            }
            result_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
            print(json.dumps(result), flush=True)
            return

        rng.shuffle(sat_patterns)
        added = 0
        for pattern in sat_patterns:
            for _ in range(args.cuts_per_pattern):
                killing, colouring = gadget.minimal_killing(
                    gadget.Uset - set(selected), pattern, rng=rng, grow=True)
                d = frozenset(killing)
                if d & set(selected):
                    raise AssertionError("new killing set is not disjoint from candidate")
                if d in seen:
                    continue
                row = witness_row(gadget, killing, pattern, colouring)
                with rows_path.open("a") as stream:
                    stream.write(json.dumps(row, separators=(",", ":")) + "\n")
                cuts.append(d)
                seen.add(d)
                added += 1

        state = {
            "status": "searching",
            "round": round_number,
            "q_count": args.q_count,
            "selected_S": len(set(selected) & set(gadget.S135)),
            "selected_Q5": len(set(selected) & set(gadget.Q5)),
            "deleted_S": sorted(set(gadget.S135) - set(selected)),
            "added_Q5": sorted(set(selected) & set(gadget.Q5)),
            "sat_patterns": len(sat_patterns),
            "new_cuts": added,
            "cuts": len(cuts),
            "minimal_cuts": len(family),
            "outer_seconds": outer_seconds,
            "elapsed_seconds": time.time() - started,
            "interface_sat_calls": gadget.calls,
            "interface_sat_seconds": gadget.time,
            **outer,
        }
        state_path.write_text(json.dumps(state, indent=2, sort_keys=True) + "\n")
        print(json.dumps(state), flush=True)
        if time.time() - started >= args.seconds:
            state["status"] = "time_limit"
            state_path.write_text(json.dumps(state, indent=2, sort_keys=True) + "\n")
            print(json.dumps(state), flush=True)
            return


if __name__ == "__main__":
    main()
