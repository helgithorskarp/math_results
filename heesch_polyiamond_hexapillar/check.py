"""Independent definition-level certificate checker; standard-library integers.

Reads the geometric tile and rigid-motion certificate, without importing the
generator or using symbolic edge labels. Boundary cycles certify disc topology;
complete six-triangle vertex stars certify full surrounding. The all-motion
upper theorem is the written corner injection in angle_capacity.md.
"""
import argparse
from collections import Counter,defaultdict
import hashlib
import json
from pathlib import Path
import resource
import time

BASE=Path(__file__).resolve().parent
DIRECTIONS=((1,0),(0,1),(-1,1),(-1,0),(0,-1),(1,-1))


def cell(raw):
    assert len(raw)==3
    assert all(len(p)==2 and all(type(x) is int for x in p) for p in raw)
    t=tuple(sorted(map(tuple,raw)))
    assert len(set(t))==3
    for i,a in enumerate(t):
        for b in t[i+1:]:
            assert (b[0]-a[0],b[1]-a[1]) in DIRECTIONS, 'nonunit triangle'
    return t


def cross(a,b):
    return a[0]*b[1]-a[1]*b[0]


def sub(a,b):
    return a[0]-b[0],a[1]-b[1]


def ccw(t):
    a,b,c=t
    determinant=cross(sub(b,a),sub(c,a))
    assert abs(determinant)==1
    return (a,b,c) if determinant==1 else (a,c,b)


def mesh(cells):
    assert cells
    incidences=defaultdict(list);vertices=set()
    for t in cells:
        a,b,c=ccw(t);vertices.update(t)
        for u,v in ((a,b),(b,c),(c,a)):
            incidences[tuple(sorted((u,v)))].append((u,v,t))
    adjacent=defaultdict(set);boundary=[]
    for entries in incidences.values():
        assert len(entries) in (1,2)
        if len(entries)==2:
            a,b,t=entries[0];c,d,u=entries[1]
            assert (a,b)==(d,c)
            adjacent[t].add(u);adjacent[u].add(t)
        else:boundary.append(entries[0][:2])
    unseen=set(cells);queue=[unseen.pop()]
    while queue:
        for t in adjacent[queue.pop()]:
            if t in unseen:unseen.remove(t);queue.append(t)
    assert not unseen,'edge-disconnected mesh'
    outgoing={};incoming={}
    for a,b in boundary:
        assert a not in outgoing and b not in incoming,'pinched boundary'
        outgoing[a]=b;incoming[b]=a
    assert set(outgoing)==set(incoming)
    start=min(outgoing);polygon=[start];v=outgoing[start]
    while v!=start:
        assert v not in polygon,'repeated boundary vertex'
        polygon.append(v);v=outgoing[v]
    assert len(polygon)==len(boundary),'multiple boundary cycles (hole)'
    angles=Counter()
    for v in polygon:
        before=sub(v,incoming[v]);after=sub(outgoing[v],v)
        i=DIRECTIONS.index(before);j=DIRECTIONS.index(after)
        turn=(j-i+3)%6-3
        assert -2<=turn<=2
        angles[180-60*turn]+=1
    chi=len(vertices)-len(incidences)+len(cells)
    assert chi==1
    return {'cells':len(cells),'vertices':len(vertices),'edges':len(incidences),
            'chi':chi,'boundary_angles':dict(sorted(angles.items()))},vertices,polygon


def star(v):
    x,y=v
    return {tuple(sorted((v,(x+DIRECTIONS[j][0],y+DIRECTIONS[j][1]),
                           (x+DIRECTIONS[(j+1)%6][0],y+DIRECTIONS[(j+1)%6][1]))))
            for j in range(6)}


def isometry(raw):
    assert len(raw)==4 and all(type(x) is int for x in raw)
    a,b,c,d=raw
    assert a*a+a*c+c*c==1 and b*b+b*d+d*d==1
    assert 2*a*b+a*d+b*c+2*c*d==1
    assert abs(a*d-b*c)==1
    return a,b,c,d


def verify(tile_file,corona_file):
    tile_raw=tile_file.read_bytes();corona_raw=corona_file.read_bytes()
    tile_data=json.loads(tile_raw);corona=json.loads(corona_raw)
    assert tile_data['grid']=='unit-equilateral-triangles'
    tile=[cell(t) for t in tile_data['triangles']];assert len(set(tile))==len(tile)
    tile=set(tile);root_stats,root_vertices,_=mesh(tile)
    depth=corona['depth'];assert type(depth) is int and depth==5
    occupied=set();copies=[];layers=[set() for _ in range(depth+1)];layer_counts=[0]*(depth+1)
    roots=0
    for p in corona['placements']:
        k=p['level'];assert type(k) is int and 0<=k<=depth
        a,b,c,d=isometry(p['matrix']);shift=p['translation']
        assert len(shift)==2 and all(type(z) is int for z in shift)
        x,y=shift
        moved={tuple(sorted((a*u+b*v+x,c*u+d*v+y) for u,v in t)) for t in tile}
        assert len(moved)==len(tile) and all(cell(t)==t for t in moved)
        assert occupied.isdisjoint(moved),'copy overlap'
        if k==0:
            roots+=1
            assert (a,b,c,d,x,y)==(1,0,0,1,0,0) and moved==tile
        occupied.update(moved);layers[k].update(moved);layer_counts[k]+=1;copies.append((k,moved))
    assert roots==1
    prefixes=[];vertices=[];statistics=[];current=set()
    for k in range(depth+1):
        current=current|layers[k];prefixes.append(current)
        row,vs,_=mesh(current);vertices.append(vs)
        row.update({'level':k,'layer_copies':layer_counts[k],'cumulative_copies':sum(layer_counts[:k+1])})
        statistics.append(row)
    for k in range(depth):
        for v in vertices[k]:
            assert star(v)<=prefixes[k+1],('incomplete vertex star',k,v)
    for k,moved in copies:
        if k:
            previous_layer_vertices={v for t in layers[k-1] for v in t}
            assert {v for t in moved for v in t}&previous_layer_vertices,('missing preceding corona contact',k)
    assert layer_counts==[1,5,11,23,39,52]
    assert root_stats['boundary_angles']=={60:8,120:30,180:2,240:22,300:9}
    assert len(tile)==215
    delta=max(max(f(x,y) for x,y in root_vertices)-min(f(x,y) for x,y in root_vertices)
              for f in (lambda x,y:x,lambda x,y:y,lambda x,y:x+y))
    assert delta==24
    k=1
    while len(tile)*9**k<=16*delta*delta*(k+1)**2*8**k:k+=1
    assert k==113
    return {'agent':'six-heesch-2','role':'researcher','cells':len(tile),
            'proof_status':'exact lower certificate plus written all-motion angle theorem',
            'claim':'5 <= Hc <= Hh <= 112; reproduction, not an exact-H or novelty claim',
            'boundary_angles':root_stats['boundary_angles'],'diameter_bound':delta,
            'first_forbidden_capacity_corona':k,'prefixes':statistics,
            'tile_sha256':hashlib.sha256(tile_raw).hexdigest(),
            'coronas_sha256':hashlib.sha256(corona_raw).hexdigest()}


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--tile',type=Path,default=BASE/'tile.json')
    parser.add_argument('--coronas',type=Path,default=BASE/'coronas.json')
    parser.add_argument('--expected',type=Path,default=BASE/'expected.json')
    parser.add_argument('--write-expected',action='store_true')
    args=parser.parse_args();start=time.monotonic()
    result=verify(args.tile,args.coronas)
    encoded=json.dumps(result,indent=2,sort_keys=True)+'\n'
    if args.write_expected:args.expected.write_text(encoded)
    else:assert json.loads(encoded)==json.loads(args.expected.read_text()),'expected result mismatch'
    print(encoded,end='')
    print(json.dumps({'seconds':round(time.monotonic()-start,3),
                      'peak_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}),flush=True)


if __name__=='__main__':
    main()
