#!/usr/bin/env python3
"""Standalone physical two-K5 checker; imports no construction or proof code."""
import itertools
import json
import sys


def verify(text,certificate):
    lines=text.splitlines()
    if not lines or len(lines[0].split())!=2: raise ValueError('graph header')
    n,m=map(int,lines[0].split())
    if n!=43 or not 0<=m<=903 or len(lines)!=m+1: raise ValueError('graph size')
    edges=set(); last=(-1,-1)
    for line in lines[1:]:
        pair=tuple(map(int,line.split()))
        if len(pair)!=2: raise ValueError('edge arity')
        u,v=pair
        if not 0<=u<v<n or pair<=last: raise ValueError('edge labels/order')
        edges.add(pair); last=pair
    if type(certificate) is not dict or set(certificate)!={'root','witnesses'}: raise ValueError('certificate fields')
    root=certificate['root']; witnesses=certificate['witnesses']
    if type(root) is not int or not 0<=root<n: raise ValueError('root')
    if type(witnesses) is not list or len(witnesses)!=2: raise ValueError('two witnesses required')
    sets=[]
    for witness in witnesses:
        if type(witness) is not dict or set(witness)!={'vertices','color'}: raise ValueError('witness fields')
        q,c=witness['vertices'],witness['color']
        if type(q) is not list or len(q)!=5 or any(type(v) is not int or not 0<=v<n for v in q) or q!=sorted(set(q)):
            raise ValueError('five labels')
        if type(c) is not int or c not in (0,1): raise ValueError('color')
        if any(int((u,v) in edges)!=c for u,v in itertools.combinations(q,2)): raise ValueError('nonmonochromatic witness')
        sets.append(set(q))
    if not sets[0].intersection(sets[1])<={root}: raise ValueError('witnesses overlap away from root')
    return {'status':'VERIFIED_TWO_PHYSICAL_MONOCHROMATIC_FIVES','n':n,'red_edges':m,
            'colors':[w['color'] for w in witnesses],'intersection':sorted(sets[0]&sets[1])}


if __name__=='__main__':
    with open(sys.argv[1],encoding='utf8') as f: text=f.read()
    with open(sys.argv[2],encoding='utf8') as f: certificate=json.load(f)
    print(json.dumps(verify(text,certificate),sort_keys=True))
