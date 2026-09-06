"""Exact repeated-contact census and positive core certificate; no native solver."""
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


def generate():
 P=sorted({pa(d,u) for d in D for u in U})
 outer=[v for v in P if v not in D]
 rho=(scalar(F(5,6)),(F(0),F(0),F(1,6),F(0)))
 W=[pa(e,rho) for e in outer]
 need(all(norm(ps(w,d)) not in (Z,ONE) for w in W for d in D),"construction invariant")
 A=[ps(w,d) for w in W for d in D]
 classcount=Counter(canon(a) for a in A)
 need(max(classcount.values())==2,"construction invariant")
 outcomes=Counter();rows=[];directions=set()
 for i,j in combinations_with_replacement(range(27),2):
  a=A[i];aa=norm(a)
  for k,r in enumerate(U):
   b=pm(A[j],r);bb=norm(b);delta=det(a,b)
   if delta==Z:
    outcomes['identical' if a==b else 'parallel_incompatible']+=1
    continue
   denominator=mul(scalar(2),delta)
   z=(div(sub(mul(aa,b[1]),mul(bb,a[1])),denominator),div(sub(mul(bb,a[0]),mul(aa,b[0])),denominator))
   if norm(z)!=ONE:
    outcomes['nonunit_circumcentre']+=1;continue
   outcomes['unit_circumcentre']+=1
   directions.add(canon(z));rows.append((i,j,k,z))
 orbits=sorted(directions)
 orbrows=[];heavy=[]
 for u in orbits:
  q=[pa(d,z) for d in D for z in orbit(u)]
  if u in U:
   orbrows.append({'direction':serial(u),'exceptional':True});continue
  need(len(set(q))==18 and not set(q)&set(P+W),"construction invariant")
  contacts=[(i,j) for i,w in enumerate(W) for j,x in enumerate(q) if norm(ps(w,x))==ONE]
  orbrows.append({'direction':serial(u),'exceptional':False,'contacts':contacts})
  if len(contacts)>=3:heavy.append(u)
 V=P+W+[pa(d,z) for u in heavy for d in D for z in orbit(u)]
 need(len(V)==len(set(V)),"construction invariant")
 E=[(i,j) for i,j in combinations(range(len(V)),2) if norm(ps(V[i],V[j]))==ONE]
 adj=[set() for _ in V]
 for i,j in E:adj[i].add(j);adj[j].add(i)
 col={V.index(d):i for i,d in enumerate(D)};nodes=[0]
 def dfs():
  nodes[0]+=1
  if len(col)==len(V):return [col[i] for i in range(len(V))]
  v=max((v for v in range(len(V)) if v not in col),key=lambda v:(len({col[x] for x in adj[v] if x in col}),len(adj[v]),-v))
  used={col[x] for x in adj[v] if x in col}
  for c in range(4):
   if c in used:continue
   col[v]=c;answer=dfs()
   if answer is not None:return answer
   del col[v]
  return None
 colour=dfs()
 need(colour is not None and all(colour[i]!=colour[j] for i,j in E),"positive core colouring")
 data={'rho':serial(rho),'patch':[serial(x) for x in P],'exterior':[serial(x) for x in W],
  'constraint_classes':sorted(classcount.values()),'outcomes':dict(outcomes),'orbits':orbrows,
  'unit_rows':[[i,j,k,orbits.index(canon(z)),orbit(canon(z)).index(z)] for i,j,k,z in rows],
  'heavy_orbit_indices':[orbits.index(u) for u in heavy],
  'vertices':[serial(x) for x in V],'edges':E,'centres':[V.index(d) for d in D],'colouring':colour,
  'dfs_nodes':nodes[0]}
 Pcol=[]
 for x,y in P:
  b=2*y[1];a=x[0]-b/2
  Pcol.append(int(a+2*b)%3)
 three=[]
 for phases in product((1,-1),repeat=len(heavy)):
  c=Pcol+[None]*9+[(i+ph*(-1)**j)%3 for ph in phases for i in range(3) for j in range(6)]
  masks=[]
  for w in range(12,21):
   seen={c[t] for t in adj[w] if c[t] is not None}
   masks.append([t for t in range(3) if t not in seen])
  empty=[i for i,m in enumerate(masks) if not m]
  need(empty,"three-colour obstruction")
  three.append({'phases':phases,'lists':masks,'empty_exterior_index':empty[0]})
 data['three_colour_obstructions']=three
 return data

def main():
 parser=argparse.ArgumentParser();parser.add_argument('--out',required=True);parser.add_argument('--discover',action='store_true');a=parser.parse_args()
 out=Path(a.out);out.mkdir(parents=True,exist_ok=False);start=time.monotonic()
 data=generate();raw=(json.dumps(data,sort_keys=True,separators=(',',':'))+'\n').encode()
 if not a.discover:need(raw==(Path(__file__).parent/'certificate.json').read_bytes(),'published certificate mismatch')
 (out/'certificate.json').write_bytes(raw)
 report={'status':'PASS','certificate_bytes':len(raw),'certificate_sha256':hashlib.sha256(raw).hexdigest(),'seconds':time.monotonic()-start,'native_solver_calls':0}
 (out/'build.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,sort_keys=True))
if __name__=='__main__':main()
