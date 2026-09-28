"""Exact CNF for arbitrary old-to-new colour maps on ten-position blocks."""

import argparse
from pathlib import Path

HERE = Path(__file__).resolve().parent
N = 537


def input_word():
    word = (HERE / "seed537.txt").read_text(encoding="ascii").strip()
    assert len(word) == N and set(word) == set("123456")
    return [0] + [int(digit) for digit in word]


def instance():
    old = input_word()
    block = [0] + [(v - 1) // 10 for v in range(1, N + 1)]
    rows = sorted({(block[v], old[v]) for v in range(1, N + 1)})
    index = {row: number for number, row in enumerate(rows)}
    supports = set()
    triples = 0
    for z in range(2, N + 1):
        for x in range(1, z // 2 + 1):
            y = z - x
            supports.add(tuple(sorted({index[(block[v], old[v])] for v in (x, y, z)})))
            triples += 1
    assert triples == 72092
    assert len(rows) == 263 and len(supports) == 52754
    root = index[(block[1], old[1])]
    assert old[1] == 2 and root == 1
    return rows, supports, root


def write_cnf(path):
    rows, supports, root = instance()
    variables = 6 * len(rows)
    clauses = 16 * len(rows) + 1 + 6 * len(supports)
    assert (variables, clauses) == (1578, 320733)
    emitted = 0

    def var(row, colour):
        return 6 * row + colour

    with Path(path).open("w", encoding="ascii", newline="\n") as out:
        out.write(f"p cnf {variables} {clauses}\n")

        def emit(literals):
            nonlocal emitted
            out.write(" ".join(map(str, literals)) + " 0\n")
            emitted += 1

        for row in range(len(rows)):
            emit([var(row, c) for c in range(1, 7)])
            for first in range(1, 7):
                for second in range(first + 1, 7):
                    emit([-var(row, first), -var(row, second)])

        # A global colour permutation can always make the image of W(1)=2
        # equal to 2, even when the block maps are noninjective.
        emit([var(root, 2)])

        for support in sorted(supports):
            for colour in range(1, 7):
                emit([-var(row, colour) for row in support])

    assert emitted == clauses
    return {"blocks": 54, "rows": len(rows), "supports": len(supports),
            "variables": variables, "clauses": clauses, "triples": 72092}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    print(write_cnf(args.output))
