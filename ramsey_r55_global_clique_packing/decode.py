"""Accept a solver model only if its complete physical graph is good43."""
from itertools import combinations
from pathlib import Path
import argparse,json
import model,verify_target

def decode(branch,text):
 p=model.Packing(branch);status=[line for line in text.splitlines() if line.startswith('s ')]
 if status!=['s SATISFIABLE']:raise ValueError('exact SAT status required')
 values={}
 for line in text.splitlines():
  if line.startswith('v '):
   for token in line.split()[1:]:
    x=int(token)
    if x==0:continue
    if abs(x) in values and values[abs(x)]!=(x>0):raise ValueError('inconsistent model')
    values[abs(x)]=x>0
 if set(values)!=set(range(1,848)) or not values[1]:raise ValueError('complete model with true constant required')
 if not all(any(values[abs(x)]==(x>0) for x in clause) for clause in p.root_clauses()):raise ValueError('SAT claim violates root normalization')
 bits=0
 for k,pair in enumerate(combinations(range(43),2)):
  color=p.fixed[pair] if pair in p.fixed else values[p.variables[pair]]
  bits|=int(color)<<k
 graph={'n':43,'red_hex':format(bits,'0226x')};result=verify_target.count(graph)
 if result['status']!='VERIFIED_GOOD43':raise ValueError('SAT claim fails physical target check')
 return graph

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--branch',required=True);p.add_argument('--solver-output',required=True);p.add_argument('--output',required=True);a=p.parse_args();out=Path(a.output)
 if out.exists():raise ValueError('output exists')
 graph=decode(list(map(int,a.branch.split(','))),Path(a.solver_output).read_text());out.write_text(json.dumps(graph,indent=2,sort_keys=True)+'\n');print('VERIFIED_GOOD43')
