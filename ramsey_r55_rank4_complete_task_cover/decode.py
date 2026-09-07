"""Decode a SAT task only after checking base gates and all physical five-sets."""
import argparse
import json
from pathlib import Path
import model
import verify_target


def decode(code,text):
    task=model.target(code)
    statuses=[line for line in text.splitlines() if line.startswith('s ')]
    if statuses!=['s SATISFIABLE']:raise ValueError('SAT status required')
    values={}
    for line in text.splitlines():
        if line.startswith('v '):
            for token in line.split()[1:]:
                literal=int(token)
                if not literal:continue
                if abs(literal) in values and values[abs(literal)]!=(literal>0):raise ValueError('conflicting model')
                values[abs(literal)]=literal>0
    if set(values)!=set(range(1,task.variables+1)):raise ValueError('complete task assignment required')
    if any(not any(values[abs(x)]==(x>0) for x in c) for c in task.base):raise ValueError('base/gate clause failure')
    columns=[]
    for row in task.labels:
        choices=[x for x,v in enumerate(row) if values[v]]
        if len(choices)!=1:raise ValueError('one-hot label failure')
        columns.append(choices[0])
    bits=sum(int(values[v])<<k for k,v in enumerate(task.internal.values()))
    graph=task.graph(columns,bits);verification=verify_target.count(graph)
    if verification['status']!='VERIFIED_GOOD43':raise ValueError('SAT claim fails physical target verification')
    return {'parameters':{'row_code':code,'columns':columns,'internal_hex':format(bits,'0111x')},'graph':graph,'verification':verification}


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--row-code',required=True,type=int);p.add_argument('--solver-output',required=True);p.add_argument('--output',required=True)
    a=p.parse_args();out=Path(a.output)
    if out.exists():raise ValueError('output already exists')
    result=decode(a.row_code,Path(a.solver_output).read_text());out.write_text(json.dumps(result['graph'],indent=2,sort_keys=True)+'\n')
    print('VERIFIED_GOOD43')
