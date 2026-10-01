"""Exact complete sector forms over Q[u], q=4+u; see PROOF.md."""
import bootstrap
from fractions import Fraction as F
from poly import R,add,neg,mul,exact_divide,gcd
ST=((0,0),(0,1),(1,0),(1,1),(2,0))
QT=((0,1),(0,2),(1,0),(1,1),(2,0))
DEGREES=((0,0),(1,0),(0,1),(1,1),(0,2))

def require(ok,message):
 if not ok:raise ValueError(message)

def choose(n,k):
 if k<0 or isinstance(n,int) and (n<0 or k>n):return R(0)
 z=R(1)
 for h in range(k):z=z*(n-h)/(h+1)
 return z

def polynomial(x):
 x=R(x);require(x.d==(F(1),),'non-polynomial input')
 return x.n

def ff_eliminate(matrix,rhs=None):
 """Fraction-free Bareiss over Q[u]; no pivoting needed for our PD normal matrix."""
 n=len(matrix);require(n>0 and all(len(row)==n for row in matrix),'nonsquare form')
 a=[[polynomial(x) for x in row] for row in matrix]
 if rhs is not None:
  require(len(rhs)==n,'rhs dimension')
  for row,x in zip(a,rhs):row.append(polynomial(x))
 prev=(F(1),);minors=[]
 for k in range(n):
  pivot=a[k][k];require(pivot!=(F(0),),'zero leading pivot')
  minors.append(R(pivot))
  if k==n-1:break
  for i in range(k+1,n):
   for j in range(k+1,len(a[i])):
    a[i][j]=exact_divide(add(mul(pivot,a[i][j]),neg(mul(a[i][k],a[k][j]))),prev)
   a[i][k]=(F(0),)
  prev=pivot
 if rhs is None:return minors
 x=[R(0)]*n
 for i in reversed(range(n)):
  x[i]=(R(a[i][-1])-sum(R(a[i][j])*x[j] for j in range(i+1,n)))/R(a[i][i])
 require(all(sum(matrix[i][j]*x[j] for j in range(n))==rhs[i] for i in range(n)),'symbolic solve residual')
 return x,minors

def recover(q):
 s=3*q+4;m=(q+2)*(q+3)/2
 ns=[choose(2,u)*choose(q,w) for u,w in ST]
 nq=[choose(2,u)*choose(q,w) for u,w in QT]
 A=[[choose(2-u,z)*choose(q-w,h) for z,h in QT] for u,w in ST]
 E=[[choose(2-z,u)*choose(q-h,w) for u,w in ST] for z,h in QT]
 ds=[sum(row) for row in A];es=[sum(row) for row in E]
 matrix=[];rhs=[]
 for i in range(5):
  row=[R(0)]*9;row[i]=ns[i]*ds[i]
  for j in range(4):row[5+j]=ns[i]*A[i][j]
  matrix.append(row);rhs.append(ns[i]*(m-ds[i]))
 for j in range(4):
  matrix.append([nq[j]*E[j][i] for i in range(5)]+[nq[j]*es[j]*int(j==h) for h in range(4)])
  rhs.append(nq[j]*(s-es[j]))
 require(all(matrix[i][j]==matrix[j][i] for i in range(9) for j in range(9)),'weighted symmetry')
 x,minors=ff_eliminate(matrix,rhs);p=x[:5];r=x[5:]+[R(0)]
 require(all(ds[i]*p[i]+sum(A[i][j]*r[j] for j in range(5))==m-ds[i] for i in range(5)),'all row balances')
 require(all(es[j]*r[j]+sum(E[j][i]*p[i] for i in range(5))==s-es[j] for j in range(5)),'all column balances')
 return p,r,minors

def action(q,j,ell,row,col):
 u,w=row;z,h=col
 return (-1)**(j+ell)*choose(2-u-j,z-j)*choose(q-w-ell,h-ell)

def sector(q,p,r,j,ell):
 s=3*q+4;n=(q*q+11*q+16)/2;m=(q+2)*(q+3)/2
 eligible=lambda a:j<=a[0]<=2-j and ell<=a[1]
 si=[i for i,a in enumerate(ST) if eligible(a)]
 qi=[i for i,a in enumerate(QT) if eligible(a)]
 sl=[ST[i] for i in si];ql=[QT[i] for i in qi]
 ns=[choose(2-2*j,u-j)*choose(q-2*ell,w-ell) for u,w in sl]
 nq=[choose(2-2*j,u-j)*choose(q-2*ell,w-ell) for u,w in ql]
 trivial=j==ell==0
 H=[[((p[i]+r[k]+1)*action(q,j,ell,ST[i],QT[k])-nq[b]*int(trivial)) for b,k in enumerate(qi)] for i in si]
 HT=[[((p[k]+r[i]+1)*action(q,j,ell,QT[i],ST[k])-ns[b]*int(trivial)) for b,k in enumerate(si)] for i in qi]
 require(all(ns[a]*H[a][b]==nq[b]*HT[b][a] for a in range(len(si)) for b in range(len(qi))),'cross adjoint')
 D=[];P=[]
 for a,i in enumerate(qi):
  dr=[];pr=[]
  for b,k in enumerate(qi):
   weight=R(0) if sum(QT[i])==sum(QT[k])==1 else (q-2)/q
   dr.append(s*int(a==b)-nq[b]*int(trivial)+weight*action(q,j,ell,QT[i],QT[k]))
   pr.append(R(int(a==b))-nq[b]*int(trivial)/m)
  D.append(dr);P.append(pr)
 square=[[sum(HT[a][h]*H[h][b] for h in range(len(si))) for b in range(len(qi))] for a in range(len(qi))]
 lower=[[nq[a]*(D[a][b]-P[a][b]/4-square[a][b]/(s-F(1,4))) for b in range(len(qi))] for a in range(len(qi))]
 upper=[[nq[a]*((n-F(1,4))*P[a][b]-D[a][b]-square[a][b]/(n-s-F(1,4))) for b in range(len(qi))] for a in range(len(qi))]
 for name,g in [('D',[[nq[a]*D[a][b] for b in range(len(qi))] for a in range(len(qi))]),('lower',lower),('upper',upper)]:
  require(all(g[a][b]==g[b][a] for a in range(len(qi)) for b in range(len(qi))),name+' symbolic Gram symmetry')
  if trivial:require(all(sum(row)==0 for row in g),name+' trivial constant residual')
 return {'degree':(j,ell),'S_indices':si,'Q_indices':qi,'S_types':sl,'Q_types':ql,'S_norms':ns,'Q_norms':nq,'B_action':H,'BT_action':HT,'D_action':D,'lower':lower,'upper':upper}

def positive_minors(g):
 n=len(g)
 require(n>0 and all(len(row)==n for row in g),'nonsquare Gram form')
 require(all(g[i][j]==g[j][i] for i in range(n) for j in range(n)),'asymmetric Gram form')
 common=(F(1),)
 for row in g:
  for x in row:common=mul(common,exact_divide(x.d,gcd(common,x.d)))
 common=tuple(c/common[-1] for c in common)
 R(common).coefficients_positive()
 scaled=[[R(mul(x.n,exact_divide(common,x.d))) for x in row] for row in g]
 minors=ff_eliminate(scaled)
 records=[]
 for h,minor in enumerate(minors,1):
  minor.coefficients_positive();positive=True
  records.append({'order':h,'numerator':minor.record()['numerator'],'coefficient_positive':positive,'negative_coefficient_count':sum(c<0 for c in minor.n)})
 return {'common_positive_denominator':R(common).record()['numerator'],'minors':records}

def serial(v):
 if isinstance(v,R):return v.record()
 if isinstance(v,dict):return {k:serial(x) for k,x in v.items()}
 if isinstance(v,(list,tuple)):return [serial(x) for x in v]
 return v
