"""Exact rational interval controls and a separate 3-colour obstruction check."""
import copy
import json
from fractions import Fraction as F
from itertools import combinations
from math import isqrt
from intervals import I, Q
from seed import HERE, certify, require
from verify import pair_partition, validate_word


def encloses(interval, lo, hi):
    require(F(interval.lo,Q) <= lo <= hi <= F(interval.hi,Q), 'interval containment')


def expect_failure(call):
    try:
        call()
    except ValueError:
        return
    raise ValueError('corrupted control was accepted')


def independent_three_colour_obstruction(edges):
    """G is 3-colourable iff deleting some independent set leaves a bipartite graph."""
    adj=[0]*17
    for u,v in edges:
        adj[u]|=1<<v
        adj[v]|=1<<u
    independent=[False]*(1<<17)
    independent[0]=True
    checked=0
    for mask in range(1<<17):
        if mask:
            bit=mask & -mask
            v=bit.bit_length()-1
            rest=mask^bit
            independent[mask]=independent[rest] and not (adj[v]&rest)
        if not independent[mask]:
            continue
        checked+=1
        colour={}
        bipartite=True
        for start in range(17):
            if mask>>start&1 or start in colour:
                continue
            colour[start]=0
            stack=[start]
            while stack and bipartite:
                u=stack.pop()
                for v in range(17):
                    if not(adj[u]>>v&1) or mask>>v&1:
                        continue
                    if v in colour:
                        if colour[v]==colour[u]:
                            bipartite=False
                            break
                    else:
                        colour[v]=1-colour[u]
                        stack.append(v)
            if not bipartite:
                break
        require(not bipartite, 'independent-set deletion is bipartite')
    return checked


def run():
    fixtures=[]
    for a,b in [(-7,-3),(-2,0),(-1,3),(0,0),(0,1),(1,1),(2,9),(-9,-2)]:
        fixtures.append(I.rational(F(a,7))+I(0,1))
        fixtures.append(I(I.rational(F(a,7)).lo,I.rational(F(b,7)).hi))
    arithmetic=0
    for a in fixtures:
        al,ah=F(a.lo,Q),F(a.hi,Q)
        squares=[al*al,ah*ah]
        encloses(a.square(),0 if al<=0<=ah else min(squares),max(squares))
        if not al<=0<=ah:
            encloses(a.reciprocal(),1/ah,1/al)
        for b in fixtures:
            bl,bh=F(b.lo,Q),F(b.hi,Q)
            encloses(a+b,al+bl,ah+bh)
            encloses(a-b,al-bh,ah-bl)
            products=[x*y for x in (al,ah) for y in (bl,bh)]
            encloses(a*b,min(products),max(products))
            if not bl<=0<=bh:
                quotients=[x/y for x in (al,ah) for y in (bl,bh)]
                encloses(a/b,min(quotients),max(quotients))
            arithmetic+=1
    sqrt_cases=0
    for n in [0,1,2,3,Q-1,Q,Q+1,2*Q,Q*Q-1,Q*Q,Q*Q+1]:
        for width in (0,1,7):
            a=I(n,n+width);s=a.sqrt()
            require(s.lo>=0 and s.lo*s.lo<=n*Q and s.hi*s.hi>=(n+width)*Q,'sqrt enclosure')
            # Also check minimal integer outward endpoints, including exact squares.
            require((s.lo+1)**2>n*Q and (s.hi==0 or (s.hi-1)**2<(n+width)*Q),'sqrt tightness')
            sqrt_cases+=1
    malformed=[lambda:I(1,0),lambda:I('0',1),lambda:I(-1,1).reciprocal(),
               lambda:I(-1,0).sqrt()]
    z,o=I.rational(0),I.rational(1)
    points=[(z,z),(z,z),(o,z)]
    validate_word(points,'001')
    malformed.extend([lambda:validate_word(points,'010'),lambda:validate_word(points,'000'),
                      lambda:validate_word(points,'00'),lambda:validate_word(points,'004')])
    p,_=certify()
    c=json.loads((HERE/'fan_certificate.json').read_text())
    missing=copy.deepcopy(c);missing[0]['pairs'].pop()
    duplicate=copy.deepcopy(c);duplicate[0]['pairs'].append(duplicate[0]['pairs'][0])
    overlap=copy.deepcopy(c);edge=overlap[2]['pairs'].pop();overlap.append(dict(pairs=[edge],word=''))
    malformed.extend([lambda:pair_partition(p,missing),lambda:pair_partition(p,duplicate),
                      lambda:pair_partition(p,overlap)])
    mid=[[F(x) for x in r] for r in json.loads((HERE/'seed_midpoint.json').read_text())]
    mid[0][0]+=F(1,10000)
    malformed.append(lambda:certify(midpoint=mid))
    for call in malformed:
        expect_failure(call)
    edges=json.loads((HERE/'seed_edges.json').read_text())
    sets=independent_three_colour_obstruction(edges)
    return dict(interval_pair_fixtures=arithmetic,square_root_boundary_cases=sqrt_cases,
                malformed_rejected=len(malformed),independent_sets_with_nonbipartite_complement=sets,
                mask_space_exhausted=1<<17,normal_assertions_not_required=True)


if __name__=='__main__':
    print(json.dumps(run(),sort_keys=True,indent=2))
