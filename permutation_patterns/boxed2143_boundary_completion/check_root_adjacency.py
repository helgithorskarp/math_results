"""Author replay of the uniform adjacent-root132 obstruction, no growth claim."""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path
import platform
import resource
import time

from boundary_completion import BoundaryCompletion
from check_boundary_completion import brute_132
from completion_templates import interleave, standardize
from definition_checker import first_occurrence


def run() -> dict[str, object]:
    start = time.monotonic()
    digest = hashlib.sha256()
    p8 = (2, 1, 4, 3, 7, 8, 5, 6)
    root_counts = {"before": 0, "after": 0}
    for rho in brute_132(7):
        gap = rho.index(7)
        if gap not in (4, 5):
            continue
        word = interleave(p8, rho)
        occurrence = first_occurrence(word)
        if occurrence is None:
            raise RuntimeError(f"Adjacent-root obstruction fails: {rho}")
        root_counts["before" if gap == 4 else "after"] += 1
        digest.update((json.dumps([rho, occurrence], separators=(",", ":")) + "\n").encode())

    left_cases = after_cases = 0
    for m in range(8, 21):
        old = (3, 1, 7, 5, 2 * m - 3)
        evens = tuple(2 * x for x in range(m - 5, m - 1))
        for scaffold in itertools.permutations(evens):
            word = tuple(x for pair in zip(old[:-1], scaffold) for x in pair) + old[-1:]
            occurrence = first_occurrence(standardize(word))
            if occurrence is None:
                raise RuntimeError(f"Before-case band obstruction fails: {m}, {scaffold}")
            left_cases += 1
            digest.update((json.dumps([m, scaffold, occurrence], separators=(",", ":")) + "\n").encode())
        for y in range(2, 2 * m - 3, 2):
            word = (2 * m - 3, y, 2 * m - 1, 2 * m - 2)
            if first_occurrence(standardize(word)) != (0, 1, 2, 3):
                raise RuntimeError("After-case consecutive pattern failed")
            after_cases += 1

    full = BoundaryCompletion(p8).solve()
    expected = (3, 2, 1, 4, 7, 6, 5, 8, 13, 10, 15, 12, 9, 14, 11)
    if tuple(full["output"]) != expected or first_occurrence(expected) is not None:
        raise RuntimeError("Named unrestricted-root completion failed")
    if tuple((x + 1) // 2 for x in expected[::2]) != p8:
        raise RuntimeError("Named completion did not recover input")
    root = Path(__file__).parent
    return {"decision_message_id": 410, "full_target_solved": False,
        "claim_status": "finite replay supporting written all-m>=8 root-choice obstruction",
        "all_132_scaffolds_at_m8": len(brute_132(7)),
        "adjacent_root_candidates_checked_at_m8": root_counts,
        "before_arbitrary_left_orderings_m8_20": left_cases,
        "after_possible_even_labels_m8_20": after_cases,
        "ordered_witness_stream_sha256": digest.hexdigest(),
        "full_input_completion": expected, "rho": tuple(x // 2 for x in expected[1::2]),
        "proof_sha256": hashlib.sha256((root / "ROOT_ADJACENCY_OBSTRUCTION.md").read_bytes()).hexdigest(),
        "source_sha256": hashlib.sha256((root / "check_root_adjacency.py").read_bytes()).hexdigest(),
        "python": platform.python_version(), "elapsed_seconds": time.monotonic() - start,
        "peak_rss_kib_linux": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}


if __name__ == "__main__":
    print(json.dumps(run(), indent=2))
