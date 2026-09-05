#!/usr/bin/env python3
"""Literal edge-orbit meanings and complete prefix/tail checks; no producer."""
from itertools import combinations, product


def need(ok, why):
    if not ok:raise ValueError(why)


def mapping():
    def sigma(v):return 3*(v//3)+(v+1)%3 if v<33 else v
    found={};number=0
    for a,b in combinations(range(33),2):
        if a//3==b//3 or (a,b) in found:continue
        number+=1;pair=(a,b)
        while pair not in found:
            found[pair]=number;pair=tuple(sorted((sigma(pair[0]),sigma(pair[1]))))
    need(number==165,'moving orbits')
    for pair in combinations(range(33,43),2):number+=1;found[pair]=number
    for fixed in range(33,43):
        for i in range(11):
            number+=1
            for phase in range(3):found[3*i+phase,fixed]=number
    need(number==320 and len(found)==870,'complete primary meanings')
    return found


def base_units(bits):
    need(len(bits)==18 and set(bits)<=set('01'),'bits')
    m=mapping();ids=[m[3*i,3*j+p] for i,j in combinations(range(4),2) for p in range(3)]
    return [x if b=='1' else -x for x,b in zip(ids,bits)]+[-m[3*i,33] for i in range(4)]


def split_rows(branch):
    need(branch in ('one','multiple'),'branch')
    m=mapping();ids=[m[3*i,34] for i in range(4)]
    return [ids] if branch=='one' else [[-x] for x in ids]


def check_layer(source, target, source_count, tail):
    with source.open('rb') as f,target.open('rb') as g:
        need(f.readline()==f'p cnf 34280 {source_count}\n'.encode(),'source header')
        need(g.readline()==f'p cnf 34280 {source_count+len(tail)}\n'.encode(),'target header')
        while data:=f.read(1<<20):need(g.read(len(data))==data,'entire inherited prefix')
        for row in tail:need(g.readline()==(' '.join(map(str,row))+' 0\n').encode(),'exact primary tail')
        need(g.read()==b'','trailing extra bytes')


def check_base(parent, base, bits):
    check_layer(parent,base,615920,[[v] for v in base_units(bits)])
    return dict(variables=34280,clauses=615942,primary_variables=320,entire_parent=True,appended_units=22)


def check(base, formula, branch):
    tail=split_rows(branch);check_layer(base,formula,615942,tail)
    return dict(variables=34280,clauses=615942+len(tail),entire_base=True,split_rows=tail)


def split_control():
    def holds(rows, values):
        return all(any(values[abs(x)]==(x>0) for x in row) for row in rows)
    one=split_rows('one');multiple=split_rows('multiple');ids=[mapping()[3*i,34] for i in range(4)]
    for bits in product((False,True),repeat=4):
        values=dict(zip(ids,bits));a=holds(one,values);b=holds(multiple,values)
        need(a==any(bits) and b==(not any(bits)) and a!=b,'complete disjoint prefix partition')
    rows=sorted(product((0,1),repeat=11));prefixes=[r[:4] for r in rows]
    need(prefixes==sorted(prefixes) and prefixes[:128]==[(0,0,0,0)]*128,'prefix ordering')
    return dict(verified=True,assignments=16,full_rows=2048,first_empty_variables=[mapping()[3*i,33] for i in range(4)],
                second_prefix_variables=ids,one_rows=one,multiple_rows=multiple)
