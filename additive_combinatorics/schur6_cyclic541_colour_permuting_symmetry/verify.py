#!/usr/bin/env python3
"""Regenerate and independently check the order-20 exclusion certificate."""
import hashlib
import json
from pathlib import Path

import audit
import checker_controls
from encode import dimacs, encode, require
from rup import RUP


def run():
    clauses, representatives, _ = encode()
    direct, _, _, _, pairs = audit.literal_encoding(541, 497)
    require(clauses == direct, "full modular CNF disagrees with reduced encoding")
    variables = 6 * len(representatives)
    data = dimacs(clauses, variables)
    # The solver is a certificate producer, not the UNSAT trust boundary.
    from pysat.solvers import Solver
    with Solver(name="glucose3", bootstrap_with=clauses, with_proof=True) as solver:
        require(solver.solve() is False, "expected UNSAT certificate was not produced")
        proof = solver.get_proof()
    require(proof is not None, "solver supplied no certificate")
    checked = RUP(variables, clauses).check(proof)
    raw = ("\n".join(proof) + "\n").encode("ascii")
    return {
        "status": "VERIFIED_ORDER20_EXCLUSION",
        "modulus": 541, "generator": 497, "cycle_lengths": [5, 1],
        "orbits": len(representatives), "variables": variables, "clauses": len(clauses),
        "literal_modular_pairs": pairs,
        "cnf_sha256": hashlib.sha256(data).hexdigest(),
        "proof_sha256": hashlib.sha256(raw).hexdigest(),
        "proof_bytes": len(raw), "proof_lines": len(proof), "rup": checked,
        "small_action_truth_tables": audit.small_truth_tables(encode),
        "checker_controls": checker_controls.controls(),
    }


if __name__ == "__main__":
    report = run()
    expected = Path(__file__).with_name("expected.json")
    require(report == json.loads(expected.read_text()), "recorded evidence changed")
    print(json.dumps(report, sort_keys=True, indent=2))
