"""Exhaustive finite sanity checks; the general theorem is proved in proof.md."""
import argparse
import hashlib
import itertools
import json
import time

from circuit import Circuit
from topology import (cubical_counts, flood_counts, local_counts,
                      topology_constraint)


def validate_topology(side):
    positions = list(itertools.product(range(side), repeat=2))
    digest = hashlib.sha256()
    connected = hole_free = discs = 0
    for mask in range(1 << len(positions)):
        cells = {p for i, p in enumerate(positions) if (mask >> i) & 1}
        f, a, b, d = local_counts(cells)
        v, e, faces = cubical_counts(cells)
        components, holes = flood_counts(cells)
        if not f - a + b - d == v - e + faces == components - holes:
            raise AssertionError((mask, (f, a, b, d), (v, e, faces), components, holes))
        connected += components == 1
        hole_free += components == 1 and holes == 0
        discs += components == 1 and holes == 0 and d == 0
        digest.update(f"{mask}:{f},{a},{b},{d}:{components},{holes}\n".encode())
    return {"side": side, "assignments": 1 << len(positions),
            "connected": connected, "connected_hole_free": hole_free,
            "discs": discs, "sha256": digest.hexdigest()}


def validate_circuit():
    checks = 0
    for size in range(9):
        for target in range(-1, size + 2):
            circuit = Circuit()
            xs = [circuit.new() for _ in range(size)]
            circuit.equal_count(xs, target)
            for values in itertools.product((False, True), repeat=size):
                assert circuit.evaluate(dict(zip(xs, values))) == (sum(values) == target)
                checks += 1
    # Repeated and negated literals count with multiplicity.
    for target in range(7):
        circuit = Circuit()
        x, y = circuit.new(), circuit.new()
        circuit.equal_count([x, x, -x, y, 1, -1], target)
        for a, b in itertools.product((False, True), repeat=2):
            assert circuit.evaluate({x: a, y: b}) == (a + b + 2 == target)
            checks += 1
    return checks


def validate_topology_cnf(side=3):
    circuits, variables = {}, {}
    for strict in (False, True):
        circuit = Circuit()
        occupancy = {p: circuit.new() for p in itertools.product(range(side), repeat=2)}
        topology_constraint(circuit, occupancy, strict_disc=strict)
        circuits[strict], variables[strict] = circuit, occupancy
    for mask in range(1 << (side * side)):
        cells = {p for i, p in enumerate(variables[False]) if (mask >> i) & 1}
        components, holes = flood_counts(cells)
        d = local_counts(cells)[3]
        for strict in (False, True):
            circuit, occupancy = circuits[strict], variables[strict]
            expected = components - holes == 1 and (not strict or d == 0)
            actual = circuit.evaluate({v: p in cells for p, v in occupancy.items()})
            assert actual == expected, (mask, strict, components, holes, d)
    return {str(strict): {"variables": c.nv, "clauses": len(c.clauses)}
            for strict, c in circuits.items()}


def validate_sat_projection():
    """Check existential auxiliary-variable projection with actual CNF solving."""
    from pysat.solvers import Solver
    from pysat import __version__
    checks = 0
    for strict in (False, True):
        circuit = Circuit()
        occupancy = {p: circuit.new() for p in itertools.product(range(3), repeat=2)}
        topology_constraint(circuit, occupancy, strict)
        with Solver(name="glucose4", bootstrap_with=circuit.clauses) as solver:
            for mask in range(512):
                cells = {p for i, p in enumerate(occupancy) if (mask >> i) & 1}
                components, holes = flood_counts(cells)
                d = local_counts(cells)[3]
                expected = components - holes == 1 and (not strict or d == 0)
                assumptions = [v if p in cells else -v for p, v in occupancy.items()]
                assert solver.solve(assumptions=assumptions) == expected, (strict, mask)
                checks += 1
    return {"checks": checks, "python_sat": __version__, "solver": "glucose4"}


def validate_rup_propagation():
    from check_rup import Propagator
    # Every subset of every non-tautological clause on two variables, and every
    # consistent partial assignment.  Compare to a separate rescan propagator.
    possible = [tuple(sign * (i + 1) for i, sign in enumerate(signs) if sign)
                for signs in itertools.product((-1, 0, 1), repeat=2)]
    assumptions = possible
    checks = 0
    for mask in range(1 << len(possible)):
        clauses = [c for i, c in enumerate(possible) if (mask >> i) & 1]
        engine = Propagator(2, clauses)
        for fixed in assumptions:
            values = {abs(x): x > 0 for x in fixed}
            conflict = False
            while True:
                changed = False
                for clause in clauses:
                    if any(abs(x) in values and values[abs(x)] == (x > 0) for x in clause):
                        continue
                    remaining = [x for x in clause if abs(x) not in values]
                    if not remaining:
                        conflict = True
                        break
                    if len(remaining) == 1:
                        x = remaining[0]
                        values[abs(x)] = x > 0
                        changed = True
                if conflict or not changed:
                    break
            assert engine.conflict(fixed) == conflict, (mask, fixed)
            checks += 1
    return checks


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--side", type=int, default=4, choices=range(1, 5))
    parser.add_argument("--sat", action="store_true")
    args = parser.parse_args()
    start = time.monotonic()
    result = {"topology": validate_topology(args.side),
              "arithmetic_assignment_checks": validate_circuit(),
              "rup_propagation_checks": validate_rup_propagation(),
              "topology_cnf_3x3": validate_topology_cnf(),
              "elapsed_seconds": round(time.monotonic() - start, 3)}
    if args.sat:
        result["sat_projection"] = validate_sat_projection()
    print(json.dumps(result, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
