"""SAT encoding for complete colour permutations on ten-position blocks."""

import argparse
from pathlib import Path

HERE = Path(__file__).resolve().parent
N = 537
WIDTH = 10


def seed_word():
    word = (HERE / "seed537.txt").read_text(encoding="ascii").strip()
    assert len(word) == N and set(word) == set("123456")
    return [0] + [int(digit) for digit in word]


def blocks(offset):
    assert 1 <= offset <= WIDTH
    ends = list(range(offset, N, WIDTH)) + [N]
    block = [0] * (N + 1)
    low = 1
    for index, high in enumerate(ends):
        for v in range(low, high + 1):
            block[v] = index
        low = high + 1
    assert low == N + 1
    return block, len(ends)


def instance(offset):
    old = seed_word()
    block, count_blocks = blocks(offset)
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
    return rows, supports, count_blocks


def write_cnf(path, offset):
    rows, supports, count_blocks = instance(offset)
    by_block = [[i for i, row in enumerate(rows) if row[0] == b]
                for b in range(count_blocks)]
    injectivity = 6 * sum(len(group) * (len(group) - 1) // 2 for group in by_block)
    total = 16 * len(rows) + injectivity + len(by_block[0]) + 6 * len(supports)
    variables = 6 * len(rows)
    emitted = 0

    def var(row_index, colour):
        return 6 * row_index + colour

    with Path(path).open("w", encoding="ascii", newline="\n") as out:
        out.write(f"p cnf {variables} {total}\n")

        def clause(literals):
            nonlocal emitted
            out.write(" ".join(map(str, literals)) + " 0\n")
            emitted += 1

        for row_index in range(len(rows)):
            clause([var(row_index, colour) for colour in range(1, 7)])
            for first in range(1, 7):
                for second in range(first + 1, 7):
                    clause([-var(row_index, first), -var(row_index, second)])

        for group in by_block:
            for first_index in range(len(group)):
                for second_index in range(first_index + 1, len(group)):
                    for colour in range(1, 7):
                        clause([-var(group[first_index], colour),
                                -var(group[second_index], colour)])

        # A global permutation of the output palette normalizes the first
        # block's injective old-to-new map to the identity on its used labels.
        for row_index in by_block[0]:
            clause([var(row_index, rows[row_index][1])])

        for support in sorted(supports):
            for colour in range(1, 7):
                clause([-var(row_index, colour) for row_index in support])

    assert emitted == total
    return {"offset": offset, "blocks": count_blocks, "rows": len(rows),
            "supports": len(supports), "variables": variables, "clauses": total}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("offset", type=int, choices=range(1, 11))
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    print(write_cnf(args.output, args.offset))
