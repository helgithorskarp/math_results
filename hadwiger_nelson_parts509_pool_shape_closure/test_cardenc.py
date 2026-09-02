#!/usr/bin/env python3
"""Tests for cardenc.py: the encodings must be satisfiable exactly on the intended
assignments (soundness *and* completeness), since an UNSAT answer on a CNF containing them
is what certifies a closure."""
import itertools, random, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import cardenc
from pysat.solvers import Solver


def check(cl, lits, pred, samples):
    for asg in samples:
        s = Solver(name='minisat22', bootstrap_with=cl)
        r = s.solve(assumptions=[l if b else -l for l, b in zip(lits, asg)])
        s.delete()
        assert r == pred(sum(asg)), (lits, asg, r)


def main():
    for n in range(1, 9):
        lits = list(range(1, n + 1))
        all_asg = list(itertools.product([0, 1], repeat=n))
        for k in range(0, n + 2):
            cl, _ = cardenc.equals_cheap(lits, k, n)
            check(cl, lits, lambda t, k=k: t == k, all_asg)
            cl, _ = cardenc.atmost(lits, k, n)
            check(cl, lits, lambda t, k=k: t <= k, all_asg)
            cl, _ = cardenc.atleast_direct(lits, k, n)
            check(cl, lits, lambda t, k=k: t >= k, all_asg)
            cl, _ = cardenc.equals_tot(lits, k, n)
            check(cl, lits, lambda t, k=k: t == k, all_asg)
    print('exhaustive n <= 8: ok')
    rng = random.Random(1)
    for _ in range(40):
        n = rng.randint(20, 180)
        k = rng.randint(0, min(n, 50))
        lits = list(range(1, n + 1))
        cl, _ = cardenc.equals_tot(lits, k, n)
        samples = []
        for _ in range(15):
            m = rng.randint(0, n)
            on = set(rng.sample(lits, m))
            samples.append(tuple(1 if l in on else 0 for l in lits))
        check(cl, lits, lambda t, k=k: t == k, samples)
    print('random n <= 180: ok')


if __name__ == '__main__':
    main()
