"""Optional template discovery with OR-Tools 9.15.6755 (not a proof dependency).

T_x selects allowed coordinate residues, and E_uv selects quotient edges on
U x F_2 incident with centers in U x {0}. Selected edges imply allowed labels.
Domination and independence are explicit. Every affine cycle has at most three
selected edges. For each allowed missing boundary edge, a Boolean witness
requires all three other edges of an affine square. The decoder checks the
finite hypotheses independently. The objective only helps find sparse outside
incidences; no optimality/nonexistence claim is used by the theorem.
"""
from ortools.sat.python import cp_model
from itertools import combinations, permutations
from pathlib import Path
import json,time

def run(k,C,D,degree2=True,seconds=30,target_size=None):
 q=1<<k; n=2*q; A=set(C+D); m=cp_model.CpModel()
 T=[m.new_bool_var(f't{x}') for x in range(q)]
 m.add(T[0]==1)
 if target_size is not None:m.add(sum(T)==target_size)
 E={}
 for u,v in combinations(range(n),2):
  if not (u in A or v in A):continue
  if (u in C and v in C) or (u in D and v in D):continue
  E[u,v]=m.new_bool_var(f'e{u}_{v}')
  m.add(E[u,v]<=T[(u^v)&(q-1)])
 def ev(u,v):return E.get(tuple(sorted((u,v))))
 for cls in (C,D):
  for u in range(n):
   if u in cls:continue
   m.add(sum(ev(u,v) for v in cls if ev(u,v) is not None)>=1)
 if degree2:
  for u in range(q,n):m.add(sum(ev(u,a) for a in A)==2)
 # Faces are affine squares, with three cycle orderings for every plane.
 faces=set()
 for u in range(n):
  for v,w in combinations([x for x in range(n) if x!=u],2):
   x=u^v^w
   face=tuple(sorted((tuple(sorted((u,v))),tuple(sorted((v,x))),tuple(sorted((x,w))),tuple(sorted((w,u))))))
   if face in faces:continue
   faces.add(face)
   if all(e in E for e in face):m.add(sum(E[e] for e in face)<=3)
 # Every available missing boundary edge must have an affine three-edge path.
 for u,v in combinations(range(n),2):
  if not (u in A or v in A):continue
  witnesses=[]
  for w in range(n):
   if w in (u,v):continue
   x=u^v^w
   edges=[ev(u,w),ev(w,x),ev(x,v)]
   if any(e is None for e in edges):continue
   y=m.new_bool_var(f'w{u}_{v}_{w}')
   for e in edges:m.add(y<=e)
   witnesses.append(y)
  literals=[T[(u^v)&(q-1)].Not()]+witnesses
  if ev(u,v) is not None:literals.append(ev(u,v))
  m.add_bool_or(literals)
 el=[e for (u,v),e in E.items() if v>=q]
 m.maximize(1000*sum(T)-sum(el))
 s=cp_model.CpSolver();s.parameters.num_search_workers=1;s.parameters.max_time_in_seconds=seconds;s.parameters.random_seed=1
 start=time.monotonic();status=s.solve(m)
 out=dict(k=k,C=C,D=D,degree2=degree2,status=s.status_name(status),target_size=target_size,elapsed_seconds=time.monotonic()-start)
 if status in (cp_model.OPTIMAL,cp_model.FEASIBLE):
  out.update(T=[x for x in range(q) if s.value(T[x])],edges=[list(e) for e,y in E.items() if s.value(y)],outside_edges=sum(s.value(e) for e in el),objective=s.objective_value,bound=s.best_objective_bound)
 return out

if __name__ == '__main__':
 import argparse
 from check_templates import check
 parser=argparse.ArgumentParser(description=__doc__)
 parser.add_argument('--seconds',type=float,default=30)
 parser.add_argument('--output',type=Path,required=True)
 args=parser.parse_args()
 r=run(4,[0,1],[2,4,8],degree2=False,seconds=args.seconds,target_size=10)
 if 'edges' not in r:raise RuntimeError('no witness found within the requested budget')
 edges=r['edges'];q=16
 t={'name':'F','k':4,'C':r['C'],'D':r['D'],'T':r['T'],
    'core_edges':[e for e in edges if e[1]<q],
    'outside_neighbors':[[a for a in sorted(r['C']+r['D']) if [a,x+q] in edges]
                         for x in range(q)]}
 verified=check(t)
 args.output.write_text(json.dumps(t,indent=2)+'\n')
 print(json.dumps({'solver_status':r['status'],'outside_edges':r['outside_edges'],
                   'verified_certificate':verified},sort_keys=True))
