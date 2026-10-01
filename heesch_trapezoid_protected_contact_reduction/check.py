"""Exact arithmetic for the written protected-contact reduction.

Actual author six-heesch-3, researcher. No solver, constructor, neighborhood
catalog or external geometry code is imported. Read proof.md for geometric
bridges and extra future-surround hypotheses.
"""
from fractions import Fraction as F
from math import gcd
from copy import deepcopy
from pathlib import Path
import argparse
import hashlib
import json
import resource
import sys
import time

if sys.flags.optimize:
    raise RuntimeError('Ordinary Python with assertions is required')
OUT=Path(__file__).resolve().parent

def add(a,b):return tuple(x+y for x,y in zip(a,b))

def neg(a):return tuple(-x for x in a)

def sub(a,b):return add(a,neg(b))

def det(a,b):return a[0]*b[1]-a[1]*b[0]

def norm(a):return a[0]*a[0]+a[0]*a[1]+a[1]*a[1]

def motion(point,h,k):
    q,r=point
    if h:q,r=add(q,r),neg(r)
    for unused in range(k):q,r=neg(r),add(q,r)
    return q,r

def affine_quad(h,k):
    poly=[((0,0),(-1,0)),((0,1),(-1,0)),((-1,1),(1,0)),((0,0),(1,0))]
    return [motion(p,h,k) for p in (poly[::-1] if h else poly)]

def audit():
    rows=[];directions=set()
    for h in (0,1):
        for k in range(6):
            poly=affine_quad(h,k)
            for index,(a,b) in enumerate(zip(poly,poly[1:]+poly[:1])):
                edge=tuple(sub(y,x) for x,y in zip(a,b))
                at8=tuple(c+8*m for c,m in edge)
                divisor=gcd(*at8);assert divisor>0
                primitive=tuple(x//divisor for x in at8)
                nonzero=next(i for i,x in enumerate(primitive) if x)
                factor=tuple(F(x,primitive[nonzero]) for x in edge[nonzero])
                assert all(tuple(x*t for t in factor)==v for x,v in zip(primitive,edge))
                assert factor[1]>=0 and factor[0]+8*factor[1]>0
                assert norm(primitive) in (1,3)
                directions.add(primitive)
                rows.append({'orientation':[h,k],'edge':index,'direction':list(primitive),
                             'positive_width_factor':[str(x) for x in factor]})
    assert len(rows)==48 and len(directions)==12
    determinants=sorted({abs(det(a,b)) for a in directions for b in directions})
    assert determinants==[0,1,2,3]
    slack=F(1,3*8);boundary=slack/2
    assert slack==F(1,24) and boundary==F(1,48)
    maximum_d=33;profile=F(1,1600)
    assert boundary/maximum_d>profile
    assert boundary/(maximum_d+1)<=profile  # bound's limit, not optimality
    return {'oriented_primitive_directions':[list(x) for x in sorted(directions)],
            'width_affine_edge_checks':rows,'determinant_magnitudes':determinants,
            'maximum_vertex_denominator_multiplier':3,
            'maximum_intersection_vertices':8,'grid_integer_slack_lower':str(slack),
            'grid_integer_boundary_distance_lower':str(boundary),
            'sufficient_common_translation_denominators':[1,maximum_d],
            'worst_certified_boundary_distance_lower':str(boundary/maximum_d),
            'profile_displacement_upper':str(profile)}

def transform(point, h, k):
    q, r = point
    if h:
        q, r = add(q, r), neg(r)
    for unused in range(k):
        q, r = neg(r), add(q, r)
    return q, r

def constant_ray(q, r):
    return (q, 0), (r, 0)

WEST = constant_ray(-1, 0)

UP = constant_ray(-1, 2)

DOWN = constant_ray(1, -2)

B = ((0, 1), (-1, 0))

C = ((-1, 1), (1, 0))

CORNER_DATA = [
    {'name': 'B', 'point': B, 'sign': -1, 'flat_ray': UP},
    {'name': 'C', 'point': C, 'sign': +1, 'flat_ray': DOWN},
]

def providers(endpoint, flat_ray, required_sign, corners):
    answer = []
    trials = 0
    for corner in corners:
        for h in (0, 1):
            for k in range(6):
                trials += 1
                if (corner['sign'] != required_sign
                    or transform(WEST, h, k) != WEST
                    or transform(corner['flat_ray'], h, k) != flat_ray):
                    continue
                translation = tuple(sub(x, y) for x, y in
                                    zip(endpoint, transform(corner['point'], h, k)))
                answer.append({'prototype_corner': corner['name'],
                               'pose_affine': [h, k, *map(list, translation)]})
    return answer, trials

def check(corners=CORNER_DATA):
    lower, first = providers(B, DOWN, +1, corners)
    upper, second = providers(C, UP, -1, corners)
    assert lower == [{'prototype_corner': 'C',
                      'pose_affine': [0, 0, [1, 0], [-2, 0]]}]
    assert upper == [{'prototype_corner': 'B',
                      'pose_affine': [0, 0, [-1, 0], [2, 0]]}]
    return {'lower_flat_endpoint': lower, 'upper_flat_endpoint': upper,
            'corner_orientation_trials': first+second,
            'forced_lower_pose': [0, 0, 1, -2],
            'forced_upper_pose': [0, 0, -1, 2]}

def controls():
    rejected = 0
    # A wrong physical sign licenses a reflected filler instead of the
    # required opposite unit arc. This must change, and fail, the audit.
    wrong_sign = deepcopy(CORNER_DATA)
    wrong_sign[1]['sign'] = -1
    # Moving a labelled corner changes the endpoint-fixed translation.
    wrong_endpoint = deepcopy(CORNER_DATA)
    wrong_endpoint[1]['point'] = ((0, 1), (1, 0))
    # A width-dependent labelled coordinate must not be reported as a
    # fixed uniform translate; checking only a sample width would miss it.
    wrong_slope = deepcopy(CORNER_DATA)
    wrong_slope[1]['point'] = ((-1, 2), (1, 0))
    for corrupted in (wrong_sign, wrong_endpoint, wrong_slope):
        try:
            check(corrupted)
        except AssertionError:
            rejected += 1
        else:
            raise AssertionError('A malformed endpoint control was accepted')
    assert rejected == 3
    return rejected

# These finite checks support the written geometric proofs; they do not
# encode arbitrary real packings or substitute for the protected-stage proof.


def canonical(value):
    return json.dumps(value,sort_keys=True,separators=(',',':')).encode()


def certificate():
    return {'minimum_width':8,'physical_profile_amplitude':'1/100',
            'grid_margin':audit(),'endpoint_fillers':check()}


def verify_certificate(data):
    assert data==certificate(),'Geometric arithmetic certificate mismatch'


def malformed_certificate_controls():
    data=certificate();cases=[]
    wrong=deepcopy(data);wrong['grid_margin']['determinant_magnitudes']=[0,1,2];cases.append(wrong)
    wrong=deepcopy(data);wrong['grid_margin']['sufficient_common_translation_denominators']=[1,34];cases.append(wrong)
    wrong=deepcopy(data);wrong['grid_margin']['oriented_primitive_directions'].pop();cases.append(wrong)
    wrong=deepcopy(data);wrong['grid_margin']['width_affine_edge_checks'][0]['positive_width_factor']=['0','-1'];cases.append(wrong)
    rejected=0
    for corrupted in cases:
        try:verify_certificate(corrupted)
        except AssertionError:rejected+=1
        else:raise AssertionError('Malformed geometric certificate accepted')
    assert rejected==4
    return rejected


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--certificate',type=Path,default=OUT/'certificate.json')
    parser.add_argument('--controls',action='store_true')
    parser.add_argument('--expected',type=Path)
    args=parser.parse_args();start=time.monotonic()
    data=json.loads(args.certificate.read_text());verify_certificate(data)
    result={'agent':'six-heesch-3','role':'researcher',
            'status':'EXACT_UNIFORM_PROTECTED_CONTACT_ARITHMETIC_VERIFIED',
            'parameter_domain':'Every integer width n>=8',
            'uniform_affine_edge_checks':48,'oriented_primitive_directions':12,
            'maximum_primitive_direction_determinant':3,
            'endpoint_corner_orientation_cases':48,
            'integer_grid_physical_interior_margin':'1/48',
            'sufficient_common_translation_denominators':[1,33],
            'worst_grid_physical_interior_margin':'1/1584',
            'profile_displacement_upper':'1/1600',
            'certificate_canonical_sha256':hashlib.sha256(canonical(data)).hexdigest()}
    if args.controls:
        result['malformed_controls_rejected']=controls()+malformed_certificate_controls()
    if args.expected:
        expected=json.loads(args.expected.read_text())
        assert {key:result[key] for key in expected}==expected,'Expected arithmetic report mismatch'
    result.update(seconds=time.monotonic()-start,rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()
