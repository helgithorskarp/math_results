"""Generate the exact one-hot Schur CNF for the fixed 82-entry suffix.

Variables 6*(v-1)+c represent the assertion that integer v has colour c.
"""

import argparse
from pathlib import Path

HERE = Path(__file__).resolve().parent
N = 537
FIRST = 456
VARIABLES = 6 * N
TRIPLES = 72092
CLAUSES = 16 * N + 6 * TRIPLES + (N - FIRST + 1)


def variable(v, c):
    return 6 * (v - 1) + c


def write_cnf(path):
    tail = (HERE / "tail82.txt").read_text(encoding="ascii").strip()
    assert len(tail) == 82 and set(tail) <= set("123456")
    count = 0
    triples = 0
    with Path(path).open("w", encoding="ascii", newline="\n") as output:
        output.write(f"p cnf {VARIABLES} {CLAUSES}\n")

        def clause(literals):
            nonlocal count
            output.write(" ".join(map(str, literals)) + " 0\n")
            count += 1

        for v in range(1, N + 1):
            clause([variable(v, c) for c in range(1, 7)])
            for c in range(1, 7):
                for d in range(c + 1, 7):
                    clause([-variable(v, c), -variable(v, d)])

        for z in range(2, N + 1):
            for x in range(1, z // 2 + 1):
                y = z - x
                for c in range(1, 7):
                    if x == y:
                        clause([-variable(x, c), -variable(z, c)])
                    else:
                        clause([-variable(x, c), -variable(y, c), -variable(z, c)])
                triples += 1

        for v, digit in enumerate(tail, FIRST):
            clause([variable(v, int(digit))])

    assert triples == TRIPLES and count == CLAUSES
    return count


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    print(f"clauses={write_cnf(args.output)} variables={VARIABLES} triples={TRIPLES}")
