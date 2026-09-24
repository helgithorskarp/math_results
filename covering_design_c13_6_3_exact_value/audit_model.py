"""Independent full marked roots and point-bijection joins."""
from collections import Counter,defaultdict
from itertools import combinations
from catalogue import CAT
from point_maps import invariant,point_maps
CACHE={}
def prepare():
    roots=[];templates=defaultdict(list)
    for d in CAT:
        degrees=[sum(b>>p&1 for b in d['blocks']) for p in range(12)]
        for high in combinations(range(12),3):
            r=max((x for x in range(12) if x not in high),key=lambda x:(degrees[x],-x))
            roots.append(dict(id=len(roots),design=d['id'],high=high,r=r,k=degrees[r]))
        for marked in range(12):
            if degrees[marked] not in (4,5):continue
            through=tuple(b&~(1<<marked) for b in d['blocks'] if b>>marked&1)
            points=tuple(p for p in range(12) if p!=marked)
            templates[invariant(through,points)].append((d['id'],marked,through,points))
    assert len(roots)==23540
    return roots,templates

def uncoloured(design,r,templates):
    cachekey=(design,r)
    if cachekey in CACHE:return CACHE[cachekey]
    for x in list(CACHE):
        if x[0]!=design:del CACHE[x]
    d=CAT[design]
    fixed={b|(1<<12) for b in d['blocks']}
    shared=tuple(b&~(1<<r) for b in d['blocks'] if b>>r&1)
    points=tuple(p for p in range(13) if p not in (r,12))
    unions={};raw=0
    for second,marked,through,spoints in templates[invariant(shared,points)]:
        for mapping in point_maps(through,spoints,shared,points):
            raw+=1;mapping[marked]=12
            star={sum(1<<mapping[p] for p in range(12) if b>>p&1)|(1<<r) for b in CAT[second]['blocks']}
            union=tuple(sorted(fixed|star))
            assert len(union)==18-len(shared)
            if union in unions:assert unions[union]==second
            unions[union]=second
    records=[]
    for union,second in sorted(unions.items()):
        degree=Counter(p for b in union for p in range(13) if b>>p&1)
        pair=Counter(t for b in union for t in combinations([p for p in range(13) if b>>p&1],2))
        records.append((union,second,tuple(degree[p] for p in range(13)),tuple(t for t,n in pair.items() if n>5)))
    CACHE[cachekey]=(records,raw)
    return records,raw

def join(root,templates):
    records,raw=uncoloured(root['design'],root['r'],templates)
    high=set(root['high']);answers=[];normalized=[]
    for union,second,degrees,heavy in records:
        if any(not 0<=(10 if p in high else 9)-degrees[p]<=20-len(union) for p in range(13)):continue
        if any(not set(t)<=high for t in heavy):continue
        answers.append(union)
        if second<=root['design']:normalized.append(union)
    return answers,normalized,raw
