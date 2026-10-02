#!/usr/bin/env python3
"""Replay the finite fan list and rational strict-point certificate, no solver."""
from copy import deepcopy
from fractions import Fraction as F
from hashlib import sha256
from itertools import combinations
from pathlib import Path
import argparse,json
import geometry as g

HERE=Path(__file__).resolve().parent


def direction(p):
    rays=((1,0),(3,1),(1,1),(0,1),(-1,1),(-3,1),(-1,0),(-3,-1),(-1,-1),(0,-1),(1,-1),(3,-1))
    choices=[i for i,r in enumerate(rays) if g.cross(p,r)==0 and p[0]*r[0]+p[1]*r[1]>0]
    g.require(len(choices)==1,'edge outside exact 30-degree ray alphabet')
    return choices[0]


def corners(cycle):
    rays=[direction(g.sub(cycle[(i+1)%len(cycle)],v)) for i,v in enumerate(cycle)]
    return {v:(6-((rays[i]-rays[i-1]+6)%12-6),rays[i],(rays[i-1]+6)%12) for i,v in enumerate(cycle)}


def anchored_fan(point,metadata):
    # The host leaves [10,12] in units of30degrees. A copy must have
    # exactly a60degree corner there. Rotations are forced by the rays.
    poses=set()
    for v,(angle,start,end) in metadata.items():
        if angle!=2:continue
        for reflected in (0,1):
            a=(10-start if not reflected else 10+end)%12
            g.require(a%2==0,'unexpected odd rotation; derive it rather than round')
            x,y=g.point((a,reflected,0,0),v)
            poses.add((a,reflected,point[0]-x,point[1]-y))
    return poses


def strict(row,blocker):
    data=row['strict'];g.require(data is not None,'missing strict collision certificate')
    ca=g.shape(7,tuple(row['pose']))[0][data['candidate_atom']]
    ba=g.shape(7,blocker)[0][data['blocker_atom']]
    point=tuple(F(v) for v in data['point'])
    signs=[g.turn(v,poly[(i+1)%len(poly)],point) for poly in (ca,ba) for i,v in enumerate(poly)]
    g.require(all(s>0 for s in signs),'point not strictly inside both atoms')
    return min(signs)


def verify(data):
    g.require(data['schema']==1 and data['tile_hexagons']==7,'wrong geometry')
    fixed={k:tuple(p) for k,p in data['fixed'].items()};P=tuple(data['forced_pose'])
    g.require(fixed=={'A':(2,0,90,-50),'B':(8,1,146,6),'C':(6,1,140,-52),'D':(10,1,146,10)},'motif changed')
    g.require(P==(2,0,98,-50),'forced copy changed')
    for a,b in combinations(fixed.values(),2):g.require(not g.pair(7,a,b)[0],'fixed copies overlap')
    g.require(all(not g.pair(7,P,p)[0] for p in fixed.values()),'forced copy already conflicts with motif')
    cycle,_=g.boundary(g.atoms(7));meta=corners(cycle)
    g.require(min(v[0] for v in meta.values())==2,'minimum angle is not60 degrees')
    g.require({v for v,angles in meta.items() if angles[0]==2}=={(4+8*j,4) for j in range(7)},'60-degree corner list differs')
    expected_stars=[('A',(8,0),(94,-46)),('B',(48,0),(122,-18))]
    for star,(host,local,point) in zip(data['stars'],expected_stars):
        g.require((star['host'],tuple(star['prototype_vertex']),tuple(star['point']))==(host,local,point),'host star changed')
        g.require(g.point(fixed[host],local)==point,'host vertex does not land at star')
        boundary,_=g.boundary(g.shape(7,fixed[host])[0]);at=corners(boundary)[point]
        g.require(at==(10,0,10),'host not300deg with exposed60deg rays10..12')
        g.require(star['gap_steps']==2 and star['start_step']==10,'star gap differs')
    g.require(len(data['stars'])==2,'wrong star count')
    minimum=None;collisions=0
    for key,star_index in (('first_fan',0),('second_fan',1)):
        rows=data[key];point=expected_stars[star_index][2]
        generated=anchored_fan(point,meta)
        g.require(len(rows)==14 and len(generated)==14,'incomplete/duplicate fan domain')
        g.require({tuple(r['pose']) for r in rows}==generated,'fan row set differs from complete all-motion domain')
        for r in rows:
            p=tuple(r['pose']);owner=r['blocker']
            if key=='first_fan' and p==P:
                g.require(owner is None and r['strict'] is None,'forced positive slot changed')
                continue
            allowed={'C'} if key=='first_fan' else {'D','P'}
            g.require(owner in allowed,'collision owner absent or not licensed at this step')
            sign=strict(r,P if owner=='P' else fixed[owner]);collisions+=1
            minimum=sign if minimum is None else min(minimum,sign)
    g.require(collisions==27,'collision count changed')
    return {'actual_agent':'six-heesch-3','role':'researcher','fixed_copy_count':4,
        'fan_candidates_each':14,'strict_collision_witnesses':27,'least_positive_cross_product':str(minimum),
        'first_star_unique_supplier':list(P),'second_star_no_supplier_after_forcing':True,
        'arbitrary_motions_allowed':True,'reflections_allowed':True,'holes_allowed':True,
        'mate_or_frame_premise_required':False,'grid_assumption_required':False,
        'shape_Heesch_upper_claimed':False,'shared_geometry':True,'formalized':False,'independently_reviewed':False}


def damaged_controls(data):
    copies=[]
    a=deepcopy(data);a['second_fan'].pop();copies.append(a)
    a=deepcopy(data);a['first_fan'][1]['strict']['point']=['0','0'];copies.append(a)
    a=deepcopy(data);a['second_fan'][4]['blocker']=None;copies.append(a)
    for d in copies:
        try:verify(d)
        except (ValueError,KeyError,IndexError,TypeError):continue
        raise ValueError('damaged negative certificate accepted')
    return len(copies)


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--out');args=parser.parse_args()
    raw=(HERE/'certificate.json').read_bytes();data=json.loads(raw)
    result=verify(data);result['damaged_certificates_rejected']=damaged_controls(data)
    result['certificate_sha256']=sha256(raw).hexdigest()
    result['stable_evidence_sha256']=sha256(json.dumps(result,sort_keys=True,separators=(',',':')).encode()).hexdigest()
    text=json.dumps(result,indent=2)+'\n'
    if args.out:Path(args.out).write_text(text)
    print(text,end='')
