"""Author finite controls of a full-entropy interval-signature fiber map."""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path
import platform
import resource
import time

from definition_checker import occurrences, validate_permutation


def guard_map(permutation: tuple[int, ...], k: int) -> tuple[int, ...]:
    p = validate_permutation(permutation)
    if not p or k < 1:
        raise ValueError("This map uses m>=1,k>=1")
    q = 2 * k + 1
    prefix = tuple(1 + q * i + j for i in range(len(p) - 1)
                   for j in range(k + 1, 2 * k + 1))
    suffix = tuple(1 + q * i + j for i in range(len(p) - 1)
                   for j in range(1, k + 1))
    word = prefix + tuple(1 + q * (x - 1) for x in p) + suffix
    validate_permutation(word)
    return word


def interval_signature(word: tuple[int, ...], k: int):
    result = []
    for lo in range(1, len(word) + 1):
        for hi in range(lo, len(word) + 1):
            selected = tuple(x for x in word if lo <= x <= hi)
            result.append((selected[:k], selected[-k:]))
    return tuple(result)


def run():
    start = time.monotonic()
    digest = hashlib.sha256()
    cases = interval_cases = 0
    rows = []
    for k in (1, 2, 3):
        for m in range(1, 6):
            reference = interval_signature(guard_map(tuple(range(1, m + 1)), k), k)
            row_cases = total_occ = avoiding_count = 0
            seen = set()
            for p in itertools.permutations(range(1, m + 1)):
                word = guard_map(p, k)
                if word in seen:
                    raise RuntimeError("Guard map is not injective")
                seen.add(word)
                offset = k * (m - 1)
                recovered = tuple((x - 1) // (2 * k + 1) + 1
                                  for x in word[offset:offset + m])
                if recovered != p:
                    raise RuntimeError("Guard map does not recover input")
                actual = tuple(occurrences(word))
                expected = tuple(tuple(i + offset for i in occurrence) for occurrence in occurrences(p))
                if actual != expected:
                    raise RuntimeError(f"Exact occurrence preservation failed: {p}, {k}")
                signature = interval_signature(word, k)
                if signature != reference:
                    raise RuntimeError(f"Full interval signature depends on input: {p}, {k}")
                interval_cases += len(signature)
                cases += 1
                row_cases += 1
                total_occ += len(actual)
                avoiding_count += not actual
                digest.update((json.dumps([k, p, word, actual], separators=(",", ":")) + "\n").encode())
            rows.append({"k": k, "m": m, "output_length": (2 * k + 1) * m - 2 * k,
                         "inputs": row_cases, "avoiding_outputs": avoiding_count,
                         "total_occurrences": total_occ, "common_signature_count": 1})
    fixture = [guard_map((1, 2), 3), guard_map((2, 1), 3)]
    if any(tuple(occurrences(word)) for word in fixture) or fixture[0] == fixture[1]:
        raise RuntimeError("Named two-avoider collision failed")
    if interval_signature(fixture[0], 3) != interval_signature(fixture[1], 3):
        raise RuntimeError("Named pair has different k3 signature")
    root = Path(__file__).parent
    return {"decision_message_id": 410, "full_target_solved": False,
        "claim_status": "author finite controls for written occurrence/signature preservation; no growth decision",
        "inputs_k_m": cases, "all_interval_entries_compared": interval_cases,
        "rows": rows, "ordered_occurrence_map_sha256": digest.hexdigest(),
        "two_avoiders_in_one_k3_signature": fixture,
        "proof_sha256": hashlib.sha256((root / "BOUNDARY_FIBER_ENTROPY.md").read_bytes()).hexdigest(),
        "source_sha256": hashlib.sha256((root / "check_boundary_fiber.py").read_bytes()).hexdigest(),
        "literal_checker_sha256": hashlib.sha256((root / "definition_checker.py").read_bytes()).hexdigest(),
        "python": platform.python_version(), "elapsed_seconds": time.monotonic() - start,
        "peak_rss_kib_linux": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}


if __name__ == "__main__":
    print(json.dumps(run(), indent=2))
