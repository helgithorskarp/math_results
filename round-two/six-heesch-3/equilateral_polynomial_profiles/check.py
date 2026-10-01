#!/usr/bin/env python3
"""Finite hypotheses for the polynomial-profile extension.

Author six-heesch-3, researcher. Standard library only. The old full
graph reader remains a required dependency; proof.md proves the new
unbounded-degree and covered-endpoint claims in writing.
"""
from collections import defaultdict
from fractions import Fraction
from hashlib import sha256
from itertools import product
from math import comb
from pathlib import Path
import argparse
import json
import sys

HERE=Path(__file__).resolve().parent
DEPENDENCY=HERE.parent/'equilateral_nonflat_classification'
sys.path.insert(0,str(DEPENDENCY))
import geometry as g

def angle_partitions(total,choices,lower=0):
    if total==0:return [()]
    return [(x,)+tail for k,x in enumerate(choices) if k>=lower and x<=total
            for tail in angle_partitions(total-x,choices,k)]

def qm(x,y):
    return x[0]*y[0]+5*x[1]*y[1],x[0]*y[1]+x[1]*y[0]
def qa(x,y):return x[0]+y[0],x[1]+y[1]
def qp(x,k):
    result=(Fraction(1),Fraction(0))
    for _ in range(k):result=qm(result,x)
    return result
def pm(a,b):
    result=[(Fraction(0),Fraction(0)) for _ in range(len(a)+len(b)-1)]
    for i,x in enumerate(a):
        for j,y in enumerate(b):result[i+j]=qa(result[i+j],qm(x,y))
    return result
def shift(p,c):
    result=[(Fraction(0),Fraction(0)) for _ in p]
    for n,x in enumerate(p):
        for k in range(n+1):
            y=qm(x,qp(c,n-k));y=tuple(comb(n,k)*v for v in y)
            result[k]=qa(result[k],y)
    return result

def alias_check():
    rational=lambda n:(Fraction(n),Fraction(0))
    f=list(map(rational,(0,0,1,-2,1)))
    left=pm(f,[(Fraction(-1),Fraction(1)),rational(2)])
    right=pm(f,[(Fraction(-1),Fraction(-1)),rational(2)])
    moved=shift(left,(Fraction(0),Fraction(-1,5)))
    difference=[qa(x,tuple(-v for v in y)) for x,y in zip(moved,right)]
    g.require(difference==[(Fraction(0),Fraction(8,125))]+[rational(0)]*5,'golden partial-alias identity')
    return {'degree':5,'shift_sqrt5_coefficient':'-1/5','vertical_sqrt5_coefficient':'8/125'}

def periodic_relations(fixture):
    poses=[tuple(p) for p in fixture['poses']];u=tuple(fixture['u']);v=tuple(fixture['v'])
    edges=defaultdict(list)
    for p,n,m in product(poses,range(-1,2),range(-1,2)):
        translation=g.add(p[2:],g.add(tuple(n*x for x in u),tuple(m*x for x in v)))
        q=p[:2]+translation;poly=g.shape(q)[0]
        for j,a in enumerate(poly):edges[tuple(sorted((a,poly[(j+1)%14])))].append((q,j,a,poly[(j+1)%14]))
    relations=set();partners=0
    for p in poses:
        poly=g.shape(p)[0]
        for i,a in enumerate(poly):
            b=poly[(i+1)%14];owners=[r for r in edges[tuple(sorted((a,b)))] if r[0]!=p]
            g.require(len(owners)==1,'periodic port partner missing or repeated')
            q,j,c,d=owners[0];rev=int(a==d)
            g.require(rev or a==c,'endpoint order')
            g.require(rev==(i+j)%2,'periodic partner violates endpoint colors')
            relations.add((min(i,j),max(i,j),rev));partners+=1
    g.require(len(relations)==7,'periodic seven-pair system')
    return {'base_copies':len(poses),'port_partners':partners,'relations':[list(r) for r in sorted(relations)]}

def verify():
    directions=[]
    for i,a in enumerate(g.VERTICES):
        chord=g.sub(g.VERTICES[(i+1)%14],a)
        g.require(g.dot(chord,chord)==(4,0),'nonunit port')
        directions.append(g.DIR_INDEX[chord])
    angles=[]
    for i,d in enumerate(directions):
        turn=(d-directions[i-1])%12
        if turn>=6:turn-=12
        angles.append(6-turn)
    g.require(angles==[8,3,4,6,4,9,4,3,4,9,4,3,8,3],'corner derivation')
    g.require(all((x in (4,8))==(i%2==0) for i,x in enumerate(angles)),'alternating endpoint color')
    partitions=angle_partitions(12,(3,4,6,8,9))
    g.require(partitions==[(3,3,3,3),(3,3,6),(3,9),(4,4,4),(4,8),(6,6)],'angle partition census')
    g.require(all(all(x in (4,8) for x in p) or all(x in (3,6,9) for x in p) for p in partitions),'mixed endpoint colors')
    for red in (4,8):g.require(not any(red in p and 6 in p for p in partitions),'regular neighbor at a red corner')
    cert_path=DEPENDENCY/'certificate.json';cert=json.loads(cert_path.read_text())
    cert_hash=sha256(cert_path.read_bytes()).hexdigest()
    g.require(cert_hash=='af9be7780a21bc75842ebadaf24b9e0a14b55257148c1b494ae3af1f06407dc1','dependency certificate changed')
    periodic=[periodic_relations(f) for f in cert['periodic_packings']]
    g.require([p['port_partners'] for p in periodic]==[28,28,56],'periodic counts')
    return {'corner_angles_in_30_degree_units':angles,'full_circle_angle_partitions':[list(p) for p in partitions],
            'mixed_color_partitions':0,'red_corner_regular_neighbor_partitions':0,
            'periodic_profiles':periodic,'partial_alias_identity':alias_check(),
            'dependency_certificate_sha256':cert_hash,'degree_restriction':'none; finite hypotheses only; written polynomial proof required'}

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--expected',action='store_true');args=parser.parse_args()
    result=verify()
    if args.expected:g.require(result==json.loads((HERE/'expected.json').read_text()),'expected result differs')
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
