"""Finite controls for the written marker obstruction, not its uniform proof."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import platform
import time
from pathlib import Path

from cartesian_fibers import load_checker, pair_key, predecessor_masks, recursive_parents, require, validate_permutation


def marker_map(values):
    sigma = validate_permutation(values)
    m = len(sigma)
    if m == 0:
        raise ValueError("Marker map requires m>=1")
    result = []
    for i, value in enumerate(sigma, 1):
        result.append(m - 1 + value)
        if i < m:
            result.extend((2 * m - 1 + i, i))
    return validate_permutation(result)


def formula_pair(m):
    if type(m) is not int or m < 1:
        raise ValueError("Require integer m>=1")
    if m == 1:
        return ((-1,), (-1,))
    n = 3 * m - 2
    minimum = [-1] * n
    maximum = [-1] * n
    x = lambda i: 3 * (i - 1)
    h = lambda i: x(i) + 1
    low = lambda i: x(i) + 2
    for i in range(1, m):
        minimum[x(i)] = low(i)
        minimum[h(i)] = x(i)
        minimum[low(i)] = low(i - 1) if i > 1 else -1
        maximum[h(i)] = h(i + 1) if i < m - 1 else -1
        maximum[low(i)] = x(i + 1)
    minimum[x(m)] = low(m - 1)
    for i in range(1, m + 1):
        maximum[x(i)] = h(max(1, i - 1))
    return tuple(minimum), tuple(maximum)


def minimum_at(m, position):
    if not 0 <= position < m:
        raise ValueError("Position out of range")
    others = iter(range(2, m + 1))
    return tuple(1 if i == position else next(others) for i in range(m))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--literal-checker", type=Path, required=True)
    parser.add_argument("--rectangle-checker", type=Path, required=True)
    parser.add_argument("--max-base", type=int, default=6)
    parser.add_argument("--max-branch-family", type=int, default=12)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if not 1 <= args.max_base <= 7 or not 2 <= args.max_branch_family <= 14:
        raise ValueError("Require 1<=max-base<=7 and 2<=max-branch-family<=14")
    literal = load_checker(args.literal_checker)
    rectangles = load_checker(args.rectangle_checker)
    sources = {str(p): hashlib.sha256(p.read_bytes()).hexdigest()
               for p in (args.literal_checker, args.rectangle_checker, Path(__file__), Path(__file__).with_name('cartesian_fibers.py'))}
    report = {"decision_message_id": 410, "claim_status": "finite controls of a separate uniform author argument",
              "python": platform.python_version(), "source_sha256": sources,
              "exhaustive_base_controls": [], "viable_position_controls": []}
    started = time.monotonic()
    for m in range(1, args.max_base + 1):
        digest = hashlib.sha256()
        count = 0
        for sigma in itertools.permutations(range(1, m + 1)):
            image = marker_map(sigma)
            expected = tuple(tuple(3 * i for i in indices) for indices in literal.occurrences(sigma))
            actual = tuple(literal.occurrences(image))
            independent = tuple(sorted(rectangles.boxed_occurrences(image)))
            require(actual == expected, f"Occurrence correspondence failed at {sigma}")
            require(independent == expected, f"Rectangle representation failed at {sigma}")
            pair = formula_pair(m)
            require(pair_key(image) == pair, f"Explicit tree formula failed at {sigma}")
            require((recursive_parents(image), recursive_parents(image, True)) == pair,
                    f"Recursive tree formula failed at {sigma}")
            require(tuple(value - m + 1 for value in image[::3]) == sigma, "Decoding failed")
            digest.update(json.dumps([sigma, image, expected, pair], separators=(",", ":")).encode()+b"\n")
            count += 1
        row = {"m": m, "image_length": 3 * m - 2, "permutations_checked": count,
               "ordered_entry_sha256": digest.hexdigest()}
        report["exhaustive_base_controls"].append(row)
        print(json.dumps(row), flush=True)
    for m in range(2, args.max_branch_family + 1):
        pair = formula_pair(m)
        pred = predecessor_masks(pair)
        chosen = sum(1 << (3 * i - 1) for i in range(1, m))
        available = [i for i in range(3 * m - 2) if not chosen & (1 << i) and not pred[i] & ~chosen]
        require(available == list(range(0, 3 * m - 2, 3)), "Available-position formula failed")
        witnesses = []
        for position in range(m):
            sigma = minimum_at(m, position)
            image = marker_map(sigma)
            require(pair_key(image) == pair, "Viable witness left common fiber")
            require(tuple(literal.occurrences(image)) == (), "Nonavoiding viable witness")
            require(tuple(rectangles.boxed_occurrences(image)) == (), "Independent viable witness failed")
            require(image[3 * position] == m, "Next-rank position failed")
            require(all(image[3 * i - 1] == i for i in range(1, m)), "Prefix changed")
            witnesses.append(image)
        report["viable_position_controls"].append({"m": m, "image_length": 3 * m - 2,
            "available_zero_based": available, "number_of_viable_witnesses": len(witnesses),
            "witness_stream_sha256": hashlib.sha256(json.dumps(witnesses, separators=(",", ":")).encode()).hexdigest(),
            "witnesses": witnesses if m <= 4 else None})
    for path, digest in sources.items():
        require(hashlib.sha256(Path(path).read_bytes()).hexdigest() == digest, "Input source changed during controls")
    report["elapsed_seconds"] = time.monotonic() - started
    report["trust_boundary"] = "Inspected Python/stdlib source and two frozen differently derived finite checkers; uniform proof is written separately"
    args.output.parent.mkdir(parents=True, exist_ok=True)
    temporary = args.output.with_suffix(args.output.suffix+".tmp")
    temporary.write_text(json.dumps(report, indent=2)+"\n")
    temporary.replace(args.output)
    print(json.dumps({"elapsed_seconds": report["elapsed_seconds"], "branch_sizes": [r['number_of_viable_witnesses'] for r in report['viable_position_controls']]}))


if __name__ == "__main__":
    main()
