"""Optional positive-word production; negative solver answers prove nothing here."""
import json,argparse
from pathlib import Path
from itertools import combinations
from pysat.solvers import Solver
import model as m
from scan import run

def produce(work,output):
    _,residual=run(work);cert=[]
    for row in residual:
        edges=row.pop('edge_list');clauses=[]
        for v in range(508):
            clauses.append([4*v+c+1 for c in range(4)])
            for a,b in combinations(range(4),2):clauses.append([-4*v-a-1,-4*v-b-1])
        for i,j in edges:
            for c in range(4):clauses.append([-4*i-c-1,-4*j-c-1])
        with Solver(name='cadical195',bootstrap_with=clauses) as s:
            s.conf_budget(1000000);sat=s.solve_limited();m.require(sat is True,'residual is UNSAT or UNKNOWN: exact physical reconstruction required')
            model={t for t in s.get_model() if t>0};word=''.join(str(next(c for c in range(4) if 4*v+c+1 in model)) for v in range(508))
        m.word_check(word,edges);cert.append(row|{'word':word})
    Path(output).write_text(json.dumps(cert,indent=2)+'\n');print('positive words',len(cert),flush=True)
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--work',type=Path,required=True);ap.add_argument('--output',type=Path,required=True);a=ap.parse_args();produce(a.work,a.output)
