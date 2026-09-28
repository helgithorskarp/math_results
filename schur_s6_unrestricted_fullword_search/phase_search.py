"""Unrestricted CaDiCaL search seeded by a complete near-colouring."""
import argparse
import tempfile
import time
from pathlib import Path

from pysat.formula import CNF
from pysat.solvers import Solver

from check import defects
from encode import write

HERE=Path(__file__).resolve().parent


def normalize_first(word):
    order=word[0]+''.join(c for c in '123456' if c!=word[0])
    translation={c:str(i) for i,c in enumerate(order,1)}
    return ''.join(translation[c] for c in word)


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--source',type=Path,default=HERE/'best4.txt')
    p.add_argument('--conflicts',type=int,default=1000000)
    p.add_argument('--out',type=Path,default=Path('/tmp/schur-six-537-word.txt'))
    a=p.parse_args()
    assert a.conflicts>0
    word=normalize_first(a.source.read_text(encoding='ascii').strip())
    assert len(word)==537 and set(word)==set('123456')
    print('start_defects',defects(word),flush=True)
    with tempfile.TemporaryDirectory(prefix='schur-six-phase-') as temp:
        path=Path(temp)/'plain.cnf'
        write(path,'plain')
        cnf=CNF(from_file=str(path))
        with Solver(name='cadical195',bootstrap_with=cnf.clauses) as solver:
            phases=[]
            for v in range(1,538):
                for c in range(1,7):
                    lit=6*(v-1)+c
                    phases.append(lit if str(c)==word[v-1] else -lit)
            solver.set_phases(phases)
            solver.conf_budget(a.conflicts)
            start=time.monotonic()
            result=solver.solve_limited(expect_interrupt=True)
            print('result',result,'seconds',round(time.monotonic()-start,2),
                  'conflicts',solver.accum_stats().get('conflicts'),flush=True)
            if result is True:
                positive={lit for lit in solver.get_model() if lit>0}
                candidate=''.join(str(next(c for c in range(1,7)
                                            if 6*(v-1)+c in positive))
                                  for v in range(1,538))
                assert not defects(candidate)
                a.out.write_text(candidate+'\n',encoding='ascii')
                print('VERIFIED_537',candidate,'out',a.out,flush=True)
            elif result is False:
                print('UNVERIFIED_UNSAT; no proof generated',flush=True)
            else:
                print('UNKNOWN; conflict budget exhausted',flush=True)


if __name__=='__main__':main()
