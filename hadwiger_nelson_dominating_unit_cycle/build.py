from fractions import Fraction as F
from itertools import combinations,product
from collections import Counter
from pathlib import Path
import argparse,hashlib,json,math,time
def clean(x):
    return {r:F(v) for r,v in x.items() if v}


def plus(x, y):
    z = dict(x)
    for r,v in y.items():
        z[r] = z.get(r,F(0))+v
    return clean(z)


def neg(x):
    return {r:-v for r,v in x.items()}


def times(x, y):
    z = {}
    for r,a in x.items():
        for s,b in y.items():
            g = math.gcd(r,s)
            t = r*s//(g*g)
            z[t] = z.get(t,F(0))+g*a*b
    return clean(z)


def cadd(z, w):
    return (plus(z[0],w[0]),plus(z[1],w[1]))


def csub(z, w):
    return (plus(z[0],neg(w[0])),plus(z[1],neg(w[1])))


def cmul(z, w):
    return (plus(times(z[0],w[0]),neg(times(z[1],w[1]))),
            plus(times(z[0],w[1]),times(z[1],w[0])))


def squared(z, w):
    a,b = csub(z,w)
    return plus(times(a,a),times(b,b))


def point(a=0,b=0,c=0,d=0):
    return (clean({1:a,3:b}),clean({1:c,3:d}))


def key(z):
    return tuple(tuple(sorted(v.items())) for v in z)


UNIT={1:F(1)}
def ea(a,b):return (a[0]+b[0],a[1]+b[1])
def es(a,b):return (a[0]-b[0],a[1]-b[1])
def em(a,b):return (a[0]*b[0]-a[1]*b[1],a[0]*b[1]+a[1]*b[0]+a[1]*b[1])
def ec(a):return (a[0]+a[1],-a[1])
def en(a):return a[0]**2+a[0]*a[1]+a[1]**2
def cart(a):return ({1:F(2*a[0]+a[1],2)} if 2*a[0]+a[1] else {},{3:F(a[1],2)} if a[1] else {})
Z=(0,0);ONE=(1,0)
U=[ONE,(0,1),(-1,1),(-1,0),(0,-1),(1,-1)]
D=[(Z,Z),(ONE,Z),(Z,ONE),(ONE,ONE)]
forms=sorted({(ea(d[0],u[0]),ea(d[1],u[1])) for d in D for u in [(x,Z) for x in U]+[(Z,x) for x in U]})
def polynomial(f,g,target):
 s,t=es(f[0],g[0]),es(f[1],g[1]);k=em(ec(s),t)
 return (2*k[0]+k[1],-k[1],en(s)+en(t)-target)
def primitive(eq):
 g=math.gcd(*eq)
 if not g:return eq
 eq=tuple(x//g for x in eq)
 if next(x for x in eq if x)<0:eq=tuple(-x for x in eq)
 return eq

BASIS=(1,3,5,15,11,33,55,165)
def encode(z):
 values=[24*axis.get(k,F(0)) for axis in z for k in BASIS]
 if any(x.denominator!=1 for x in values):raise ValueError('denominator24')
 if any(k not in BASIS for axis in z for k in axis):raise ValueError('unexpected radical')
 return [int(x) for x in values]


def generate():
 equations=sorted({primitive(polynomial(f,g,t)) for f,g in combinations(forms,2) for t in (0,1) if polynomial(f,g,t)[:2]!=(0,0)})
 def sqrtint(n):
  if n==0:return {}
  a=1;b=1;p=2
  while p*p<=n:
   e=0
   while n%p==0:n//=p;e+=1
   a*=p**(e//2)
   if e%2:b*=p
   p+=1
  b*=n
  return {b:F(a)}
 parameters={}
 rootcounts=Counter()
 for A,B,C in equations:
  L=A*A+3*B*B;delta=L-C*C
  if delta<0:rootcounts[0]+=1;continue
  values=[]
  for sign in (-1,1):
   x=plus({1:F(-A*C,L)},times({1:F(sign*B,L)},sqrtint(3*delta)))
   y=plus({3:F(-B*C,L)},times({1:F(-sign*A,L)},sqrtint(delta)))
   z=(clean(x),clean(y));parameters[key(z)]=z;values.append(key(z))
  rootcounts[len(set(values))]+=1
 parameters=[parameters[k] for k in sorted(parameters)]

 def solve(V,E,lists):
  adj=[set() for _ in V]
  for i,j in E:adj[i].add(j);adj[j].add(i)
  c={};nodes=[0]
  def dfs():
   nodes[0]+=1
   if len(c)==len(V):return [c[i] for i in range(len(V))]
   v=min((i for i in range(len(V)) if i not in c),key=lambda i:(len(set(lists[i])-{c[j] for j in adj[i] if j in c}),-len(adj[i]),i))
   used={c[j] for j in adj[v] if j in c}
   for k in lists[v]:
    if k in used:continue
    c[v]=k;a=dfs()
    if a is not None:return a
    del c[v]
   return None
  a=dfs()
  return a,nodes[0]
 def serial(z):return [[[k,v.numerator,v.denominator] for k,v in sorted(a.items())] for a in z]
 rows=[]
 for n,beta in enumerate(parameters):
  evaluated=[cadd(cart(s),cmul(cart(t),beta)) for s,t in forms]
  V=[];idx={};aliases=[]
  for z in evaluated:
   if key(z) not in idx:idx[key(z)]=len(V);V.append(z)
   aliases.append(idx[key(z)])
  centres=[idx[key(cadd(cart(s),cmul(cart(t),beta)))] for s,t in D]
  E=[(i,j) for i,j in combinations(range(len(V)),2) if squared(V[i],V[j])==UNIT]
  coincident=len(set(centres))<4
  lists=[]
  for j,v in enumerate(V):
   owners={i for i,d in enumerate(centres) if squared(v,V[d])==UNIT}
   if coincident:allowed=list(range(4))
   elif j in centres:allowed=[(2,3,0,1)[centres.index(j)]]
   elif owners in ({0},{1}):allowed=[0,1]
   elif owners in ({2},{3}):allowed=[2,3]
   else:allowed=list(range(4))
   lists.append(allowed)
  c,nodes=solve(V,E,lists)
  if c is None:print('FAILED',n,serial(beta),len(V),len(E),flush=True)
  if c is None:raise ValueError('exceptional patch unresolved')
  rows.append({'parameter':encode(beta),'aliases':aliases,'edges':len(E),
   'lists':[sum(1<<v for v in allowed) for allowed in lists],
   'colouring':c,'coincident':coincident,'nodes':nodes})

 generic_edges=[(i,j) for i,j in combinations(range(len(forms)),2) if polynomial(forms[i],forms[j],1)==(0,0,0)]
 centres=[forms.index(d) for d in D]
 generic_lists=[]
 for j,f in enumerate(forms):
  owners={i for i,d in enumerate(D) if polynomial(f,d,1)==(0,0,0)}
  if j in centres:allowed=[(2,3,0,1)[centres.index(j)]]
  elif owners in ({0},{1}):allowed=[0,1]
  elif owners in ({2},{3}):allowed=[2,3]
  else:allowed=list(range(4))
  generic_lists.append(allowed)
 gc,gn=solve(forms,generic_edges,generic_lists)
 if gc is None:raise ValueError('generic patch unresolved')
 rho=({1:F(5,6)},{11:F(1,6)})
 root=({},{});tip=({3:F(1)},{})
 a=({3:F(1,2)},{1:F(1,2)});b=({3:F(1,2)},{1:F(-1,2)})
 spindle=[root,tip,a,b,cmul(tip,rho),cmul(a,rho),cmul(b,rho)]
 return {'denominator':24,'forms':[list(s+t) for s,t in forms],
  'equations':[list(e) for e in equations],'root_count_histogram':{str(k):v for k,v in sorted(rootcounts.items())},
  'generic':{'edges':len(generic_edges),'lists':[sum(1<<x for x in L) for L in generic_lists],
             'colouring':gc,'nodes':gn},
  'cases':rows,'sharpness':{'vertices':[encode(z) for z in spindle],
   'colouring':[0,1,2,3,0,2,3],'dominating_cycle':[0,2,1,3]}}

def main():
 p=argparse.ArgumentParser();p.add_argument('--out',required=True);p.add_argument('--discover',action='store_true')
 a=p.parse_args();out=Path(a.out);out.mkdir(parents=True,exist_ok=False);start=time.monotonic()
 data=generate();raw=(json.dumps(data,sort_keys=True,separators=(',',':'))+'\n').encode()
 if not a.discover and raw!=(Path(__file__).parent/'certificate.json').read_bytes():raise ValueError('published certificate mismatch')
 (out/'certificate.json').write_bytes(raw)
 report={'status':'PASS','certificate_bytes':len(raw),'certificate_sha256':hashlib.sha256(raw).hexdigest(),'seconds':time.monotonic()-start,'native_solver_calls':0}
 (out/'build.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,sort_keys=True))
if __name__=='__main__':main()
