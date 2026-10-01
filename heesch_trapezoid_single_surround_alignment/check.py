"""Exact uniform angle/type certificate for the single-surround proof.

Pure Python standard library. This checks finite arithmetic/type obligations;
written analytic coincidence, whole-flat and endpoint-isometry arguments
remain mathematical trust boundaries. No solver or previous executable.
"""
from itertools import product
from pathlib import Path
import argparse
import copy
import hashlib
import json
import resource
import sys
import time

if sys.flags.optimize:
    raise RuntimeError('Optimized Python is unsupported: ordinary assertions required')
HERE = Path(__file__).resolve().parent
RAYS = ((1,0),(1,1),(0,1),(-1,2),(-1,1),(-2,1),
        (-1,0),(-1,-1),(0,-1),(1,-2),(1,-1),(2,-1))
EDGE_DIRECTIONS = ((1,0),(-1,2),(-1,0),(0,-1))
SIDE_FACTORS = ((0,1),(1,0),(-1,1),(2,0))  # c+m*n
SIDE_STATES = (-1,0,1,1)
NAMES = ('A','B','C','D')


def det(a,b): return a[0]*b[1]-a[1]*b[0]
def norm(a): return a[0]**2+a[0]*a[1]+a[1]**2
def dot2(a,b): return 2*a[0]*b[0]+a[0]*b[1]+a[1]*b[0]+2*a[1]*b[1]
def canonical(value): return json.dumps(value,sort_keys=True,separators=(',',':')).encode()


def compositions(total, allowed):
    if total == 0:
        return [()]
    return [(angle,)+rest for angle in sorted(allowed) if angle<=total
            for rest in compositions(total-angle,allowed)]


def corner_catalog():
    result=[]
    for i,name in enumerate(NAMES):
        incoming=EDGE_DIRECTIONS[i-1];outgoing=EDGE_DIRECTIONS[i]
        reverse=tuple(-x for x in incoming)
        angle=30*((RAYS.index(reverse)-RAYS.index(outgoing))%12)
        result.append({'name':name,'angle':angle,'ordered_states':[SIDE_STATES[i],SIDE_STATES[i-1]],
                       'incoming_direction':list(incoming),'outgoing_direction':list(outgoing)})
    return result


def labelled_types():
    result={}
    for corner in corner_catalog():
        angle=corner['angle'];s=tuple(corner['ordered_states'])
        result.setdefault(angle,set()).update((s,s[::-1]))
    result[180]={(-1,-1),(1,1)}
    return {angle:tuple(sorted(states)) for angle,states in sorted(result.items())}


def state_words(angles, outside):
    types=labelled_types();successful=[]
    for states in product(*(types[a] for a in angles)):
        if states[0][0]+outside[0] or states[-1][1]+outside[1]:
            continue
        if any(a[1]+b[0] for a,b in zip(states,states[1:])):
            continue
        successful.append({'angles':list(angles),'states':[list(s) for s in states]})
    return successful


def small_gap_table():
    result=[]
    for angle in (30,60,90,120,150):
        for outside in product((-1,0,1),repeat=2):
            words=[]
            for parts in compositions(angle,(60,90,120)):
                words.extend(state_words(parts,outside))
            result.append({'angle':angle,'outside_states':list(outside),'words':words})
    return result


def certificate():
    partitions=compositions(180,(60,90,120,180))
    flat_angles=[parts for parts in partitions if parts[0]==parts[-1]==90]
    flat_words=[word for parts in flat_angles for word in state_words(parts,(0,0))]
    old_cases=[{'flat_word':word,'old_labelled_position':position}
               for word in flat_words for position in (0,1)]
    return {'family':{'minimum_integer_width':8,'amplitude':'1/100',
                      'side_directions':[list(d) for d in EDGE_DIRECTIONS],
                      'side_factors_c_plus_mn':[list(f) for f in SIDE_FACTORS],
                      'side_states':list(SIDE_STATES)},
            'corner_catalog':corner_catalog(),
            'regular_label_types':[
                {'kind':'bottom','angle':180,'states':[-1,-1],'count_c_plus_mn':[-1,1]},
                {'kind':'top','angle':180,'states':[1,1],'count_c_plus_mn':[-2,1]},
                {'kind':'left','angle':180,'states':[1,1],'count_c_plus_mn':[1,0]}],
            'remaining_180_compositions':[list(parts) for parts in partitions],
            'smooth_flat_angle_compositions':[list(parts) for parts in flat_angles],
            'smooth_flat_typed_words':flat_words,
            'old_labelled_flat_cases':old_cases,
            'small_gap_table':small_gap_table()}


def verify(c):
    f=c['family'];minimum=f['minimum_integer_width']
    assert minimum==8 and f['amplitude']=='1/100'
    directions=tuple(map(tuple,f['side_directions']))
    factors=tuple(map(tuple,f['side_factors_c_plus_mn']))
    assert directions==EDGE_DIRECTIONS and f['side_states']==list(SIDE_STATES)
    assert factors==SIDE_FACTORS
    assert all(type(z) is int for pair in factors for z in pair)
    assert all(m>=0 and constant+minimum*m>0 for constant,m in factors)
    for coefficient in (0,1):
        assert tuple(sum(factors[i][coefficient]*directions[i][axis] for i in range(4)) for axis in (0,1))==(0,0)
    for a,b in zip(RAYS,RAYS[1:]+RAYS[:1]):
        assert det(a,b)>0 and dot2(a,b)>0
        assert dot2(a,b)**2==3*norm(a)*norm(b)  # exact positive30-degree angle
    assert all(det(a,b)>0 for a,b in zip(directions,directions[1:]+directions[:1]))
    catalog=corner_catalog();assert c['corner_catalog']==catalog
    assert [row['angle'] for row in catalog]==[60,90,90,120]
    assert labelled_types()=={60:((-1,1),(1,-1)),90:((-1,0),(0,-1),(0,1),(1,0)),
                             120:((1,1),),180:((-1,-1),(1,1))}
    regular=certificate()['regular_label_types'];assert c['regular_label_types']==regular
    assert all(row['count_c_plus_mn'][1]>=0 and
               row['count_c_plus_mn'][0]+minimum*row['count_c_plus_mn'][1]>0 for row in regular)
    assert [4+sum(row['count_c_plus_mn'][0] for row in regular),
            sum(row['count_c_plus_mn'][1] for row in regular)]==[2,2]
    partitions=compositions(180,labelled_types())
    assert c['remaining_180_compositions']==[list(p) for p in partitions] and len(partitions)==5
    flat_angles=[p for p in partitions if p[0]==p[-1]==90]
    assert flat_angles==[(90,90)]
    assert c['smooth_flat_angle_compositions']==[[90,90]]
    flat_words=[w for p in flat_angles for w in state_words(p,(0,0))]
    assert c['smooth_flat_typed_words']==flat_words and len(flat_words)==2
    assert c['old_labelled_flat_cases']==[{'flat_word':word,'old_labelled_position':position}
                                         for word in flat_words for position in (0,1)]
    assert len(c['old_labelled_flat_cases'])==4
    table=small_gap_table();assert c['small_gap_table']==table and len(table)==45
    possible=sum(bool(row['words']) for row in table)
    assert possible==13
    assert not next(row['words'] for row in table if row['angle']==120 and row['outside_states']==[1,1])
    assert all(not row['words'] for row in table if row['angle']==60 and
               row['outside_states'] in ([-1,-1],[1,1]))
    return {'status':'EXACT_UNIFORM_SINGLE_SURROUND_STAR_TYPES_VERIFIED',
            'parameter_domain':'Every integer n>=8','genuine_corner_angles':[60,90,90,120],
            'positive_affine_side_factors':4,'regular_label_count':'2*n+2',
            'exact_30_degree_ray_steps':12,'remaining_smooth_star_angle_compositions':5,
            'smooth_flat_possible_angle_compositions':1,'smooth_flat_typed_words':2,
            'old_labelled_flat_cases_requiring_whole_mate':4,
            'small_gap_boundary_state_cases':45,'small_gap_cases_with_a_word':possible,
            'small_gap_cases_without_a_word':45-possible,
            'certificate_canonical_sha256':hashlib.sha256(canonical(c)).hexdigest()}


def controls(c):
    damaged=[]
    x=copy.deepcopy(c);x['family']['side_factors_c_plus_mn'][0]=[-8,1];damaged.append(x)
    x=copy.deepcopy(c);x['family']['side_directions'][1]=[-1,1];damaged.append(x)
    x=copy.deepcopy(c);x['corner_catalog'][0]['ordered_states']=[1,1];damaged.append(x)
    x=copy.deepcopy(c);x['regular_label_types'][1]['count_c_plus_mn']=[-3,1];damaged.append(x)
    x=copy.deepcopy(c);x['remaining_180_compositions'].pop();damaged.append(x)
    x=copy.deepcopy(c);x['old_labelled_flat_cases'].pop();damaged.append(x)
    x=copy.deepcopy(c)
    row=next(r for r in x['small_gap_table'] if r['angle']==120 and r['outside_states']==[1,1])
    row['words']=[{'angles':[120],'states':[[-1,-1]]}];damaged.append(x)
    for x in damaged:
        try:
            verify(x)
        except AssertionError:
            continue
        raise AssertionError('Malformed mathematical certificate accepted')
    return len(damaged)


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--controls',action='store_true')
    parser.add_argument('--expected');args=parser.parse_args();start=time.monotonic()
    data=json.loads((HERE/'certificate.json').read_text());report=verify(data)
    report['malformed_controls_rejected']=controls(data) if args.controls else 0
    if args.expected:
        assert report==json.loads(Path(args.expected).read_text())
    print(json.dumps(dict(report,seconds=time.monotonic()-start,
                          rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss),indent=2))
