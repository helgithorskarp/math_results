"""Fresh exact helpers: rational congruence and independent determinant interpolation."""
from fractions import Fraction as F
from math import gcd,lcm
import hashlib,json

def need(ok,why):
 if not ok:raise ValueError(why)
def canon(v):return json.dumps(v,sort_keys=True,separators=(',',':')).encode()+b'\n'
def digest(v):return hashlib.sha256(canon(v)).hexdigest()
def rref(a):
 a=[list(map(F,r))for r in a]; piv=[];at=0
 if not a:return a,piv
 for c in range(len(a[0])):
  k=next((k for k in range(at,len(a))if a[k][c]),None)
  if k is None:continue
  a[at],a[k]=a[k],a[at];q=a[at][c];a[at]=[v/q for v in a[at]]
  for k in range(len(a)):
   if k!=at:
    q=a[k][c]
    if q:a[k]=[x-q*y for x,y in zip(a[k],a[at],strict=True)]
  piv.append(c);at+=1
  if at==len(a):break
 return a,piv

def ldlt(a):
 """Diagonal pivot congruence; zero diagonal forces an entirely zero row."""
 n=len(a);need(all(len(r)==n for r in a),'square');a=[list(map(F,r))for r in a]
 need(all(a[i][j]==a[j][i]for i in range(n)for j in range(n)),'symmetric');p=[]
 while a:
  need(all(a[i][i]>=0 for i in range(len(a))),'negative pivot')
  k=next((i for i in range(len(a))if a[i][i]>0),None)
  if k is None:need(not any(x for r in a for x in r),'zero diagonal nonzero row');break
  if k:a[0],a[k]=a[k],a[0];a=[r[k:k+1]+r[1:k]+r[:1]+r[k+1:]for r in a]
  q=a[0][0];p.append(str(q));a=[[a[i][j]-a[i][0]*a[0][j]/q for j in range(1,len(a))]for i in range(1,len(a))]
 return len(p),p

def determinant(a):
 """Integer Bareiss determinant including row exchange and singular zero."""
 a=[r[:]for r in a];n=len(a)
 if not n:return 1
 sign=1;previous=1
 for k in range(n-1):
  t=next((i for i in range(k,n)if a[i][k]),None)
  if t is None:return 0
  if t!=k:a[t],a[k]=a[k],a[t];sign=-sign
  p=a[k][k]
  for i in range(k+1,n):
   for j in range(k+1,n):
    z=a[i][j]*p-a[i][k]*a[k][j];need(z%previous==0,'Bareiss division');a[i][j]=z//previous
   a[i][k]=0
  previous=p
 return sign*a[-1][-1]

def polynomial_psd(a):
 """det(t I+D A), all coefficients; no PSD pivot assumptions or known kernels."""
 n=len(a);need(all(len(r)==n for r in a),'poly square');need(all(a[i][j]==a[j][i]for i in range(n)for j in range(n)),'poly symmetry')
 den=lcm(*(x.denominator for r in a for x in r));b=[[int(x*den)for x in r]for r in a]
 values=[determinant([[b[i][j]+(t if i==j else 0)for j in range(n)]for i in range(n)])for t in range(n+1)]
 dif=[];row=values[:]
 while row:dif.append(row[0]);row=[row[i+1]-row[i]for i in range(len(row)-1)]
 coef=[F(0)]*(n+1);basis=[F(1)]
 for k,d in enumerate(dif):
  for i,v in enumerate(basis):coef[i]+=d*v
  if k<n:
   new=[F(0)]*(len(basis)+1)
   for i,v in enumerate(basis):new[i]-=k*v/(k+1);new[i+1]+=v/(k+1)
   basis=new
 need(all(x.denominator==1 for x in coef),'integer determinant polynomial');coef=list(map(int,coef));need(coef[-1]==1,'monic')
 # One unused interpolation point independently checks the entire reconstruction.
 t=n+1;need(sum(v*t**i for i,v in enumerate(coef))==determinant([[b[i][j]+(t if i==j else 0)for j in range(n)]for i in range(n)]),'full polynomial reconstruction')
 need(all(v>=0 for v in coef),'negative characteristic coefficient');null=next(i for i,v in enumerate(coef)if v)
 return n-null,dict(denominator=den,coefficients=coef,unused_point=t)
