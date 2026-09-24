"""Complete shared-row identifications for point links."""
from collections import defaultdict
from itertools import combinations,permutations,product
from catalogue import CAT
P=12
PAIRLIST=list(combinations(range(13),2))
PAIRINDEX={p:i for i,p in enumerate(PAIRLIST)}
ALLBLOCKS=[sum(1<<x for x in t) for t in combinations(range(13),6)]
BITS={b:tuple(x for x in range(13) if b>>x&1) for b in ALLBLOCKS}
PAIRS={b:tuple(PAIRINDEX[t] for t in combinations(BITS[b],2)) for b in ALLBLOCKS}
def columns(rows,vertices):
    return tuple(sum(1<<i for i,b in enumerate(rows) if b>>p&1) for p in vertices)

def key(rows,vertices):
    cols=columns(rows,vertices);k=len(rows)
    return min(tuple(sorted(sum(1<<perm[i] for i in range(k) if m>>i&1) for m in cols)) for perm in permutations(range(k)))

def embeddings(source,target_rows,target_vertices):
    source_groups=defaultdict(list)
    for p,c in zip(source['vertices'],columns(source['through'],source['vertices'])):source_groups[c].append(p)
    sizes={m:len(v) for m,v in source_groups.items()}
    keys=sorted(source_groups)
    for target_order in permutations(target_rows):
        target_groups=defaultdict(list)
        for p,c in zip(target_vertices,columns(target_order,target_vertices)):target_groups[c].append(p)
        if sizes!={m:len(v) for m,v in target_groups.items()}:continue
        for choices in product(*(permutations(target_groups[m]) for m in keys)):
            action=[None]*12;action[source['marked']]=P
            for m,images in zip(keys,choices):
                for old,new in zip(source_groups[m],images):action[old]=new
            yield action

def pointed_templates():
    templates=defaultdict(list)
    for d in CAT:
        for orbit in d['point_orbits']:
            marked=orbit[0];k=d['point_signatures'][marked].bit_count()
            if k not in (4,5):continue
            through=tuple(b&~(1<<marked) for b in d['blocks'] if b>>marked&1)
            vertices=tuple(x for x in range(12) if x!=marked)
            templates[(k,key(through,vertices))].append(dict(design=d['id'],marked=marked,through=through,vertices=vertices,blocks=d['blocks']))
    return templates
