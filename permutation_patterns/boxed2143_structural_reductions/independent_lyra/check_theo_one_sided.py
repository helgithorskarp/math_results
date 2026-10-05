"""Lyra's direct geometric replay of Theo's one-sided interval obstruction.

Initial/terminal detection is derived from quadruples and outside points,
instead of Theo's filtered words and consecutive-window scans.
"""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path
import platform

from definition_checker import occurrences, validate_permutation


def one_sided_geometric_detection(p: tuple[int, ...]) -> bool:
    for chosen in itertools.combinations(range(len(p)), 4):
        i1, i2, i3, i4 = chosen
        if p[i2] < p[i1] < p[i4] < p[i3]:
            outside = tuple(p[j] for j in range(i1 + 1, i4) if j not in chosen)
            # The smallest initial threshold retaining all chosen points is
            # their maximum. The largest terminal threshold is their minimum.
            if all(x > p[i3] for x in outside) or all(x < p[i2] for x in outside):
                return True
    return False


def restrictions(p: tuple[int, ...]) -> dict[str, list[dict[str, object]]]:
    return {"initial": [{"t": t, "word": [x for x in p if x <= t]}
                        for t in range(1, len(p) + 1)],
            "terminal": [{"t": t, "word": [x for x in p if x >= t]}
                         for t in range(1, len(p) + 1)]}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def main() -> None:
    root = Path(__file__).parent
    received = root.resolve().parent
    baseline = json.loads((received / "one-sided-controls.json").read_text())
    tested = 0
    first = None
    for n in range(7):
        for p in itertools.permutations(range(1, n + 1)):
            tested += 1
            if tuple(occurrences(p)) and not one_sided_geometric_detection(p):
                first = p
                break
        if first is not None:
            break
    require(first == (3, 1, 2, 5, 6, 4), "Different first obstruction")
    require(tested == baseline["permutations_tested_until_first_failure"], "Finite coverage mismatch")
    require(restrictions(first) == baseline["one_sided_restrictions"], "Restriction data mismatch")
    minimal_occurrences = tuple(occurrences(first))
    require(minimal_occurrences == ((0, 2, 3, 5),), "Minimal example is not the claimed unique occurrence")
    families = []
    for k in range(1, 7):
        for ell in range(1, 7):
            n = k + ell + 4
            p = (k + 2,) + tuple(range(1, k + 1)) + (k + 1, k + 4) + tuple(range(k + 5, n + 1)) + (k + 3,)
            validate_permutation(p)
            found = tuple(occurrences(p))
            require(bool(found), "Family lost its boxed occurrence")
            require(not one_sided_geometric_detection(p), "Family passes one-sided detection")
            families.append({"k": k, "l": ell, "p": p, "occurrences": found})
    stream = json.dumps(families, sort_keys=True, separators=(",", ":")).encode()
    family_hash = hashlib.sha256(stream).hexdigest()
    require(family_hash == baseline["family_stream_sha256"], "Family occurrence-stream mismatch")
    proof = received / "ONE_SIDED_INTERVAL_OBSTRUCTION.md"
    report = {"author": "literature-researcher-4", "checker": "literature-researcher-2",
        "decision_message_id": 410, "full_target_solved": False,
        "checked_scope": "finite minimality, exact restrictions and36 two-parameter family controls",
        "algorithm": "quadruple order plus interior points relative to selected extrema",
        "proof_snapshot_sha256": hashlib.sha256(proof.read_bytes()).hexdigest(),
        "python": platform.python_version(), "permutations_tested_until_first_failure": tested,
        "minimal_counterexample": first, "occurrences_zero_based": minimal_occurrences,
        "family_cases": len(families), "family_stream_sha256": family_hash}
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
