#!/usr/bin/env python3
"""Definition-level checker for SAT models of the lifted Myrvold encoding."""

from __future__ import annotations

import argparse
import sys

N = 10
DARK = 2
WHITE = 3

TYPE_ROWS = {
    "R": [1] * 8 + [4] * 2,
    "S": [1] * 7 + [3] * 3,
    "T": [1] * 7 + [2, 3, 4],
    "U": [1] * 6 + [2] * 2 + [3] * 2,
    "V": [1] * 6 + [2] * 3 + [4],
    "W": [1] * 5 + [2] * 4 + [3],
    "X": [1] * 4 + [2] * 6,
}

OMEGAS = {
    "z4": [[0, 1, 2, 3], [1, 2, 3, 0], [2, 3, 0, 1], [3, 0, 1, 2]],
    "z2xz2": [[0, 1, 2, 3], [1, 0, 3, 2], [2, 3, 0, 1], [3, 2, 1, 0]],
}


def read_positive_literals(stream) -> set[int]:
    positive: set[int] = set()
    saw_sat = False
    for line in stream:
        if line.startswith("s "):
            if "UNSATISFIABLE" in line:
                raise ValueError("the supplied solver output is UNSAT")
            if "SATISFIABLE" in line:
                saw_sat = True
        if line.startswith("v "):
            for token in line.split()[1:]:
                literal = int(token)
                if literal > 0:
                    positive.add(literal)
    if not saw_sat:
        raise ValueError("no SATISFIABLE status found")
    return positive


def decode_one_hot(positive: set[int], block: int) -> list[list[int]]:
    """Decode a 1000-variable row/column/symbol block numbered from zero."""
    base = block * N**3
    result = [[-1] * N for _ in range(N)]
    for i in range(N):
        for j in range(N):
            values = [k for k in range(N) if base + i * N * N + j * N + k + 1 in positive]
            assert len(values) == 1, (block, i, j, values)
            result[i][j] = values[0]
    return result


def decode_flag(positive: set[int], block: int, i: int, j: int, k: int) -> bool:
    return block * N**3 + i * N * N + j * N + k + 1 in positive


def is_latin(square: list[list[int]]) -> bool:
    target = list(range(N))
    return all(sorted(row) == target for row in square) and all(
        sorted(square[i][j] for i in range(N)) == target for j in range(N)
    )


def is_trp(a: list[list[int]], b: list[list[int]]) -> bool:
    """Check Definition 1 directly: two rows agree in at most one column."""
    return all(
        sum(a[i][j] == b[ip][j] for j in range(N)) <= 1
        for i in range(N)
        for ip in range(N)
    )


def is_orthogonal(a: list[list[int]], b: list[list[int]]) -> bool:
    return len({(a[i][j], b[i][j]) for i in range(N) for j in range(N)}) == N * N


def is_composition_witness(a: list[list[int]], b: list[list[int]], witness: list[list[int]]) -> bool:
    """Check B=A*W in the column-permutation convention of the paper."""
    return all(a[witness[ip][j]][j] == b[ip][j] for ip in range(N) for j in range(N))


def colours(positive: set[int], symbol_square: list[list[int]], block: int) -> list[list[str]]:
    result = [[""] * N for _ in range(N)]
    for i in range(N):
        for j in range(N):
            dark = decode_flag(positive, block, i, j, DARK)
            white_flag = decode_flag(positive, block, i, j, WHITE)
            if j < 6:
                assert not white_flag
                assert not (symbol_square[i][j] < 4 and dark)
                result[i][j] = "w" if symbol_square[i][j] < 4 else ("d" if dark else "l")
            else:
                assert not dark
                result[i][j] = "w" if symbol_square[i][j] < 4 else "l"
                assert white_flag == (result[i][j] == "w")
    return result


def check_type(square: list[list[int]], colour: list[list[str]], name: str) -> None:
    for i, count in enumerate(TYPE_ROWS[name]):
        assert colour[i][6:].count("w") == count
        assert colour[i][:6].count("d") == 2 * count - 2
        assert colour[i][:6].count("w") == 4 - count
        assert colour[i][:6].count("l") == 4 - count
        assert colour[i][6:].count("l") == 4 - count
        assert colour[i][6:].count("d") == 0
        assert all((symbol < 4) == (c == "w") for symbol, c in zip(square[i], colour[i]))


def compatible(square: list[list[int]], omega: list[list[int]]) -> bool:
    for row in square:
        for j in range(6, N):
            for jp in range(j + 1, N):
                for k in range(4):
                    if row[j] == omega[k][j - 6] and row[jp] == omega[k][jp - 6]:
                        return False
    return True


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--type", default="UU", choices=[a + b for a in TYPE_ROWS for b in TYPE_ROWS])
    parser.add_argument("--omega", required=True, choices=sorted(OMEGAS))
    parser.add_argument("--encoding", choices=("composition", "direct"), default="composition")
    parser.add_argument("--distinguished-subsquare", action="store_true")
    parser.add_argument("model", nargs="?", help="solver output; stdin if omitted")
    args = parser.parse_args()

    if args.model:
        with open(args.model, encoding="utf-8") as handle:
            positive = read_positive_literals(handle)
    else:
        positive = read_positive_literals(sys.stdin)

    # Blocks 0,1 are colour flags; 2,3 are P,Q; 4 is their witness;
    # blocks 5,6,7 are L and the P-L and Q-L witnesses.
    p = decode_one_hot(positive, 2)
    q = decode_one_hot(positive, 3)
    z = decode_one_hot(positive, 4)
    ell = decode_one_hot(positive, 5)
    named_squares = [("P", p), ("Q", q), ("Z", z), ("L", ell)]
    if args.encoding == "composition":
        pl = decode_one_hot(positive, 6)
        ql = decode_one_hot(positive, 7)
        named_squares.extend([("PL", pl), ("QL", ql)])

    for name, square in named_squares:
        assert is_latin(square), f"{name} is not Latin"
    assert is_trp(p, q)
    assert is_trp(p, ell)
    assert is_trp(q, ell)
    assert is_composition_witness(p, q, z)
    if args.encoding == "composition":
        assert is_composition_witness(p, ell, pl)
        assert is_composition_witness(q, ell, ql)
    else:
        for block, square in [(6, p), (7, q)]:
            for i in range(N):
                for ip in range(N):
                    for j in range(N):
                        assert decode_flag(positive, block, i, ip, j) == (square[i][j] == ell[ip][j])

        # Theorem 3.1(b): from mutual TRPs (L,P,Q), recover the three
        # mutually orthogonal squares L, P^{-1}L, and Q^{-1}L directly
        # from the agreement tensors.
        pinv_l = [[next(i for i in range(N) if p[i][j] == ell[ip][j]) for j in range(N)] for ip in range(N)]
        qinv_l = [[next(i for i in range(N) if q[i][j] == ell[ip][j]) for j in range(N)] for ip in range(N)]
        assert is_latin(pinv_l) and is_latin(qinv_l)
        assert is_orthogonal(ell, pinv_l)
        assert is_orthogonal(ell, qinv_l)
        assert is_orthogonal(pinv_l, qinv_l)

    pc = colours(positive, p, 0)
    qc = colours(positive, q, 1)
    check_type(p, pc, args.type[0])
    check_type(q, qc, args.type[1])
    for j in range(6):
        assert sum(pc[i][j] == "d" for i in range(N)) == 2
        assert sum(qc[i][j] == "d" for i in range(N)) == 2
        assert {p[i][j] for i in range(N) if pc[i][j] == "d"} == {
            q[i][j] for i in range(N) if qc[i][j] == "d"
        }

    assert p[0] in (
        [0, 1, 2, 4, 5, 6, 3, 7, 8, 9],
        [0, 1, 3, 4, 5, 6, 2, 7, 8, 9],
        [0, 2, 3, 4, 5, 6, 1, 7, 8, 9],
    )
    for square, name in [(p, args.type[0]), (q, args.type[1])]:
        for i in range(N - 1):
            if TYPE_ROWS[name][i] == TYPE_ROWS[name][i + 1]:
                assert square[i][0] < square[i + 1][0]
    if args.distinguished_subsquare:
        omega = OMEGAS[args.omega]
        assert all(ell[i + 6][j + 6] == omega[i][j] for i in range(4) for j in range(4))
        assert [ell[i][0] for i in range(6)] == sorted(ell[i][0] for i in range(6))
        assert [ell[i][0] for i in range(4)] == list(range(4))
        for a, colour in [(p, pc), (q, qc)]:
            for i in range(N):
                for j in range(N):
                    source_row = next(r for r in range(N) if ell[r][j] == a[i][j])
                    if j < 6:
                        assert (colour[i][j] == "d") == (source_row < 6 and a[i][j] >= 4)
                    else:
                        assert (colour[i][j] == "w") == (source_row >= 6)
    else:
        assert [ell[i][0] for i in range(N)] == list(range(N))
    assert compatible(p, OMEGAS[args.omega])
    assert compatible(q, OMEGAS[args.omega])

    print("verified: P,Q,L are Latin and pairwise TRPs")
    print(f"verified: type={args.type}, omega={args.omega}, all normalizations")


if __name__ == "__main__":
    main()
