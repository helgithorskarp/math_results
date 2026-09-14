"""Separate primitive-element geometry and interior-first exhaustive relation audit.

No imports from the source model, verifier, or certificate.
"""
from fractions import Fraction as F
from itertools import product,combinations
from hashlib import sha256
import json

def need(ok,message):
    if not ok:raise ValueError(message)
def p(*a):return tuple(map(F,a+(0,)*(4-len(a))))
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def neg(a):return tuple(-x for x in a)
def sub(a,b):return add(a,neg(b))
def scale(a,b):return tuple(x*b for x in a)
def mul(a,b):
    c=[F(0)]*7
    for i in range(4):
        for j in range(4):c[i+j]+=a[i]*b[j]
    # x=i(sqrt(3)+sqrt(11)); x^4+28*x^2+64=0.
    for i in range(6,3,-1):
        c[i-2]-=28*c[i];c[i-4]-=64*c[i]
    return tuple(c[:4])
def conj(a):return tuple((-1)**i*x for i,x in enumerate(a))
def digest(obj):return sha256(json.dumps(obj,separators=(',',':')).encode()).hexdigest()

def audit():
    one=p(1);zero=p(0);x=p(0,1)
    alpha=p(0,F(-5,4),0,F(-1,16))
    beta=p(0,F(9,4),0,F(1,16))
    need(add(alpha,beta)==x and mul(alpha,alpha)==p(-3)
         and mul(beta,beta)==p(-11),'primitive element identities')
    rho=scale(add(one,alpha),F(1,2));t=scale(add(p(5),beta),F(1,6))
    pts=[zero,one,rho,add(one,rho),t,mul(t,rho),mul(t,add(one,rho)),
         conj(rho),scale(rho,2),scale(t,2),mul(t,sub(rho,one))]
    need(len(set(pts))==11,'primitive-element collision check')
    edges=[]
    for a,b in combinations(range(11),2):
        d=sub(pts[a],pts[b])
        if mul(d,conj(d))==one:edges.append((a,b))
    need(len(edges)==19,'primitive-element complete edge count')
    interior=[(a,b) for a,b in edges if b<7]
    neighbors={v:[a for a,b in edges if b==v] for v in range(7,11)}
    relation={};proper=0;full=0;same=set();different=set()
    for w in product(range(4),repeat=7):
        if any(w[a]==w[b] for a,b in interior):continue
        proper+=1
        choices=[sorted(set(range(4))-{w[a] for a in neighbors[v]})
                 for v in range(7,11)]
        for pin in product(*choices):
            full+=1;relation[pin]=relation.get(pin,0)+1
            whole=w+pin
            for a,b in combinations(range(11),2):
                (same if whole[a]==whole[b] else different).add((a,b))
    expected={w for w in product(range(4),repeat=4)
              if w[0]!=w[1] or w[2]!=w[3]}
    need(set(relation)==expected,'interior-first full labelled relation')
    all_pairs=set(combinations(range(11),2))
    need(same==all_pairs-set(edges) and different==all_pairs,
         'every individual two-point relation equals its bare graph relation')
    # Independent full three-colour interior enumeration for chi>=4.
    three=sum(all(w[a]!=w[b] for a,b in interior)
              for w in product(range(3),repeat=7))
    need(three==0,'Moser has no three-colouring')
    return {'status':'PRIMITIVE-ELEMENT AND INTERIOR-FIRST AUDIT PASS',
            'points':11,'strict_unit_edges':len(edges),'all_pairs':55,
            'interior_four_colour_words':proper,'full_four_colour_words':full,
            'labelled_terminal_patterns':len(relation),'interior_three_colour_words':three,
            'same_colour_nonunit_pairs':len(same),'different_colour_pairs':len(different),
            'edge_sha256':digest(edges),'labelled_relation_sha256':digest(sorted(relation)),
            'extension_multiplicity_sha256':digest(sorted(relation.items()))}

if __name__=='__main__':print(json.dumps(audit(),indent=2,sort_keys=True))
