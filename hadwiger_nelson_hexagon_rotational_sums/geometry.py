import collections,itertools,json,math
from fractions import Fraction as F

def dump(p,x):p.write_text(json.dumps(x,sort_keys=True,indent=2)+'\n')
def H(r=2):return [(a,b) for a in range(-r,r+1) for b in range(-r,r+1) if max(abs(a),abs(b),abs(a+b))<=r]
def norm(v):a,b=v;return a*a+a*b+b*b

def sf(n):
 f=1;s=n;k=2
 while k*k<=s:
  while s%(k*k)==0:f*=k;s//=k*k
  k+=1
 return f,s

def normal(s,x0,x1,y0,y1):
 if s in (0,1):x0+=x1*(s==1);y0+=y1*(s==1);x1=y1=F(0);s=0
 if x1==y1==0:s=0
 return s,F(x0),F(x1),F(y0),F(y1)
def rot(k):
 s,a,b,c,d=k;return normal(s,(a-3*c)/2,(b-3*d)/2,(a+c)/2,(b+d)/2)
def conj(k):s,a,b,c,d=k;return s,a,b,-c,-d
def canon(k):
 out=[]
 for i in range(6):out.extend((k,conj(k)));k=rot(k)
 return min(out)
def scale(k):
 L=math.lcm(*(x.denominator for x in k[1:]));return (k[0],*(int(x*L) for x in k[1:]),L)
def keyjson(k):return list(scale(k))
def catalog(ds):
 keys=set();events=collections.Counter()
 for d in ds:
  if d==(0,0):continue
  a,b=d;m=norm(d)
  for e in ds:
   if e==(0,0):continue
   A,B=e;n=norm(e);p=2*a*A+a*B+b*A+2*b*B;q=b*A-a*B;c=1-m-n;T=4*m*n-c*c
   if T>=0:
    f,s=sf(3*T) if T else (0,0)
    for sig in (-1,1):
     k=normal(s,F(p*c,4*m*n),F(-sig*q*f,4*m*n),F(q*c,4*m*n),F(sig*p*f,12*m*n));keys.add(canon(k));events['unit_roots_with_multiplicity']+=1
   if m==n:
    keys.add(canon(normal(0,F(-p,2*n),0,F(-q,2*n),0)));events['collision_roots_with_multiplicity']+=1
 return sorted(keys),dict(events)
def displacement(d,e,K):
 s,A,B,C,D,L=K;p,q=2*d[0]+d[1],d[1];r,t=2*e[0]+e[1],e[1]
 return p*L+r*A-3*t*C,r*B-3*t*D,q*L+t*A+r*C,t*B+r*D

def graph(h,ds,k):
 K=scale(k);s,A,B,C,D,L=K
 types={}
 for d in ds:
  for e in ds:
   x,z,y,w=displacement(d,e,K);r=x*x+s*z*z+3*y*y+3*s*w*w;t=2*x*z+6*y*w
   if r==t==0:types[d,e]=0
   elif r==4*L*L and t==0:types[d,e]=1
 coords=[displacement(v,w,K) for v in h for w in h]
 # D=0 has identically zero radical coefficients by canonical representation.
 positions=sorted(set(coords));ix={v:i for i,v in enumerate(positions)};labels=[ix[v] for v in coords]
 edges=set();N=len(h)
 for i,(a,b) in enumerate(itertools.product(h,repeat=2)):
  for j in range(i):
   c,d=h[j//N],h[j%N];da=(a[0]-c[0],a[1]-c[1]);db=(b[0]-d[0],b[1]-d[1]);tp=types.get((da,db),-1)
   if (labels[i]==labels[j]) != (tp==0):raise ValueError('collision mismatch')
   if tp==1:edges.add(tuple(sorted((labels[i],labels[j]))))
 return positions,sorted(edges),labels
