#!/usr/bin/env python3
"""Check literal input family and physical five-set; import no producer/extractor."""
from itertools import combinations
import json


def verify(data,cert):
    def need(ok,msg):
        if not ok:raise ValueError(msg)
    need(type(data.get('n')) is int and data['n']==43,'order')
    ids=data.get('core_embedding');orientation=data.get('core_color')
    need(isinstance(ids,list) and len(ids)==24 and all(type(v) is int and 0<=v<43 for v in ids) and len(set(ids))==24,'embedding')
    need(type(orientation) is int and orientation in (0,1),'orientation')
    need(isinstance(data.get('red_edges'),list),'edge list')
    edges=set()
    for e in data['red_edges']:
        need(isinstance(e,list) and len(e)==2 and all(type(v) is int for v in e),'edge syntax')
        u,v=e;need(0<=u<v<43 and (u,v) not in edges,'edge identity');edges.add((u,v))
    cycle={frozenset((0,1)),frozenset((1,2)),frozenset((2,3)),frozenset((3,4)),frozenset((0,4))}
    for u,v in combinations(range(24),2):
        bu,bv=u//5,v//5
        expected=frozenset((u%5,v%5)) in cycle if bu==bv else frozenset((bu,bv)) in cycle
        physical=tuple(sorted((ids[u],ids[v]))) in edges
        need(physical==(bool(orientation) if expected else not bool(orientation)),'core pair')
    need(cert.get('schema')==1,'certificate schema')
    five=cert.get('five');color=cert.get('color')
    need(isinstance(five,list) and len(five)==5 and all(type(v) is int and 0<=v<43 for v in five) and len(set(five))==5,'five distinct physical vertices')
    need(type(color) is int and color in (0,1),'witness color')
    need(all((tuple(sorted((u,v))) in edges)==bool(color) for u,v in combinations(five,2)),'literal five-set pairs')
    mechanism=cert.get('mechanism');in_core=sum(v in ids for v in five)
    need((mechanism=='one_vertex_attachment' and in_core==4) or (mechanism=='outside_four' and in_core==1),'mechanism scope')
    return {'status':'VERIFIED_PHYSICAL_MONOCHROMATIC_FIVE','five':five,'color':color,'mechanism':mechanism,'pairs_checked':10}

if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('graph');p.add_argument('certificate');args=p.parse_args()
    print(json.dumps(verify(json.load(open(args.graph)),json.load(open(args.certificate))),indent=2))
