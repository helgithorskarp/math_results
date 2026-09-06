#!/usr/bin/env python3
"""Replay two abstract solver-interface controls; not geometric constructions."""
import argparse
import json
from pathlib import Path
import subprocess
import sys

HERE=Path(__file__).resolve().parent


def run(out):
    out.mkdir(exist_ok=False);result=[]
    for order,expected in [(4,'SAT'),(5,'UNSAT')]:
        clauses=[[4*v+c+1 for c in range(4)] for v in range(order)]
        clauses += [[-4*u-c-1,-4*v-c-1] for u in range(order) for v in range(u+1,order) for c in range(4)]
        f=out/f'K{order}.cnf'
        f.write_text(f'p cnf {4*order} {len(clauses)}\n'+''.join(' '.join(map(str,c))+' 0\n' for c in clauses))
        answer=out/f'K{order}.json'
        subprocess.run([sys.executable,'-B',str(HERE/'pilot.py'),'--worker',str(f),'--answer',str(answer)],check=True,timeout=60)
        x=json.loads(answer.read_text())
        if x['status']!=expected:raise ValueError('solver control status')
        if expected=='SAT':
            truth={v for v in x['model'] if v>0}
            colours=[min(k for k in range(4) if 4*v+k+1 in truth) for v in range(order)]
            if len(set(colours))!=order:raise ValueError('K4 positive witness')
        result.append(dict(abstract_graph=f'K{order}',expected=expected,actual=x['status'],model_directly_checked=expected=='SAT'))
    print(json.dumps(dict(solver_controls=result,not_unit_distance_constructions=True),sort_keys=True))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);a=p.parse_args();run(a.out)
