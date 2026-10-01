#!/usr/bin/env python3
"""Generate one bounded primitive, retaining exact checked partial progress."""
import argparse
import importlib.util
import json
import resource
import time
from pathlib import Path
import verify as v

spec = importlib.util.spec_from_file_location("uniform64_square_bitmask_generator",
    v.BASE / "van_der_waerden_27_qr617_mixed_edit_region/generate.py")
g = importlib.util.module_from_spec(spec)
spec.loader.exec_module(g)


def empty_trace(root, B):
    return {"format": v.TRACE_FORMAT, "endpoint": 0, "root": root, "budget": B,
            "status": "STALLED", "records": [], "contradiction": {}}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--output", type=Path, required=True)
    p.add_argument("--budget", type=int, nargs=2, required=True)
    p.add_argument("--root", type=int, required=True)
    p.add_argument("--child", type=int)
    p.add_argument("--seconds", type=float, default=90)
    a = p.parse_args()
    B, root = a.budget, a.root
    v.require(B in v.BUDGETS and root in v.ROOTS and 0 < a.seconds <= 90, "Wrong primitive or cap")
    v.require(a.child is None or (root == 1 and a.child in v.CHILDREN), "Wrong distinct split child")
    a.output.mkdir(parents=True, exist_ok=True)
    attempts = a.output.parent / "attempts"
    attempts.mkdir(exist_ok=True)
    name = v.filename_for(root, B)
    target = a.output / name
    token = f"{B[0]}-{B[1]}-root{root}" + ("-parent" if a.child is None else f"-child{a.child}")
    marker = attempts / (token+".json")
    v.require(not marker.exists(), "Saved or interrupted primitive; never retry automatically")
    initial = None
    if a.child is None:
        v.require(not target.exists(), "A saved parent is not an untouched primitive")
    else:
        data = json.loads(target.read_text())
        v.require((data["endpoint"], data["root"], data["budget"]) == (0, root, B), "Wrong parent case")
        state = v.verify_tree(data, complete=False, include_state=True)
        v.require(not state["closed"], "Complete root needs no further generation")
        node = data["node"]
        if "split" not in node:
            v.require(node["trace"]["status"] == "STALLED", "An incomplete parent is not a split frontier")
            parent = state["leaves"][0]
            K = sorted(v.core.mandatory_clause([1,285], 0, set(parent["forced_positions"])) &
                       set(parent["allowed_positions"]))
            v.require(K == v.CHILDREN, "Changed necessary full split cover")
            parents = a.output.parent / "parents"
            parents.mkdir(exist_ok=True)
            g.write_certificate(parents, name, data)
            node["split"] = {"ap": [1,285], "children": [
                {"assumption": x, "node": {"trace": empty_trace(root, B)}} for x in K]}
            v.verify_tree(data, complete=False)
            g.write_certificate(a.output, name, data)
        v.require(node["split"]["ap"] == [1,285], "Changed saved actual split AP")
        state = v.verify_tree(data, complete=False, include_state=True)
        leaf = next(row for row in state["leaves"] if row["path"] == [a.child])
        child = next(row for row in node["split"]["children"] if row["assumption"] == a.child)
        old = child["node"]["trace"]
        v.require(not leaf["closed"] and old["status"] == "STALLED" and not old["records"],
                  "Saved/open child requires a new justified frontier")
        initial = {**leaf, "records": []}
    attempt = {"endpoint": 0, "root": root, "budget": B, "child": a.child, "status": "STARTED"}
    g.write_certificate(attempts, marker.name, attempt)
    start = time.monotonic()
    critical = g.critical_progressions()
    trace = g.conditional_certificate(0, root, B, critical, a.seconds, initial)
    if a.child is None:
        data = {"format": v.FORMAT, "endpoint": 0, "root": root, "budget": B, "node": {"trace": trace}}
    else:
        child["node"]["trace"] = trace
    entry = g.write_certificate(a.output, name, data)
    state = v.verify_tree(data, complete=False, include_state=True)
    if a.child is None:
        leaf = state["leaves"][0]
        strict = v.core.verify_branch(trace, complete=False, include_state=True)
        v.require(leaf["allowed_positions"] == strict["allowed_positions"] and
                  leaf["forced_positions"] == strict["forced_positions"] and
                  leaf["counts"] == strict["step_counts"], "Full parent states differ")
        if leaf["closed"]:
            v.core.verify_branch(trace)
        v.require((root == 1 and trace["status"] == "STALLED") or leaf["closed"],
                  "Unexpected incomplete parent; no exclusion follows")
    else:
        leaf = next(row for row in state["leaves"] if row["path"] == [a.child])
        v.require(leaf["closed"], "Open child saved; no complete root exclusion follows")
    attempt.update(status=trace["status"], checked_saved=True, closed=leaf["closed"],
                   seconds=round(time.monotonic()-start,3), max_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    g.write_certificate(attempts, marker.name, attempt)
    print(json.dumps({**attempt, "certificate": entry, "root_closed": state["closed"]}), flush=True)


if __name__ == "__main__":
    main()
