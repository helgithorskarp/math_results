#!/usr/bin/env python3
"""Direct stage verifier: does not import or recompute the producer's graph."""
import argparse
from fractions import Fraction
import json
from pathlib import Path


def q(x):
    if type(x) is int or isinstance(x, str):
        return Fraction(x)
    raise ValueError('Only exact rational coordinates are accepted')


def point(x):
    if not isinstance(x, list) or len(x) != 3:
        raise ValueError('Expected three coordinates')
    return tuple(q(t) for t in x)


def square_distance(x, y):
    return sum((a-b)**2 for a,b in zip(x,y))


def check(data, certificate):
    if set(data) != {'source', 'target'}:
        raise ValueError('Invalid input keys')
    p, target = list(map(point,data['source'])), list(map(point,data['target']))
    if not p or len(p) != len(target) or len(set(p)) != len(p):
        raise ValueError('Invalid source labels')
    if certificate.get('status') != 'CERTIFIED':
        raise ValueError('A positive certificate is required')
    moved = {i for i in range(len(p)) if p[i] != target[i]}
    seen, comparisons = set(), 0
    current = p[:]
    for block in certificate['blocks']:
        indices = block['indices']
        if (not indices or any(type(i) is not int or i not in moved for i in indices)
                or len(set(indices)) != len(indices) or seen.intersection(indices)):
            raise ValueError('Invalid or repeated switch labels')
        following = current[:]
        for i in indices:
            following[i] = target[i]
        # Direct distances, including every unchanged label and all collisions.
        for i in range(len(p)):
            for j in range(i):
                if square_distance(following[i], following[j]) > square_distance(current[i], current[j]):
                    raise ValueError('A claimed stage expands a pair')
                comparisons += 1
        if block['kind'] == 'COMMON_ANCHOR':
            anchor = point(block['anchor'])
            if any(square_distance(current[i], anchor) != square_distance(following[i], anchor)
                   for i in range(len(p))):
                raise ValueError('Anchor does not preserve all endpoint radii')
        elif block['kind'] == 'DISPLACEMENT_PLANE':
            normal = point(block['normal'])
            if not any(normal):
                raise ValueError('Normal is zero')
            if any(sum(normal[k]*(following[i][k]-current[i][k]) for k in range(3))
                   for i in range(len(p))):
                raise ValueError('Displacement leaves the stated plane')
        else:
            raise ValueError('Unknown proof primitive')
        seen.update(indices)
        current = following
    if seen != moved or current != target:
        raise ValueError('Endpoint chain is incomplete')
    return dict(status='ENDPOINT_BLOCK_CERTIFICATE_VERIFIED', labels=len(p),
                stages=len(certificate['blocks']), pair_stage_checks=comparisons,
                trust='Rational stage hypotheses checked; analytic conclusions use PROOF.md inputs.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input', type=Path)
    parser.add_argument('certificate', type=Path)
    a = parser.parse_args()
    print(json.dumps(check(json.loads(a.input.read_text()),
                           json.loads(a.certificate.read_text())), indent=2))
