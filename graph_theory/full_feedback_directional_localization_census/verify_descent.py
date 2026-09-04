#!/usr/bin/env python3
"""Definition-level replay of the response-fiber descent criterion."""

from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path

from reference_solver import decode_graph6, encode_graph6
from verify_rank3 import BoundedDirectionalGame


def has_descent_action(game: BoundedDirectionalGame, belief: int) -> bool:
    for classes in game.partitions:
        succeeds = True
        for class_mask in classes:
            cell = belief & class_mask
            if cell.bit_count() <= 1:
                continue
            successor = game.closure(cell)
            if successor.bit_count() >= belief.bit_count() and game.resolver(successor) is None:
                succeeds = False
                break
        if succeeds:
            return True
    return False


def parse_cpp_rows(output: bytes) -> dict[bytes, tuple[str, int, int]]:
    rows: dict[bytes, tuple[str, int, int]] = {}
    for line in output.splitlines():
        fields = line.split(b"\t")
        if len(fields) != 5:
            raise AssertionError(f"unexpected C++ row: {line!r}")
        record = fields[0]
        if record in rows:
            raise AssertionError(f"duplicate C++ row: {record!r}")
        rows[record] = (fields[2].decode("ascii"), int(fields[3], 16), int(fields[4]))
    return rows


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--compare", type=Path, required=True, help="path to compiled dirloc_solver")
    parser.add_argument("--geng", type=Path, required=True, help="path to nauty/Traces geng")
    parser.add_argument("--max-order", type=int, default=8)
    args = parser.parse_args()
    if not 1 <= args.max_order <= 8:
        raise SystemExit("--max-order must lie in 1..8")
    solver = args.compare.resolve()
    geng = args.geng.resolve()
    if not solver.is_file() or not geng.is_file():
        raise SystemExit("--compare and --geng must name existing files")

    summaries = []
    total_states = 0
    for order in range(1, args.max_order + 1):
        generated = subprocess.run(
            [str(geng), "-cq", str(order)],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        ).stdout
        checked = subprocess.run(
            [str(solver), "--check-descent", "--all"],
            check=True,
            input=generated,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        records = generated.splitlines()
        cpp_rows = parse_cpp_rows(checked.stdout)
        if len(records) != len(cpp_rows):
            raise AssertionError("C++ output did not contain one row per generated graph")
        order_states = 0
        for record in records:
            adjacency = decode_graph6(record)
            if encode_graph6(adjacency) != record:
                raise AssertionError(f"graph6 round trip failed for {record!r}")
            status, counterexample, cpp_states = cpp_rows[record]
            if order == 1:
                python_states = 0
            else:
                game = BoundedDirectionalGame(adjacency)
                beliefs = {
                    game.closure(generator)
                    for generator in range(1, 1 << order)
                    if game.closure(generator).bit_count() > 1
                }
                python_states = len(beliefs)
                for belief in beliefs:
                    if not has_descent_action(game, belief):
                        raise AssertionError(
                            f"Python criterion failure for {record.decode()}: belief={belief:x}"
                        )
            if status != "DESCENT_OK" or counterexample != 0 or cpp_states != python_states:
                raise AssertionError(
                    f"C++/Python mismatch for {record.decode()}: "
                    f"status={status}, counterexample={counterexample:x}, "
                    f"cpp_states={cpp_states}, python_states={python_states}"
                )
            order_states += python_states
        summaries.append(
            {
                "checked_states": order_states,
                "connected_graphs": len(records),
                "order": order,
            }
        )
        total_states += order_states
    print(
        json.dumps(
            {"exact_cpp_python_agreement": True, "orders": summaries, "total_checked_states": total_states},
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
