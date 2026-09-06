"""Finite component assembly. Default: verify placement frames, not a big dump."""
import json
from hashlib import sha256
from itertools import combinations
from pathlib import Path
from radicals import (ZERO,ONE,ROT_SPINDLE,point,scalar,norm,distance,cmul,
                      frame,apply)

ROOT=Path(__file__).resolve().parent

def placements():
    g40=list(map(point,json.loads((ROOT/'g40.json').read_text())))
    g49=list(map(point,json.loads((ROOT/'g49.json').read_text())))
    rotated=[cmul(ROT_SPINDLE,p) for p in g40]
    if norm(ROT_SPINDLE)!=ONE or distance(g40[1],rotated[1])!=scalar(1296):
        raise ValueError('Incorrect spindle rotation')
    base=sorted(set(g40+rotated))
    if len(base)!=79:raise ValueError('Wrong base order')
    pairs=[(i,j) for i,j in combinations(range(40),2)
           if distance(g40[i],g40[j])==scalar(4752)]
    triangles=[t for t in combinations(range(49),3)
               if all(distance(g49[i],g49[j])==scalar(432)
                      for i,j in combinations(t,2))]
    terminals=list(map(point,[(0,0,12,0),(-6,0,-6,0),(6,0,-6,0)]))
    if len(pairs)!=59 or len(triangles)!=18:raise ValueError('Wrong local counts')
    g49_frames=[];forcing_frames=[]
    for host in (g40,rotated):
        for i,j in pairs:
            outer=frame(g49[0],g49[1],host[i],host[j],4752)
            if apply(outer,g49[0])!=host[i] or apply(outer,g49[1])!=host[j]:
                raise ValueError('Pair attachment mismatch')
            g49_frames.append(outer)
            for t in triangles:
                targets=[apply(outer,g49[v]) for v in t]
                f=frame(terminals[0],terminals[1],targets[0],targets[1],432)
                if apply(f,terminals[2])!=targets[2]:
                    f=frame(terminals[0],terminals[1],targets[0],targets[1],432,True)
                if any(apply(f,s)!=t for s,t in zip(terminals,targets)):
                    raise ValueError('Triangle attachment mismatch')
                forcing_frames.append(f)
    return base,g49,g49_frames,forcing_frames

def summary():
    base,g49,pair_frames,triangle_frames=placements()
    def canonical(frame):
        z,t,r=frame
        return [[[str(v) for v in xy] for xy in p] for p in (z,t)]+[r]
    data=json.dumps([canonical(f) for f in pair_frames+triangle_frames],separators=(',',':')).encode()
    return {'base_vertices':len(base),'pair_attachments':len(pair_frames),
            'triangle_attachments':len(triangle_frames),
            'vertex_upper_bound':79+118*47+2124*372,
            'all_frames_are_exact_isometries':True,
            'frame_sha256':sha256(data).hexdigest()}

def vertices(forcer_points):
    """Stream a finite point multiset; the graph uses its set of distinct points.

    The input must be the 375 paper-convention rows, with terminals first.
    The omitted attachment vertices already occur in the earlier components.
    """
    if len(forcer_points)!=375:raise ValueError('Wrong forcing gadget order')
    base,g49,pair_frames,triangle_frames=placements()
    yield from base
    for f in pair_frames:
        for p in g49[2:]:yield apply(f,p)
    for f in triangle_frames:
        for p in forcer_points[3:]:yield apply(f,point(p))

if __name__=='__main__':
    print(json.dumps(summary(),sort_keys=True))
