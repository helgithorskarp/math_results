"""Require contiguous complete extension coverage and compare all physical records."""
import argparse
import collections
import hashlib
import json
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--producer", type=Path, required=True)
    parser.add_argument("--checker", type=Path, required=True)
    parser.add_argument("--optimized", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    pieces = sorted(args.producer.glob("*.json"))
    for directory in (args.checker, args.optimized):
        if [p.name for p in pieces] != [p.name for p in sorted(directory.glob("*.json"))]:
            raise ValueError("Incomplete extension transcript file set")
    cursor = raw_trials = presentations = 0
    histogram = collections.Counter()
    physical = {}
    quad_sha = None
    for p in pieces:
        raw = p.read_bytes()
        if any(raw != (d / p.name).read_bytes() for d in (args.checker, args.optimized)):
            raise ValueError("Whole independently generated extension transcript differs")
        part = json.loads(raw)
        if part["start"] != cursor or not cursor < part["stop"] <= 64108:
            raise ValueError("Gap, repetition or overlap in physical quadruple domain")
        cursor = part["stop"]
        if quad_sha is not None and quad_sha != part["quad_records_sha256"]:
            raise ValueError("Changed quadruple corpus")
        quad_sha = part["quad_records_sha256"]
        raw_trials += part["raw_trials"]
        presentations += part["capacity_presentations"]
        histogram.update(dict(part["common_histogram"]))
        for r in part["records"]:
            a = tuple(r["A"])
            if a != tuple(sorted(set(a))) or len(a) != 5 or a[0] != 1:
                raise ValueError("Physical anchored five-row tuple")
            if len(r["C"]) not in (2, 3):
                raise ValueError("Small whole common scope")
            if sum(min(2, len(s)) for s in r["singleton"]) < 8:
                raise ValueError("Insufficient physical singleton capacity")
            if physical.setdefault(a, r) != r:
                raise ValueError("Distinct quadruple presentations disagree")
    if cursor != 64108 or raw_trials != 19488832 or sum(histogram.values()) != raw_trials:
        raise ValueError("Whole quantified extension domain missing")
    records = [r for _, r in sorted(physical.items())]
    encoded = json.dumps(records, sort_keys=True, separators=(",", ":")).encode()
    counts = collections.Counter(len(r["C"]) for r in records)
    nonzero = collections.Counter()
    physical_column_incidences = collections.Counter()
    for r in records:
        c = len(r["C"])
        if r["p10"]:
            nonzero[c, 10] += 1
        if r["p9_single"] + r["p9_double"]:
            nonzero[c, 9] += 1
        if c == 2:
            physical_column_incidences["12/12:c2,s2,k10"] += r["p10"]
        else:
            physical_column_incidences["11/13:c3,s3,k10"] += r["p10"]
            physical_column_incidences["12/12:c3,s2,k10"] += 3 * r["p10"]
            physical_column_incidences["12/12:c3,s3,k9,single"] += r["p9_single"]
            physical_column_incidences["12/12:c3,s3,k9,double"] += r["p9_double"]
    result = {"schema": "character617-small-common-complete-v1",
              "raw_trials": raw_trials, "quadruples": cursor,
              "quad_records_sha256": quad_sha,
              "extension_common_histogram": sorted(histogram.items()),
              "capacity_presentations": presentations,
              "distinct_capacity_prefixes": len(records),
              "distinct_prefix_common_histogram": sorted(counts.items()),
              "nonzero_coefficient_prefixes": [[c, k, n] for (c, k), n in sorted(nonzero.items())],
              "physical_prefix_column_incidences": dict(sorted(physical_column_incidences.items())),
              "records_sha256": hashlib.sha256(encoded).hexdigest(), "records": records}
    args.output.write_text(json.dumps(result, sort_keys=True, separators=(",", ":")) + "\n")
    print(json.dumps({k: v for k, v in result.items() if k != "records"}, sort_keys=True))


if __name__ == "__main__":
    main()
