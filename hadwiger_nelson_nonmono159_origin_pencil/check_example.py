#!/usr/bin/env python3
"""Direct geometry in Q(sqrt(3),sqrt(11),sqrt(13)) at u=(5+i sqrt(39))/8.

This checker uses neither the quadratic-pencil reduction nor its field code.
It reconstructs every strict unit edge for both roots and both parities.
"""

from hashlib import sha256
from itertools import permutations
import json
from math import prod
from pathlib import Path

HERE = Path(__file__).resolve().parent
RADICALS = (3, 11, 13)
PRODUCTS = [[(i ^ j, prod(RADICALS[k] for k in range(3)
                        if (i & j) >> k & 1))
             for j in range(8)] for i in range(8)]


def square(v):
    out = [0]*8
    entries = [(i,x) for i,x in enumerate(v) if x]
    for k,(i,x) in enumerate(entries):
        for j,y in entries[k:]:
            ix, factor = PRODUCTS[i][j]
            out[ix] += x*y*factor*(1 if i==j else 2)
    return out


def unit(p, q):
    x = square(tuple(a-b for a,b in zip(p[:8],q[:8])))
    y = square(tuple(a-b for a,b in zip(p[8:],q[8:])))
    return tuple(a+b for a,b in zip(x,y)) == (96**2,0,0,0,0,0,0,0)


def main():
    path = HERE.parent/'hadwiger_nelson_nonmono159_214_lowden2/points159.tsv'
    raw = path.read_bytes()
    if sha256(raw).hexdigest() != '4f72fa06d18434472ce77cebe38880333694ec04b94945ede073a4a1c6d5bc02':
        raise ValueError('wrong coordinates')
    coefficients = []
    for line in raw.decode().splitlines():
        if line and not line.startswith('#'):
            v = list(map(int,line.split()))
            coefficients.append(tuple(v[i] for i in (0,5,9,12)))
    original = []
    for a,b,c,d in coefficients:
        x,y = [0]*8,[0]*8
        x[0],x[3],y[1],y[2] = 8*a,8*b,8*c,8*d
        original.append(tuple(x+y))
    library = [tuple(map(int,s)) for s in (HERE/'colorings.txt').read_text().splitlines()]
    perms = [(0,)+p for p in permutations((1,2,3))]
    result = []
    for reflected in (False,True):
        for sign in (-1,1):
            image = []
            for a,b,c0,d0 in coefficients:
                c,d = (-c0,-d0) if reflected else (c0,d0)
                x,y = [0]*8,[0]*8
                x[0],x[3],x[4],x[7] = 5*a,5*b,-sign*3*c,-sign*d
                y[1],y[2],y[5],y[6] = 5*c,5*d,sign*a,sign*3*b
                image.append(tuple(x+y))
            vertices = original+image[1:]
            if len(vertices)!=317 or len(set(vertices))!=317 or original[0]!=image[0]:
                raise ValueError('wrong overlap')
            edges = [(j,i) for i in range(317) for j in range(i) if unit(vertices[i],vertices[j])]
            witness = None
            for a,ca in enumerate(library):
                for b,cb in enumerate(library):
                    for k,p in enumerate(perms):
                        colors = ca+tuple(p[v] for v in cb[1:])
                        if all(colors[i]!=colors[j] for i,j in edges):
                            witness = a,b,k
                            break
                    if witness is not None: break
                if witness is not None: break
            if witness is None:
                raise ValueError('example not covered')
            result.append({'reflected':reflected,'radical_sign':sign,'vertices':317,
                           'strict_edges':len(edges),'new_cross_edges':len(edges)-1292,
                           'witness':witness,'edge_sha256':sha256(json.dumps(edges).encode()).hexdigest()})
    print(json.dumps(result,indent=2))


if __name__=='__main__':
    main()
