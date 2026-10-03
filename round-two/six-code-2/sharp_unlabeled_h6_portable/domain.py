"""Entire projected boundary domain from independently audited actual maps."""
import argparse
from collections import Counter
import hashlib
from itertools import combinations
import json
from pathlib import Path
import resource
import time
from operations import check_operations


def need(ok, message):
    if not ok:
        raise ValueError(message)


def encoded(value):
    return (json.dumps(value, sort_keys=True, separators=(",", ":")) + "\n").encode()


def read(path):
    return json.loads(path.read_bytes())


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--case-root", type=Path, action="append", required=True)
    parser.add_argument("--work", type=Path, required=True)
    args = parser.parse_args()
    need(len(args.case_root) == 4 and not args.work.exists(), "four declared cases and fresh domain output")
    args.work.mkdir(parents=True)
    begin = time.monotonic()
    domains = []
    for root in args.case_root:
        check_operations()
        audit = read(root / "point-cover-audit/EXACT_RESULT.json")
        need(audit["status"] == "COMPLETE_PHYSICAL_ACTUAL_IMAGES_OF_ONE_LITERAL_H6_PAIR" and
             audit["cover_sha256"] == digest(root / "cover/COVER.json") and
             audit["positive69_witness_sha256"] == digest(root / "graph/WITNESS69.json"), "whole physical point-audit bindings")
        cover = read(root / "cover/COVER.json")
        rows = cover["targets"]
        need(all(len(row) == 4 and all(type(v) is int for v in row) for row in rows), "complete target row format")
        # The last field identifies a representative map. It is not a boundary coordinate.
        domain = {tuple(row[:3]) for row in rows}
        need(len(domain) == len(rows) == audit["actual_targets"] and
             hashlib.sha256(encoded(sorted(domain))).hexdigest() == audit["actual_target_domain_sha256"], "entire physical projected domain")
        domains.append(domain)
    intersections = [len(a & b) for a, b in combinations(domains, 2)]
    need(intersections == [0] * 6, "four actual boundary families disjoint")
    union = set().union(*domains)
    counts = Counter(q for q, e1, e2 in union)
    need(len(union) == 40800 and len(counts) == 2040 and set(counts.values()) == {20}, "entire declared union and per-Q coverage")
    full = encoded(sorted(union))
    (args.work / "FULL_DOMAIN.json").write_bytes(full)
    result = {"family_sizes": [len(d) for d in domains],
              "family_domain_sha256": [hashlib.sha256(encoded(sorted(d))).hexdigest() for d in domains],
              "pairwise_intersections": intersections, "union_targets": len(union), "distinct_Q_images": len(counts),
              "combined_target_domain_sha256": hashlib.sha256(full).hexdigest(), "combined_domain_bytes": len(full), "pairs_per_Q": 20}
    check_operations()
    need(time.monotonic() - begin < 60 and sum(map(len, domains)) <= 2000000, "INCOMPLETE original domain guards")
    (args.work / "EXACT_RESULT.json").write_bytes(encoded(result))
    (args.work / "EXECUTION.json").write_bytes(encoded({"seconds": time.monotonic() - begin, "peak_RSS_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss, "original_math_seconds": 60, "original_math_states": 2000000}))
    print(json.dumps({"status": "COMPLETE_PROJECTED_DOMAIN", "union_targets": len(union)}, sort_keys=True), flush=True)


if __name__ == "__main__":
    main()
