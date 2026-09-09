#!/usr/bin/env python3
"""Independent exact tower arithmetic and fresh-modulus physical graph audit."""
from fractions import Fraction as Q
from itertools import combinations
from pathlib import Path
import argparse,hashlib,json
HERE=Path(__file__).resolve().parent
N=16;ZERO=(Q(0),)*N;ONE=(Q(1),)+(Q(0),)*15
FACTORS=[(-3 if m&1 else 1)*(-11 if m&2 else 1)*(5 if m&4 else 1) for m in range(8)]
MOD=1000000321
ROOTS=(11447578,70971245,387152957,315670077)

def need(ok,msg):
 if not ok:raise ValueError(msg)
def basis(i):return tuple(Q(k==i) for k in range(N))
def add(x,y):return tuple(a+b for a,b in zip(x,y))
def sub(x,y):return tuple(a-b for a,b in zip(x,y))
def scale(x,s):return tuple(s*a for a in x)
def p8(x,y):
 z=[Q(0)]*8
 for i,a in enumerate(x):
  if a:
   for j,b in enumerate(y):
    if b:z[i^j]+=a*b*FACTORS[i&j]
 return tuple(z)
def mul(x,y):
 lo=list(p8(x[:8],y[:8]));hi=add(p8(x[:8],y[8:]),p8(x[8:],y[:8]))
 for i,a in enumerate(p8(x[8:],y[8:])):
  lo[i]-=3320*a;lo[i^3]+=632*a*FACTORS[i&3]
 return tuple(lo)+hi
def bar(x):return tuple((-v if (i&11).bit_count()%2 else v) for i,v in enumerate(x))
def norm(x):return mul(x,bar(x))
def inv(x):
 cols=[mul(x,basis(i)) for i in range(N)]
 rows=[[cols[j][i] for j in range(N)]+[Q(i==0)] for i in range(N)]
 for col in range(N):
  pivot=next((r for r in range(col,N) if rows[r][col]),None)
  need(pivot is not None,'zero divisor in field inverse')
  rows[col],rows[pivot]=rows[pivot],rows[col]
  lead=rows[col][col];rows[col]=[v/lead for v in rows[col]]
  for r in range(N):
   if r!=col and rows[r][col]:
    lead=rows[r][col];rows[r]=[a-lead*b for a,b in zip(rows[r],rows[col])]
 ans=tuple(r[-1] for r in rows);need(mul(x,ans)==ONE,'inverse identity');return ans

def seed(rows):
 need(len(rows)==27 and all(len(r)==4 and all(type(x) is int for x in r) for r in rows),'seed shape')
 A,B,C,E=[basis(i) for i in (1,2,4,8)]
 w=scale(add(ONE,A),Q(1,2));v=scale(add(scale(ONE,5),B),Q(1,6));wv=mul(w,v)
 def lin(*terms):
  z=ZERO
  for s,x in terms:z=add(z,scale(x,Q(s)))
  return z
 p=add(lin((3,ONE),(Q(17,8),w),(Q(-7,8),v),(2,wv)),mul(C,lin((Q(-1,4),ONE),(Q(1,8),w),(Q(-1,8),v),(Q(1,4),wv))))
 q=add(lin((Q(11,4),ONE),(Q(13,8),w),(Q(-1,8),v),(2,wv)),scale(mul(E,lin((-1,w),(1,v),(1,wv))),Q(1,64)))
 pts=[p,q]+[lin((a,ONE),(b,w),(c,v),(d,wv)) for a,b,c,d in rows]
 need(len(set(pts))==29,'seed distinctness');return pts

def evaluate(x):
 out=0
 for i,a in enumerate(x):
  need(a.denominator%MOD!=0,'denominator modulo new prime')
  z=a.numerator*pow(a.denominator,-1,MOD)%MOD
  for k,r in enumerate(ROOTS):
   if i&(1<<k):z=z*r%MOD
  out=(out+z)%MOD
 return out

def apply(f,x):
 t,u,k=f;return add(t,mul(u,bar(x) if k else x))
def compose(f,g):
 t,u,k=f;s,v,l=g
 return (add(t,mul(u,bar(s) if k else s)),mul(u,bar(v) if k else v),k^l)

def graph(points):
 a,b,c,e=ROOTS
 need((a*a+3)%MOD==0 and (b*b+11)%MOD==0 and (c*c-5)%MOD==0 and (e*e+3320-632*a*b)%MOD==0,'fresh residue homomorphism')
 values=[evaluate(x) for x in points];conjs=[evaluate(bar(x)) for x in points]
 edges=[];false=0
 for i,j in combinations(range(len(points)),2):
  if (values[i]-values[j])*(conjs[i]-conjs[j])%MOD==1:
   if norm(sub(points[i],points[j]))==ONE:edges.append((i,j))
   else:false+=1
 return edges,false

def verify(cert,rows):
 need(type(cert) is dict and set(cert)=={'version','generator_anchors','copy_tape','address_colours','physical_vertices','copies','producer_modular_edges'},'certificate keys')
 need(cert['version']==1,'version')
 pts=seed(rows);gs=[]
 for r in cert['generator_anchors']:
  need(type(r) is list and len(r)==5 and all(type(x) is int for x in r),'anchor format')
  i,j,k,l,flip=r
  need(all(0<=x<29 for x in r[:4]) and flip in (0,1) and i!=j and k!=l,'anchor bounds')
  x=sub(pts[j],pts[i]);y=sub(pts[l],pts[k]);need(norm(x)==norm(y),'anchor congruence')
  if flip:x=bar(x)
  u=mul(y,inv(x));t=sub(pts[k],mul(u,bar(pts[i]) if flip else pts[i]))
  g=(t,u,flip)
  need(norm(u)==ONE and apply(g,pts[i])==pts[k] and apply(g,pts[j])==pts[l],'physical isometry')
  gs.append(g)
 need(len(gs)==len(set(gs))==62,'generator count')
 fs=[(ZERO,ONE,0)]
 for r in cert['copy_tape']:
  need(type(r) is list and len(r)==2 and all(type(x) is int for x in r),'copy tape format')
  p,g=r;need(0<=p<len(fs) and 0<=g<len(gs),'acyclic copy tape')
  fs.append(compose(fs[p],gs[g]))
 need(len(fs)==len(set(fs))==cert['copies']==64,'copy count')
 word=cert['address_colours'];need(type(word) is str and len(word)==29*len(fs) and set(word)<={'0','1','2','3'},'address colours')
 physical={};cursor=0;prefix=[]
 for f in fs:
  for x in pts:
   y=apply(f,x);colour=int(word[cursor]);cursor+=1
   if y in physical:need(physical[y]==colour,'coincident address colours')
   physical[y]=colour
  prefix.append(len(physical))
 need(len(physical)==cert['physical_vertices'] and len(physical)<=508,'physical order')
 ordered=sorted(physical);edges,false=graph(ordered)
 need(all(physical[ordered[i]]!=physical[ordered[j]] for i,j in edges),'monochromatic physical edge')
 selected=set(fs);internal=sum(compose(f,g) in selected for f in fs for g in gs)
 canonical='\n'.join(','.join(str(a) for a in x) for x in ordered).encode()
 return {'verified':True,'copies':len(fs),'generators':len(gs),'formal_addresses':len(word),'distinct_physical_points':len(ordered),'strict_unit_edges':len(edges),'all_pairs_checked':len(ordered)*(len(ordered)-1)//2,'fresh_modulus':MOD,'fresh_modulus_false_edges':false,'closed_directed_generator_transitions':internal,'all_directed_generator_transitions':len(fs)*len(gs),'four_colourable':True,'record_improvement':False,'prefix_orders':prefix,'canonical_physical_points_sha256':hashlib.sha256(canonical).hexdigest()}

def main():
 p=argparse.ArgumentParser();p.add_argument('--certificate',type=Path,default=HERE/'certificate.json');p.add_argument('--check-expected',action='store_true');a=p.parse_args()
 out=verify(json.loads(a.certificate.read_text()),json.loads((HERE/'seed.json').read_text())['moser_rows'])
 if a.check_expected:need(out==json.loads((HERE/'EXPECTED.json').read_text()),'expected output')
 print(json.dumps(out,indent=2,sort_keys=True))
if __name__=='__main__':main()
