#!/usr/bin/env python3
"""Small exhaustive and randomized controls for the independent review code."""
from __future__ import annotations

import argparse
import importlib.util
import itertools
import json
import random
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent


def load_checker():
    spec = importlib.util.spec_from_file_location("six_review_checker", HERE / "independent_check.py")
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def brute_weighted(singletons, pairs, width):
    full = (1 << width) - 1
    items = [(mask, 1) for mask in singletons] + [(mask, 2) for mask in pairs]
    for chosen in range(1 << len(items)):
        cost = 0
        union = 0
        for index, (mask, item_cost) in enumerate(items):
            if chosen >> index & 1:
                cost += item_cost
                union |= mask
        if cost <= 6 and union == full:
            return True
    return False


def run_controls(work):
    checker = load_checker()
    rng = random.Random(0xB50306)
    feasible = infeasible = 0
    for case in range(100):
        width = rng.randrange(1, 10)
        singleton_count = rng.randrange(1, 8)
        pair_count = rng.randrange(1, 7)
        limit = 1 << width
        singletons = [rng.randrange(limit) for _ in range(singleton_count)]
        pairs = [rng.randrange(limit) for _ in range(pair_count)]
        expected = brute_weighted(singletons, pairs, width)
        observed, _ = checker.weighted_six_cover(singletons, pairs, width)
        checker.require(observed == expected, f"weighted control {case}")
        feasible += expected
        infeasible += not expected

    posting_queries = 0
    for case in range(100):
        width = rng.randrange(1, 12)
        count = rng.randrange(1, 30)
        limit = 1 << width
        items = [(index,) for index in range(count)]
        masks = [rng.randrange(limit) for _ in range(count)]
        table = checker.PostingTable(items, masks, width)
        for _ in range(20):
            residual = rng.randrange(limit)
            expected = [index for index, mask in enumerate(masks) if mask & residual == residual]
            observed = list(table.supersets(residual))
            checker.require(observed == expected, f"posting control {case}")
            posting_queries += 1

    template = checker.tree_template_control()
    checker.require(
        template
        == {
            "connected_labelled_graphs": 26704,
            "relabelled_template_counts": [6, 360, 120, 90, 360, 360],
            "missed": 0,
        },
        "tree-template control transcript",
    )

    # Exercise the C++ traversal under undefined-behaviour sanitization on K6.
    executable = work / "connected_tree_check_ubsan"
    subprocess.run(
        [
            "g++",
            "-std=c++17",
            "-O1",
            "-g",
            "-Wall",
            "-Wextra",
            "-Wpedantic",
            "-fsanitize=undefined",
            "-fno-sanitize-recover=all",
            str(HERE / "connected_tree_check.cpp"),
            "-o",
            str(executable),
        ],
        check=True,
    )
    graph = work / "k6-input.txt"
    with graph.open("w") as output:
        output.write("6 6 1\n")
        for vertex in range(6):
            neighbours = [other for other in range(6) if other != vertex]
            output.write(
                " ".join(map(str, [vertex, 4, 0, 0, len(neighbours), *neighbours])) + "\n"
            )
    result = subprocess.run([str(executable), str(graph)], text=True, capture_output=True)
    checker.require(result.returncode == 0, "sanitized C++ control")
    rows = [list(map(int, line.split())) for line in result.stdout.splitlines()]
    checker.require(rows == [[shape, 720, 720, 0] for shape in range(6)], "K6 map counts")

    weighted_executable = work / "weighted_cover_check_ubsan"
    subprocess.run(
        [
            "g++",
            "-std=c++17",
            "-O1",
            "-g",
            "-Wall",
            "-Wextra",
            "-Wpedantic",
            "-fsanitize=undefined",
            "-fno-sanitize-recover=all",
            str(HERE / "weighted_cover_check.cpp"),
            "-o",
            str(weighted_executable),
        ],
        check=True,
    )
    compiled_weighted_cases = 40
    for case in range(compiled_weighted_cases):
        width = rng.randrange(1, 9)
        limit = 1 << width
        original_singles = [rng.randrange(limit) for _ in range(rng.randrange(1, 7))]
        original_pairs = [rng.randrange(limit) for _ in range(rng.randrange(1, 6))]
        expected = brute_weighted(original_singles, original_pairs, width)
        singles = checker.maximal_masks(original_singles)
        pairs = checker.maximal_masks(
            mask
            for mask in set(original_pairs) - {0}
            if not any(mask & ~single == 0 for single in singles)
        )
        instance = work / f"weighted-{case}.txt"
        with instance.open("w") as output:
            output.write(f"{width} {len(singles)} {len(pairs)}\n")
            for mask in (*singles, *pairs):
                output.write(f"{mask} 0 0\n")
        result = subprocess.run(
            [str(weighted_executable), str(instance)], text=True, capture_output=True
        )
        observed = result.returncode == 10 and result.stdout.startswith("SAT ")
        checker.require(
            observed == expected and result.returncode in (0, 10),
            f"compiled weighted control {case}",
        )

    return {
        "status": "PASS",
        "weighted_cases": 100,
        "weighted_feasible": feasible,
        "weighted_infeasible": infeasible,
        "posting_queries": posting_queries,
        "compiled_weighted_cases": compiled_weighted_cases,
        "tree_template_control": template,
        "ubsan_k6_rows": rows,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--work", type=Path, required=True)
    args = parser.parse_args()
    args.work.mkdir(parents=True, exist_ok=True)
    result = run_controls(args.work)
    (args.work / "controls-output.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
