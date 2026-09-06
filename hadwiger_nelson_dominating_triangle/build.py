"""Exact compact witnesses for the dominating-triangle theorem (stdlib only)."""
import argparse
import hashlib
import json
import time
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path

HERE = Path(__file__).resolve().parent


def need(ok, msg):
    if not ok:
        raise ValueError(msg)


# A point is (a,b,c,d), meaning (a+b*sqrt3,c+d*sqrt3).
def add(x, y):
    return tuple(a+b for a, b in zip(x, y))


def rotate(x):
    a,b,c,d = x
    return ((a-3*d)/2, (b-c)/2, (c+3*b)/2, (d+a)/2)


def norm(x, y):
    a,b,c,d = (v-w for v,w in zip(x,y))
    return (a*a+3*b*b+c*c+3*d*d, 2*(a*b+c*d))


def serial(x):
    need(all((v*10).denominator == 1 for v in x), 'scale10')
    return [int(v*10) for v in x]


def generate():
    D = [tuple(map(F,x)) for x in [(0,0,0,0),(1,0,0,0),(F(1,2),0,0,F(1,2))]]
    # a+b*omega is an integer triangular-lattice coordinate.
    U = [(1,0),(0,1),(-1,1),(-1,0),(0,-1),(1,-1)]
    centres = [(0,0),(1,0),(0,1)]
    lattice = sorted({(a+x,b+y) for a,b in centres for x,y in U})
    P = [(F(a)+F(b,2),F(0),F(0),F(b,2)) for a,b in lattice]
    orbit = [(F(3,5),F(0),F(4,5),F(0))]
    for _ in range(5):
        orbit.append(rotate(orbit[-1]))
    need(rotate(orbit[-1]) == orbit[0], 'rotation closure')
    Q = [add(d,u) for d in D for u in orbit]
    V = P+Q
    need(len(set(V)) == 30, 'distinct points')
    E = [list(e) for e in combinations(range(30),2) if norm(V[e[0]],V[e[1]]) == (1,0)]
    patch_colours = [(a+2*b)%3 for a,b in lattice]
    rows = [patch_colours + [(i+sign*(-1)**j)%3 for i in range(3) for j in range(6)]
            for sign in (1,-1)]
    need(all(all(c[a]!=c[b] for a,b in E) for c in rows), 'colour witnesses')
    chord = []
    roots = [(F(a)+F(b,2),F(0),F(0),F(b,2)) for a,b in U]
    for j,z in enumerate(roots):
        n = norm(z,roots[0])
        need(n[1] == 0 and n[0].denominator == 1, 'chord')
        chord.append(int(n[0]))
    return {'coordinate_scale':10,'coordinate_map':'(a,b,c,d)/10 -> ((a+b*sqrt3)/10,(c+d*sqrt3)/10)',
            'patch_lattice':lattice,'vertices':[serial(v) for v in V],
            'centres':[P.index(d) for d in D],
            'generic_labels':[[i,j] for i in range(3) for j in range(6)],
            'edges':E,'pinned_colourings':rows,'rotation_chord_squared':chord,
            'generic_column_derangements':[[1,2,0],[2,0,1]]}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--out',required=True)
    parser.add_argument('--discover',action='store_true')
    args = parser.parse_args()
    out = Path(args.out)
    out.mkdir(parents=True,exist_ok=False)
    start = time.monotonic()
    raw = (json.dumps(generate(),sort_keys=True,separators=(',',':'))+'\n').encode()
    if not args.discover:
        need(raw == (HERE/'certificate.json').read_bytes(),'certificate mismatch')
    (out/'certificate.json').write_bytes(raw)
    report = {'status':'PASS','certificate_bytes':len(raw),
              'certificate_sha256':hashlib.sha256(raw).hexdigest(),
              'seconds':time.monotonic()-start,'native_solver_calls':0}
    (out/'build.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,sort_keys=True))


if __name__ == '__main__':
    main()
