#!/usr/bin/env python3
"""Generate positive four-colour witnesses for the 70 exact physical unions."""
from argparse import ArgumentParser
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path
import subprocess

from verify import (SOURCE, TARGET, TARGET_CERT, build_s1, canonical_union,
                    enumerate_embeddings, map_copy, proper, unit_edges)


def solve(solver, n, edges):
    clauses = []
    for vertex in range(n):
        variables = [4*vertex+colour+1 for colour in range(4)]
        clauses.append(variables)
        clauses.extend([-variables[a], -variables[b]]
                       for a, b in combinations(range(4), 2))
    clauses.extend([-4*a-colour-1, -4*b-colour-1]
                   for a, b in edges for colour in range(4))
    clauses.append([1])
    dimacs = f"p cnf {4*n} {len(clauses)}\n" + "".join(
        " ".join(map(str, clause)) + " 0\n" for clause in clauses)
    run = subprocess.run([str(solver)], input=dimacs, text=True,
                         capture_output=True)
    if run.returncode != 10 or "s SATISFIABLE" not in run.stdout:
        raise RuntimeError("solver did not return SAT: " + run.stderr[-1000:])
    positive = {int(x) for line in run.stdout.splitlines() if line.startswith("v ")
                for x in line[2:].split() if int(x) > 0}
    colours = tuple(next(c for c in range(4) if 4*v+c+1 in positive)
                    for v in range(n))
    if not proper(colours, edges):
        raise ValueError("decoded solver word is not proper")
    return "".join(map(str, colours))


def row_hash(rows):
    return sha256("".join(",".join(map(str, row)) + "\n"
                          for row in rows).encode()).hexdigest()


def point_key(point):
    return tuple(str(v) for coordinate in point for v in coordinate)


def main():
    parser = ArgumentParser()
    parser.add_argument("--solver", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    source_raw, s0, s1, s1_edges, _, _ = build_s1()
    found = enumerate_embeddings(s0, s1)
    target_points = [s0[v] for v in TARGET]
    rows = []
    for ids in found:
        mapped = map_copy(s1, ids, target_points)
        points, blocker_map, host_map = canonical_union(s1, mapped)
        edges = unit_edges(points)
        edge_set = set(edges)
        internal = {tuple(sorted((blocker_map[a], blocker_map[b])))
                    for a, b in s1_edges}
        internal |= {tuple(sorted((host_map[a], host_map[b])))
                     for a, b in s1_edges}
        rows.append({
            "embedding": list(ids),
            "points": len(points),
            "edges": len(edges),
            "overlap": 230-len(points),
            "incidental_edges": len(edge_set-internal),
            "point_sha256": row_hash([point_key(p) for p in points]),
            "edge_sha256": row_hash(edges),
            "four_colour_word": solve(args.solver, len(points), edges),
        })
    result = {
        "schema": "hn-moser-s1-physical-unions-review-v1",
        "source_sha256": sha256(source_raw).hexdigest(),
        "target_certificate_sha256": sha256(TARGET_CERT.read_bytes()).hexdigest(),
        "target_terminals": list(TARGET),
        "s1_points": len(s1),
        "s1_edges": len(s1_edges),
        "embedding_count": len(found),
        "unions": rows,
    }
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")


if __name__ == "__main__":
    main()
