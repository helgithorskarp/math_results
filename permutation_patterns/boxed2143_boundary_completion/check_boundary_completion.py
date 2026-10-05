"""Definition-level finite verification of the boundary completion algorithm.

Compare every reachable subproblem's exact signature/canonical-witness map
against factorial scaffold enumeration with a direct boxed-occurrence scan.
"""

from __future__ import annotations

import argparse
import functools
import hashlib
import itertools
import json
from pathlib import Path
import platform
import resource
import time

from boundary_completion import BoundaryCompletion
from completion_templates import standardize
from definition_checker import avoids


@functools.lru_cache(maxsize=None)
def brute_132(r: int) -> tuple[tuple[int, ...], ...]:
    return tuple(p for p in itertools.permutations(range(1, r + 1))
                 if not any(b > c > a for a, b, c in itertools.combinations(p, 3)))


def brute_states(solver: BoundaryCompletion, key: tuple[int, int, int]) -> dict:
    first, end, low = key
    size = end - first
    result = {}
    for rho in brute_132(size - 1):
        word = []
        for j in range(size):
            word.append(2 * solver.p[first + j] - 1)
            if j < size - 1:
                word.append(2 * (low + rho[j] - 1))
        word = tuple(word)
        if avoids(standardize(word)):
            signature = solver.signature(word)
            previous = result.get(signature)
            if previous is None or word < previous:
                result[signature] = word
    return result


def no_unhit_old_rectangle(solver: BoundaryCompletion, key: tuple[int, int, int]) -> bool:
    first, end, low = key
    high = low + end - first - 2
    old = tuple(2 * x - 1 for x in solver.p[first:end])
    lower = tuple(x for x in old if x < 2 * low)
    upper = tuple(x for x in old if x > 2 * high)
    return avoids(standardize(lower)) and avoids(standardize(upper))


def run(max_m: int) -> dict[str, object]:
    if not 1 <= max_m <= 5:
        raise ValueError("Entry-level verification is deliberately capped at m<=5")
    start = time.monotonic()
    digest = hashlib.sha256()
    inputs = keys = 0
    rows = []
    first_insufficient_band_condition = None
    for m in range(1, max_m + 1):
        row_inputs = row_keys = 0
        largest_total_states = largest_root_states = 0
        for p in itertools.permutations(range(1, m + 1)):
            solver = BoundaryCompletion(p)
            summary = solver.solve()
            inputs += 1
            row_inputs += 1
            largest_total_states = max(largest_total_states, summary["total_state_count"])
            largest_root_states = max(largest_root_states, summary["root_state_count"])
            for key, states in sorted(solver.memo.items()):
                keys += 1
                row_keys += 1
                expected = brute_states(solver, key)
                if states != expected:
                    raise RuntimeError(f"Exact state map mismatch: {p}, {key}")
                band_condition = no_unhit_old_rectangle(solver, key)
                if states and not band_condition:
                    raise RuntimeError("Necessary old-rectangle condition failed")
                if not states and band_condition and first_insufficient_band_condition is None:
                    first_insufficient_band_condition = {"input": p, "subproblem": key}
                ordered = sorted(states.items())
                digest.update((json.dumps([p, key, ordered], separators=(",", ":")) + "\n").encode())
            if not summary["root_state_count"]:
                raise RuntimeError(f"Restricted completion existence already fails at {p}")
        rows.append({"m": m, "inputs": row_inputs, "subproblems_compared": row_keys,
                     "largest_total_states": largest_total_states,
                     "largest_root_states": largest_root_states})
    root = Path(__file__).parent
    return {"decision_message_id": 410, "full_target_solved": False,
        "claim_status": "exact finite soundness/completeness comparison; no universal existence theorem",
        "inputs": inputs, "subproblems_compared": keys, "rows": rows,
        "ordered_state_map_sha256": digest.hexdigest(),
        "first_empty_state_with_band_condition": first_insufficient_band_condition,
        "algorithm_source_sha256": hashlib.sha256((root / "boundary_completion.py").read_bytes()).hexdigest(),
        "python": platform.python_version(), "elapsed_seconds": time.monotonic() - start,
        "peak_rss_kib_linux": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-m", type=int, default=5)
    args = parser.parse_args()
    print(json.dumps(run(args.max_m), indent=2))
