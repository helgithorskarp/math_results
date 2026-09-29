"""Exact potentials, planar surface and three-pair half-balance certificate.

Python 3.11+, standard library only. The solver used to discover the box
is not part of the proof or reproduction dependency.
"""
from itertools import combinations
from pathlib import Path
import hashlib
import json

HERE=Path(__file__).resolve().parent
N=32
ALL=(1<<N)-1


def components(adj,removed):
    left=ALL&~removed;parts=[]
    while left:
        bit=left&-left;left^=bit;part=todo=bit
        while todo:
            bit=todo&-todo;todo^=bit;new=adj[bit.bit_length()-1]&left
            left^=new;part|=new;todo|=new
        parts.append(part)
    return parts


def run():
    raw=(HERE/'certificate.json').read_bytes();c=json.loads(raw)
    pentagons=c['pentagons'];assert len(pentagons)==12
    edges=set();triangles=[]
    for z,F in enumerate(pentagons,20):
        assert len(F)==len(set(F))==5 and all(0<=u<20 for u in F)
        for u,v in zip(F,F[1:]+F[:1]):
            edges.update((tuple(sorted((u,v))),(u,z),(v,z)))
            triangles.append((u,v,z))
    assert len(edges)==90 and len(triangles)==60 and N-len(edges)+len(triangles)==2
    darts=[(u,v) for F in triangles for u,v in zip(F,F[1:]+F[:1])]
    assert len(darts)==len(set(darts)) and all((v,u) in darts for u,v in darts)
    adj=[0]*N
    for u,v in edges:adj[u]|=1<<v;adj[v]|=1<<u
    assert len(components(adj,0))==1
    for v in range(N):
        link={}
        for F in triangles:
            if v in F:
                i=F.index(v);assert F[(i+1)%3] not in link;link[F[(i+1)%3]]=F[(i+2)%3]
        first=min(link);u=first;seen=set()
        while u not in seen:seen.add(u);u=link[u]
        assert u==first and seen==set(link)==set(link.values())
        assert sum(1<<u for u in seen)==adj[v]
    centers={(u,v):w for u,v,w in c['edge_centers']}
    assert len(centers)==len(c['edge_centers'])==90 and set(centers)==edges
    radius=c['radius'];assert radius==1 and min(centers.values())==7 and max(centers.values())==14
    assert all(type(w) is int and w>radius for w in centers.values())
    pairs=c['pairs'];assert len(pairs)==3 and all(len(pair)==2 for pair in pairs)
    paths=[P for pair in pairs for P in pair];pots=c['adverse_corner_potentials'];assert len(pots)==6
    inequalities=0
    for P,pot in zip(paths,pots):
        assert P and len(P)==len(set(P)) and len(pot)==N and all(type(x) is int for x in pot)
        selected={tuple(sorted(e)) for e in zip(P,P[1:])};assert selected<=edges
        for e,w in centers.items():
            u,v=e;length=w+radius if e in selected else w-radius
            assert abs(pot[v]-pot[u])<=length;inequalities+=1
        assert pot[P[-1]]-pot[P[0]]==sum(centers[e]+radius for e in selected)
    parts=[components(adj,sum(1<<v for v in set(P+Q))) for P,Q in pairs]
    large=[sorted(C for C in row if C.bit_count()>4) for row in parts]
    assert list(map(len,large))==[1,1,2]
    A=large[0][0];B=large[1][0]
    assert all(not C&A or not C&B for C in large[2])
    connectivity_checks=0
    for removed in combinations(range(N),4):
        assert len(components(adj,sum(1<<v for v in removed)))==1;connectivity_checks+=1
    assert connectivity_checks==35960 and min(C.bit_count() for C in adj)==5
    return {'status':'PASS','vertices':N,'edges':len(edges),'faces':len(triangles),
            'vertex_connectivity':5,'four_vertex_deletion_checks':connectivity_checks,
            'independent_price_dimensions':90,'box_radius':radius,'minimum_center':7,'maximum_center':14,
            'prescribed_pairs':3,'prescribed_paths':6,'potential_inequalities':inequalities,
            'residual_component_orders':[sorted(C.bit_count() for C in row) for row in parts],
            'heavy_four_vertex_repair_required':True,'certificate_sha256':hashlib.sha256(raw).hexdigest()}


if __name__=='__main__':print(json.dumps(run(),sort_keys=True))
