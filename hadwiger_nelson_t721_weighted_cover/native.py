#!/usr/bin/env python3
"""Producer geometry: restricted AST, conjugate inverses, dense XOR products."""
import ast,hashlib,json,math,re
from fractions import Fraction as F
from pathlib import Path
from functools import reduce
D=(1,2,3,6,5,10,15,30)
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def neg(a):return tuple(-x for x in a)
def mul(a,b):
 out=[F(0)]*8
 for i,x in enumerate(a):
  if x:
   for j,y in enumerate(b):
    if y:out[i^j]+=x*y*D[i&j]
 return tuple(out)
def scalar(x):return (F(x),)+(F(0),)*7
def inv(a):
 prod=scalar(1)
 for signs in range(1,8):
  conj=tuple((-1 if (i&signs).bit_count()%2 else 1)*x for i,x in enumerate(a));prod=mul(prod,conj)
 norm=mul(a,prod)
 if any(norm[1:]) or not norm[0]:raise ValueError('denominator')
 return tuple(x/norm[0] for x in prod)
def parse(text):
 def visit(n):
  if isinstance(n,ast.Constant) and type(n.value)is int:return scalar(n.value)
  if isinstance(n,ast.UnaryOp) and isinstance(n.op,(ast.USub,ast.UAdd)):
   a=visit(n.operand);return neg(a) if isinstance(n.op,ast.USub) else a
  if isinstance(n,ast.BinOp):
   a,b=visit(n.left),visit(n.right)
   if isinstance(n.op,ast.Add):return add(a,b)
   if isinstance(n.op,ast.Sub):return add(a,neg(b))
   if isinstance(n.op,ast.Mult):return mul(a,b)
   if isinstance(n.op,ast.Div):return mul(a,inv(b))
  if isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id=='Sqrt' and len(n.args)==1:
   a=visit(n.args[0])
   if any(a[1:]) or a[0]<0:raise ValueError('root argument')
   for i,d in enumerate(D):
    x=a[0]/d;p,q=math.isqrt(x.numerator),math.isqrt(x.denominator)
    if p*p==x.numerator and q*q==x.denominator:
     v=[F(0)]*8;v[i]=F(p,q);return tuple(v)
  raise ValueError(ast.dump(n))
 return visit(ast.parse(text.replace('[','(').replace(']',')'),mode='eval').body)
def half(path):
 rows=Path(path).read_text().splitlines();pts=[]
 for row in rows:
  x,y=row.strip()[1:-1].split(',');pts.append(parse(x.strip())+parse(y.strip()))
 if len(pts)!=721 or len(set(pts))!=721:raise ValueError('count')
 return pts
def transform(p):
 x=add(p[:8],scalar(1));y=p[8:];r=scalar(F(7,8));s=[F(0)]*8;s[6]=F(1,8);s=tuple(s)
 return add(add(mul(x,r),neg(mul(y,s))),scalar(-1))+add(mul(x,s),mul(y,r))
def edges(pts,scale):
 out=[];surv=0
 for u,a in enumerate(pts):
  for v in range(u):
   delta=[a[i]-pts[v][i] for i in range(16)]
   if sum(D[i%8]*z*z for i,z in enumerate(delta))!=scale*scale:continue
   surv+=1;norm=[0]*8
   for start in (0,8):
    for i in range(8):
     for j in range(i+1,8):norm[i^j]+=2*delta[start+i]*delta[start+j]*D[i&j]
   if not any(norm):out.append((v,u))
 return sorted(out),surv
def build(path):
 hp=half(path);rp=[transform(p)for p in hp];full=sorted(set(hp)|set(rp));scale=math.lcm(*(x.denominator for p in full for x in p));points=[tuple(int(x*scale)for x in p)for p in full];ids={p:i for i,p in enumerate(full)}
 left=[ids[p]for p in hp];right=[ids[p]for p in rp];ee,survivors=edges(points,scale);L=set(left);local={v:i for i,v in enumerate(left)}
 he=sorted(tuple(sorted((local[u],local[v])))for u,v in ee if u in L and v in L)
 lookup={p:i for i,p in enumerate(hp)};rotations=[];current=hp;c=scalar(F(1,2));s=[F(0)]*8;s[2]=F(1,2);s=tuple(s)
 for k in range(6):
  rotations.append([lookup[p]for p in current]);current=[add(mul(c,p[:8]),neg(mul(s,p[8:])))+add(mul(s,p[:8]),mul(c,p[8:]))for p in current]
 if current!=hp:raise ValueError('rotation order')
 return {'points':points,'left':left,'right':right,'edges':ee,'half_edges':he,'rotations':rotations,'scale':scale,'filter_survivors':survivors}
