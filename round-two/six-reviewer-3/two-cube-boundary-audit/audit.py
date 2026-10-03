#!/usr/bin/env python3
"""Own physical row projections over QQ(h); no target code or data input."""
import argparse,json,hashlib,time,math
from pathlib import Path
from poly import Rat,add,mul,sub,scale,neg,power,primitive,prem,exactdiv,gcdp,require,tick,F,evaluate
R=Rat
H=R((0,1))
POS=((0,1),(-1,1),(4,3),(-2,3),(-1,3),(2,3))
def scalar_data(h=H):
 s=3*h+2; ell=3*h+4; d=3*h-2;t=3*h-1;rho=1/d
 e2=2/(3*h)+t/(3*d*d);c0=(12*h-8)/(ell*ell)
 f=-6*d/(ell*t);g=-3*f;a0=f/(2*h);cl=24/(ell*s)
 b=-9*h*(h+1)/(ell*s*(h-1));a=-b/2
 ch=27*(h+1)/(2*ell*s)-6*d/(h*h*ell*t*s)
 b2=s*(h-1)/(3*h);w=s-1
 hl=w-c0-a0*a0*e2-a*a*b2-2*s*ch*ch/3
 hf=w-c0-b*b*b2-2*s*ch*ch/(3*(h-1))-2*s*cl*cl/(3*h*h)
 ll=w-c0-f*f*e2-2*s*cl*cl/3;lf=w-c0-9*f*f*e2
 ph=-1-c0-a*b*b2;pl=-1-c0+3*f*f*e2
 mh=(2*ph+hf)/3;ml=(2*pl+lf)/3
 ah=2*(2*hl-ph-hf);al=2*(2*ll-pl-lf);bh=hf-mh;bl=lf-ml
 nu=(h*mh-ml/h)/(h-1)
 return locals()
def vec(n,items):
 v=[R() for _ in range(n)]
 for i,x in items.items():v[i]=R(x) if isinstance(x,int) else x
 return v
def plus(*vs):return [sum((v[i] for v in vs),R()) for i in range(len(vs[0]))]
def times(v,k):return [x*k for x in v]
def cap(metric,weighted,N):
 n=len(metric);m=[[R() for _ in range(n)] for _ in range(n)]
 for c,weight in weighted:
  v=[x*y for x,y in zip(c,metric)]
  for i in range(n):
   for j in range(n):m[i][j]-=weight*v[i]*v[j]
 for i in range(n):m[i][i]+=(N-1)*metric[i]
 require(all(not (m[i][j]-m[j][i]).n for i in range(n) for j in range(n)),'symmetric physical cap')
 return m

def forms(name):
 z=scalar_data();h,s,ell,ch,cl,a,b,a0,f,g,rho,ah,al,bh,bl,nu,ml=[z[k] for k in ('h','s','ell','ch','cl','a','b','a0','f','g','rho','ah','al','bh','bl','nu','ml')];N=6*h+10
 if name in ('heavy-odd','light-odd'):
  c,alpha=(ch,ah) if name=='heavy-odd' else (cl,al)
  metric=[2*s,alpha];weighted=[([R(1)/2,R()],2),([-c/2,R(1)/2],2)]
 elif name=='contrast':
  metric=[2*s/3,12*s,2*bh,2*nu]
  weighted=[([R(1)/2,R(1)/12,R(),R()],4),([R(1)/2,-R(1)/6,R(),R()],2),([a/2,ch/12,-R(1)/4,R(1)/2],4),([b/2,ch/(6*(h-1)),R(1)/2,R(1)/2],2)]
 elif name=='fixed':
  metric=[R(1),3*h,3*h,6*h*s,s*(h-1)/(3*h),6*s,h*bh,bl,ml]
  k=vec(9,{0:1,1:1/h,2:(h-1)/h,4:3});zz=times(k,-1/ell)
  e=vec(9,{1:(1-rho)/(3*h),2:(1+rho)/(3*h),4:-rho})
  x=vec(9,{1:1/(3*h),2:1/(3*h)});y=vec(9,{1:1/(3*h),2:-1/(3*h),4:1})
  weighted=[(vec(9,{0:1,2:-1}),1),(vec(9,{0:1,2:1}),1),(vec(9,{0:-1,1:-1}),1),(zz,1)]
  weighted += [(plus(x,vec(9,{3:1/(6*h)})),2*h),(plus(x,vec(9,{3:-1/(3*h)})),h),(plus(y,vec(9,{5:R(1)/6})),2),(plus(y,vec(9,{5:-R(1)/3})),1)]
  weighted += [(plus(zz,times(e,a0),vec(9,{3:ch/(6*h),6:-1/(2*h),8:1/h})),2*h),(plus(zz,vec(9,{3:-ch/(3*h),5:-cl/(3*h),6:1/h,8:1/h})),h),(plus(zz,times(e,f),vec(9,{5:cl/6,7:-R(1)/2,8:-1})),2),(plus(zz,times(e,g),vec(9,{7:1,8:-1})),1)]
  require(not (sum((w for _,w in weighted),R())-N).n,'every original row including empty')
 else:raise ValueError('sector')
 return metric,cap(metric,weighted,N)

def strip(p):
 removed=[]
 for f in POS:
  e=0
  while p and len(p)>=len(f) and not prem(p,f):p=exactdiv(p,f);e+=1
  removed.append(e)
 content=math.gcd(*p) if p else 0
 return primitive(p),removed,content

def shift(p):return tuple(sum(p[j]*math.comb(j,i)*2**(j-i) for j in range(i,len(p))) for i in range(len(p)))
def positive(p):
 q,removed,content=strip(p);coeff=shift(q)
 require(bool(coeff) and coeff[0]>0 and all(v>=0 for v in coeff),'all-h shifted positivity')
 return {'numerator':list(q),'positive_factor_exponents':removed,'positive_content':content,'shifted_coefficients':list(coeff)}
def denominator(p):
 q,e,c=strip(p);require(q==(1,),'denominator must factor only into positive original poles');return {'factor_exponents':e,'content':c}

def bareiss(a):
 a=[list(r) for r in a];previous=(1,);n=len(a)
 for k in range(n-1):
  pivot=a[k][k];require(bool(pivot),'zero Bareiss pivot')
  for i in range(k+1,n):
   for j in range(k+1,n):a[i][j]=exactdiv(sub(mul(pivot,a[i][j]),mul(a[i][k],a[k][j])),previous)
  previous=pivot;tick()
 return a[-1][-1]

def uniform(name):
 if name=='scalars':
  z=scalar_data();return {'sector':name,'signs':{k:{'positive':positive(z[k].n),'denominator':denominator(z[k].d),'rational':[list(z[k].n),list(z[k].d)]} for k in ('ah','bh','al','bl','nu','ml')}}
 metric,m=forms(name);n=len(m);rows=[];clear=[]
 for r in m:
  d=(1,)
  for z in r:d=exactdiv(mul(d,z.d),gcdp(d,z.d))
  dp=denominator(d);polys=[mul(z.n,exactdiv(d,z.d)) for z in r]
  common=()
  for p in polys:common=gcdp(common,p)
  _,ex,_=strip(common);factor=(1,)
  for f,e in zip(POS,ex):factor=mul(factor,power(f,e))
  polys=[exactdiv(p,factor) for p in polys]
  c=math.gcd(*(v for p in polys for v in p));polys=[tuple(v//c for v in p) for p in polys]
  rows.append(polys);clear.append({'denominator':list(d),'positive_denominator':dp,'removed_positive_factor':list(factor),'positive_row_content':c})
 signs=[]
 for k in range(1,n+1):signs.append(positive(bareiss([r[:k] for r in rows[:k]])))
 tick();return {'sector':name,'metric':[[list(z.n),list(z.d)] for z in metric],'rational_form':[[[list(z.n),list(z.d)] for z in r] for r in m],'clearing':clear,'integer_polynomial_rows':rows,'signs':signs}

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--sector',required=True,choices=['scalars','heavy-odd','light-odd','contrast','fixed']);ap.add_argument('--output',required=True);ap.add_argument('--check');a=ap.parse_args();o=uniform(a.sector)
 if a.check:require(json.dumps(json.loads(Path(a.check).read_text()),sort_keys=True,separators=(',',':'))==json.dumps(o,sort_keys=True,separators=(',',':')),'complete expected record')
 raw=json.dumps(o,sort_keys=True,separators=(',',':')).encode();Path(a.output).write_bytes(raw+b'\n');print(json.dumps({'status':'PASS','sector':a.sector,'record_bytes':len(raw)+1,'sha256':hashlib.sha256(raw+b'\n').hexdigest(),'positive_obligations':len(o['signs'])}))
if __name__=='__main__':main()
