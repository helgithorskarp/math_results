#!/usr/bin/env python3
"""Separate geometry reconstruction and audit of the three new colour words.

Imports no other implementation. The 506 inherited word reconstructions remain
checked by verify.py and its explicitly pinned parent-certificate decoder.
"""
import base64
from fractions import Fraction
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
MOVES = [(0,217,190),(1,220,80),(4,347,175),(5,350,123),(6,353,149),
         (7,356,96),(8,375,211),(9,413,56),(10,415,43)]

def need(ok, message):
    if not ok:
        raise ValueError(message)

def multiply(a, b):
    out = [0]*8
    for i, x in enumerate(a):
        if x:
            for j, y in enumerate(b):
                if not y:
                    continue
                factor = 1
                for bit, rad in enumerate((3,5,11)):
                    if (i & j) & (1 << bit):
                        factor *= rad
                out[i ^ j] += x*y*factor
    return out

def main():
    manifest = json.loads((HERE/'manifest.json').read_text())
    for path, h in manifest['inputs'].items():
        need(sha256((REPO/path).read_bytes()).hexdigest() == h, 'input identity')
    original = []
    for line in (REPO/'hadwiger_nelson_parts509_completion_census_degree9/points.tsv').read_text().splitlines():
        if line and not line.startswith('#'):
            row = tuple(3*int(x) for x in line.split())
            need(len(row) == 16, 'coordinate width')
            original.append(row)
    need(len(original) == 509, 'original order')
    q = json.loads((REPO/'hadwiger_nelson_parts509_swap_closure/completion_points.json').read_text())['points']
    def completion(i):
        v = [288*Fraction(x) for axis in ('x','y') for x in q[i][axis]]
        need(all(x.denominator == 1 for x in v), 'scale')
        return tuple(map(int,v))
    points = {v: p for v,p in enumerate(original) if v not in {u for _,u,_ in MOVES}}
    points.update({509+row:completion(i) for row,_,i in MOVES})
    pp = [points[v] for v in sorted(points)]+[completion(10)]
    need(len(pp) == len(set(pp)) == 510, 'collision merging')
    prime = 1321
    need(all(prime % d for d in range(2,37)), 'prime')
    roots = (321,416,501)
    need(all(r*r % prime == d for r,d in zip(roots,(3,5,11))), 'roots')
    basis = []
    for mask in range(8):
        x = 1
        for bit,r in enumerate(roots):
            if mask & (1 << bit):
                x = x*r % prime
        basis.append(x)
    images = [tuple(sum(p[k+i]*basis[i] for i in range(8)) % prime for k in (0,8)) for p in pp]
    excluded = exact = 0
    edges = []
    for a,b in combinations(range(510),2):
        dx = images[a][0]-images[b][0]
        dy = images[a][1]-images[b][1]
        if (dx*dx+dy*dy-288**2) % prime:
            excluded += 1
            continue
        total = [0]*8
        for offset in (0,8):
            delta = [pp[a][offset+i]-pp[b][offset+i] for i in range(8)]
            square = multiply(delta,delta)
            total = [x+y for x,y in zip(total,square)]
        exact += 1
        if total == [288**2]+[0]*7:
            edges.append((a,b))
    need(excluded+exact == 129795 and len(edges) == 2456, 'complete graph')
    eh = sha256(''.join(f'{a} {b}\n' for a,b in edges).encode()).hexdigest()
    expected = json.loads((HERE/'EXPECTED.json').read_text())
    need(eh == expected['host_edge_sha256'], 'entrywise edge identity')
    cert = json.loads((HERE/'certificate.json').read_text())
    raw = base64.b64decode(cert['packed_colours_base64'],validate=True)
    need(sha256(raw).hexdigest() == cert['packed_sha256'] and len(raw) == 384, 'payload identity')
    checks = 0
    for row,missing in enumerate(cert['new_deleted_vertices']):
        block = raw[128*row:128*(row+1)]
        need(block[-1] < 4, 'padding')
        colours = {}
        for i,v in enumerate(x for x in range(510) if x != missing):
            colours[v] = (block[i//4] >> (2*(i % 4))) & 3
        for a,b in edges:
            if missing not in (a,b):
                need(colours[a] != colours[b], ('monochromatic edge',row,a,b))
                checks += 1
    print(json.dumps({'all_checks':True,'host_vertices':510,'host_edges':len(edges),
                      'host_edge_sha256':eh,'modular_nonunit_exclusions':excluded,
                      'exact_polynomial_decisions':exact,'new_words_checked':3,
                      'new_word_edge_checks':checks,'inherited_decoder_reimplemented':False},indent=2,sort_keys=True))

if __name__ == '__main__':
    main()
