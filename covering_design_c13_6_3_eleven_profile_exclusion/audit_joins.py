"""Independent point-bijection joins, retaining every marked-point choice."""
from collections import Counter,defaultdict
from itertools import combinations
from hashlib import sha256
import json
from catalogue import CAT

def digest(configurations):return sha256(json.dumps(sorted(configurations),separators=(',',':')).encode()).hexdigest()

def invariant(rows,points):
    return (len(rows),tuple(sorted(sum(b>>p&1 for b in rows) for p in points)),
            tuple(sorted((a&b).bit_count() for a,b in combinations(rows,2))),
            tuple(sorted((a&b&c).bit_count() for a,b,c in combinations(rows,3))))

def point_maps(source,spoints,target,tpoints):
    sd={p:sum(b>>p&1 for b in source) for p in spoints}
    td={p:sum(b>>p&1 for b in target) for p in tpoints}
    if Counter(sd.values())!=Counter(td.values()):return
    options={p:tuple(q for q in tpoints if sd[p]==td[q]) for p in spoints}
    order=sorted(spoints,key=lambda p:(len(options[p]),-sd[p],p))
    patterns=[]
    for depth in range(1,len(order)+1):
        patterns.append(tuple(sorted(sum(1<<i for i,p in enumerate(order[:depth]) if b>>p&1) for b in source)))
    mapping={}
    def visit(depth,used,images):
        if depth==len(order):yield dict(mapping);return
        p=order[depth]
        for q in options[p]:
            if used>>q&1:continue
            new=tuple(v|((1<<depth) if b>>q&1 else 0) for b,v in zip(target,images))
            if tuple(sorted(new))!=patterns[depth]:continue
            mapping[p]=q
            yield from visit(depth+1,used|(1<<q),new)
            del mapping[p]
    yield from visit(0,0,(0,)*len(target))

def prepare():
    roots=[];templates=defaultdict(list)
    for d in CAT:
        degrees=[sum(b>>p&1 for b in d['blocks']) for p in range(12)]
        for h in range(12):
            if degrees[h]!=5:continue
            for q in range(12):
                if q==h:continue
                r=max((x for x in range(12) if x not in (h,q)),key=lambda x:(degrees[x],-x))
                roots.append(dict(id=len(roots),design=d['id'],h=h,q=q,r=r,k=degrees[r]))
        for marked in range(12):
            if degrees[marked] not in (4,5):continue
            through=tuple(b&~(1<<marked) for b in d['blocks'] if b>>marked&1)
            points=tuple(p for p in range(12) if p!=marked)
            templates[invariant(through,points)].append((d['id'],marked,through,points))
    return roots,templates

JOIN_CACHE={}

def join(root,templates):
    d=CAT[root['design']];h,q,r=(root[n] for n in ('h','q','r'))
    fixed={b|(1<<12) for b in d['blocks']}
    shared=tuple(b&~(1<<r) for b in d['blocks'] if b>>r&1)
    points=tuple(p for p in range(13) if p not in (r,12))
    cachekey=(root['design'],r)
    if cachekey not in JOIN_CACHE:
        # The uncoloured joins do not depend on which points are h and q.
        # Limit retained data to the current first-link design.
        for key in list(JOIN_CACHE):
            if key[0]!=root['design']:del JOIN_CACHE[key]
        all_unions=set();raw=0
        for design,marked,through,spoints in templates[invariant(shared,points)]:
            for mapping in point_maps(through,spoints,shared,points):
                raw+=1;mapping[marked]=12
                second={sum(1<<mapping[p] for p in range(12) if b>>p&1)|(1<<r) for b in CAT[design]['blocks']}
                union=tuple(sorted(fixed|second))
                if len(union)!=18-root['k']:raise ValueError('bad common-block identification')
                all_unions.add(union)
        records=[]
        for union in sorted(all_unions):
            degrees=Counter(p for b in union for p in range(13) if b>>p&1)
            pair=Counter(t for b in union for t in combinations([p for p in range(13) if b>>p&1],2))
            records.append((union,tuple(degrees[p] for p in range(13)),tuple(t for t,n in pair.items() if n>5)))
        JOIN_CACHE[cachekey]=(records,raw)
    records,raw=JOIN_CACHE[cachekey];answers=set()
    for union,degrees,heavy in records:
        if any(not 0<=(11 if p==h else 10 if p==q else 9)-degrees[p]<=20-len(union) for p in range(13)):continue
        if any(set(t)!={h,q} for t in heavy):continue
        answers.add(union)
    return sorted(answers),raw
