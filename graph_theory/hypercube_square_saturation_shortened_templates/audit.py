#!/usr/bin/env python3
"""Reconstruct full quotient graphs and audit exact coefficient inequalities.

The quotient audit does not import the certificate checker or constructor.
The separate arithmetic audit imports only the public parameter/bound routines.
"""
from __future__ import annotations
import itertools
import json
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def quotient(t: dict, m: int) -> dict:
    q = 1 << t['k']; Q = q*m
    C, D, T = set(t['C']), set(t['D']), set(t['T'])
    A = C | D
    E = {frozenset(e) for e in t['core_edges']}
    for z in range(1, m):
        for x, centers in enumerate(t['outside_neighbors']):
            E.update(frozenset((a, z*q+x)) for a in centers)
    nb = [set() for _ in range(Q)]
    for e in E:
        a, b = e
        if ((a ^ b) % q) not in T or not (e & A):
            raise RuntimeError('host or cover failure')
        nb[a].add(b); nb[b].add(a)
    for cls in (C, D):
        for x in range(Q):
            if x in cls:
                if nb[x] & cls:
                    raise RuntimeError('independence failed')
            elif not nb[x] & cls:
                raise RuntimeError('domination failed')
    tested = saturated = 0
    for a, b in itertools.combinations(range(Q), 2):
        if ((a ^ b) % q) not in T:
            continue
        tested += 1
        witnesses = [v for u in nb[a] for v in (nb[u] & nb[b])
                     if u != b and v != a and a ^ b ^ u ^ v == 0]
        if b in nb[a]:
            if witnesses:
                raise RuntimeError('affine square')
        elif a in A or b in A:
            saturated += 1
            if not witnesses:
                raise RuntimeError('boundary edge not saturated')
    r0=len(t['core_edges']);r1=sum(map(len,t['outside_neighbors']))
    if len(E) != r0+(m-1)*r1:
        raise RuntimeError('edge formula')
    return {'name':t['name'],'scale':m,'order':Q,'edges':len(E),
            'host_edges_tested':tested,'missing_boundary_edges_checked':saturated}


def arithmetic() -> dict:
    from construct import choose, bound
    tested = 0
    for n in range(14, 4097):
        a,b,r = choose(n)
        if r < 0 or a.length + b.length + r != n:
            raise RuntimeError('bad parameter choice')
        if bound(n,a,b) >= 6 + Fraction(49,n+2):
            raise RuntimeError('uniform bound failure')
        tested += 1
    # Endpoints for the affine leading terms and quadratic completion terms.
    maxima = [Fraction(47,8),Fraction(191,32),Fraction(95,16),
              Fraction(189,32),Fraction(6),Fraction(6)]
    patchmax = [Fraction(729,16),Fraction(375,8),Fraction(363,8),
                Fraction(45),Fraction(49),Fraction(48)]
    endpoint_tests = 0
    for power in range(61):
        m = 1 << power
        for x in (16*m,18*m-1,18*m,20*m-1,20*m,22*m-1,
                  22*m,24*m-1,24*m,28*m-1,28*m,32*m-1):
            a,b,r=choose(x-2)
            if bound(x-2,a,b) >= 6+Fraction(49,x):
                raise RuntimeError('large endpoint failure')
            endpoint_tests += 1
        # The upper endpoints themselves use the preceding interval's pair.
        for j,(x,ta,sa,tb,sb) in enumerate(((18*m,'H',2*m,'H',2*m),
                (20*m,'H',2*m,'F',m),(22*m,'H',2*m,'S',4*m),
                (24*m,'F',m,'S',4*m),(28*m,'S',4*m,'S',4*m),
                (32*m,'S',4*m,'H',4*m))):
            from construct import Block
            a,b=Block(ta,sa),Block(tb,sb)
            leading=Fraction(a.r1,a.q)+Fraction(b.r1,b.q)+(
                a.delta*(x-a.length-1)+b.delta*(x-b.length-1))/4
            if leading!=maxima[j] or x*x*a.delta*b.delta!=patchmax[j]:
                raise RuntimeError('endpoint identity failed')
    return {'consecutive_dimensions_checked':tested,'large_endpoint_checks':endpoint_tests,
            'leading_endpoint_maxima':list(map(str,maxima)),
            'completion_endpoint_maxima':list(map(str,patchmax))}


def main() -> None:
    templates=json.loads((ROOT/'templates.json').read_text())
    qs=[quotient(t,m) for t in templates for m in (1,2,4,8)]
    print(json.dumps({'quotients':qs,'arithmetic':arithmetic()},indent=2,sort_keys=True))


if __name__=='__main__':
    main()
