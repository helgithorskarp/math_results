"""Every free hole-free one-cell graft of a specified seventeen-cell seed."""
from geometry import canonical,halo,holes,orientations

S16=((-4,4),(-3,3),(-3,4),(-2,1),(-2,2),(-1,1),(-1,2),(0,0),(0,1),(0,2),
     (1,0),(1,1),(1,2),(1,3),(2,0),(2,2))
ARTICULATIONS=((-3,3),(-2,2),(1,2))

def grafts(seed):
    seed=set(seed)
    return tuple(sorted({canonical(seed|{p}) for p in halo(seed) if not holes(seed|{p})}))

def embeds(query,target):
    target_set=set(target)
    for o in orientations(query):
        a,b=min(o)
        for x,y in target:
            if all((u+x-a,v+y-b) in target_set for u,v in o):return True
    return False

def earlier_family_overlap(family):
    remainders=[set(S16)-{p} for p in ARTICULATIONS]
    return [i for i,t in enumerate(family) if embeds(S16,t) or any(embeds(r,t) for r in remainders)]
