#!/usr/bin/env python3
"""Find a physical monochromatic five-set in every member of the H24 family."""
from itertools import combinations
import json


def read_graph(data):
    if type(data.get('n')) is not int or data['n']!=43:raise ValueError('requires order43')
    embed=data.get('core_embedding');color=data.get('core_color')
    if type(color) is not int or color not in (0,1):raise ValueError('core_color must be0 or1')
    if not isinstance(embed,list) or len(embed)!=24 or any(type(v) is not int or not 0<=v<43 for v in embed) or len(set(embed))!=24:
        raise ValueError('24 distinct core labels required')
    if not isinstance(data.get('red_edges'),list):raise ValueError('red_edges')
    a=[[False]*43 for _ in range(43)];seen=set()
    for row in data['red_edges']:
        if not isinstance(row,list) or len(row)!=2 or any(type(x) is not int for x in row):raise ValueError('edge format')
        u,v=row
        if not 0<=u<v<43 or (u,v) in seen:raise ValueError('edge bounds/order/duplicate')
        seen.add((u,v));a[u][v]=a[v][u]=True
    for u,v in combinations(range(24),2):
        i,j=divmod(u,5);k,l=divmod(v,5)
        expected=(j-l)%5 in (1,4) if i==k else (i-k)%5 in (1,4)
        if (a[embed[u]][embed[v]]==bool(color))!=expected:raise ValueError('wrong inducedH24')
    return a,embed,color


def extract(data):
    a,embed,color=read_graph(data)
    outside=sorted(set(range(43))-set(embed))
    four=[[],[]]
    for q in combinations(embed,4):
        cols={int(a[u][v]) for u,v in combinations(q,2)}
        if len(cols)==1:four[next(iter(cols))].append(q)
    for x in outside:
        for c in (0,1):
            for q in four[c]:
                if all(a[x][v]==bool(c) for v in q):
                    return {'schema':1,'mechanism':'one_vertex_attachment','color':c,'five':sorted([x,*q])}
    # Complete kernel implies these four incidences for every outside vertex.
    for x in outside:
        if any(a[x][embed[v]]!=bool(color) for v in (20,23)) or any(a[x][embed[v]]==bool(color) for v in (21,22)):
            raise RuntimeError('complete attachment theorem mismatch')
    # R(4,4)<=18 guarantees a monochromatic four-set in the19 outside vertices.
    for q in combinations(outside,4):
        cols={int(a[u][v]) for u,v in combinations(q,2)}
        if len(cols)==1:
            c=next(iter(cols));v=embed[20 if c==color else 21]
            return {'schema':1,'mechanism':'outside_four','color':c,'five':sorted([v,*q])}
    raise RuntimeError('R44 theorem mismatch: no monochromatic four-set')

if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('graph');args=p.parse_args()
    print(json.dumps(extract(json.load(open(args.graph))),indent=2))
