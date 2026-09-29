"""Regenerate a bounded Glucose-4 DRUP proof and check it independently."""
import argparse
import json
import threading
from pathlib import Path

import audit
import encode


if __name__=='__main__':
    from pysat.solvers import Solver
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--drat-trim',type=Path,required=True)
    parser.add_argument('--seconds',type=int,default=120)
    parser.add_argument('--conflicts',type=int,default=1000000)
    a=parser.parse_args();audit.require(a.seconds>0 and a.conflicts>0,'positive limits')
    a.output.mkdir(parents=True,exist_ok=True)
    cnf=a.output/'capacity.cnf';proof=a.output/'capacity.drup'
    cnf.write_bytes(encode.dimacs());audit.audit(cnf)
    variables,clauses=encode.formula()
    with Solver(name='glucose4',bootstrap_with=clauses,with_proof=True) as solver:
        solver.conf_budget(a.conflicts)
        timer=threading.Timer(a.seconds,solver.interrupt);timer.start()
        try:answer=solver.solve_limited(expect_interrupt=True)
        finally:timer.cancel();timer.join()
        audit.require(answer is False,'solver did not finish UNSAT; no exclusion claimed')
        lines=solver.get_proof();size=sum(len(line)+1 for line in lines)
        audit.require(size<=128*1024*1024,'proof exceeds local 128 MiB cap')
        proof.write_text('\n'.join(lines)+'\n');del lines
    result=audit.audit(cnf,proof,a.drat_trim.resolve(),a.seconds)
    (a.output/'audit.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
