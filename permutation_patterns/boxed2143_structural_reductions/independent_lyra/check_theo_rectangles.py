"""Lyra's entry-level reproduction of Theo's canonical rectangle checker.

Different algorithms: quadruples with direct shading versus value-interval factors.
No finite bound in this report implies an infinite growth classification.
"""

from __future__ import annotations

import hashlib
import importlib.util
import itertools
import json
import math
from pathlib import Path
import platform
import sys
import time

from definition_checker import occurrences as direct_2143


THEO_ROOT = Path(__file__).resolve().parents[1]


def direct_2413(p: tuple[int, ...]) -> tuple[tuple[int, ...], ...]:
    output = []
    for i1, i2, i3, i4 in itertools.combinations(range(len(p)), 4):
        if p[i3] < p[i1] < p[i4] < p[i2]:
            chosen = {i1, i2, i3, i4}
            if not any(j not in chosen and p[i3] < p[j] < p[i2]
                       for j in range(i1 + 1, i4)):
                output.append((i1, i2, i3, i4))
    return tuple(output)


def main() -> None:
    # Avoid writing bytecode into another researcher's workspace.
    sys.dont_write_bytecode = True
    source = THEO_ROOT / "rectangle_checker.py"
    spec = importlib.util.spec_from_file_location("theo_rectangles_reviewed", source)
    if spec is None or spec.loader is None:
        raise RuntimeError("Could not load reviewed source")
    theo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(theo)
    theo.controls()
    baseline = json.loads((THEO_ROOT / "rectangle-baseline.json").read_text())
    expected_hashes = {row["n"]: row["ordered_occurrence_stream_sha256"]
                       for row in baseline["rows"]}
    rows = []
    started = time.monotonic()
    for n in range(8):
        hashes = {p: hashlib.sha256() for p in ("2143", "2413")}
        counts = {p: 0 for p in hashes}
        tested = 0
        for p in itertools.permutations(range(1, n + 1)):
            tested += 1
            for pattern, direct in (("2143", tuple(direct_2143(p))), ("2413", direct_2413(p))):
                rectangles = theo.boxed_occurrences(p, pattern)
                if direct != rectangles:
                    raise RuntimeError(f"Occurrence mismatch at {p}, {pattern}: {direct}, {rectangles}")
                counts[pattern] += not direct
                encoded = json.dumps([p, direct], separators=(",", ":")) + "\n"
                hashes[pattern].update(encoded.encode("ascii"))
        if tested != math.factorial(n):
            raise RuntimeError("Incomplete enumeration")
        observed_hashes = {p: h.hexdigest() for p, h in hashes.items()}
        if expected_hashes[n] != observed_hashes:
            raise RuntimeError(f"Recorded Theo baseline hash mismatch at n={n}")
        rows.append({"n": n, "permutations_tested": tested, "avoiders": counts,
                     "ordered_occurrence_stream_sha256": observed_hashes})
    report = {"author": "literature-researcher-4", "checker": "literature-researcher-2",
        "decision_message_id": 410, "full_target_solved": False,
        "checked_scope": "complete occurrence sets for 2143 and 2413, every permutation n=0..7",
        "claim_status": "definition-level finite internal reproduction, no growth theorem",
        "reviewed_source": str(source), "reviewed_source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
        "direct_checker_sha256": hashlib.sha256((Path(__file__).parent / "definition_checker.py").read_bytes()).hexdigest(),
        "python": platform.python_version(), "permutations_tested": sum(r["permutations_tested"] for r in rows),
        "rows": rows, "elapsed_seconds": time.monotonic() - started}
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
