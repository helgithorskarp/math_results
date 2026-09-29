"""Three symmetry-complete SAT branches for classical Schur six at 537."""
import argparse
import hashlib
from pathlib import Path

N = 537
K = 6
TRIPLES = 72092
CLAUSES = 441147


def var(v, c):
    return K * (v - 1) + c


def write(path, branch):
    if branch not in (1, 2, 3):
        raise ValueError("branch must be 1, 2, or 3")
    count = 0
    triples = 0
    with Path(path).open("w", encoding="ascii", newline="\n") as stream:
        stream.write(f"p cnf {N*K} {CLAUSES}\n")

        def clause(lits):
            nonlocal count
            stream.write(" ".join(map(str, lits)) + " 0\n")
            count += 1

        clause([var(1, 1)])
        for v in range(1, N + 1):
            clause([var(v, c) for c in range(1, K + 1)])
            for c in range(1, K + 1):
                for d in range(c + 1, K + 1):
                    clause([-var(v, c), -var(v, d)])
        for z in range(2, N + 1):
            for x in range(1, z // 2 + 1):
                y = z - x
                triples += 1
                for c in range(1, K + 1):
                    clause([-var(v, c) for v in sorted({x, y, z})])
        clause([var(2, 2)])
        clause([var(N, branch)])
    assert triples == TRIPLES and count == CLAUSES
    digest = hashlib.sha256(Path(path).read_bytes()).hexdigest()
    return {"branch": branch, "vars": N*K, "clauses": count,
            "triples": triples, "sha256": digest}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("branch", type=int, choices=(1, 2, 3))
    parser.add_argument("cnf", type=Path)
    args = parser.parse_args()
    print(write(args.cnf, args.branch))
