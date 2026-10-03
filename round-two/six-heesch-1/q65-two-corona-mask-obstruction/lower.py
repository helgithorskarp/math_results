"""Independent literal-disc corona reader using oriented boundary cycles.

The producer tests complementary cell connectivity. This reader transforms
physical square vertices and verifies a single simple, positive-area boundary
cycle for each prefix. It imports no solver or other research source.
"""
import argparse,json
from collections import Counter
from itertools import product
from pathlib import Path

def require(ok,msg):
    if not ok:raise ValueError(msg)

def images(raw):
    out=set()
    for swap in (False,True):
        for sx,sy in product((-1,1),repeat=2):
            footprint=[]
            for x,y in raw:
                vs=[(sx*(y+v if swap else x+u),sy*(x+u if swap else y+v)) for u,v in product((0,1),repeat=2)]
                footprint.append((min(q[0] for q in vs),min(q[1] for q in vs)))
            ax=min(q[0] for q in footprint);ay=min(q[1] for q in footprint)
            out.add(tuple(sorted((x-ax,y-ay) for x,y in footprint)))
    return tuple(sorted(out))

def boundary_disc(cells):
    require(bool(cells),'empty prefix')
    edges=set()
    for x,y in cells:
        if (x,y-1) not in cells:edges.add(((x,y),(x+1,y)))
        if (x+1,y) not in cells:edges.add(((x+1,y),(x+1,y+1)))
        if (x,y+1) not in cells:edges.add(((x+1,y+1),(x,y+1)))
        if (x-1,y) not in cells:edges.add(((x,y+1),(x,y)))
    outgoing=Counter(a for a,b in edges);incoming=Counter(b for a,b in edges)
    require(outgoing==incoming and all(v==1 for v in outgoing.values()),'boundary has a pinch or branch')
    successor=dict(edges);start=min(successor);current=start;seen=set()
    while current not in seen:
        seen.add(current);current=successor[current]
    require(current==start and len(seen)==len(edges),'multiple boundary cycles: hole or disconnected component')
    area2=sum(a[0]*b[1]-a[1]*b[0] for a,b in edges)
    require(area2==2*len(cells),'boundary signed area does not equal occupied area')
    return len(edges)

def check(data):
    raw=[tuple(q) for q in data['cells']]
    require(raw and len(raw)==len(set(raw)) and all(len(q)==2 and all(type(z) is int for z in q) for q in raw),'invalid source cells')
    source=set(raw);boundary_disc(source);shapes=images(raw)
    require(min(x for x,y in source)==min(y for x,y in source)==0,'source is not normalized')
    levels=data['levels'];require(levels and len(levels[0])==1,'wrong central-copy count')
    occupied=set();stats=[];copies=0
    for k,lev in enumerate(levels):
        before=set(occupied)
        target={(x+dx,y+dy) for x,y in before for dx,dy in product((-1,0,1),repeat=2)}-before
        for pose in lev:
            require(len(pose)==3 and all(type(z) is int for z in pose),'invalid whole-copy pose')
            o,tx,ty=pose;require(0<=o<len(shapes),'orientation outside D4 image inventory')
            fp={(x+tx,y+ty) for x,y in shapes[o]}
            require(not fp&occupied,'overlapping whole copies')
            require(not k or fp&target,'new copy does not touch prior prefix')
            if not k:require(fp==source,'root is not the literal source')
            occupied|=fp;copies+=1
        require(not k or target<=occupied,'incomplete halo')
        stats.append(dict(level=k,shell_copies=len(lev),cumulative_copies=copies,cells=len(occupied),boundary_edges=boundary_disc(occupied)))
    return dict(prototype_area=len(source),complete_disc_coronas=len(levels)-1,prefixes=stats,finite_status='not established')

def main():
    ap=argparse.ArgumentParser();ap.add_argument('input',type=Path)
    args=ap.parse_args();print(json.dumps(check(json.loads(args.input.read_text())),indent=2))
if __name__=='__main__':main()
