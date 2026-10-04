"""Independent physical set-count engine, by six-reviewer-5.
Only the defining TABLE and set recipe are credited from our earlier10190 literal
binding. New endpoint energies/dual norms/finite reading are implemented here.
No new target program, expected record or control is imported.
"""
from fractions import Fraction as F
from math import comb
from itertools import combinations

def need(x,m):
 if not x:raise ValueError(m)

def choose(x,r):
 if r==0:return x*0+1
 if r==1:return x
 if r==2:return x*(x-1)/2
 raise ValueError('carrier outside-size')

def table(q):
 s=3*q+4;h=1/(3*q+5);z=q*0
 o,p,a,b,c,d,e=(0,1),(0,2),(1,0),(1,1),(2,0),(2,1),(3,0);T={}
 def put(x,y,v,w=z):T[tuple(sorted((x,y)))]=(v,w)
 put(o,o,(6/q-q-4)/(q-1),1/(q-1));put(o,p,q*(q-3)/((q-1)*(q-2)))
 den=(q-2)*(q-3)/2
 put(p,p,(6/q+2*q/(q-1)-s+q*(q-1)/2)/den,(1-6*h*(q+1)/(q*(q-1)))/den)
 for leaf,vals in ((o,((1-1/q,z),(1+1/q,z),(1+6/q,z))),
                   (p,((1,2*h/(q*(q-1))),(1+2*(q-1)/(q*(q-2)),2*h/((q-1)*(q-2))),(1+6/q,-6*h*(q+1)/(q*(q-1)))))):
  for core,i in ((a,0),(c,0),(b,1),(d,1),(e,2)):put(leaf,core,*vals[i])
 rr=3+2/q;ww=(s-rr)/(q-1)
 for x,y,v in ((a,a,z),(a,b,z),(b,b,z),(a,c,2),(a,d,rr),(b,c,rr),(b,d,ww)):put(x,y,v)
 return T

KEYS=sorted((c,z,w) for c in range(8) for z in range(3) for w in range(3)
 if (1<=c.bit_count()+z+w<=2 or c.bit_count()+z+w==3 and c.bit_count()>=2) and (c,z,w)!=(6,1,0))
need(len(KEYS)==23,'complete split physical types')

def forms(q,k):
 zero=q*0;N=(q*q+13*q+16)/2-k;s=3*q+4;T=table(q)
 m=[choose(k,z)*choose(q-k,w) for c,z,w in KEYS]
 out=[[[zero for _ in KEYS] for _ in KEYS] for _ in range(6)]
 for i,(c,z,w) in enumerate(KEYS):
  for j,(d,zz,ww) in enumerate(KEYS):
   count=zero if c&d else choose(k-z,zz)*choose(q-k-w,ww)
   base,slope=T[tuple(sorted(((c.bit_count(),z+w),(d.bit_count(),zz+ww))))] if count else (zero,zero)
   out[0][i][j]=(s*m[i] if i==j else zero)-m[i]*m[j]+m[i]*count*base
   out[1][i][j]=m[i]*count*slope
   out[2][i][j]=(N*m[i] if i==j else zero)-m[i]*m[j]-out[0][i][j]
 def edge(a,b,num,A):
  i,j=KEYS.index(a),KEYS.index(b);A[i][j]+=num;A[j][i]+=num
 for a,b,v,idx in [((1,0,0),(2,0,0),1,3),((2,0,0),(5,0,0),-1,3),((1,0,0),(4,0,0),1,4),((4,0,0),(3,0,0),-1,4),((2,0,0),(4,0,0),1,5)]:edge(a,b,v,out[idx])
 need(sum(m,zero)==N-1,'complete physical cardinality')
 need(all(A[i][j]==A[j][i] for A in out for i in range(23) for j in range(23)),'all original symmetry equations')
 return N,m,out

def energy(A,x):return sum((x[i]*A[i][j]*x[j] for i in range(23) for j in range(23)),A[0][0]*0)
def plane(out,x,cap=False):
 e=[energy(A,x) for A in out];return [e[2],-e[1],-e[3],-e[4],-e[5]] if cap else [e[0],e[1],e[3],e[4],e[5]]
def beta(N,m,x):return sum((a*b*b for a,b in zip(m,x)),N*0)-sum((a*b for a,b in zip(m,x)),N*0)**2/N

def constant_vectors():
 y=[];v=[];zeta=[]
 for c,z,w in KEYS:
  r=z+w;y.append(F(1,2) if (c==1 and r==1 or c==7) else F(1) if c in (2,4) and r==0 else F(3,4) if c in (2,4) and r==1 else F(-1,4) if c in (3,5) and r==1 else F(0))
  v.append(F(1) if c in (2,4) and r==0 else F(2));zeta.append(F(1) if c==0 else F(-1) if c==7 else F(0))
 return y,v,zeta

def literal(q,k):
 """Full original members, unaggregated ordered pair rows; all six forms."""
 X=[sum(1<<i for i in S) for r in (1,2,3) for S in combinations(range(q+3),r)
    if (r<=2 or sum(i<3 for i in S)>=2) and not(r==3 and S[:2]==(1,2) and S[2]<k+3)]
 N,m,fast=forms(F(q),F(k));T=table(F(q));Z=((1<<k)-1)<<3
 bins=[KEYS.index((A&7,(A&Z).bit_count(),(A&~(Z|7)).bit_count())) for A in X]
 mass=[F(bins.count(i)) for i in range(23)];slow=[[[F(0) for _ in KEYS] for _ in KEYS] for _ in range(6)]
 need(len(X)==N-1 and mass==m,'every physical zero/positive orbit mass')
 for ai,A in enumerate(X):
  i=bins[ai]
  for bj,B in enumerate(X):
   j=bins[bj]
   if A==B:a,b=F(3*q+3),F(0)
   elif A&B:a,b=F(-1),F(0)
   else:
    a,b=T[tuple(sorted((((A&7).bit_count(),(A>>3).bit_count()),((B&7).bit_count(),(B>>3).bit_count()))))];a-=1
   slow[0][i][j]+=a;slow[1][i][j]+=b;slow[2][i][j]+=N*int(ai==bj)-1-a
   for name,edges in ((3,{(1,2):1,(2,5):-1}),(4,{(1,4):1,(3,4):-1}),(5,{(2,4):1})):
    if A>>3==B>>3==0:slow[name][i][j]+=edges.get(tuple(sorted((A,B))),0)
 need(slow==fast,'entire6 physical coefficient forms literal/count match')
 return {'q':q,'k':k,'N':int(N),'ordered_pairs':len(X)**2,'all6_entries':6*23**2,'empty_physical_orbits':sum(x==0 for x in m)}
