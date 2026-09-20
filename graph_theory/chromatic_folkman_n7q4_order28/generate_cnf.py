#!/usr/bin/env python3
"""Generate a DIMACS CNF for six-colourability of the order-28 graph."""

import argparse
from pathlib import Path

from verify import ADJACENCY


def variable(vertex, colour):
    return 1 + 6 * vertex + colour


def clauses():
    # At least one colour per vertex.  At-most-one clauses are unnecessary:
    # choosing any true colour gives an ordinary proper colouring.
    for vertex in range(28):
        yield tuple(variable(vertex, colour) for colour in range(6))
    for u in range(28):
        for v in range(u + 1, 28):
            if not ((ADJACENCY[u] >> v) & 1):
                continue
            for colour in range(6):
                yield (-variable(u, colour), -variable(v, colour))
    # Colour names are interchangeable, so fix the identity vertex's colour.
    yield (variable(0, 0),)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    formula = list(clauses())
    assert len(formula) == 1037
    with args.output.open("w", encoding="ascii", newline="\n") as handle:
        handle.write("c 6-colourability of the 28-vertex Cayley graph\n")
        handle.write("c variable 1+6*v+c means vertex v receives colour c\n")
        handle.write("c unit 1 breaks colour symmetry at the identity\n")
        handle.write(f"p cnf 168 {len(formula)}\n")
        for clause in formula:
            handle.write(" ".join(map(str, clause)) + " 0\n")
    print(f"wrote {args.output}: variables=168 clauses={len(formula)}")


if __name__ == "__main__":
    main()
