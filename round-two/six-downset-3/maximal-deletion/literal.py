"""Literal matrices, rational balancing solve and complete action checks."""
import math
from itertools import combinations
from fractions import Fraction as F
import bootstrap
from symbolic import R,ST,QT,DEGREES,sector,require
from exact import schur_psd,lift,digest,polynomial_psd

def validate_q(q):
 require(type(q) is int and q>=4,'literal q must be an integer at least four')

def gaussian(matrix,rhs):
 n=len(matrix)
 require(n>0 and all(len(row)==n for row in matrix) and len(rhs)==n,'literal linear system dimensions')
 a=[[F(x) for x in row]+[F(rhs[i])] for i,row in enumerate(matrix)]
 for k in range(n):
  h=next((i for i in range(k,n) if a[i][k]),None)
  require(h is not None,'singular literal linear system')
  a[k],a[h]=a[h],a[k]
  scale=a[k][k];a[k]=[x/scale for x in a[k]]
  for i in range(n):
   if i!=k:
    scale=a[i][k];a[i]=[x-scale*y for x,y in zip(a[i],a[k])]
 return [row[-1] for row in a]

def potentials(q):
 """Independent rational Gaussian solve, without symbolic field elimination."""
 validate_q(q);s=3*q+4;m=(q+2)*(q+3)//2
 choose=lambda n,k:math.comb(n,k) if 0<=k<=n else 0
 A=[[choose(2-u,z)*choose(q-w,h) for z,h in QT] for u,w in ST]
 E=[[choose(2-z,u)*choose(q-h,w) for u,w in ST] for z,h in QT]
 ds=[sum(row) for row in A];es=[sum(row) for row in E]
 matrix=[];rhs=[]
 for i in range(5):
  matrix.append([ds[i]*int(h==i) for h in range(5)]+A[i][:4]);rhs.append(m-ds[i])
 for j in range(4):
  matrix.append(E[j]+[es[j]*int(h==j) for h in range(4)]);rhs.append(s-es[j])
 x=gaussian(matrix,rhs);p=x[:5];r=x[5:]+[F(0)]
 require(all(ds[i]*p[i]+sum(A[i][j]*r[j] for j in range(5))==m-ds[i] for i in range(5)),'literal row balance')
 require(all(es[j]*r[j]+sum(E[j][i]*p[i] for i in range(5))==s-es[j] for j in range(5)),'literal column balance')
 return p,r

def delta(X,q):
 """Credited all-star trade: all nonempty vertices retained, larger layers zero."""
 validate_q(q);weights={(1,1):q*(q+1),(1,2):-q,(2,2):1}
 return [[F(weights.get(tuple(sorted((a.bit_count(),b.bit_count()))),0)) if not a&b else F(0) for b in X[1:]] for a in X[1:]]

def construct(q,t):
 validate_q(q)
 require(isinstance(t,(int,F)) and not isinstance(t,bool),'inexact repair parameter')
 require(0<t<=F(1,12*q*(q+1)*(q+2)),'repair outside proved sufficient interval')
 p,r=potentials(q);X,C=literal(q,p,r);d=delta(X,q)
 Ct=[[C[i][j]+t*d[i][j] for j in range(len(C))] for i in range(len(C))]
 return X,lift(Ct)

def verify_full(q,X,L):
 validate_q(q);n=len(X);s=3*q+4
 require(n==(q*q+11*q+16)//2 and X==domain(q),'wrong original vertex domain')
 require(len(L)==n and all(len(row)==n for row in L),'wrong full matrix dimensions')
 require(all(isinstance(x,(int,F)) for row in L for x in row),'inexact full matrix')
 require(all(L[i][j]==L[j][i] for i in range(n) for j in range(n)),'whole symmetry')
 require(all(sum(row)==n for row in L),'whole row sum')
 require(all(L[i][j]==s*int(i==j) for i in range(n) for j in range(n) if X[i]&X[j]),'whole support')
 z=[F(bool(x&1))-F(s,n) for x in X]
 require(all(sum(row[j]*z[j] for j in range(n))==0 for row in L),'whole forced centered star')
 require(schur_psd(L)==n-1,'whole maximal lower rank')
 require(schur_psd([[F(n*int(i==j))-L[i][j] for j in range(n)] for i in range(n)])==n-1,'whole simple unit rank')

def read_r(rec):return R(tuple(F(x) for x in rec['numerator']),tuple(F(x) for x in rec['denominator']))

def domain(q):
 p=q+3
 validate_q(q)
 masks=[]
 for size in [1,2,3]:
  for subset in combinations(range(p),size):
   x=sum(1<<i for i in subset)
   if size<=2 or x&1 and x&6:masks.append(x)
 return [0]+sorted(masks)

def literal(q,p,r):
 X=domain(q);Y=X[1:];s=3*q+4;n=len(X)
 typ=lambda x:((x&6).bit_count(),(x>>3).bit_count())
 C=[]
 for x in Y:
  row=[]
  for y in Y:
   if x&1 and y&1:z=F(s*int(x==y)-1)
   elif not x&1 and not y&1:z=F(s-1) if x==y else F(-1) if x&y or x.bit_count()==y.bit_count()==1 else F(-2,q)
   else:
    sx,qq=(x,y) if x&1 else (y,x)
    z=F(-1) if x&y else p[ST.index(typ(sx))]+r[QT.index(typ(qq))]
   row.append(z)
  C.append(row)
 return X,C

def harmonic(x,j,ell):
 core=1 if j==0 else int(bool(x&2))-int(bool(x&4))
 w=x>>3
 outside=1 if ell==0 else int(bool(w&1))-int(bool(w&2)) if ell==1 else (int(bool(w&1))-int(bool(w&2)))*(int(bool(w&4))-int(bool(w&8)))
 return core*outside

def check(q,p,r,sp,rp):
 s=3*q+4;X,C=literal(q,p,r);Y=X[1:];n=len(X);m=n-1-s
 require(all(a.at(q-4)==b for a,b in zip(sp+rp,p+r)),'symbolic/literal potential mismatch')
 count=0;dims=[];secondary=0
 typ=lambda x:((x&6).bit_count(),(x>>3).bit_count())
 for j,ell in DEGREES:
  b=sector(R(q),[R(v) for v in p],[R(v) for v in r],j,ell)
  columns=[];levels=[];norms=[]
  for isstar,kinds,norm in [(True,b['S_types'],b['S_norms']),(False,b['Q_types'],b['Q_norms'])]:
   for t,h in zip(kinds,norm):
    col=[harmonic(x,j,ell) if bool(x&1)==isstar and typ(x)==t else 0 for x in Y]
    require(sum(x*x for x in col)==h.at(0)*2**(j+ell),'literal lift norm')
    columns.append(col);levels.append((isstar,t));norms.append(h.at(0))
  ns=len(b['S_types']);nq=len(b['Q_types']);H=[]
  for a in range(ns+nq):
   row=[]
   for c in range(ns+nq):
    if a<ns and c<ns:z=F(s*int(a==c))-(norms[c] if j==ell==0 else 0)
    elif a<ns:z=b['B_action'][a][c-ns].at(0)
    elif c<ns:z=b['BT_action'][a-ns][c].at(0)
    else:z=b['D_action'][a-ns][c-ns].at(0)
    row.append(z)
   H.append(row)
  for h,col in enumerate(columns):
   lhs=[sum(row[k]*col[k] for k in range(n-1)) for row in C]
   rhs=[sum(columns[a][k]*H[a][h] for a in range(len(columns))) for k in range(n-1)]
   require(lhs==rhs,'literal whole sector action');count+=1
  for name in ['lower','upper']:
   G=[[v.at(0) for v in row] for row in b[name]]
   require(schur_psd(G)==nq-int(j==ell==0),'literal Schur quotient rank')
   if q==4:
    require(polynomial_psd(G)[0]==nq-int(j==ell==0),'independent characteristic-polynomial rank')
    secondary+=1
  copies=1 if ell==0 else q-1 if ell==1 else q*(q-3)//2
  dims.append(len(columns)*copies)
 require(sum(dims)==n-1,'complete sector dimension sum')
 star=[int(bool(x&1)) for x in Y];other=[1-x for x in star]
 P=[[F(int(i==j))-F(star[i]*star[j],s)-F(other[i]*other[j],m) for j in range(n-1)] for i in range(n-1)]
 U=[[F(n*int(i==j)-1)-C[i][j] for j in range(n-1)] for i in range(n-1)]
 require(schur_psd([[C[i][j]-P[i][j]/4 for j in range(n-1)] for i in range(n-1)])==n-3,'whole lower quarter floor')
 require(schur_psd([[U[i][j]-F(i==j)/4 for j in range(n-1)] for i in range(n-1)])==n-1,'whole upper quarter floor')
 d=delta(X,q);K=3*q*(q+1)*(q+2)//2;t=F(1,8*K)
 require(max(sum(abs(v) for v in row) for row in d)<=K,'trade row-sum norm bound')
 Ct=[[C[i][j]+t*d[i][j] for j in range(n-1)] for i in range(n-1)]
 Ut=[[U[i][j]-t*d[i][j]-F(i==j)/8 for j in range(n-1)] for i in range(n-1)]
 require(schur_psd(Ct)==n-2 and schur_psd(Ut)==n-1,'closed repaired rank and upper eighth floor')
 L=lift(Ct);V=[[F(n*int(i==j))-L[i][j] for j in range(n)] for i in range(n)]
 require(schur_psd(L)==n-1 and schur_psd(V)==n-1,'whole ranks')
 require(all(sum(row)==n for row in L),'whole row sum')
 verify_full(q,X,L)
 require(schur_psd([[V[i][j]-(F(i==j)-F(1,n))/8 for j in range(n)] for i in range(n)])==n-1,'whole upper eighth floor')
 return {'q':q,'N':n,'s':s,'action_columns':count,'sector_dimensions_with_copies':dims,'t':str(t),'rank_L':n-1,'rank_upper':n-1,'whole_upper_eighth_floor':True,'secondary_characteristic_forms':secondary}
