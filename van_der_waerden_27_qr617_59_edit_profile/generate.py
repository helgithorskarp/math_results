#!/usr/bin/env python3
"""Generate the42 exact QR617 profile certificates with the published pure kernel."""
import argparse
import hashlib
import importlib.util
import json
import resource
import time
from pathlib import Path
import verify

CORE_PATH = Path(__file__).resolve().parent.parent / "van_der_waerden_27_qr617_mixed_edit_region/generate.py"
spec = importlib.util.spec_from_file_location("qr617_profile_generator_core", CORE_PATH)
core = importlib.util.module_from_spec(spec)
spec.loader.exec_module(core)
select_witness = core.select_witness

# Discovery's case list is separately checked against verify.py's exact cover.
ROOTS = {0: [1, 618, 1235, 1852, 2469, 3086],
         1: [3421, 3468, 3515, 3562, 3609, 3656]}
BOXES = {0: [(27, 1848), (1848, 28), (29, 29), (28, 30)],
         1: [(28, 1848), (1848, 28), (29, 29)]}


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
    for e, roots in ROOTS.items():
        for a, b in BOXES[e]:
            for root in roots:
                name = f"branch-{e}-{root}-{a}-{b}.json"
                target = args.output / name
                initial = None
                cached = False
                case_start = time.monotonic()
                if target.exists():
                    if not args.resume:
                        raise RuntimeError(f"Refusing to overwrite {name}; use another directory")
                    data = json.loads(target.read_text())
                    if (data.get("endpoint"), data.get("root"), data.get("budget")) != (e, root, [a, b]):
                        raise ValueError(f"Mismatched cached branch {name}")
                    if data["status"] == "EXCLUDED":
                        verify.verify_branch(data)
                        cached = True
                    else:
                        state = verify.verify_branch(data, complete=False, include_state=True)
                        initial = {**state, "records": data["records"]}
                if not cached:
                    data = core.conditional_certificate(e, root, [a, b], critical,
                                                        args.seconds_per_case, initial)
                    core.write_certificate(args.output, name, data)
                raw = target.read_bytes()
                item = {"file": name, "bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()}
                manifest.append(item)
                timing = {"file": name, "seconds": round(time.monotonic() - case_start, 3),
                          "status": data["status"], "cached_and_verified": cached}
                timings.append(timing)
                core.write_certificate(args.output, "manifest.json", {"certificates": manifest,
                                        "incomplete": data["status"] != "EXCLUDED"})
                print(json.dumps({**item, **timing}, sort_keys=True), flush=True)
                if data["status"] != "EXCLUDED":
                    print("Incomplete attempt; the saved deductions establish no exclusion.", flush=True)
                    raise SystemExit(1)
    # Mathematical verification is a separate command, not generator status.
    summary = {"agent": "six-vdw-2", "role": "researcher", "generated": len(manifest),
               "seconds": round(time.monotonic() - start, 3),
               "max_rss_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
               "weight_guides": 0, "branch_timings": timings}
    core.write_certificate(args.output, "generation-summary.json", summary)
    print(json.dumps({k: v for k, v in summary.items() if k != "branch_timings"}, sort_keys=True))


if __name__ == "__main__":
    main()
