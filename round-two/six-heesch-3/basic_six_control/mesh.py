"""Exact registered-grid cells for the fixed-control replay; no search."""
from functools import lru_cache
import geometry as b

def plus(p,q):
    return p[0]+q[0],p[1]+q[1]


def triangle_key(p):
    return (1,)+tuple(x for v in sorted(p) for x in v)


def split_triangle(p):
    g=(sum(v[0] for v in p)//3,sum(v[1] for v in p)//3)
    b.require(all(sum(v[k] for v in p)%3==0 for k in (0,1)),'nonintegral triangle centroid')
    result=[]
    for i,v in enumerate(p):
        w=p[(i+1)%3]
        b.require(all((v[k]+w[k])%2==0 for k in (0,1)),'nonintegral edge midpoint')
        mid=tuple((v[k]+w[k])//2 for k in (0,1))
        result.extend(((v,mid,g),(mid,w,g)))
    return tuple(result)


def hex_vertices(c):
    return tuple(plus(c,v) for v in ((-12,0),(-6,6),(6,6),(12,0),(6,-6),(-6,-6)))


def cell_vertices(key):
    if key[0]:
        return tuple(zip(key[1::2],key[2::2]))
    p=hex_vertices(key[1:])
    return p+tuple(((a[0]+p[(i+1)%6][0])//2,(a[1]+p[(i+1)%6][1])//2) for i,a in enumerate(p))


@lru_cache(None)
def local_cells(m):
    cells=[]
    for j in range(m):
        cells.append((0,12+24*j,0))
        up=((24*j+6,6),(24*j+12,12),(24*j+18,6))
        cells.extend(triangle_key(t) for t in split_triangle(up))
        if j<m-1:
            down=((24*j+18,6),(24*j+24,0),(24*j+30,6))
            cells.extend(triangle_key(t) for t in split_triangle(down))
    a=(24*m-6,6);v=(24*m,0);mid=(24*m,6);ab=(24*m-3,3);g=(24*m,4)
    cells.extend(triangle_key(t) for t in ((a,ab,g),(ab,v,g),(a,g,mid)))
    b.require(len(cells)==13*m-3 and len(set(cells))==len(cells),'bad prototype cell count')
    return tuple(cells)


def transform(key,angle,flip,translation):
    if key[0]==0:
        p=b.point((angle,flip,*translation),key[1:])
        return (0,*p)
    p=tuple(b.point((angle,flip,*translation),v) for v in cell_vertices(key))
    return triangle_key(p)


def shifted(key,c):
    if key[0]==0:
        return (0,key[1]+c[0],key[2]+c[1])
    return (1,)+tuple(v+c[i%2] for i,v in enumerate(key[1:]))


def footprint(m,pose):
    a,f,tx,ty=pose
    return frozenset(transform(k,a,f,(3*tx,3*ty)) for k in local_cells(m))
