"""Join two complete pointed links along a high through-codegree pair."""
from itertools import combinations,permutations,product
from collections import Counter,defaultdict
import json,time,argparse

def points(mask,n=12):return tuple(i for i in range(n) if mask>>i&1)
def move(mask,action):return sum(1<<action[i] for i in range(11) if mask>>i&1)

def joins(root,all_templates):
    p=11
    a0=tuple(x|(1<<p) for x in root['a'])
    b0=tuple(x|(1<<p) for x in root['b'])
    deg=[(sum(r>>q&1 for r in a0),sum(r>>q&1 for r in b0)) for q in range(11)]
    q=max(range(11),key=lambda q:(deg[q][0],-deg[q][1],-q))
    alpha,beta=deg[q]
    if alpha<3:raise ValueError('completion without a heavy pair')
    target_a=tuple(r&~((1<<p)|(1<<q)) for r in a0 if r>>q&1)
    target_b=tuple(r&~((1<<p)|(1<<q)) for r in b0 if r>>q&1)
    targets=tuple(x for x in range(12) if x not in (p,q))
    triples=tuple(sum(1<<x for x in t) for t in combinations(range(12),3))
    pairs=tuple(sum(1<<x for x in t) for t in combinations(range(12),2))
    results=set();raw=0;compatible=0
    for temp in all_templates:
        for marked in range(11):
            if (sum(r>>marked&1 for r in temp['a']),sum(r>>marked&1 for r in temp['b']))!=(alpha,beta):continue
            source_a=tuple(r&~(1<<marked) for r in temp['a'] if r>>marked&1)
            source_b=tuple(r&~(1<<marked) for r in temp['b'] if r>>marked&1)
            sources=tuple(x for x in range(11) if x!=marked)
            source_groups=defaultdict(list)
            for x in sources:
                signature=sum(1<<i for i,r in enumerate(source_a+source_b) if r>>x&1)
                source_groups[signature].append(x)
            for aa in permutations(target_a):
                for bb in permutations(target_b):
                    target_groups=defaultdict(list)
                    for x in targets:
                        signature=sum(1<<i for i,r in enumerate(aa+bb) if r>>x&1)
                        target_groups[signature].append(x)
                    if {s:len(g) for s,g in source_groups.items()}!={s:len(g) for s,g in target_groups.items()}:continue
                    keys=sorted(source_groups)
                    for images in product(*(permutations(target_groups[s]) for s in keys)):
                        raw+=1
                        mapping=[None]*11;mapping[marked]=p
                        for s,image in zip(keys,images):
                            for x,y in zip(source_groups[s],image):mapping[x]=y
                        aq=tuple(move(r,mapping)|(1<<q) for r in temp['a'])
                        bq=tuple(move(r,mapping)|(1<<q) for r in temp['b'])
                        a=tuple(sorted(set(a0+aq)));b=tuple(sorted(set(b0+bq)))
                        if len(a)!=10-alpha or len(b)!=8-beta:raise ValueError('incorrect overlap count')
                        if any(sum(r>>x&1 for r in a)>5 or sum(r>>x&1 for r in b)>4 for x in range(12)):continue
                        if any(sum(r&t==t for r in a)>2 for t in triples):continue
                        if any(sum(r&t==t for r in a+b)>5 for t in pairs):continue
                        compatible+=1;results.add((a,b))
    return dict(p=p,q=q,alpha=alpha,beta=beta,raw_embeddings=raw,compatible_embeddings=compatible,
                configurations=[dict(a=list(a),b=list(b)) for a,b in sorted(results)])
