#!/usr/bin/env python3
"""Author audit using independently published generic quotient-ring arithmetic."""
from pathlib import Path
from fractions import Fraction as Q
from functools import lru_cache
from collections import defaultdict,Counter
from math import gcd,lcm
from hashlib import sha256
import importlib.util,json,itertools,time,sys,argparse
sys.dont_write_bytecode=True
root=Path(__file__).resolve().parent.parent
parser=argparse.ArgumentParser(description='Independent determinant and full-incidence audit of the one-low-point stratum.')
parser.add_argument('--candidate-work',type=Path,required=True);parser.add_argument('--work',type=Path,required=True);args=parser.parse_args();w=args.work
rp=root/'hadwiger_nelson_dense506_two_point_extension_review1/independent_check.py'
assert sha256(rp.read_bytes()).hexdigest()=='9b7e9de99164784b1e7504800442bc1931ecdcaf5217cbae4382b026187e3b72'
spec=importlib.util.spec_from_file_location('R',rp);R=importlib.util.module_from_spec(spec);spec.loader.exec_module(R)
data=json.load(open(args.candidate_work/'candidates.json'));table=json.load(open(w/'centres.json'))
assert R.digest(data['points'])=='3bcfcab7e411f6adff3426ceb1cfff97718d634fe41a0e7a71982a57995c4c45'
color_raw=(root/'hadwiger_nelson_dense506_two_point_extension/host_colors.txt').read_bytes()
assert sha256(color_raw).hexdigest()=='010e6190aa14b6eadc285a6131d7b455bd5434f79ed9b4f69cdfb2848acddcb4'
colors=list(map(int,color_raw.decode().strip()))
source=root/'hadwiger_nelson_nonmono159_214_lowden2';A=R.read_source(source/'points159.tsv',159);V=R.read_source(source/'points214.tsv',214)
P=R.build_host(A,V,1)
for row in data['points']:
 a,d=R.decode_candidate(row);assert R.D%d==0;P.append(R.scale(a,R.D//d))
actual=set(P)
t0=time.perf_counter();uedges,utests=R.graph_edges([(a,R.D) for a in P]);assert len(uedges)==12074
adj=[0]*1926;hn=[[] for _ in range(1420)];cc=set()
for i,j in uedges:
 adj[i]|=1<<j;adj[j]|=1<<i
 if i<506<=j:hn[j-506].append(i)
 elif i>=506:cc.add((i-506,j-506))
allowed=[set(range(4))-{colors[v] for v in nn} for nn in hn]
assert hn==data['neighbors'];assert all(colors[i]!=colors[j] for i,j in uedges if j<506)
assert all(allowed);assert all(not(len(allowed[i])==len(allowed[j])==1 and allowed[i]==allowed[j]) for i,j in cc)
p,z,r=5281,126,3928
assert z*z%p==33 and r*r%p==(-408+72*z)%p
invD=pow(R.D,-1,p)
xy=[(sum(a[i]*v for i,v in zip((0,1,4,5),(1,z,r,z*r)))*invD%p,sum(a[i]*v for i,v in zip((2,3,6,7),(1,z,r,z*r)))*invD%p) for a in P]
md=[[((a-x)**2+3*(b-y)**2)%p for x,y in xy] for a,b in xy[:506]]
choices={tuple(pair):[506+i for i,a in enumerate(allowed) if a<=set(pair)] for pair in itertools.combinations(range(4),2)}
retained=[];eligible=0
for i in range(506):
 xi,yi=xy[i]
 for j in range(i+1,506):
  if colors[i]==colors[j]:continue
  palette=tuple(sorted(set(range(4))-{colors[i],colors[j]}));ks=choices[palette];eligible+=len(ks)
  dx,dy=xy[j][0]-xi,xy[j][1]-yi;a=md[i][j];di,dj=md[i],md[j]
  for k in ks:
   ex,ey=xy[k][0]-xi,xy[k][1]-yi;det=(dx*ey-ex*dy)%p
   if (a*di[k]*dj[k]-12*det*det)%p==0:retained.append((i,j,k-506))
print('screen complete',len(retained),file=sys.stderr,flush=True)
@lru_cache(None)
def distance(i,j):return R.norm(R.sub(P[j],P[i]))
def inverse(a):
 numerator=R.multiply(R.multiply(R.conjugate(a),R.sigma(a)),R.conjugate(R.sigma(a)))
 n=R.multiply(a,numerator);assert not any(n[2:]);den=n[0]*n[0]-33*n[1]*n[1];assert den
 top=R.multiply(numerator,(n[0],-n[1],0,0,0,0,0,0));return tuple(Q(x,den) for x in top)
def key(a):
 nums=tuple(Q(a[i],R.D) for i in (0,1,4,5,2,3,6,7));den=lcm(*(x.denominator for x in nums));ints=tuple(int(x*den) for x in nums);g=gcd(den,*ints);return (den//g,)+tuple(x//g for x in ints)
centres=defaultdict(list);positive=[];known=0
for i,j,ci in retained:
 k=506+ci;d=R.sub(P[j],P[i]);e=R.sub(P[k],P[i]);det=R.sub(R.multiply(R.conjugate(d),e),R.multiply(R.conjugate(e),d))
 a,b,c=distance(i,j),distance(i,k),distance(j,k)
 if R.add(R.multiply(R.multiply(a,b),c),R.scale(R.multiply(det,det),R.D**2))!=R.ZERO:continue
 assert det!=R.ZERO
 common=adj[i]&adj[j]&adj[k]
 if common:
  assert common.bit_count()==1;known+=1;continue
 v=R.multiply(R.sub(R.multiply(a,e),R.multiply(b,d)),inverse(det));h=R.add(P[i],v)
 assert R.norm(v)==R.scale(R.ONE,R.D**2);assert h not in actual
 hk=key(h);centres[hk].append((i,j,ci));positive.append((i,j,ci))
points=sorted(centres)
assert points==list(map(tuple,table['points']));assert positive==list(map(tuple,table['positive_triples']))
assert known==62877
print('exact centres checked',len(points),file=sys.stderr,flush=True)

def modpoint(v):
 a,d=v
 if d%p==0:return None
 iv=pow(d,-1,p)
 return (sum(a[i]*t for i,t in zip((0,1,4,5),(1,z,r,z*r)))*iv%p,sum(a[i]*t for i,t in zip((2,3,6,7),(1,z,r,z*r)))*iv%p)
def maybe(a,b):return a is None or b is None or ((a[0]-b[0])**2+3*(a[1]-b[1])**2-1)%p==0
basis=[tuple(int(i==j) for j in range(8)) for i in range(8)]
for a,b in itertools.product(basis,repeat=2):assert R.sigma(R.multiply(a,b))==R.multiply(R.sigma(a),R.sigma(b))
for a in basis:assert R.conjugate(R.sigma(a))==R.sigma(R.conjugate(a))
summary=[];witness_hash=sha256()
for epsilon in (1,-1):
 QP=[(a if epsilon==1 else R.sigma(a),R.D) for a in P]
 qx=[R.decode_candidate(row) for row in points]
 if epsilon==-1:qx=[(R.sigma(a),d) for a,d in qx]
 mods=list(map(modpoint,QP));mx=list(map(modpoint,qx));tests=0;entries=0;checked_pairs=0;full_degrees=Counter()
 for ix,(q,mq) in enumerate(zip(qx,mx)):
  neighbors=[]
  for j,(v,mv) in enumerate(zip(QP,mods)):
   if maybe(mq,mv):
    tests+=1
    if R.unit_pair(q,v):neighbors.append(j)
  hosts=[v for v in neighbors if v<506];assert hosts==table['host_pairs'][ix] and len(hosts)==2
  remaining=set(range(4))-{colors[v] for v in hosts};assert len(remaining)==2
  ns=[v-506 for v in neighbors if v>=506 and allowed[v-506]<=remaining]
  assert ns==table['eligible_candidate_neighbors'][ix]
  entries+=len(neighbors);full_degrees[len(neighbors)]+=1
  for a,b in itertools.combinations(ns,2):
   coloring=next(((x,y,z) for x in sorted(remaining) for y in sorted(allowed[a]) for z in sorted(allowed[b]) if x!=y and x!=z and ((a,b) not in cc or y!=z)),None)
   assert coloring is not None,(ix,a,b)
   if epsilon==1:witness_hash.update(json.dumps([ix,a,b,*coloring],separators=(',',':')).encode()+b'\n')
   checked_pairs+=1
 summary.append({'root':epsilon,'all_U_incidence_pairs':len(P)*len(qx),'exact_norm_tests_after_screen':tests,'full_U_incidence_edges':entries,'full_U_degree_histogram':dict(sorted(full_degrees.items())),'eligible_pairs_explicitly_coloured':checked_pairs})
result={'prime':p,'z':z,'r':r,'eligible_triples':eligible,'modular_survivors_no_early_U_removal':len(retained),'modular_survivor_sha256':R.digest(retained),'known_U_centre_triples':known,'external_centre_triples':len(positive),'external_centres':len(points),'every_point_and_positive_triple_match':True,'point_sha256':R.digest(points),'positive_triple_sha256':R.digest(positive),'roots':summary,'pair_colouring_stream_sha256':witness_hash.hexdigest(),'uncovered':0}
print(json.dumps(result,indent=2),flush=True)
