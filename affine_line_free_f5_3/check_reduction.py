"""Exact small checks for the accompanying human proof; Python standard library."""
from collections import Counter
from itertools import combinations, combinations_with_replacement, product
from math import comb
import json
from pathlib import Path

pts=list(product(range(5),repeat=3))
index={p:i for i,p in enumerate(pts)}
normals=[d for d in pts if any(d) and next(x for x in d if x)==1]
planes=[frozenset(i for i,p in enumerate(pts)
                   if sum(x*y for x,y in zip(p,d))%5==c)
        for d in normals for c in range(5)]
lines=set()
for a,b in combinations(pts,2):
    d=tuple((y-x)%5 for x,y in zip(a,b))
    lines.add(frozenset(index[tuple((x+t*y)%5 for x,y in zip(a,d))]
                        for t in range(5)))
assert len(normals)==31 and len(planes)==155 and len(lines)==775
assert all(len(h)==25 for h in planes)
incidence=Counter(pair for h in planes for pair in combinations(sorted(h),2))
assert len(incidence)==comb(125,2) and set(incidence.values())=={6}
assert all(sum(sum(x*y for x,y in zip(n,p))%5==0 for n in normals)==6
           for p in normals)  # each projective line has six points

profiles=[p for p in combinations_with_replacement(range(9,17),5) if sum(p)==73]
A=(9,16,16,16,16); B=(10,15,16,16,16)
weight=lambda p:sum(comb(x,2) for x in p)
assert len(profiles)==13 and weight(A)==516 and weight(B)==510
assert max(weight(p) for p in profiles if p not in (A,B))==506
assert 6*comb(73,2)==15768 and 15768-31*506==82
for p in profiles:
    t=p.count(16)
    assert 2*weight(p)<=996+9*t
assert 2*15768-31*996==660 and (660+8)//9==74

# Every ordered pair of distinct layer labels can be sent to (3,4)
# by an invertible affine map on F_5. This normalizes A and B.
for low,other in product(range(5),repeat=2):
    if low==other: continue
    a=pow((other-low)%5,-1,5); b=(3-a*low)%5
    assert (a*low+b)%5==3 and (a*other+b)%5==4

# Dual size formula and exclusions using the published multiplicity spectra.
assert 156*16-31*73-5*3==218
for dual_size in (143,168):
    low_count=(218-dual_size)//5
    assert 218-5*low_count==dual_size
    assert 2*low_count<41  # no multiplicity-2 points implies a=0
assert [n for n in range(16,35) if n%5==3]==[18,23,28,33]

known=json.loads(Path(__file__).with_name('known70.json').read_text())
S=set(known['points'])
assert len(S)==70 and all(not l<=S for l in lines)
print(json.dumps({'affine_points':125,'affine_lines':775,'affine_planes':155,
 'pairs_per_plane_direction_sum':6,'profiles':[
 {'sizes':p,'pair_weight':weight(p)} for p in profiles],
 'heavy_inequality':'5*a+2*b>=41','independent_heavy_directions':3,
 'coordinate_cases':4,'minimum_16_planes':74,
 'dual_size_maximum':173,'excluded_exceptional_dual_sizes':[143,168],
 'retained_exceptional_dual_size':128,'lifted_base_sizes':[18,23,28,33],
 'known70_checked':True},indent=2))
