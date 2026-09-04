#!/usr/bin/env python3
"""Independent CNF audit of the load-bearing 39-transversal claim.

This checker deliberately does not import either published Parts verifier.  It
reads the pinned triple certificate, extracts its deletion hypergraph, and
encodes the question "is there a hitting set of size at most 38?" as DIMACS.
The optional ``--pairs-only`` flag keeps only the two-element deletion sets;
if that smaller formula is UNSAT, it gives a strictly stronger and simpler
lower-bound certificate than using all 330 deletion sets.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


EXPECTED_CERTIFICATE_SHA256 = (
    "46ee849ead7b3601e887cee2aa2d5a1d02d12cf083a673c9890e2d2552bef795"
)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


class Cnf:
    def __init__(self, primary_variables: int) -> None:
        self.variables = primary_variables
        self.clauses: list[tuple[int, ...]] = []

    def new_variable(self) -> int:
        self.variables += 1
        return self.variables

    def add(self, *literals: int) -> None:
        if not literals or any(literal == 0 for literal in literals):
            raise ValueError("a DIMACS clause must contain nonzero literals")
        self.clauses.append(tuple(literals))

    def dimacs(self) -> bytes:
        lines = [f"p cnf {self.variables} {len(self.clauses)}"]
        lines.extend(" ".join(map(str, clause)) + " 0" for clause in self.clauses)
        return ("\n".join(lines) + "\n").encode("ascii")


def add_at_most(cnf: Cnf, variables: list[int], bound: int) -> None:
    """Add the Sinz sequential-counter encoding of sum(variables) <= bound."""
    n = len(variables)
    if bound < 0:
        cnf.add(1)
        cnf.add(-1)
        return
    if bound >= n:
        return
    if bound == 0:
        for variable in variables:
            cnf.add(-variable)
        return

    # s[i,j] means that at least j of x_1,...,x_i are true.  Only states
    # 1 <= j <= min(i,bound), 1 <= i < n, are needed.
    state: dict[tuple[int, int], int] = {}
    for i in range(1, n):
        for j in range(1, min(i, bound) + 1):
            state[i, j] = cnf.new_variable()

    for i in range(1, n):
        x_i = variables[i - 1]
        cnf.add(-x_i, state[i, 1])
        if i > 1:
            cnf.add(-state[i - 1, 1], state[i, 1])
        for j in range(2, min(i, bound) + 1):
            cnf.add(-x_i, -state[i - 1, j - 1], state[i, j])
            if j <= i - 1:
                cnf.add(-state[i - 1, j], state[i, j])

    # Selecting x_i when the first i-1 positions already contain bound
    # selected vertices would overflow the counter.
    for i in range(bound + 1, n + 1):
        cnf.add(-variables[i - 1], -state[i - 1, bound])


def counter_self_test() -> None:
    """Exhaustively test the encoding, including existential auxiliary bits."""
    for n in range(1, 6):
        for bound in range(n + 1):
            cnf = Cnf(n)
            add_at_most(cnf, list(range(1, n + 1)), bound)
            auxiliary_count = cnf.variables - n
            for primary_mask in range(1 << n):
                found = False
                for auxiliary_mask in range(1 << auxiliary_count):
                    assignment = {
                        variable: bool(primary_mask & (1 << (variable - 1)))
                        for variable in range(1, n + 1)
                    }
                    assignment.update({
                        n + offset + 1: bool(auxiliary_mask & (1 << offset))
                        for offset in range(auxiliary_count)
                    })
                    if all(any(assignment[abs(literal)] == (literal > 0) for literal in clause)
                           for clause in cnf.clauses):
                        found = True
                        break
                if found != (primary_mask.bit_count() <= bound):
                    raise AssertionError(
                        f"sequential counter failed n={n}, bound={bound}, mask={primary_mask}"
                    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("certificate", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--bound", type=int, default=38)
    parser.add_argument("--pairs-only", action="store_true")
    args = parser.parse_args()

    counter_self_test()

    raw = args.certificate.read_bytes()
    digest = sha256_bytes(raw)
    if digest != EXPECTED_CERTIFICATE_SHA256:
        raise ValueError(f"unexpected triple certificate SHA-256: {digest}")
    certificate = json.loads(raw)
    free = certificate["free_vertices"]
    if free != sorted(set(free)) or len(free) != 63:
        raise AssertionError("expected 63 distinct sorted free vertices")
    free_index = {vertex: index + 1 for index, vertex in enumerate(free)}

    all_sets: list[tuple[int, ...]] = []
    for row in certificate["killing_sets"]:
        deleted = tuple(row["deleted"])
        if deleted != tuple(sorted(set(deleted))) or not set(deleted) <= set(free):
            raise AssertionError("malformed deletion set")
        all_sets.append(deleted)
    if len(all_sets) != 330 or len(set(all_sets)) != 330:
        raise AssertionError("expected 330 distinct deletion sets")

    selected_sets = [edge for edge in all_sets if len(edge) == 2] if args.pairs_only else all_sets
    cnf = Cnf(len(free))
    for edge in selected_sets:
        cnf.add(*(free_index[vertex] for vertex in edge))
    add_at_most(cnf, list(range(1, len(free) + 1)), args.bound)
    dimacs = cnf.dimacs()
    args.output.write_bytes(dimacs)

    summary = {
        "all_deletion_sets": len(all_sets),
        "bound": args.bound,
        "certificate_sha256": digest,
        "clauses": len(cnf.clauses),
        "cnf_sha256": sha256_bytes(dimacs),
        "counter_self_test": True,
        "pairs_only": args.pairs_only,
        "selected_deletion_sets": len(selected_sets),
        "universe": len(free),
        "variables": cnf.variables,
    }
    print(json.dumps(summary, sort_keys=True))


if __name__ == "__main__":
    main()
