"""Exact boundary-state search for 132-avoiding even scaffolds.

This is a complete finite algorithm for the specified stronger completion
format, not a proof that an avoiding completion exists for every input. A state
keeps the first/last three entries after every global value-interval restriction.
"""

from __future__ import annotations

import argparse
import json
import platform
import resource
import time
from collections.abc import Sequence

from definition_checker import validate_permutation

Signature = tuple[tuple[tuple[int, ...], tuple[int, ...]], ...]
StateMap = dict[Signature, tuple[int, ...]]


class BoundaryCompletion:
    def __init__(self, permutation: Sequence[int]):
        self.p = validate_permutation(permutation)
        if not 1 <= len(self.p) <= 9:
            raise ValueError("Exploratory implementation is capped at1<=m<=9")
        self.m = len(self.p)
        self.n = 2 * self.m - 1
        self.intervals = tuple((lo, hi) for lo in range(1, self.n + 1)
                               for hi in range(lo, self.n + 1))
        self.memo: dict[tuple[int, int, int], StateMap] = {}
        self.merges_attempted = 0
        self.merges_rejected = 0

    def signature(self, word: Sequence[int]) -> Signature:
        rows = []
        for lo, hi in self.intervals:
            retained = tuple(x for x in word if lo <= x <= hi)
            rows.append((retained[:3], retained[-3:]))
        return tuple(rows)

    def merge(self, left: Signature, root: int, right: Signature) -> Signature | None:
        """Exact composition criterion for two internally avoiding words."""
        self.merges_attempted += 1
        rows = []
        for (lo, hi), (lp, ls), (rp, rs) in zip(self.intervals, left, right):
            middle = (root,) if lo <= root <= hi else ()
            boundary = ls + middle + rp
            for j in range(len(boundary) - 3):
                a, b, c, d = boundary[j:j + 4]
                if b < a < d < c:
                    self.merges_rejected += 1
                    return None
            rows.append(((lp + middle + rp)[:3], (ls + middle + rs)[-3:]))
        return tuple(rows)

    def states(self, first: int, end: int, even_low: int) -> StateMap:
        """Return one canonical witness for every realizable avoiding signature.

        The segment uses original odd values2*p[first:end]-1 and the even ranks
        even_low,...,even_low+segment_length-2. Original values stay absolute.
        """
        size = end - first
        if not 0 <= first < end <= self.m or even_low < 1:
            raise ValueError("Invalid segment or even-rank lower endpoint")
        even_high = even_low + size - 2
        if size > 1 and even_high > self.m - 1:
            raise ValueError("Even-rank segment is outside the global alphabet")
        key = first, end, even_low
        if key in self.memo:
            return self.memo[key]
        if size == 1:
            word = (2 * self.p[first] - 1,)
            result = {self.signature(word): word}
            self.memo[key] = result
            return result
        result: StateMap = {}
        for cut in range(first + 1, end):
            right_ranks = end - cut - 1
            left_states = self.states(first, cut, even_low + right_ranks)
            right_states = self.states(cut, end, even_low)
            root = 2 * even_high
            for left_signature, left_word in left_states.items():
                for right_signature, right_word in right_states.items():
                    signature = self.merge(left_signature, root, right_signature)
                    if signature is not None:
                        word = left_word + (root,) + right_word
                        previous = result.get(signature)
                        if previous is None or word < previous:
                            result[signature] = word
        self.memo[key] = result
        return result

    def solve(self) -> dict[str, object]:
        start = time.monotonic()
        roots = self.states(0, self.m, 1)
        word = min(roots.values()) if roots else None
        rho = tuple(x // 2 for x in word[1::2]) if word is not None else None
        if word is not None and tuple((x + 1) // 2 for x in word[::2]) != self.p:
            raise RuntimeError("Completion failed its input recovery check")
        sizes = {str(key): len(states) for key, states in sorted(self.memo.items())}
        return {"decision_message_id": 410,
            "claim_status": "finite exact132-scaffold completion search; no universal existence proof",
            "input": self.p, "output": word, "rho": rho,
            "root_state_count": len(roots), "subproblem_count": len(self.memo),
            "total_state_count": sum(len(x) for x in self.memo.values()),
            "subproblem_state_counts": sizes, "merges_attempted": self.merges_attempted,
            "merges_rejected": self.merges_rejected,
            "python": platform.python_version(), "elapsed_seconds": time.monotonic() - start,
            "peak_rss_kib_linux": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
            "full_target_solved": False}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--permutation", required=True)
    args = parser.parse_args()
    p = tuple(int(x) for x in args.permutation.split(","))
    print(json.dumps(BoundaryCompletion(p).solve(), indent=2))


if __name__ == "__main__":
    main()
