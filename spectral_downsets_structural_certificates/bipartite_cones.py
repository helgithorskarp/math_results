#!/usr/bin/env python3
"""Capped maximal-rank H matrices for K1 joined to K_(u,v),2<=u<=v.

The two parts may be swapped to normalize any u,v>=2. Signed entries are
allowed. See BIPARTITE_CONES.md for the complete all-parameter proof.
centered_face returns a necessary invariant affine face, not a PSD test.
"""
from fractions import Fraction as F
from itertools import product
import certificates as base
from maxrank_mixtures import integer_at_least,repaired_core


def scope(u,v):
    integer_at_least(u,2,'u');integer_at_least(v,u,'v')


def centered_face(u,v,aL=0,aR=0,tL=0,tR=0,bL=0,bR=0,bT=0):
    scope(u,v)
    values=(aL,aR,tL,tR,bL,bR,bT)
    if any(not isinstance(a,(int,F)) or isinstance(a,bool) for a in values):
        raise ValueError('Face coordinates must be exact rational numbers')
    aL,aR,tL,tR,bL,bR,bT=map(F,values)
    pL=1-(u-1)*aL-v*tL;pR=1-(v-1)*aR-u*tR
    wL=F(v+1,v*(u-1))-aL/v-tR/(u-1)
    wR=F(u+1,u*(v-1))-aR/u-tL/(v-1)
    q=2-(u-1)*wL-(v-1)*wR
    cL=-(u+(u-1)*bL+v*bT)/F(v*(u-1))
    cR=-(v+(v-1)*bR+u*bT)/F(u*(v-1))
    z=-cL/(v-1)-cR/(u-1)
    return dict(aL=aL,aR=aR,tL=tL,tR=tR,bL=bL,bR=bR,bT=bT,
                pL=pL,pR=pR,q=q,wL=wL,wR=wR,cL=cL,cR=cR,z=z)


def parameters(u,v):
    scope(u,v)
    return centered_face(u,v,tL=F(1,v),tR=F(1,u),
                         bL=-F(v,u*u),bR=-1,bT=F(u-1,u*u))


def family(u,v,shift=0):
    scope(u,v);integer_at_least(shift,0,'shift')
    h=u+v;a=1 << h
    members=[0,a]+[1 << i for i in range(h)]+[a|(1 << i) for i in range(h)]
    members += [(1 << i)|(1 << (u+j)) for i,j in product(range(u),range(v))]
    return sorted(x << shift for x in members)


def core(u,v,weights=None):
    """Literal core. Custom face weights carry no PSD/cap guarantee."""
    w=parameters(u,v) if weights is None else weights
    if set(w)!=set(parameters(u,v)) or any(not isinstance(x,(int,F)) or isinstance(x,bool) for x in w.values()):
        raise ValueError('Invalid exact core weights')
    h=u+v;a=1 << h;leftmask=(1 << u)-1;members=family(u,v)[1:]
    def kind(x):return 'a' if x==a else 'c' if x.bit_count()==1 else 'x' if x & a else 'e'
    def part(x):return 'L' if x & leftmask else 'R'
    answer=[]
    for x in members:
        row=[]
        for y in members:
            types=''.join(sorted((kind(x),kind(y))))
            if x==y:z=F(h)
            elif x & y:z=F(-1)
            elif types=='ac':z=w['p'+part(y if x==a else x)]
            elif types=='ae':z=w['q']
            elif types=='cc':z=w['b'+part(x)] if part(x)==part(y) else w['bT']
            elif types=='cx':
                c=x if kind(x)=='c' else y;sp=y if kind(x)=='c' else x
                z=w[('a' if part(c)==part(sp) else 't')+part(c)]
            elif types=='ce':z=w['c'+part(x if kind(x)=='c' else y)]
            elif types=='ex':z=w['w'+part(x if kind(x)=='x' else y)]
            elif types=='ee':z=w['z']
            else:raise ValueError('Missing disjoint pair type')
            row.append(F(z))
        answer.append(row)
    return answer


def make_nonconstant(members,colors,s):
    """A proper s-color partition; center-star colors stay unchanged."""
    counts=[colors.count(c) for c in range(s)]
    if len(set(counts))>1:return list(colors)
    leaf=1;index=members.index(leaf)
    used={c for x,c in zip(members,colors) if x & leaf}
    target=next((c for c in range(s) if c not in used),None)
    if target is None:raise ValueError('No unused singleton color')
    answer=list(colors);answer[index]=target
    return answer


def colors(u,v):
    s=u+v+1;members=family(u,v)[1:];answer=[]
    for x in members:
        vertices=[i for i in range(s) if x & (1 << i)]
        answer.append((2*vertices[0] if len(vertices)==1 else sum(vertices)) % s)
    return make_nonconstant(members,answer,s)


def centered_certificate(u,v,shift=0):
    return family(u,v,shift),base.lift(core(u,v),u+v+1),u+v+1


def certificate(u,v,shift=0):
    C,_=repaired_core(core(u,v),colors(u,v),u+v+1)
    return family(u,v,shift),base.lift(C,u+v+1),u+v+1
