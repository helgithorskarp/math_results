"""Optional independent CNF/DRAT replay of the imported E477 equality fact.

Requires python-sat==1.9.dev15 and a path to drat-trim.  All generated CNF,
proof, and log bytes are written to the explicitly supplied scratch directory.
"""

import argparse
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path
import subprocess
import time

from independent_check import PARENT_CERTIFICATE, EXPECTED_HASHES, file_hash, require, source_edges


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--checker", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    require(not args.out.exists(), "output directory already exists")
    args.out.mkdir(parents=True)
    require(file_hash(PARENT_CERTIFICATE) == EXPECTED_HASHES[PARENT_CERTIFICATE], "parent input hash")

    from pysat.solvers import Glucose3

    rows = json.loads(PARENT_CERTIFICATE.read_text())["equal"]["points"]
    edges = source_edges(rows)
    n = len(rows)

    def variable(vertex, colour):
        return 4 * vertex + colour + 1

    clauses = []
    for vertex in range(n):
        clauses.append([variable(vertex, colour) for colour in range(4)])
        clauses.extend(
            [-variable(vertex, first), -variable(vertex, second)]
            for first, second in combinations(range(4), 2)
        )
    for u, v in edges:
        clauses.extend([-variable(u, colour), -variable(v, colour)] for colour in range(4))
    clauses.extend([[variable(0, 0)], [variable(1, 1)]])

    cnf = args.out / "e477-terminals-different.cnf"
    proof = args.out / "e477-terminals-different.drat"
    log = args.out / "drat-trim.log"
    cnf.write_text(
        f"p cnf {4*n} {len(clauses)}\n"
        + "".join(" ".join(map(str, clause)) + " 0\n" for clause in clauses)
    )

    started = time.monotonic()
    with Glucose3(bootstrap_with=clauses, with_proof=True) as solver:
        require(solver.solve() is False, "contrary terminal query was not UNSAT")
        proof.write_text("\n".join(solver.get_proof()) + "\n")
    with log.open("w") as output:
        completed = subprocess.run(
            [str(args.checker.resolve()), str(cnf), str(proof)],
            stdout=output,
            stderr=subprocess.STDOUT,
            check=False,
        )
    log_text = log.read_text()
    require(completed.returncode == 0 and "s VERIFIED" in log_text, "drat-trim rejected proof")

    result = {
        "vertices": n,
        "edges": len(edges),
        "variables": 4 * n,
        "clauses": len(clauses),
        "cnf_sha256": sha256(cnf.read_bytes()).hexdigest(),
        "drat_sha256": sha256(proof.read_bytes()).hexdigest(),
        "drat_bytes": proof.stat().st_size,
        "drat_trim_verified": True,
        "seconds": time.monotonic() - started,
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
