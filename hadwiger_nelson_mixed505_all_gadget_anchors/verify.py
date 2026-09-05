#!/usr/bin/env python3
"""Exact all-anchor mixed505 census with integer projective arithmetic."""

from pathlib import Path
from collections import Counter,defaultdict
from hashlib import sha256
from math import gcd,isqrt
from itertools import permutations
from functools import cache
import json,struct,time,sys

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
ZERO=(0,0,0,0)
NAMES=('no_unit_roots','roots_in_E','outside_E_pairs')

def require(ok,msg):
 if not ok:raise ValueError(msg)

def read_points(n):
 pins={159:'4f72fa06d18434472ce77cebe38880333694ec04b94945ede073a4a1c6d5bc02',214:'97c9b3a964ed19874ae3fe932eb8c085fd637f618d2481fffaebbd1fbae55c2f'}
 raw=(ROOT/f'hadwiger_nelson_nonmono159_214_lowden2/points{n}.tsv').read_bytes()
 require(sha256(raw).hexdigest()==pins[n],'coordinate pin mismatch')
 require(raw.decode().splitlines()[0]=='# scale 12','wrong scale')
 rows=[]
 for line in raw.decode().splitlines():
  if not line or line.startswith('#'):continue
  a=tuple(map(int,line.split()));require(len(a)==16 and not any(a[i] for i in range(16) if i not in (0,5,9,12)),'unsupported coordinate')
  rows.append(tuple(a[i] for i in (0,5,9,12)))
 require(len(rows)==len(set(rows))==n,'wrong coordinate count')
 return rows

def subtract(a,b):return tuple(x-y for x,y in zip(a,b))
def norm(v):
 a,b,c,d=v
 return (a*a+33*b*b+3*c*c+11*d*d,2*(a*b+c*d))

def edges(V,scale):
 return [(i,j) for i in range(len(V)) for j in range(i+1,len(V)) if norm(subtract(V[i],V[j]))==(scale*scale,0)]

def construction():
 A=read_points(159);V=read_points(214)
 B=list(dict.fromkeys([tuple(6*x for x in a) for a in A]+[(5*a-11*d,5*b-c,5*c+11*b,5*d+a) for a,b,c,d in A]))
 require(len(B)==292 and B[0]==ZERO,'wrong B assembly')
 require({(a,b,-c,-d) for a,b,c,d in V}==set(V),'V is not conjugation-invariant')
 raw_inc=defaultdict(list)
 for q,a in enumerate(V):
  for j,b in enumerate(V):
   if q!=j:raw_inc[subtract(b,a)].append((q,j))
 D=[ZERO]+sorted(raw_inc);inc=[[]]+[raw_inc[d] for d in D[1:]]
 require(len(D)==4419,'wrong difference set')
 EB,EV=edges(B,72),edges(V,12)
 require((len(EB),len(EV))==(1251,977),'wrong internal edges')
 return B,V,D,inc,EB,EV

def sign_real(p,q):
 if p==0:return (q>0)-(q<0)
 if q==0:return (p>0)-(p<0)
 if p>0 and q>0:return 1
 if p<0 and q<0:return -1
 r=p*p-33*q*q
 return ((r>0)-(r<0))*(1 if p>0 else -1)

def rational_square(n,d):
 if n<0:return False
 g=gcd(n,d);n//=g;d//=g
 return isqrt(n)**2==n and isqrt(d)**2==d

def field_roots(p,q):
 # Tests whether (p+q*sqrt(33))/3 is a square in Q(sqrt(33)).
 if q==0:return rational_square(p,3) or rational_square(p,99)
 N=p*p-33*q*q
 if N<0:return False
 k=isqrt(N)
 if k*k!=N:return False
 return any(p+e*k>0 and rational_square(p+e*k,6) for e in (-1,1))

def primitive(den,*nums):
 g=gcd(den,*nums)
 if den<0:g=-g
 return tuple(x//g for x in (den,)+nums)

def classify(b,d,nb,nd):
 S0,S1=nb[0]+36*nd[0]-5184,nb[1]+36*nd[1]
 delta0=144*(nb[0]*nd[0]+33*nb[1]*nd[1])-S0*S0-33*S1*S1
 delta1=144*(nb[0]*nd[1]+nb[1]*nd[0])-2*S0*S1
 if sign_real(delta0,delta1)<0:return 0,None
 if field_roots(delta0,delta1):return 1,None
 A,B,C,D=b;a,h,c,e=d
 cr0=A*a+33*B*h+3*C*c+11*D*e
 cr1=A*h+B*a+C*e+D*c
 ci0=3*(A*c+11*B*e-C*a-11*D*h)
 ci1=A*e+3*B*c-D*a-3*C*h
 if (S0,S1)!=(0,0):
  key=(0,)+primitive(S0*S0-33*S1*S1,cr0*S0-33*cr1*S1,cr1*S0-cr0*S1,ci0*S0-33*ci1*S1,ci1*S0-ci0*S1)
 elif (cr0,cr1)!=(0,0):
  key=(1,)+primitive(cr0*cr0-33*cr1*cr1,ci0*cr0-33*ci1*cr1,ci1*cr0-ci0*cr1)
 else:key=(2,)
 return 2,key

def enumerate_groups(B,D,progress=False):
 normsB=list(map(norm,B));normsD=list(map(norm,D));counts=Counter();groups=defaultdict(list);classification=sha256();start=time.monotonic()
 for i,b in enumerate(B[1:],1):
  for j,d in enumerate(D[1:],1):
   case,key=classify(b,d,normsB[i],normsD[j]);counts[NAMES[case]]+=1
   classification.update(f'{i},{j}:{NAMES[case]}\n'.encode())
   if case==2:groups[key].append((i,j))
  if progress and i%50==0:print('B rows',i,'classes',len(groups),'seconds',round(time.monotonic()-start,2),file=sys.stderr,flush=True)
 return dict(counts),groups,classification.hexdigest()

def libraries(B,V,EB,EV):
 files=[(ROOT/'hadwiger_nelson_nonmono159_moser_triple/colors_B.txt',B,EB,'b9285f2967686bf5458588c6f949173ac8795412a7ffd94a60d687e5a8c260a3'),(ROOT/'hadwiger_nelson_mixed505_anchor0/colors_H.txt',V,EV,'25a072d1c55cef2318b76cd849ce3096091d25b37981c83bc11d00c416393b58')]
 libs=[]
 for path,pts,ee,pin in files:
  raw=path.read_bytes();require(sha256(raw).hexdigest()==pin,'wrong coloring bytes')
  lib=[tuple(map(int,s)) for s in raw.decode().splitlines()]
  require(all(len(c)==len(pts) and all(x in range(4) for x in c) and all(c[i]!=c[j] for i,j in ee) for c in lib),'bad internal coloring')
  libs.append(lib)
 require(all(c[0]==0 for c in libs[0]),'B origin color is nonzero')
 return libs

def cover(groups,inc,libB,libV,progress=False):
 perms=[(0,)+p for p in permutations((1,2,3))]
 choices=[(i,j,k) for i in range(len(libB)) for j in range(len(libV)) for k in range(6)]
 FULL=(1<<len(choices))-1
 sigB=list(zip(*libB));sigV=list(zip(*libV))
 @cache
 def mask(bs,qs,vs):
  return sum(1<<r for r,(i,j,k) in enumerate(choices) if bs[i]!=perms[k][vs[j]^qs[j]])
 partition,coverage=sha256(),sha256();hist=[Counter() for _ in sigV];residual=[0]*len(sigV);top=[];total=0;maximum=0
 for gi,ee in enumerate(sorted(groups.values())):
  partition.update((';'.join(f'{b},{d}' for b,d in ee)+'\n').encode())
  by_anchor=defaultdict(list)
  for b,d in ee:
   for q,v in inc[d]:by_anchor[q].append((b,v))
  for q,qe in sorted(by_anchor.items()):
   hist[q][len(qe)]+=1;total+=1;maximum=max(maximum,len(qe));ok=FULL
   for b,v in qe:ok &=mask(sigB[b],sigV[q],sigV[v])
   if ok:
    w=(ok&-ok).bit_length()-1;i,j,k=choices[w];pi=perms[k]
    require(all(libB[i][b]!=pi[libV[j][v]^libV[j][q]] for b,v in qe),'invalid selected coloring')
   else:
    w=-1;residual[q]+=1
    top.append({'anchor':q,'ambient_class':gi,'cross_edges':sorted(qe),'ambient_edges':ee})
    top.sort(key=lambda x:(-len(x['cross_edges']),x['anchor'],x['ambient_class']));top=top[:20]
   coverage.update(struct.pack('<IIi',gi,q,w))
  if progress and gi and gi%100000==0:print('projected',gi,'anchor classes',total,'residual',sum(residual),file=sys.stderr,flush=True)
 return {'ambient_edge_partition_sha256':partition.hexdigest(),'coverage_sha256':coverage.hexdigest(),'anchor_classes_total':total,'maximum_cross_edges':maximum,'uncovered_total':sum(residual),'anchors':[{'anchor':q,'classes':sum(h.values()),'unit_multipliers':2*sum(h.values()),'histogram':dict(sorted(h.items())),'uncovered':residual[q]} for q,h in enumerate(hist)]},top

def anchor_table(rows):
 out=['anchor\tclasses\tunit_multipliers\tmax_cross_edges\tuncovered\thistogram\n']
 for r in rows:
  out.append(f"{r['anchor']}\t{r['classes']}\t{r['unit_multipliers']}\t{max(r['histogram'])}\t{r['uncovered']}\t"+json.dumps(r['histogram'],separators=(',',':'))+'\n')
 return ''.join(out)

def main():
 import argparse
 parser=argparse.ArgumentParser(description=__doc__)
 parser.add_argument('--anchors',type=Path,help='write the full compact anchor table')
 args=parser.parse_args()
 B,V,D,inc,EB,EV=construction();libB,libV=libraries(B,V,EB,EV)
 counts,groups,ch=enumerate_groups(B,D)
 result,top=cover(groups,inc,libB,libV)
 require(result['uncovered_total']==0,'uncovered anchor/quadratic class')
 table=anchor_table(result.pop('anchors'))
 if args.anchors:args.anchors.write_text(table)
 result={'B_vertices':len(B),'V_vertices':len(V),'difference_vectors':len(D)-1,'nonzero_pairs':(len(B)-1)*(len(D)-1),'pairs':counts,'ambient_classes':len(groups),'classification_sha256':ch,**result,'anchor_table_sha256':sha256(table.encode()).hexdigest()}
 print(json.dumps(result,indent=2))

if __name__=='__main__':main()
