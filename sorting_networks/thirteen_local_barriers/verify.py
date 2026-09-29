#!/usr/bin/env python3
"""Check the public fixture and both local barriers, with one build at a time."""
from __future__ import annotations

import argparse
import hashlib
import os
from pathlib import Path
import subprocess
import time

BASE = Path(__file__).resolve().parent
HASHES = {
    "incumbent.txt": "f30f374c8f12472e7bbabdb23dfe980635b5640affbaf2b06c3bc2dbbbc22e5d",
    "witnesses.txt": "41335672c1ed9251ba687f9b9d44435b4de005cb0ef31429c20bacdb36fa3212",
}


def run(args: list[str], env: dict[str, str]) -> str:
    result = subprocess.run(args, check=True, text=True, capture_output=True, env=env)
    if result.stderr:
        print(result.stderr, end="", flush=True)
    return result.stdout


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--work-dir", type=Path, default=BASE / "scratch")
    parser.add_argument("--regenerate", action="store_true")
    args = parser.parse_args()
    work = args.work_dir.resolve()
    work.mkdir(parents=True, exist_ok=True)
    env = os.environ.copy()
    for key in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "BLIS_NUM_THREADS", "NUMEXPR_NUM_THREADS"):
        env[key] = "1"
    for name, expected in HASHES.items():
        actual = hashlib.sha256((BASE / name).read_bytes()).hexdigest()
        if actual != expected:
            raise ValueError(f"{name}: certificate hash mismatch: {actual}")

    fields = list(map(int, (BASE / "incumbent.txt").read_text().split()))
    n, m = fields[:2]
    if (n, m, len(fields)) != (13, 45, 92):
        raise ValueError("unexpected incumbent dimensions")
    gates = list(zip(fields[2::2], fields[3::2]))
    if any(not 0 <= a < b < n for a, b in gates):
        raise ValueError("malformed incumbent")
    # Direct Boolean-list simulation, independent of both packed C++ checkers.
    for x in range(1 << n):
        values = [(x >> i) & 1 for i in range(n)]
        for a, b in gates:
            if values[a] > values[b]:
                values[a], values[b] = values[b], values[a]
        if values != sorted(values):
            raise ValueError(f"incumbent fails Boolean input {x}")
    print("incumbent: all 8192 Boolean inputs pass", flush=True)

    programs = ["check_circuit", "check_windows"]
    if args.regenerate:
        programs.append("generate")
    for program in programs:
        run(["g++", "-std=c++20", "-O3", "-Wall", "-Wextra", "-Wpedantic", "-Wconversion", "-Wshadow",
             str(BASE / (program + ".cpp")), "-o", str(work / program)], env)

    start = time.monotonic()
    result = run([str(work / "check_circuit"), str(BASE / "incumbent.txt"), str(BASE / "witnesses.txt")], env)
    expected = "certified=1 pairs=990 parameters=4458189 acyclic=2290014 cyclic=2168175 witnesses=174\n"
    if result != expected:
        raise ValueError(f"unexpected circuit result: {result}")
    print(result, end="", flush=True)
    print(f"circuit checker elapsed: {time.monotonic() - start:.3f}s", flush=True)

    start = time.monotonic()
    result = run([str(work / "check_windows"), str(BASE / "incumbent.txt"), str(BASE / "witnesses.txt"),
                  "6", "5", "0", "39"], env)
    if not result.endswith("complete=1 windows=40 strings=115486974720\n"):
        raise ValueError(f"unexpected window result: {result}")
    print(result.splitlines()[-1], flush=True)
    print(f"window checker elapsed: {time.monotonic() - start:.3f}s", flush=True)

    if args.regenerate:
        generated = work / "regenerated-witnesses.txt"
        result = run([str(work / "generate"), str(BASE / "incumbent.txt"), str(generated), str(work / "generated-summary.json")], env)
        if generated.read_bytes() != (BASE / "witnesses.txt").read_bytes():
            raise ValueError("regenerated certificate differs entry by entry")
        print(result, end="", flush=True)
        print("regenerated certificate: byte-for-byte match", flush=True)
    print("both local barriers verified; no global size lower bound claimed", flush=True)


if __name__ == "__main__":
    main()
