"""Sequential source-only normal/optimized replay with20s child guards."""

import argparse
from hashlib import sha256
import json
import os
from pathlib import Path
import subprocess
import sys
import time


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--scratch", type=Path, required=True)
    args = ap.parse_args()
    root = Path(__file__).resolve().parent
    scratch = args.scratch.resolve()
    scratch.mkdir(parents=True, exist_ok=True)
    env = dict(os.environ)
    for name in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS"):
        env[name] = "1"
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    receipts = []
    evidence = {}
    start = time.monotonic()
    for mode, flags in (("normal", ["-B"]), ("optimized", ["-B", "-O"])):
        produced = scratch / ("certificate-" + mode + ".json")
        jobs = (("produce", ["--out", str(produced)]),
                ("check", ["--expected", str(root / "expected.json")]),
                ("small_models", []), ("controls", []), ("audit_stage", []))
        for name, extra in jobs:
            label = name + "-" + mode
            job_start = time.monotonic()
            try:
                process = subprocess.run([sys.executable, *flags, str(root / (name + ".py")), *extra],
                                         env=env, capture_output=True, text=True, timeout=20, check=False)
            except subprocess.TimeoutExpired as error:
                raise RuntimeError("Operational20s guard: " + label + ". This is not a mathematical exclusion.") from error
            (scratch / (label + ".stdout.json")).write_text(process.stdout)
            (scratch / (label + ".stderr.txt")).write_text(process.stderr)
            if process.returncode != 0:
                raise RuntimeError(label + " failed: " + process.stderr)
            result = json.loads(process.stdout)
            receipts.append({"label": label, "exit_code": process.returncode,
                             "wall_seconds": round(time.monotonic() - job_start, 6),
                             "max_RSS_KiB": result["max_RSS_KiB"]})
            if name == "produce":
                if produced.read_bytes() != (root / "certificate.json").read_bytes():
                    raise RuntimeError("producer changed the frozen certificate")
            else:
                if name in evidence and evidence[name] != result["evidence"]:
                    raise RuntimeError("normal/optimized evidence differs for " + name)
                evidence[name] = result["evidence"]
    frozen_controls = json.loads((root / "expected-controls.json").read_text())
    if {name: value for name, value in evidence.items() if name != "check"} != frozen_controls:
        raise RuntimeError("frozen small-model/control/stage evidence differs")
    result = {"agent": "six-covering-3", "role": "researcher", "status": "ALL SOURCE CHECKS PASSED",
              "jobs": receipts, "evidence": evidence, "normal_optimized_equal": True,
              "certificate_sha256": sha256((root / "certificate.json").read_bytes()).hexdigest(),
              "total_seconds": round(time.monotonic() - start, 6),
              "resource_scope": "oneCPU/2GiB unchanged; one sequential child; numerical threads1;20s child guard"}
    (scratch / "verification.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({k: v for k, v in result.items() if k != "evidence"}, sort_keys=True))


if __name__ == "__main__":
    main()
