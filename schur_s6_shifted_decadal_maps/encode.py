"""Exact CNF for arbitrary colour maps on a shifted decadal grid."""

import argparse
from pathlib import Path

HERE = Path(__file__).resolve().parent
N = 537


def word():
    digits = (HERE / "seed537.txt").read_text(encoding="ascii").strip()
    assert len(digits) == N and set(digits) == set("123456")
    return [0] + [int(digit) for digit in digits]


def instance(offset):
    assert 1 <= offset <= 10
    old = word()

    def block(v):
        return 0 if v <= offset else 1 + (v - offset - 1) // 10

    rows = sorted({(block(v), old[v]) for v in range(1, N + 1)})
    index = {row: i for i, row in enumerate(rows)}
    supports = set()
    triples = 0
    for z in range(2, N + 1):
        for x in range(1, z // 2 + 1):
            y = z - x
            supports.add(tuple(sorted({index[(block(v), old[v])] for v in (x, y, z)})))
            triples += 1
    assert triples == 72092 and old[1] == 2
    root = index[(block(1), old[1])]
    return rows, supports, root, 1 + max(block(v) for v in range(1, N + 1))


def write_cnf(offset, path):
    rows, supports, root, blocks = instance(offset)
    variables = 6 * len(rows)
    clauses = 16 * len(rows) + 1 + 6 * len(supports)
    var = lambda row, colour: 6 * row + colour
    count = 0
    with Path(path).open("w", encoding="ascii", newline="\n") as out:
        out.write(f"p cnf {variables} {clauses}\n")

        def emit(literals):
            nonlocal count
            out.write(" ".join(map(str, literals)) + " 0\n")
            count += 1

        for row in range(len(rows)):
            emit([var(row, c) for c in range(1, 7)])
            for c in range(1, 7):
                for d in range(c + 1, 7):
                    emit([-var(row, c), -var(row, d)])
        # Global output-colour relabelling, valid for noninjective maps.
        emit([var(root, 2)])
        for support in sorted(supports):
            for colour in range(1, 7):
                emit([-var(row, colour) for row in support])
    assert count == clauses
    return {"offset": offset, "blocks": blocks, "rows": len(rows),
            "supports": len(supports), "variables": variables,
            "clauses": clauses, "triples": 72092}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("offset", type=int)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    print(write_cnf(args.offset, args.output))
