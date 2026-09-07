"""Independent complete edges via rational interval exclusion and gcd radicals."""
from pathlib import Path
from math import isqrt,gcd
from itertools import combinations
from hashlib import sha256
import json,sys,time
W=Path(__file__).resolve().parent/'out'
RAD=[1,2,3,6,11,22,33,66];INDEX={v:i for i,v in enumerate(RAD)};Q=1<<40
LOW=[isqrt(d*Q*Q) for d in RAD];HIGH=[v if v*v==d*Q*Q else v+1 for d,v in zip(RAD,LOW)]

def interval(a):
 lo=sum(v*(LOW[i] if v>=0 else HIGH[i]) for i,v in enumerate(a))
 hi=sum(v*(HIGH[i] if v>=0 else LOW[i]) for i,v in enumerate(a))
 return lo,hi

def squared_norm(p):
 out=[0]*8
 for co in (p[:8],p[8:]):
  for i,a in enumerate(co):
   out[0]+=a*a*RAD[i]
   if not a:continue
   for j in range(i):
    b=co[j]
    if b:
     g=gcd(RAD[i],RAD[j]);d=RAD[i]*RAD[j]//(g*g)
     out[INDEX[d]]+=2*a*b*g
 return out

def square_bounds(lo,hi):
 return (0 if lo<=0<=hi else min(lo*lo,hi*hi),max(lo*lo,hi*hi))

def main():
 start=time.monotonic();path=Path(sys.argv[1]);g=json.loads(path.read_text());ps=g['points'];n=len(ps)
 if g['denominator']!=12 or g['radicands']!=RAD:raise ValueError('Wrong coordinate convention')
 if any(len(p)!=16 or any(type(x) is not int for x in p) for p in ps):raise ValueError('Bad row')
 if len(set(map(tuple,ps)))!=n:raise ValueError('Repeated point')
 iv=[interval(p[:8])+interval(p[8:]) for p in ps];unit=(12*Q)**2;es=[];near=0
 for i,(a,b,c,d) in enumerate(iv):
  for j in range(i):
   e,f,h,k=iv[j]
   xl,xh=square_bounds(a-f,b-e);yl,yh=square_bounds(c-k,d-h)
   if xl+yl<=unit<=xh+yh:
    near+=1
    if squared_norm([x-y for x,y in zip(ps[i],ps[j])])==[144,0,0,0,0,0,0,0]:es.append([j,i])
 es.sort()
 if es!=g['edges']:raise ValueError('Complete exact edge list differs from producer')
 out={'vertices':n,'edges':len(es),'all_pairs':n*(n-1)//2,'interval_survivors':near,
 'complete_exact_edges_match':True,'seconds':time.monotonic()-start,
 'points_sha256':sha256(json.dumps(ps,separators=(',',':')).encode()).hexdigest(),
 'edges_sha256':sha256(json.dumps(es,separators=(',',':')).encode()).hexdigest()}
 colour=path.parent/(path.stem+'_colour.json')
 if colour.exists():
  x=json.loads(colour.read_text());word=x.get('colouring')
  if word is not None:
   if len(word)!=n or any(c not in '0123' for c in word) or any(word[a]==word[b] for a,b in es):raise ValueError('Bad word')
   out['four_colouring_verified']=True
 (path.parent/(path.stem+'_verified.json')).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
