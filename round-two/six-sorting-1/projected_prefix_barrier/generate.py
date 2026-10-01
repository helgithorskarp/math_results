#!/usr/bin/env python3
"""Reconstruct the pinned projection family, then run the incremental C++ screen."""
import argparse
import hashlib
import importlib.util
import itertools
import json
from pathlib import Path
import subprocess
import time

ROOT = Path(__file__).resolve().parent
SEED_SHA = "8eaf44524362295a699d0a9aacb13368f0ec9d5a8c7ce4d14bbecf2ad6bf4cd9"
PARENT_SHA = "f6e8d9c7405699af79fea64e2259f8da1779cb9536899c19e9c61ecd24cb8ae4"
GENERATOR_SHA = "1e674f8a017cca408aa95cadfc31f644b40af64dce0d913f122ef08c66292faa"


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--parent-dir", type=Path, default=ROOT.parent / "projection_deletion_barrier")
    p.add_argument("--work-dir", type=Path, default=ROOT.parents[2] / "scratch" / "projected-prefix-barrier")
    args = p.parse_args()
    for name, pin in [("parents.json", PARENT_SHA), ("generate.py", GENERATOR_SHA)]:
        if hashlib.sha256((args.parent_dir / name).read_bytes()).hexdigest() != pin:
            raise ValueError("dependency bytes differ: "+name)
    spec = importlib.util.spec_from_file_location("projection_producer", args.parent_dir / "generate.py")
    old = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(old)
    parents = json.loads((args.parent_dir / "parents.json").read_text())["parents"]
    unique = set()
    for parent in parents:
        n, gates = parent["n"], parent["gates"]
        for deleted in itertools.combinations(range(n), n-13):
            for signs in itertools.product((0, 1), repeat=n-13):
                low = {i for i, s in zip(deleted, signs) if not s}
                word = old.projection(gates, n, low, set(deleted)-low)
                if len(word) <= 46:
                    unique.add(word)
    seeds = sorted(unique)
    text = str(len(seeds))+"\n"+"".join("13 "+str(len(gates))+"\n"+
        "".join(f"{a} {b}\n" for a, b in gates) for gates in seeds)
    if hashlib.sha256(text.encode()).hexdigest() != SEED_SHA:
        raise ValueError("canonical seed family differs")
    args.work_dir.mkdir(parents=True, exist_ok=True)
    for index in (396, 591):
        prefix = seeds[index][:24]
        (args.work_dir / f"survivor-{index}-cut24.txt").write_text("13 24\n"+
            "".join(f"{a} {b}\n" for a, b in prefix))
    seed_file = args.work_dir / "seeds.txt"
    seed_file.write_text(text)
    binary = args.work_dir / "screen_anchors"
    subprocess.run(["g++", "-std=c++20", "-O3", "-Wall", "-Wextra", "-Wpedantic", "-Wconversion",
                    "-Wshadow", str(ROOT / "screen_anchors.cpp"), "-o", str(binary)], check=True)
    output = args.work_dir / "raw-screen.json"
    start = time.monotonic()
    subprocess.run([str(binary), str(seed_file), str(output)], check=True)
    doc = json.loads(output.read_text())
    doc.pop("seconds")
    doc["seed_sha256"] = SEED_SHA
    canonical = json.dumps(doc, sort_keys=True, separators=(",", ":"))+"\n"
    (args.work_dir / "certificate.json").write_text(canonical)
    if (ROOT / "certificate.json").exists() and canonical != (ROOT / "certificate.json").read_text():
        raise ValueError("certificate differs")
    print("screen_seconds", round(time.monotonic()-start, 3), "passing_counts", doc["passing_counts"])


if __name__ == "__main__":
    main()
