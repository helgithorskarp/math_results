from encode import Formula,build,decode
from itertools import product,combinations_with_replacement
from pathlib import Path
from pysat.solvers import Solver
import json,time
p=Path(__file__).resolve().parent;t=time.monotonic();counter_checks=0;color_checks=0
for n in range(0,9):
 for k in range(n+1):
  f=Formula(n);f.atmost(list(range(1,n+1)),k)
  with Solver(name='g3',bootstrap_with=f.clauses) as solver:
   for bits in product([False,True],repeat=n):
    ok=solver.solve(assumptions=[i+1 if v else -(i+1) for i,v in enumerate(bits)])
    assert ok==(sum(bits)<=k),(n,k,bits,ok);counter_checks+=1
for domain in [list(range(n)) for n in range(2,7)]+[[0,2,3,7,8],[0,1,4,6,11,13]]:
 n=len(domain)
 for q in [2,3]:
  profiles=[s for s in product(range(n+1),repeat=q) if sum(s)==n and tuple(sorted(s,reverse=True))==s]
  for sizes in profiles:
   for symmetry in [False,True]:
    models={}
    for kind in ['difference','sums']:
     f,m=build(domain,list(sizes),kind,symmetry);count=0
     with Solver(name='g3',bootstrap_with=f.clauses) as solver:
      for colors in product(range(q),repeat=n):
       rows=[[x for x,c in zip(domain,colors) if c==j] for j in range(q)]
       expected=all(len(a)==s for a,s in zip(rows,sizes))
       expected &= all(len(set(x+y for x,y in combinations_with_replacement(a,2)))==len(a)*(len(a)+1)//2 for a in rows)
       if symmetry:
        expected &= all(not rows[c] or (rows[c-1] and min(rows[c-1])<min(rows[c])) for c in range(1,q) if sizes[c]==sizes[c-1])
       expected=bool(expected)
       ok=solver.solve(assumptions=[i*q+c+1 for i,c in enumerate(colors)])
       assert ok==expected,(domain,sizes,symmetry,kind,colors,ok,expected)
       if ok:assert decode(solver.get_model(),m)==rows;count+=1
       color_checks+=1
     models[kind]=count
    assert models['difference']==models['sums']
report={'counter_assignments_checked':counter_checks,'color_assignments_checked':color_checks,'both_encodings':True,'symmetry_on_and_off':True,'seconds':time.monotonic()-t}
print(json.dumps(report))
