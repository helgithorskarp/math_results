#!/usr/bin/env python3
"""Explore and certify minimum transversals of the Parts-509 list-interface instance."""

from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import importlib.util
import json
from pathlib import Path
import time

from pysat.card import CardEnc, EncType
from pysat.formula import CNF
from pysat.solvers import Solver


UNIVERSE_SIZE = 183
OPTIMUM = 14


def load_instance(path: Path) -> tuple[list[tuple[int, ...]], list[tuple[int, int]]]:
    cert = json.loads(path.read_text(encoding="utf-8"))
    assert cert["minimum_extra_edges"] == OPTIMUM
    extras = [tuple(map(int, edge)) for edge in cert["extra_edges"]]
    assert len(extras) == UNIVERSE_SIZE
    hyperedges = [
        tuple(map(int, row["violated_extra_indices"]))
        for row in cert["constraints"]
    ]
    assert len(hyperedges) == cert["hitting_constraints"] == 144
    return hyperedges, extras


def enumerate_minimum_transversals(
    hyperedges: list[tuple[int, ...]],
    *,
    limit: int | None,
    seconds: float | None,
) -> tuple[list[tuple[int, ...]], bool]:
    cnf = CNF()
    cnf.extend([[i + 1 for i in edge] for edge in hyperedges])
    cnf.extend(
        CardEnc.equals(
            lits=list(range(1, UNIVERSE_SIZE + 1)),
            bound=OPTIMUM,
            top_id=UNIVERSE_SIZE,
            encoding=EncType.seqcounter,
        ).clauses
    )
    models: list[tuple[int, ...]] = []
    complete = True
    deadline = None if seconds is None else time.monotonic() + seconds
    with Solver(name="cadical153", bootstrap_with=cnf.clauses) as solver:
        while solver.solve():
            truth = {abs(lit): lit > 0 for lit in solver.get_model()}
            chosen = tuple(i for i in range(UNIVERSE_SIZE) if truth[i + 1])
            assert len(chosen) == OPTIMUM
            models.append(chosen)
            solver.add_clause([-(i + 1) for i in chosen])
            if limit is not None and len(models) >= limit:
                complete = False
                break
            if deadline is not None and time.monotonic() >= deadline:
                complete = False
                break
    return models, complete


def exact_at_most(variables: list[int], bound: int, start_variable: int) -> list[list[int]]:
    """Encode z[i,j] iff at least j of variables[:i] are true, then forbid bound+1."""
    width = bound + 2

    def threshold(i: int, j: int) -> int:
        return start_variable + i * width + j

    clauses = [[threshold(0, 0)]]
    clauses.extend([[-threshold(0, j)] for j in range(1, width)])
    for i, variable in enumerate(variables, 1):
        current = threshold(i, 0)
        above = threshold(i - 1, 0)
        clauses.extend([[-current, above], [-above, current]])
        for j in range(1, width):
            current = threshold(i, j)
            above = threshold(i - 1, j)
            diagonal = threshold(i - 1, j - 1)
            clauses.extend(
                [
                    [-current, above, diagonal],
                    [-current, above, variable],
                    [-above, current],
                    [-diagonal, -variable, current],
                ]
            )
    clauses.append([-threshold(len(variables), bound + 1)])
    return clauses


def write_completeness_cnf(
    path: Path,
    hyperedges: list[tuple[int, ...]],
    models: list[tuple[int, ...]],
) -> tuple[int, int, str]:
    clauses = [[i + 1 for i in edge] for edge in hyperedges]
    clauses.extend(
        exact_at_most(list(range(1, UNIVERSE_SIZE + 1)), OPTIMUM, UNIVERSE_SIZE + 1)
    )
    clauses.extend([[-(i + 1) for i in model] for model in sorted(models)])
    variables = max(abs(lit) for clause in clauses for lit in clause)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="ascii") as handle:
        handle.write(f"p cnf {variables} {len(clauses)}\n")
        for clause in clauses:
            handle.write(" ".join(map(str, clause)) + " 0\n")
    return variables, len(clauses), hashlib.sha256(path.read_bytes()).hexdigest()


def load_list_kernel_module(path: Path):
    spec = importlib.util.spec_from_file_location("parts509_list_kernel", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def classify_full_interface_kernels(
    models: list[tuple[int, ...]],
    certificate_path: Path,
    edge_path: Path,
    list_kernel_path: Path,
) -> tuple[list[tuple[int, ...]], list[dict[str, object]]]:
    lk = load_list_kernel_module(list_kernel_path)
    cert = json.loads(certificate_path.read_text(encoding="utf-8"))
    strict_edges = lk.load_edges(edge_path)
    adj = lk.adjacency(strict_edges)
    base_internal = [tuple(edge) for edge in cert["base_internal_edges"]]
    extras = [tuple(edge) for edge in cert["extra_edges"]]
    representatives = {tuple(row["available_masks"]) for row in cert["states"]}
    allowed = set().union(*(lk.orbit(state) for state in representatives))
    core = [v for v in range(lk.N) if v not in set(lk.DEGREE_FOUR)]

    common = lk.graph_coloring_clauses(core, base_internal)
    common.extend([[lk.color_var(v, c)] for c, v in enumerate(lk.PINNED_TRIANGLE)])
    common.extend(lk.list_reification_clauses(adj))
    common.extend(lk.state_block(state) for state in sorted(allowed))
    selector_offset = max(abs(lit) for clause in common for lit in clause)
    guarded_edges = [
        [-(selector_offset + i + 1), -lk.color_var(u, c), -lk.color_var(v, c)]
        for i, (u, v) in enumerate(extras)
        for c in range(lk.K)
    ]
    successful: list[tuple[int, ...]] = []
    failures: list[dict[str, object]] = []
    with Solver(name="cadical153", bootstrap_with=common + guarded_edges) as solver:
        for indices in models:
            chosen = set(indices)
            assumptions = [
                selector_offset + i + 1 if i in chosen else -(selector_offset + i + 1)
                for i in range(len(extras))
            ]
            if not solver.solve(assumptions=assumptions):
                successful.append(indices)
                continue
            truth = {abs(lit): lit > 0 for lit in solver.get_model()}
            colors = [
                next(c for c in range(lk.K) if truth[lk.color_var(v, c)])
                if v in core
                else -1
                for v in range(lk.N)
            ]
            failures.append(
                {
                    "indices": list(indices),
                    "forbidden_state": list(lk.available_state(colors, adj)),
                    "core_coloring": "".join(str(colors[v]) for v in core),
                }
            )
    return successful, failures


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("certificate", type=Path)
    parser.add_argument("--limit", type=int)
    parser.add_argument("--seconds", type=float)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--completeness-cnf", type=Path)
    parser.add_argument("--classify-interface", action="store_true")
    parser.add_argument("--edges", type=Path)
    parser.add_argument("--list-kernel-source", type=Path)
    args = parser.parse_args()
    hyperedges, extras = load_instance(args.certificate)
    start = time.monotonic()
    models, complete = enumerate_minimum_transversals(
        hyperedges, limit=args.limit, seconds=args.seconds
    )
    elapsed = time.monotonic() - start
    frequency = Counter(i for model in models for i in model)
    result = {
        "complete": complete,
        "count": len(models),
        "elapsed_seconds": elapsed,
        "edge_frequencies": [
            {"index": i, "edge": list(extras[i]), "count": frequency[i]}
            for i in sorted(frequency, key=lambda x: (-frequency[x], x))
        ],
        "transversals": [list(model) for model in models],
    }
    if args.completeness_cnf is not None:
        assert complete
        variables, clauses, digest = write_completeness_cnf(
            args.completeness_cnf, hyperedges, models
        )
        result["completeness_cnf"] = {
            "variables": variables,
            "clauses": clauses,
            "sha256": digest,
        }
    if args.classify_interface:
        assert complete
        assert args.edges is not None and args.list_kernel_source is not None
        successful, failures = classify_full_interface_kernels(
            models,
            args.certificate,
            args.edges,
            args.list_kernel_source,
        )
        result["full_interface_kernel_count"] = len(successful)
        result["full_interface_kernels"] = [list(model) for model in successful]
        result["failed_transversal_count"] = len(failures)
        result["failure_witnesses"] = failures
    print(json.dumps({k: v for k, v in result.items() if k != "transversals"}, indent=2))
    if args.output is not None:
        args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
