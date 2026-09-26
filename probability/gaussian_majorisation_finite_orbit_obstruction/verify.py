#!/usr/bin/env python3
"""Exact rational geometry and 48-label Gaussian hinge certificate.

The universal impossibility theorem uses the written finite-support argument
and rational-root proof in PROOF.md; this is not a numerical integration.
"""
import argparse
from collections import Counter
from copy import deepcopy
from fractions import Fraction as F
import hashlib
import itertools
import json
from pathlib import Path


def require(condition, message):
    if not condition:
        raise ValueError(message)


def dot(a, b):
    return sum(x*y for x, y in zip(a, b))


def transpose(a):
    return list(map(list, zip(*a)))


def multiply(a, b):
    return [[dot(row, col) for col in transpose(b)] for row in a]


def mv(a, v):
    return [dot(row, v) for row in a]


def identity():
    return [[F(i == j) for j in range(3)] for i in range(3)]


def det(a):
    total = F(0)
    for p in itertools.permutations(range(3)):
        inversions = sum(p[i] > p[j] for i in range(3) for j in range(i+1,3))
        total += (-1)**inversions*a[0][p[0]]*a[1][p[1]]*a[2][p[2]]
    return total


def rank(a):
    a = [list(map(F, row)) for row in a]
    r = 0
    for c in range(len(a[0])):
        pivot = next((i for i in range(r, len(a)) if a[i][c]), None)
        if pivot is None:
            continue
        a[r], a[pivot] = a[pivot], a[r]
        q = a[r][c]
        a[r] = [v/q for v in a[r]]
        for i in range(len(a)):
            if i != r:
                q = a[i][c]
                a[i] = [v-q*w for v, w in zip(a[i], a[r])]
        r += 1
    return r


def encode(obj):
    return (json.dumps(obj, indent=2, sort_keys=True)+'\n').encode()


def audit(cert):
    a, b = cert['A'], cert['B']
    require(a == [[1,0,1],[0,1,1],[-1,0,1],[0,-1,1]], 'A directions')
    require(b == [[1,1,1],[-1,1,1],[-1,-1,1],[1,-1,1]], 'B directions')
    source = [[0,0,0]]+a+[[-v for v in row] for row in b]
    target = [[0,0,0]]+a+b
    losses = []
    for i, j in itertools.combinations(range(9), 2):
        dx = [v-w for v, w in zip(source[i], source[j])]
        dy = [v-w for v, w in zip(target[i], target[j])]
        losses.append(dot(dx,dx)-dot(dy,dy))
    require(min(losses) >= 0, 'Contraction inequality')
    require(rank([x+y for x,y in zip(source[1:],target[1:])]) == 6,
            'Paired rank')

    reflections = []
    for j in range(3):
        s = [[F(i == k)-2*F(b[j][i]*b[j][k],dot(b[j],b[j]))
              for k in range(3)] for i in range(3)]
        require(multiply(transpose(s),s) == identity() and det(s) == -1,
                'Reflection is not orthogonal')
        require(mv(s,b[j]) == [-v for v in b[j]], 'Normal is not reversed')
        fixed = [v for v in a if dot(v,b[j]) == 0]
        require(len(fixed) == 2 and rank(fixed+[b[j]]) == 3,
                'Congruent triple does not span')
        require(all(mv(s,v) == v for v in fixed), 'Fixed site moved')
        reflections.append(s)
    p = multiply(reflections[0],reflections[1])
    trace = sum(p[i][i] for i in range(3))
    require(det(p) == 1 and trace == F(cert['product_trace']) == F(-5,9),
            'Infinite-order rotation certificate')
    require((trace-1).denominator != 1, 'Rational-root obstruction absent')
    require([[str(v) for v in row] for row in p] == cert['product'],
            'Product matrix mismatch')

    group = [(permutation, signs) for permutation in itertools.permutations(range(3))
             for signs in itertools.product((-1,1),repeat=3)]
    counts = Counter()
    observations = []
    # gx = observation/2; all exponents in the Gaussian/c ratio are integral.
    for permutation, signs in group:
        obs = tuple(signs[i]*int(permutation[i] == 0) for i in range(3))
        observations.append(obs)
        counts[obs] += 1
    require(len(counts) == 6 and set(counts.values()) == {8}, 'Orbit multiplicity')
    records = []
    for fixture in cert['fixtures']:
        weights = [F(w) for w in fixture['packet_weights']]
        require(len(weights) == 8 and min(weights) >= 0 and sum(weights) == 1,
                'Invalid packet probability law')
        threshold = F(fixture['threshold_over_c_without_origin'])
        gap = F(0)
        value_pairs = []
        for obs in observations:
            fs = sum(w*F(2)**(dot(obs,v)-dot(v,v))
                     for w,v in zip(weights,source[1:]))
            gs = sum(w*F(2)**(dot(obs,v)-dot(v,v))
                     for w,v in zip(weights,target[1:]))
            gap += max(gs-threshold,0)-max(fs-threshold,0)
            value_pairs.append((str(fs),str(gs)))
        gap /= len(group)
        require(gap == F(fixture['average_gap_over_c_without_origin']) < 0,
                'Wrong signed Gaussian orbit gap')
        # Exact threshold translation by an arbitrary common origin term:
        # verify representative p values; the universal identity is scalar.
        for origin in [F(0),F(1,2),F(999,1000)]:
            translated = F(0)
            for fs,gs in value_pairs:
                h = origin+(1-origin)*threshold
                translated += max(origin+(1-origin)*F(gs)-h,0)
                translated -= max(origin+(1-origin)*F(fs)-h,0)
            require(translated/48 == (1-origin)*gap, 'Origin translation')
        records.append({'name':fixture['name'],'gap':str(gap),
                        'distinct_value_pairs':len(set(value_pairs))})
    return {'status':'FINITE_ORTHOGONAL_OBSTRUCTION_INPUTS_PASS',
            'contraction_pairs':len(losses),'squared_loss_counts':dict(Counter(map(str,losses))),
            'paired_affine_rank':6,'product_trace':str(trace),
            'rotation_trace_minus_one':str(trace-1),'orthogonal_labels':48,
            'axis_multiplicity':8,'fixtures':records}


def controls(cert):
    broken = []
    c = deepcopy(cert); c['product_trace'] = '3'; broken.append(c)
    c = deepcopy(cert); c['B'][0][0] = 2; broken.append(c)
    c = deepcopy(cert); c['fixtures'][0]['packet_weights'][0] = '-1/4'; broken.append(c)
    c = deepcopy(cert); c['fixtures'][1]['average_gap_over_c_without_origin'] = '1/384'; broken.append(c)
    for c in broken:
        try:
            audit(c)
        except ValueError:
            continue
        raise ValueError('Invalid certificate accepted')
    return len(broken)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check',action='store_true')
    parser.add_argument('--certificate',type=Path)
    args = parser.parse_args()
    here = Path(__file__).resolve().parent
    cert = json.loads((args.certificate or here/'CERTIFICATE.json').read_text())
    record = audit(cert)
    record['invalid_controls_rejected'] = controls(cert)
    record['certificate_sha256'] = hashlib.sha256(encode(cert)).hexdigest()
    if args.check:
        require(encode(record) == (here/'EXPECTED.json').read_bytes(), 'Expected record mismatch')
        print(record['status'],hashlib.sha256(encode(record)).hexdigest())
    else:
        print(encode(record).decode(),end='')


if __name__ == '__main__':
    main()
