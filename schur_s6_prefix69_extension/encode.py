"""Emit the exact one-hot CNF for Schur-colouring [1,n] with a fixed prefix.

Variables v(i,c)=6(i-1)+c, with 1<=i<=n and 1<=c<=6. Every unordered
Schur triple x<=y, x+y<=n occurs for every colour, including x=y.
Only Python's standard library is needed.
"""

import argparse
from pathlib import Path


def variable(i: int, colour: int) -> int:
    return 6 * (i - 1) + colour


def emit(n: int, prefix: str, output: Path) -> None:
    if not 1 <= len(prefix) <= n or set(prefix) - set("123456"):
        raise ValueError("prefix must contain 1..6 digits and fit in [1,n]")
    if n < 1:
        raise ValueError("n must be positive")

    # floor(n^2/4) unordered triples x<=y with x+y<=n.
    triple_count = n * n // 4
    clause_count = 16 * n + 6 * triple_count + len(prefix)
    with output.open("w", encoding="ascii") as stream:
        stream.write(f"p cnf {6*n} {clause_count}\n")
        for i in range(1, n + 1):
            stream.write(" ".join(str(variable(i, c)) for c in range(1, 7)) + " 0\n")
            for c in range(1, 7):
                for d in range(1, c):
                    stream.write(f"-{variable(i,c)} -{variable(i,d)} 0\n")
        for x in range(1, n + 1):
            for y in range(x, n - x + 1):
                for c in range(1, 7):
                    # x=y makes a two-literal clause after duplicate removal.
                    literals = sorted({-variable(x, c), -variable(y, c), -variable(x+y, c)})
                    stream.write(" ".join(map(str, literals)) + " 0\n")
        for i, digit in enumerate(prefix, 1):
            stream.write(f"{variable(i,int(digit))} 0\n")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--n", type=int, required=True)
    parser.add_argument("--prefix", type=Path, default=Path(__file__).with_name("prefix69.txt"))
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    emit(args.n, args.prefix.read_text(encoding="ascii").strip(), args.output)


if __name__ == "__main__":
    main()
