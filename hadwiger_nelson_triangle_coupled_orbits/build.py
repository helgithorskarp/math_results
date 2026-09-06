"""Exact two-orbit exterior-family census and common positive certificate."""
from fractions import Fraction as F
from itertools import combinations,combinations_with_replacement,product
from collections import Counter
from pathlib import Path
import argparse,hashlib,json,time

def need(ok,message):
 if not ok:raise ValueError(message)

Z=(F(0),)*4
ONE=(F(1),F(0),F(0),F(0))
def scalar(x):return (F(x),F(0),F(0),F(0))
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def neg(a):return tuple(-x for x in a)
def sub(a,b):return add(a,neg(b))
def mul(a,b):
 r=[F(0)]*4
 for i,x in enumerate(a):
  for j,y in enumerate(b):
   common=i&j
   r[i^j]+=x*y*(3 if common&1 else 1)*(11 if common&2 else 1)
 return tuple(r)
def inv(a):
 c=tuple(x*(-1 if i&2 else 1) for i,x in enumerate(a))
 n=mul(a,c);need(n[2:]==Z[2:],"norm subfield")
 cc=tuple(x*(-1 if i&1 else 1) for i,x in enumerate(n))
 q=mul(n,cc);need(q[1:]==Z[1:] and q[0],"nonzero norm")
 return tuple(x/q[0] for x in mul(c,cc))
def div(a,b):return mul(a,inv(b))
def pa(a,b):return (add(a[0],b[0]),add(a[1],b[1]))
def ps(a,b):return (sub(a[0],b[0]),sub(a[1],b[1]))
def pm(a,b):return (sub(mul(a[0],b[0]),mul(a[1],b[1])),add(mul(a[0],b[1]),mul(a[1],b[0])))
def norm(a):return add(mul(a[0],a[0]),mul(a[1],a[1]))
def det(a,b):return sub(mul(a[0],b[1]),mul(a[1],b[0]))
O=(Z,Z);R=(scalar(F(1,2)),(F(0),F(1,2),F(0),F(0)))
D=[O,(ONE,Z),R]
U=[(ONE,Z)]
for _ in range(5):U.append(pm(U[-1],R))
def orbit(z):return [pm(z,r) for r in U]
def canon(z):return min(orbit(z))
def serial(z):return [[[x.numerator,x.denominator] for x in v] for v in z]


def encode(z):
 values=[12*x for axis in z for x in axis]
 need(all(x.denominator==1 for x in values),'coordinate denominator')
 return [int(x) for x in values]


def generate():
 P=sorted({pa(d,u) for d in D for u in U});B=[p for p in P if p not in D]
 rho=(scalar(F(5,6)),(F(0),F(0),F(1,6),F(0)))
 sigma=((F(-1,4),F(0),F(0),F(-1,12)),(F(0),F(-1,12),F(1,4),F(0)))
 cases=[];normalset=set()
 for a,b in product(range(6),repeat=2):
  W=[pa(p,orbit(z)[k]) for z,k in [(rho,a),(sigma,b)] for p in B]
  need(len(set(W))==18 and all(norm(ps(w,d)) not in (Z,ONE) for w in W for d in D),'outside')
  cs=Counter(canon(ps(w,d)) for w in W for d in D)
  need(max(cs.values())<=2,'normal multiplicity')
  normalset.update(cs);cases.append((a,b,W,cs))
 N=sorted(normalset);
 outcomes=Counter();directions=set();rows=[]
 for i,j in combinations_with_replacement(range(len(N)),2):
  a=N[i];aa=norm(a)
  for k,r in enumerate(U):
   b=pm(N[j],r);bb=norm(b);de=det(a,b)
   if de==Z:outcomes['identical' if a==b else 'parallel_incompatible']+=1;continue
   den=mul(scalar(2),de)
   z=(div(sub(mul(aa,b[1]),mul(bb,a[1])),den),div(sub(mul(bb,a[0]),mul(aa,b[0])),den))
   if norm(z)!=ONE:outcomes['nonunit']+=1;continue
   outcomes['unit']+=1;directions.add(canon(z));rows.append((i,j,k,z))
 directions=sorted(directions);Q={u:[pa(d,z) for d in D for z in orbit(u)] for u in directions if u not in U}

 ALL=sorted(set(P+sum((x[2] for x in cases),[])+sum(Q.values(),[])))

 idx={v:i for i,v in enumerate(ALL)}
 E=[(i,j) for i,j in combinations(range(len(ALL)),2) if norm(ps(ALL[i],ALL[j]))==ONE]
 adj=[set() for _ in ALL]
 for i,j in E:adj[i].add(j);adj[j].add(i)

 I=list(range(len(ALL)));col={idx[d]:i for i,d in enumerate(D)};nodes=[0]
 def dfs():
  nodes[0]+=1
  if len(col)==len(I):return [col[i] for i in I]
  v=max((i for i in I if i not in col),key=lambda i:(len({col[n] for n in adj[i] if n in col}),len(adj[i]),-i))
  used={col[n] for n in adj[v] if n in col}
  for c in range(4):
   if c in used:continue
   col[v]=c;r=dfs()
   if r is not None:return r
   del col[v]
  return None
 c=dfs();need(c is not None,'common positive colouring')
 case_rows=[]
 for a,b,W,cs in cases:
  contacts={u:sum(idx[q] in adj[idx[w]] for w in W for q in qq) for u,qq in Q.items()}
  heavy=[u for u in Q if contacts[u]>=3]
  V=P+W+sum((Q[u] for u in heavy),[]);ids={idx[v] for v in V}
  need(len(V)==len(ids),'distinct core')
  case_rows.append({'orientation':[a,b],'normal_class_sizes':sorted(cs.values()),
   'heavy':[directions.index(u) for u in heavy],'incidences':[contacts[u] for u in heavy],
   'vertices':len(V),'edges':sum(j in ids for i in ids for j in adj[i])//2,
   'cross_edges':sum(idx[w] in adj[idx[v]] for w in W[:9] for v in W[9:])})
 return {'denominator':12,'shifts':[encode(rho),encode(sigma)],
  'normal_representatives':[encode(n) for n in N],
  'directions':[encode(u) for u in directions], 'outcomes':dict(outcomes),
  'unit_rows':[[i,j,k,directions.index(canon(z)),orbit(canon(z)).index(z)] for i,j,k,z in rows],
  'vertices':[encode(v) for v in ALL],'edges':E,'colouring':c,
  'dfs_nodes':nodes[0],'cases':case_rows}

def main():
 parser=argparse.ArgumentParser();parser.add_argument('--out',required=True);parser.add_argument('--discover',action='store_true');a=parser.parse_args()
 out=Path(a.out);out.mkdir(parents=True,exist_ok=False);start=time.monotonic()
 data=generate();raw=(json.dumps(data,sort_keys=True,separators=(',',':'))+'\n').encode()
 if not a.discover:need(raw==(Path(__file__).parent/'certificate.json').read_bytes(),'published certificate mismatch')
 (out/'certificate.json').write_bytes(raw)
 report={'status':'PASS','certificate_bytes':len(raw),'certificate_sha256':hashlib.sha256(raw).hexdigest(),'seconds':time.monotonic()-start,'native_solver_calls':0}
 (out/'build.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,sort_keys=True))
if __name__=='__main__':main()
