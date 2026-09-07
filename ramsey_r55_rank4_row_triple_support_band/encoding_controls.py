#!/usr/bin/env python3
"""Small exhaustive semantic controls for the production cardinality encoder."""

from __future__ import annotations

from itertools import product
import json
from pathlib import Path
import tempfile

from joint_completion import StreamCNF


def parse_cnf(path):
    lines = path.read_text(encoding="ascii").splitlines()
    header = lines[0].split()
    variables, declared = map(int, header[2:4])
    clauses = []
    for line in lines[1:]:
        literals = list(map(int, line.split()))
        if not literals or literals[-1] != 0:
            raise RuntimeError("malformed DIMACS clause")
        clauses.append(tuple(literals[:-1]))
    if len(clauses) != declared:
        raise RuntimeError("DIMACS clause-count mismatch")
    return variables, clauses


def satisfiable_with_fixed(variables, clauses, fixed):
    assignment = dict(fixed)

    def search(current):
        current = dict(current)
        while True:
            unit = None
            for clause in clauses:
                undecided = []
                satisfied = False
                for literal in clause:
                    value = current.get(abs(literal))
                    if value is None:
                        undecided.append(literal)
                    elif value == (literal > 0):
                        satisfied = True
                        break
                if satisfied:
                    continue
                if not undecided:
                    return False
                if len(undecided) == 1:
                    unit = undecided[0]
                    break
            if unit is None:
                break
            variable, value = abs(unit), unit > 0
            if variable in current and current[variable] != value:
                return False
            current[variable] = value
        for variable in range(1, variables + 1):
            if variable not in current:
                left = dict(current)
                left[variable] = False
                if search(left):
                    return True
                right = dict(current)
                right[variable] = True
                return search(right)
        return True

    return search(assignment)


def encoded(kind, n, bound, gated=False, repeated=None):
    with tempfile.TemporaryDirectory() as temporary:
        temporary = Path(temporary)
        cnf = StreamCNF(temporary / "body")
        primary = [cnf.new_var() for _ in range(n)]
        gate = cnf.new_var() if gated else None
        literals = primary if repeated is None else [primary[i] for i in repeated]
        getattr(cnf, kind)(literals, bound, gate)
        output = temporary / "test.cnf"
        cnf.finish(output)
        variables, clauses = parse_cnf(output)
    return primary, gate, variables, clauses


def main():
    assignments_checked = 0
    encodings_checked = 0
    for n in range(1, 6):
        for kind in ("at_most", "at_least"):
            for bound in range(0, n + 1):
                for gated in (False, True):
                    primary, gate, variables, clauses = encoded(kind, n, bound, gated)
                    encodings_checked += 1
                    for bits in product((False, True), repeat=n):
                        gate_values = (False, True) if gated else (None,)
                        for gate_value in gate_values:
                            fixed = dict(zip(primary, bits))
                            if gate is not None:
                                fixed[gate] = gate_value
                            count = sum(bits)
                            predicate = count <= bound if kind == "at_most" else count >= bound
                            expected = predicate or (gated and not gate_value)
                            observed = satisfiable_with_fixed(variables, clauses, fixed)
                            if observed != expected:
                                raise RuntimeError((kind, n, bound, gated, bits,
                                                    gate_value, expected, observed))
                            assignments_checked += 1

    # Repeated literals encode repeated physical edges sharing one Boolean
    # color.  Their multiplicities must still count separately.
    pattern = [0, 0, 1, 1, 1, 2]
    duplicate_assignments = 0
    for kind in ("at_most", "at_least"):
        for bound in range(0, len(pattern) + 1):
            primary, gate, variables, clauses = encoded(
                kind, 3, bound, gated=True, repeated=pattern
            )
            for bits in product((False, True), repeat=3):
                for gate_value in (False, True):
                    fixed = dict(zip(primary, bits))
                    fixed[gate] = gate_value
                    count = sum(bits[index] for index in pattern)
                    predicate = count <= bound if kind == "at_most" else count >= bound
                    expected = predicate or not gate_value
                    if satisfiable_with_fixed(variables, clauses, fixed) != expected:
                        raise RuntimeError("repeated-literal cardinality failure")
                    duplicate_assignments += 1

    print(json.dumps({
        "status": "VERIFIED_CARDINALITY_ENCODING_CONTROLS",
        "encodings_checked": encodings_checked,
        "assignments_checked": assignments_checked,
        "duplicate_assignments_checked": duplicate_assignments,
    }, sort_keys=True))


if __name__ == "__main__":
    main()
