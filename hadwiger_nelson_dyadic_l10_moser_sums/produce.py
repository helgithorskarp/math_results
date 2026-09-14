"""Optional exact-geometry discovery of positive interface certificates."""
from pathlib import Path
from itertools import product
import argparse,base64,json,hashlib,time
import census
import geometry as g

def source_patterns(ps):
 den,points=g.integral(ps);es=g.exact_edges(den,points)
 back=[set()for _ in ps]
 for a,b in es:back[b].add(a)
 out=[]
 def rec(w):
  i=len(w)
  if i==len(ps):out.append(tuple(w));return
  for c in range(min(3,max(w,default=-1)+1)+1):
   if all(w[j]!=c for j in back[i]):rec(w+[c])
 rec([]);return out

def formula(es):
 return [[4*i+c+1 for c in range(4)]for i in range(448)]+[[-4*a-c-1,-4*b-c-1]for a,b in es for c in range(4)]
def solve(s,pins):
 s.conf_budget(200000)
 result=s.solve_limited(assumptions=pins)
 if result is not True:return None
 model=set(s.get_model())
 word=[next(c for c in range(4)if 4*i+c+1 in model)for i in range(448)]
 # ALO permits several true colours. At a pinned vertex select the pin,
 # rather than the first true colour. All adjacent true sets are disjoint.
 selected={}
 for lit in pins:
  if lit not in model:raise ValueError('model violates a positive pin')
  vertex=(lit-1)//4;colour=(lit-1)%4
  if vertex in selected and selected[vertex]!=colour:raise ValueError('conflicting pins')
  selected[vertex]=colour;word[vertex]=colour
 return ''.join(map(str,word))
def digest(x):return hashlib.sha256(json.dumps(x,separators=(',',':')).encode()).hexdigest()

def produce(output):
 from pysat.solvers import Cadical153
 phases,_=census.phases();graphs=[]
 for phase in phases:
  den,points,ids=census.construct(phase);graphs.append(g.exact_edges(den,points))
 union=sorted(set().union(*map(set,graphs)))
 universal=Cadical153(bootstrap_with=formula(union))
 solvers=[Cadical153(bootstrap_with=formula(es))for es in graphs]
 L,M,P=census.sources();pool={};queries=0
 for name,ps in [('L',L),('first_M',M),('last_M',M)]:
  for pat in source_patterns(ps):
   pins=[4*i+c+1 for i,c in zip(ids[name],pat)]
   queries+=1;w=solve(universal,pins)
   if w is not None:
    if not all(w[a]!=w[b]for a,b in union):raise ValueError('invalid universal model')
    pool[w]=(1<<28)-1;continue
   # An unsuccessful supergraph query is only a compression failure.
   # Neither UNSAT nor UNKNOWN from it is a mathematical premise.
   pending=set(range(28))
   while pending:
    phase=min(pending);queries+=1;w=solve(solvers[phase],pins)
    if w is None:raise RuntimeError('incomplete positive certificate')
    covered=[j for j in pending if all(w[a]!=w[b]for a,b in graphs[j])]
    if phase not in covered:raise ValueError('invalid individual model')
    mask=sum(1<<j for j in covered);pool[w]=pool.get(w,0)|mask;pending.difference_update(covered)
  print(name,'completed; pool',len(pool),flush=True)
 for solver in [universal]+solvers:solver.delete()
 rows=[]
 for w,mask in sorted(pool.items()):
  packed=bytes(sum(int(w[i+j])<<(2*j)for j in range(4))for i in range(0,448,4))
  rows.append([mask,base64.b64encode(packed).decode()])
 phase_rows=[[[str(z)for z in x],[str(z)for z in y]]for x,y in phases]
 cert={'format':'two-bit-little-endian-v1','phase_sha256':digest(phase_rows),'words':rows}
 output.write_text(json.dumps(cert,separators=(',',':'))+'\n')
 print(json.dumps({'complete':True,'queries':queries,'words':len(rows),'bytes':output.stat().st_size}))

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);a=p.parse_args()
 if a.output.exists():raise FileExistsError('choose a fresh output path')
 st=time.monotonic();produce(a.output);print('seconds',time.monotonic()-st)
