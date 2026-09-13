#!/usr/bin/env python3
"""Discover a portable norm-rigidity certificate by exact Macaulay linear algebra."""
import sympy as S,itertools,time,json
from pathlib import Path
a,b,c,d=S.symbols('a b c d');U=(a,b);V=(1-a,-b);W=(c,d);om=(S.Rational(1,2),S.Rational(1,2));om2=(-S.Rational(1,2),S.Rational(1,2))
add=lambda x,y:(x[0]+y[0],x[1]+y[1])
scale=lambda k,x:(k*x[0],k*x[1])
mul=lambda x,y:(S.expand(x[0]*y[0]-3*x[1]*y[1]),S.expand(x[0]*y[1]+x[1]*y[0]))
norm=lambda x:S.expand(x[0]**2+3*x[1]**2)
u,v,w=map(norm,(U,V,W));D=S.expand(u*v*w*(u-v)*(u-w)*(v-w)*(u-1)*(v-1)*(w-1));out=[]
from flint import fmpq_mat,fmpq
variables=(d,c,b,a)

def monomials(n):
 return sorted(t for t in itertools.product(range(n+1),repeat=4) if sum(t)<=n)
def terms(f):
 return [(list(m),str(co)) for m,co in S.Poly(f,*variables,domain=S.QQ).terms()]
def certify(F,G):
 for degree in range(max(2,max(S.Poly(g,*variables).total_degree() for g in G)),9):
  mm=monomials(degree);lookup={t:i for i,t in enumerate(mm)};shifts=monomials(degree-2);columns=[(i,t) for i in range(4) for t in shifts];n=len(columns);M=fmpq_mat(len(mm),n+len(G))
  for j,(i,t) in enumerate(columns):
   for m,co in S.Poly(F[i],*variables).terms():M[lookup[tuple(u+v for u,v in zip(m,t))],j]=fmpq(str(co))
  for j,g in enumerate(G):
   for m,co in S.Poly(g,*variables).terms():M[lookup[m],n+j]=fmpq(str(co))
  R,rank=M.rref();pivots=[];good=True
  for row in range(rank):
   pivot=next((j for j in range(n) if R[row,j]),None)
   if pivot is None:good=False;break
   pivots.append(pivot)
  if not good:continue
  certificates=[]
  for j,g in enumerate(G):
   cs=[[] for _ in F]
   for row,col in enumerate(pivots):
    co=R[row,n+j]
    if co:fi,m=columns[col];cs[fi].append([list(m),str(co)])
   # Verify coefficient identity immediately in the CAS too.
   pol=lambda ss:sum(S.Rational(co)*S.prod(v**e for v,e in zip(variables,m)) for m,co in ss)
   if S.expand(sum(pol(cs[i])*F[i] for i in range(4))-g)!=0:raise ValueError('bad Macaulay identity')
   certificates.append(cs)
  return degree,certificates
 raise ValueError('membership degree beyond bound')

import argparse
parser=argparse.ArgumentParser();parser.add_argument('--out',type=Path,required=True);args=parser.parse_args()
output=[];Delta=S.expand((u-v)*(u-w)*(v-w))
for signs in itertools.product((-1,1),repeat=5):
 e,s,t,k,l=signs;F=[norm(add(U,W))-1,norm(add(V,scale(e,W)))-1,norm(add(add(U,scale(s,mul(om,V))),scale(t,mul(om2,W))))-1,norm(add(add(U,scale(k,mul(om2,V))),scale(l,mul(om,W))))-1]
 start=time.time();gb=S.groebner(F,*variables,order='grevlex');G=[p.as_expr() for p in gb.polys];degree,identities=certify(F,G);delta_zero=gb.reduce(Delta)[1]==0
 targets=[Delta] if delta_zero else [S.expand(Delta*(4*n-1)*(4*n-3)*(4*n-7)) for n in (u,v,w)]
 if not all(gb.reduce(t)[1]==0 for t in targets):raise ValueError('norm classification fails')
 row={'signs':list(signs),'membership_degree':degree,'basis':[terms(g) for g in G],'identities':identities,'delta_zero':delta_zero};output.append(row)
 print(signs,'D',degree,'basis',len(G),'sec',round(time.time()-start,2),flush=True)
with args.out.open('x') as handle:
 json.dump(output,handle,sort_keys=True,separators=(',',':'));handle.write('\n')
print('complete',len(output))
