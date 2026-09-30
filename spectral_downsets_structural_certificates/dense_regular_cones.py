#!/usr/bin/env python3
"""Rational capped maximal-rank H matrices for dense regular graph cones.

The leaf graph is simple d-regular on h vertices, h/2 <= d <= h-2.
The ordinary reduction and exact determinant certificate are in
DENSE_REGULAR_CONES.md. Construction functions do not replace that proof.
"""
from fractions import Fraction as F
import certificates as base
from maxrank_mixtures import integer_at_least, repaired_core


def parameters(h,d):
    integer_at_least(h,4,"h")
    integer_at_least(d,2,"d")
    if not h <= 2*d or d > h-2:
        raise ValueError("Requires h/2 <= d <= h-2")
    return dict(alpha=F(h-d,d),q=F(2,d),
                w=F(2*(d-1),d*(h-2)),
                z=F(2*(2*d-h),d*(h-4)+2))


def normalize(h,edges):
    integer_at_least(h,4,"h")
    pairs=[]
    degrees=[0]*h
    for pair in edges:
        if len(pair)!=2:
            raise ValueError("Every leaf edge must have two endpoints")
        i,j=pair
        if any(not isinstance(v,int) or isinstance(v,bool) or not 0<=v<h
               for v in (i,j)) or i==j:
            raise ValueError("Invalid leaf edge")
        edge=tuple(sorted((i,j)))
        if edge in pairs:
            raise ValueError("Repeated leaf edge")
        pairs.append(edge)
        degrees[i]+=1;degrees[j]+=1
    d=degrees[0]
    if any(a!=d for a in degrees):
        raise ValueError("Leaf graph must be regular")
    parameters(h,d)
    return sorted(pairs),d


def family(h,edges,shift=0):
    pairs,_=normalize(h,edges)
    integer_at_least(shift,0,"shift")
    center=1 << h
    members=[0,center]+[1 << i for i in range(h)]
    members += [center|(1 << i) for i in range(h)]
    members += [(1 << i)|(1 << j) for i,j in pairs]
    return sorted(a << shift for a in members)


def core(h,edges):
    pairs,d=normalize(h,edges)
    weights=parameters(h,d);present=set(pairs)
    center=1 << h
    members=family(h,pairs)[1:]
    def kind(a):
        return "a" if a==center else "c" if a.bit_count()==1 else "x" if a & center else "e"
    def leaf(a):
        return (a ^ center if a & center else a).bit_length()-1
    answer=[]
    for a in members:
        row=[]
        for b in members:
            types="".join(sorted((kind(a),kind(b))))
            if a==b:value=F(h)
            elif a & b:value=F(-1)
            elif types=="ac":value=F(-1)
            elif types=="ae":value=weights["q"]
            elif types=="cc":
                value=-weights["alpha"] if tuple(sorted((leaf(a),leaf(b)))) in present else F(0)
            elif types=="cx":
                value=F(2,d) if tuple(sorted((leaf(a),leaf(b)))) in present else F(0)
            elif types=="ce":value=F(0)
            elif types=="ex":value=weights["w"]
            elif types=="ee":value=weights["z"]
            else:raise ValueError("Uncovered nonempty disjoint pair type")
            row.append(value)
        answer.append(row)
    return answer


def colors(h,edges):
    members=family(h,edges)[1:];s=h+1
    answer=[]
    for a in members:
        vertices=[i for i in range(s) if a & (1 << i)]
        answer.append((2*vertices[0] if len(vertices)==1 else sum(vertices)) % s)
    return answer


def centered_certificate(h,edges,shift=0):
    return family(h,edges,shift),base.lift(core(h,edges),h+1),h+1


def certificate(h,edges,shift=0):
    repaired,_=repaired_core(core(h,edges),colors(h,edges),h+1)
    return family(h,edges,shift),base.lift(repaired,h+1),h+1
