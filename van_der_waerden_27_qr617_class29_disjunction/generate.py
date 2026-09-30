#!/usr/bin/env python3
"""Generate all six exact trees, retaining checked state for bounded resumption."""
import argparse
import importlib.util
import json
import resource
import time
from pathlib import Path
import verify

CORE_PATH = Path(__file__).resolve().parent.parent / "van_der_waerden_27_qr617_mixed_edit_region/generate.py"
spec = importlib.util.spec_from_file_location("qr617_disjunction_generator_core", CORE_PATH)
core = importlib.util.module_from_spec(spec)
spec.loader.exec_module(core)

# Discovery chooses these APs. The checker independently proves they are
# mandatory and reconstructs every child from the surviving allowed petal.
SPLIT_APS = {1: [1, 362], 618: [618, 285], 1235: [1047, 47],
             1852: [1617, 47], 2469: [2253, 54], 3086: [1556, 255]}


def empty_trace(root):
    return {"format": verify.TRACE_FORMAT, "endpoint": 0, "root": root,
            "budget": [28, 1848], "status": "STALLED", "records": [],
            "contradiction": {}}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=Path("build"))
    parser.add_argument("--seconds-per-case", type=float, default=90)
    parser.add_argument("--resume", action="store_true")
    args = parser.parse_args()
    if not 0 < args.seconds_per_case <= 90:
        parser.error("seconds-per-case must be positive and at most90")
    args.output.mkdir(parents=True, exist_ok=True)
    start = time.monotonic()
    critical = core.critical_progressions()
    manifest, timings = [], []
    roots = sorted(SPLIT_APS)
    if set(roots) != verify.core.endpoint_points(verify.core.ENDPOINT_APS[0], 0):
        raise ValueError("Discovery root list differs from checked endpoint cover")
    for root in roots:
        name = f"tree-0-{root}-28-1848.json"
        target = args.output / name
        if target.exists():
            if not args.resume:
                raise RuntimeError(f"Refusing to overwrite {name}; use another directory")
            data = json.loads(target.read_text())
            if (data.get("endpoint"), data.get("root"), data.get("budget")) != (0, root, [28, 1848]):
                raise ValueError("Wrong cached tree scope")
            verify.verify_tree(data, complete=False)
        else:
            case_start = time.monotonic()
            parent = core.conditional_certificate(0, root, [28, 1848], critical,
                                                  args.seconds_per_case)
            data = {"format": verify.FORMAT, "endpoint": 0, "root": root,
                    "budget": [28, 1848], "node": {"trace": parent}}
            core.write_certificate(args.output, name, data)
            verify.verify_tree(data, complete=False)
            timings.append({"root": root, "child": None,
                            "seconds": round(time.monotonic() - case_start, 3),
                            "status": parent["status"]})
            if parent["status"] == "INCOMPLETE_TIME_LIMIT":
                print("Saved partial deductions; no exclusion follows.", flush=True)
                raise SystemExit(1)
        state = verify.verify_tree(data, complete=False, include_state=True)
        if (not state["closed"] and "split" not in data["node"] and
                data["node"]["trace"]["status"] == "INCOMPLETE_TIME_LIMIT"):
            leaf = state["leaves"][0]
            initial = {**leaf, "records": data["node"]["trace"]["records"]}
            parent = core.conditional_certificate(0, root, [28, 1848], critical,
                                                  args.seconds_per_case, initial)
            data["node"]["trace"] = parent
            core.write_certificate(args.output, name, data)
            state = verify.verify_tree(data, complete=False, include_state=True)
            if parent["status"] == "INCOMPLETE_TIME_LIMIT":
                print("Saved partial parent; no exclusion follows.", flush=True)
                raise SystemExit(1)
        if not state["closed"] and "split" not in data["node"]:
            # A cached open parent is replayed before deriving its child cover.
            leaf = state["leaves"][0]
            petal = verify.core.mandatory_clause(SPLIT_APS[root], 0,
                        set(leaf["forced_positions"])) & set(leaf["allowed_positions"])
            if not petal:
                raise ValueError("Chosen split has no allowed mandatory petal")
            data["node"]["split"] = {"ap": SPLIT_APS[root], "children": [
                {"assumption": w, "node": {"trace": empty_trace(root)}}
                for w in sorted(petal)]}
            verify.verify_tree(data, complete=False)
            core.write_certificate(args.output, name, data)
        for child in data["node"].get("split", {}).get("children", []):
            if "split" in child["node"]:
                raise ValueError("Generator resumes only its specified one-level cover")
            w = child["assumption"]
            before = verify.verify_tree(data, complete=False, include_state=True)
            leaf = next(x for x in before["leaves"] if x["path"] == [w])
            if leaf["closed"]:
                continue
            case_start = time.monotonic()
            initial = {**leaf, "records": child["node"]["trace"]["records"]}
            trace = core.conditional_certificate(0, root, [28, 1848], critical,
                                                args.seconds_per_case, initial)
            child["node"]["trace"] = trace
            core.write_certificate(args.output, name, data)
            after = verify.verify_tree(data, complete=False)
            leaf = next(x for x in after["leaves"] if x["path"] == [w])
            timing = {"root": root, "child": w,
                      "seconds": round(time.monotonic() - case_start, 3),
                      "status": trace["status"], "checked_closed": leaf["closed"]}
            timings.append(timing)
            core.write_certificate(args.output, "generation-progress.json", {"cases": timings})
            print(json.dumps(timing, sort_keys=True), flush=True)
            if not leaf["closed"]:
                print("Saved partial deductions; no parent or class exclusion follows.", flush=True)
                raise SystemExit(1)
        verify.verify_tree(data)
        manifest.append(core.write_certificate(args.output, name, data))
        core.write_certificate(args.output, "manifest.json", {"certificates": manifest})
    # Separate verify.py establishes complete quantified coverage, not this status.
    summary = {"agent": "six-vdw-2", "role": "researcher", "generated": len(manifest),
               "seconds": round(time.monotonic() - start, 3),
               "max_rss_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
               "case_timings": timings}
    core.write_certificate(args.output, "generation-summary.json", summary)
    print(json.dumps({k: v for k, v in summary.items() if k != "case_timings"}, sort_keys=True))


if __name__ == "__main__":
    main()
