"""Source-only sequential replay, normal/O, unchanged20s child guards."""

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
    env = dict(os.environ, OMP_NUM_THREADS="1", OPENBLAS_NUM_THREADS="1", MKL_NUM_THREADS="1",
               NUMEXPR_NUM_THREADS="1", PYTHONDONTWRITEBYTECODE="1")
    manifest = json.loads((root / "manifest.json").read_text())
    for row in manifest["files"]:
        p = root / row["file"]
        if p.stat().st_size != row["bytes"] or sha256(p.read_bytes()).hexdigest() != row["sha256"]:
            raise ValueError("source manifest differs: " + row["file"])
    expected = json.loads((root / "expected.json").read_text())
    evidence, receipts = {}, []
    start = time.monotonic()
    for mode, flags in (("normal", ("-B",)), ("optimized", ("-B", "-O"))):
        full, single = scratch / (mode + "-full.cnf"), scratch / (mode + "-B13.cnf")
        generated = scratch / (mode + "-certificate.json")
        jobs = (("produce", "produce", ("--out", str(generated))),
                ("check", "check", ()),
                ("encode-full", "encode", ("--out", str(full))),
                ("encode-B13", "encode", ("--out", str(single), "--only-B13")),
                ("audit", "audit", ("--full", str(full), "--B13", str(single))),
                ("controls", "controls", ("--full", str(full), "--B13", str(single))))
        for label, module, extra in jobs:
            tag = label + "-" + mode
            child_start = time.monotonic()
            try:
                p = subprocess.run([sys.executable, *flags, str(root / (module + ".py")), *extra],
                                   env=env, capture_output=True, text=True, timeout=20)
            except subprocess.TimeoutExpired as error:
                raise RuntimeError("Operational20s guard at " + tag + "; this is not a mathematical exclusion.") from error
            (scratch / (tag + ".stdout.json")).write_text(p.stdout)
            (scratch / (tag + ".stderr.txt")).write_text(p.stderr)
            if p.returncode != 0:
                raise RuntimeError(tag + ": " + p.stderr)
            result = json.loads(p.stdout)
            receipts.append({"label": tag, "exit_code": p.returncode,
                             "seconds": round(time.monotonic() - child_start, 6),
                             "max_RSS_KiB": result["max_RSS_KiB"]})
            if label == "produce":
                if generated.read_bytes() != (root / "certificate.json").read_bytes():
                    raise ValueError("frozen certificate bytes differ")
            else:
                if result["evidence"] != expected[label]:
                    raise ValueError("frozen evidence differs: " + tag)
                evidence[label] = result["evidence"]
    result = {"agent": "six-covering-3", "role": "researcher", "status": "ALL SOURCE CHECKS PASSED",
              "normal_optimized_equal": True, "certificate_sha256": sha256((root / "certificate.json").read_bytes()).hexdigest(),
              "source_manifest_entries": len(manifest["files"]),
              "jobs": receipts, "evidence": evidence, "total_seconds": round(time.monotonic() - start, 6),
              "resource_scope": "Existing1CPU/2GiB unchanged; one sequential child; numerical threads1;20s child guards."}
    (scratch / "verification.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({k: v for k, v in result.items() if k != "evidence"}, sort_keys=True))


if __name__ == "__main__":
    main()
