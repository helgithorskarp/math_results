"""Independent point-bijection enumeration through projected row multisets."""
from collections import Counter
from itertools import combinations
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
