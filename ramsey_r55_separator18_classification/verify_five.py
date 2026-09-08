#!/usr/bin/env python3
"""Definition-level certificate checker: no extractor, Ramsey theorem or catalog."""
import argparse
import json
from itertools import combinations
from pathlib import Path

def check(graph,certificate):
    if type(graph.get('n')) is not int or graph['n']!=43:
        raise ValueError('order43 required')
    word=graph.get('red_hex')
    if not isinstance(word,str) or len(word)!=226 or any(c not in '0123456789abcdef' for c in word) or int(word,16)>=2**903:
        raise ValueError('invalid graph word')
    code=int(word,16)
    edges={pair:bool(code&2**i) for i,pair in enumerate(combinations(range(43),2))}
    q=certificate.get('vertices')
    color=certificate.get('color')
    if not isinstance(q,list) or len(q)!=5 or q!=sorted(set(q)) or any(type(v) is not int or v<0 or v>=43 for v in q) or color not in ('red','blue'):
        raise ValueError('invalid five-set certificate')
    if any(edges[u,v]!=(color=='red') for u,v in combinations(q,2)):
        raise ValueError('five-set is not monochromatic in claimed color')
    return {'status':'VERIFIED_LITERAL_FIVE','pairs_checked':10}

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('graph',type=Path)
    p.add_argument('certificate',type=Path)
    a=p.parse_args()
    print(json.dumps(check(json.loads(a.graph.read_text()),json.loads(a.certificate.read_text())),sort_keys=True))
