"""Lyra's direct-occurrence controls for Theo's four structural reductions.

The accompanying written review checks the universal proofs. These finite
controls do not establish an infinite entropy bound or new growth theorem.
"""

from __future__ import annotations

import hashlib
import itertools
import json
import math
from pathlib import Path
import platform
import time

from definition_checker import occurrences, validate_permutation


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def skew_components(p: tuple[int, ...]) -> tuple[tuple[int, tuple[int, ...]], ...]:
    n = len(p)
    cuts = [0] + [k for k in range(1, n + 1)
                  if set(p[:k]) == set(range(n - k + 1, n + 1))]
    result = []
    for left, right in zip(cuts, cuts[1:]):
        raw = p[left:right]
        low = min(raw)
        component = tuple(x - low + 1 for x in raw)
        validate_permutation(component)
        result.append((left, component))
    return tuple(result)


def inflate(p: tuple[int, ...], sizes: tuple[int, ...]) -> tuple[tuple[int, ...], tuple[int, ...]]:
    validate_permutation(p)
    require(len(sizes) == len(p) and all(type(s) is int and s > 0 for s in sizes),
            "Expected one positive integer size per original position")
    result = []
    starts = []
    for i, value in enumerate(p):
        starts.append(len(result))
        lower_values = sum(sizes[j] for j in range(len(p)) if p[j] < value)
        result.extend(range(lower_values + 1, lower_values + sizes[i] + 1))
    output = tuple(result)
    validate_permutation(output)
    return output, tuple(starts)


def forced_lifts(p: tuple[int, ...], sizes: tuple[int, ...], starts: tuple[int, ...]) -> tuple[tuple[int, ...], ...]:
    return tuple(sorted((starts[i1] + sizes[i1] - 1,
                         starts[i2] + sizes[i2] - 1,
                         starts[i3], starts[i4])
                        for i1, i2, i3, i4 in occurrences(p)))


def main() -> None:
    began = time.monotonic()
    decomposition_hash = hashlib.sha256()
    a = []
    b = []
    decomposition_cases = 0
    for n in range(8):
        an = bn = count = 0
        for p in itertools.permutations(range(1, n + 1)):
            count += 1
            decomposition_cases += 1
            components = skew_components(p)
            expected = tuple(sorted(tuple(index + start for index in occurrence)
                                    for start, q in components for occurrence in occurrences(q)))
            direct = tuple(occurrences(p))
            require(expected == direct, f"Skew separation mismatch at {p}")
            an += not direct
            bn += bool(p) and len(components) == 1 and not direct
            entry = json.dumps([p, components, direct], separators=(",", ":")) + "\n"
            decomposition_hash.update(entry.encode("ascii"))
        require(count == math.factorial(n), "Incomplete component enumeration")
        a.append(an)
        b.append(bn)
        if n:
            require(an == sum(b[k] * a[n - k] for k in range(1, n + 1)),
                    f"Skew recurrence mismatch at {n}")

    inflation_hash = hashlib.sha256()
    inflation_cases = 0
    for m in range(6):
        for p in itertools.permutations(range(1, m + 1)):
            for sizes in itertools.product((1, 2), repeat=m):
                output, starts = inflate(p, sizes)
                expected = forced_lifts(p, sizes, starts)
                direct = tuple(occurrences(output))
                require(expected == direct, f"Inflation lift mismatch at {p}, {sizes}")
                inflation_cases += 1
                entry = json.dumps([p, sizes, output, direct], separators=(",", ":")) + "\n"
                inflation_hash.update(entry.encode("ascii"))
    unequal_p = (2, 1, 4, 3)
    unequal_sizes = (1, 2, 3, 4)
    output, starts = inflate(unequal_p, unequal_sizes)
    require(tuple(occurrences(output)) == forced_lifts(unequal_p, unequal_sizes, starts),
            "Unequal-size inflation mismatch")
    source = Path(__file__).resolve().parents[1] / "structural_reductions.md"
    report = {"author": "literature-researcher-4", "checker": "literature-researcher-2",
        "decision_message_id": 410, "full_target_solved": False,
        "claim_status": "finite controls for universally argued partial reductions",
        "proof_snapshot_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
        "python": platform.python_version(), "decomposition_cases": decomposition_cases,
        "a_n0_7": a, "b_n0_7": b,
        "decomposition_stream_sha256": decomposition_hash.hexdigest(),
        "inflation_cases": inflation_cases, "inflation_stream_sha256": inflation_hash.hexdigest(),
        "unequal_fixture": {"p": unequal_p, "sizes": unequal_sizes, "output": output,
                            "occurrences_zero_based": tuple(occurrences(output))},
        "elapsed_seconds": time.monotonic() - began}
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
