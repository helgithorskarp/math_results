#!/usr/bin/env python3
"""Generate compact common-atom profiles and fourteen exact strict second-fan points."""
from fractions import Fraction as F
from pathlib import Path
import json
import geometry as g

HERE=Path(__file__).resolve().parent
FIXED={'A':(2,0,90,-50),'B':(8,1,146,6),'D':(10,1,146,10)}
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
    first=fan((94,-46)); H=g.shape(7,first[1])[0][0]
    ordinary=[{'fan_index':i,'candidate_atom':3*(i-1) if i<=6 else 3*(i-6)} for i in range(1,13)]
    last=[{'candidate_atom':i,'polygon':g.shape(7,first[13])[0][i]} for i in (20,18)]
    out={'schema':1,'agent':'six-heesch-3','role':'researcher','tile_hexagons':7,
         'parameter_open_interval':['98','156'],
         'fixed':{k:FIXED[k] for k in ('A','B','D')},'forced_pose':P,
         'ordinary_first_fan_atoms':ordinary,'ordinary_hexagon':H,'last_first_fan_atoms':last,
         'interval_profiles':[{'blocker_atom':0,'interval':['92','108']},
                              {'blocker_atom':1,'interval':['98','104']},
                              {'blocker_atom':1,'interval':['100','108']}],
         'second_fan':[]}
    for i,p in enumerate(fan((122,-18))):
        owner='D' if i in (0,1,13) else 'P'
        out['second_fan'].append({'pose':p,'blocker':owner,
                                 'strict':strict_witness(p,P if owner=='P' else FIXED[owner])})
    return out


if __name__=='__main__':
    value=certificate()
    (HERE/'certificate.json').write_text(json.dumps(value,indent=2)+'\n')
    print(json.dumps({'convex_interval_types':3,'strict_second_fan_points':14}))
