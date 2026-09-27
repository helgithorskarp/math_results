"""Uniform low-threshold envelopes for every prior in the simplex.
Floating root proposals are never accepted without exact integer bounds.
"""
from fractions import Fraction as F
from hashlib import sha256
from common import r
import math,time

def proposal(S,record,lower):
 dots,norms=record; ff=[(d/r.Q,n/(2*r.Q)) for d,n in zip(dots,norms)];s=float(S);lo=2.25;hi=s+3
 for _ in range(28):
  x=(lo+hi)/2;exponents=[s*s/2-x*x/2+x*d-n for d,n in ff]
  largest=max(exponents);val=[math.exp(v-largest) for v in exponents]
  total=15*sum(val)+(0 if lower else 16)
  if largest+math.log(total)>math.log(256):lo=x
  else:hi=x
 return int((lo if lower else hi)*r.RQ)+(-2 if lower else 3)

def checked(S,record,x,lower):
 dots,norms=record;q=S*S/2*r.EQ;r.need(q.denominator==1,'q');base=int(q)-x*x*(1<<(r.D-r.RB));vals=[]
 for dot,norm in zip(dots,norms):
  a,b=r.exp_signed(base+2*x*dot-norm*(1<<r.RB));vals.append(a if lower else b)
 total=15*sum(vals)+(0 if lower else 16*max(vals));slack=total-256*r.EXPQ if lower else 256*r.EXPQ-total
 r.need(x>F(9,4)*r.RQ and slack>0,'unverified root');return slack


def band(n,step,start,stop,progress=False):
 ps=r.patches(n);N=int((stop-start)/step);r.need(start+N*step==stop,'cover');prev=None;best=None;arg=None;slack=None;stream=sha256();starttime=time.monotonic()
 for k in range(N+1):
  S=start+k*step;xx=[];yy=[]
  for p in ps:
   x=proposal(S,p['x'],True);y=proposal(S,p['y'],False)
   for rec,root,lower in [(p['x'],x,True),(p['y'],y,False)]:
    ss=checked(S,rec,root,lower);slack=ss if slack is None else min(slack,ss)
   xx.append(x);yy.append(y);stream.update(f'{k},{p["index"]},{x},{y};'.encode())
  if prev is not None:
   value=F(0)
   for p,x,y in zip(ps,prev,yy):
    d=F(x**3-y**3,r.RQ**3);value+=8*p['area']*d*(p['jl'] if d>=0 else p['ju'])
   r.need(value>F(1,2),f'failed volume band{n} S{S-step}: {float(value)}')
   if best is None or value<best:best=value;arg=S-step
  prev=xx
  if progress and k%40==0:print('band',n,'row',k,'of',N,'seconds',round(time.monotonic()-starttime,1),flush=True)
 return {'n':n,'step':str(step),'start':str(start),'stop':str(stop),'patches':len(ps),'windows':N,'roots':2*(N+1)*len(ps),'lower':str(best),'worst_S':str(arg),'minimum_slack':slack,'stream_sha256':stream.hexdigest()}
