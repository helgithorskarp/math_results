"""Exact corner propagation for integral orthogonal-tile prefixes.

The written angle argument justifies each forcing step for arbitrary real
motions. Failure to propagate is inconclusive; no SAT solver is used here.
"""
from collections import deque

QUADRANTS=((0,0),(-1,0),(-1,-1),(0,-1))  # NE, NW, SW, SE


def cells(raw):
    result=tuple(tuple(p) for p in raw)
    if (not result or len(result)!=len(set(result))
            or any(len(p)!=2 or any(type(x) is not int for x in p) for p in result)):
        raise ValueError('nonempty distinct integer cell pairs required')
    return tuple(sorted(result))


def normalize(raw):
    shape=cells(raw)
    ax=min(x for x,y in shape);ay=min(y for x,y in shape)
    return tuple(sorted((x-ax,y-ay) for x,y in shape))


def image_cell(p,swap,sx,sy):
    x,y=p
    return (sx*(y if swap else x)-(sx==-1),sy*(x if swap else y)-(sy==-1))


def variants(raw):
    shape=cells(raw)
    return tuple(sorted({normalize(image_cell(p,swap,sx,sy) for p in shape)
                         for swap in (False,True) for sx in (-1,1) for sy in (-1,1)}))


def footprint(shape,translation):
    tx,ty=translation
    if type(tx) is not int or type(ty) is not int:
        raise ValueError('integer translation required')
    return frozenset((x+tx,y+ty) for x,y in cells(shape))


def vertices(raw):
    return {(x+dx,y+dy) for x,y in raw for dx in (0,1) for dy in (0,1)}


def disc(raw):
    """Edge connectivity, no diagonal pinches, and no bounded empty component."""
    shape=set(cells(raw));pending=[next(iter(shape))];seen=set(pending)
    while pending:
        x,y=pending.pop()
        for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)):
            p=x+dx,y+dy
            if p in shape and p not in seen:seen.add(p);pending.append(p)
    if seen!=shape:return False
    for vx,vy in vertices(shape):
        qs=[(vx+dx,vy+dy) in shape for dx,dy in QUADRANTS]
        if sum(qs)==2 and qs[0]==qs[2]:return False
    xmin=min(x for x,y in shape)-1;xmax=max(x for x,y in shape)+1
    ymin=min(y for x,y in shape)-1;ymax=max(y for x,y in shape)+1
    empty={(x,y) for x in range(xmin,xmax+1) for y in range(ymin,ymax+1)}-shape
    pending=deque([(xmin,ymin)]);seen={(xmin,ymin)}
    while pending:
        x,y=pending.popleft()
        for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)):
            p=x+dx,y+dy
            if p in empty and p not in seen:seen.add(p);pending.append(p)
    return seen==empty


def choices(shapes,target,occupied):
    """All integral D4 poses covering the required complete unit cell."""
    result=[];ux,uy=target
    for shape in shapes:
        for a,b in shape:
            translation=ux-a,uy-b
            squares=footprint(shape,translation)
            if not squares&occupied:
                result.append((shape,translation,squares))
    return result


def isolated_gaps(vertex,occupied):
    vx,vy=vertex
    qs=[(vx+dx,vy+dy) in occupied for dx,dy in QUADRANTS]
    return [i for i in range(4) if not qs[i] and qs[(i-1)%4] and qs[(i+1)%4]]


def propagate(tile,copies,max_steps=128):
    """Try to prove that all vertices of the specified copies cannot be interior.

    Only original vertices are required interior. Vertices first introduced by
    a forced neighboring tile are never added to this requirement.
    """
    if not disc(tile):raise ValueError('the orthogonal neighbor must be a disc')
    shapes=variants(tile);occupied=set();original=set()
    for shape,translation in copies:
        if cells(shape) not in shapes:raise ValueError('noncongruent fixed copy')
        squares=footprint(shape,translation)
        if squares&occupied:raise ValueError('fixed-copy interior overlap')
        occupied.update(squares);original.update(vertices(squares))
    original=sorted(original);trace=[]
    while True:
        changed=False
        for vertex in original:
            for quadrant in isolated_gaps(vertex,occupied):
                dx,dy=QUADRANTS[quadrant];target=vertex[0]+dx,vertex[1]+dy
                feasible=choices(shapes,target,occupied)
                if not feasible:
                    return {'status':'contradiction','trace':trace,
                            'empty_corner':{'vertex':vertex,'quadrant':quadrant,
                                            'target_cell':target,'feasible_poses':0}}
                if len(feasible)==1:
                    if len(trace)>=max_steps:
                        return {'status':'step_guard; inconclusive','trace':trace}
                    shape,translation,squares=feasible[0]
                    trace.append({'vertex':vertex,'quadrant':quadrant,'target_cell':target,
                                  'shape':shape,'translation':translation,'feasible_poses':1})
                    occupied.update(squares);changed=True;break
            if changed:break
        if not changed:return {'status':'propagation exhausted; inconclusive','trace':trace}
