#!/usr/bin/env python3
"""Compare the closed table with the preceding finite relaxation."""

from __future__ import annotations

import argparse
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
import sys

sys.dont_write_bytecode = True

import universal_verify as universal


def load_finite_verifier():
    path = (
        Path(__file__).resolve().parent.parent
        / "odd_cycle_stacking_ancestry_certificates"
        / "verify.py"
    )
    spec = spec_from_file_location("finite_ancestry_verifier", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def evaluate(expr: universal.Affine, k: int, d: int) -> int:
    value = expr.p * 2**k + expr.z * 2**d + expr.c
    if value.denominator != 1:
        raise AssertionError(f"nonintegral table entry at k={k}, d={d}: {value}")
    return value.numerator


def closed_rows(k: int, vertex: int):
    parity = k % 2
    order = 2 * k + 1
    if vertex <= k - 1:
        distance = vertex
        rows = universal.left_generic_rows(parity, distance % 2)
    elif vertex == k:
        distance = k
        rows = universal.left_special_rows(parity)
    elif vertex == k + 1:
        distance = k
        rows = universal.right_middle_rows(parity)
    elif vertex == k + 2:
        distance = k - 1
        rows = universal.right_y_rows(parity)
    else:
        distance = order - vertex
        rows = universal.right_generic_rows(parity, distance % 2)
    return [
        [evaluate(entry, k, distance) for entry in row]
        for row in rows
    ]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-k", type=int, default=250)
    args = parser.parse_args()
    if args.max_k < 3:
        parser.error("--max-k must be at least 3")

    finite = load_finite_verifier()
    entries = 0
    for k in range(3, args.max_k + 1):
        exact = finite.construct_tree_table(k)
        for vertex in range(2 * k + 1):
            closed = closed_rows(k, vertex)
            if closed != exact[vertex]:
                raise AssertionError(
                    f"table mismatch at k={k}, vertex={vertex}: "
                    f"closed={closed}, relaxation={exact[vertex]}"
                )
            entries += 12
    print(f"EXACT TABLE MATCH k=3..{args.max_k} entries={entries}")


if __name__ == "__main__":
    main()
