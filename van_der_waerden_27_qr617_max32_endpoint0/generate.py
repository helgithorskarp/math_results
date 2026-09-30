#!/usr/bin/env python3
"""Generate the six endpoint-zero ORIGINAL equal-cap31 root cases without private certificate inputs."""
import argparse, importlib.util, json, resource, time
from pathlib import Path
import verify as v

CORE_PATH = Path(__file__).resolve().parent.parent / "van_der_waerden_27_qr617_mixed_edit_region/generate.py"
spec = importlib.util.spec_from_file_location("qr617_endpoint0_max32_pure_generator", CORE_PATH)
core = importlib.util.module_from_spec(spec)
spec.loader.exec_module(core)
SPLIT_APS = {(0, 1, 31, 31): [1, 285]}


def empty_trace(e, root, B):
    return {"format": v.TRACE_FORMAT, "endpoint": e, "root": root,
            "budget": B.copy(), "status": "STALLED", "records": [], "contradiction": {}}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=Path("build"))
    parser.add_argument("--seconds-per-case", type=float, default=90)
    parser.add_argument("--resume", action="store_true")
    args = parser.parse_args()
    if not 0 < args.seconds_per_case <= 90:
        parser.error("Each primitive search case must have a positive limit of at most90 seconds")
    args.output.mkdir(parents=True, exist_ok=True)
    start = time.monotonic()
    critical = None
    manifest = []
    progress_path = args.output / "generation-progress.json"
    if progress_path.exists() and not args.resume:
        raise RuntimeError("Saved progress exists; use --resume or a fresh directory")
    timings = json.loads(progress_path.read_text())["case_timings"] if args.resume and progress_path.exists() else []

    def generate_trace(e, root, B, child=None, initial=None):
        nonlocal critical
        # Record the attempt before discovery; an interruption is never
        # silently retried as if the child were still an untouched slot.
        row = {"endpoint": e, "root": root, "budget": B.copy(), "child": child,
               "status": "STARTED", "seconds": None}
        timings.append(row)
        core.write_certificate(args.output, "generation-progress.json", {"case_timings": timings})
        primitive_start = time.monotonic()
        if critical is None:
            critical = core.critical_progressions()
        trace = core.conditional_certificate(e, root, B, critical, args.seconds_per_case, initial)
        row.update(status=trace["status"], seconds=round(time.monotonic()-primitive_start,3))
        return trace

    def save_progress():
        core.write_certificate(args.output, "generation-progress.json", {"case_timings": timings})
    for e, root, B in v.cases():
        name = v.filename(e, root, B)
        target = args.output / name
        cached = target.exists()
        if cached:
            if not args.resume:
                raise RuntimeError("Refusing to overwrite a saved proof; use --resume or another directory")
            data = json.loads(target.read_text())
            v.require((data.get("endpoint"), data.get("root"), data.get("budget")) == (e, root, B),
                      "Wrong saved quantified case")
            state = v.verify_tree(data, complete=False, include_state=True)
            if state["closed"]:
                # All nodes, terminal deductions and full child covers were
                # replayed above. Complete=False only permits an open return;
                # closed=True already proves this entire cached case.
                manifest.append(core.write_certificate(args.output, name, data))
                core.write_certificate(args.output, "manifest.json", {"certificates": manifest})
                print(json.dumps({"endpoint": e, "root": root, "budget": B,
                                  "exactly_closed": True, "cached": True}, sort_keys=True), flush=True)
                continue
        else:
            if any(t["endpoint"] == e and t["root"] == root and
                   t["budget"] == B and t["child"] is None for t in timings):
                raise RuntimeError("Recorded primitive has no saved proof; no automatic retry")
            trace = generate_trace(e, root, B)
            data = {"format": v.FORMAT, "endpoint": e, "root": root, "budget": B,
                    "node": {"trace": trace}}
            core.write_certificate(args.output, name, data)
            state = v.verify_tree(data, complete=False, include_state=True)
            save_progress()
            if trace["status"] == "INCOMPLETE_TIME_LIMIT":
                print("Checked partial parent saved; no exclusion follows.", flush=True)
                raise SystemExit(1)
        parent = data["node"]
        if not state["closed"] and "split" not in parent and parent["trace"]["status"] == "INCOMPLETE_TIME_LIMIT":
            raise RuntimeError("Saved timed-out parent proves no exclusion; preserve it and report the limit")
        if not state["closed"] and "split" not in parent:
            ap = SPLIT_APS.get((e, root, *B))
            if ap is None:
                raise RuntimeError("Stalled parent has no published covering AP; no exclusion follows")
            leaf = state["leaves"][0]
            petal = v.core.mandatory_clause(ap, e, set(leaf["forced_positions"])) & set(leaf["allowed_positions"])
            v.require(petal, "An empty mandatory petal needs a checked terminal")
            parent["split"] = {"ap": ap, "children": [
                {"assumption": w, "node": {"trace": empty_trace(e, root, B)}} for w in sorted(petal)]}
            v.verify_tree(data, complete=False)
            core.write_certificate(args.output, name, data)
        for child in parent.get("split", {}).get("children", []):
            w = child["assumption"]
            state = v.verify_tree(data, complete=False, include_state=True)
            leaf = next(x for x in state["leaves"] if x["path"] == [w])
            if leaf["closed"]:
                continue
            previous = child["node"]["trace"]
            if previous["status"] == "INCOMPLETE_TIME_LIMIT":
                raise RuntimeError("Saved timed-out child proves no exclusion; preserve it and report the limit")
            attempted = any(t["endpoint"] == e and t["root"] == root and
                            t["budget"] == B and t["child"] == w for t in timings)
            if attempted or (previous["status"] == "STALLED" and previous["records"]):
                raise RuntimeError("A saved stalled child needs a new justified cover, not repeated search")
            initial = {**leaf, "records": previous["records"]}
            trace = generate_trace(e, root, B, w, initial)
            child["node"]["trace"] = trace
            core.write_certificate(args.output, name, data)
            state = v.verify_tree(data, complete=False, include_state=True)
            leaf = next(x for x in state["leaves"] if x["path"] == [w])
            save_progress()
            if not leaf["closed"]:
                print("Checked partial child saved; no endpoint0 max32 exclusion follows.", flush=True)
                raise SystemExit(1)
        v.verify_tree(data)
        manifest.append(core.write_certificate(args.output, name, data))
        core.write_certificate(args.output, "manifest.json", {"certificates": manifest})
        core.write_certificate(args.output, "generation-progress.json", {"case_timings": timings})
        print(json.dumps({"endpoint": e, "root": root, "budget": B,
                          "exactly_closed": True, "cached": cached}, sort_keys=True), flush=True)
    summary = {"agent": "six-vdw-2", "role": "researcher", "generated": len(manifest),
               "seconds": round(time.monotonic()-start, 3),
               "max_rss_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
               "case_timings": timings}
    core.write_certificate(args.output, "resume-summary.json" if args.resume else "generation-summary.json", summary)
    print(json.dumps({k: value for k, value in summary.items() if k != "case_timings"}, sort_keys=True))


if __name__ == "__main__":
    main()
