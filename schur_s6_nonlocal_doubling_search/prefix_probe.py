"""Full Schur SAT with only a given colouring's first p entries fixed."""
import argparse
import time
from pathlib import Path
from pysat.solvers import Solver

p=argparse.ArgumentParser()
p.add_argument('input',type=Path)
p.add_argument('--prefix',type=int,required=True)
p.add_argument('--budget',type=int,default=100000)
a=p.parse_args()
s=a.input.read_text().strip()
if len(s)!=537 or set(s)!=set('123456') or not 0<=a.prefix<=537:
 raise ValueError('invalid word or prefix length')
v=lambda i,c:6*(i-1)+c
clauses=[]
for i in range(1,538):
 clauses.append([v(i,c) for c in range(1,7)])
 for c in range(1,7):
  for d in range(1,c):clauses.append([-v(i,c),-v(i,d)])
for x in range(1,538):
 for y in range(x,538-x):
  for c in range(1,7):clauses.append(sorted(set((-v(x,c),-v(y,c),-v(x+y,c)))))
phase=[v(i,c) if int(s[i-1])==c else -v(i,c)
       for i in range(1,538) for c in range(1,7)]
assumptions=[v(i,int(s[i-1])) for i in range(1,a.prefix+1)]
with Solver(name='cadical195',bootstrap_with=clauses) as solver:
 solver.set_phases(phase)
 solver.conf_budget(a.budget)
 start=time.monotonic()
 result=solver.solve_limited(assumptions=assumptions,expect_interrupt=True)
 print('prefix',a.prefix,'result',result,'seconds',round(time.monotonic()-start,2),
       'stats',solver.accum_stats(),flush=True)
 if result is False:print('core',len(solver.get_core() or []),flush=True)
 if result is True:
  model=set(solver.get_model());word=''.join(str(next(c for c in range(1,7) if v(i,c) in model)) for i in range(1,538))
  col=[0]+[int(c) for c in word]
  bad=[(x,y,x+y) for x in range(1,538) for y in range(x,538-x) if col[x]==col[y]==col[x+y]]
  if bad:raise ValueError(('bad model',bad[:5]))
  print('VERIFIED_537_COLOURING',word,flush=True)
