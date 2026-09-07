#!/usr/bin/env python3
"""A classical exact seven-point guard against two scope overextensions."""
from itertools import combinations, product
import json
from pathlib import Path

def cartesian_norm(d):
    a,b,c,e=d
    return (a*a+33*b*b+3*c*c+11*e*e,2*(a*b+c*e))

def tensor_norm(d):
    # z=a+c*r+e*s-b*r*s, r=i sqrt3, s=i sqrt11.
    a,b,c,e=d;x=(a,c,e,-b);y=(a,-c,-e,-b);out=[0]*4
    for i,j in product(range(4),repeat=2):
        factor=(-3 if i&j&1 else 1)*(-11 if i&j&2 else 1)
        out[i^j]+=x[i]*y[j]*factor
    return tuple(out)

def proper(word,n,edges,k):
    if type(word)!=str or len(word)!=n or set(word)-set(map(str,range(k))):
        raise ValueError('bad colour word')
    if any(word[a]==word[b] for a,b in edges):raise ValueError('monochromatic edge')

def verify_guard(data):
    pts=data['points'];cycle=data['cycle_order'];D=data['denominator']
    if data['format']!=1 or D!=12 or len(pts)!=7 or len(set(map(tuple,pts)))!=7:
        raise ValueError('wrong guard geometry')
    if any(len(p)!=4 or any(type(x)!=int for x in p) for p in pts):
        raise ValueError('malformed coordinate')
    if sorted(cycle)!=list(range(7)):raise ValueError('cycle is not spanning')
    strict=[];checks=0
    for a,b in combinations(range(7),2):
        d=tuple(x-y for x,y in zip(pts[a],pts[b]));A,B=cartesian_norm(d)
        if tensor_norm(d)!=(A,0,0,-B):raise ValueError('independent norms disagree')
        checks+=1
        if (A,B)==(D*D,0):strict.append((a,b))
    E={tuple(sorted((cycle[i],cycle[(i+1)%7]))) for i in range(7)}
    if len(E)!=7 or not E<=set(strict) or len(strict)!=11:raise ValueError('wrong cycle/completion')
    proper(data['cycle_three_colouring'],7,E,3)
    proper(data['strict_four_colouring'],7,strict,4)
    cycle3=strict3=0
    for w in product(range(3),repeat=7):
        cycle3+=all(w[a]!=w[b] for a,b in E)
        strict3+=all(w[a]!=w[b] for a,b in strict)
    strict4=sum(all(w[a]!=w[b] for a,b in strict) for w in product(range(4),repeat=7))
    if (cycle3,strict3,strict4)!=(126,0,384):raise ValueError('wrong colouring counts')
    # The two unit diamonds each have a forced same-colour apex and opposite tip
    # in every three-colouring. Their union misses exactly the tip-to-tip edge.
    pieces=data['diamond_vertices'];piece_edges=[]
    for p in pieces:
        if len(p)!=4 or len(set(p))!=4 or any(v not in range(7) for v in p):raise ValueError('bad diamond')
        es={e for e in strict if e[0] in p and e[1] in p};piece_edges.append(es)
        if len(es)!=5:raise ValueError('not a unit diamond')
        proper('0120',4,[(p.index(a),p.index(b)) for a,b in es],3)
    missing=set(strict)-set.union(*piece_edges)
    if missing!={(3,6)}:raise ValueError('wrong cross contact')
    degrees=[sum(v in e for e in strict) for v in range(7)]
    if degrees!=[4,3,3,3,3,3,3]:raise ValueError('wrong strict degree sequence')
    return {'verified':True,'points':7,'exact_pair_tests':checks,'independent_norm_agreements':checks,
            'abstract_cayley_cycle_edges':7,'strict_unit_edges':11,'additional_unit_edges':4,
            'cycle_chromatic_number':3,'strict_chromatic_number':4,
            'proper_cycle_three_colourings':cycle3,'proper_strict_three_colourings':strict3,
            'proper_strict_four_colourings':strict4,'exhaustive_colour_words':3**7+4**7,
            'diamond_edges_each':[len(e) for e in piece_edges],'cross_contact':[3,6],
            'strict_degree_sequence':degrees,'new_record_candidate':False,
            'example_is_classical':True}

if __name__=='__main__':
    p=Path(__file__).with_name('scope_guard.json')
    print(json.dumps(verify_guard(json.loads(p.read_text())),indent=2,sort_keys=True))
