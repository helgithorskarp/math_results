"""Independently join links by backtracking point bijections, without cell maps."""
from itertools import combinations
from collections import Counter
import json,time

def members(mask,n=12):return tuple(p for p in range(n) if mask&(1<<p))

def point_maps(source_a,source_b,target_a,target_b,source_points,target_points):
    source=source_a+source_b;target=target_a+target_b
    sa=len(source_a);ta=len(target_a)
    sd={p:(sum(p in e for e in source_a),sum(p in e for e in source_b)) for p in source_points}
    td={p:(sum(p in e for e in target_a),sum(p in e for e in target_b)) for p in target_points}
    if Counter(sd.values())!=Counter(td.values()):return
    options={p:tuple(q for q in target_points if sd[p]==td[q]) for p in source_points}
    order=sorted(source_points,key=lambda p:(len(options[p]),-sum(sd[p]),p))
    mapping={};used=set()
    def search(depth):
        if depth==len(order):
            yield dict(mapping);return
        p=order[depth]
        for q in options[p]:
            if q in used:continue
            mapping[p]=q;used.add(q)
            valid=True
            for i,e in enumerate(source):
                family=target[:ta] if i<sa else target[ta:]
                if not any(all((x in e)==(y in f) for x,y in mapping.items()) for f in family):
                    valid=False;break
            if valid:yield from search(depth+1)
            used.remove(q);del mapping[p]
    yield from search(0)

def check_union(a,b):
    da=Counter(p for r in a for p in members(r));db=Counter(p for r in b for p in members(r))
    if max(da.values())>5 or max(db.values())>4:return False
    triples=Counter(t for r in a for t in combinations(members(r),3))
    if max(triples.values())>2:return False
    pairs=Counter(t for r in a+b for t in combinations(members(r),2))
    return max(pairs.values())<=5
