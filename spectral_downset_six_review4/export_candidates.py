#!/usr/bin/env python3
"""Regenerate untrusted candidate partitions using the published source.

This bridge imports the researcher's generator, which is NOT a trusted part
of the reviewer audit. The independent checker proves domain coverage and
validates every positive partition. Keep the generated JSONL in scratch.
"""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
import time

HERE = Path(__file__).resolve().parent
TARGET = HERE.parent / "spectral_downset_six_exact"
PINS = {
    "census.py": "24bf915c7a2219a610a69d03ada76a9f78254f5edde95d09e4430629d17af91f",
    "verify.py": "3eff145c91e2b23a6cc9b82d2cf98339f8c336efa3fa655268246d19ab97c458",
    "RESULTS.json": "53dca0d1175fccf9aebcac4f2434d708fc1446e93f35647c123df34d6374405c",
}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--target", type=Path, default=TARGET)
    p.add_argument("--out", type=Path, required=True)
    args = p.parse_args()
    for name, digest in PINS.items():
        if hashlib.sha256((args.target / name).read_bytes()).hexdigest() != digest:
            raise ValueError("source identity differs: " + name)
    sys.path.insert(0, str(args.target.resolve()))
    spec = importlib.util.spec_from_file_location("candidate_census", args.target / "census.py")
    source = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(source)
    start = time.monotonic()
    classes, section_pairs, labelled = source.six_classes()
    expected = json.loads((args.target / "RESULTS.json").read_text())
    class_hash = hashlib.sha256()
    witness_hash = hashlib.sha256()
    tmp = args.out.with_suffix(args.out.suffix + ".incomplete")
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with tmp.open("w") as out:
        for family, orbit in classes:
            class_hash.update(f"{family}:{orbit}\n".encode())
            if family == source.EXCEPTION:
                bins = None
            else:
                bins, _ = source.partition(family)
                if bins is None:
                    raise RuntimeError("INCOMPLETE: missing positive partition")
                witness_hash.update((json.dumps([family, bins], separators=(",", ":"))
                                     + "\n").encode())
            out.write(json.dumps({"family": family, "orbit": orbit, "bins": bins},
                                 separators=(",", ":")) + "\n")
    if (class_hash.hexdigest() != expected["census_sha256"]
            or witness_hash.hexdigest() != expected["partition_witness_stream_sha256"]
            or len(classes) != 16353 or labelled != 7828354
            or section_pairs != 82486):
        raise ValueError("source stream differs from committed finite claim")
    tmp.replace(args.out)
    print(json.dumps({"candidate_classes": len(classes), "labeled_count": labelled,
                      "section_pair_orbits": section_pairs,
                      "census_sha256": class_hash.hexdigest(),
                      "partition_witness_stream_sha256": witness_hash.hexdigest(),
                      "candidate_bytes": args.out.stat().st_size,
                      "seconds": time.monotonic() - start}, sort_keys=True))


if __name__ == "__main__":
    main()
