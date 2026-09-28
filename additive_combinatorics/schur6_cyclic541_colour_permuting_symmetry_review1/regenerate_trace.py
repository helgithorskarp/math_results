#!/usr/bin/env python3
"""Regenerate the target CNF and Glucose proof for an external checker."""

import argparse
import hashlib
from pathlib import Path
import sys

SOURCE = Path(__file__).resolve().parent.parent / "schur6_cyclic541_colour_permuting_symmetry"
sys.path.insert(0, str(SOURCE))
from encode import dimacs, encode  # noqa: E402
from pysat.solvers import Solver  # noqa: E402


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("cnf", type=Path)
    parser.add_argument("proof", type=Path)
    args = parser.parse_args()
    clauses, reps, _ = encode()
    cnf = dimacs(clauses, 6 * len(reps))
    with Solver(name="glucose3", bootstrap_with=clauses, with_proof=True) as solver:
        if solver.solve() is not False:
            raise ValueError("the target CNF was not refuted")
        lines = solver.get_proof()
    if lines is None:
        raise ValueError("no proof trace")
    proof = ("\n".join(lines) + "\n").encode("ascii")
    args.cnf.write_bytes(cnf)
    args.proof.write_bytes(proof)
    print("CNF SHA-256", hashlib.sha256(cnf).hexdigest())
    print("proof SHA-256", hashlib.sha256(proof).hexdigest())
    print("proof records", len(lines))


if __name__ == "__main__":
    main()
