#!/usr/bin/env python3
"""One frozen exact G79--G49 complement; positive ordinary colour witnesses."""
from pathlib import Path
import sys,json,hashlib,time,argparse
from fractions import Fraction as F
from itertools import combinations
HERE=Path(__file__).resolve().parent
SOURCE=HERE.parent/'hadwiger_nelson_small_triangle_forcer375'
sys.path.insert(0,str(SOURCE))
import radicals as R
import geometry as G


def need(ok,msg):
    if not ok:raise ValueError(msg)


def digest(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def encode(points):
    out=[]
    for p in points:
        row=[]
        for a in p:
            b=[F(x)*128 for x in a];need(all(x.denominator==1 for x in b),'common denominator');row.append([int(x) for x in b])
        out.append(row)
    return out


def graph(points):return [[i,j] for i,j in combinations(range(len(points)),2) if R.distance(points[i],points[j])==R.scalar(1296)]


def main():
    pa=argparse.ArgumentParser();pa.add_argument('--out',type=Path,required=True);a=pa.parse_args();start=time.monotonic()
    g40=list(map(R.point,G.read('g40.json')));g49=list(map(R.point,G.read('g49.json')))
    P=R.point((0,0,30,-6));Q=R.point((0,0,30,6));need(P in g40 and Q in g40,'named anchors')
    need(R.distance(P,Q)==R.scalar(4752),'anchor metric');need(R.psub(Q,P)==R.psub(g49[1],g49[0]),'translation pair frame')
    shift=(R.ZERO,R.scalar(24))
    frame=lambda p:R.padd(R.conjugate(p),shift)
    g79=set(g40+[R.cmul(R.ROT_SPINDLE,p) for p in g40]);need(len(g79)==79,'G79 exact order')
    moved49=[frame(R.padd(P,p)) for p in g49];moved79={frame(p) for p in g79}
    host_rows,_=G.graph();host=list(map(R.point,host_rows));pins=host[:3]
    need([moved49[i] for i in [4,2,3]]==pins,'marked triangle frame')
    cset=moved79|set(moved49);comp=pins+sorted(cset-set(pins));need(len(comp)<=136,'complement cap')
    union=host+sorted(cset-set(host));need(len(union)<=508,'physical union cap')
    ce=graph(comp);ue=graph(union);he=graph(host)
    need(len(he)==1661,'host edge count')
    print('GEOMETRY',len(comp),len(ce),len(union),len(ue),round(time.monotonic()-start,3),flush=True)
    from pysat.solvers import Solver
    n=len(union);var=lambda v,c:4*v+c+1
    cnf=[[var(v,c) for c in range(4)] for v in range(n)]
    cnf += [[-var(v,c),-var(v,d)] for v in range(n) for c in range(4) for d in range(c)]
    cnf += [[-var(v,c),-var(w,c)] for v,w in ue for c in range(4)]
    with Solver(name='cadical195',bootstrap_with=cnf,with_proof=True) as solver:
        sat=solver.solve()
        if not sat:
            a.out.with_suffix('.drat').write_text('\n'.join(solver.get_proof())+'\n')
            a.out.with_suffix('.cnf').write_text('p cnf %d %d\n'%(4*n,len(cnf))+''.join(' '.join(map(str,row))+' 0\n' for row in cnf))
            raise ValueError('NONFOUR SIGNAL: preserve exact support, proof-check, then obtain five-word')
        positive={v for v in solver.get_model() if v>0}
    word=[next(c for c in range(4) if var(v,c) in positive) for v in range(n)]
    need(all(word[v]!=word[w] for v,w in ue),'complete union colour word')
    need(len(set(word[:3]))>1,'nonmonochromatic target pins')
    index={p:i for i,p in enumerate(union)};cmap=[index[p] for p in comp];cword=[word[v] for v in cmap]
    inherited={tuple(e) for e in he}|{tuple(sorted((cmap[v],cmap[w]))) for v,w in ce}
    cross=[e for e in ue if tuple(e) not in inherited]
    outside=[i for i,p in enumerate(comp) if any(p[xy][b] for xy in (0,1) for b in range(4,8))]
    cert={'schema':'hn-t375-g79-g49-one-complement-v1','complement_points':len(comp),'complement_edges':len(ce),'union_points':len(union),'union_edges':len(ue),'overlap_count':len(set(host)&cset),'extra_cross_edges':cross,'complement_to_union':cmap,'complement_colour_word':cword,'union_colour_word':word,'pins':word[:3],'outside_native_field_indices':outside,'complement_point_sha256':digest(encode(comp)),'union_point_sha256':digest(encode(union)),'complement_edge_sha256':digest(ce),'union_edge_sha256':digest(ue),'scale':4608,'record_candidate':False}
    a.out.write_text(json.dumps(cert,sort_keys=True,indent=2)+'\n')
    print(json.dumps({k:v for k,v in cert.items() if not isinstance(v,list)},indent=2));print('PINS',word[:3],'DONE',round(time.monotonic()-start,3),flush=True)


if __name__=='__main__':main()
