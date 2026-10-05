"""Definition-level checker for the exact boxed-2143 target in chat decision 410.

Permutation entries are one based; returned indices are zero based. This checker
enumerates four indices and scans the open rectangle directly. It is an exact
finite-input checker, not an infinite growth proof. Only Python's standard library
is used. Empty input is permitted as an insertion-tree root, with zero occurrences.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import platform
import time
from collections.abc import Iterator, Sequence


def validate_permutation(permutation: Sequence[int]) -> tuple[int, ...]:
    p = tuple(permutation)
    if any(type(v) is not int for v in p) or sorted(p) != list(range(1, len(p) + 1)):
        raise ValueError("Expected a permutation of 1,...,n")
    return p


def is_boxed_occurrence(p: Sequence[int], indices: tuple[int, int, int, int]) -> bool:
    """Check one candidate using exactly the strict inequalities in decision 410."""
    i1, i2, i3, i4 = indices
    if not (0 <= i1 < i2 < i3 < i4 < len(p)):
        raise ValueError("Candidate indices must be strictly increasing and in range")
    if not p[i2] < p[i1] < p[i4] < p[i3]:
        return False
    chosen = set(indices)
    return not any(
        j not in chosen and p[i2] < p[j] < p[i3]
        for j in range(i1 + 1, i4)
    )


def occurrences(permutation: Sequence[int]) -> Iterator[tuple[int, int, int, int]]:
    p = validate_permutation(permutation)
    for indices in itertools.combinations(range(len(p)), 4):
        if is_boxed_occurrence(p, indices):
            yield indices


def first_occurrence(permutation: Sequence[int]) -> tuple[int, int, int, int] | None:
    return next(occurrences(permutation), None)


def avoids(permutation: Sequence[int]) -> bool:
    return first_occurrence(permutation) is None


def self_check() -> dict[str, object]:
    # Explicit hand-sized boundary and shading checks, including a classical
    # occurrence whose internal blocker makes this particular tuple nonboxed.
    def require(condition: bool, message: str) -> None:
        if not condition:
            raise RuntimeError(message)

    require(avoids(()), "Empty root has an occurrence")
    require(avoids((1, 2, 3)), "Length-three input has an occurrence")
    require(first_occurrence((2, 1, 4, 3)) == (0, 1, 2, 3), "Basic 2143 mismatch")
    require(not is_boxed_occurrence((2, 1, 3, 5, 4), (0, 1, 3, 4)), "Blocker missed")
    require(avoids((2, 1, 3, 5, 4)), "Blocked example misclassified")
    require(avoids((2, 4, 1, 5, 3)), "Source Remark 7.2 mismatch")
    # The last example is the source's Remark 7.2: it contains the adjacent-middle
    # vincular pattern and lies outside the known plane-permutation subclass.
    p = (2, 4, 1, 5, 3)
    require(p[2] < p[0] < p[4] < p[3], "Vincular control mismatch")
    require(not is_boxed_occurrence(p, (0, 2, 3, 4)), "Remark 7.2 blocker missed")
    for malformed in ((0,), (1, 1), (2,), (True,)):
        try:
            validate_permutation(malformed)
        except ValueError:
            pass
        else:
            raise AssertionError(f"Accepted malformed input: {malformed}")
    return {"status": "passed", "valid_fixtures": 5, "malformed_fixtures": 4}


def count_avoiders(max_n: int) -> list[dict[str, object]]:
    if not 0 <= max_n <= 9:
        raise ValueError("This transparent reference census supports 0<=max_n<=9")
    output = []
    for n in range(max_n + 1):
        started = time.monotonic()
        count = 0
        digest = hashlib.sha256()
        for p in itertools.permutations(range(1, n + 1)):
            if avoids(p):
                count += 1
                digest.update(json.dumps(p, separators=(",", ":")).encode() + b"\n")
        output.append({"n": n, "a_n": count, "ordered_avoider_sha256": digest.hexdigest(),
                       "elapsed_seconds": time.monotonic() - started})
    return output


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--count-max", type=int)
    parser.add_argument("--permutation", help="Comma-separated entries, e.g. 2,1,4,3")
    args = parser.parse_args()
    report: dict[str, object] = {"python": platform.python_version(),
        "decision_message_id": 410, "claim_status": "finite exact checker / observation",
        "trust_boundary": "Python interpreter, standard library, and inspected source",
        "self_check": self_check()}
    if args.count_max is not None:
        report["census"] = count_avoiders(args.count_max)
    if args.permutation is not None:
        p = tuple(int(x) for x in args.permutation.split(","))
        witness = first_occurrence(p)
        report["permutation"] = p
        report["avoids"] = witness is None
        report["first_occurrence_zero_based"] = witness
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
