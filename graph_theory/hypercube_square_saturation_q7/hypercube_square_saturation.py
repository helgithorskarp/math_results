#!/usr/bin/env python3
"""Generate and verify SAT instances for square-saturated hypercube subgraphs.

The host graph Q_d has vertices 0,...,2^d-1.  An edge is represented by
``(u, i)``, where bit i of u is zero and the other endpoint is ``u ^ (1<<i)``.

The CNF has one primary variable per edge.  It enforces:

* no square has all four edges; and
* every omitted edge is the missing edge of a square whose other three edges
  are present.

Optional Sinz sequential-counter clauses enforce an upper bound on the number
of selected edges.  Auxiliary witness variables and counter variables are not
part of the mathematical certificate; ``verify`` checks a decoded primary
assignment directly from the definitions.
"""

from __future__ import annotations

import argparse
import functools
import json
import random
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Sequence


Edge = tuple[int, int]


def edges(d: int) -> list[Edge]:
    return [(u, i) for u in range(1 << d) for i in range(d) if not (u >> i) & 1]


def edge_key(u: int, v: int) -> Edge:
    delta = u ^ v
    if delta == 0 or delta & (delta - 1):
        raise ValueError(f"{u}, {v} are not adjacent hypercube vertices")
    i = delta.bit_length() - 1
    return (u if not (u >> i) & 1 else v, i)


def squares(d: int) -> list[tuple[Edge, Edge, Edge, Edge]]:
    result: list[tuple[Edge, Edge, Edge, Edge]] = []
    for u in range(1 << d):
        for i in range(d):
            if (u >> i) & 1:
                continue
            for j in range(i + 1, d):
                if (u >> j) & 1:
                    continue
                result.append(
                    (
                        edge_key(u, u ^ (1 << i)),
                        edge_key(u, u ^ (1 << j)),
                        edge_key(u ^ (1 << i), u ^ (1 << i) ^ (1 << j)),
                        edge_key(u ^ (1 << j), u ^ (1 << i) ^ (1 << j)),
                    )
                )
    return result


@dataclass
class CNF:
    next_var: int = 1
    clauses: list[list[int]] | None = None

    def __post_init__(self) -> None:
        if self.clauses is None:
            self.clauses = []

    def new_var(self) -> int:
        answer = self.next_var
        self.next_var += 1
        return answer

    def add(self, *literals: int) -> None:
        assert self.clauses is not None
        self.clauses.append(list(literals))

    @property
    def variables(self) -> int:
        return self.next_var - 1


def add_at_most(cnf: CNF, variables: Sequence[int], bound: int) -> None:
    """Add the Sinz sequential-counter encoding of sum(variables) <= bound."""
    n = len(variables)
    if bound < 0:
        cnf.add()
        return
    if bound >= n:
        return
    if bound == 0:
        for variable in variables:
            cnf.add(-variable)
        return

    # s[i][j] says that among x[0],...,x[i], at least j+1 are true.
    # Only rows 0,...,n-2 are required by the sequential encoding.
    s = [[cnf.new_var() for _ in range(bound)] for _ in range(n - 1)]
    for i in range(n - 1):
        cnf.add(-variables[i], s[i][0])
    for i in range(1, n - 1):
        for j in range(bound):
            cnf.add(-s[i - 1][j], s[i][j])
        for j in range(1, bound):
            cnf.add(-variables[i], -s[i - 1][j - 1], s[i][j])
    for i in range(1, n):
        cnf.add(-variables[i], -s[i - 1][bound - 1])


def build_cnf(d: int, bound: int | None, fix_edge: bool = True) -> tuple[CNF, list[Edge]]:
    all_edges = edges(d)
    all_squares = squares(d)
    cnf = CNF()
    edge_var = {edge: cnf.new_var() for edge in all_edges}

    incident: dict[Edge, list[tuple[Edge, Edge, Edge]]] = {edge: [] for edge in all_edges}
    for square in all_squares:
        cnf.add(*(-edge_var[edge] for edge in square))
        for edge in square:
            incident[edge].append(tuple(other for other in square if other != edge))  # type: ignore[arg-type]

    for edge in all_edges:
        witnesses: list[int] = []
        for other_edges in incident[edge]:
            witness = cnf.new_var()
            witnesses.append(witness)
            for other in other_edges:
                cnf.add(-witness, edge_var[other])
        cnf.add(edge_var[edge], *witnesses)

    if bound is not None:
        add_at_most(cnf, [edge_var[edge] for edge in all_edges], bound)
    if fix_edge:
        # Every saturated subgraph for d >= 2 contains an edge.  Edge transitivity
        # therefore makes this a sound isomorph rejection constraint.
        cnf.add(edge_var[(0, 0)])
    return cnf, all_edges


def write_dimacs(path: Path, cnf: CNF, metadata: dict[str, object]) -> None:
    assert cnf.clauses is not None
    with path.open("w", encoding="ascii") as handle:
        handle.write("c " + json.dumps(metadata, sort_keys=True) + "\n")
        handle.write(f"p cnf {cnf.variables} {len(cnf.clauses)}\n")
        for clause in cnf.clauses:
            handle.write(" ".join(map(str, clause)) + " 0\n")


def parse_solver_model(text: str, primary_count: int) -> list[bool]:
    values: dict[int, bool] = {}
    for line in text.splitlines():
        if line.startswith("v "):
            for token in line.split()[1:]:
                literal = int(token)
                if literal:
                    values[abs(literal)] = literal > 0
    missing = [variable for variable in range(1, primary_count + 1) if variable not in values]
    if missing:
        raise ValueError(f"solver model omits primary variables: {missing[:10]}")
    return [values[variable] for variable in range(1, primary_count + 1)]


def verify_selected(d: int, selected: Iterable[Edge]) -> dict[str, int]:
    selected_set = set(selected)
    all_edges = edges(d)
    all_squares = squares(d)
    if not selected_set <= set(all_edges):
        raise ValueError("certificate contains an edge outside Q_d")

    completed = [square for square in all_squares if all(edge in selected_set for edge in square)]
    if completed:
        raise ValueError(f"certificate contains a square: {completed[0]}")

    witnesses = 0
    for edge in all_edges:
        if edge in selected_set:
            continue
        if not any(edge in square and sum(other in selected_set for other in square) == 3 for square in all_squares):
            raise ValueError(f"omitted edge has no saturation witness: {edge}")
        witnesses += 1
    return {
        "dimension": d,
        "vertices": 1 << d,
        "host_edges": len(all_edges),
        "squares": len(all_squares),
        "selected_edges": len(selected_set),
        "omitted_edges_with_witness": witnesses,
    }


def write_certificate(path: Path, d: int, selected: Sequence[Edge]) -> None:
    payload = {
        "dimension": d,
        "edge_encoding": "[lower_endpoint, changed_zero_bit]",
        "selected_edges": [list(edge) for edge in selected],
    }
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def read_certificate(path: Path) -> tuple[int, list[Edge]]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    d = int(payload["dimension"])
    if "selected_edges" in payload:
        return d, [tuple(map(int, edge)) for edge in payload["selected_edges"]]
    representatives = [tuple(map(int, edge)) for edge in payload["selected_orbit_representatives"]]
    translations = translation_code(d, str(payload["translation_code"]))
    selected = {
        edge_key(
            representative[0] ^ translation,
            (representative[0] ^ (1 << representative[1])) ^ translation,
        )
        for representative in representatives
        for translation in translations
    }
    return d, sorted(selected)


def translation_code(d: int, kind: str) -> set[int]:
    if d != 7:
        raise ValueError(f"code {kind!r} is currently defined only in dimension 7")
    if kind == "hamming7":
        return {
            u
            for u in range(1 << 7)
            if not functools.reduce(int.__xor__, (i + 1 for i in range(7) if (u >> i) & 1), 0)
        }
    elif kind == "simplex7":
        return {sum(((a & (i + 1)).bit_count() & 1) << i for i in range(7)) for a in range(8)}
    raise ValueError(f"unknown code {kind!r}")


def initial_edges(d: int, kind: str) -> set[Edge]:
    if kind == "empty":
        return set()
    centers = translation_code(d, kind)
    return {
        edge_key(u, u ^ (1 << i))
        for u in centers
        for i in range(d)
    }


def edge_orbits(d: int, code_kind: str) -> tuple[list[list[Edge]], dict[Edge, int]]:
    translations = translation_code(d, code_kind)
    unassigned = set(edges(d))
    orbits: list[list[Edge]] = []
    edge_to_orbit: dict[Edge, int] = {}
    while unassigned:
        representative = min(unassigned)
        orbit = sorted(
            {
                edge_key(representative[0] ^ translation, (representative[0] ^ (1 << representative[1])) ^ translation)
                for translation in translations
            }
        )
        orbit_index = len(orbits)
        orbits.append(orbit)
        for edge in orbit:
            if edge not in unassigned:
                raise AssertionError("translation orbits overlap")
            unassigned.remove(edge)
            edge_to_orbit[edge] = orbit_index
    return orbits, edge_to_orbit


def build_orbit_cnf(d: int, code_kind: str) -> tuple[CNF, list[list[Edge]]]:
    """CNF for subgraphs invariant under translations by a binary code."""
    orbits, edge_to_orbit = edge_orbits(d, code_kind)
    cnf = CNF()
    orbit_var = [cnf.new_var() for _ in orbits]
    all_squares = squares(d)
    square_set = {frozenset(square) for square in all_squares}

    square_clauses: set[tuple[int, ...]] = set()
    for square in all_squares:
        clause = tuple(sorted({-orbit_var[edge_to_orbit[edge]] for edge in square}))
        square_clauses.add(clause)
    for clause in sorted(square_clauses):
        cnf.add(*clause)

    for orbit_index, orbit in enumerate(orbits):
        representative = orbit[0]
        incident = [square for square in all_squares if representative in square]
        if len(incident) != d - 1:
            raise AssertionError("wrong number of incident squares")
        witnesses = []
        for square in incident:
            witness = cnf.new_var()
            witnesses.append(witness)
            for other_orbit in {edge_to_orbit[edge] for edge in square if edge != representative}:
                cnf.add(-witness, orbit_var[other_orbit])
        cnf.add(orbit_var[orbit_index], *witnesses)

    # Assert that orbit translation really preserves the square family.
    translations = translation_code(d, code_kind)
    for square in all_squares:
        for translation in translations:
            translated = frozenset(
                edge_key(edge[0] ^ translation, (edge[0] ^ (1 << edge[1])) ^ translation) for edge in square
            )
            if translated not in square_set:
                raise AssertionError("translation failed to preserve squares")
    return cnf, orbits


def optimize_orbits(args: argparse.Namespace) -> int:
    try:
        from pysat.examples.rc2 import RC2
        from pysat.formula import WCNF
    except ImportError as error:
        raise RuntimeError("orbit-optimize requires python-sat") from error
    cnf, orbits = build_orbit_cnf(args.dimension, args.code)
    weighted = WCNF()
    for clause in cnf.clauses or []:
        weighted.append(clause)
    for variable, orbit in enumerate(orbits, 1):
        weighted.append([-variable], weight=len(orbit))
    with RC2(weighted, solver=args.backend, adapt=True, exhaust=True, minz=True, trim=5, verbose=args.verbose) as optimizer:
        literals = optimizer.compute()
        if literals is None:
            raise RuntimeError("orbit-invariant hard constraints are unsatisfiable")
        positive = {literal for literal in literals if literal > 0}
        selected = [edge for variable, orbit in enumerate(orbits, 1) if variable in positive for edge in orbit]
        summary = verify_selected(args.dimension, selected)
        if optimizer.cost != len(selected):
            raise AssertionError("weighted orbit objective disagrees with decoded edge count")
        write_certificate(Path(args.certificate), args.dimension, selected)
        print(
            json.dumps(
                summary
                | {
                    "translation_code": args.code,
                    "translation_group_order": len(translation_code(args.dimension, args.code)),
                    "edge_orbits": len(orbits),
                    "maxsat_cost": optimizer.cost,
                },
                indent=2,
                sort_keys=True,
            )
        )
    return 0


def greedy(
    d: int,
    seed: int,
    trials: int,
    seed_kind: str = "empty",
    initial: Iterable[Edge] | None = None,
    drop: int = 0,
) -> list[Edge]:
    rng = random.Random(seed)
    all_edges = edges(d)
    all_squares = squares(d)
    edge_squares: dict[Edge, list[tuple[Edge, Edge, Edge, Edge]]] = {edge: [] for edge in all_edges}
    for square in all_squares:
        for edge in square:
            edge_squares[edge].append(square)

    base = set(initial) if initial is not None else initial_edges(d, seed_kind)
    # Minimum distance at least three between the code centers ensures that
    # their incident-edge union is square-free; check this independently.
    if any(all(edge in base for edge in square) for square in all_squares):
        raise ValueError(f"seed construction {seed_kind!r} already contains a square")
    best = all_edges
    for _ in range(trials):
        order = all_edges.copy()
        rng.shuffle(order)
        selected = set(base)
        if drop:
            selected.difference_update(rng.sample(sorted(selected), min(drop, len(selected))))
        for edge in order:
            if edge in selected:
                continue
            if not any(all(other == edge or other in selected for other in square) for square in edge_squares[edge]):
                selected.add(edge)
        if len(selected) < len(best):
            best = sorted(selected)
            print(f"c greedy incumbent {len(best)}", file=sys.stderr)
    verify_selected(d, best)
    return best


def solve(args: argparse.Namespace) -> int:
    cnf_path = Path(args.cnf)
    proof_path = Path(args.proof) if args.proof else None
    certificate_path = Path(args.certificate) if args.certificate else None
    cnf, all_edges = build_cnf(args.dimension, args.bound, not args.no_fix_edge)
    write_dimacs(
        cnf_path,
        cnf,
        {"dimension": args.dimension, "edge_bound": args.bound, "primary_variables": len(all_edges)},
    )
    command = [args.solver, *args.solver_arg]
    if proof_path is not None:
        # CaDiCaL accepts the proof as the second positional file argument.
        # Text DRAT is larger but interoperates directly with drat-trim.
        command.append("--no-binary")
    command.append(str(cnf_path))
    if proof_path is not None:
        command.append(str(proof_path))
    completed = subprocess.run(command, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    sys.stdout.write(completed.stdout)
    status_match = re.search(r"^s (SATISFIABLE|UNSATISFIABLE|UNKNOWN)$", completed.stdout, re.MULTILINE)
    if not status_match:
        raise RuntimeError(f"could not parse solver status (exit {completed.returncode})")
    status = status_match.group(1)
    if status == "SATISFIABLE":
        model = parse_solver_model(completed.stdout, len(all_edges))
        selected = [edge for edge, value in zip(all_edges, model, strict=True) if value]
        summary = verify_selected(args.dimension, selected)
        print("c verified " + json.dumps(summary, sort_keys=True))
        if args.bound is not None and len(selected) > args.bound:
            raise AssertionError("decoded model violates requested edge bound")
        if certificate_path is not None:
            write_certificate(certificate_path, args.dimension, selected)
        return 10
    if status == "UNSATISFIABLE":
        return 20
    return 0


def optimize(args: argparse.Namespace) -> int:
    """Minimize selected primary edges with PySAT's core-guided RC2 MaxSAT."""
    try:
        from pysat.examples.rc2 import RC2
        from pysat.formula import WCNF
    except ImportError as error:
        raise RuntimeError("the optional optimize command requires python-sat") from error

    cnf, all_edges = build_cnf(args.dimension, None, not args.no_fix_edge)
    weighted = WCNF()
    for clause in cnf.clauses or []:
        weighted.append(clause)
    for variable in range(1, len(all_edges) + 1):
        weighted.append([-variable], weight=1)

    with RC2(
        weighted,
        solver=args.backend,
        adapt=True,
        exhaust=True,
        minz=True,
        trim=5,
        verbose=args.verbose,
    ) as optimizer:
        model_literals = optimizer.compute()
        if model_literals is None:
            raise RuntimeError("hard square-saturation constraints are unexpectedly unsatisfiable")
        model = {abs(literal): literal > 0 for literal in model_literals}
        selected = [edge for variable, edge in enumerate(all_edges, 1) if model.get(variable, False)]
        summary = verify_selected(args.dimension, selected)
        if optimizer.cost != len(selected):
            raise AssertionError(f"RC2 cost {optimizer.cost} differs from decoded size {len(selected)}")
        write_certificate(Path(args.certificate), args.dimension, selected)
        print(json.dumps(summary | {"maxsat_cost": optimizer.cost}, indent=2, sort_keys=True))
    return 0


def optimize_cp_sat(args: argparse.Namespace) -> int:
    """Optimize with OR-Tools CP-SAT, reporting both incumbent and lower bound."""
    try:
        from ortools.sat.python import cp_model
    except ImportError as error:
        raise RuntimeError("the optional cp-optimize command requires ortools") from error

    d = args.dimension
    all_edges = edges(d)
    all_squares = squares(d)
    model = cp_model.CpModel()
    edge_var = {edge: model.new_bool_var(f"e_{edge[0]}_{edge[1]}") for edge in all_edges}
    incident: dict[Edge, list[tuple[Edge, Edge, Edge]]] = {edge: [] for edge in all_edges}
    for square in all_squares:
        model.add(sum(edge_var[edge] for edge in square) <= 3)
        for edge in square:
            incident[edge].append(tuple(other for other in square if other != edge))  # type: ignore[arg-type]
    for edge in all_edges:
        witness_vars = []
        for witness_index, others in enumerate(incident[edge]):
            witness = model.new_bool_var(f"w_{edge[0]}_{edge[1]}_{witness_index}")
            witness_vars.append(witness)
            for other in others:
                model.add(witness <= edge_var[other])
        model.add(edge_var[edge] + sum(witness_vars) >= 1)
    if not args.no_fix_edge:
        model.add(edge_var[(0, 0)] == 1)
    if args.hint_certificate:
        hint_dimension, hint_edges = read_certificate(Path(args.hint_certificate))
        if hint_dimension != d:
            raise ValueError("hint certificate has the wrong dimension")
        hint_set = set(hint_edges)
        for edge in all_edges:
            model.add_hint(edge_var[edge], int(edge in hint_set))
    model.minimize(sum(edge_var.values()))

    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = args.time_limit
    solver.parameters.num_search_workers = args.workers
    solver.parameters.log_search_progress = args.log_progress
    status = solver.solve(model)
    if status not in (cp_model.FEASIBLE, cp_model.OPTIMAL):
        print(json.dumps({"status": solver.status_name(status)}, sort_keys=True))
        return 1
    selected = [edge for edge in all_edges if solver.boolean_value(edge_var[edge])]
    summary = verify_selected(d, selected)
    write_certificate(Path(args.certificate), d, selected)
    print(
        json.dumps(
            summary
            | {
                "cp_sat_status": solver.status_name(status),
                "best_bound": solver.best_objective_bound,
                "wall_time_seconds": solver.wall_time,
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)

    generate_parser = subparsers.add_parser("generate", help="write a CNF instance")
    generate_parser.add_argument("dimension", type=int)
    generate_parser.add_argument("cnf")
    generate_parser.add_argument("--bound", type=int)
    generate_parser.add_argument("--no-fix-edge", action="store_true")

    solve_parser = subparsers.add_parser("solve", help="generate and run a SAT solver")
    solve_parser.add_argument("dimension", type=int)
    solve_parser.add_argument("cnf")
    solve_parser.add_argument("--bound", type=int)
    solve_parser.add_argument("--solver", default="cadical")
    solve_parser.add_argument("--solver-arg", action="append", default=[])
    solve_parser.add_argument("--proof")
    solve_parser.add_argument("--certificate")
    solve_parser.add_argument("--no-fix-edge", action="store_true")

    verify_parser = subparsers.add_parser("verify", help="verify a JSON construction")
    verify_parser.add_argument("certificate")
    verify_parser.add_argument("--translation-code", choices=("hamming7", "simplex7"))

    decode_parser = subparsers.add_parser("decode", help="decode a SAT-competition model")
    decode_parser.add_argument("dimension", type=int)
    decode_parser.add_argument("model")
    decode_parser.add_argument("certificate")

    optimize_parser = subparsers.add_parser("optimize", help="minimize edges with PySAT RC2 MaxSAT")
    optimize_parser.add_argument("dimension", type=int)
    optimize_parser.add_argument("certificate")
    optimize_parser.add_argument("--backend", default="g4")
    optimize_parser.add_argument("--verbose", type=int, default=1)
    optimize_parser.add_argument("--no-fix-edge", action="store_true")

    cp_parser = subparsers.add_parser("cp-optimize", help="minimize edges with OR-Tools CP-SAT")
    cp_parser.add_argument("dimension", type=int)
    cp_parser.add_argument("certificate")
    cp_parser.add_argument("--time-limit", type=float, default=300.0)
    cp_parser.add_argument("--workers", type=int, default=8)
    cp_parser.add_argument("--log-progress", action="store_true")
    cp_parser.add_argument("--hint-certificate")
    cp_parser.add_argument("--no-fix-edge", action="store_true")

    orbit_parser = subparsers.add_parser(
        "orbit-optimize", help="optimize among code-translation-invariant subgraphs"
    )
    orbit_parser.add_argument("dimension", type=int)
    orbit_parser.add_argument("certificate")
    orbit_parser.add_argument("--code", choices=("hamming7", "simplex7"), required=True)
    orbit_parser.add_argument("--backend", default="g4")
    orbit_parser.add_argument("--verbose", type=int, default=1)

    orbit_generate_parser = subparsers.add_parser(
        "orbit-generate", help="write a bounded code-translation-orbit CNF"
    )
    orbit_generate_parser.add_argument("dimension", type=int)
    orbit_generate_parser.add_argument("cnf")
    orbit_generate_parser.add_argument("--code", choices=("hamming7", "simplex7"), required=True)
    orbit_generate_parser.add_argument("--bound-orbits", type=int, required=True)

    greedy_parser = subparsers.add_parser("greedy", help="search random maximal square-free graphs")
    greedy_parser.add_argument("dimension", type=int)
    greedy_parser.add_argument("certificate")
    greedy_parser.add_argument("--seed", type=int, default=0)
    greedy_parser.add_argument("--trials", type=int, default=1000)
    greedy_parser.add_argument("--seed-kind", choices=("empty", "hamming7", "simplex7"), default="empty")
    greedy_parser.add_argument("--initial-certificate")
    greedy_parser.add_argument("--drop", type=int, default=0)

    args = parser.parse_args()
    if args.command == "generate":
        cnf, all_edges = build_cnf(args.dimension, args.bound, not args.no_fix_edge)
        write_dimacs(
            Path(args.cnf),
            cnf,
            {"dimension": args.dimension, "edge_bound": args.bound, "primary_variables": len(all_edges)},
        )
        print(json.dumps({"variables": cnf.variables, "clauses": len(cnf.clauses or [])}, sort_keys=True))
        return 0
    if args.command == "solve":
        return solve(args)
    if args.command == "verify":
        d, selected = read_certificate(Path(args.certificate))
        summary = verify_selected(d, selected)
        if args.translation_code:
            selected_set = set(selected)
            translations = translation_code(d, args.translation_code)
            for edge in selected:
                for translation in translations:
                    translated = edge_key(
                        edge[0] ^ translation,
                        (edge[0] ^ (1 << edge[1])) ^ translation,
                    )
                    if translated not in selected_set:
                        raise ValueError("certificate is not invariant under the requested translations")
            summary |= {
                "translation_code": args.translation_code,
                "translation_group_order": len(translations),
            }
        print(json.dumps(summary, indent=2, sort_keys=True))
        return 0
    if args.command == "decode":
        all_edges = edges(args.dimension)
        model = parse_solver_model(Path(args.model).read_text(encoding="ascii"), len(all_edges))
        selected = [edge for edge, value in zip(all_edges, model, strict=True) if value]
        summary = verify_selected(args.dimension, selected)
        write_certificate(Path(args.certificate), args.dimension, selected)
        print(json.dumps(summary, indent=2, sort_keys=True))
        return 0
    if args.command == "optimize":
        return optimize(args)
    if args.command == "cp-optimize":
        return optimize_cp_sat(args)
    if args.command == "orbit-optimize":
        return optimize_orbits(args)
    if args.command == "orbit-generate":
        cnf, orbits = build_orbit_cnf(args.dimension, args.code)
        add_at_most(cnf, list(range(1, len(orbits) + 1)), args.bound_orbits)
        write_dimacs(
            Path(args.cnf),
            cnf,
            {
                "dimension": args.dimension,
                "translation_code": args.code,
                "edge_orbits": len(orbits),
                "orbit_sizes": [len(orbit) for orbit in orbits],
                "selected_orbit_bound": args.bound_orbits,
            },
        )
        print(json.dumps({"variables": cnf.variables, "clauses": len(cnf.clauses or [])}, sort_keys=True))
        return 0
    if args.command == "greedy":
        initial = None
        if args.initial_certificate:
            initial_dimension, initial = read_certificate(Path(args.initial_certificate))
            if initial_dimension != args.dimension:
                raise ValueError("initial certificate has the wrong dimension")
        selected = greedy(args.dimension, args.seed, args.trials, args.seed_kind, initial, args.drop)
        write_certificate(Path(args.certificate), args.dimension, selected)
        print(json.dumps(verify_selected(args.dimension, selected), indent=2, sort_keys=True))
        return 0
    raise AssertionError("unreachable")


if __name__ == "__main__":
    raise SystemExit(main())
