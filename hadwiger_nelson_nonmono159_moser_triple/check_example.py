#!/usr/bin/env python3
"""Full strict graphs for B union uA and B union u conjugate(A), u=(5 +/- i sqrt(39))/8.

Independent integer geometry in Q(sqrt(3),sqrt(11),sqrt(13)), scale 288.
"""

from hashlib import sha256
from itertools import permutations
from math import prod
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent
TABLE=[[(i^j,prod(p for k,p in enumerate((3,11,13)) if (i&j)>>k&1))
        for j in range(8)] for i in range(8)]


def square(v):
    out=[0]*8
    nonzero=[(i,x) for i,x in enumerate(v) if x]
    for k,(i,x) in enumerate(nonzero):
        for j,y in nonzero[k:]:
            ix,f=TABLE[i][j]
            out[ix]+=x*y*f*(1 if i==j else 2)
    return out


def edges(points):
    ee=[]
    for i,p in enumerate(points):
        for j,q in enumerate(points[:i]):
            dx=square(tuple(p[k]-q[k] for k in range(8)))
            dy=square(tuple(p[8+k]-q[8+k] for k in range(8)))
            if tuple(a+b for a,b in zip(dx,dy))==(288**2,0,0,0,0,0,0,0):
                ee.append((j,i))
    return ee


def main():
    raw=(HERE.parent/'hadwiger_nelson_nonmono159_214_lowden2/points159.tsv').read_bytes()
    if sha256(raw).hexdigest()!='4f72fa06d18434472ce77cebe38880333694ec04b94945ede073a4a1c6d5bc02':
        raise ValueError('coordinate hash mismatch')
    coefficients=[]
    for line in raw.decode().splitlines():
        if line and not line.startswith('#'):
            v=tuple(map(int,line.split()))
            coefficients.append(tuple(v[i] for i in (0,5,9,12)))
    A=[];inner=[]
    for a,b,c,d in coefficients:
        x,y=[0]*8,[0]*8
        x[0],x[3],y[1],y[2]=24*a,24*b,24*c,24*d
        A.append(tuple(x+y))
        x,y=[0]*8,[0]*8
        x[0],x[3],y[1],y[2]=4*(5*a-11*d),4*(5*b-c),4*(11*b+5*c),4*(a+5*d)
        inner.append(tuple(x+y))
    B=list(dict.fromkeys(A+inner))
    if len(B)!=292 or len(set(A)&set(inner))!=26 or len(edges(B))!=1251:
        raise ValueError('incorrect inner geometry')
    libA=[tuple(map(int,s)) for s in (HERE/'colors_A.txt').read_text().splitlines()]
    libB=[tuple(map(int,s)) for s in (HERE/'colors_B.txt').read_text().splitlines()]
    perms=[(0,)+p for p in permutations((1,2,3))]
    results=[]
    for reflected in (False,True):
        for sign in (-1,1):
            image=[]
            for a,b,c0,d0 in coefficients:
                c,d=(-c0,-d0) if reflected else (c0,d0)
                x,y=[0]*8,[0]*8
                x[0],x[3],x[4],x[7]=15*a,15*b,-sign*9*c,-sign*3*d
                y[1],y[2],y[5],y[6]=15*c,15*d,sign*3*a,sign*9*b
                image.append(tuple(x+y))
            points=B+image[1:]
            if len(points)!=450 or len(set(points))!=450 or B[0]!=image[0]:
                raise ValueError('incorrect union overlap')
            ee=edges(points)
            witness=None
            for i,cb in enumerate(libB):
                for j,ca in enumerate(libA):
                    for k,p in enumerate(perms):
                        colors=cb+tuple(p[v] for v in ca[1:])
                        if all(colors[a]!=colors[b] for a,b in ee):
                            witness=i,j,k;break
                    if witness is not None:break
                if witness is not None:break
            if witness is None:raise ValueError('uncolored example')
            results.append({'reflected':reflected,'radical_sign':sign,'vertices':len(points),
                            'strict_edges':len(ee),'new_cross_edges':len(ee)-1897,
                            'witness':witness,'edge_sha256':sha256(json.dumps(ee).encode()).hexdigest()})
    print(json.dumps(results,indent=2))


if __name__=='__main__':main()
