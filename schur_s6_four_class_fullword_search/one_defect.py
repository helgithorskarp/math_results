"""Exact at-most-one-defect CNF for unrestricted four-class trades."""
import argparse
from pathlib import Path
from encode import make


def write(seed, fixed, target):
    old, free, domains, variables, clauses, schur_count = make(seed, fixed)
    clauses = clauses[:-schur_count]
    free_set = set(free)
    possible_triples = 0
    selectors = []
    next_var = len(variables)
    for z in range(2, 538):
        for x in range(1, z // 2 + 1):
            y = z - x
            vertices = sorted({x, y, z})
            common = set.intersection(*(domains[v] for v in vertices))
            if not common:
                continue
            next_var += 1
            selector = next_var
            selectors.append(selector)
            possible_triples += 1
            for c in sorted(common):
                clause = [-variables[v, c] for v in vertices if v in free_set]
                assert clause
                clauses.append(clause + [selector])
    assert len(selectors) > 1
    # Sinz sequential at-most-one counter on triple selectors.
    auxiliary = []
    for _ in range(len(selectors) - 1):
        next_var += 1
        auxiliary.append(next_var)
    clauses.append([-selectors[0], auxiliary[0]])
    for i in range(1, len(selectors) - 1):
        clauses.extend(([-selectors[i], auxiliary[i]],
                        [-auxiliary[i - 1], auxiliary[i]],
                        [-selectors[i], -auxiliary[i - 1]]))
    clauses.append([-selectors[-1], -auxiliary[-1]])
    with Path(target).open("w", encoding="ascii", newline="\n") as out:
        out.write(f"p cnf {next_var} {len(clauses)}\n")
        for clause in clauses:
            out.write(" ".join(map(str, clause)) + " 0\n")
    print(f"fixed={''.join(map(str,fixed))} free={len(free)} "
          f"variables={next_var} clauses={len(clauses)} "
          f"possible_triples={possible_triples} schur_clauses={schur_count}",
          flush=True)


if __name__ == "__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--fixed",required=True)
    p.add_argument("--seed",type=Path,required=True)
    p.add_argument("--cnf",type=Path,required=True)
    a=p.parse_args()
    assert len(a.fixed)==2
    write(a.seed,tuple(map(int,a.fixed)),a.cnf)
