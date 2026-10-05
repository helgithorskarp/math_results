"""Falsify a specific rank-choice rule; successful finite tests are not proofs.

Hypothesis H1: in each fixed Cartesian-tree-pair poset, every boxed-2143
avoiding rank assignment chooses the leftmost or rightmost currently available
position when assigning successive values. A theorem H1 would give <=2^n
avoiding assignments per fiber. This script retains the first counterexample.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import platform
import time
from pathlib import Path

from cartesian_fibers import load_checker, pair_key, predecessor_masks, require


def first_internal_choice(p):
    pair = pair_key(p)
    pred = predecessor_masks(pair)
    chosen = 0
    for rank in range(1, len(p) + 1):
        available = [i for i in range(len(p)) if not chosen & (1 << i) and not pred[i] & ~chosen]
        position = p.index(rank)
        require(position in available, "Actual permutation violates its heap constraints")
        if position not in (available[0], available[-1]):
            return {"rank": rank, "position_zero_based": position,
                    "available_positions_zero_based": available,
                    "chosen_mask": chosen, "predecessor_masks": pred,
                    "min_parents": pair[0], "max_parents": pair[1]}
        chosen |= 1 << position
    return None


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-n", type=int, default=8)
    parser.add_argument("--checker-path", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if not 0 <= args.max_n <= 9:
        raise ValueError("Require 0<=max-n<=9")
    checker = load_checker(args.checker_path)
    result = {"decision_message_id": 410, "hypothesis": "H1 extreme available rank choice",
              "claim_status": "finite falsification probe, not a growth theorem",
              "python": platform.python_version(), "checker_path": str(args.checker_path.resolve()),
              "checker_sha256": hashlib.sha256(args.checker_path.read_bytes()).hexdigest(),
              "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              "fully_exhausted_lengths": [], "counterexample": None}
    started = time.monotonic()
    for n in range(args.max_n + 1):
        total = avoiding = 0
        for p in itertools.permutations(range(1, n + 1)):
            total += 1
            if not checker.avoids(p):
                continue
            avoiding += 1
            violation = first_internal_choice(p)
            if violation is not None:
                result["counterexample"] = {"permutation": p, "complete_occurrences": list(checker.occurrences(p)),
                    "violation": violation, "permutations_examined_at_length": total,
                    "avoiders_examined_at_length": avoiding}
                break
        if result["counterexample"] is not None:
            break
        result["fully_exhausted_lengths"].append({"n": n, "permutations": total, "avoiders": avoiding})
        print(json.dumps(result["fully_exhausted_lengths"][-1]), flush=True)
    result["elapsed_seconds"] = time.monotonic() - started
    args.output.parent.mkdir(parents=True, exist_ok=True)
    temporary = args.output.with_suffix(args.output.suffix+".tmp")
    temporary.write_text(json.dumps(result, indent=2)+"\n")
    temporary.replace(args.output)
    print(json.dumps({"counterexample": result["counterexample"], "elapsed_seconds": result["elapsed_seconds"]}))


if __name__ == "__main__":
    main()
