"""Optional deterministic SAT discovery of positive complete-pair witnesses."""
from itertools import combinations
from pathlib import Path
import json,sys
from pysat.solvers import Solver
from model import build
P,E,_=build();n=len(P);pairs=set(combinations(range(n),2));missing_same=pairs-set(E);missing_different=set(pairs)
cnf=[]
v=lambda i,c:4*i+c+1
for i in range(n):
 cnf.append([v(i,c) for c in range(4)])
 for c,d in combinations(range(4),2):cnf.append([-v(i,c),-v(i,d)])
for i,j in E:
 for c in range(4):cnf.append([-v(i,c),-v(j,c)])
words=[]
with Solver(name='cadical195',bootstrap_with=cnf) as solver:
 while missing_same or missing_different:
  same=bool(missing_same);i,j=min(missing_same if same else missing_different)
  if not solver.solve(assumptions=[v(i,0),v(j,0 if same else 1)]):
   print(json.dumps({'status':'NONTRIVIAL RELATION SIGNAL - REQUIRE PROOF','pair':[i,j],'equal_request':same}));sys.exit(2)
  model=set(solver.get_model());w=[next(c for c in range(4) if v(i,c) in model) for i in range(n)]
  if any(w[i]==w[j] for i,j in E):raise ValueError('bad SAT decoder')
  words.append(''.join(map(str,w)))
  missing_same={p for p in missing_same if w[p[0]]!=w[p[1]]}
  missing_different={p for p in missing_different if w[p[0]]==w[p[1]]}
print(json.dumps({'status':'PAIR RELATIONS NEUTRAL','points':n,'edges':len(E),'words':len(words),'same_requests':len(pairs-set(E)),'different_requests':len(pairs)}))
Path(sys.argv[1]).write_text(json.dumps({'schema':'vnd-sqrt7-pair-v1','words':words},indent=2)+'\n')
