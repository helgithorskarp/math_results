"""Bounded full Schur SAT for four-class trades of a 537-word."""
from itertools import combinations
from pathlib import Path
import argparse
import time
from pysat.solvers import Solver

p=argparse.ArgumentParser()
p.add_argument('input',type=Path)
p.add_argument('--defect-colour',type=int,required=True)
p.add_argument('--budget',type=int,default=100000)
a=p.parse_args()
s=a.input.read_text().strip()
if len(s)!=537 or set(s)!=set('123456') or not 1<=a.defect_colour<=6:
 raise ValueError('invalid word or defect colour')
v=lambda i,c:6*(i-1)+c
clauses=[]
for i in range(1,538):
 clauses.append([v(i,c) for c in range(1,7)])
 for c in range(1,7):
  for d in range(1,c):clauses.append([-v(i,c),-v(i,d)])
for x in range(1,538):
 for y in range(x,538-x):
  for c in range(1,7):clauses.append(sorted(set((-v(x,c),-v(y,c),-v(x+y,c)))))
phases=[v(i,c) if int(s[i-1])==c else -v(i,c)
        for i in range(1,538) for c in range(1,7)]
with Solver(name='cadical195',bootstrap_with=clauses) as solver:
 solver.set_phases(phases)
 for other in combinations([c for c in range(1,7) if c!=a.defect_colour],3):
  palette={a.defect_colour,*other}
  assumptions=[]
  for i in range(1,538):
   old=int(s[i-1])
   if old in palette:
    assumptions.extend(-v(i,c) for c in range(1,7) if c not in palette)
   else:assumptions.append(v(i,old))
  solver.conf_budget(a.budget)
  start=time.monotonic()
  result=solver.solve_limited(assumptions=assumptions,expect_interrupt=True)
  print('palette',''.join(map(str,sorted(palette))),'result',result,
        'seconds',round(time.monotonic()-start,2),
        'conflicts',solver.accum_stats()['conflicts'],
        'core',len(solver.get_core() or []) if result is False else '-',flush=True)
  if result is True:
   model=set(solver.get_model())
   word=''.join(str(next(c for c in range(1,7) if v(i,c) in model)) for i in range(1,538))
   col=[0]+[int(c) for c in word]
   bad=[(x,y,x+y) for x in range(1,538) for y in range(x,538-x) if col[x]==col[y]==col[x+y]]
   if bad:raise ValueError(('bad model',bad[:5]))
   print('VERIFIED_537_COLOURING',word,flush=True)
   break
