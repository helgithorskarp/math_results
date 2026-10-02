#!/usr/bin/env python3
"""Exact real-parameter two-gap obstruction, standard library only."""
from copy import deepcopy
from fractions import Fraction as F
from hashlib import sha256
from itertools import combinations
from pathlib import Path
import argparse, json
import geometry as g

HERE = Path(__file__).resolve().parent


def direction(p):
    rays = ((1,0),(3,1),(1,1),(0,1),(-1,1),(-3,1),(-1,0),(-3,-1),(-1,-1),(0,-1),(1,-1),(3,-1))
    found = [i for i,r in enumerate(rays) if g.cross(p,r) == 0 and p[0]*r[0]+p[1]*r[1] > 0]
    g.require(len(found) == 1, 'edge outside exact ray alphabet')
    return found[0]


def corners(cycle):
    rays = [direction(g.sub(cycle[(i+1)%len(cycle)],p)) for i,p in enumerate(cycle)]
    return {p:(6-((rays[i]-rays[i-1]+6)%12-6),rays[i],(rays[i-1]+6)%12) for i,p in enumerate(cycle)}


def fan(point, metadata):
    poses = set()
    for v,(angle,start,end) in metadata.items():
        if angle != 2:
            continue
        for f in (0,1):
            a = (10-start if not f else 10+end)%12
            g.require(a%2 == 0, 'derive unexpected odd rotation')
            x,y = g.point((a,f,0,0),v)
            poses.add((a,f,point[0]-x,point[1]-y))
    x,y = point
    ordered = [(2,0,x+4-4*j,y-4-4*j) for j in range(7)] + [(8,1,x+8+4*j,y+4*j) for j in range(7)]
    g.require(len(poses) == 14 and poses == set(ordered), 'complete all-motion fan differs')
    return ordered


def hull(points):
    points = sorted(set(points))
    def half(order):
        result = []
        for p in order:
            while len(result) >= 2 and g.turn(result[-2],result[-1],p) <= 0:
                result.pop()
            result.append(p)
        return result
    return tuple(half(points)[:-1] + half(reversed(points))[:-1])


def collision_interval(a,b):
    """Exact open interval of t with int(a) meeting int(b+(t,0))."""
    h = hull(g.sub(p,q) for p in a for q in b)
    if not min(y for x,y in h) < 0 < max(y for x,y in h):
        return None
    xs = []
    for i,p in enumerate(h):
        q = h[(i+1)%len(h)]
        if p[1] == 0:
            xs.append(F(p[0]))
        if p[1]*q[1] < 0:
            xs.append(F(p[0])-F(p[1])*F(q[0]-p[0],q[1]-p[1]))
    g.require(len(xs) >= 2 and min(xs) < max(xs), 'degenerate projected interior')
    return min(xs),max(xs)


def interval_union(intervals):
    result = []
    for lo,hi in sorted(intervals):
        if result and lo < result[-1][1]:
            result[-1] = (result[-1][0],max(result[-1][1],hi))
        else:
            result.append((lo,hi))
    return result


def strict(row, blocker):
    data = row['strict']
    a = g.shape(7,tuple(row['pose']))[0][data['candidate_atom']]
    b = g.shape(7,blocker)[0][data['blocker_atom']]
    p = tuple(F(t) for t in data['point'])
    signs = [g.turn(v,poly[(i+1)%len(poly)],p) for poly in (a,b) for i,v in enumerate(poly)]
    g.require(all(s > 0 for s in signs), 'point not strictly inside both atoms')
    return min(signs)


def verify(data):
    g.require(data['schema'] == 1 and data['tile_hexagons'] == 7, 'wrong shape')
    g.require(data['parameter_open_interval'] == ['98','156'], 'wrong parameter range')
    fixed = {k:tuple(p) for k,p in data['fixed'].items()}
    g.require(fixed == {'A':(2,0,90,-50),'B':(8,1,146,6),'D':(10,1,146,10)}, 'fixed configuration changed')
    P = tuple(data['forced_pose']); g.require(P == (2,0,98,-50), 'forced pose changed')
    cycle,_ = g.boundary(g.atoms(7)); meta = corners(cycle)
    g.require(min(v[0] for v in meta.values()) == 2, 'minimum angle differs')
    g.require({v for v,a in meta.items() if a[0] == 2} == {(4+8*j,4) for j in range(7)}, 'corner list differs')
    for host,local,point in [('A',(8,0),(94,-46)),('B',(48,0),(122,-18))]:
        g.require(g.point(fixed[host],local) == point, 'host vertex differs')
        boundary,_ = g.boundary(g.shape(7,fixed[host])[0])
        g.require(corners(boundary)[point] == (10,0,10), 'host exposed wedge differs')
    first = fan((94,-46),meta); second = fan((122,-18),meta)
    ordinary = data['ordinary_first_fan_atoms']
    g.require(sorted(r['fan_index'] for r in ordinary) == list(range(1,13)), 'ordinary fan role missing or repeated')
    H = tuple(tuple(p) for p in data['ordinary_hexagon'])
    for r in ordinary:
        g.require(set(g.shape(7,first[r['fan_index']])[0][r['candidate_atom']]) == set(H), 'ordinary common hexagon differs')
    shapes = [H]
    for r in data['last_first_fan_atoms']:
        p = tuple(tuple(v) for v in r['polygon'])
        g.require(set(p) == set(g.shape(7,first[13])[0][r['candidate_atom']]), 'last fan atom differs')
        shapes.append(p)
    g.require(len(shapes) == 3 and len(data['interval_profiles']) == 3, 'incomplete interval types')
    moving = g.shape(7,(6,1,0,-52))[0]
    intervals = []
    controls = 0
    for i,row in enumerate(data['interval_profiles']):
        a = shapes[i]; base_atom = row['blocker_atom']
        z = collision_interval(a,moving[base_atom])
        g.require(z == tuple(F(t) for t in row['interval']), 'projected collision interval changed')
        shifted = []
        for j in range(7):
            translated = tuple((x-8*j,y) for x,y in moving[base_atom])
            g.require(set(translated) == set(moving[3*j+base_atom]), 'blocker atom does not translate along strip')
            zz = collision_interval(a,translated)
            g.require(zz == (z[0]+8*j,z[1]+8*j), 'translation interval does not shift exactly')
            shifted.append(zz)
        intervals.append(shifted)
        # These exact rational controls are separate from the real-parameter derivation.
        for t in (z[0]-F(1,2),z[0],(z[0]+z[1])/2,z[1],z[1]+F(1,2)):
            shifted_atom = tuple((x+t,y) for x,y in moving[base_atom])
            g.require(g.convex_intersection(a,shifted_atom,False) == (z[0] < t < z[1]), 'interval disagrees with separate exact interior test')
            controls += 1
    ordinary_union = interval_union(intervals[0]); last_union = interval_union(intervals[1]+intervals[2])
    g.require(ordinary_union == [(F(92),F(156))] and last_union == [(F(98),F(156))], 'continuous open interval has an uncovered join')
    rows = data['second_fan']
    g.require(len(rows) == 14 and {tuple(r['pose']) for r in rows} == set(second), 'second fan incomplete')
    least = None
    for r in rows:
        index = second.index(tuple(r['pose']))
        owner = 'D' if index in (0,1,13) else 'P'
        g.require(r['blocker'] == owner, 'second-fan blocker differs')
        value = strict(r,fixed['D'] if owner == 'D' else P)
        least = value if least is None else min(value,least)
    packing_controls = 0
    for t in (100,108,116,124,132,140,148):
        poses = [*fixed.values(),(6,1,t,-52)]
        g.require(all(not g.pair(7,a,b)[0] for a,b in combinations(poses,2)), 'selected nonvacuous motif does not pack')
        packing_controls += 1
    return {'actual_agent':'six-heesch-3','role':'researcher','parameter_open_interval':['98','156'],
            'ordinary_common_hexagon_candidates':12,'complete_fan_candidates_each':14,
            'base_convex_translation_interval_types':3,'translated_atom_intervals_checked':21,
            'ordinary_collision_union':[['92','156']],'last_candidate_collision_union':[['98','156']],
            'strict_second_fan_points':14,'least_second_fan_cross_product':str(least),
            'exact_rational_interval_controls':controls,'nonvacuous_fixed_motif_controls':packing_controls,
            'arbitrary_new_tile_motions_allowed':True,'holes_elsewhere_allowed':True,
            'mate_or_grid_premise_required':False,'shape_Heesch_upper_claimed':False,
            'shared_geometry':True,'formalized':False,'independently_reviewed':False}


def damaged_controls(data):
    a=deepcopy(data);a['ordinary_first_fan_atoms'].pop()
    b=deepcopy(data);b['interval_profiles'][1]['interval'][0]='97'
    c=deepcopy(data);c['second_fan'][0]['strict']['point']=['0','0']
    d=deepcopy(data);d['interval_profiles'][1]['blocker_atom']=2
    for broken in (a,b,c,d):
        try:
            verify(broken)
        except (ValueError,KeyError,IndexError,TypeError):
            continue
        raise ValueError('damaged certificate accepted')
    return 4


if __name__ == '__main__':
    p=argparse.ArgumentParser();p.add_argument('--out');args=p.parse_args()
    raw=(HERE/'certificate.json').read_bytes();data=json.loads(raw)
    out=verify(data);out['damaged_certificates_rejected']=damaged_controls(data)
    out['certificate_sha256']=sha256(raw).hexdigest()
    out['stable_evidence_sha256']=sha256(json.dumps(out,sort_keys=True,separators=(',',':')).encode()).hexdigest()
    text=json.dumps(out,indent=2)+'\n'
    if args.out:Path(args.out).write_text(text)
    print(text,end='')
