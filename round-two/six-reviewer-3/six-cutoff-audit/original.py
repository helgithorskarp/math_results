"""Independent actual-set integer reconstruction, never imports author code."""
from itertools import combinations
from fractions import Fraction as F
from math import lcm
from exact import need

def members(q,k):
 need(type(q)is int and type(k)is int and 4<=q<=18 and 0<=k<=q,'bounded original domain')
 # Construct by levels and filter explicit labels, rather than author domain.
 sets=[0]
 for size in (1,2,3):
  for pts in combinations(range(q+3),size):
   mask=sum(1<<i for i in pts)
   if size==3 and (mask&7).bit_count()<2:continue
   if mask&7==6 and mask>>3 and (mask>>3).bit_length()<=k:continue
   sets.append(mask)
 return sets

def table(q):
 # Defining credited affine weight table, expanded anew, coefficients Q0,Q1.
 q=F(q);s=3*q+4;h=1/(3*q+5);T={}
 def put(x,y,a,b=0):T[tuple(sorted((x,y)))]=(F(a),F(b))
 o,p,a,b,c,d,e=(0,1),(0,2),(1,0),(1,1),(2,0),(2,1),(3,0)
 put(o,o,(6/q-q-4)/(q-1),1/(q-1));put(o,p,q*(q-3)/((q-1)*(q-2)))
 put(p,p,(6/q+2*q/(q-1)-s+q*(q-1)/2)*2/((q-2)*(q-3)),(1-6*h*(q+1)/(q*(q-1)))*2/((q-2)*(q-3)))
 for leaf,A,B,E in [(o,(1-1/q,0),(1+1/q,0),(1+6/q,0)),(p,(1,2*h/(q*(q-1))),(1+2*(q-1)/(q*(q-2)),2*h/((q-1)*(q-2))),(1+6/q,-6*h*(q+1)/(q*(q-1))))]:
  for typ,v in [(a,A),(c,A),(b,B),(d,B),(e,E)]:put(leaf,typ,*v)
 rr=3+2/q
 for x,y,v in [(a,a,0),(a,b,0),(b,b,0),(a,c,2),(a,d,rr),(b,c,rr),(b,d,(s-rr)/(q-1))]:put(x,y,v)
 need(len(T)==20,'all twenty defining unordered disjoint types')
 return T

def build(q,k):
 X=members(q,k);N=len(X);s=3*q+4;n=N-1
 need(N==(q*q+13*q+16)//2-k,'whole original cardinality')
 T=table(q);den=lcm(*(v.denominator for pair in T.values() for v in pair))
 tab={key:((a-1)*den,b*den) for key,(a,b) in T.items()}
 need(all(a.denominator==b.denominator==1 for a,b in tab.values()),'integer coefficient scale')
 tab={key:(int(a),int(b)) for key,(a,b) in tab.items()}
 A=X[1:];types=[((v&7).bit_count(),(v>>3).bit_count()) for v in A]
 C=[];D=[]
 for i,v in enumerate(A):
  row=[];slope=[]
  for j,w in enumerate(A):
   if i==j:a,b=(s-1)*den,0
   elif v&w:a,b=-den,0
   else:a,b=tab[tuple(sorted((types[i],types[j])))]
   row.append(a);slope.append(b)
  C.append(row);D.append(slope)
 ix={v:i for i,v in enumerate(A)}
 groups={};keys=[]
 for i,v in enumerate(A):
  z=((v>>3)&((1<<k)-1)).bit_count();key=(v&7,z,(v>>3).bit_count()-z)
  if key not in groups:groups[key]=len(keys);keys.append(key)
 g=[groups[(v&7,((v>>3)&((1<<k)-1)).bit_count(),(v>>3).bit_count()-((v>>3)&((1<<k)-1)).bit_count())] for v in A]
 weights=[g.count(i) for i in range(len(keys))]
 need(all(w>0 for w in weights),'drop every nonexistent orbit')
 return {'q':q,'k':k,'X':X,'N':N,'s':s,'den':den,'C':C,'D':D,'ix':ix,'keys':keys,'g':g,'weights':weights}

def vectors(data):
 q=data['q'];A=data['X'][1:];ix=data['ix'];n=len(A)
 one=[1]*n;y=[int(v&7==1 and (v>>3).bit_count()==1) for v in A]
 star=[[int(bool(v&(1<<i))) for v in A] for i in range(3)]
 triangle=[int((v&7).bit_count()>=2) for v in A]
 z=[1-b-c+t for b,c,t in zip(star[1],star[2],triangle)]
 h=[int(v in (2,4)) for v in A];gg=[int(v in (3,5)) for v in A]
 u2=[b+c-2*t for b,c,t in zip(star[1],star[2],triangle)]
 ds=[[a-b+c for a,b,c in zip(u2,h,gg)],[int(v==1)+int(v in (3,5)) for v in A],[int(v==6) for v in A],[int(v==7) for v in A],y]
 vc=[int(bool(v&6) and v not in (3,5)) for v in A]
 return one,y,star,triangle,z,h,ds,vc

def pairing(matrix,v,w,den=1):
 vd=lcm(*(F(x).denominator for x in v));wd=lcm(*(F(x).denominator for x in w))
 vi=[int(F(x)*vd) for x in v];wi=[int(F(x)*wd) for x in w]
 return F(sum(vi[i]*sum(a*b for a,b in zip(row,wi)) for i,row in enumerate(matrix)),den*vd*wd)

def edge(v,w,which):
 edges={'Rb':[(1,2,1),(2,5,-1)],'Rc':[(1,4,1),(4,3,-1)],'B':[(2,4,1)]}[which]
 return sum(c*(v[a]*w[b]+v[b]*w[a]) for a,b,c in edges)

def core_amplitudes(data,v):return {a:v[data['ix'][a]] for a in range(1,8)}

def compression(matrix,data,den=1):
 m=len(data['keys']);out=[[0]*m for _ in range(m)];g=data['g']
 for i,row in enumerate(matrix):
  for j,a in enumerate(row):out[g[i]][g[j]]+=a
 return [[F(a,den) for a in row] for row in out]

def psd(A):
 """Exact diagonal pivoted congruence; full zero row is necessary at zero pivot."""
 A=[list(map(F,row)) for row in A];n=len(A);order=list(range(n));piv=[]
 need(all(A[i][j]==A[j][i] for i in range(n) for j in range(n)),'symmetric exact PSD input')
 for k in range(n):
  need(all(A[i][i]>=0 for i in range(k,n)),'nonnegative diagonal in every congruence remainder')
  candidate=next((i for i in range(k,n) if A[i][i]>0),None)
  if candidate is None:
   need(all(A[i][j]==0 for i in range(k,n) for j in range(k,n)),'zero remainder must be entirely zero');break
  if candidate!=k:
   A[k],A[candidate]=A[candidate],A[k]
   for row in A:row[k],row[candidate]=row[candidate],row[k]
   order[k],order[candidate]=order[candidate],order[k]
  d=A[k][k];piv.append(d)
  for i in range(k+1,n):
   for j in range(i,n):A[i][j]=A[j][i]=A[i][j]-A[i][k]*A[k][j]/d
 return {'rank':len(piv),'pivots':list(map(str,piv)),'order':order}
