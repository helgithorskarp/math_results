"""Separate integer-scaled original-member decoder; no orbit count formula."""
from fractions import Fraction as F
from itertools import combinations
from exact import need

def table(q,x,y):
 # Closed integer-rational expressions, independently simplified from8757.
 s=3*q+4
 if x>y:x,y=y,x
 if x[0]==y[0]==0:
  if x==y==(0,1):return F(6-q*(q+4),q*(q-1)),F(1,q-1)
  if x!=y:return F(q*(q-3),(q-1)*(q-2)),F(0)
  return F(12*(q-1)+4*q*q-2*s*q*(q-1)+q*q*(q-1)**2,q*(q-1)*(q-2)*(q-3)),F(2*(q*(q-1)*(3*q+5)-6*(q+1)),q*(q-1)*(q-2)*(q-3)*(3*q+5))
 if x[0]==0:
  if y==(3,0):return F(q+6,q),F(0)if x[1]==1 else F(-6*(q+1),q*(q-1)*(3*q+5))
  if x[1]==1:return (F(q+1,q)if y[1]else F(q-1,q)),F(0)
  return (F(q*q-2,q*(q-2)),F(2,(q-1)*(q-2)*(3*q+5)))if y[1]else(F(1),F(2,q*(q-1)*(3*q+5)))
 if x==(1,0)and y==(2,0):return F(2),F(0)
 if (x,y)in [((1,0),(2,1)),((1,1),(2,0))]:return F(3*q+2,q),F(0)
 if x==(1,1)and y==(2,1):return F(3*q*q+q-2,q*(q-1)),F(0)
 need((x,y)in [((1,0),(1,0)),((1,0),(1,1)),((1,1),(1,1))],'literal complete feasible type');return F(0),F(0)
def rebuild(q):
 deleted=((1<<7)-1)<<3;members=[]
 for size in (1,2,3):
  for a in combinations(range(q+3),size):
   mask=sum(1<<i for i in a);c=mask&7
   if size==3 and(c.bit_count()<2 or(c==6 and mask&deleted)):continue
   members.append(mask)
 members.sort();key=lambda a:(a&7,(a&deleted).bit_count(),(a&~(deleted|7)).bit_count());kk=sorted(set(map(key,members)));d=len(kk);index={k:i for i,k in enumerate(kk)};ix=[index[key(a)]for a in members];types=[((a&7).bit_count(),(a&~7).bit_count())for a in members];N=(q*q+13*q+16)//2-7;s=3*q+4;den=q*(q-1)*(q-2)*(q-3)*(3*q+5)
 need(len(members)==N-1,'literal entire domain');need(len(set(members))==N-1,'distinct members')
 W=[0]*d
 for i in ix:W[i]+=1
 scaled={}
 for a,b in combinations(members,2):
  if not a&b:
   x=((a&7).bit_count(),(a&~7).bit_count());y=((b&7).bit_count(),(b&~7).bit_count());t=tuple(sorted((x,y)))
   if t not in scaled:
    v=table(q,*t);need(all((z*den).denominator==1 for z in v),'integer clearing');scaled[t]=tuple(int(z*den)for z in v)
 forms=[[[0]*d for _ in range(d)]for _ in range(5)];row0=[];row1=[];norm=[];stars=[bool(a&1)for a in members]
 repair={}
 for a,b,t,value in [(1,2,2,1),(2,5,2,-1),(1,4,3,1),(4,3,3,-1),(2,4,4,1)]:repair[a,b]=repair[b,a]=(t,value)
 pairs=0
 for r,a in enumerate(members):
  i=ix[r];x=types[r];u=v=star0=star1=absolute=0
  for t,b in enumerate(members):
   pairs+=1;j=ix[t];p=(s if a==b else 0)*den-den;delta=0
   if not a&b:
    p0,delta=scaled[tuple(sorted((x,types[t])))];p+=p0
   forms[0][i][j]+=p;forms[1][i][j]+=delta;u+=p;v+=delta;star0+=p*stars[t];star1+=delta*stars[t];absolute+=abs(delta)
   if (a,b)in repair:k,value=repair[a,b];forms[k][i][j]+=value*den
  need(star0==0 and star1==0,'literal forced star EVERY row');row0.append(u);row1.append(v);norm.append(absolute)
 forms=[[[F(z,den)for z in r]for r in a]for a in forms]
 U=[[F(N*W[i]if i==j else 0)-W[i]*W[j]-forms[0][i][j]for j in range(d)]for i in range(d)]
 return dict(q=q,N=N,s=s,keys=kk,weights=W,forms=forms+[U],pairs=pairs,row0=row0,row1=row1,denominator=den,delta_absolute_row_norm=F(max(norm),den),members=members)
