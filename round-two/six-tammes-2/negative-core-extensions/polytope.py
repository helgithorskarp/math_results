"""Exact root brackets, bounded avoidance geometry and witness selection."""
from pathlib import Path
from itertools import combinations
from collections import Counter
from math import isqrt
import json,sys,time,hashlib
from dependency import e
import model as curve
Q,I,S=e.Q,e.I,e.S
LO=Q(577,1000)
HI=Q('0.59260590292507377809642492233276')
LABELS=(0,1,2,4,5,6,7,8,9,10,11,12,13,'cut')
QUAD=(7,8,10,11)
TRIPLES=tuple(combinations(range(14),3))
CRITICAL=tuple(LABELS.index(i) for i in (1,4,7))
CONTACTS={tuple(sorted(pair)) for pair in ((0,5),(0,6),(0,7),(0,11),(1,2),(1,4),(1,10),(1,12),
 (2,4),(2,8),(2,10),(2,13),(4,8),(5,7),(5,9),(5,11),(6,8),(6,11),(7,12),(8,13),
 (9,10),(9,11),(10,12))}
OUTER_BOUND=10
MAX_DEPTH=18
MAX_NODES=20000
def edot(a,b):return sum((x*y for x,y in zip(a,b)),I())
def cm(A,rhs):
    pairs=(e.cross(A[1],A[2]),e.cross(A[2],A[0]),e.cross(A[0],A[1]))
    D=edot(A[0],pairs[0])
    C=[sum((rhs[j]*pairs[j][i] for j in range(3)),I()) for i in range(3)]
    return C,D
def sqrt_interval(x):
    e.require(x.l>0,'strictly positive square-root argument')
    l=isqrt(x.l*S);h=isqrt(x.h*S)
    if h*h<x.h*S:h+=1
    return I.raw(l,h)
def root(left,right,bits=32):
    rows=e.factor_bernstein(-1,0,left,right)
    a,b=Q(29,5),Q(39,5);sa,sb=e.point_sign(rows,a),e.point_sign(rows,b)
    e.require(sa*sb==-1,'uniform quartic bracket signs')
    low,high=a,b
    for _ in range(bits):
        m=(low+high)/2
        if e.point_sign(rows,m)==sa:low=m
        else:high=m
    aa=low;low,high=a,b
    for _ in range(bits):
        m=(low+high)/2
        if e.point_sign(rows,m)==sb:high=m
        else:low=m
    bb=high
    e.require(aa<bb and e.point_sign(rows,aa)==sa and e.point_sign(rows,bb)==sb,'root enclosure')
    return aa,bb
def geometry(left,right):
    a,b=root(left,right);mid=(left+right)/2;ma,mb=root(mid,mid,48)
    model=curve.enclosed_model(left,right,a,b,ma,mb);t=I(left,right)
    P={i:[z.v for z in p] for i,p in model['P'].items()}
    H=[[z.v for z in row] for row in model['H']]
    A=[[P[i][j] for i in QUAD[:3]] for j in range(3)]
    w=e.solve(A,[-v for v in P[QUAD[3]]])
    if not all(x.l>0 for x in w):raise ArithmeticError('positive-spanning weights unresolved')
    for triple in combinations(QUAD,3):
        v=e.solve([e.mv(H,P[i]) for i in triple],[t]*3)
        if any(max(abs(x.l),abs(x.h))>=OUTER_BOUND*S for x in v):
            raise ArithmeticError('outer coordinate bound unresolved')
    nn=model['nn'].v
    if nn.l<=0:raise ArithmeticError('nonzero cut normal unresolved')
    rhs=[t]*13+[Q(893,1000)*model['length'].v]
    A=[[z.v for z in model['rows'][i]] for i in LABELS]
    model['A']=[model['rows'][i] for i in LABELS]
    model['A0']=[model['rows0'][i] for i in LABELS]
    model['rhs']=[model['t']]*13+[Q(893,1000)*model['length']]
    model['rhs0']=[model['t0']]*13+[Q(893,1000)*model['length0']]
    return A,rhs,H,(a,b),nn.l,model
def dual_dot(a,b):return sum((x*y for x,y in zip(a,b)),curve.D())
def dual_cm(A,rhs):
    pairs=(curve.cross(A[1],A[2]),curve.cross(A[2],A[0]),curve.cross(A[0],A[1]))
    D=dual_dot(A[0],pairs[0])
    C=[sum((rhs[j]*pairs[j][i] for j in range(3)),curve.D()) for i in range(3)]
    return C,D
def cut_gram_norm(triple,model):
    if triple[-1]!=13:return None
    a,b=(LABELS[i] for i in triple[:2]);P,H,n,t=(model[k] for k in ('P','H','n','t'))
    s=t if tuple(sorted((a,b))) in CONTACTS else curve.dot(P[a],P[b],H)
    if (1-s*s).v.l<=0:return None
    # Every summand defining n is an intersection with the B4 plane.
    def product(label):
        return Q(14,5)*t if label==4 else curve.dot(n,P[label],H)
    na,nb=product(a),product(b)
    perpendicular=model['nn']-(na*na+nb*nb-2*s*na*nb)/(1-s*s)
    if perpendicular.v.l<=0:return None
    height=Q(893,1000)*model['length']-t*(na+nb)/(1+s)
    norm=2*t*t/(1+s)+height*height/perpendicular
    if norm.v.h<S:return ('gram-norm',norm.v.h)
    return None
def classify_centered(triple,model):
    A,A0,rhs,rhs0,H,H0,radius=(model[k] for k in ('A','A0','rhs','rhs0','H','H0','radius'))
    C,D=dual_cm([A[i] for i in triple],[rhs[i] for i in triple])
    C0,D0=dual_cm([A0[i] for i in triple],[rhs0[i] for i in triple])
    D=curve.recondition(D,D0,radius)
    C=[curve.recondition(c,c0,radius) for c,c0 in zip(C,C0)]
    ds=D.v.sign();dh=max(abs(D.v.l),abs(D.v.h))
    for j,c in enumerate(C):
        if c.v.sign() and min(abs(c.v.l),abs(c.v.h))>OUTER_BOUND*dh:
            return ('mvt-coordinate',j)
    if ds and D0.v.sign():
        x0=[c/D0 for c in C0]
        x=[curve.recondition(c/D,c0,radius) for c,c0 in zip(C,x0)]
        norm=curve.recondition(curve.dot(x,x,H),curve.dot(x0,x0,H0),radius).v
        if norm.h<S:return ('mvt-norm',norm.h)
    need_positive=ds>=0;need_negative=ds<=0;wp=wn=None
    for j,row in enumerate(A):
        if j in triple:continue
        res=curve.recondition(dual_dot(row,C)-rhs[j]*D,
            dual_dot(A0[j],C0)-rhs0[j]*D0,radius).v
        if need_positive and res.l>0:wp=j;need_positive=False
        if need_negative and res.h<0:wn=j;need_negative=False
        if not need_positive and not need_negative:return ('mvt-homogeneous',(wp,wn))
    return None
def classify(triple,A,rhs,H):
    if triple==CRITICAL:return ('analytic-critical',None)
    C,D=cm([A[i] for i in triple],[rhs[i] for i in triple]);ds=D.sign()
    dh=max(abs(D.l),abs(D.h))
    for j,c in enumerate(C):
        if c.sign() and min(abs(c.l),abs(c.h))>OUTER_BOUND*dh:
            return ('coordinate',j)
    if ds:
        x=[c/D for c in C];norm=e.dot(x,x,H)
        if norm.h<S:return ('norm',norm.h)
    need_positive=ds>=0;need_negative=ds<=0;wp=wn=None
    for j,row in enumerate(A):
        if j in triple:continue
        res=edot(row,C)-rhs[j]*D
        if need_positive and res.l>0:wp=j;need_positive=False
        if need_negative and res.h<0:wn=j;need_negative=False
        if not need_positive and not need_negative:return ('homogeneous',(wp,wn))
    return None
