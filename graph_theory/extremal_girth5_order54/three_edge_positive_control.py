from pathlib import Path
from itertools import permutations
from collections import Counter,defaultdict
import json
from pysat.solvers import Solver
from three_edge_sat import build
from three_quad_orbits import reps
S=Path(__file__).resolve().parent
from four_edge_orbits import forest
from verify_four_edge_layer import witness

def check_fixture(r):
 witness(r)
 old={i:(d,frozenset(B),j) for i,d,B,j in r['vertices']};qs=[i for i,(d,B,j) in old.items() if len(B)==4];degrees=[old[i][0] for i in qs]
 n6=degrees.count(6);n7=degrees.count(7);oldcolors={t:tuple(j for j,q in enumerate(qs) if t in old[q][1]) for t in range(12)}
 found=[]
 for orbit,Qs in enumerate(reps(n6,n7)):
  for perm in permutations(range(len(qs))):
   if any(degrees[j]!=(6 if perm[j]<n6 else 7) for j in range(len(qs))):continue
   A=defaultdict(list);B=defaultdict(list)
   for t in range(12):
    A[tuple(sorted(perm[j] for j in oldcolors[t]))].append(t)
    B[tuple(j for j,Q in enumerate(Qs) if t in Q)].append(t)
   if {k:len(v) for k,v in A.items()}!={k:len(v) for k,v in B.items()}:continue
   mapping={u:v for color in A for u,v in zip(A[color],B[color])};found.append((orbit,mapping));break
 if len(found)!=1:raise ValueError('Fixture orbit')
 orbit,point=found[0];cnf,data=build(r['case'][0],orbit,stage=r['stage'],expected_m=4)
 slots={(d,B,j):i for i,(d,B,j) in enumerate(data['vertices'])}
 vertex={i:slots[d,frozenset(point[t] for t in B),j] for i,(d,B,j) in old.items()}
 chosen=set(vertex.values());H={tuple(sorted((point[a],point[b]))) for a,b in forest(r['case'][1])}
 N={tuple(sorted((vertex[a],vertex[b]))) for a,b in r['near']};F={tuple(sorted((vertex[a],vertex[b]))) for a,b in r['far']}
 covers={(vertex[v],tuple(sorted(vertex[u] for u in fs))) for v,fs in r['covers']};bad={v for v,fs in covers}
 assumptions=[x if i in chosen else -x for i,x in enumerate(data['X'])]
 for name,selected in [('H',H),('N',N),('F',F),('bad',bad)]:assumptions.extend(v if key in selected else -v for key,v in data[name].items())
 assumptions.extend(c if (v,tuple(sorted(fs))) in covers else -c for c,(v,fs) in data['covers'].items())
 with Solver(name='g4',bootstrap_with=cnf) as solver:
  if not solver.solve(assumptions=assumptions):raise ValueError('Valid independent fixture rejected')
 return dict(original_case=r['case'],stage=r['stage'],new_quad_orbit=orbit,variables=cnf.nv,clauses=len(cnf.clauses),fixed_main_literals=len(assumptions),accepted=True)
