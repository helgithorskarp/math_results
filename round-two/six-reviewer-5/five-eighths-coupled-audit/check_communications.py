"""Exact original-polynomial controls; no numeric root finder or author code."""
from fractions import Fraction as Q
from math import comb
from pathlib import Path
import json, hashlib

Z=(Q(0),Q(0)); I=(Q(0),Q(1)); U=(Q(1),Q(0))
def add(x,y):return (x[0]+y[0],x[1]+y[1])
def neg(x):return (-x[0],-x[1])
def mul(x,y):return (x[0]*y[0]-x[1]*y[1],x[0]*y[1]+x[1]*y[0])
def norm(x):return x[0]**2+x[1]**2
def inv(x):
    if norm(x)==0:raise ValueError('zero complex division')
    return (x[0]/norm(x),-x[1]/norm(x))
def scale(x,a):return (x[0]*a,x[1]*a)
def power(x,n):
    y=U
    for _ in range(n):y=mul(y,x)
    return y
def pmul(a,b):
    out=[Z]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b):out[i+j]=add(out[i+j],mul(x,y))
    return out
def product(xs):
    y=U
    for x in xs:y=mul(y,x)
    return y
def value(p,z):
    y=Z
    for x in reversed(p):y=add(mul(y,z),x)
    return y
def substitute(p,a,b):
    out=[Z]*len(p)
    for k,x in enumerate(p):
        for i in range(k+1):out[i]=add(out[i],scale(mul(x,mul(power(a,k-i),power(b,i))),Q(comb(k,i))))
    return out
def integrate(p):return tuple(sum((x[j]/Q(i+1) for i,x in enumerate(p)),Q(0)) for j in range(2))
def check(a,roots,rotator=U):
    if len(roots)!=8 or norm(a)>Q(25,64) or any(norm(x)>1 for x in roots):raise ValueError('all nine original disk inputs')
    original=[U]
    for z in [a]+roots:original=pmul(original,[neg(z),U])
    derivative=[scale(original[k],Q(k)) for k in range(1,10)]
    da=value(derivative,a)
    if norm(da)==0:return dict(branch='marked multiple zero; infinity',original=original,derivative=derivative)
    if a[1]!=0 or a[0]<=0:raise ValueError('positive real normalized mark')
    aa=a[0]
    origin=scale(mul(integrate(substitute(derivative,a,neg(a))),inv(da)),Q(9))
    expected_origin=scale(mul(product(roots),inv(da)),Q(9))
    polar=scale(mul(integrate(substitute(derivative,a,(1/aa-aa,Q(0)))),inv(da)),aa**8)
    expected_polar=product([mul(add(U,neg(scale(z,aa))),inv(add(a,neg(z)))) for z in roots])
    if origin!=expected_origin or polar!=expected_polar:raise ValueError('whole original communication identities')
    if norm(polar)<1 or norm(origin)>norm(scale(inv(da),Q(9))):raise ValueError('original channel modulus caps')
    # Exact coefficient covariance under arbitrary chosen unit rotation.
    if norm(rotator)!=1:raise ValueError('unit rotation')
    rotated=[U]
    for z in [a]+roots:rotated=pmul(rotated,[neg(mul(rotator,z)),U])
    if rotated!=[mul(original[k],power(rotator,9-k)) for k in range(10)]:raise ValueError('full monic rotation covariance')
    return dict(branch='simple mark',a=a,roots=roots,original=original,derivative=derivative,origin=origin,polar=polar,rotator=rotator,rotated=rotated)

if __name__=='__main__':
    roots=[U,I,(Q(-1,2),Q(0)),(Q(1,2),Q(1,3)),(Q(1,4),Q(1,2)),(Q(1,4),Q(1,2)),(Q(0),Q(-1,3)),(Q(1,7),Q(-1,2))]
    records=[]
    for a in (Q(3,5),Q(5,8)):
        for zero in (False,True):
            rr=roots[:]
            if zero:rr[0]=Z
            records.append(check((a,Q(0)),rr,(Q(3,5),Q(4,5))))
        rr=roots[:];rr[0]=(a,Q(0));records.append(check((a,Q(0)),rr))
    # Moment identities on an exposed rational Gaussian tuple, with exact radii.
    directions=[U,I,neg(U),neg(I),(Q(3,5),Q(4,5)),(Q(4,5),Q(-3,5)),(Q(-3,5),Q(4,5)),U]
    radii=[Q(7,8),Q(9,8),Q(3,4),Q(5,4),Q(1),Q(7,8),Q(9,8),Q(1)]
    q=[scale(d,r) for d,r in zip(directions,radii)]
    mu=scale(tuple(sum((x[k] for x in q),Q(0)) for k in range(2)),Q(1,8));F=sum(radii,Q(0))
    E=sum((norm(add(x,neg(U))) for x in q),Q(0));T=sum(((r-1)**2 for r in radii),Q(0));Pi=F-8*mu[0]
    S=sum((norm(add(x,neg(mu))) for x in q),Q(0))
    if E!=T+2*Pi or S!=E-8*norm(add(mu,neg(U))) or S!=T+2*F-8-8*norm(mu):raise ValueError('all coupled moment identities')
    records.append(dict(q=q,radii=radii,mu=mu,F=F,E=E,T=T,Pi=Pi,S=S))
    raw=json.dumps(records,sort_keys=True,separators=(',',':'),default=str).encode()
    p=Path(__file__).resolve().parent;(p/'communications-private.json').write_bytes(raw)
    print(json.dumps(dict(status='PASS',original_polynomial_cases=6,moment_cases=1,record_bytes=len(raw),record_sha256=hashlib.sha256(raw).hexdigest())))
