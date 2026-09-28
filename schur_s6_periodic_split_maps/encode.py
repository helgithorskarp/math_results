"""Exact Schur CNF for periodic refinements of shifted decadal grids."""

import argparse
from pathlib import Path

HERE = Path(__file__).resolve().parent
N = 537


def instance(period, offset, phase=0):
    assert period in (2, 4)
    assert 1 <= offset <= 10
    assert 0 <= phase < period
    digits = (HERE / "seed537.txt").read_text(encoding="ascii").strip()
    assert len(digits) == N and set(digits) == set("123456")
    old = [0] + list(map(int, digits))

    def block(v):
        if v <= offset:
            return 0
        cycle, within = divmod(v - offset - 1, 10 * period)
        block_in_cycle, within_block = divmod(within, 10)
        prior_split = block_in_cycle > phase
        current_split = block_in_cycle == phase and within_block >= 5
        return (1 + (period + 1) * cycle + block_in_cycle
                + prior_split + current_split)

    rows = sorted({(block(v), old[v]) for v in range(1, N + 1)})
    index = {row: i for i, row in enumerate(rows)}
    supports = set()
    triples = 0
    for z in range(2, N + 1):
        for x in range(1, z // 2 + 1):
            y = z - x
            supports.add(tuple(sorted({index[(block(v), old[v])]
                                       for v in (x, y, z)})))
            triples += 1
    assert triples == 72092
    return rows, supports


def write_cnf(period, offset, path, phase=0):
    rows, supports = instance(period, offset, phase)
    count_rows = len(rows)
    variables = 6 * count_rows
    rgs_clauses = 1 + 5 * (count_rows - 1)
    clauses = 16 * count_rows + rgs_clauses + 6 * len(supports)
    var = lambda row, colour: 6 * row + colour
    emitted = 0
    with Path(path).open("w", encoding="ascii", newline="\n") as out:
        out.write(f"p cnf {variables} {clauses}\n")

        def emit(literals):
            nonlocal emitted
            out.write(" ".join(map(str, literals)) + " 0\n")
            emitted += 1

        for row in range(count_rows):
            emit([var(row, colour) for colour in range(1, 7)])
            for first in range(1, 7):
                for second in range(first + 1, 7):
                    emit([-var(row, first), -var(row, second)])

        # Globally relabel output colours by first appearance in row order.
        emit([var(0, 1)])
        for row in range(1, count_rows):
            for colour in range(2, 7):
                emit([-var(row, colour)]
                     + [var(earlier, colour - 1) for earlier in range(row)])

        for support in sorted(supports):
            for colour in range(1, 7):
                emit([-var(row, colour) for row in support])
    assert emitted == clauses
    result = {"period": period, "offset": offset, "rows": count_rows,
              "supports": len(supports), "variables": variables,
              "clauses": clauses, "rgs_clauses": rgs_clauses,
              "triples": 72092}
    if phase:
        result["phase"] = phase
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("period", type=int, choices=(2, 4))
    parser.add_argument("offset", type=int)
    parser.add_argument("output", type=Path)
    parser.add_argument("--phase", type=int, default=0)
    args = parser.parse_args()
    print(write_cnf(args.period, args.offset, args.output, args.phase))
