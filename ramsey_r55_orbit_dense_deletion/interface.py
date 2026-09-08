#!/usr/bin/env python3
"""Certify supplied automorphisms and extract a literal bad five in a 43-set.

No claim is made that supplied generators give the full automorphism group.
"""
import argparse,json
from collections import deque
from fractions import Fraction
from itertools import combinations
from pathlib import Path


def need(ok, message):
    if not ok:
        raise ValueError(message)


def validate(data):
    n = data['n'];need(type(n) is int and 46 <= n <= 53, 'ambient order')
    edges = data['red_edges'];seen=set();adj=[0]*n
    for edge in edges:
        need(isinstance(edge,list) and len(edge)==2, 'edge pair')
        u,v=edge;need(type(u) is int and type(v) is int and 0 <= u < v < n, 'edge endpoints')
        need((u,v) not in seen, 'duplicate edge');seen.add((u,v));adj[u]|=1<<v;adj[v]|=1<<u
    selected = data['selected']
    need(isinstance(selected,list) and len(selected)==43 and all(type(v) is int and 0<=v<n for v in selected)
         and selected==sorted(set(selected)), 'selected 43-set')
    generators=data['generators'];need(isinstance(generators,list) and generators, 'generators')
    for permutation in generators:
        need(isinstance(permutation,list) and len(permutation)==n and all(type(v) is int for v in permutation)
             and sorted(permutation)==list(range(n)), 'generator permutation')
        for u,v in combinations(range(n),2):
            need(bool(adj[u]>>v&1)==bool(adj[permutation[u]]>>permutation[v]&1), 'generator is not automorphism')
    remaining=set(range(n));orbits=[]
    while remaining:
        orbit={min(remaining)};queue=list(orbit)
        for v in queue:
            for p in generators:
                if p[v] not in orbit:orbit.add(p[v]);queue.append(p[v])
        orbits.append(sorted(orbit));remaining-=orbit
    return adj,orbits


def find_five(adj):
    # A seed exists throughout the declared range by R(5,5)<=46. For the
    # concrete order-53 family even R(4,5)=25 and a degree argument suffice.
    vertices=(1<<len(adj))-1
    def clique(chosen,candidates,color):
        if len(chosen)==5:return chosen
        if candidates.bit_count()<5-len(chosen):return None
        while candidates:
            bit=candidates & -candidates;candidates^=bit;v=bit.bit_length()-1
            neighbors=adj[v] if color else ~adj[v]
            answer=clique(chosen+[v],candidates & neighbors,color)
            if answer is not None:return answer
        return None
    for color in (True,False):
        seed=clique([],vertices,color)
        if seed is not None:return seed,'red' if color else 'blue'
    raise ValueError('no ambient five found; imported Ramsey guarantee failed')


def certify(data):
    adj,orbits=validate(data);selected=set(data['selected']);n=data['n']
    profile=[{'orbit':orbit,'retained':len(selected.intersection(orbit)), 'size':len(orbit)} for orbit in orbits]
    if any(5*row['retained'] <= 4*row['size'] for row in profile):
        return {'status':'OUTSIDE_DECLARED_ORBIT_DENSE_FAMILY','orbit_profile':profile,'ramsey_verdict':None}
    seed,color=find_five(adj)
    deleted=set(range(n))-selected
    mean=sum(Fraction(len(set(seed).intersection(o))*len(deleted.intersection(o)),len(o)) for o in orbits)
    need(mean<1,'strict orbit average')
    start=tuple(seed);queue=deque([start]);predecessor={start:None};word_step={}
    while queue:
        current=queue.popleft()
        if set(current)<=selected:
            word=[];walk=current
            while predecessor[walk] is not None:
                word.append(word_step[walk]);walk=predecessor[walk]
            word.reverse()
            return {'status':'CERTIFIED_MONOCHROMATIC_FIVE_IN_PHYSICAL43', 'ambient_order':n,
                    'orbit_profile':profile,'seed':seed,'color':color,
                    'expected_deleted_intersection':[mean.numerator,mean.denominator],
                    'generator_word':word,'ambient_witness':list(current),
                    'physical_witness':[data['selected'].index(v) for v in current],
                    'visited_five_sets':len(predecessor),'target43_found':False}
        for i,p in enumerate(data['generators']):
            nxt=tuple(sorted(p[v] for v in current))
            if nxt not in predecessor:
                predecessor[nxt]=current;word_step[nxt]=i;queue.append(nxt)
    raise ValueError('orbit avoidance proof failed')


def main():
    parser=argparse.ArgumentParser();parser.add_argument('input');args=parser.parse_args()
    print(json.dumps(certify(json.loads(Path(args.input).read_text())),indent=2,sort_keys=True))


if __name__=='__main__':main()
