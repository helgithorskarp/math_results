"""Alternative solver probe; any SAT model is checked as a complete word."""
import argparse
import time
from pathlib import Path

from pysat.formula import CNF
from pysat.solvers import Solver

from encode import make


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--fixed", required=True)
    p.add_argument("--budget", type=int, default=1_000_000)
    p.add_argument("--seed", type=Path, required=True)
    p.add_argument("--cnf", type=Path, required=True)
    p.add_argument("--out", type=Path, required=True)
    p.add_argument("--max-defects", type=int, default=0)
    p.add_argument("--phase-hint", action="store_true")
    a = p.parse_args()
    old, free, _, variables, _, _ = make(a.seed, tuple(map(int, a.fixed)))
    problem = CNF(from_file=str(a.cnf))
    start = time.monotonic()
    with Solver(name="g3", bootstrap_with=problem.clauses) as solver:
        if a.phase_hint:
            fixed_set = set(map(int, a.fixed))
            free_labels = [c for c in range(1, 7) if c not in fixed_set]
            seen = []
            for v in free:
                if old[v] not in seen:
                    seen.append(old[v])
            rename = dict(zip(seen, free_labels))
            solver.set_phases([variable if d == rename[old[v]] else -variable
                               for (v, d), variable in variables.items()])
        solver.conf_budget(a.budget)
        result = solver.solve_limited(expect_interrupt=True)
        elapsed = time.monotonic() - start
        print(f"fixed={a.fixed} result={result} elapsed={elapsed:.2f} "
              f"stats={solver.accum_stats()}", flush=True)
        if result is True:
            model = set(solver.get_model())
            colour = old.copy()
            for v in free:
                chosen = [d for (u, d), variable in variables.items()
                          if u == v and variable in model]
                assert len(chosen) == 1
                colour[v] = chosen[0]
            defects = [(x, y, x + y) for x in range(1, 538)
                       for y in range(x, 538 - x)
                       if colour[x] == colour[y] == colour[x + y]]
            assert len(defects) <= a.max_defects
            word = "".join(map(str, colour[1:]))
            a.out.write_text(word + "\n")
            print(f"VERIFIED_WORD defects={len(defects)} triples={defects} "
                  f"word={word}", flush=True)


if __name__ == "__main__":
    main()
