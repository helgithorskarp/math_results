"""Exact balancing systems and exhaustive sector actions; see PROOF.md."""
from fractions import Fraction as F
import bootstrap
from symbolic import R,choose,ff_eliminate,serial,require
from poly import mul,gcd,exact_divide
ST=((0,0,0),(0,0,1),(0,1,0),(1,0,0),(1,0,1),(1,1,0),(2,0,0))
QT=((0,0,1),(0,1,0),(1,0,0),(0,0,2),(0,1,1),(1,0,1),(1,1,0),(2,0,0),(2,1,0))

DEGREES=((0,0),(1,0),(0,1),(1,1),(0,2))

def count(q,t):u,d,w=t;return choose(2,u)*choose(1,d)*choose(q-1,w)
def disjoint(q,row,col,j=0,ell=0):
 u,d,w=row;z,e,h=col
 return (-1)**(j+ell)*choose(2-u-j,z-j)*choose(1-d,e)*choose(q-1-w-ell,h-ell)

def recover(q):
 s=3*q+4;m=(q+2)*(q+3)/2+1;a=len(ST);b=len(QT)
 ns=[count(q,t) for t in ST];nq=[count(q,t) for t in QT]
 A=[[disjoint(q,x,y) for y in QT] for x in ST]
 E=[[disjoint(q,x,y) for y in ST] for x in QT]
 ds=[sum(row) for row in A];es=[sum(row) for row in E]
 matrix=[];rhs=[]
 for i in range(a):
  matrix.append([ns[i]*ds[i]*int(h==i) for h in range(a)]+[ns[i]*v for v in A[i][:-1]])
  rhs.append(ns[i]*(m-ds[i]))
 for j in range(b-1):
  matrix.append([nq[j]*v for v in E[j]]+[nq[j]*es[j]*int(h==j) for h in range(b-1)])
  rhs.append(nq[j]*(s-es[j]))
 require(all(matrix[i][j]==matrix[j][i] for i in range(a+b-1) for j in range(a+b-1)),'cross weighted normal symmetry')
 x,cross_minors=ff_eliminate(matrix,rhs);p=x[:a];r=x[a:]+[R(0)]
 require(all(ds[i]*p[i]+sum(A[i][j]*r[j] for j in range(b))==m-ds[i] for i in range(a)),'cross row identities')
 require(all(es[j]*r[j]+sum(E[j][i]*p[i] for i in range(a))==s-es[j] for j in range(b)),'cross column identities')
 internal=[[disjoint(q,x,y) for y in QT] for x in QT]
 degree=[sum(row) for row in internal]
 normal=[[nq[i]*(degree[i]*int(i==j)+internal[i][j]) for j in range(b)] for i in range(b)]
 require(all(normal[i][j]==normal[j][i] for i in range(b) for j in range(b)),'internal weighted normal symmetry')
 d,internal_minors=ff_eliminate(normal,[v*(m-s) for v in nq])
 require(all(degree[i]*d[i]+sum(internal[i][j]*d[j] for j in range(b))==m-s for i in range(b)),'internal row identities')
 return p,r,d,cross_minors,internal_minors

def sector(q,p,r,d,j,ell):
 s=3*q+4;n=(q*q+11*q+18)/2;m=(q+2)*(q+3)/2+1
 valid=lambda t:j<=t[0]<=2-j and ell<=t[2]
 si=[i for i,t in enumerate(ST) if valid(t)];qi=[i for i,t in enumerate(QT) if valid(t)]
 sl=[ST[i] for i in si];ql=[QT[i] for i in qi]
 norm=lambda t:choose(2-2*j,t[0]-j)*choose(q-1-2*ell,t[2]-ell)
 ns=[norm(t) for t in sl];nq=[norm(t) for t in ql];triv=j==ell==0
 H=[[((p[i]+r[k]+1)*disjoint(q,ST[i],QT[k],j,ell)-nq[b]*int(triv)) for b,k in enumerate(qi)] for i in si]
 HT=[[((p[k]+r[i]+1)*disjoint(q,QT[i],ST[k],j,ell)-ns[b]*int(triv)) for b,k in enumerate(si)] for i in qi]
 require(all(ns[a]*H[a][b]==nq[b]*HT[b][a] for a in range(len(si)) for b in range(len(qi))),'cross harmonic adjoint')
 D=[];P=[]
 for a,i in enumerate(qi):
  D.append([s*int(a==b)-nq[b]*int(triv)+(d[i]+d[k])*disjoint(q,QT[i],QT[k],j,ell) for b,k in enumerate(qi)])
  P.append([R(a==b)-nq[b]*int(triv)/m for b in range(len(qi))])
 square=[[sum(HT[a][h]*H[h][b] for h in range(len(si))) for b in range(len(qi))] for a in range(len(qi))]
 lower=[[nq[a]*(D[a][b]-P[a][b]/4-square[a][b]/(s-F(1,4))) for b in range(len(qi))] for a in range(len(qi))]
 upper=[[nq[a]*((n-F(1,4))*P[a][b]-D[a][b]-square[a][b]/(n-s-F(1,4))) for b in range(len(qi))] for a in range(len(qi))]
 for name,g in [('D',[[nq[a]*D[a][b] for b in range(len(qi))] for a in range(len(qi))]),('lower',lower),('upper',upper)]:
  require(all(g[a][b]==g[b][a] for a in range(len(qi)) for b in range(len(qi))),name+' Gram symmetry')
  if triv:require(all(sum(row)==0 for row in g),name+' constant kernel')
 return {'degree':(j,ell),'S_types':sl,'Q_types':ql,'S_norms':ns,'Q_norms':nq,'B_action':H,'BT_action':HT,'D_action':D,'lower':lower,'upper':upper}

def read_r(r):return R(tuple(F(x) for x in r['numerator']),tuple(F(x) for x in r['denominator']))
