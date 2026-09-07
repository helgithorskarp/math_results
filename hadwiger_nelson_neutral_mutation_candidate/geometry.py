#!/usr/bin/env python3
"""Generate a coupled unit-circle augmentation of the certified mutation seed."""
import argparse
from fractions import Fraction as Q
from itertools import combinations
import hashlib
import json
from pathlib import Path
import sys
from verify import HERE, REPO, construct, load_inputs, require

KFIELD_SHA256 = '648cb0317b5a4c96959e8447327c5e1cf19945c8049a746e86cceed130a18b31'
CATALOGUE_SHA256 = 'b82909c48ce088deb89b555f4c8fa554bba44030570fdaaf0b9b607e9552a5a6'
kpath = REPO / 'hadwiger_nelson_parts509_swap_closure/kfield.py'
require(hashlib.sha256(kpath.read_bytes()).hexdigest() == KFIELD_SHA256, 'field source hash')
sys.path.insert(0, str(kpath.parent))
import kfield as k

ONE=k.one(3)

def decode(v):return tuple(tuple(Q(a) for a in row) for row in v)
def encode(v):return [[str(a) for a in row] for row in v]
def add(a,b):return tuple(k.add(x,y) for x,y in zip(a,b))
def sub(a,b):return tuple(k.sub(x,y) for x,y in zip(a,b))
def scale(a,r):return tuple(k.scale(x,r) for x in a)
def sqdist(a,b):
    d=sub(a,b);return k.add(k.mul(d[0],d[0],3),k.mul(d[1],d[1],3))

def intersections(a,b):
    d=sub(b,a);s=sqdist(a,b)
    if not any(s):raise ValueError('coincident centres')
    rho=k.sub(k.inv(s,3),k.const(3,Q(1,4)))
    root=k.field_sqrt(rho,3)
    if root is None:return []
    mid=scale(add(a,b),Q(1,2))
    perp=(k.neg(k.mul(d[1],root,3)),k.mul(d[0],root,3))
    out=sorted(set([add(mid,perp),sub(mid,perp)]))
    for p in out:
        if sqdist(a,p)!=ONE or sqdist(b,p)!=ONE:raise ValueError('bad exact intersection')
    return out

MOD=1000081
ROOTS=(964569,816716,970601)
if any(r*r%MOD!=p for r,p in zip(ROOTS,(3,5,11))):raise ValueError('bad modular embedding')
BASIS=[1]*8
for m in range(8):
    for j,r in enumerate(ROOTS):
        if m>>j&1:BASIS[m]=BASIS[m]*r%MOD

def project(x):
    return sum(a.numerator*pow(a.denominator,-1,MOD)*r for a,r in zip(x,BASIS))%MOD

def strict_edges(points):
    images=[tuple(project(x) for x in p) for p in points]
    edges=[];tests=0
    for a,b in combinations(range(len(points)),2):
        x=(images[a][0]-images[b][0])%MOD;y=(images[a][1]-images[b][1])%MOD
        if (x*x+y*y)%MOD==1:
            tests+=1
            if sqdist(points[a],points[b])==ONE:edges.append((a,b))
    return edges,tests


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    certificate = json.loads((HERE / 'certificate.json').read_text())
    inputs = load_inputs(certificate)
    active, rows, swaps = construct(certificate, inputs)
    seed = [(tuple(Q(x, 96) for x in row[:8]), tuple(Q(x, 96) for x in row[8:])) for row in rows]
    cp = REPO / 'hadwiger_nelson_parts509_swap_closure/completion_points.json'
    require(hashlib.sha256(cp.read_bytes()).hexdigest() == CATALOGUE_SHA256, 'catalogue hash')
    source = inputs['hadwiger_nelson_parts509_heule_union_minimum/certificate_H510.json']['coordinates']
    catalogue = {decode(source[str(v)]) for v in range(509)}
    catalogue.update(decode([q['x'], q['y']]) for q in json.loads(cp.read_text())['points'])
    require(len(catalogue) == 1667 and set(seed) <= catalogue, 'unexpected original catalogue')
    moved = [i for i, raw in enumerate(active) if raw >= 509]
    images = [tuple(project(a) for a in p) for p in seed]
    seen, births = set(), {}
    counts = {'source_pairs': 0, 'K_roots': 0, 'outside_catalogue': 0}
    for q in moved:
        for v in range(509):
            if v == q or (v in moved and v < q):
                continue
            counts['source_pairs'] += 1
            for point in intersections(seed[q], seed[v]):
                counts['K_roots'] += 1
                if point in catalogue or point in seen:
                    continue
                seen.add(point)
                counts['outside_catalogue'] += 1
                x, y = [project(a) for a in point]
                ns = [u for u, (a, b) in enumerate(images)
                      if ((x-a)**2+(y-b)**2) % MOD == 1 and sqdist(point, seed[u]) == ONE]
                if len(ns) >= 3:
                    births[point] = ns
    ordered = sorted(births)
    pairs, _ = strict_edges(ordered)
    used = sorted({i for pair in pairs for i in pair})
    host = seed + [ordered[i] for i in used]
    edges, _ = strict_edges(host)
    summary = dict(counts, new_points=len(ordered), new_degree_histogram={str(d):
        sum(len(ns) == d for ns in births.values()) for d in sorted({len(ns) for ns in births.values()})},
        unit_pairs_between_new_points=len(pairs), paired_new_points=len(used),
        host_vertices=len(host), host_edges=len(edges))
    expected = json.loads((HERE / 'geometry_expected.json').read_text())
    require(summary == expected, 'geometry result mismatch')
    args.output.mkdir(parents=True, exist_ok=True)
    (args.output / 'circle_centres.json').write_text(json.dumps({'points': [encode(p) for p in ordered],
        'seed_neighbours': [births[p] for p in ordered], 'unit_pairs': pairs}, separators=(',', ':')) + '\n')
    (args.output / 'augmented_host.json').write_text(json.dumps({'points': [encode(p) for p in host],
        'edges': edges, 'birth_indices': used}, separators=(',', ':')) + '\n')
    print(json.dumps(summary, sort_keys=True))


if __name__ == '__main__':
    main()
