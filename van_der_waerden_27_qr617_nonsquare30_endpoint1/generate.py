#!/usr/bin/env python3
"""Generate six direct endpoint-one nonsquare full-width proofs from public source."""
import argparse
import importlib.util
import json
import resource
import time
from pathlib import Path
import verify as v

CORE_PATH = Path(__file__).resolve().parent.parent / "van_der_waerden_27_qr617_mixed_edit_region/generate.py"
spec = importlib.util.spec_from_file_location("qr617_endpoint1_nonsquare30_pure_generator", CORE_PATH)
core = importlib.util.module_from_spec(spec)
spec.loader.exec_module(core)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=Path("build"))
    parser.add_argument("--seconds-per-case", type=float, default=90)
    parser.add_argument("--resume", action="store_true")
    args = parser.parse_args()
    if not 0 < args.seconds_per_case <= 90:
        parser.error("Each primitive case requires a positive cap of at most 90 seconds")
    args.output.mkdir(parents=True, exist_ok=True)
    start = time.monotonic()
    critical = core.critical_progressions()
    manifest, timings = [], []
    for e, root, B in v.cases():
        name = v.filename(e, root, B)
        target = args.output / name
        cached = target.exists()
        if cached:
            if not args.resume:
                raise RuntimeError("Refusing to overwrite a saved proof; use --resume")
            data = json.loads(target.read_text())
            v.require((data.get("endpoint"), data.get("root"), data.get("budget")) == (e, root, B),
                      "Wrong saved quantified case")
            state = v.verify_tree(data, complete=False)
            if not state["closed"]:
                raise RuntimeError("Saved open or timed-out root proves no exclusion; no automatic retry")
        else:
            case_start = time.monotonic()
            trace = core.conditional_certificate(e, root, B, critical, args.seconds_per_case)
            data = {"format": v.FORMAT, "endpoint": e, "root": root, "budget": B,
                    "node": {"trace": trace}}
            core.write_certificate(args.output, name, data)
            state = v.verify_tree(data, complete=False)
            timings.append({"endpoint": e, "root": root, "budget": B,
                            "status": trace["status"], "seconds": round(time.monotonic()-case_start, 3)})
            core.write_certificate(args.output, "generation-progress.json", {"case_timings": timings})
            if not state["closed"]:
                print("Checked partial root saved; no class30 exclusion follows.", flush=True)
                raise SystemExit(1)
        # Complete=False still checks every EXCLUDED leaf's contradiction.
        # closed=True therefore certifies this entire root without another replay.
        manifest.append(core.write_certificate(args.output, name, data))
        core.write_certificate(args.output, "manifest.json", {"certificates": manifest})
        print(json.dumps({"endpoint": e, "root": root, "budget": B,
                          "exactly_closed": True, "cached": cached}, sort_keys=True), flush=True)
    summary = {"agent": "six-vdw-2", "role": "researcher", "generated": len(manifest),
               "seconds": round(time.monotonic()-start, 3),
               "max_rss_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
               "case_timings": timings}
    # Preserve the fresh timings during a cache-only resumption.
    core.write_certificate(args.output, "resume-summary.json" if args.resume else
                           "generation-summary.json", summary)
    print(json.dumps({k: value for k, value in summary.items() if k != "case_timings"}, sort_keys=True))


if __name__ == "__main__":
    main()
