"""Bounded SAT construction search in a listed alignment union."""
import argparse
import json
import time
from pathlib import Path

from pysat.solvers import Solver

from check import defects
from encode import HERE, make


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--case',required=True)
    p.add_argument('--budget',type=int,default=200000)
    p.add_argument('--solver',default='cadical195')
    p.add_argument('--out',type=Path,default=Path('/tmp/schur-537-candidate.txt'))
    a=p.parse_args()
    alignment,domains,var,clauses,_,_=make(a.case)
    sources=json.loads((HERE/'sources.json').read_text(encoding='ascii'))
    name,perm=alignment[0]
    hint=''.join(perm[int(d)-1] for d in sources[name]['word'])
    start=time.monotonic()
    with Solver(name=a.solver,bootstrap_with=clauses) as solver:
        solver.set_phases([var[v,c] if c==int(hint[v-1]) else -var[v,c]
                           for (v,c) in var])
        solver.conf_budget(a.budget)
        result=solver.solve_limited(expect_interrupt=True)
        print(f'case={a.case} result={result} elapsed={time.monotonic()-start:.2f} '
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
            print('UNVERIFIED_UNSAT; proof required for an exclusion',flush=True)
        else:
            print('UNKNOWN; conflict budget exhausted',flush=True)


if __name__=='__main__': main()
