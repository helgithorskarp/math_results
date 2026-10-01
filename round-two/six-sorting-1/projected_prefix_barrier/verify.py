#!/usr/bin/env python3
"""Independent projection reconstruction and Python anchor certificate replay."""
import argparse
import hashlib
import importlib.util
import itertools
import json
from pathlib import Path
import resource
import time

ROOT = Path(__file__).resolve().parent
PINS = {
    "parents.json": "f6e8d9c7405699af79fea64e2259f8da1779cb9536899c19e9c61ecd24cb8ae4",
    "verify.py": "79d5f8dc26b8a9be87a2b04a00a960c5bce94a1fc05d9426e8ba476be5b0701a",
    "profile.py": "dca9c8d6331c3fc548c514ca8f5f1cd170f4a0bb39a3c05250876247d0362719",
    "anchors.py": "0b95573e7e3c446d0b7ca5352f6b5f4b8d92b91d6f3c72e7b4f783cd99d89902",
}
SEED_SHA = "8eaf44524362295a699d0a9aacb13368f0ec9d5a8c7ce4d14bbecf2ad6bf4cd9"


def pinned(path):
    if hashlib.sha256(path.read_bytes()).hexdigest() != PINS[path.name]:
        raise ValueError("dependency bytes differ: "+str(path))


def module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    obj = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(obj)
    return obj


def seed_text(seeds):
    return str(len(seeds))+"\n"+"".join("13 "+str(len(gates))+"\n"+
        "".join(f"{a} {b}\n" for a, b in gates) for gates in seeds)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--parent-dir", type=Path, default=ROOT.parent / "projection_deletion_barrier")
    p.add_argument("--profile-dir", type=Path, default=ROOT.parents[1] / "six-sorting-2" / "semantic-pruning")
    p.add_argument("--certificate", type=Path, default=ROOT / "certificate.json")
    p.add_argument("--output", type=Path, default=ROOT.parents[2] / "scratch" / "prefix-barrier-check.json")
    args = p.parse_args()
    for path in [args.parent_dir / "parents.json", args.parent_dir / "verify.py",
                 args.profile_dir / "profile.py", args.profile_dir / "anchors.py"]:
        pinned(path)
    projection = module("independent_projection", args.parent_dir / "verify.py")
    profile = module("independent_semantic_profile", args.profile_dir / "profile.py")
    anchors = module("independent_semantic_anchors", args.profile_dir / "anchors.py")
    parents = json.loads((args.parent_dir / "parents.json").read_text())["parents"]
    seeds = set()
    for parent in parents:
        n, gates = parent["n"], parent["gates"]
        for survivors in itertools.combinations(range(n), 13):
            for choices in itertools.product((False, True), repeat=n-13):
                word = projection.normalized_projection(gates, n, list(survivors), choices)
                if len(word) <= 46:
                    seeds.add(word)
    seeds = sorted(seeds)
    if hashlib.sha256(seed_text(seeds).encode()).hexdigest() != SEED_SHA:
        raise ValueError("canonical seed family differs")
    doc = json.loads(args.certificate.read_text())
    if doc["n"] != 13 or doc["budget"] != 44 or doc["seed_sha256"] != SEED_SHA:
        raise ValueError("certificate scope differs")
    cuts = doc["cuts"]
    if cuts != [8, 12, 16, 20, 24] or len(doc["records"]) != len(seeds):
        raise ValueError("certificate coverage differs")
    counts = [0]*len(cuts)
    start = time.monotonic()
    for i, (gates, row) in enumerate(zip(seeds, doc["records"])):
        if row["seed_index"] != i:
            raise ValueError("seed record index differs")
        units = []
        for j, cut in enumerate(cuts):
            data = profile.analyze(13, gates[:cut])
            actual = anchors.both(13, data)
            pair = [actual[side]["normalized_mass"] for side in ("low", "high")]
            if any(actual[side]["base"] != 35 for side in ("low", "high")):
                raise ValueError("normalization base differs")
            units.append(pair)
            counts[j] += max(pair) <= 512
        if units != row["units"]:
            raise ValueError("anchor units differ at seed "+str(i))
        if (i+1) % 50 == 0:
            print("checked", i+1, "seconds", round(time.monotonic()-start, 3), flush=True)
    if counts != doc["passing_counts"]:
        raise ValueError("passing counts differ")
    if len({g[:24] for g in seeds}) != len(seeds):
        raise ValueError("24-gate prefixes are not distinct")
    survivors = [r["seed_index"] for r in doc["records"] if max(r["units"][-1]) <= 512]
    if survivors != [396, 591] or counts != [869, 869, 869, 356, 2]:
        raise ValueError("claimed reduction differs")
    result = {"status": "ALL_PREFIX_BARRIER_CHECKS_PASSED", "agent": "six-sorting-1",
              "role": "researcher", "seeds": len(seeds), "checked_prefixes": len(seeds)*len(cuts),
              "passing_counts": counts, "survivor_indices": survivors,
              "seconds": time.monotonic()-start, "peak_rss_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
              "certificate_sha256": hashlib.sha256(args.certificate.read_bytes()).hexdigest()}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, sort_keys=True)+"\n")
    print(json.dumps(result, sort_keys=True), flush=True)


if __name__ == "__main__":
    main()
