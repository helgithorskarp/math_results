#!/usr/bin/env python3
"""Produce the compact exact-four concurrence certificate from F4 residues."""
from collections import defaultdict
from pathlib import Path
import argparse
import hashlib
import importlib.util
import json
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
SOURCE = ROOT / "hadwiger_nelson_complex_radix_architecture"
FOUR_SOURCE = ROOT / "hadwiger_nelson_complex_radix_four_curve_gate"
sys.path.insert(0, str(SOURCE))
sys.path.insert(0, str(HERE))
import common  # noqa: E402

spec = importlib.util.spec_from_file_location("architecture_concurrence_producer", SOURCE / "verify.py")
ARCH = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ARCH)
spec = importlib.util.spec_from_file_location("four_gate_concurrence_producer", FOUR_SOURCE / "produce.py")
FOUR = importlib.util.module_from_spec(spec)
spec.loader.exec_module(FOUR)


def file_sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def source_data():
    rows, events, factors, _, _, _, _, circle = ARCH.build()
    factor_ids = {factor: i for i, factor in enumerate(factors)}
    representatives = {}
    for row, event in zip(rows, events):
        if event:
            representatives.setdefault(factor_ids[event], row)
    common.need(len(representatives) == len(factors), "incomplete curve representatives")
    buckets = defaultdict(lambda: defaultdict(list))
    curve_k = {}
    curve_constant = {}
    for curve in range(len(factors)):
        if curve == circle:
            continue
        row = representatives[curve]
        normal, constant = FOUR.projective(
            tuple(FOUR.residue(digit) for digit in row[1:]), FOUR.residue(row[0])
        )
        buckets[normal][constant].append(curve)
        curve_k[curve] = max(i for i, digit in enumerate(row) if digit != (0, 0))
        curve_constant[curve] = constant
    buckets = {
        normal: {constant: curves for constant, curves in sections.items()}
        for normal, sections in buckets.items()
    }
    return factors, curve_k, curve_constant, buckets


def make_certificate(prime, processes):
    factors, curve_k, curve_constant, buckets = source_data()
    result = common.run_sieve(
        factors, curve_k, curve_constant, buckets, prime, processes
    )
    common.need(result["all_eligible_quartets_excluded"], "unexpected quartet survivor")
    return {
        "schema": "hn-complex-radix-four-concurrence-v1",
        "sources": {
            "architecture_certificate_sha256": file_sha256(SOURCE / "certificate.json"),
            "four_curve_interface_sha256": file_sha256(FOUR_SOURCE / "exact_four_interface.json"),
            "factor_inventory_sha256": ARCH.digest(factors),
        },
        "result": result,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--prime", type=int, default=1_000_003)
    parser.add_argument("--processes", type=int, default=1)
    args = parser.parse_args()
    certificate = make_certificate(args.prime, args.processes)
    args.out.write_text(json.dumps(certificate, sort_keys=True, separators=(",", ":")) + "\n")
    print(json.dumps({
        "output": str(args.out),
        "bytes": args.out.stat().st_size,
        "sha256": file_sha256(args.out),
        "candidate_count": len(certificate["result"]["primary"]["survivors"]),
        "final_survivor_count": len(certificate["result"]["final_survivors"]),
    }, sort_keys=True))


if __name__ == "__main__":
    main()
