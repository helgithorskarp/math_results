"""All free eighteen-cell articulation-growth polyhexes, excluding two-add growth."""
from geometry import DIRS,halo,orientations,holes
SEED = ((-4,4),(-3,3),(-3,4),(-2,1),(-2,2),(-1,1),(-1,2),(0,0),(0,1),(0,2),(1,0),(1,1),(1,2),(1,3),(2,0),(2,2))
def connected(cells):
    todo=set(cells);q=[todo.pop()]
    while q:
        x,y=q.pop()
        for a,b in DIRS:
            p=(x+a,y+b)
            if p in todo:todo.remove(p);q.append(p)
    return not todo

def canonical(cells):return min(orientations(cells))

def growth(seeds,steps):
    shapes={canonical(s) for s in seeds}
    for _ in range(steps):
        shapes={canonical(set(s)|{p}) for s in shapes for p in halo(s)}
    return shapes

def family():
    seeds=[set(SEED)-{p} for p in SEED if not connected(set(SEED)-{p})]
    shapes=growth(seeds,3)
    old={s for s in growth([SEED],2) if not holes(s)}
    return sorted(s for s in shapes-old if connected(s) and not holes(s))
