#!/usr/bin/env python3
"""Independent recursive-descent parser and rational radical-dictionary geometry."""
import math,re,hashlib,json
from fractions import Fraction as Q
from pathlib import Path
RAD=(1,2,3,6,5,10,15,30)
HASH='a63fa371d7cf42faa8a3b26d56df81b0c25c1f149d6791dd25c7c356abe1b7c6'
def clean(x):return {d:v for d,v in x.items() if v}
def add(a,b):
 out=dict(a)
 for d,v in b.items():out[d]=out.get(d,0)+v
 return clean(out)
def neg(a):return {d:-v for d,v in a.items()}
def mul(a,b):
 out={}
 for d,v in a.items():
  for e,w in b.items():
   g=math.gcd(d,e);k=d*e//(g*g);out[k]=out.get(k,0)+v*w*g
 return clean(out)
def quotient(a,b):
 ds=RAD[:4]
 columns=[mul(b,{d:1})for d in ds]
 mat=[[Q(c.get(d,0))for c in columns]+[Q(a.get(d,0))]for d in ds]
 if set(a)-set(ds)or set(b)-set(ds):raise ValueError('base field')
 for i in range(4):
  pivot=next((j for j in range(i,4)if mat[j][i]),None)
  if pivot is None:raise ValueError('zero denominator')
  mat[i],mat[pivot]=mat[pivot],mat[i];z=mat[i][i];mat[i]=[v/z for v in mat[i]]
  for j in range(4):
   if j!=i:
    z=mat[j][i];mat[j]=[v-z*w for v,w in zip(mat[j],mat[i])]
 return clean({d:mat[i][-1]for i,d in enumerate(ds)})
class Parser:
 def __init__(self,s):
  self.tokens=re.findall(r'Sqrt|[0-9]+|[+*/(),\[\]{}-]',s)
  if ''.join(self.tokens)!=re.sub(r'\s','',s):raise ValueError('invalid token')
  self.i=0
 def pop(self):
  if self.i>=len(self.tokens):raise ValueError('end of expression')
  x=self.tokens[self.i];self.i+=1;return x
 def peek(self):return self.tokens[self.i]if self.i<len(self.tokens)else None
 def factor(self):
  t=self.pop()
  if t in ('+','-'):
   a,b=self.factor();return (neg(a),b)if t=='-'else(a,b)
  if t.isdigit():return ({1:int(t)},{1:1})
  if t=='(':
   out=self.expr()
   if self.pop()!=')':raise ValueError('parenthesis')
   return out
  if t=='Sqrt':
   if self.pop()!='[':raise ValueError('root bracket')
   a,b=self.expr()
   if self.pop()!=']':raise ValueError('root bracket')
   value=quotient(a,b)
   if set(value)-{1}or value.get(1,0)<0:raise ValueError('root argument')
   q=value.get(1,Q(0));z=q.numerator*q.denominator
   for d in RAD[:4]:
    if z%d==0:
     u=math.isqrt(z//d)
     if u*u*d==z:return ({d:Q(u,q.denominator)},{1:1})
   raise ValueError('root outside field')
  raise ValueError('factor')
 def term(self):
  a,b=self.factor()
  while self.peek()in('*','/'):
   t=self.pop();c,d=self.factor()
   if t=='*':a,b=mul(a,c),mul(b,d)
   else:a,b=mul(a,d),mul(b,c)
  return a,b
 def expr(self):
  a,b=self.term()
  while self.peek()in('+','-'):
   t=self.pop();c,d=self.term()
   a,b=add(mul(a,d),mul(c,b)if t=='+'else neg(mul(c,b))),mul(b,d)
  return a,b
 def point(self):
  if self.pop()!='{':raise ValueError('point bracket')
  x=quotient(*self.expr())
  if self.pop()!=',':raise ValueError('comma')
  y=quotient(*self.expr())
  if self.pop()!='}'or self.peek()is not None:raise ValueError('point end')
  return x,y
def key(p):return tuple(Q(c.get(d,0))for c in p for d in RAD)
def unpack(p):return tuple({d:p[s+i]for i,d in enumerate(RAD)if p[s+i]}for s in(0,8))
def rotate(p):
 x,y=p;x=add(x,{1:1});c={1:Q(7,8)};s={15:Q(1,8)}
 return add(add(mul(c,x),neg(mul(s,y))),{1:-1}),add(mul(s,x),mul(c,y))
def construct(path):
 data=Path(path).read_bytes()
 if len(data)!=40529 or hashlib.sha256(data).hexdigest()!=HASH:raise ValueError('input hash')
 hp=[key(Parser(row).point())for row in data.decode().splitlines()]
 if len(hp)!=721 or len(set(hp))!=721:raise ValueError('half count')
 rp=[key(rotate(unpack(p)))for p in hp];allp=sorted(set(hp)|set(rp));den=math.lcm(*(x.denominator for p in allp for x in p))
 if den!=96:raise ValueError('scale')
 points=[tuple(int(x*den)for x in p)for p in allp];ids={p:i for i,p in enumerate(allp)}
 return points,[ids[p]for p in hp],[ids[p]for p in rp]
def edges(points,prime=1009):
 # Three checked square roots define a necessary ring homomorphism.
 roots={d:next(r for r in range(prime)if r*r%prime==d)for d in(2,3,5)}
 images=[]
 for d in RAD:
  r=1
  for p,z in roots.items():
   if d%p==0:r=r*z%prime
  images.append(r)
 projected=[tuple(sum(p[s+i]*images[i]for i in range(8))%prime for s in(0,8))for p in points]
 es=[];survivors=0
 for u,(x,y)in enumerate(projected):
  for v in range(u):
   xx,yy=projected[v]
   if ((x-xx)**2+(y-yy)**2-96*96)%prime:continue
   survivors+=1;norm={}
   for s in(0,8):
    d=clean({rad:points[u][s+i]-points[v][s+i]for i,rad in enumerate(RAD)})
    norm=add(norm,mul(d,d))
   if norm=={1:96*96}:es.append((v,u))
 return sorted(es),survivors
