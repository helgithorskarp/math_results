"""Bounded SAT search across arbitrary global alignments of the five words."""
import argparse
import time
from pathlib import Path

from pysat.solvers import Solver

from check import defects
from encode import make


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--set',action='append',default=[],metavar='NAME=PERM')
    p.add_argument('--budget',type=int,default=200000)
    p.add_argument('--solver',default='cadical195')
    p.add_argument('--out',type=Path,default=Path('/tmp/schur-537-candidate.txt'))
    a=p.parse_args()
    overrides=dict(item.split('=',1) for item in a.set)
    assert len(overrides)==len(a.set)
    _,aligned,domains,var,clauses,_,_=make(overrides)
    start=time.monotonic()
    with Solver(name=a.solver,bootstrap_with=clauses) as solver:
        hint=aligned[0]
        solver.set_phases([var[v,c] if c==int(hint[v-1]) else -var[v,c]
                           for (v,c) in var])
        solver.conf_budget(a.budget)
        result=solver.solve_limited(expect_interrupt=True)
        print(f'result={result} elapsed={time.monotonic()-start:.2f} '
              f'stats={solver.accum_stats()}',flush=True)
        if result is True:
            model=set(solver.get_model())
            word=''.join(str(next(c for c in domains[v] if var[v,c] in model))
                         for v in range(1,538))
            bad=defects(word)
            assert not bad,bad
            a.out.write_text(word+'\n',encoding='ascii')
            print(f'VERIFIED_537 word={word} out={a.out}',flush=True)
        elif result is False:
            print('UNVERIFIED_UNSAT; use verify.py and its DRAT check for the default alignment',flush=True)
        else:
            print('UNKNOWN; conflict budget exhausted',flush=True)


if __name__=='__main__': main()
