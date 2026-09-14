#!/usr/bin/env python3
"""Solver-free, exact verification of one complete 507-point strict graph."""
import hashlib
import json
from math import gcd
from pathlib import Path

HERE = Path(__file__).resolve().parent
RADICANDS = (1, 3, 5, 15, 11, 33, 55, 165)
SCALE = 288

def require(ok, message):
    if not ok:
        raise ValueError(message)

def validate_payload(points, word):
    require(len(points) == 507, 'point count')
    require(all(len(p) == 16 and all(type(x) is int for x in p) for p in points), 'exact coordinates')
    require(points == sorted(points) and len(set(points)) == len(points), 'canonical distinct points')
    require(len(word) == len(points) and all(c in '0123' for c in word), 'four-colour word')

def norm_coefficients(p, q):
    # Independent sparse radical expansion: sqrt(a)*sqrt(b)=gcd(a,b)*sqrt(ab/gcd(a,b)^2).
    out = {}
    for offset in (0,8):
        terms = [(RADICANDS[i],p[offset+i]-q[offset+i]) for i in range(8) if p[offset+i]!=q[offset+i]]
        for a,x in terms:
            for b,y in terms:
                g=gcd(a,b)
                k=a*b//(g*g)
                out[k]=out.get(k,0)+g*x*y
    return {a:x for a,x in out.items() if x}

def is_unit(p,q):
    return norm_coefficients(p,q)=={1:SCALE*SCALE}

def check_word(edges, word):
    require(all(word[u]!=word[v] for u,v in edges), 'monochromatic physical unit edge')

def compute():
    manifest=json.loads((HERE/'inputs.json').read_text())
    for name,key in [('points.json','points_sha256'),('four_colour.txt','colour_sha256')]:
        require(hashlib.sha256((HERE/name).read_bytes()).hexdigest()==manifest[key], 'payload hash: '+name)
    points=[tuple(p) for p in json.loads((HERE/'points.json').read_text())]
    word=(HERE/'four_colour.txt').read_text().strip()
    validate_payload(points,word)
    edges=[(u,v) for u in range(len(points)) for v in range(u+1,len(points)) if is_unit(points[u],points[v])]
    check_word(edges,word)
    bits=(2,3,6,7,10,11,14,15)
    large=[not any(p[k] for k in bits) for p in points]
    counts={'large':0,'small_without_origin':0,'cross':0}
    for u,v in edges:
        counts['large' if large[u] and large[v] else 'small_without_origin' if not large[u] and not large[v] else 'cross']+=1
    result={'all_checks':True,'vertices':len(points),'unit_edges':len(edges),'pair_checks':len(points)*(len(points)-1)//2,
            'large_vertices':sum(large),'nonfixed_vertices':len(points)-sum(large),'edge_partition':counts,
            'edge_sha256':hashlib.sha256((json.dumps(edges,separators=(',',':'))+'\n').encode()).hexdigest(),
            'proper_four_colouring_checked':True,'record_candidate':False,'parent_obstruction_survives':False,
            'claim_scope':'one fixed exact native-frame support; no phase or family exclusion'}
    return result,points,edges,word

if __name__=='__main__':
    result,*_=compute()
    if (HERE/'expected.json').exists():
        require(result==json.loads((HERE/'expected.json').read_text()), 'expected exact result')
    print(json.dumps(result,sort_keys=True))
