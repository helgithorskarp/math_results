#!/usr/bin/env python3
"""Run and audit the complete nauty/Traces census used in this result."""

from __future__ import annotations

import argparse
import concurrent.futures
import json
import subprocess
from collections import Counter
from pathlib import Path


CONNECTED_COUNTS = {
    1: 1,
    2: 1,
    3: 2,
    4: 6,
    5: 21,
    6: 112,
    7: 853,
    8: 11_117,
    9: 261_080,
    10: 11_716_571,
}

CONNECTED_CUBIC_COUNTS = {
    4: 1,
    6: 2,
    8: 5,
    10: 19,
    12: 85,
    14: 509,
    16: 4_060,
    18: 41_301,
    20: 510_489,
}


def parse_summary(stderr: bytes) -> tuple[int, Counter[int]]:
    fields: dict[str, str] = {}
    for token in stderr.decode("utf-8", errors="strict").strip().split():
        if "=" not in token:
            raise AssertionError(f"unexpected solver diagnostic token: {token!r}")
        key, value = token.split("=", 1)
        fields[key] = value
    required = {"processed", "obstructions", "cops", "elapsed_seconds"}
    if not required <= fields.keys():
        raise AssertionError(f"incomplete solver summary: {fields}")
    if int(fields["obstructions"]) != 0 or int(fields["cops"]) != 2:
        raise AssertionError(f"unexpected solver outcome: {fields}")
    ranks = Counter(
        {int(key.removeprefix("rank_")): int(value) for key, value in fields.items() if key.startswith("rank_")}
    )
    processed = int(fields["processed"])
    if any(rank < 0 for rank in ranks) or sum(ranks.values()) != processed:
        raise AssertionError(f"incomplete or inconsistent rank summary: {fields}")
    float(fields["elapsed_seconds"])
    return processed, ranks


def run_partition(
    geng: Path,
    solver: Path,
    family: str,
    order: int,
    residue: int,
    modulus: int,
) -> tuple[int, Counter[int], list[str]]:
    command = [str(geng), "-cq"]
    round_limit = 2
    if family == "all":
        command.append(str(order))
    elif family == "cubic":
        edges = 3 * order // 2
        command.extend(["-d3", "-D3", str(order), f"{edges}:{edges}"])
        round_limit = 3
    else:
        raise AssertionError(f"unknown family {family!r}")
    if modulus > 1:
        command.append(f"{residue}/{modulus}")

    generator = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if generator.stdout is None or generator.stderr is None:
        raise AssertionError("failed to open generator pipes")
    solver_command = [str(solver), "--max-rounds", str(round_limit)]
    if family == "cubic":
        solver_command.extend(["--emit-rank", "3"])
    checker = subprocess.Popen(
        solver_command,
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
            f"geng failed for {family} n={order} part={residue}/{modulus}: "
            f"{generator_stderr.decode(errors='replace')}"
        )
    if checker.returncode != 0:
        raise RuntimeError(
            f"solver failed for {family} n={order} part={residue}/{modulus}: "
            f"{checker_stderr.decode(errors='replace')}"
        )
    processed, ranks = parse_summary(checker_stderr)
    witnesses = []
    for row in checker_stdout.splitlines():
        fields = row.split(b"\t")
        if len(fields) != 5 or fields[1] != str(order).encode() or fields[2:4] != [b"WIN", b"3"]:
            raise AssertionError(
                f"unexpected solver row for {family} n={order} part={residue}/{modulus}: {row!r}"
            )
        witnesses.append(fields[0].decode("ascii"))
    if family == "all" and witnesses:
        raise AssertionError("rank-three row emitted in the two-round all-connected census")
    if len(witnesses) != ranks[3]:
        raise AssertionError("rank-three witness count does not match the aggregate summary")
    return processed, ranks, witnesses


def run_family(
    executor: concurrent.futures.Executor,
    geng: Path,
    solver: Path,
    family: str,
    counts: dict[int, int],
    partitions: int,
) -> list[dict[str, object]]:
    results = []
    for order, expected in counts.items():
        futures = [
            executor.submit(run_partition, geng, solver, family, order, residue, partitions)
            for residue in range(partitions)
        ]
        processed = 0
        ranks: Counter[int] = Counter()
        rank_three_witnesses: list[str] = []
        for future in futures:
            part_processed, part_ranks, part_witnesses = future.result()
            processed += part_processed
            ranks.update(part_ranks)
            rank_three_witnesses.extend(part_witnesses)
        if processed != expected:
            raise AssertionError(
                f"{family} order {order}: generated {processed} graphs, expected {expected}"
            )
        if len(rank_three_witnesses) != len(set(rank_three_witnesses)):
            raise AssertionError(f"duplicate rank-three witness for {family} order {order}")
        result: dict[str, object] = {
            "order": order,
            "graphs": processed,
            "rank_counts": {str(rank): count for rank, count in sorted(ranks.items())},
        }
        if rank_three_witnesses:
            result["rank_3_graph6"] = sorted(rank_three_witnesses)
        results.append(result)
    return results


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--geng", type=Path, required=True, help="path to nauty/Traces geng")
    parser.add_argument("--solver", type=Path, required=True, help="path to compiled dirloc_solver")
    parser.add_argument("--scope", choices=("all", "cubic", "both"), default="both")
    parser.add_argument("--partitions", type=int, default=1)
    parser.add_argument("--jobs", type=int, default=1)
    args = parser.parse_args()
    if args.partitions < 1 or args.jobs < 1:
        raise SystemExit("--partitions and --jobs must be positive")
    if not args.geng.is_file() or not args.solver.is_file():
        raise SystemExit("--geng and --solver must name existing files")
    geng = args.geng.resolve()
    solver = args.solver.resolve()

    output: dict[str, object] = {
        "method": {
            "all_connected_max_rounds": 2,
            "connected_cubic_max_rounds": 3,
            "cops": 2,
            "generator_requirement": "nauty/Traces geng 2.9.3",
        },
        "families": {},
    }
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.jobs) as executor:
        families = output["families"]
        assert isinstance(families, dict)
        if args.scope in ("all", "both"):
            families["all_connected"] = run_family(
                executor, geng, solver, "all", CONNECTED_COUNTS, args.partitions
            )
        if args.scope in ("cubic", "both"):
            families["connected_cubic"] = run_family(
                executor, geng, solver, "cubic", CONNECTED_CUBIC_COUNTS, args.partitions
            )
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
