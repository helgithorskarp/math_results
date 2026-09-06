#!/usr/bin/env python3
"""Decode a complete primary assignment; target checking is separate in check.py."""
from itertools import combinations
from pathlib import Path
import generate


def values(path):
    result={}
    ended=False
    for line in Path(path).read_text().splitlines():
        if not line.startswith('v '):
            continue
        for x in map(int,line.split()[1:]):
            generate.need(not ended,'model content after terminator')
            if not x:
                ended=True
                continue
            generate.need(1<=abs(x)<=320,'primary model index')
            generate.need(abs(x) not in result or result[abs(x)]==(x>0),'conflicting model')
            result[abs(x)]=x>0
    generate.need(ended and set(result)==set(range(1,321)),'complete terminated primary model')
    return result


def write(log,path):
    model=values(log)
    red=[]
    for e in combinations(range(43),2):
        x=generate.variable(*e)
        value=(x==generate.T) if abs(x)==generate.T else model[x]
        if value:
            red.append(e)
    Path(path).write_text('43\n'+''.join(f'{a} {b}\n' for a,b in red))
    return model


def satisfies(model,cnf):
    with Path(cnf).open() as stream:
        header=stream.readline().split()
        generate.need(header[:3]==['p','cnf','320'],'model CNF header')
        count=0
        for line in stream:
            row=list(map(int,line.split()))
            generate.need(row and row[-1]==0 and all(1<=abs(x)<=320 for x in row[:-1]),'model CNF row')
            generate.need(any(model[abs(x)]==(x>0) for x in row[:-1]),'model fails formula')
            count+=1
        generate.need(count==int(header[3]),'model CNF EOF')
