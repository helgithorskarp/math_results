#!/usr/bin/env python3
"""Run the exact response-fiber descent census in deterministic partitions."""

from __future__ import annotations

import argparse
import concurrent.futures
import json
import subprocess
from pathlib import Path

from run_census import CONNECTED_COUNTS


def parse_summary(stderr: bytes) -> tuple[int, int, int]:
    fields: dict[str, str] = {}
    for token in stderr.decode("utf-8", errors="strict").strip().split():
        if "=" not in token:
            raise AssertionError(f"unexpected solver diagnostic token: {token!r}")
        key, value = token.split("=", 1)
        fields[key] = value
    required = {"processed", "descent_failures", "checked_states", "elapsed_seconds"}
    if fields.keys() != required:
        raise AssertionError(f"unexpected solver summary fields: {fields}")
    float(fields["elapsed_seconds"])
    return (
        int(fields["processed"]),
        int(fields["descent_failures"]),
        int(fields["checked_states"]),
    )


def run_partition(
    geng: Path,
    solver: Path,
    order: int,
    residue: int,
    modulus: int,
) -> tuple[int, int]:
    command = [str(geng), "-cq", str(order)]
    if modulus > 1:
        command.append(f"{residue}/{modulus}")
    generator = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if generator.stdout is None or generator.stderr is None:
        raise AssertionError("failed to open generator pipes")
    checker = subprocess.Popen(
        [str(solver), "--check-descent"],
        stdin=generator.stdout,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    generator.stdout.close()
    checker_stdout, checker_stderr = checker.communicate()
    generator_stderr = generator.stderr.read()
    generator_returncode = generator.wait()
    if generator_returncode != 0:
        raise RuntimeError(
            f"geng failed for n={order} part={residue}/{modulus}: "
            f"{generator_stderr.decode(errors='replace')}"
        )
    if checker.returncode != 0:
        raise RuntimeError(
            f"solver failed for n={order} part={residue}/{modulus}: "
            f"{checker_stderr.decode(errors='replace')}"
        )
    processed, failures, checked_states = parse_summary(checker_stderr)
    if failures != 0 or checker_stdout:
        raise AssertionError(
            f"descent obstruction for n={order} part={residue}/{modulus}: "
            f"{checker_stdout[:500]!r}"
        )
    return processed, checked_states


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--geng", type=Path, required=True, help="path to nauty/Traces geng")
    parser.add_argument("--solver", type=Path, required=True, help="path to compiled dirloc_solver")
    parser.add_argument("--max-order", type=int, default=10)
    parser.add_argument("--partitions", type=int, default=1)
    parser.add_argument("--jobs", type=int, default=1)
    args = parser.parse_args()
    if not 1 <= args.max_order <= max(CONNECTED_COUNTS):
        raise SystemExit(f"--max-order must lie in 1..{max(CONNECTED_COUNTS)}")
    if args.partitions < 1 or args.jobs < 1:
        raise SystemExit("--partitions and --jobs must be positive")
    if not args.geng.is_file() or not args.solver.is_file():
        raise SystemExit("--geng and --solver must name existing files")
    geng = args.geng.resolve()
    solver = args.solver.resolve()

    orders = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.jobs) as executor:
        for order in range(1, args.max_order + 1):
            futures = [
                executor.submit(run_partition, geng, solver, order, residue, args.partitions)
                for residue in range(args.partitions)
            ]
            processed = 0
            checked_states = 0
            for future in futures:
                part_processed, part_states = future.result()
                processed += part_processed
                checked_states += part_states
            expected = CONNECTED_COUNTS[order]
            if processed != expected:
                raise AssertionError(f"order {order}: generated {processed} graphs, expected {expected}")
            orders.append(
                {
                    "checked_states": checked_states,
                    "connected_graphs": processed,
                    "criterion_failures": 0,
                    "order": order,
                }
            )

    output = {
        "criterion": (
            "every neighborhood-generated belief has an action whose unresolved successors "
            "are smaller or statically two-resolvable"
        ),
        "generator_requirement": "nauty/Traces geng 2.9.3",
        "orders": orders,
        "total_checked_states": sum(int(row["checked_states"]) for row in orders),
    }
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
