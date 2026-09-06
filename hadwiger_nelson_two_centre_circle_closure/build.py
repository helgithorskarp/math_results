"""Small exact certificates for the two-centre circle theorem; no solver."""
import argparse, hashlib, json, time
from itertools import combinations
from pathlib import Path
HERE = Path(__file__).resolve().parent

def need(ok, message):
    if not ok:
        raise ValueError(message)

def times(x, y):
    a,b,c,d = x
    e,f,g,h = y
    return (a*e+3*b*f+11*c*g+33*d*h,
            a*f+b*e+11*c*h+11*d*g,
            a*g+3*b*h+c*e+3*d*f,
            a*h+b*g+c*f+d*e)

def norm(a, b):
    diffs = [tuple(x-y for x,y in zip(c,d)) for c,d in zip(a,b)]
    squares = [times(v,v) for v in diffs]
    return tuple(sum(v[i] for v in squares) for i in range(4))

def generate():
    # (s,t) denotes (s*sqrt3/2,t/2); centres are (0,0),(2,0).
    A = [(1,1),(0,2),(-1,1),(-1,-1),(0,-2),(1,-1)]
    B = [(s+2,t) for s,t in A]
    V = list(dict.fromkeys([(0,0),(2,0)] + A + B))
    q = lambda x,y: 3*(x[0]-y[0])**2+(x[1]-y[1])**2
    E = [list(e) for e in combinations(range(12),2) if q(V[e[0]],V[e[1]])==4]
    colours = [2,0,1,0,1,0,1,3,1,2,1,2]
    need(len(E)==23 and all(colours[a]!=colours[b] for a,b in E), 'patch colouring')
    closure = []
    for side, ring in enumerate((A,B)):
        other = V[1-side]
        for x in ring:
            squared = q(x,other)//4
            ys = [i for i,y in enumerate(V) if q(x,y)==q(other,y)==4]
            need(len(ys)=={1:2,4:1,7:0}[squared], 'circle completion')
            closure.append([side,V.index(x),squared,ys])
    roots = [(2,0),(1,1),(-1,1),(-2,0),(-1,-1),(1,-1)]
    chord_rows = []
    for j,(a,b) in enumerate(roots):
        squared = ((a-2)**2+3*b*b)//4
        chord_rows.append([j,j%2,squared,4-squared])
    z = (0,0,0,0)
    M = [(z,z),((12,0,0,0),z),((6,0,0,0),(0,6,0,0)),
         ((18,0,0,0),(0,6,0,0)),((10,0,0,0),(0,0,2,0)),
         ((5,0,0,-1),(0,5,1,0)),((15,0,0,-1),(0,5,3,0))]
    ME = [list(e) for e in combinations(range(7),2) if norm(M[e[0]],M[e[1]])==(144,0,0,0)]
    return {'patch':{'coordinate_map':'(s,t) -> (s*sqrt3/2,t/2)',
                    'vertices':V,'centres':[0,1],'rings':[[V.index(x) for x in ring] for ring in (A,B)],
                    'edges':E,'colours':colours,'cross_circle_closure':closure},
            'orbit_chords':{'columns':['step','parity','chord_squared','centre_distance_squared'],
                            'rows':chord_rows},
            'sharpness':{'name':'classical Moser spindle','coordinate_scale':12,
                         'basis':['1','sqrt3','sqrt11','sqrt33'],'vertices':M,
                         'edges':ME,'dominating_pair':[0,3],'colours':[0,1,2,3,1,3,2]}}

def main():
    p = argparse.ArgumentParser()
    p.add_argument('--out',required=True)
    p.add_argument('--discover',action='store_true')
    a = p.parse_args()
    out = Path(a.out)
    out.mkdir(parents=True,exist_ok=False)
    start = time.monotonic()
    raw = (json.dumps(generate(),sort_keys=True,separators=(',',':'))+'\n').encode()
    if not a.discover:
        need(raw==(HERE/'certificate.json').read_bytes(),'certificate mismatch')
    (out/'certificate.json').write_bytes(raw)
    r = {'status':'PASS','certificate_bytes':len(raw),'certificate_sha256':hashlib.sha256(raw).hexdigest(),
         'native_solver_calls':0,'seconds':time.monotonic()-start}
    (out/'build.json').write_text(json.dumps(r,indent=2)+'\n')
    print(json.dumps(r,sort_keys=True))
if __name__=='__main__':
    main()
