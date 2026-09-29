#!/usr/bin/env python3
"""Exact 536 SAT search minimizing one colour's 537-extension conflicts."""
import argparse
import time
from pathlib import Path

from pysat.card import ITotalizer
from pysat.solvers import Solver

from check import bad_triples, pair_counts, read_word


def var(v, colour):
    return 6 * (v - 1) + colour


def base_clauses():
    for v in range(1, 537):
        yield [var(v, c) for c in range(1, 7)]
        for a in range(1, 7):
            for b in range(a + 1, 7):
                yield [-var(v, a), -var(v, b)]
    for z in range(2, 537):
        for x in range(1, z // 2 + 1):
            y = z - x
            for c in range(1, 7):
                yield [-var(v, c) for v in sorted({x, y, z})]


def run(budget, target, outdir):
    baseline = read_word(Path(__file__).resolve().parent.parent /
                         "schur_s6_fredricksen_sweet_distance/baseline.txt", 536)
    assert not bad_triples(baseline)
    clauses = list(base_clauses())
    assert len(clauses) == 439520
    markers = []
    for x in range(1, 269):
        y = 537 - x
        marker = 3216 + x
        markers.append(marker)
        clauses.append([-var(x, target), -var(y, target), marker])
    outdir.mkdir(parents=True, exist_ok=True)
    print("baseline_pair_counts", pair_counts(baseline), flush=True)
    start = time.monotonic()
    with ITotalizer(lits=markers, ubound=32, top_id=3484) as totalizer:
        clauses.extend(totalizer.cnf.clauses)
        with Solver(name="cadical195", bootstrap_with=clauses) as solver:
            solver.set_phases([var(v, int(c)) for v, c in enumerate(baseline, 1)])
            bound = pair_counts(baseline)[target - 1] - 1
            while bound >= 0:
                solver.conf_budget(budget)
                status = solver.solve_limited(assumptions=[-totalizer.rhs[bound]],
                                              expect_interrupt=True)
                if status is not True:
                    # UNSAT needs a separately checked proof; a solver status
                    # alone establishes no lower bound on the pair count.
                    print("UNKNOWN" if status is None else "UNVERIFIED_UNSAT",
                          "bound", bound, "seconds", round(time.monotonic() - start, 2),
                          "conflicts", solver.accum_stats()["conflicts"], flush=True)
                    break
                positive = {lit for lit in solver.get_model() if lit > 0}
                word = "".join(str(next(c for c in range(1, 7)
                                        if var(v, c) in positive))
                               for v in range(1, 537))
                assert not bad_triples(word)
                count = pair_counts(word)[target - 1]
                assert count <= bound
                path = outdir / f"valid536-pairs{count}.txt"
                path.write_text(word + "\n")
                print("SAT", "bound", bound, "achieved", count,
                      "changes", sum(a != b for a, b in zip(word, baseline)),
                      "seconds", round(time.monotonic() - start, 2),
                      "out", path, flush=True)
                if count == 0:
                    complete = word + str(target)
                    assert not bad_triples(complete)
                    (outdir / "VERIFIED537.txt").write_text(complete + "\n")
                    print("VERIFIED537", flush=True)
                    break
                solver.set_phases([var(v, int(c)) for v, c in enumerate(word, 1)])
                bound = count - 1


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--budget", type=int, default=100000)
    parser.add_argument("--target", type=int, default=5)
    parser.add_argument("--outdir", type=Path, default=Path("/tmp/schur-six-reflected"))
    args = parser.parse_args()
    if args.budget <= 0 or not 1 <= args.target <= 6:
        parser.error("budget must be positive and target in 1,...,6")
    run(args.budget, args.target, args.outdir)
