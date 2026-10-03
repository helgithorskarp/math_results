"""Independent exact QQ(h,q) certificate generator; no producer modules/data."""
import json,sys
from pathlib import Path
from sympy import QQ
from sympy.polys.fields import field
from sectors import params,matrices
K,h,q=field('h,q',QQ);p=params(h,q);forms=matrices(p)
def poly(f):
 return [[list(m),[int(c.numerator),int(c.denominator)]]for m,c in sorted(f.items())]
def rf(f):
 f=K(f)
 return dict(n=poly(f.numer),d=poly(f.denom))
def block(name):
 if name in ['mu','alpha','beta']:metric=[K(1)];A=[[p[name]]]
 elif name in ['old_plus','old_minus']:metric=[K(1)];A=[[p['N']-1-(2*q if name=='old_plus'else 6*h)]]
 elif name=='odd_old':metric=[forms['odd'][0][0]];A=[[p['N']-1-forms['odd'][1][0][0]/metric[0]]]
 elif name=='odd_mean':metric=[forms['odd'][0][3]];A=[[p['N']-1-forms['odd'][1][3][3]/metric[0]]]
 else:
  source,ind={'leaf':('leaf',[0,1]),'standard':('standard',[0,1,2,3]),'even_old':('even',[0,1,2]),'trace':('even',[3,4])}[name]
  gm,S=forms[source];metric=[gm[i]for i in ind]
  A=[[(p['N']-1 if i==j else 0)-S[r][c]/gm[r]for j,c in enumerate(ind)]for i,r in enumerate(ind)]
 orig=[[rf(a)for a in row]for row in A];pivots=[];updates=[]
 for k in range(len(A)):
  z=A[k][k];pivots.append(rf(z))
  for i in range(k+1,len(A)):
   for j in range(k+1,len(A)):
    before=A[i][j];left=A[i][k];right=A[k][j];after=before-left*right/z
    updates.append(dict(k=k,i=i,j=j,pivot=rf(z),before=rf(before),left=rf(left),right=rf(right),after=rf(after)))
    A[i][j]=after
 return dict(name=name,metric=[rf(a)for a in metric],original=orig,pivots=pivots,updates=updates)
name=sys.argv[1];r=block(name);out=Path(sys.argv[2]);out.write_text(json.dumps(r,sort_keys=True,separators=(',',':'))+'\n');print(json.dumps(dict(block=name,bytes=out.stat().st_size,pivots=len(r['pivots']),updates=len(r['updates']))))
