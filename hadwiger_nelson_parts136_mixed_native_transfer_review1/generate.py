#!/usr/bin/env python3
"""Generate the independent positive four-colour review witness."""
from argparse import ArgumentParser
from itertools import combinations
import hashlib
import json
from pathlib import Path
import subprocess

from verify import INPUT_HASHES, RECEIVER, TARGET, TARGET_HASH, build, graph, proper


def solve(solver, n, edges, pins):
    clauses = []
    for vertex in range(n):
        variables = [4*vertex+colour+1 for colour in range(4)]
        clauses.append(variables)
        clauses.extend((-variables[a], -variables[b])
                       for a, b in combinations(range(4), 2))
    clauses.extend((-4*a-colour-1, -4*b-colour-1)
                   for a, b in edges for colour in range(4))
    clauses.extend((4*v+int(c)+1,) for v, c in pins.items())
    dimacs = f"p cnf {4*n} {len(clauses)}\n" + "".join(
        " ".join(map(str, clause)) + " 0\n" for clause in clauses)
    run = subprocess.run([str(solver)], input=dimacs, text=True,
                         capture_output=True)
    if run.returncode != 10 or "s SATISFIABLE" not in run.stdout:
        raise RuntimeError("solver did not return SAT: " + run.stderr[-1000:])
    positive = {int(x) for line in run.stdout.splitlines() if line.startswith("v ")
                for x in line[2:].split() if int(x) > 0}
    word = "".join(str(next(c for c in range(4) if 4*v+c+1 in positive))
                   for v in range(n))
    if not proper(word, edges, n):
        raise ValueError("decoded solver word is not proper")
    return word


def main():
    parser = ArgumentParser()
    parser.add_argument("--solver", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    raws, _, _, _, _, _, points, _ = build()
    edges, _ = graph(points)
    target_raw = (TARGET / "certificate.json").read_bytes()
    if hashlib.sha256(target_raw).hexdigest() != TARGET_HASH:
        raise ValueError("target hash")
    target = json.loads(target_raw)
    fixtures = json.loads((RECEIVER / "fixtures.json").read_text())["host_rows"]
    fixture_index = 1
    host_word = fixtures[fixture_index]["witness"]
    extra_pins = [[136, 0], [294, 0]]
    pins = {v: c for v, c in enumerate(host_word)}
    pins.update(extra_pins)
    fresh = solve(args.solver, len(points), edges, pins)
    result = {
        "schema": "hn-parts136-native-transfer-independent-review-v1",
        "target_certificate_sha256": TARGET_HASH,
        "input_sha256": [hashlib.sha256(raw).hexdigest() for raw in raws],
        "fresh_four_colour_word": fresh,
        "fresh_host_fixture_index": fixture_index,
        "fresh_boundary_pattern": fixtures[fixture_index]["pattern"],
        "fresh_extra_pins": extra_pins,
        "fresh_word_differs_from_target_positions": sum(
            a != b for a, b in zip(fresh, target["colour4"])),
        "fresh_word_difference_by_block": [
            sum(a != b for a, b in zip(fresh[:136], target["colour4"][:136])),
            sum(a != b for a, b in zip(fresh[136:294], target["colour4"][136:294])),
            sum(a != b for a, b in zip(fresh[294:], target["colour4"][294:])),
        ],
    }
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")


if __name__ == "__main__":
    main()
