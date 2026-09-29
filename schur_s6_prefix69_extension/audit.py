"""Independently audit every clause of the prefix Schur CNF."""

import argparse
from pathlib import Path


def decode(literal: int, n: int) -> tuple[int, int]:
    if not 1 <= abs(literal) <= 6 * n:
        raise ValueError(f"variable out of range: {literal}")
    q, r = divmod(abs(literal) - 1, 6)
    return q + 1, r + 1


def audit(path: Path, prefix: str, n: int) -> None:
    if not 1 <= len(prefix) <= n:
        raise ValueError("invalid prefix length")
    seen_at_least: set[int] = set()
    seen_pairs: set[tuple[int, int, int]] = set()
    seen_triples: set[tuple[int, int, int]] = set()
    seen_prefix: set[int] = set()
    with path.open(encoding="ascii") as source:
        header = source.readline().split()
        expected_count = 16 * n + 6 * (n*n//4) + len(prefix)
        if header != ["p", "cnf", str(6*n), str(expected_count)]:
            raise ValueError(f"wrong header: {header}")
        count = 0
        for line in source:
            terms = [int(t) for t in line.split()]
            if not terms or terms[-1] != 0 or 0 in terms[:-1]:
                raise ValueError(f"malformed clause: {line!r}")
            clause = terms[:-1]
            count += 1
            if len(clause) == 1 and clause[0] > 0:
                i, c = decode(clause[0], n)
                if i > len(prefix) or c != int(prefix[i-1]) or i in seen_prefix:
                    raise ValueError("invalid or duplicate prefix unit")
                seen_prefix.add(i)
            elif len(clause) == 6 and all(t > 0 for t in clause):
                positions = [decode(t, n) for t in clause]
                i = positions[0][0]
                if i in seen_at_least or set(positions) != {(i,c) for c in range(1,7)}:
                    raise ValueError("invalid or duplicate at-least-one clause")
                seen_at_least.add(i)
            elif len(clause) == 2 and all(t < 0 for t in clause):
                (i,c),(j,d) = [decode(t,n) for t in clause]
                if i == j:
                    key = (i,min(c,d),max(c,d))
                    if c == d or key in seen_pairs:
                        raise ValueError("invalid or duplicate at-most-one clause")
                    seen_pairs.add(key)
                else:
                    x,z = sorted((i,j))
                    key = (x,x,c)
                    if c != d or z != 2*x or key in seen_triples:
                        raise ValueError("invalid or duplicate doubling clause")
                    seen_triples.add(key)
            elif len(clause) == 3 and all(t < 0 for t in clause):
                positions = sorted(decode(t,n) for t in clause)
                (x,c),(y,d),(z,e) = positions
                key = (x,y,c)
                if not (x < y and x+y == z and c == d == e) or key in seen_triples:
                    raise ValueError("invalid or duplicate distinct-summand clause")
                seen_triples.add(key)
            else:
                raise ValueError(f"unexpected clause: {clause}")
    expected = (n, 15*n, 6*(n*n//4), len(prefix))
    actual = (len(seen_at_least),len(seen_pairs),len(seen_triples),len(seen_prefix))
    if actual != expected or count != expected_count:
        raise ValueError(f"missing or extra clauses: {actual}, count={count}")
    print(f"PASS n={n} clauses={count} triples={n*n//4} prefix={len(prefix)}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("cnf", type=Path)
    parser.add_argument("--n", type=int, default=339)
    parser.add_argument("--prefix", type=Path, default=Path(__file__).with_name("prefix69.txt"))
    args = parser.parse_args()
    audit(args.cnf, args.prefix.read_text(encoding="ascii").strip(), args.n)


if __name__ == "__main__":
    main()
