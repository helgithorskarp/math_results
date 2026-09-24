#!/usr/bin/env python3
"""An alternative direct Horn/PB proof of the twelve-block positive witness.

Regenerates the CNF, obtains a DRAT proof from Glucose, converts it to text
LRAT using DRAT-trim, and checks every RUP addition using strict_rup.py.
Bulky CNF/DRAT/LRAT files belong in the explicitly supplied output directory.
"""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import time

from pysat.formula import CNF
from pysat.pb import PBEnc, EncType
from pysat.solvers import Glucose4
from strict_rup import check


def encode():
    n = 8
    N = 1 << n
    weights = [6, 6, 4, 3, 3, 3, 4, 4]
    generators = [15, 23, 39, 71, 135, 75, 139, 83, 147, 99, 163, 195]
    cnf = CNF()
    for a in range(N):
        for b in range(a + 1, N):
            c = a | b
            if c != a and c != b:
                cnf.append([-a - 1, -b - 1, c + 1])
    uc = len(cnf.clauses)
    for a in generators:
        for b in range(N):
            c = a | b
            if c != b:
                cnf.append([-b - 1, c + 1])
    stability = len(cnf.clauses) - uc
    q = [2 * sum(weights[i] for i in range(n) if s >> i & 1) - sum(weights)
         for s in range(N)]
    negative = sum(-v for v in q if v < 0)
    pb = PBEnc.atmost(lits=[s + 1 if v > 0 else -s - 1 for s, v in enumerate(q) if v],
                      weights=[abs(v) for v in q if v], bound=negative - 1,
                      top_id=N, encoding=EncType.bdd)
    cnf.extend(pb.clauses)
    return cnf, {"variables": cnf.nv, "clauses": len(cnf.clauses),
                 "union_closure_clauses": uc, "stability_clauses": stability,
                 "pb_clauses": len(pb.clauses), "pb_bound": negative - 1}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--output", type=Path, required=True)
    ap.add_argument("--drat-trim", type=Path, required=True)
    args = ap.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    cnf_path = args.output / "lex_positive.cnf"
    drat = args.output / "lex_positive.drat"
    lrat = args.output / "lex_positive.lrat"
    cnf, result = encode()
    cnf.to_file(str(cnf_path))
    started = time.monotonic()
    with Glucose4(bootstrap_with=cnf, with_proof=True) as solver:
        if solver.solve():
            raise ValueError("Found a share-negative admissible family")
        proof = solver.get_proof()
        drat.write_text("\n".join(proof) + "\n")
        result.update(solver_stats=solver.accum_stats(), drat_lines=len(proof))
    result["solver_seconds"] = time.monotonic() - started
    with (args.output / "drat-trim.log").open("w") as log:
        subprocess.run([str(args.drat_trim.resolve()), str(cnf_path), str(drat), "-L", str(lrat)],
                       stdout=log, stderr=subprocess.STDOUT, check=True)
    result["strict_rup"] = check(cnf_path, lrat)
    result["files"] = {p.name: {"bytes": p.stat().st_size,
                                "sha256": hashlib.sha256(p.read_bytes()).hexdigest()}
                       for p in (cnf_path, drat, lrat)}
    (args.output / "sat_result.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
