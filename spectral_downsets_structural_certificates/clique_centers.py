#!/usr/bin/env python3
"""Centered and maximal-rank rational certificates for K_r joined to I_t."""
from fractions import Fraction as F
from itertools import combinations
import certificates as base
from maxrank_mixtures import integer_at_least, repaired_core


def validate(r,t,shift=0):
    integer_at_least(r,3,"r")
    integer_at_least(t,2,"t")
    integer_at_least(shift,0,"shift")


def family(r,t,shift=0):
    validate(r,t,shift)
    members = [0]+[1 << i for i in range(r+t)]
    members += [(1 << i) | (1 << j) for i,j in combinations(range(r),2)]
    members += [(1 << i) | (1 << j) for i in range(r) for j in range(r,r+t)]
    return sorted(a << shift for a in members)


def parameters(r,t):
    validate(r,t)
    if t >= r-1:
        return dict(alpha=F(0),q=F(0),eta=F(0),p=F(-(r-1),t),
                    beta=-1+F(r*(r-3)*(t-r+1),2*t*(t-1)),
                    u=F(t-r+3,t),v=F(1,t),w=F(2,t),
                    h=F((r-2)*(r-1-t),t*(t-1)),
                    z=F(2*t-2*r+3,t*(t-1)))
    delta = F(t*(t-1),r-1+t*(t-1))
    q = F(2*(r-1-t),(r-1)*(r-2))
    return dict(alpha=-1+delta,q=q,eta=q,p=F(-1),beta=F(-1),
                u=F(2,r-1),v=F(2,r-1)-delta/t,w=F(2,r-1),
                h=F(0),z=delta/(t*(t-1)))


def core(r,t):
    weights = parameters(r,t)
    center_mask = (1 << r)-1
    def kind(a):
        if a.bit_count() == 1:
            return "A" if a & center_mask else "C"
        return "E" if (a & center_mask) == a else "X"
    members = family(r,t)[1:]
    answer = []
    for a in members:
        row = []
        for b in members:
            if a == b:
                value = F(r+t-1)
            elif a & b:
                value = F(-1)
            else:
                types = "".join(sorted((kind(a),kind(b))))
                key = {"AA":"alpha","AC":"p","CC":"beta","AE":"q",
                       "CE":"u","AX":"v","EE":"eta","EX":"w",
                       "CX":"h","XX":"z"}[types]
                value = weights[key]
            row.append(value)
        answer.append(row)
    return answer


def centered_certificate(r,t,shift=0):
    return family(r,t,shift),base.lift(core(r,t),r+t),r+t


def unbalance_if_needed(members,colors,s,leaf):
    """From a proper partition, use a nonsaturated leaf to break equal sizes."""
    counts = [colors.count(c) for c in range(s)]
    if min(counts) != max(counts):
        return colors[:]
    used = {c for a,c in zip(members,colors) if a & leaf}
    available = [c for c in range(s) if c not in used]
    if not available or leaf not in members:
        raise ValueError("No available leaf singleton recoloring")
    answer = colors[:]
    answer[members.index(leaf)] = available[0]
    return answer


def colors(r,t):
    validate(r,t)
    s = r+t
    members = family(r,t)[1:]
    assignment = []
    for a in members:
        vertices = [i for i in range(s) if a & (1 << i)]
        assignment.append((2*vertices[0] if len(vertices)==1 else sum(vertices)) % s)
    return unbalance_if_needed(members,assignment,s,1 << r)


def certificate(r,t,shift=0):
    members = family(r,t,shift)
    repaired,_ = repaired_core(core(r,t),colors(r,t),r+t)
    return members,base.lift(repaired,r+t),r+t
