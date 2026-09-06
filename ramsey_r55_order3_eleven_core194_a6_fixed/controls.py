#!/usr/bin/env python3
"""Evidence-status controls; mathematical formula/model controls are inherited."""
from pathlib import Path
import argparse
import json
import subprocess
import run


def main():
    p=argparse.ArgumentParser(); p.add_argument('--work',type=Path,required=True)
    p.add_argument('--drat-trim',type=Path,required=True); a=p.parse_args()
    work=a.work.resolve(); run.need(not work.is_relative_to(run.ROOT.parent),'external controls')
    work.mkdir(parents=True,exist_ok=True)
    for code,token in [(0,'UNKNOWN'),(10,'SATISFIABLE'),(20,'UNSATISFIABLE')]:
        run.terminal(code,'c diagnostic\ns '+token+'\n')
    rejected=[]
    for name,code,text in [('no_status',20,''),('wrong_status',20,'s UNKNOWN\n'),('wrong_exit',10,'s UNSATISFIABLE\n'),
        ('duplicate_status',20,'s UNSATISFIABLE\ns UNSATISFIABLE\n'),('conflicting_status',20,'s SATISFIABLE\ns UNSATISFIABLE\n'),
        ('crash',-9,'s UNSATISFIABLE\n'),('substring_only',20,'c s UNSATISFIABLE\n')]:
        try: run.terminal(code,text)
        except ValueError: rejected.append(name)
        else: raise ValueError('accepted '+name)
    # Complete DRAT must reject an empty-clause claim on a satisfiable formula.
    cnf=work/'sat.cnf'; trace=work/'false.drat'
    cnf.write_text('p cnf 1 1\n1 0\n'); trace.write_text('0\n')
    with (work/'false.log').open('w') as log:
        p=subprocess.run([str(a.drat_trim),str(cnf),str(trace),'-t','10'],stdout=log,stderr=subprocess.STDOUT,timeout=20)
    out=(work/'false.log').read_text()
    run.need(p.returncode != 0 and 's VERIFIED' not in out,'invalid full proof rejected')
    run.atomic(work/'controls.json',dict(status_inputs_rejected=rejected,false_refutation_rejected=True))
    print('PASS seven status controls and invalid full DRAT proof')


if __name__=='__main__': main()
