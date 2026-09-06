"""Exact finite audits for the written parallel-line full-support theorems."""
from fractions import Fraction as F
from functools import cmp_to_key,lru_cache
from itertools import combinations,product
from math import gcd,isqrt
from pathlib import Path
import argparse,hashlib,json,time

def need(ok,msg):
 if not ok:raise ValueError(msg)
def clean(a):return {d:c for d,c in a.items() if c}
def add(a,b):
 c=a.copy()
 for d,x in b.items():c[d]=c.get(d,F(0))+x
 return clean(c)
def scale(a,t):return clean({d:c*t for d,c in a.items()})
def sub(a,b):return add(a,scale(b,-1))
def root(q):
 q=F(q);need(q>=0,'nonnegative radicand')
 if not q:return {}
 n=q.numerator*q.denominator;outside=1;d=2
 while d*d<=n:
  while n%(d*d)==0:n//=d*d;outside*=d
  d+=1
 return {n:F(outside,q.denominator)}
def enc(a):return [[d,[c.numerator,c.denominator]] for d,c in sorted(a.items())]
def dec(a):return {d:F(*v) for d,v in a}
def key(a):return tuple(sorted(a.items()))
@lru_cache(None)
def signkey(a):
 if not a:return 0
 bits=4
 while True:
  lo=hi=F(0);s=1<<bits
  for d,c in a:
   t=isqrt(d*s*s);l=F(t,s);u=l if t*t==d*s*s else F(t+1,s)
   lo+=c*(l if c>0 else u);hi+=c*(u if c>0 else l)
  if lo>0:return 1
  if hi<0:return -1
  bits*=2
def sign(a):return signkey(key(a))
def raw(x):return (json.dumps(x,sort_keys=True,separators=(',',':'))+'\n').encode()
def digest(x):return hashlib.sha256(raw(x)).hexdigest()
def integer(x):need(x.denominator==1,'integer colour coordinate');return x.numerator

def fixture(name,d2,gens,bounds,rows,method,**extra):
 return dict(name=name,spacing_squared=[F(d2).numerator,F(d2).denominator],generators=[enc(g) for g in gens],bounds=bounds,rows=rows,method=method,**extra)
def fixtures():
 one={1:F(1)}
 return [
 fixture('comb_two_shifts',F(3,4),[{1:F(1,2)}],[[-4,4]],list(range(-2,3)),'projection'),
 fixture('comb_three_shifts_rational_relation',F(4,25),[{1:F(1,5)},root(F(21,25))],[[-8,8],[-1,1]],list(range(-2,3)),'projection'),
 fixture('comb_three_independent_shifts',F(9,64),[one,root(F(55,64)),root(F(7,16))],[[-1,1]]*3,list(range(-1,3)),'projection'),
 fixture('comb_middle_interval_triangle',F(3,16),[{1:F(1,2)},root(F(13,16))],[[-3,3],[-1,1]],list(range(-2,3)),'projection'),
 fixture('third_spacing_bipartite',F(1,9),[one,root(F(8,9)),root(F(5,9))],[[-1,1]]*3,list(range(-3,4)),'third'),
 fixture('half_spacing_three_colours',F(1,4),[one,root(F(3,4))],[[-1,1]]*2,list(range(-2,3)),'half'),
 fixture('unit_spacing_grid',1,[one],[[-2,2]],list(range(-2,3)),'one'),
 fixture('separated_lines',4,[one],[[-3,3]],list(range(-2,3)),'projection'),
 fixture('irrational_two_colour_case',F(1,2),[one,root(F(1,2))],[[-1,1]]*2,list(range(-2,3)),'irrational_two'),
 fixture('rational_two_colour_even_numerator',F(5,9),[{1:F(1,3)}],[[-5,5]],list(range(-2,3)),'rational_two',p=2,q=3),
 fixture('rational_two_colour_odd_numerator',F(8,9),[{1:F(1,3)}],[[-5,5]],list(range(-2,3)),'rational_two',p=1,q=3),
 fixture('three_irregular_lines_with_vertical_edges',1,[{1:F(1,5)},root(F(21,25))],[[-5,5],[-1,1]],[0,1,2],'three_lines',heights=[[0,1],[3,5],[1,1]])]

def geometry(spec):
 xs={}
 for vals in product(*(range(a,b+1) for a,b in spec['bounds'])):
  x={}
  for v,g in zip(vals,spec['generators']):x=add(x,scale(dec(g),v))
  xs[key(x)]=x
 X=[xs[k] for k in sorted(xs)];rows=spec['rows'];d2=F(*spec['spacing_squared'])
 Y=[{1:F(*h)} if F(*h) else {} for h in spec['heights']] if 'heights' in spec else [scale(root(d2),j) for j in rows]
 V=[(x,y) for x in X for y in Y];E=[]
 for a,b in combinations(range(len(V)),2):
  ra,rb=a%len(rows),b%len(rows)
  q=(F(*spec['heights'][ra])-F(*spec['heights'][rb]))**2 if 'heights' in spec else d2*(rows[ra]-rows[rb])**2
  if q>1:continue
  w=root(1-q);dx=sub(V[a][0],V[b][0])
  if dx==w or dx==scale(w,-1):E.append((a,b))
 return X,Y,V,E

def colour(spec,X,Y,V,E):
 method=spec['method'];rows=spec['rows'];count=len(rows)
 if method in ('projection','three_lines'):
  if method=='projection':
   d2=F(*spec['spacing_squared']);D=[{1:F(1)}];k=1
   while k*k*d2<=1:
    need(k*k*d2!=1,'projection must not collapse vertical unit edges');D.append(root(1-k*k*d2));k+=1
   need(len(D)<=3,'at most three horizontal shifts')
   EE=[(a,b) for a,b in combinations(range(len(X)),2) if any(sub(X[a],X[b])==d or sub(X[a],X[b])==scale(d,-1) for d in D)]
   order=sorted(range(len(X)),key=cmp_to_key(lambda a,b:sign(sub(X[a],X[b]))));n=len(X);bound=len(D)
  else:
   EE=E;order=sorted(range(len(V)),key=cmp_to_key(lambda a,b:sign(sub(V[a][0],V[b][0])) or sign(sub(V[a][1],V[b][1]))));n=len(V);bound=3
  adj=[set() for _ in range(n)]
  for a,b in EE:adj[a].add(b);adj[b].add(a)
  col=[-1]*n;maximum=0
  for v in order:
   seen={col[u] for u in adj[v] if col[u]>=0};maximum=max(maximum,sum(col[u]>=0 for u in adj[v]));need(len(seen)<=bound,'directional predecessor bound')
   col[v]=next(c for c in range(bound+1) if c not in seen)
  return [col[a//count] for a in range(len(V))] if method=='projection' else col,maximum
 colours=[]
 for x,y in V:
  j=rows[len(colours)%count];m=integer(x.get(1,F(0))) if method!='rational_two' else None
  if method=='third':c=(m+integer(3*x.get(5,F(0)))+j)%2
  elif method=='half':c=(m+j)%3
  elif method in ('one','irrational_two'):c=(m+j)%2
  elif method=='rational_two':c=(integer(spec['q']*x.get(1,F(0)))+(1-spec['p'])*j)%2
  else:raise ValueError('unknown method')
  colours.append(c)
 return colours,None

def build():
 cases=[]
 for spec in fixtures():
  X,Y,V,E=geometry(spec);col,maximum=colour(spec,X,Y,V,E);need(all(col[a]!=col[b] for a,b in E),'positive edge check')
  cases.append(dict(input=spec,vertices=len(V),edges=len(E),colouring=''.join(map(str,col)),predecessor_maximum=maximum,point_sha256=digest([[enc(x),enc(y)] for x,y in V]),edge_sha256=digest(E)))
 odd=[[p,q] for q in range(2,21,2) for p in range(1,q) if gcd(p,q)==1 and 4*p*p<3*q*q]
 return {'schema':1,'claim':'written full-support theorem; finite audits only','cases':cases,'odd_cycle_parameters':odd,'target_found':False}

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--out',required=True);ap.add_argument('--discover',action='store_true');args=ap.parse_args();out=Path(args.out);out.mkdir(parents=True,exist_ok=False);start=time.monotonic();data=build();blob=raw(data)
 if not args.discover:need(blob==(Path(__file__).parent/'certificate.json').read_bytes(),'certificate replay')
 (out/'certificate.json').write_bytes(blob)
 report={'status':'PASS','fixture_count':len(data['cases']),'vertices':sum(c['vertices'] for c in data['cases']),'edges':sum(c['edges'] for c in data['cases']),'odd_cycle_fixtures':len(data['odd_cycle_parameters']),'certificate_bytes':len(blob),'certificate_sha256':hashlib.sha256(blob).hexdigest(),'seconds':time.monotonic()-start}
 (out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
if __name__=='__main__':main()
