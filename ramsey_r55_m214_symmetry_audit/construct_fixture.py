#!/usr/bin/env python3
"""Construct the sharp degree/incidence fixture; it contains a blue K5."""
from itertools import combinations

def construct():
    # Z/13Z, acted on by multiplication by 3. Its four nonzero orbits
    # label the first four rotating triples; 0 labels fixed vertex 36.
    unused=set(range(1,13)); orbits=[]
    while unused:
        a=min(unused); orbit=(a,3*a%13,9*a%13)
        orbits.append(orbit);unused.difference_update(orbit)
    residues=[x for orbit in orbits for x in orbit]
    value={v:x for v,x in enumerate(residues)};value[36]=0
    quadratic={x*x%13 for x in range(1,13)}
    E=set(range(12))|{36};red=set()
    def add(a,b):
        if a == b:
            raise ValueError("loop in construction")
        red.add(tuple(sorted((a,b))))
    for a,b in combinations(sorted(E),2):
        if (value[b]-value[a])%13 in quadratic:add(a,b)
    # Six fixed central vertices correspond to the pairs of four E-orbits.
    fixed_pairs=list(combinations(range(4),2))
    for h,pair in enumerate(fixed_pairs):
        for i in pair:
            for s in range(3):add(3*i+s,37+h)
    for h in (0,5):add(36,37+h)
    # Eight rotating central triples. In each block, red offset 0 is always
    # present. A balanced 4x8 matrix selects the blocks with an extra offset.
    for j in range(8):
        if j<4:
            for t in range(3):add(36,12+3*j+t)
        for i in range(4):
            extra=(i==j) if j<4 else (i in ((j-4)%4,(j-3)%4))
            for s in range(3):
                add(3*i+s,12+3*j+s)
                if extra:add(3*i+s,12+3*j+(s+1)%3)
    # A 12-regular circulant on Z/24Z; adding 8 induces the same rotation.
    moving=[12+3*j+s for s in range(3) for j in range(8)]
    for u,v in combinations(range(24),2):
        if min((v-u)%24,(u-v)%24)<=6:add(moving[u],moving[v])
    # Central moving/fixed incidences: each triple sees three fixed vertices,
    # while every fixed vertex sees four triples (twelve vertices).
    for j in range(8):
        neighbors={(j+t)%6 for t in range(3)} if j<6 else set(range(3*(j-6),3*(j-5)))
        for h in neighbors:
            for s in range(3):add(12+3*j+s,37+h)
    # K_3,3 minus one edge gives degree 2 at fixed vertices 37 and 42.
    for h in range(3):
        for k in range(3,6):
            if (h,k)!=(0,5):add(37+h,37+k)
    return E,red
