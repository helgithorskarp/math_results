"""Validate the C35 implementation and its maximizing phase witnesses.

Build optimizer.cpp first; no third-party Python dependencies.
Target-scale fixtures test the budget algorithm, not covering existence.
"""

import argparse
import json
import resource
import subprocess
from pathlib import Path
from random import Random
from time import monotonic

from budget import actual_value, exact_budget, require
from check import equal


def encode(B, b, u, v, fixed):
    rows = [f"{B} {b}"]
    for d in (1, 5, 7, 35):
        t, r = fixed.get(d, (-1, -1))
        rows.append(f"{t} {r}")
    rows.extend(" ".join(map(str, row)) for row in u)
    rows.extend(" ".join(map(str, row)) for row in v)
    return "\n".join(rows) + "\n"


def run(exe, B, b, u, v, fixed=None):
    fixed = {} if fixed is None else fixed
    completed = subprocess.run([str(exe)], input=encode(B, b, u, v, fixed),
                               text=True, capture_output=True, timeout=50, check=True)
    result = json.loads(completed.stdout)
    equal((result["B"], result["C"], result["b"]), (B, 35, b), "instance metadata")
    phases = []
    for expected_d, (d, t, r) in zip((1, 5, 7, 35), result["phases"]):
        equal(d, expected_d, "witness modulus order")
        require(0 <= t < B and 0 <= r < d, "witness phase range")
        if d in fixed:
            equal((t, r), fixed[d], "prescribed top phase")
        phases.append((t, r))
    equal(len(phases), 4, "complete phase witness")
    equal(actual_value(B, 35, b, u, v, phases), result["value"], "literal witness value")
    return result


def controls(exe, targets):
    result = {"small_full_reference_comparisons": [], "fixtures": []}
    rng = Random(835)
    for B, b, fixed in (
            (6, 1, {1: (0, 0), 5: (2, 1)}),
            (6, 1, {5: (2, 1), 7: (4, 3)}),
            (12, 2, {5: (7, 2), 35: (0, 17)}),
            (12, 2, {1: (6, 0), 7: (3, 4)}),
            (18, 1, {1: (0, 0), 5: (8, 4), 7: (13, 6)})):
        u = [[rng.randrange(7) for _ in range(35)] for _ in range(B)]
        v = [[rng.randrange(5) for _ in range(35)] for _ in range(b)]
        for d, (t, r) in fixed.items():
            for z in range(r, 35, d):
                u[t][z] = 0
        compiled = run(exe, B, b, u, v, fixed)
        equal(compiled["value"], exact_budget(B, 35, b, u, v, fixed), "Python full reference")
        result["small_full_reference_comparisons"].append(compiled)
    # Analytically proved strict optimal-charge fixture, also evaluated by
    # the full literal-profile Python DP during development (561).
    B, b = 6, 1
    u = [[10] * 35 if t == 0 else
         [20 if z % 5 == 0 else 0 for z in range(35)] if t == 2 else [0] * 35
         for t in range(B)]
    v = [[int(z == 0) for z in range(35)]]
    compiled = run(exe, B, b, u, v)
    equal(compiled["value"], 561, "four-top optimal-charge fixture")
    result["fixtures"].append(compiled)
    bases = (12, 288, 432) if targets else (12,)
    for B in bases:
        T, b = B // 6, B // 6
        u = [[10] * 35 if t in (0, 3 * T) else [0] * 35 for t in range(B)]
        v = [[int(q == 0 and z == 0) for z in range(35)] for q in range(b)]
        compiled = run(exe, B, b, u, v)
        equal(compiled["value"], 482, "block-label fixture")
        equal(compiled["cofactor_tuples"], 1225, "complete cofactor tuples")
        equal(compiled["local_candidate_visits"], 1225 * T * 2400, "complete local visits")
        result["fixtures"].append(compiled)
    if targets:
        for B, b in ((288, 12), (432, 18)):
            u = [[((37 * t + 19 * z + t * z) % 23) for z in range(35)] for t in range(B)]
            v = [[((11 * q + 7 * z + q * z) % 13) for z in range(35)] for q in range(b)]
            result["fixtures"].append(run(exe, B, b, u, v))
    return result


def reject_controls(exe):
    B, b = 6, 1
    u, v = [[0] * 35 for _ in range(B)], [[0] * 35]
    text = encode(B, b, u, v, {})
    samples = (text + "99\n", text[:-8], text.replace("6 1", "30 1", 1),
               text.replace("-1 -1", "6 0", 1),
               text.replace("6 1", "6 2", 1),
               encode(B, b, [[-1] * 35 for _ in range(B)], v, {}),
               encode(B, b, [[1000000001] * 35 for _ in range(B)], v, {}),
               encode(B, b, [[1] * 35 for _ in range(B)], v, {1: (0, 0)}))
    for i, sample in enumerate(samples):
        p = subprocess.run([str(exe)], input=sample, text=True, capture_output=True, timeout=5)
        if p.returncode == 0 or "Incomplete or invalid computation:" not in p.stderr:
            raise RuntimeError(f"malformed compiled input {i} accepted")
    return len(samples)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--optimizer", type=Path, required=True)
    parser.add_argument("--small", action="store_true", help="sanitizer control subset")
    args = parser.parse_args()
    exe = args.optimizer.resolve()
    started = monotonic()
    result = controls(exe, targets=not args.small)
    result["rejected_inputs"] = reject_controls(exe)
    expected = Path(__file__).with_name("expected-cpp-small.json" if args.small else "expected-cpp.json")
    if expected.exists():
        equal(result, json.loads(expected.read_text()), "published compiled output")
    print(json.dumps(result, indent=2, sort_keys=True))
    print(json.dumps({"seconds": round(monotonic() - started, 3),
                      "child_peak_RSS_KiB": resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss}),
          file=__import__('sys').stderr)


if __name__ == "__main__":
    main()
