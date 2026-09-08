#!/usr/bin/env python3
"""Instantiate the generic suffix metadata in every h3887 macro class."""
from pathlib import Path
import argparse
import json
import stratify


def need(ok, message):
    if not ok:
        raise ValueError(message)


def run(cache):
    expected = json.loads((Path(__file__).resolve().parent / "DIMENSIONS.json").read_text())
    rows = []
    for wanted in expected["rows"]:
        q, r = wanted["q"], wanted["r"]
        task = f"bo1-q{q}-r{r}-c000000"
        # The suffix numbering and dimensions are independent of the optional
        # shared-triangle base.  Use the much smaller direct build here; the
        # complete triangle form is audited separately in FORMULA_AUDIT.json.
        meta = stratify.build(task, cache, False)[-1]
        need(meta["variables"] - meta["k4_expansion_variables"] ==
             wanted["added_variables"], "added variables")
        need(meta["clauses"] - meta["k4_expansion_clauses"] ==
             wanted["added_clauses"], "added clauses")
        need(meta["contact_stratum_clauses"] ==
             wanted["contact_stratum_clauses"], "contact clauses")
        rows.append({
            "task": task,
            "q": q,
            "r": r,
            "red_blocks": r,
            "blue_blocks": q - r,
            "k4_expansion_variables": meta["k4_expansion_variables"],
            "k4_expansion_clauses": meta["k4_expansion_clauses"],
            "stratified_variables": meta["variables"],
            "stratified_clauses": meta["clauses"],
        })
    need(len(rows) == 18, "complete macro-class instantiation")
    return {"status": "VERIFIED_ALL_MACRO_CLASS_INSTANTIATIONS",
            "macro_classes": len(rows), "rows": rows,
            "solver_calls": 0, "target43_found": False}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("cache", type=Path)
    args = parser.parse_args()
    print(json.dumps(run(args.cache), indent=2, sort_keys=True))
