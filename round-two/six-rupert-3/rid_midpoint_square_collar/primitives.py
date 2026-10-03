"""Pinned original RID primitives and direct geometric algorithms."""
from pathlib import Path
from fractions import Fraction as Q
import hashlib, json
HERE=Path(__file__).resolve().parent
FIELD_SHA='7801bce4e611b05c8d3d982a862d3f281db7585ef5219ea8fb901c6417c129b0'
if hashlib.sha256((HERE/'field.py').read_bytes()).hexdigest()!=FIELD_SHA:
    raise ValueError('pinned public original RID arithmetic differs')
from field import F,ZERO as Z,ONE as O,PHI as phi,vertices,dot,cross,sub,encode,determinant as matrix_det
def need(p,message):
    if not p: raise ValueError(message)
def digest(data):return hashlib.sha256(json.dumps(data,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def rotate(c,v):
    c2=dot(c,c);cv=dot(c,v);cxv=cross(c,v)
    return tuple(((O-c2)*v[j]+2*c[j]*cv+2*cxv[j])/(O+c2) for j in range(3))
def projection(v,r):return (v[0]-r[0]*v[2],v[1]-r[1]*v[2])
def turn(a,b,c):return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
def hull(points):
    ordered=sorted(set(points));low=[];high=[]
    for p in ordered:
        while len(low)>1 and turn(low[-2],low[-1],p)<=Z:low.pop()
        low.append(p)
    for p in reversed(ordered):
        while len(high)>1 and turn(high[-2],high[-1],p)<=Z:high.pop()
        high.append(p)
    h=low[:-1]+high[:-1]
    need(len(h)>=3 and all(turn(a,b,p)>=Z for a,b in zip(h,h[1:]+h[:1]) for p in ordered),'full literal hull fails')
    return h
