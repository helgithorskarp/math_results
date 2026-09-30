#!/usr/bin/env python3
"""Capped maximal-rank H for K2 joined to K_(u,v), u,v>=2.

Normalize 2<=u<=v. TWO_CENTER_BIPARTITE.md gives the all-parameter proof.
centered_face is an affine characterization, not a PSD test. Custom core
weights carry no PSD/cap guarantee. The production parameters are proved.
"""
from fractions import Fraction as F
from itertools import product
import certificates as base
from maxrank_mixtures import integer_at_least,repaired_core
from bipartite_cones import make_nonconstant


def scope(u,v):
    integer_at_least(u,2,'u');integer_at_least(v,u,'v')


def family(u,v,shift=0):
    scope(u,v);integer_at_least(shift,0,"shift");h=u+v;A=[1 << h,1 << (h+1)]
    members=[0]+A+[A[0]|A[1]]+[1 << i for i in range(h)]+[a|(1 << i) for a in A for i in range(h)]
    members += [(1 << i)|(1 << (u+j)) for i,j in product(range(u),range(v))]
    return sorted(x << shift for x in members)


def centered_face(u,v,kL=0,kR=0,kT=0,aL=0,aR=0,tL=0,tR=0,bL=0,bR=0,bT=0,qL=0,qR=0):
    scope(u,v)
    raw=(kL,kR,kT,aL,aR,tL,tR,bL,bR,bT,qL,qR)
    if not all(isinstance(x,(int,F)) and not isinstance(x,bool) for x in raw):
        raise ValueError('Require exact rational coordinates')
    kL,kR,kT,aL,aR,tL,tR,bL,bR,bT,qL,qR=map(F,raw)
    pL=2-(u-1)*kL-v*kT;pR=2-(v-1)*kR-u*kT
    bA=1-u*pL-v*pR
    qA=-(1+u*qL+v*qR)/F(u*v)
    rL=1-(u-1)*aL-v*tL-qL;rR=1-(v-1)*aR-u*tR-qR
    wL=(v-(u-1)*aL-v*tR)/F(v*(u-1))
    wR=(u-(v-1)*aR-u*tL)/F(u*(v-1))
    qF=2-(u-1)*wL-(v-1)*wR-qA
    cL=-(u+qL+(u-1)*(aL+bL)+v*(tL+bT))/F(v*(u-1))
    cR=-(v+qR+(v-1)*(aR+bR)+u*(tR+bT))/F(u*(v-1))
    z=(qF-1-(u-1)*cL-(v-1)*cR)/F((u-1)*(v-1))
    return dict(kL=kL,kR=kR,kT=kT,aL=aL,aR=aR,tL=tL,tR=tR,bL=bL,bR=bR,bT=bT,qL=qL,qR=qR,
                pL=pL,pR=pR,bA=bA,qA=qA,rL=rL,rR=rR,wL=wL,wR=wR,qF=qF,cL=cL,cR=cR,z=z)


def _tail_face(u,v,alpha=1):
    scope(u,v)
    return centered_face(u,v,kL=F(2,u-1),kR=F(2,v-1),tL=F(2,v),tR=F(2,u),
                bL=-F(alpha*v,u*u),bR=-1+F(1,v),bT=F(alpha*(u-1),u*u),qR=-F(1,3))


def parameters(u,v):
    scope(u,v)
    if u!=2 or v>=5:return _tail_face(u,v)
    h=u+v
    old=centered_face(u,v,kL=F(2,h),kR=F(2,h),kT=F(2,h),bL=-F(h+1,h),bR=-F(h+1,h),
             bT=-F(h+1,h),qL=-F(1,h),qR=-F(1,h))
    new=_tail_face(u,v,F(3,4))
    return {k:(old[k]+new[k])/2 for k in old}


def core(u,v,weights=None):
    w=parameters(u,v) if weights is None else weights
    if not isinstance(w,dict) or set(w)!=set(centered_face(u,v)) or any(not isinstance(x,(int,F)) or isinstance(x,bool) for x in w.values()):
        raise ValueError('Invalid exact core weights')
    h=u+v;centers=(1 << h)|(1 << (h+1));left=(1 << u)-1;D=family(u,v)[1:]
    def kind(x):
        if x.bit_count()==1:return 'A' if x & centers else 'C'
        return 'F' if x==centers else 'P' if x & centers else 'E'
    def part(x):return 'L' if x & left else 'R'
    result=[]
    for x in D:
        row=[]
        for y in D:
            a,b=kind(x),kind(y);types=''.join(sorted((a,b)))
            if x==y:z=F(h+1)
            elif x & y:z=F(-1)
            elif types=='AA':z=w['bA']
            elif types=='AC':z=w['q'+part(y if a=='A' else x)]
            elif types=='AP':z=w['p'+part(y if a=='A' else x)]
            elif types=='AE':z=w['qA']
            elif types=='CF':z=w['r'+part(x if a=='C' else y)]
            elif types=='EF':z=w['qF']
            elif types=='CC':z=w['b'+part(x)] if part(x)==part(y) else w['bT']
            elif types=='CP':
                c=x if a=='C' else y;p=y if a=='C' else x
                z=w[('a' if part(c)==part(p) else 't')+part(c)]
            elif types=='CE':z=w['c'+part(x if a=='C' else y)]
            elif types=='PP':z=w['k'+part(x)] if part(x)==part(y) else w['kT']
            elif types=='EP':z=w['w'+part(x if a=='P' else y)]
            elif types=='EE':z=w['z']
            else:raise ValueError('Missing disjoint orbit '+types)
            row.append(F(z))
        result.append(row)
    return result



def colors(u,v):
    s=u+v+2;members=family(u,v)[1:];answer=[]
    for x in members:
        vertices=[i for i in range(s) if x & (1 << i)]
        answer.append((2*vertices[0] if len(vertices)==1 else sum(vertices)) % s)
    return make_nonconstant(members,answer,s)


def centered_certificate(u,v,shift=0):
    return family(u,v,shift),base.lift(core(u,v),u+v+2),u+v+2


def certificate(u,v,shift=0):
    repaired,_=repaired_core(core(u,v),colors(u,v),u+v+2)
    return family(u,v,shift),base.lift(repaired,u+v+2),u+v+2
