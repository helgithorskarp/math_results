"""Offline cold replay with fixed serial limits and complete compact comparisons."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time
from independent import encoded, require
from summarize import summary, provenance
from check_witnesses import verify


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--work", type=Path, required=True)
    args = p.parse_args()
    root = Path(__file__).parent.resolve()
    args.work.mkdir(parents=True, exist_ok=True)
    require(not any(args.work.iterdir()), "use initially empty work directory")
    flags = [sys.executable, "-B"] + (["-O"] if sys.flags.optimize else [])
    env = {**os.environ, **{k: "1" for k in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS",
                                            "NUMEXPR_NUM_THREADS", "BLIS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS")}}
    receipts = []
    def run(name, limit, command):
        start = time.monotonic()
        # A timeout is an exception, with no mathematical absence conclusion.
        r = subprocess.run(flags + command, env=env, capture_output=True, timeout=limit)
        (args.work / (name + ".out")).write_bytes(r.stdout)
        (args.work / (name + ".err")).write_bytes(r.stderr)
        require(r.returncode == 0, name + " incomplete/failed: " + r.stderr.decode())
        receipts.append({"name": name, "seconds": time.monotonic() - start,
                         "fixed_guard_seconds": limit, "returncode": r.returncode})
    record_path = args.work / "whole.json"
    run("complete", 180, [str(root / "independent.py"), "--core", str(root / "CORE.json"), "--out", str(record_path)])
    run("controls", 60, [str(root / "controls.py"), str(record_path), str(args.work / "controls.json")])
    raw = record_path.read_bytes()
    record = json.loads(raw)
    result, exceptions, sharp, tails = summary(record, raw)
    result["identification"] = provenance(record["core"], tails, json.loads((root / "IDENTIFICATION.json").read_bytes()), (root / "acl69.txt").read_bytes())
    for name, value in (("expected.json", result), ("EXACT55_EXCEPTIONS.json", exceptions),
                        ("SHARP_TAILS.json", sharp), ("FULL_CORE_TAILS.json", tails)):
        require(encoded(value) == (root / name).read_bytes(), "complete compact evidence differs: " + name)
    require((args.work / "controls.json").read_bytes() == (root / "controls.json").read_bytes(), "whole control record differs")
    witness_result = verify(record["core"], tails, exceptions, sharp)
    checked = {"actual_agent": "six-reviewer-4", "role": "independent mathematical reviewer",
               "complete": True, "python_version": sys.version.split()[0],
               "whole_record_sha256": hashlib.sha256(raw).hexdigest(),
               "entire_compact_readout_agrees": True, "witnesses": witness_result, "receipts": receipts}
    (args.work / "validation.json").write_bytes(encoded(checked))
    print(json.dumps(checked, sort_keys=True))


if __name__ == "__main__":
    main()
