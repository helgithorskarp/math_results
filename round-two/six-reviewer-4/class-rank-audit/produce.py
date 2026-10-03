"""Exact full positive witnesses; complete fractional congruence evidence."""
import json,sys
from pathlib import Path
from fractions import Fraction as F
from math import comb
from exact import need,canon,digest,ldlt
from model import table,sectors,original_rows

def run(w):
 out=[]
 for case in w['cases']:
  n=case['n'];N=2**n-n-1;s=2**(n-1)-n;b=table(case);eps=F(case['floor']);need(eps>0,'positive floor');parts=[];lr=0;ur=0;dim=0
  for p in sectors(n,b):
   L=p['lower'];U=p['upper'];g=p['g'];keep=p['keep'];m=len(g)
   for z in p['kernels']:need(all(sum(L[i][k]*z[k]for k in range(m))==0 for i in range(m)),'full kernel')
   A=[[L[i][k]-(eps*g[i]if i==k else 0)for k in keep]for i in keep];V=[[U[i][k]-(eps*g[i]if i==k else 0)for k in range(m)]for i in range(m)]
   rank,lp=ldlt(L);u,up=ldlt(U);a,ap=ldlt(A);v,vp=ldlt(V)
   need(rank==m-len(p['kernels'])and a==len(keep),'complete lower kernel');need(u==m and v==m,'complete upper floor')
   lr+=rank*p['multiplicity'];ur+=u*p['multiplicity'];dim+=m*p['multiplicity']
   parts.append({k:p[k]for k in ['j','layers','g','multiplicity','keep']}|dict(lower=[[str(x)for x in r]for r in L],upper=[[str(x)for x in r]for r in U],kernels=[[str(x)for x in r]for r in p['kernels']],lower_rank=rank,upper_rank=u,lower_pivots=lp,upper_pivots=up,lower_floor_pivots=ap,upper_floor_pivots=vp))
  need(dim==N-1,'whole harmonic dimension');q=sum(comb(n,a)for a in range(2,n//2)if a not in case['active']);need(1+lr==N-n-q and ur==N-1,'weighted exact original rank')
  out.append(dict(n=n,N=N,s=s,h=N-s,active=case['active'],coordinate_count=len(case['names']),floor=str(eps),table=[[str(x)for x in row]for row in b],original=original_rows(n,b),parts=parts,q=q,lower_rank=1+lr,upper_rank=ur,gap=str(eps/(N-s))))
 return dict(cases=out)
if __name__=='__main__':
 w=json.loads(Path(__file__).with_name('WITNESS.json').read_text());v=run(w);Path(sys.argv[1]).write_bytes(canon(v));print(json.dumps({'complete':True,'bytes':len(canon(v)),'sha256':digest(v),'ranks':[(c['n'],c['lower_rank'],c['upper_rank'])for c in v['cases']]}))
