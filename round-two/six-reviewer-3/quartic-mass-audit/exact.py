"""six-reviewer-3: small exact operations; credited owned kernels.
New rational cardinal interpolation uses symmetric nodes, not the target's
forward-difference integer interpolation. Fixed determinants are QQ Gaussian.
"""
from fractions import Fraction as F
from math import gcd,lcm
from polys import Poly,cast,need
from certificates import trim,add,mul,scale,divrem

ORDER=('E','r','v','w','B','t')
def degree(p,x):return max((dict(k).get(x,0) for k in p.terms),default=-1)
def key(k):return tuple(dict(k).get(x,0) for x in ORDER)
def primitive(p):
 need(bool(p.terms),'nonzero primitive')
 need(all(z[1]==0 for z in p.terms.values()),'real rational coefficients')
 den=lcm(*(z[0].denominator for z in p.terms.values()))
 nums=[int(z[0]*den) for z in p.terms.values()];content=gcd(*nums)
 lead=p.terms[max(p.terms,key=key)][0]
 if lead<0:content=-content
 q=p*(F(den,content));need(all(z[0].denominator==1 for z in q.terms.values()),'primitive integer result')
 return q
def divide(p,d):
 need(bool(d.terms),'nonzero polynomial divisor');q=cast(0);rem=cast(0);p=cast(p);original=p
 dk=max(d.terms,key=key);dc=d.terms[dk][0];dm=dict(dk)
 while p.terms:
  pk=max(p.terms,key=key);pc=p.terms[pk][0];pm=dict(pk)
  if all(pm.get(x,0)>=n for x,n in dk):
   term=Poly({tuple(sorted((x,n-dm.get(x,0)) for x,n in pm.items() if n-dm.get(x,0))):(pc/dc,0)})
   q+=term;p-=term*d
  else:
   term=Poly({pk:(pc,0)});rem+=term;p-=term
 need(q*d+rem==original,'entire quotient remainder identity')
 return q,rem
def quotient(p,d):
 q,r=divide(p,d);need(r==0 and q*d==p,'whole exact polynomial division');return q
def determinant(m):
 a=[[F(z) for z in row] for row in m];n=len(a);need(all(len(r)==n for r in a),'square fixed matrix');ans=F(1)
 for j in range(n):
  k=next((k for k in range(j,n) if a[k][j]),None)
  if k is None:return F(0)
  if k!=j:a[k],a[j]=a[j],a[k];ans=-ans
  pivot=a[j][j];ans*=pivot
  for i in range(j+1,n):
   ratio=a[i][j]/pivot
   for k in range(j+1,n):a[i][k]-=ratio*a[j][k]
   a[i][j]=0
 return ans
def scalar(p):
 need(not any(k for k in p.terms),'complete scalar');return p.terms.get((),(F(0),F(0)))[0]
def coefficients(p,x):return [scalar(p.coefficient(x,j)) for j in range(degree(p,x)+1)]
def sylvester(p,q,x,m,n):
 need(degree(p,x)<=m and degree(q,x)<=n,'formal fixed degrees')
 a=list(reversed([p.coefficient(x,j) for j in range(m+1)]));b=list(reversed([q.coefficient(x,j) for j in range(n+1)]))
 return [[cast(0)]*j+a+[cast(0)]*(n-1-j) for j in range(n)]+[[cast(0)]*j+b+[cast(0)]*(m-1-j) for j in range(m)]
def evaluate(matrix,mapping):return [[scalar(z.substitute(mapping)) for z in row] for row in matrix]
def lagrange(nodes,values):
 product=[F(1)]
 for x in nodes:product=mul(product,[-F(x),F(1)])
 out=[]
 for x,y in zip(nodes,values):
  basis,rem=divrem(product,[-F(x),F(1)]);need(not rem,'whole cardinal factor')
  den=sum(z*F(x)**j for j,z in enumerate(basis));need(den!=0,'distinct cardinal nodes')
  out=add(out,scale(basis,F(y)/den))
 need(all(sum(c*F(x)**j for j,c in enumerate(out))==y for x,y in zip(nodes,values)),'every cardinal value')
 return out
def mt(a,p):return trim([int(z)%p for z in a])
def ma(a,b,p):return mt(add(a,b),p)
def mm(a,b,p):return mt(mul(a,b),p)
def ms(a,c,p):return mt(scale(a,c),p)
def md(a,b,p):
 a=mt(a,p);b=mt(b,p);need(bool(b),'nonzero finite-field divisor');q=[0]*max(0,len(a)-len(b)+1)
 while a and len(a)>=len(b):
  j=len(a)-len(b);z=a[-1]*pow(b[-1],-1,p)%p;q[j]=z
  for k,c in enumerate(b):a[j+k]=(a[j+k]-z*c)%p
  a=mt(a,p)
 return mt(q,p),a
def unit(a,b,p):
 a=mt(a,p);b=mt(b,p);u,v,uu,vv=[1],[],[],[1]
 while b:
  q,r=md(a,b,p);a,b=b,r;u,uu=uu,ma(u,ms(mm(q,uu,p),-1,p),p);v,vv=vv,ma(v,ms(mm(q,vv,p),-1,p),p)
 need(len(a)==1,'finite-field coprimality');u=ms(u,pow(a[0],-1,p),p);v=ms(v,pow(a[0],-1,p),p)
 return u,v
