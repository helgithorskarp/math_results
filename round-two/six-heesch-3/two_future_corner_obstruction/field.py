#!/usr/bin/env python3
"""Exact Q(sqrt(3)) extension of the strip's polygon packing reader.

Coordinates still mean (x,sqrt(3)*y)/4. Unlike the integer lower reader,
this module accepts all twelve rotations in 30-degree steps and arbitrary
translations in Q(sqrt(3)). It does not restrict arbitrary translations to
this field without a geometric anchor. Shared SAT code is not independent
verification; the field and congruence formulas are checked separately.
Author six-heesch-3, researcher.
"""
from dataclasses import dataclass
from fractions import Fraction
from functools import lru_cache,total_ordering
import geometry as b


@total_ordering
@dataclass(frozen=True,slots=True)
class Q3:
    a: Fraction
    b: Fraction=Fraction(0)

    def __post_init__(self):
        object.__setattr__(self,'a',Fraction(self.a))
        object.__setattr__(self,'b',Fraction(self.b))

    @staticmethod
    def of(value):
        return value if isinstance(value,Q3) else Q3(value)

    def sign(self):
        a,c=self.a,self.b
        if not c:return (a>0)-(a<0)
        if not a:return (c>0)-(c<0)
        if a>0 and c>0:return 1
        if a<0 and c<0:return -1
        delta=a*a-3*c*c
        b.require(delta!=0,'nonzero rational equals irrational sqrt3')
        return ((delta>0)-(delta<0))*(1 if a>0 else -1)

    def __add__(self,other):
        other=Q3.of(other);return Q3(self.a+other.a,self.b+other.b)
    __radd__=__add__

    def __neg__(self):return Q3(-self.a,-self.b)
    def __sub__(self,other):return self+-Q3.of(other)
    def __rsub__(self,other):return Q3.of(other)+-self

    def __mul__(self,other):
        other=Q3.of(other)
        return Q3(self.a*other.a+3*self.b*other.b,
                  self.a*other.b+self.b*other.a)
    __rmul__=__mul__

    def __eq__(self,other):
        if not isinstance(other,(Q3,int,Fraction)):return NotImplemented
        other=Q3.of(other);return self.a==other.a and self.b==other.b

    def __hash__(self):
        return hash(self.a) if not self.b else hash((self.a,self.b,'sqrt3'))

    def __lt__(self,other):return (self-Q3.of(other)).sign()<0
    def serial(self):return [str(self.a),str(self.b)]


def linear(a,f,p):
    b.require(a in range(12) and f in (0,1),'bad 30-degree linear part')
    x,y=p
    if f:y=-y
    x,y=b.rotate(a-a%2,(x,y))
    if a%2:return Q3(0,Fraction(x-y,2)),Q3(0,Fraction(x+3*y,6))
    return Q3(x),Q3(y)


def point(pose,p):
    a,f,tx,ty=pose;x,y=linear(a,f,p)
    return x+tx,y+ty


def int_pose(pose):
    a,f,x,y=pose;return a,f,Q3(x),Q3(y)


def pose_serial(pose):
    a,f,x,y=pose;return [a,f,x.serial(),y.serial()]


def anchor(a,f,prototype_vertex,target_vertex):
    x,y=linear(a,f,prototype_vertex)
    return a,f,Q3(target_vertex[0])-x,Q3(target_vertex[1])-y


@lru_cache(None)
def shape(m,pose):
    a,f,tx,ty=pose
    aa=tuple(tuple(reversed(q)) if f else q for q in
             (tuple(point(pose,v) for v in atom) for atom in b.atoms(m)))
    return aa,tuple(b.box(p) for p in aa),b.box(tuple(v for p in aa for v in p))


@lru_cache(None)
def pair(m,p,q):
    aa,ab,abox=shape(m,p);bb,bc,bbox=shape(m,q)
    if not b.boxes_meet(abox,bbox):return False,False
    touch=False
    for pa,ba in zip(aa,ab):
        for pb,bp in zip(bb,bc):
            if not b.boxes_meet(ba,bp):continue
            if b.boxes_meet(ba,bp,False) and b.convex_intersection(pa,pb,False):
                return True,True
            if not touch and b.convex_intersection(pa,pb,True):touch=True
    return False,touch
