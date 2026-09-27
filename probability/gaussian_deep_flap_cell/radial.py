#!/usr/bin/env python3
"""Integer-verified radial volume signs for the deep-flap parameter cell.

Floating point proposes radial brackets ONLY. Each used endpoint is checked
with integer exponential enclosures before it enters a volume bound.
"""
from collections import Counter
from fractions import Fraction as F
from hashlib import sha256
from math import exp, isqrt
from pathlib import Path
import argparse, json, sys, time

HERE=Path(__file__).resolve().parent
DEPENDENCY=HERE.parent/'gaussian_prior_localization'
PINS = {'direct_hinge.py': '94e9ee5f643a6d98bf18983eda3a13f5b8513f2f6e06753ad133ad046d2e5bb9', 'DIRECT_HINGE.md': 'b6abfa8a14481aa834869403f80c424c7d9f62b75a62e5db6890d1278c4867ea', 'CUBATURE_FRONTIER.md': '0dbcaf36263ee8ce2976d75d1073db4f878db908fd5c53161e55485c5da53632'}
for name,digest in PINS.items():
    if sha256((DEPENDENCY/name).read_bytes()).hexdigest()!=digest:
        raise ValueError('dependency mismatch: '+name)
sys.path.insert(0,str(DEPENDENCY))
from direct_hinge import exp_neg, sqrt_bounds

D=40;Q=1<<D;RB=20;RQ=1<<RB;EP=D+RB+1;EQ=1<<EP
BITS=50;EXPQ=1<<BITS
EPS=F(1,1024)
V=[(1,1,1),(1,-1,-1),(-1,1,-1),(-1,-1,1)]
X=[tuple(F(a,2) for a in v) for v in V]
Y=[tuple(F(63*a,128) for a in v) for v in V]
for i in range(4):
    for j in range(4):
        if i!=j:
            X.append(tuple(F(V[j][k]-2*V[i][k],2) for k in range(3)))
            Y.append(tuple(F(63*(V[j][k]+2*V[i][k]),128) for k in range(3)))

def need(c,msg):
    if not c:raise ValueError(msg)

def ceilq(x):return -((-x.numerator)//x.denominator)

def exp_neg_dyadic(num,power,bits=BITS):
    """exp(-num/2**power), integer outward enclosure /2**bits."""
    need(num>=0 and power>=0 and bits>=16,'invalid exponential')
    out=1<<bits
    if not num:return out,out
    sq=max(0,num.bit_length()-power+3)
    work=bits+2*sq+16;S=1<<work
    den=1<<(power+sq)
    rl=(num*S)//den;rh=(num*S+den-1)//den
    need(0<=rl<=rh<=S//8,'range reduction')
    tl=th=S;sl=sh=S;n=0
    while True:
        n+=1;prev_high=sh
        tl=tl*rl//(S*n);th=(th*rh+S*n-1)//(S*n)
        if n%2:sl-=th;sh-=tl
        else:sl+=tl;sh+=th
        if n%2 and th<=1:
            lo,hi=sl,prev_high
            break
        need(n<=200,'Taylor termination')
    for _ in range(sq):
        lo=lo*lo//S;hi=min(S,(hi*hi+S-1)//S)
    scale=1<<(work-bits)
    lo//=scale;hi=min(out,(hi+scale-1)//scale)
    need(0<=lo<=hi<=out and hi-lo<=2,'exp enclosure invariant')
    return lo,hi

def exp_signed(num,power=EP):
    if num<=0:return exp_neg_dyadic(-num,power)
    a,b=exp_neg_dyadic(num,power)
    need(a>0,'unbounded positive relative exponential')
    return EXPQ*EXPQ//b,(EXPQ*EXPQ+a-1)//a

def patches(n):
    ans=[]
    for i in range(n):
        for j in range(i,n):
            u=F(2*i+1,2*n);v=F(2*j+1,2*n)
            norm=1+u*u+v*v
            il,ih=sqrt_bounds(1/norm,D+8)
            radius=F(3,4*n)*sqrt_bounds(1/(1+F(i,n)**2+F(j,n)**2),D+8)[1]
            jlow=sqrt_bounds(1/(1+F(i+1,n)**2+F(j+1,n)**2)**3,D+8)[0]
            jhigh=sqrt_bounds(1/(1+F(i,n)**2+F(j,n)**2)**3,D+8)[1]
            area=F(1 if i<j else 1, n*n*(1 if i<j else 2))
            for parity in [1,-1]:
                records=[]
                for P,lower in [(X,True),(Y,False)]:
                    dots=[];norms=[]
                    for p in P:
                        ns=sum(a*a for a in p);rn=sqrt_bounds(ns,D+8)[1]
                        numer=p[0]*parity*u+p[1]*v+p[2]
                        dl=numer*(il if numer>=0 else ih)
                        dh=numer*(ih if numer>=0 else il)
                        if lower:
                            d=(dl-rn*radius-EPS)
                            norm2=ns+2*rn*EPS+EPS*EPS
                            dots.append((d*Q).__floor__());norms.append(ceilq(norm2*Q))
                        else:
                            d=dh+rn*radius+EPS
                            norm2=ns-2*rn*EPS
                            dots.append(ceilq(d*Q));norms.append((norm2*Q).__floor__())
                    records.append((dots,norms))
                ans.append({'index':[i,j,parity],'area':area,'jl':jlow,'ju':jhigh,'x':records[0],'y':records[1]})
    return ans

def root_proposal(S,record,lower):
    dots,norms=record
    ff=[(d/Q,n/(2*Q)) for d,n in zip(dots,norms)]
    s=float(S);q=s*s/2
    lo=max(2.25,s-5);hi=s+3
    for _ in range(28):
        r=(lo+hi)/2
        val=sum(exp(q-r*r/2+r*d-n) for d,n in ff)
        if val>16:lo=r
        else:hi=r
    if lower:return int(lo*RQ)-2
    return int(hi*RQ)+3

def check_root(S,record,root,lower):
    need(root>F(9,4)*RQ,'root below monotone ray')
    dots,norms=record
    q_scaled=S*S/2*EQ
    need(q_scaled.denominator==1,'threshold not on the fixed dyadic scale')
    base=int(q_scaled)-root*root*(1<<(D-RB))
    total=0
    for dot,norm in zip(dots,norms):
        e=base+2*root*dot-norm*(1<<RB)
        a,b=exp_signed(e)
        total += a if lower else b
    slack=total-16*EXPQ if lower else 16*EXPQ-total
    need(slack>0,'proposed radial bracket was not verified')
    return slack

def run_band(n,step,start,stop,progress=False):
    ps=patches(n);N=int((stop-start)/step)
    need(start+N*step==stop,'incomplete parameter window')
    stream=sha256();previous=None;best=None;arg=None;minimum_slack=None
    elapsed=time.monotonic()
    for k in range(N+1):
        s=start+k*step;xl=[];yu=[]
        for p in ps:
            x=root_proposal(s,p['x'],True);y=root_proposal(s,p['y'],False)
            for data,r,lower in [(p['x'],x,True),(p['y'],y,False)]:
                slack=check_root(s,data,r,lower)
                minimum_slack=slack if minimum_slack is None else min(minimum_slack,slack)
            xl.append(x);yu.append(y)
            stream.update(f'{k},{p["index"]},{x},{y}\n'.encode())
        if previous is not None:
            total=F(0)
            for p,x,y in zip(ps,previous,yu):
                dif=F(x**3-y**3,RQ**3)
                total += 8*p['area']*dif*(p['jl'] if dif>=0 else p['ju'])
            need(total>F(1,2),f'volume margin failed at {s-step}')
            if best is None or total<best:best=total;arg=s-step
        previous=xl
        if progress and k%40==0:print(json.dumps({'band':n,'step':k,'of':N,'elapsed':round(time.monotonic()-elapsed,2)}),flush=True)
    return {'n':n,'start':str(start),'stop':str(stop),'step':str(step),'patches':len(ps),'windows':N,
       'verified_roots':2*(N+1)*len(ps),'minimum_relative_slack_units':minimum_slack,
       'volume_lower':str(best),'worst_S':str(arg),'stream_sha256':stream.hexdigest(),
       'verified_volume_margin':'1/2'}

def controls():
    cases=0
    for b in [32,50,64]:
        for p in [0,3,8,16,40,61]:
            for a in [0,1,2,3,7,8,9,31,127,255,1023,65535]:
                lo,hi=exp_neg_dyadic(a,p,b)
                L,H=exp_neg(F(a,1<<p),b+20)
                need(F(lo,1<<b)<=F(L,1<<(b+20))<=F(H,1<<(b+20))<=F(hi,1<<b), 'independent high-precision exp check')
                cases+=1
    return {'exponential_controls':cases}

