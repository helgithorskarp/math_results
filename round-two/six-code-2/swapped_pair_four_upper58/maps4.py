"""Actual multiplicity-four exchanged-pair maps, two finite generators.

six-code-2, researcher. Complete exchanged-pair carrier; completion proof is in PROOF.md.
"""
from collections import Counter
from itertools import combinations, permutations, product
from pathlib import Path
import sys
import time
from bootstrap import ensure_runtime
ensure_runtime()
from carrier import check_code, image, mask, matching, normalize, require


def common(quads,mate):
    tails=tuple(sorted(tuple(v for v in q if v!=mate) for q in quads if mate in q))
    require(len(tails)==4 and all(len(t)==3 for t in tails) and
            len({v for t in tails for v in t})==12,'four disjoint common tails')
    left=tuple(sorted(set(range(18))-{17,mate}-{v for t in tails for v in t}))
    require(len(left)==4,'four complement points')
    return tails,left


def check_map(g,tails,left,mate):
    require(sorted(g)==list(range(18)) and all(g[g[v]]==v for v in range(18)) and
            sum(g[v]==v for v in range(18))==2 and g[17]==mate and g[mate]==17,
            'actual swapped2^8*1^2 permutation')
    require({frozenset(g[v] for v in t) for t in tails}=={frozenset(t) for t in tails}
            and set(g[v] for v in left)==set(left),'common-tail/complement action')
    fixed=sum({g[v] for v in t}==set(t) for t in tails)
    require(fixed in (0,2),'zero or two fixed common tails')
    return fixed


def pair(g,a,b):
    require(g[a]==g[b]==-1 and a!=b,'unassigned transposition')
    g[a],g[b]=b,a


def tail_maps(quads,mate):
    tails,left=common(quads,mate);out=[];counts=Counter()
    # No fixed tail: four tails exchanged in pairs; complement has two fixed points.
    for pairs in matching(tuple(range(4))):
        for targets in product(*(tuple(permutations(tails[b])) for a,b in pairs)):
            for a,b in combinations(left,2):
                g=[-1]*18;pair(g,17,mate);pair(g,a,b)
                for v in left:
                    if g[v]==-1:g[v]=v
                for (i,j),target in zip(pairs,targets):
                    for v,w in zip(tails[i],target):pair(g,v,w)
                counts[check_map(g,tails,left,mate)]+=1;out.append(tuple(g))
    # Two fixed tails each supply one fixed vertex; complement has two transpositions.
    for fixed_tails in combinations(range(4),2):
        other=tuple(i for i in range(4) if i not in fixed_tails);a,b=other
        for fixed_vertices in product(*(tails[i] for i in fixed_tails)):
            for target in permutations(tails[b]):
                for left_pairs in matching(left):
                    g=[-1]*18;pair(g,17,mate)
                    for i,v in zip(fixed_tails,fixed_vertices):
                        g[v]=v;unfixed=tuple(w for w in tails[i] if w!=v);pair(g,*unfixed)
                    for v,w in zip(tails[a],target):pair(g,v,w)
                    for v,w in left_pairs:pair(g,v,w)
                    counts[check_map(g,tails,left,mate)]+=1;out.append(tuple(g))
    require(len(out)==len(set(out))==1620 and counts=={0:648,2:972},'tail case count')
    return tuple(sorted(out))


def point_maps(quads,mate,node_cap=100000,seconds=5):
    """All two-fixed-point choices, point matching and block-image domains."""
    require(0<=node_cap<=100000 and 0<seconds<=5,'fixed operational guards')
    tails,left=common(quads,mate)
    block_of={v:i for i,t in enumerate(tails) for v in t};block_of.update({v:4 for v in left})
    out=[];nodes=0;started=time.monotonic()
    for fixed_vertices in combinations(sorted(block_of),2):
        # A fixed three-tail has an odd number of fixed points, hence exactly one here.
        if any(sum(v in t for v in fixed_vertices)==2 for t in tails):continue
        g=[-1]*18;pair(g,17,mate)
        partners={4:4}
        for v in fixed_vertices:
            g[v]=v;partners[block_of[v]]=block_of[v]
        def visit():
            nonlocal nodes
            nodes+=1
            if nodes>node_cap or time.monotonic()-started>seconds:
                raise TimeoutError('INCOMPLETE point-map100000/5s guard')
            remaining=tuple(v for v in sorted(block_of) if g[v]==-1)
            if not remaining:
                check_map(g,tails,left,mate);out.append(tuple(g));return
            a=min(remaining,key=lambda v:(0 if block_of[v] in partners else 1,v));ia=block_of[a]
            for b in remaining:
                if a==b:continue
                ib=block_of[b]
                if ia in partners and partners[ia]!=ib or ib in partners and partners[ib]!=ia:continue
                if ia==ib and ia not in partners:continue
                new=ia not in partners
                if new:partners[ia],partners[ib]=ib,ia
                pair(g,a,b);visit();g[a],g[b]=-1,-1
                if new:del partners[ia];del partners[ib]
        visit()
    require(len(out)==len(set(out))==1620,'point carrier count/uniqueness')
    return tuple(sorted(out)),nodes


def anchor(quads,mate,g):
    star=tuple(mask(q)|(1<<17) for q in quads)
    private=tuple(w for w in star if not w>>mate&1)
    moved=tuple(image(w,g) for w in private)
    if any((a&b).bit_count()>2 for a in private for b in moved):return None
    words=tuple(sorted(set(star)|{image(w,g) for w in star}))
    degrees=check_code(words,g)
    require(len(words)==36 and degrees[17]==degrees[mate]==20 and
            sum(w>>17&1 and w>>mate&1 for w in words)==4,'complete lambda4 star union')
    return words
