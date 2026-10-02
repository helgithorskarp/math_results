#!/usr/bin/env python3
"""Generate only 27 strict interior witnesses for the explicit two-gap motif."""
from fractions import Fraction as F
from pathlib import Path
import json
import geometry as g

HERE=Path(__file__).resolve().parent
FIXED={'A':(2,0,90,-50),'B':(8,1,146,6),
       'C':(6,1,140,-52),'D':(10,1,146,10)}
P=(2,0,98,-50)


def fan(v):
    x,y=v
    return [(2,0,x+4-4*j,y-4-4*j) for j in range(7)]+[(8,1,x+8+4*j,y+4*j) for j in range(7)]


def clip(poly,edge):
    a,b=edge; result=[]
    for i,p in enumerate(poly):
        q=poly[(i+1)%len(poly)];u,v=g.turn(a,b,p),g.turn(a,b,q)
        if u>=0:result.append(p)
        if (u<0 and v>0) or (u>0 and v<0):
            t=F(u,u-v)
            result.append(tuple(p[k]+t*(q[k]-p[k]) for k in (0,1)))
    return result


def strict_witness(p,q):
    for i,a in enumerate(g.shape(7,p)[0]):
        for j,b in enumerate(g.shape(7,q)[0]):
            if not g.boxes_meet(g.box(a),g.box(b),False):continue
            polygon=[tuple(F(x) for x in v) for v in a]
            for k,v in enumerate(b):
                if not polygon:break
                polygon=clip(polygon,(v,b[(k+1)%len(b)]))
            if not polygon or g.twice_area(polygon)<=0:continue
            point=tuple(sum(v[k] for v in polygon)/len(polygon) for k in (0,1))
            if all(g.turn(v,s[(k+1)%len(s)],point)>0 for s in (a,b) for k,v in enumerate(s)):
                return {'candidate_atom':i,'blocker_atom':j,'point':[str(x) for x in point]}
    raise ValueError('no strict interior witness for prescribed collision')


def certificate():
    out={'schema':1,'agent':'six-heesch-3','role':'researcher','tile_hexagons':7,
         'fixed':FIXED,'forced_pose':P,'stars':[{'host':'A','prototype_vertex':(8,0),'point':(94,-46),'gap_steps':2,'start_step':10},
         {'host':'B','prototype_vertex':(48,0),'point':(122,-18),'gap_steps':2,'start_step':10}],
         'first_fan':[],'second_fan':[]}
    for i,p in enumerate(fan((94,-46))):
        owner=None if i==0 else 'C'
        out['first_fan'].append({'pose':p,'blocker':owner,'strict':None if owner is None else strict_witness(p,FIXED[owner])})
    for i,p in enumerate(fan((122,-18))):
        owner='D' if i in (0,1,13) else 'P'
        blocker=P if owner=='P' else FIXED[owner]
        out['second_fan'].append({'pose':p,'blocker':owner,'strict':strict_witness(p,blocker)})
    return out


if __name__=='__main__':
    value=certificate()
    (HERE/'certificate.json').write_text(json.dumps(value,indent=2)+'\n')
    print(json.dumps({'strict_interior_certificates':27,'fixed_copy_count':4,'fan_candidates_each':14}))
