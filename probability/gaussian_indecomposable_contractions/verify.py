#!/usr/bin/env python3
"""Exact small controls for the indecomposable-contraction reduction.

The general Brehm/finite-placement argument is written in PROOF.md. This
program exhausts the complete intermediate configurations of four specified
face-anchored fixtures. No Gaussian integral or general mesh is computed.
"""
import argparse
from fractions import Fraction as F
import hashlib
from itertools import combinations, product
import json
from math import lcm
from pathlib import Path


def require(condition, message):
    if not condition:
        raise ValueError(message)


def sub(x, y):
    return tuple(a - b for a, b in zip(x, y))


def dot(x, y):
    return sum(a * b for a, b in zip(x, y))


def cross(x, y):
    return (x[1]*y[2]-x[2]*y[1], x[2]*y[0]-x[0]*y[2], x[0]*y[1]-x[1]*y[0])


def distance(x, y):
    z = sub(x, y)
    return dot(z, z)


def rank(rows):
    a = [list(map(F, row)) for row in rows]
    if not a:
        return 0
    pivot = 0
    for col in range(len(a[0])):
        chosen = next((j for j in range(pivot, len(a)) if a[j][col]), None)
        if chosen is None:
            continue
        a[pivot], a[chosen] = a[chosen], a[pivot]
        divisor = a[pivot][col]
        a[pivot] = [x/divisor for x in a[pivot]]
        for j in range(pivot+1, len(a)):
            factor = a[j][col]
            if factor:
                a[j] = [x-factor*y for x, y in zip(a[j], a[pivot])]
        pivot += 1
        if pivot == len(a):
            break
    return pivot


def matrix(points):
    return tuple(distance(points[i], points[j]) for i, j in combinations(range(len(points)), 2))


def leq(a, b):
    return all(x <= y for x, y in zip(a, b))


def digest(data):
    return hashlib.sha256(json.dumps(data, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def fixtures():
    core = ((0,0,0), (-1,0,0), (0,-1,0), (0,0,-1))
    yield ('two_independent_caps', core+((1,-1,-1), (-1,1,-1)),
           core+((-1,-1,-1), (-1,-1,-1)), 4, 4)
    p = ((0,0,0), (-1,-1,0), (-1,0,1), (0,-1,1),
         (1,-2,5), (-2,-5,-1), (-5,1,2))
    v = ((1,1,1), (1,-1,-1), (-1,1,-1))
    q = p[:4] + tuple(tuple(x-F(8,3)*n for x,n in zip(p[4+i], v[i])) for i in range(3))
    yield ('three_cyclic_caps', p, q, 8, 2)
    v = tuple(p for p in product((-1,1), repeat=3) if p[0]*p[1]*p[2] == 1)
    for depth in (1, 2):
        labels = tuple((i,j) for i in range(4) for j in range(4) if i != j)
        p = v + tuple(tuple(v[j][k]-depth*v[i][k] for k in range(3)) for i,j in labels)
        q = v + tuple(tuple(v[j][k]+depth*v[i][k] for k in range(3)) for i,j in labels)
        yield ('classical_flaps_depth_'+str(depth), p, q, 2, 2)


def analyze(name, original_p, original_q, expected_tight, expected_interval):
    # Clear denominators once. All enumeration distances are Python integers.
    scale = lcm(*(F(x).denominator for z in original_p+original_q for x in z))
    p, q = (tuple(tuple(int(scale*F(x)) for x in z) for z in points)
            for points in (original_p, original_q))
    n = len(p)
    require(p[:4] == q[:4] and rank([sub(z,p[0]) for z in p[1:4]]) == 3,
            'fixed nondegenerate core')
    pairs = tuple(combinations(range(n), 2))
    upper, lower = matrix(p), matrix(q)
    require(leq(lower, upper), 'endpoint contraction')
    tight = [k for k in range(len(pairs)) if lower[k] == upper[k]]
    anchor_faces = []
    for i in range(4, n):
        require(p[i] != q[i], 'each noncore label has two distinct options')
        anchors = [j for j in range(4) if distance(p[i],p[j]) == distance(q[i],q[j])]
        require(len(anchors) == 3, 'three tight core anchors')
        a,b,c = (p[j] for j in anchors)
        normal = cross(sub(b,a), sub(c,a))
        nn = dot(normal, normal)
        require(nn > 0, 'noncollinear anchors')
        depth = dot(sub(p[i],a), normal)
        require(depth != 0, 'nondegenerate face attachment')
        reflected = tuple(x-F(2*depth, nn)*z for x,z in zip(p[i],normal))
        require(reflected == q[i], 'two sphere-intersection options are the endpoints')
        anchor_faces.append(anchors)

    # For every pair precompute all four exact distances. Core bits are zero.
    tables = [tuple(distance((p,q)[a][i], (p,q)[b][j])
                    for a,b in ((0,0),(0,1),(1,0),(1,1))) for i,j in pairs]
    tight_states, interval = [], {}
    for moving_bits in product((0,1), repeat=n-4):
        bits = (0,0,0,0)+moving_bits
        if not all(tables[k][2*bits[pairs[k][0]]+bits[pairs[k][1]]] == upper[k] for k in tight):
            continue
        tag = ''.join(map(str,moving_bits))
        tight_states.append(tag)
        d = tuple(tables[k][2*bits[i]+bits[j]] for k,(i,j) in enumerate(pairs))
        if leq(lower,d) and leq(d,upper):
            # Direct reconstruction independently checks the table lookup.
            points = tuple((p,q)[bits[i]][i] for i in range(n))
            require(matrix(points) == d, 'reconstructed state distances')
            interval[tag] = d
    require(len(tight_states) == expected_tight, 'tight-framework realization count')
    require(len(interval) == expected_interval, 'complete interval count')
    require(len(set(interval.values())) == len(interval), 'distance-matrix quotient count')

    covers = []
    for a, da in interval.items():
        for b, db in interval.items():
            if a == b or not leq(db, da):
                continue
            if not any(c not in (a,b) and leq(db,dc) and leq(dc,da) for c,dc in interval.items()):
                covers.append([a,b])
    first, last = '0'*(n-4), '1'*(n-4)
    chains = []
    def walk(path):
        if path[-1] == last:
            chains.append(path)
        else:
            for a,b in covers:
                if a == path[-1]:
                    walk(path+[b])
    walk([first])
    require(bool(chains), 'saturated endpoint chain')
    if expected_interval == 2:
        require(chains == [[first,last]], 'indecomposable control')
    else:
        require(name == 'two_independent_caps' and len(chains) == 2
                and all(len(c) == 3 for c in chains), 'diamond decomposition control')

    paired = [x+y for x,y in zip(p,q)]
    return {'name':name, 'labels':n, 'input_distinct':len(set(p)), 'output_distinct':len(set(q)),
            'integer_coordinate_scale':scale, 'coordinate_digest':digest([p,q]),
            'paired_affine_rank':rank([sub(z,paired[0]) for z in paired[1:]]),
            'pairs':len(pairs), 'tight_pairs':len(tight),
            'core_face_anchors_for_labels_4_onward':anchor_faces,
            'binary_candidates_tested':2**(n-4), 'tight_states':tight_states,
            'interval_states':list(interval), 'covers':covers, 'saturated_chains':chains,
            'interval_distance_hashes':{bits:digest(d) for bits,d in interval.items()}}


def run():
    data = [analyze(*fixture) for fixture in fixtures()]
    require(data[0]['paired_affine_rank'] == 5, 'rank-five decomposable control')
    require(all(d['paired_affine_rank'] == 6 for d in data[1:]), 'rank-six controls')
    require(data[2]['output_distinct'] == 10 and data[3]['output_distinct'] == 16,
            'collision and injective classical controls')
    return {'scope':'Exact fixture intervals; universal reduction and source no-R5 theorem are external to this checker.',
            'fixtures':data}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--emit', action='store_true')
    args = parser.parse_args()
    text = json.dumps(run(), indent=2, sort_keys=True)+'\n'
    if args.emit:
        print(text, end='')
    else:
        require(text == Path(__file__).with_name('EXPECTED.json').read_text(), 'expected record mismatch')
        print('PASS: intermediate-state counts 4,2,2,2; exact saturated chains and collision controls')
        print('PASS: 4096 binary placements exhausted for each classical flap depth')
        print('EXPECTED.json sha256 '+hashlib.sha256(text.encode()).hexdigest())


if __name__ == '__main__':
    main()
