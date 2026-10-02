"""Regenerate the complete independent record, with fixed serial guards."""
import argparse
import hashlib
import json
import os
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def canonical(value):
    return (json.dumps(value, sort_keys=True, separators=(",", ":")) + "\n").encode()


def run(command, work, label):
    env = os.environ.copy()
    for name in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS",
                 "NUMEXPR_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "BLIS_NUM_THREADS"):
        env[name] = "1"
    started = time.monotonic()
    with (work / (label + ".stdout")).open("wb") as out, (work / (label + ".stderr")).open("wb") as err:
        result = subprocess.run(command, env=env, stdout=out, stderr=err, timeout=60)
    (work / (label + ".receipt.json")).write_bytes(canonical({"command": command,
        "returncode": result.returncode, "guard_seconds": 60, "threads": 1,
        "elapsed_seconds": time.monotonic() - started}))
    if result.returncode:
        raise RuntimeError("stage failed: " + label)


def aggregate(work):
    return {"inventory": json.loads((work / "inventory.json").read_bytes()),
            "completion": json.loads((work / "completion.stdout").read_bytes()),
            "structure": json.loads((work / "structure.json").read_bytes()),
            "complete_k_word_stream_sha256": hashlib.sha256((work / "native.kwords.txt").read_bytes()).hexdigest(),
            "complete_valid_byte_stream_sha256": hashlib.sha256((work / "native.valid.bin").read_bytes()).hexdigest()}


def check(record, fixture):
    if canonical(record) != canonical(fixture):
        raise ValueError("entire mathematical record differs")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--work", type=Path, required=True)
    parser.add_argument("--optimized", action="store_true")
    parser.add_argument("--sanitize", action="store_true")
    args = parser.parse_args()
    work = args.work.resolve()
    if work == ROOT or ROOT in work.parents:
        raise ValueError("generated corpora belong in a separate scratch directory")
    work.mkdir(parents=True, exist_ok=False)
    python = [sys.executable] + (["-O"] if args.optimized else [])
    run(python + [str(ROOT / "inventory.py"), "--work", str(work)], work, "inventory")
    run(python + [str(ROOT / "structure.py"), "--output", str(work / "structure.json")], work, "structure")
    flags = ["-std=c++17", "-Wall", "-Wextra", "-Werror"]
    flags += ["-O1", "-g", "-fsanitize=address,undefined", "-fno-omit-frame-pointer"] if args.sanitize else ["-O2"]
    run(["g++"] + flags + [str(ROOT / "complete.cpp"), "-o", str(work / "complete")], work, "compile")
    run([str(work / "complete"), str(work / "frames.txt"), str(ROOT / "primary21.rows"), str(work / "native")], work, "completion")
    record = aggregate(work)
    raw = canonical(record)
    (work / "RESULTS.json").write_bytes(raw)
    check(record, json.loads((ROOT / "RESULTS.json").read_bytes()))
    print(json.dumps({"status": "REPRODUCTION_PASS", "sha256": hashlib.sha256(raw).hexdigest(), "bytes": len(raw)}, sort_keys=True))


if __name__ == "__main__":
    main()
