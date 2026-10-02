"""Produce a compact divisibility certificate, not a search transcript."""

import argparse
from collections import Counter
import json
from pathlib import Path
import resource
import time

from model import D, PREFIX, BASE, constraints, frontier, implies


def produce():
    original = constraints()
    reduced = frontier()
    return {"schema": "covering-cardinality-cores-v1",
            "agent": "six-covering-3", "role": "researcher",
            "D": D, "prefix": PREFIX, "base_moduli": BASE,
            "frontier": reduced,
            "implications": [[sum(1 << D.index(d) for d in row["B"]),
                              next(i for i, f in enumerate(reduced)
                                   if implies(f, row))]
                             for row in original],
            "original_predicates": len(original),
            "distinct_pair_families": len({row["pairs"] for row in original}),
            "frontier_predicates": len(reduced),
            "required_counts": dict(sorted(Counter(r["required"] for r in reduced).items())),
            "frontier_full_phase_pairs_per_fiber": sum(d * e for r in reduced for d, e in r["pairs"]),
            "scope": "Exact reduction of necessary local support predicates only; no tail or root feasibility assertion."}


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()
    start = time.monotonic()
    args.out.write_text(json.dumps(produce(), separators=(",", ":"), sort_keys=True) + "\n")
    print(json.dumps({"seconds": round(time.monotonic() - start, 6),
                      "max_RSS_KiB": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}))
