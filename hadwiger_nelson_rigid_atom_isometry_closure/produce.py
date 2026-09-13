#!/usr/bin/env python3
"""Generate positive four-colour certificates with a SAT solver."""

import argparse
import json
from pathlib import Path
import subprocess
import tempfile

from geometry import closure_geometry


def variable(vertex, colour):
    return 4 * vertex + colour + 1


def clauses(vertex_count, edges):
    out = []
    for vertex in range(vertex_count):
        out.append(tuple(variable(vertex, colour) for colour in range(4)))
        out.extend((-variable(vertex, a), -variable(vertex, b))
                   for a in range(4) for b in range(a + 1, 4))
    for a, b in edges:
        out.extend((-variable(a, colour), -variable(b, colour)) for colour in range(4))
    # The first three points form the canonical unit triangle in all cases.
    out.extend(((variable(0, 0),), (variable(1, 1),), (variable(2, 2),)))
    return out


def solve(solver, points, edges):
    formula = clauses(len(points), edges)
    with tempfile.TemporaryDirectory(prefix="hn-rigid-closure-") as temporary:
        path = Path(temporary) / "four_colour.cnf"
        with path.open("w", encoding="ascii") as handle:
            handle.write(f"p cnf {4 * len(points)} {len(formula)}\n")
            for clause in formula:
                handle.write(" ".join(map(str, clause)) + " 0\n")
        process = subprocess.run([solver, str(path)], capture_output=True, text=True,
                                 check=False)
    if process.returncode != 10:
        raise RuntimeError(f"expected SAT, solver returned {process.returncode}")
    positive = set()
    for line in process.stdout.splitlines():
        if line.startswith("v "):
            positive.update(x for x in map(int, line[2:].split()) if x > 0)
    word = []
    for vertex in range(len(points)):
        colours = [colour for colour in range(4) if variable(vertex, colour) in positive]
        if len(colours) != 1:
            raise ValueError("malformed SAT model")
        word.append(colours[0])
    if not all(word[a] != word[b] for a, b in edges):
        raise ValueError("SAT model fails the graph definition")
    return "".join(map(str, word)), 4 * len(points), len(formula)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--solver", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    rows = []
    for name in ("moser_self", "golomb_self", "mixed_aligned"):
        row, points, edges = closure_geometry(name)
        row["colour_word"], row["variables"], row["clauses"] = solve(
            args.solver, points, edges
        )
        rows.append(row)
    certificate = {"field_basis": ["1", "sqrt33", "i_sqrt3", "i_sqrt11"],
                   "rows": rows}
    Path(args.output).write_text(json.dumps(certificate, sort_keys=True) + "\n",
                                 encoding="utf-8")
    print(json.dumps({"output": args.output,
                      "rows": [{k: row[k] for k in
                                ("name", "vertices", "edges", "copy_point_sets")}
                               for row in rows]}, sort_keys=True))


if __name__ == "__main__":
    main()
