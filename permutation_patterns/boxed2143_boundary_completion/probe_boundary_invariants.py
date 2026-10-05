"""Decisive probes of two named induction invariants, not a growth census."""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path
import platform
import resource
import time

from boundary_completion import BoundaryCompletion, StateMap
from check_boundary_completion import no_unhit_old_rectangle
from completion_templates import standardize
from definition_checker import first_occurrence


class AdjacentMaximumCompletion(BoundaryCompletion):
    """Restrict EVERY internal split to either side of its largest old odd."""

    def states(self, first: int, end: int, even_low: int) -> StateMap:
        key = first, end, even_low
        if key in self.memo:
            return self.memo[key]
        if end - first == 1:
            return super().states(first, end, even_low)
        even_high = even_low + end - first - 2
        maximum_position = max(range(first, end), key=self.p.__getitem__)
        result: StateMap = {}
        for cut in (maximum_position, maximum_position + 1):
            if not first < cut < end:
                continue
            right_ranks = end - cut - 1
            left = self.states(first, cut, even_low + right_ranks)
            right = self.states(cut, end, even_low)
            for ls, lw in left.items():
                for rs, rw in right.items():
                    signature = self.merge(ls, 2 * even_high, rs)
                    if signature is not None:
                        word = lw + (2 * even_high,) + rw
                        previous = result.get(signature)
                        if previous is None or word < previous:
                            result[signature] = word
        self.memo[key] = result
        return result


def adjacent_candidates(p: tuple[int, ...], first: int, end: int,
                        low: int) -> tuple[tuple[int, ...], ...]:
    """Separate grammar enumeration; every tree obeys the proposed split rule."""
    if end - first == 1:
        return ((2 * p[first] - 1,),)
    hi = low + end - first - 2
    position = max(range(first, end), key=p.__getitem__)
    words = []
    for cut in (position, position + 1):
        if first < cut < end:
            for left in adjacent_candidates(p, first, cut, low + end - cut - 1):
                for right in adjacent_candidates(p, cut, end, low):
                    words.append(left + (2 * hi,) + right)
    return tuple(sorted(words))


def run() -> dict[str, object]:
    start = time.monotonic()
    examined = 0
    adjacent_failure = None
    for m in range(1, 8):
        for p in itertools.permutations(range(1, m + 1)):
            solver = AdjacentMaximumCompletion(p)
            result = solver.solve()
            examined += 1
            if result["output"] is None:
                witnesses = []
                for word in adjacent_candidates(p, 0, m, 1):
                    occurrence = first_occurrence(word)
                    if occurrence is None:
                        raise RuntimeError("DP rejected an avoiding restricted grammar witness")
                    witnesses.append({"word": word, "rho": tuple(x // 2 for x in word[1::2]),
                                      "occurrence_zero_based": occurrence,
                                      "selected_values": tuple(word[i] for i in occurrence)})
                adjacent_failure = {"input": p, "all_candidate_witnesses": witnesses,
                    "candidates": len(witnesses),
                    "minimality_scope": "all shorter inputs then prior lexicographic inputs",
                    "unrestricted_132_completion": BoundaryCompletion(p).solve()}
                break
        if adjacent_failure is not None:
            break

    # This state is reachable at cut4 of the full root for the displayed input.
    p = (2, 1, 4, 3, 5, 6, 7)
    solver = BoundaryCompletion(p)
    result = solver.solve()
    key = (0, 4, 3)
    if key not in solver.memo:
        raise RuntimeError("Named local band state was not reached by the grammar")
    if solver.memo[key] or not no_unhit_old_rectangle(solver, key):
        raise RuntimeError("Proposed band-condition obstruction did not occur")
    old = (3, 1, 7, 5)
    band_witnesses = []
    for even_word in itertools.permutations((6, 8, 10)):
        word = tuple(x for pair in zip(old[:-1], even_word) for x in pair) + old[-1:]
        occurrence = first_occurrence(standardize(word))
        if occurrence is None:
            raise RuntimeError("Named local counterexample has an arbitrary-scaffold completion")
        band_witnesses.append({"even_word": even_word, "word": word,
            "occurrence_zero_based": occurrence,
            "selected_values": tuple(word[i] for i in occurrence)})
    root = Path(__file__).parent
    return {"decision_message_id": 410, "full_target_solved": False,
        "claim_status": "two explicit failed induction invariants; no failure of full completion",
        "adjacent_max_inputs_examined": examined,
        "adjacent_max_failure": adjacent_failure,
        "band_condition_failure": {"input": p, "reachable_subproblem": key,
            "old_word": old, "even_band": (6, 8, 10),
            "old_words_below_and_above_band_avoid": True,
            "all_six_arbitrary_even_scaffold_witnesses": band_witnesses,
            "full_input_still_has_132_completion": result},
        "source_sha256": hashlib.sha256((root / "probe_boundary_invariants.py").read_bytes()).hexdigest(),
        "python": platform.python_version(), "elapsed_seconds": time.monotonic() - start,
        "peak_rss_kib_linux": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}


if __name__ == "__main__":
    print(json.dumps(run(), indent=2))
