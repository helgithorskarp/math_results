"""Independent physical formula and exact family auditor; no producer imports."""
from pathlib import Path
from itertools import combinations
from math import comb
import argparse,hashlib,json
HERE=Path(__file__).resolve().parent

def physical(name,cache):
 prefix,Q,R,C=name.split('-');q=int(Q[1:]);r=int(R[1:]);idx=int(C[1:]);n=43-4*q
 if prefix!='mp1' or not 7<=q<=10 or not 5<=r<=q:raise ValueError('task')
 s=next(x for x in json.loads((HERE/'INPUTS.json').read_text()) if x['n']==n)
 raw=(Path(cache)/s['name']).read_bytes()
 if hashlib.sha256(raw).hexdigest()!=s['sha256'] or not 0<=idx<s['count']:raise ValueError('input/index')
 record=raw.splitlines()[idx];word=0
 for byte in record[1:]:word=64*word+byte-63
 padding=6*(len(record)-1)-comb(n,2);word>>=padding
 fixed={};k=comb(n,2)-1
 for v in range(n):
  for u in range(v):fixed[4*q+u,4*q+v]=(word>>k)&1;k-=1
 for u,v in combinations(range(4*q),2):
  if u//4==v//4:fixed[u,v]=int(u//4<r)
 variables={};k=2
 for e in combinations(range(43),2):
  if e not in fixed:variables[e]=k;k+=1
 return q,r,n,fixed,variables

def clauses(q,r,fixed,variables):
 yield (1,)
 for block in range(1,q):
  for c in range(3):
   for left,right in combinations(range(16),2):
    ans=[]
    for v,word in [(4*block+c,left),(4*block+c+1,right)]:
     for u in range(4):ans.append(variables[u,v]*(1-2*((word>>u)&1)))
    yield tuple(ans)
 for k,vertices,colors in [(5,range(43),(1,0)),(4,range(4*r,43),(1,))]:
  for vs in combinations(vertices,k):
   fixed_colors=set();unknown=[]
   for edge in combinations(vs,2):
    if edge in fixed:fixed_colors.add(fixed[edge])
    else:unknown.append(variables[edge])
   for color in colors:
    if not fixed_colors-set([color]):yield tuple((-x if color else x) for x in unknown)

def formula(name,cache,path):
 q,r,n,fixed,variables=physical(name,cache);h=hashlib.sha256();count=0;hist={};size=0
 with Path(path).open('rb') as f:
  line=f.readline();h.update(line);size+=len(line);header=line.decode().split()
  if len(header)!=4 or header[:2]!=['p','cnf'] or int(header[2])!=len(variables)+1:raise ValueError('header')
  for wanted in clauses(q,r,fixed,variables):
   line=f.readline();h.update(line);size+=len(line);count+=1
   tokens=tuple(map(int,line.split()))
   if tokens!=wanted+(0,):raise ValueError(('physical clause disagreement',name,count))
   hist[len(wanted)]=hist.get(len(wanted),0)+1
  if f.read(1) or count!=int(header[3]):raise ValueError('length')
 return dict(task=name,variables=len(variables)+1,clauses=count,sha256=h.hexdigest(),bytes=size,clause_lengths=hist)

def registry():
 actual=json.loads((HERE/'TASKS.json').read_text());specs=json.loads((HERE/'INPUTS.json').read_text());summaries=json.loads((HERE/'CATALOG_CENSUS.json').read_text());old=json.loads((HERE/'COMPARISON.json').read_text())
 offset=0;tasks=0;results=[]
 for row in actual['classes']:
  q=row['q'];r=row['r'];n=43-4*q;s=next(x for x in specs if x['n']==n);value=1
  for i,j in combinations(range(q),2):value*=((1998 if j<r else 1931) if i==0 else (37823 if (i<r)==(j<r) else 35714))
  for _ in range(q):
   for _ in range(n):value*=15
  cores=next(x for x in summaries if x['n']==n)
  if sum(x[3] for x in cores['histogram'])!=s['count']:raise ValueError('census')
  wanted=dict(q=q,r=r,n=n,core_start=0,core_stop=s['count'],first_task=f'mp1-q{q}-r{r}-c000000',last_task=f"mp1-q{q}-r{r}-c{s['count']-1:06d}",per_task=value,code_start=offset,code_stop=offset+value*s['count'],physical_variables=903-6*q-comb(n,2),input_sha256=s['sha256'])
  if wanted!=row:raise ValueError('task registry')
  offset+=value*s['count'];tasks+=s['count'];results.append((q,r))
 if results!=[(q,r) for q in range(7,11) for r in range(5,q+1)] or actual['carrier_count']!=offset or actual['tasks']!=tasks or actual['macro_classes']!=18:raise ValueError('cover')
 H=old['H']
 if offset!=old['N'] or not 4096*offset<H or not 18767*offset<H<18768*offset or not offset<2**770:raise ValueError('global reduction gate')
 return dict(status='COMPLETE_REGISTRY_AND_EXACT_GATE_VERIFIED',macro_classes=18,tasks=tasks,N=offset,lower_ratio=18767,upper_ratio=18768,gate_4096=True)

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--cache');p.add_argument('--task');p.add_argument('--cnf');a=p.parse_args()
 print(json.dumps(formula(a.task,a.cache,a.cnf) if a.cnf else registry(),sort_keys=True))
