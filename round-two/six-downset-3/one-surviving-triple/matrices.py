"""Literal centered cores using an independent Fraction Gaussian solve."""
from fractions import Fraction as F
import math
import bootstrap
from literal import gaussian,delta,domain as old_domain
from systems import ST,QT
from exact import require,schur_psd,lift,digest

def choose(n,k):return math.comb(n,k) if 0<=k<=n else 0
def typ(x):return ((x&6).bit_count(),int(bool(x&8)),(x>>4).bit_count())
def count(q,t):u,d,w=t;return choose(2,u)*choose(1,d)*choose(q-1,w)
def disjoint(q,row,col):
 u,d,w=row;z,e,h=col
 return choose(2-u,z)*choose(1-d,e)*choose(q-1-w,h)

def solve_potentials(q):
 require(type(q) is int and q>=4,'q must be an integer at least four')
 s=3*q+4;m=(q+2)*(q+3)//2+1
 A=[[disjoint(q,x,y) for y in QT] for x in ST]
 E=[[disjoint(q,x,y) for y in ST] for x in QT]
 ds=[sum(row) for row in A];es=[sum(row) for row in E]
 a=len(ST);b=len(QT)
 matrix=[];rhs=[]
 for i in range(a):
  matrix.append([ds[i]*int(h==i) for h in range(a)]+A[i][:-1]);rhs.append(m-ds[i])
 for j in range(b-1):
  matrix.append(E[j]+[es[j]*int(h==j) for h in range(b-1)]);rhs.append(s-es[j])
 answer=gaussian(matrix,rhs);p=answer[:a];r=answer[a:]+[F(0)]
 require(all(ds[i]*p[i]+sum(A[i][j]*r[j] for j in range(b))==m-ds[i] for i in range(a)),'cross row balance')
 require(all(es[j]*r[j]+sum(E[j][i]*p[i] for i in range(a))==s-es[j] for j in range(b)),'cross column balance')
 internal=[[disjoint(q,x,y) for y in QT] for x in QT]
 degree=[sum(row) for row in internal]
 normal=[[degree[i]*int(i==j)+internal[i][j] for j in range(b)] for i in range(b)]
 d=gaussian(normal,[m-s]*b)
 require(all(degree[i]*d[i]+sum(internal[i][j]*d[j] for j in range(b))==m-s for i in range(b)),'internal balance')
 return p,r,d

def build(q):
 X=sorted(old_domain(q)+[14]);Y=X[1:];n=len(X);s=3*q+4;m=n-1-s
 require(n==(q*q+11*q+18)//2,'new domain size')
 require({typ(x) for x in Y if x&1}==set(ST) and {typ(x) for x in Y if not x&1}==set(QT),'type coverage')
 p,r,d=solve_potentials(q)
 C=[]
 for x in Y:
  row=[]
  for y in Y:
   if x&1 and y&1:z=F(s*int(x==y)-1)
   elif not x&1 and not y&1:
    z=F(s-1) if x==y else F(-1) if x&y else -1+d[QT.index(typ(x))]+d[QT.index(typ(y))]
   else:
    xx,yy=(x,y) if x&1 else (y,x)
    z=F(-1) if x&y else p[ST.index(typ(xx))]+r[QT.index(typ(yy))]
   row.append(z)
  C.append(row)
 require(all(sum(row)==0 for row in C),'centered whole core')
 star=[int(bool(x&1)) for x in Y];other=[1-x for x in star]
 require(sum(star)==s and sum(other)==m,'partition sizes')
 require(all(sum(row[j]*star[j] for j in range(n-1))==0 for row in C),'star kernel')
 require(all(C[i][j]==C[j][i] and (C[i][j]==s-1 if i==j else C[i][j]==-1 if Y[i]&Y[j] else True) for i in range(n-1) for j in range(n-1)),'exact support')
 U=[[F(n*int(i==j)-1)-C[i][j] for j in range(n-1)] for i in range(n-1)]
 P=[[F(i==j)-F(star[i]*star[j],s)-F(other[i]*other[j],m) for j in range(n-1)] for i in range(n-1)]
 return X,C,U,P,{'q':q,'N':n,'s':s,'m':m,'p':[str(x) for x in p],'r':[str(x) for x in r],'internal_d':[str(x) for x in d]}

def domain(q):
 return sorted(old_domain(q)+[14])

def construct(q,t):
 require(type(q) is int and q>=4,'q must be an integer at least four')
 require(isinstance(t,(int,F)) and not isinstance(t,bool),'inexact repair parameter')
 require(0<t<=F(1,12*q*(q+1)*(q+2)),'repair outside sufficient interval')
 X,C,_,_,_=build(q);trade=delta(X,q)
 return X,lift([[x+t*trade[i][j] for j,x in enumerate(row)] for i,row in enumerate(C)])

def verify_full(q,X,L):
 require(type(q) is int and q>=4,'q must be an integer at least four')
 n=len(X);s=3*q+4
 require(X==domain(q) and n==(q*q+11*q+18)//2,'wrong original domain')
 require(len(L)==n and all(len(row)==n for row in L),'wrong full matrix dimensions')
 require(all(isinstance(x,(int,F)) and not isinstance(x,bool) for row in L for x in row),'inexact full matrix')
 require(all(L[i][j]==L[j][i] for i in range(n) for j in range(n)),'whole symmetry')
 require(all(sum(row)==n for row in L),'whole row sum')
 require(all(L[i][j]==s*int(i==j) for i in range(n) for j in range(n) if X[i]&X[j]),'whole support')
 z=[F(bool(x&1))-F(s,n) for x in X]
 require(all(sum(row[j]*z[j] for j in range(n))==0 for row in L),'whole centered a-star')
 require(schur_psd(L)==n-1,'whole greatest lower rank')
 require(schur_psd([[F(n*int(i==j))-L[i][j] for j in range(n)] for i in range(n)])==n-1,'whole simple unit rank')
