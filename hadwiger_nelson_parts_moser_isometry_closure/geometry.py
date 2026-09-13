"""Complete exact enumeration of Parts/Moser isometries; no floating point."""
from fractions import Fraction as F
from itertools import combinations, permutations, product
from collections import defaultdict, Counter
from pathlib import Path
import json,math,time,hashlib
HERE=Path(__file__).resolve().parent
REPO=HERE.parent
def require(condition,message):
 if not condition:raise ValueError(message)

R=(1,3,5,15,11,33,55,165)
Z=(0,)*8; O=(1,)+(0,)*7

def add(a,b):return tuple(x+y for x,y in zip(a,b))
def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def scale(a,c):return tuple(x*c for x in a)
def mul(a,b):
 o=[0]*8
 for i,x in enumerate(a):
  if x:
   for j,y in enumerate(b):
    if y:o[i^j]+=x*y*R[i&j]
 return tuple(o)
def inv(a):
 b=O
 for s in range(1,8):b=mul(b,tuple((-1 if (s&i).bit_count()%2 else 1)*x for i,x in enumerate(a)))
 n=mul(a,b)
 require(n[0] and not any(n[1:]), 'exact geometry invariant')
 return scale(b,F(1,n[0]))
def cmul(a,b):return sub(mul(a[:8],b[:8]),mul(a[8:],b[8:]))+add(mul(a[:8],b[8:]),mul(a[8:],b[:8]))
def norm(a):return add(mul(a[:8],a[:8]),mul(a[8:],a[8:]))
def cdiv(a,b):return tuple(v for h in (mul(cmul(a,b[:8]+scale(b[8:],-1))[:8],inv(norm(b))),mul(cmul(a,b[:8]+scale(b[8:],-1))[8:],inv(norm(b))))for v in h)

def spindle():
 w=(F(1,2),)+(0,)*7+(0,F(1,2))+(0,)*6
 one=O+Z;z=Z+Z;rho=(F(5,6),)+(0,)*7+(0,0,0,0,F(1,6),0,0,0)
 far=add(one,w)
 return [z,one,w,far,rho,cmul(rho,w),cmul(rho,far)]
def build(progress=False):
 M=spindle();mn=[norm(sub(a,b))for a,b in combinations(M,2)]
 require(sum(x==O for x in mn)==11, 'exact geometry invariant')
 bydist=defaultdict(set)
 for i,j in permutations(range(7),2):
  d=norm(sub(M[j],M[i]))
  for s in (1,-1):
   shape=[]
   for m in M:
    v=cdiv(sub(m,M[i]),sub(M[j],M[i]));shape.append(v[:8]+scale(v[8:],s))
   bydist[d].add(tuple(sorted(shape)))
 L=math.lcm(*(F(c).denominator for ss in bydist.values()for sh in ss for p in sh for c in p));D=96*L
 if progress: print('exact normalization denominator',L,flush=True)
 templates={tuple(int(c*96**2)for c in k):[tuple(tuple(int(c*L)for c in p)for p in sh)for sh in sorted(ss)]for k,ss in bydist.items()}
 # M distances have denominator 6 etc, all scale integrally at96 squared.
 require(all(all(F(c*96**2).denominator==1 for c in k)for k in bydist), 'exact geometry invariant')
 raw=(REPO/'hadwiger_nelson_parts509_completion_census_degree9/points.tsv').read_bytes()
 P=[tuple(map(int,l.split()))for l in raw.decode().splitlines()if not l.startswith('#')];PS={scale(p,L):i for i,p in enumerate(P)}
 edges=[];pairs=defaultdict(list)
 for i,j in combinations(range(509),2):
  d=norm(sub(P[j],P[i]))
  if d==scale(O,96**2):edges.append((i,j))
  if d in templates:pairs[d].append((i,j))
 require(len(edges)==2442, 'exact geometry invariant')
 if progress: print('matching-pair census complete',flush=True)
 allshapes={};routes=0
 for d,ts in templates.items():
  for i,j in pairs[d]:
   a=scale(P[i],L);delta=sub(P[j],P[i])
   for ti,shape in enumerate(ts):
    out=tuple(sorted(add(a,cmul(delta,p))for p in shape));routes+=1
    require(len(set(out))==7, 'exact geometry invariant')
    if out not in allshapes:allshapes[out]=[i,j,list(templates).index(d),ti]
  if progress: print('distinct placements so far',len(allshapes),flush=True)
 if progress: print('overlaps',Counter(sum(p in PS for p in sh)for sh in allshapes),flush=True)
 # Reconstruct every external point, including partial spindle supports later.
 Q=sorted({p for sh in allshapes for p in sh if p not in PS});qi={p:i for i,p in enumerate(Q)}
 prime=1000081;roots=(964569,816716,970601)
 vals=[math.prod(roots[b]for b in range(3)if i>>b&1)%prime for i in range(8)]
 require(all(pow(roots[i],2,prime)==(3,5,11)[i]for i in range(3)), 'exact geometry invariant')
 def ev(p):return sum(x*v for x,v in zip(p,vals))%prime
 pmod=[(ev(p[:8])*pow(96,-1,prime)%prime,ev(p[8:])*pow(96,-1,prime)%prime)for p in P]
 unit=scale(O,D*D);neigh=[];survivors=0
 for k,q in enumerate(Q):
  x,y=ev(q[:8])*pow(D,-1,prime)%prime,ev(q[8:])*pow(D,-1,prime)%prime
  nn=[]
  for i,(a,b)in enumerate(pmod):
   if ((x-a)**2+(y-b)**2-1)%prime==0:
    survivors+=1
    if norm(sub(q,scale(P[i],L)))==unit:nn.append(i)
  neigh.append(nn)
  if progress and k%10000==0:print('neighbours',k,'of',len(Q),flush=True)
 outcomes=Counter();viable=[];new_edges=Counter()
 for sh,route in allshapes.items():
  fresh=[p for p in sh if p not in PS]
  if not fresh:continue
  qs=[qi[p]for p in fresh]
  fe=[(a,b)for a,b in combinations(range(len(fresh)),2)if norm(sub(fresh[a],fresh[b]))==unit]
  deg=[len(neigh[i])for i in qs]
  for a,b in fe:deg[a]+=1;deg[b]+=1
  outcomes[tuple(sorted(deg))]+=1
  viable.append({'route':route,'fresh':qs,'edges':fe,'degrees':deg,'overlap':[PS[p]for p in sh if p in PS]})
 summary={'scale':D,'template_counts':[len(v)for v in templates.values()],'matching_pair_counts':[len(pairs[d])for d in templates],'routes':routes,'placements':len(allshapes),'overlap_histogram':dict(Counter(sum(p in PS for p in sh)for sh in allshapes)),'fresh_points':len(Q),'modular_unit_survivors':survivors,'noncontained_placements':len(viable),'five_fresh_minimum_degree_at_least_four':sum(len(a['fresh'])==5 and min(a['degrees'])>=4 for a in viable)}
 return {'summary':summary,'scale':D,'points':Q,'neighbours':neigh,'assemblies':viable,'base_edges':edges,'base_points':P}

if __name__=='__main__':
 print(json.dumps(build(True)['summary'],indent=2))
