"""Exact quartic construction of a regular phase-obstruction realization."""
from fractions import Fraction as F
from itertools import combinations,product
from collections import deque
import json,hashlib,argparse,time
from pathlib import Path
N=4
Z=(F(0),)*4
O=(F(1),F(0),F(0),F(0))
def scalar(v):return (F(v),F(0),F(0),F(0))
def plus(a,b):return tuple(x+y for x,y in zip(a,b))
def neg(a):return tuple(-x for x in a)
def mul(a,b):
 c=[F(0)]*4
 for i,x in enumerate(a):
  for j,y in enumerate(b):c[(i+j)%4]+=x*y*(12 if i+j>=4 else 1)
 return tuple(c)
def sub(a,b):return plus(a,neg(b))
def scale(a,b):return tuple(b*x for x in a)
def ca(a,b):return plus(a[0],b[0]),plus(a[1],b[1])
def cn(a):return neg(a[0]),neg(a[1])
def cs(a,b):return ca(a,cn(b))
def cm(a,b):return sub(mul(a[0],b[0]),mul(a[1],b[1])),plus(mul(a[0],b[1]),mul(a[1],b[0]))
def cscale(a,b):return scale(a[0],b),scale(a[1],b)
def norm(a,b):
 x,y=cs(a,b);return plus(mul(x,x),mul(y,y))
def orbit(a):
 vs=[cm(a,u) for u in U];rep=min(vs);return rep,next(k for k,u in enumerate(U) if cm(rep,u)==a)
zero=(Z,Z);one=(O,Z);sqrt3=(F(0),F(0),F(1,2),F(0));eta=(F(0),F(1),F(0),F(0))
omega=(scalar(F(1,2)),scale(sqrt3,F(1,2)));U=[one]
for k in range(5):U.append(cm(U[-1],omega))
zeta=U[2];a1=U[4];u=(scale(sqrt3,F(1,2)),scalar(F(-1,2)))
y=cm(u,(scale(sub(O,sqrt3),F(1,2)),scale(eta,F(1,2))))
z=cm(u,(scale(sub(O,sqrt3),F(1,2)),scale(eta,F(-1,2))))
def encode(point):return [[[v.numerator,v.denominator] for v in axis] for axis in point]
def raw(data):return (json.dumps(data,sort_keys=True,separators=(',',':'))+'\n').encode()
def digest(data):return hashlib.sha256(raw(data)).hexdigest()
def check(ok,msg):
 if not ok:raise ValueError(msg)

def colour_graph(V,E,pins):
 adj=[set() for _ in V]
 for a,b in E:adj[a].add(b);adj[b].add(a)
 col=[-1]*len(V);masks=[15]*len(V);nodes=0
 for i,c in pins.items():masks[i]=1<<c
 def rec():
  nonlocal nodes
  nodes+=1
  domains={i:[c for c in range(4) if masks[i]>>c&1 and all(col[j]!=c for j in adj[i])] for i in range(len(V)) if col[i]<0}
  if not domains:return col.copy()
  v=min(domains,key=lambda i:(len(domains[i]),-sum(col[j]>=0 for j in adj[i]),-len(adj[i]),i))
  for c in domains[v]:
   col[v]=c;result=rec()
   if result is not None:return result
  col[v]=-1
  return None
 result=rec();check(result is not None,'no positive graph colouring found')
 return result,nodes

def build():
 D=[zero,a1,cs(cn(one),y),ca(cn(zeta),z)];tips=[cn(one),cn(zeta)]
 check(all(norm(t,zero)==O for t in [u,y,z]),'unit directions')
 check(norm(D[0],D[1])==O and norm(D[2],D[3])==O,'unit segments')
 check(len(set(D))==4,'four distinct centres')
 check(len({orbit(t)[0] for t in [one,y,z]})==3,'three distinct cross orbits')
 cross=[(0,2),(0,3),(1,2),(1,3)]
 I=[sorted([tips[b-2],cs(ca(D[a],D[b]),tips[b-2])]) for a,b in cross]
 check(all(norm(x,D[a])==norm(x,D[b])==O for (a,b),row in zip(cross,I) for x in row),'circle roots')
 reps=[one,y,z]
 def phase_info(v):
  candidates=[(j,k) for j,r in enumerate(reps) for k,rotation in enumerate(U) if cm(r,rotation)==v]
  check(len(candidates)==1,'unique direction label');return candidates[0]
 clauses=[];independent=[]
 for (a,b),row in zip(cross,I):
  pair=[]
  for x in row:
   v,k=phase_info(cs(x,D[a]));w,l=phase_info(cs(x,D[b]));s=(1+a+b-2)%2
   c=sorted([[v,(s+k)%2],[w,(1+s+l)%2]])
   pair.append(c)
   independent.append(sorted([[v,(s+k)%2],[3+w,(s+l)%2]]))
  check(pair[0]==pair[1],'paired root clause');clauses.append(pair[0])
 check(not any(all(any(a[v]==b for v,b in c) for c in clauses) for a in product(range(2),repeat=3)),'coupled obstruction')
 check(not any(all(any(a[v]==b for v,b in c) for c in independent) for a in product(range(2),repeat=6)),'independent phases obstruction')
 S=[set(),set()]
 for g in range(2):
  seeds=[cs(D[2*g+1],D[2*g])]
  for (a,b),row in zip(cross,I):
   seeds.extend(cs(x,D[a if g==0 else b]) for x in row)
  for t in seeds:S[g].update(cm(t,v) for v in U)
 V=sorted({ca(d,s) for h,d in enumerate(D) for s in S[h//2]});idx={v:i for i,v in enumerate(V)}
 E=[(i,j) for i,j in combinations(range(len(V)),2) if norm(V[i],V[j])==O]
 owners=[{h for h,d in enumerate(D) if norm(v,d)==O} for v in V];ci=[idx[d] for d in D]
 listed=[1<<(2,3,0,1)[ci.index(i)] if i in ci else 3 if own<={0,1} else 12 if own<={2,3} else 15 for i,own in enumerate(owners)]
 colour,nodes=colour_graph(V,E,dict(zip(ci,(2,3,0,1))))
 check(all(colour[a]!=colour[b] for a,b in E),'proper graph colouring')
 path=list(map(idx.__getitem__,[cn(one),zeta,cn(a1),one,cn(zeta)]))
 check(all(tuple(sorted((a,b))) in E for a,b in zip(path,path[1:])),'four-edge path')
 check(all(owners[i]=={0} for i in path[1:-1]),'A-only path interior')
 check(owners[path[0]]=={0,1,2} and owners[path[-1]]=={0,1,3},'forced endpoint colours')
 return {'schema':1,'field_polynomial':'T^4-12','embedding':'eta positive','parameters':{'u':encode(u),'y':encode(y),'z':encode(z)},'centres':list(map(encode,D)),'intersections':[[encode(t) for t in row] for row in I],'cross_squared_distances':[[[v.numerator,v.denominator] for v in norm(D[a],D[b])] for a,b in cross],'coupled_clauses':clauses,'independent_phase_clauses':independent,'direction_sizes':list(map(len,S)),'mixed_points':len({t for row in I for t in row}),'vertices':len(V),'edges':len(E),'point_sha256':digest(list(map(encode,V))),'edge_sha256':digest(E),'centre_indices':ci,'kernel_lists':''.join(format(m,'x') for m in listed),'list_obstruction_path':path,'path_forced_colours':[1,0],'colouring':''.join(map(str,colour)),'positive_search_nodes':nodes,'full_support_colouring_claimed':False,'target_found':False}

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--out',required=True);ap.add_argument('--discover',action='store_true');args=ap.parse_args()
 out=Path(args.out);out.mkdir(parents=True,exist_ok=False);start=time.monotonic();data=build();blob=raw(data)
 if not args.discover:check(blob==(Path(__file__).parent/'certificate.json').read_bytes(),'certificate mismatch')
 (out/'certificate.json').write_bytes(blob)
 report={'status':'PASS','vertices':data['vertices'],'edges':data['edges'],'mixed_points':data['mixed_points'],'positive_search_nodes':data['positive_search_nodes'],'certificate_bytes':len(blob),'certificate_sha256':hashlib.sha256(blob).hexdigest(),'seconds':time.monotonic()-start}
 (out/'build.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
if __name__=='__main__':main()
