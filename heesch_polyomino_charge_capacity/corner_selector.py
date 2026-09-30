"""Necessary simultaneous isolated-quadrant cover of fixed integral copies."""
import itertools
from atlas import BASE
from corners import choices,footprint,isolated_gaps,normalize,variants,vertices,QUADRANTS

def corner_formula(tile,codes):
    shapes=variants(tile);fixed=[];occupied=set();required=set()
    for i,x,y in codes:
        sq=footprint(shapes[i],(x,y))
        if occupied&sq:raise ValueError('overlapping fixed copies')
        fixed.append(sq);occupied.update(sq);required.update(vertices(sq))
    targets=sorted({(v[0]+QUADRANTS[q][0],v[1]+QUADRANTS[q][1])
                    for v in required for q in isolated_gaps(v,occupied)})
    candidates={}
    for target in targets:
        for shape,translation,square in choices(shapes,target,occupied):
            candidates[(shapes.index(shape),*translation)]=square
    codes=sorted(candidates);squares=[candidates[q] for q in codes];owners={}
    for i,square in enumerate(squares,1):
        for p in square:owners.setdefault(p,[]).append(i)
    clauses=[owners.get(p,[]) for p in targets]
    conflicts=sorted({(a,b) for zs in owners.values() for a,b in itertools.combinations(zs,2)})
    clauses.extend([-a,-b] for a,b in conflicts)
    return codes,squares,targets,clauses
