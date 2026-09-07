"""Untrusted deterministic clause discovery; only verify.py and check_rup.py certify it.

Python 3.12, python-sat 1.9.dev15, bundled CaDiCaL 1.9.5.
Generated formulas, witnesses, and traces belong in an external work directory.
"""
from itertools import combinations
from pathlib import Path
import json,time,sys
from pysat.solvers import Cadical195
import argparse
parser=argparse.ArgumentParser(description="Produce geometric collision clauses for the critical shift graph W4.")
parser.add_argument("work",type=Path)
args=parser.parse_args()
w=args.work.resolve();w.mkdir(parents=True,exist_ok=True)

def source(k):
 N=2**k+1;I=[(2**l,2**k-2**(k-l)+2) for l in range(k+1)]
 V=[(i,j) for i,j in combinations(range(1,N+1),2) if any(a<=i<j<=b for a,b in I)]
 E=[(a,b) for a,b in combinations(range(len(V)),2) if V[a][1]==V[b][0] or V[b][1]==V[a][0]]
 return V,E

def wheel(nb,center):
 sub=nb[center];colour={};par={}
 for root in sorted(sub):
  if root in colour:continue
  colour[root]=0;par[root]=None;q=[root]
  for u in q:
   for v in sorted(nb[u]&sub):
    if v not in colour:colour[v]=1-colour[u];par[v]=u;q.append(v)
    elif colour[v]==colour[u]:
     a=[];p=u
     while p is not None:a.append(p);p=par[p]
     b=[];p=v
     while p not in a:b.append(p);p=par[p]
     cyc=a[:a.index(p)+1]+b[::-1]
     if len(cyc)%2!=1:raise ValueError('not odd')
     return cyc
 return None

k=4
V,E=source(k);n=len(V);pairs=list(combinations(range(n),2));var={p:i+1 for i,p in enumerate(pairs)}
def eq(a,b):
 if a==b:return None
 return var[tuple(sorted((a,b)))]
nb=[set() for _ in V]
for a,b in E:nb[a].add(b);nb[b].add(a)
clauses=[]
for a,b,c in combinations(range(n),3):
 x,y,z=eq(a,b),eq(a,c),eq(b,c);clauses.extend([[-x,-y,z],[-x,-z,y],[-y,-z,x]])
clauses.extend([[-eq(a,b)] for a,b in E])
original=[]
for a,b in pairs:
 for tri in combinations(sorted(nb[a]&nb[b]),3):
  c,d,e=tri;clauses.append([eq(a,b),eq(c,d),eq(c,e),eq(d,e)]);original.append([a,b,*tri])
print(json.dumps({'k':k,'vertices':n,'edges':len(E),'vars':len(var),'clauses':len(clauses),'original_k23':len(original)}),flush=True)
learned=[];start=time.time();budget=2000000
with Cadical195(bootstrap_with=clauses) as s:
 for iteration in range(1000):
  s.conf_budget(budget);ok=s.solve_limited();print(json.dumps({'iteration':iteration,'status':str(ok),'seconds':round(time.time()-start,3),'clauses':len(clauses)}),flush=True)
  if ok is not True:
   result={'status':str(ok),'iteration':iteration,'seconds':time.time()-start};break
  model=set(s.get_model());rep=[]
  for a in range(n):rep.append(next((b for b in range(a) if eq(a,b) in model),a))
  if any(rep[rep[a]]!=rep[a] for a in range(n)):raise ValueError('bad equivalence')
  qnb={a:set() for a in sorted(set(rep))};witness={}
  for a,b in E:
   c,d=rep[a],rep[b]
   if c==d:raise ValueError('edge collapse')
   if c>d:c,d=d,c;a,b=b,a
   qnb[c].add(d);qnb[d].add(c);witness.setdefault((c,d),(a,b))
  def premises(qedges):
   es=[];pv=[]
   for c,d in qedges:
    if c>d:c,d=d,c
    a,b=witness[c,d];es.append([c,d,a,b])
    for u,v in [(c,a),(d,b)]:
     if u!=v:pv.append(-eq(u,v))
   return es,pv
  new=[]
  # One odd wheel per quotient centre, already including all detected K4s.
  for c in qnb:
   cyc=wheel(qnb,c)
   if cyc:
    ed=[(c,a) for a in cyc]+list(zip(cyc,cyc[1:]+cyc[:1]));ws,cl=premises(ed)
    rec={'kind':'wheel','center':c,'cycle':cyc,'witnesses':ws};new.append((cl,rec))
  # Quotient common-neighbour exclusions, all triples for a complete finite gate.
  for a,b in combinations(qnb,2):
   for c,d,e in combinations(sorted(qnb[a]&qnb[b]),3):
    ws,cl=premises([(u,v) for u in (a,b) for v in (c,d,e)])
    cl += [eq(a,b),eq(c,d),eq(c,e),eq(d,e)]
    rec={'kind':'k23','left':[a,b],'right':[c,d,e],'witnesses':ws};new.append((cl,rec))
  if not new:
   result={'status':'QUOTIENT_SURVIVES','iteration':iteration,'representatives':rep,'qvertices':len(qnb),'qedges':len(witness),'seconds':time.time()-start};break
  seen=set()
  for cl,rec in new:
   cl=tuple(sorted(set(cl)))
   if cl in seen:continue
   seen.add(cl)
   if any((l in model) for l in cl):raise ValueError('new clause not falsified')
   clauses.append(list(cl));s.add_clause(list(cl));learned.append(rec)
 else:result={'status':'ITERATION_LIMIT','seconds':time.time()-start}
(w/'geometric.json').write_text(json.dumps({'source_k':k,'result':{'status':result['status'],'iteration':result.get('iteration')},'original_k23':original,'learned':learned},separators=(',',':'))+'\n')
with (w/'instance.cnf').open('w') as f:
 f.write(f'p cnf {len(var)} {len(clauses)}\n')
 for cl in clauses:f.write(' '.join(map(str,cl))+' 0\n')
print(json.dumps(result),flush=True)
