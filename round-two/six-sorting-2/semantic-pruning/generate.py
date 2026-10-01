"""Generate or reproduce the compact exact semantic-pruning certificate."""

import argparse
import hashlib
import json
from pathlib import Path
import time

from profile import analyze, lower_bound, require, truth_columns

ROOT = Path(__file__).resolve().parent


def activity(n, gates):
    values = list(truth_columns(n))
    witnesses = []
    for a, b in gates:
        bad = values[a] & ~values[b]
        require(bad != 0, "fixture contains a globally redundant gate")
        witnesses.append((bad & -bad).bit_length() - 1)
        values[a], values[b] = values[a] & values[b], values[a] | values[b]
    return witnesses


def build(fixture):
    cases = {}
    for name in ("prefix", "incumbent", "small_sorter", "small_duplicate"):
        n = fixture["n"] if name in ("prefix", "incumbent") else 4
        gates = fixture[name]
        families = analyze(n, gates)
        cases[name] = {"n": n, "size": len(gates), "families": families,
                       "lower_bound": max(lower_bound(n, x) for x in families.values())}
    mixed = cases["prefix"]["families"]["mixed_pair"]
    require(mixed["summary"]["ordinary_mass"] == 388, "ordinary witness mass")
    require(mixed["summary"]["semantic_mass"] == 524, "semantic witness mass")
    require(cases["prefix"]["lower_bound"] == 45, "witness lower bound")
    require(sum(r[5] for r in mixed["records"]) == 30, "redundancy count")
    for case in ("incumbent", "small_sorter", "small_duplicate"):
        require(cases[case]["lower_bound"] <= cases[case]["size"],
                "positive control violates necessary bound")
    return {"schema": "sorting-extreme-semantic-pruning-v1",
            "agent": "six-sorting-2", "role": "researcher",
            "record_fields": ["input_low_mask", "input_high_mask", "output_low_mask",
                              "output_high_mask", "D", "R", "redundant_gate_mask"],
            "cases": cases, "prefix_activity_witnesses": activity(13, fixture["prefix"])}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    start = time.monotonic()
    fixture = json.loads((ROOT / "fixture.json").read_text())
    certificate = build(fixture)
    encoded = (json.dumps(certificate, separators=(",", ":"), sort_keys=True) + "\n").encode()
    path = ROOT / "certificate.json"
    if args.write:
        path.write_bytes(encoded)
    else:
        require(path.read_bytes() == encoded, "certificate is not reproduced byte for byte")
    print(json.dumps({"status": "GENERATOR_CHECKS_PASSED",
                      "certificate_sha256": hashlib.sha256(encoded).hexdigest(),
                      "ordinary_mixed_mass": 388, "semantic_mixed_mass": 524,
                      "full_sorter_size_lower_bound": 45,
                      "seconds": round(time.monotonic() - start, 3)}, sort_keys=True))


if __name__ == "__main__":
    main()
