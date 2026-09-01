#!/usr/bin/env python3
"""Exact/SAT generation and solver-free replay for 16 degree-9 completion points.

This specializes the previously published degree-10 replacement engine to the
sixteen external degree-9 centers certified in centers.json.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import os
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent
PRIOR = Path(
    os.environ.get(
        "HN_PRIOR_REPLACEMENT",
        HERE.parent / "hadwiger_nelson_parts509_degree10_replacements",
    )
)


def load_prior_module():
    path = PRIOR / "pair_replacement.py"
    spec = importlib.util.spec_from_file_location("parts509_prior_replacement", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def degree9_neighbor_sets():
    document = json.loads((HERE / "centers.json").read_text())
    result = tuple(
        tuple(row["neighbors"])
        for row in document["centers"]
        if row["existing_vertex"] is None and row["degree"] == 9
    )
    if len(result) != 16 or any(len(row) != 9 for row in result) or len(set(result)) != 16:
        raise ValueError("center manifest does not contain 16 distinct external degree-9 neighborhoods")
    return result


PRIOR_MODULE = load_prior_module()
# Load and validate the prior exact geometry before replacing its four points.
PARTS, POINTS, EDGES, DELETION_ROWS, _ = PRIOR_MODULE.load_base_data()
NEIGHBOR_SETS = degree9_neighbor_sets()
PRIOR_MODULE.MAGIC = b"HN509D91"
PRIOR_MODULE.EXPECTED_NEIGHBORS = NEIGHBOR_SETS
PRIOR_MODULE.load_base_data = lambda: (
    PARTS,
    POINTS,
    EDGES,
    DELETION_ROWS,
    NEIGHBOR_SETS,
)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    verify = subparsers.add_parser("verify", help="solver-free exact replay")
    verify.add_argument("certificate", type=Path)
    generate = subparsers.add_parser("generate", help="regenerate SAT coloring witnesses")
    generate.add_argument("output", type=Path)
    generate.add_argument("--solver", default="minisat22")
    args = parser.parse_args()
    if args.command == "verify":
        PRIOR_MODULE.command_verify(args.certificate)
    else:
        PRIOR_MODULE.command_generate(args.output, args.solver)


if __name__ == "__main__":
    main()
