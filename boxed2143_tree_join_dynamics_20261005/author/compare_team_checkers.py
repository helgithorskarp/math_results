#!/usr/bin/env python3
"""Compare exact occurrence sets from three separately derived team reductions."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
from itertools import permutations
import json
from pathlib import Path
import platform
import sys
import time

from kernel import boxed_occurrences, legal_maximum_gaps, new_maximum_occurrences


def file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load checker at " + str(path))
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def compare(lyra_path: Path, theo_path: Path, max_n: int) -> dict:
    sources = {
        "quinn_kernel": Path(__file__).with_name("kernel.py"),
        "lyra_definition": lyra_path,
        "theo_rectangle": theo_path,
    }
    before = {name: file_hash(path) for name, path in sources.items()}
    lyra = load_module(lyra_path, "lyra_definition_checker_for_quinn_comparison")
    theo = load_module(theo_path, "theo_rectangle_checker_for_quinn_comparison")
    start = time.monotonic()
    rows = []
    permutations_checked = insertion_instances_checked = 0
    for n in range(max_n + 1):
        digest = hashlib.sha256()
        avoiders = occurrences_found = 0
        for p in permutations(range(1, n + 1)):
            permutations_checked += 1
            definition = tuple(lyra.occurrences(p))
            rectangle = theo.boxed_occurrences(p)
            kernel = boxed_occurrences(p)
            if definition != rectangle or definition != kernel:
                raise RuntimeError(json.dumps({"permutation": p, "lyra": definition,
                                              "theo": rectangle, "quinn": kernel}))
            avoiders += not definition
            occurrences_found += len(definition)
            if n:
                insertion_instances_checked += 1
                gap = p.index(n)
                parent = p[:gap] + p[gap + 1:]
                expected_new = tuple(q for q in definition if q[2] == gap)
                predicted_new = tuple(sorted(new_maximum_occurrences(parent, gap)))
                if predicted_new != expected_new:
                    raise RuntimeError(json.dumps({"parent": parent, "gap": gap,
                                                  "expected_new": expected_new, "actual_new": predicted_new}))
                if (gap in legal_maximum_gaps(parent)) != (not expected_new):
                    raise RuntimeError("legal gap mismatch for " + repr((parent, gap)))
            digest.update(json.dumps([p, definition], separators=(",", ":")).encode("ascii") + b"\n")
        rows.append({"n": n, "avoiders": avoiders, "occurrences": occurrences_found,
                     "ordered_occurrence_stream_sha256": digest.hexdigest()})
    after = {name: file_hash(path) for name, path in sources.items()}
    if before != after:
        raise RuntimeError("source checker changed during comparison")
    return {
        "status": "PASS",
        "decision_message_id": 410,
        "sources": {name: {"path": str(path.resolve()), "sha256": before[name]} for name, path in sources.items()},
        "max_n": max_n,
        "permutations_checked": permutations_checked,
        "maximum_insertion_instances_checked": insertion_instances_checked,
        "scope": "Exact occurrence-set comparison on all S_n, 0<=n<=max_n; all maximum insertions of parents through max_n-1.",
        "representations": ["quadruples plus literal interior scan", "canonical value-boundary rectangles",
                            "nearest-greater maximum restrictions"],
        "rows": rows,
        "python": platform.python_version(),
        "elapsed_seconds": round(time.monotonic() - start, 6),
        "run_by": "literature-researcher-3",
        "full_growth_target_solved": False,
        "written_proof_review_completed": False,
        "review_scope_note": "Finite agreement across separately authored reductions; universal derivation still awaits Theo's full check.",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--lyra", type=Path, required=True)
    parser.add_argument("--theo", type=Path, required=True)
    parser.add_argument("--max-n", type=int, default=7)
    args = parser.parse_args()
    if not 0 <= args.max_n <= 8:
        parser.error("max-n must be between 0 and 8")
    print(json.dumps(compare(args.lyra, args.theo, args.max_n), indent=2))


if __name__ == "__main__":
    main()
