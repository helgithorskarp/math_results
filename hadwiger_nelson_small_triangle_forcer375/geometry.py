"""Producer geometry, in the paper's integer numerator convention."""
import json
from pathlib import Path
from itertools import combinations
from hashlib import sha256

ROOT=Path(__file__).resolve().parent
TERMINALS=[(0,0,12,0),(-6,0,-6,0),(6,0,-6,0)]

def read(name):
    return json.loads((ROOT/name).read_text())

def rotate(p):
    a,b,c,d=p
    doubled=(-a-c,-b-3*d,3*a-c,b-d)
    if any(v%2 for v in doubled):raise ValueError('Nonintegral orbit')
    return tuple(v//2 for v in doubled)

def reference(axis='y'):
    points=set()
    for row in read('appendix.json'):
        p=tuple(row)
        for _ in range(3):
            a,b,c,d=p;points.add(p)
            points.add((-a,-b,c,d) if axis=='y' else (a,b,-c,-d))
            p=rotate(p)
    return TERMINALS+sorted(points-set(TERMINALS)) if axis=='y' else sorted(points)

def squared(p,q):
    a,b,c,d=(x-y for x,y in zip(p,q))
    return 3*a*a+11*b*b+c*c+33*d*d, 2*a*b+2*c*d

def edges(points, numerator=1296):
    return [[i,j] for i,j in combinations(range(len(points)),2)
            if squared(points[i],points[j])==(numerator,0)]

def digest(value):
    return sha256(json.dumps(value,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def graph():
    pts=reference();cert=read('certificate.json')
    chosen=[pts[i] for i in cert['retained_reference_indices']]
    return chosen,edges(chosen)

if __name__=='__main__':
    pts,es=graph()
    print(json.dumps({'vertices':len(pts),'edges':len(es),'point_sha256':digest(pts),
                      'edge_sha256':digest(es)},sort_keys=True))
