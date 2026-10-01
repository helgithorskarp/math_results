#!/usr/bin/env python3
"""Literal two-corona reader; no search, solver or external fixture.

Author six-heesch-3, researcher. Analytic bridges are in proof.md.
"""
import argparse
from collections import defaultdict
from copy import deepcopy
from fractions import Fraction
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path
import geometry as g

HERE=Path(__file__).resolve().parent

def boundary_disk(edges,poses):
    successor={};predecessor={}
    for owners in edges.values():
        if len(owners)!=1:continue
        k,i=owners[0];poly=g.shape(poses[k])[0];a,b=poly[i],poly[(i+1)%14]
        if poses[k][1]:a,b=b,a
        if a in successor or b in predecessor:return False
        successor[a]=b;predecessor[b]=a
    if not successor or set(successor)!=set(predecessor):return False
    start=min(successor);v=start;seen=set()
    while v not in seen:seen.add(v);v=successor[v]
    return v==start and len(seen)==len(successor)

def point_segment(p,a,b):
    """Sixteen times squared distance, represented in Z[sqrt(3)]."""
    u=g.sub(b,a);v=g.sub(p,a);d=g.dot(v,u)
    g.require(g.dot(u,u)==(4,0),'nonunit segment')
    if g.qsign(d)<=0:return tuple(4*x for x in g.dot(v,v))
    if g.qcmp(d,(4,0))>=0:return tuple(4*x for x in g.dot(g.sub(p,b),g.sub(p,b)))
    return g.qsub(tuple(4*x for x in g.dot(v,v)),g.qmul(d,d))

def disjoint_segments(a,b,c,d):
    values=(g.qsign(g.cross(g.sub(b,a),g.sub(c,a))),g.qsign(g.cross(g.sub(b,a),g.sub(d,a))),
            g.qsign(g.cross(g.sub(d,c),g.sub(a,c))),g.qsign(g.cross(g.sub(d,c),g.sub(b,c))))
    for value,p,x,y in zip(values,(c,d,a,b),(a,a,c,c),(b,b,d,d)):
        if value==0 and g.on_segment(p,x,y):return False
    return not (values[0]*values[1]<0 and values[2]*values[3]<0)

def patch(poses,amplitudes):
    stars={};edges=defaultdict(list)
    for k,p in enumerate(poses):
        poly=g.shape(p)[0]
        for i,v in enumerate(poly):
            star=g.star_image(g.SECTORS[i],p[0],p[1]);old=stars.get(v,0)
            g.require(not old&star,'angular overlap');stars[v]=old|star
            edges[tuple(sorted((v,poly[(i+1)%14])))].append((k,i))
    for p,q in combinations(poses,2):g.require(g.geometry(p,q) is not None,'overlap or proper T contact')
    for owners in edges.values():
        g.require(len(owners)<=2,'more than two edge owners')
        if len(owners)==2:g.require(sum(amplitudes[i] for k,i in owners)==0,'unmatched bowed interface')
    g.require(boundary_disk(edges,poses),'prefix is not a disk')
    return stars,edges

def verify(data):
    epsilon=Fraction(*data['epsilon']);g.require(0<epsilon<=Fraction(1,4),'epsilon range')
    amps=tuple(data['amplitudes']);g.require(len(amps)==14 and all(x in (-1,0,1) for x in amps),'amplitudes')
    g.require((amps.count(1),amps.count(-1),amps.count(0))==(4,2,8),'profile multiplicities')
    poses=tuple(tuple(p) for p in data['poses']);sizes=tuple(data['prefix_sizes'])
    g.require(sizes[0]==1 and sizes[-1]==len(poses) and len(sizes)==3,'corona prefixes')
    g.require(all(a<b for a,b in zip(sizes,sizes[1:])),'prefix order')
    g.require(poses[0]==g.IDENTITY and len(set(poses))==len(poses),'root or duplicate copy')
    g.require(all(len(p)==6 and 0<=p[0]<12 and p[1] in (0,1) and all(type(x) is int for x in p) for p in poses),'pose format')
    info=[]
    for n in sizes:
        stars,edges=patch(poses[:n],amps)
        info.append((stars,edges))
    for layer,(old,n) in enumerate(zip(sizes,sizes[1:])):
        stars,edges=info[layer+1]
        preceding_start=0 if layer==0 else sizes[layer-1]
        preceding_vertices={v for p in poses[preceding_start:old] for v in g.shape(p)[0]}
        for k,p in enumerate(poses[:old]):
            poly=g.shape(p)[0]
            for i,v in enumerate(poly):
                g.require(stars[v]==4095,'older vertex is not fully covered')
                g.require(len(edges[tuple(sorted((v,poly[(i+1)%14])))])==2,'older port is not fully covered')
        for p in poses[old:n]:
            g.require(bool(set(g.shape(p)[0])&preceding_vertices),'new tile does not touch the preceding corona')
    edges=tuple(info[-1][1]);least=None;checked=0
    for (a,b),(c,d) in combinations(edges,2):
        if {a,b}&{c,d}:continue
        g.require(disjoint_segments(a,b,c,d),'crossing nonincident reference edges')
        for point,x,y in ((a,c,d),(b,c,d),(c,a,b),(d,a,b)):
            distance=point_segment(point,x,y)
            # Distinct nonincident reference edges are disjoint by patch().
            g.require(g.qsign((distance[0]*epsilon.denominator**2-16*epsilon.numerator**2,
                               distance[1]*epsilon.denominator**2))>0,'insufficient arc separation')
            if least is None or g.qcmp(distance,least)<0:least=distance
        checked+=1
    # Unique incident unit chords have distinct rays in the 30-degree group.
    rays=defaultdict(set)
    for a,b in edges:
        for v,w in ((a,b),(b,a)):
            direction=g.DIR_INDEX[g.sub(w,v)]
            g.require(direction not in rays[v],'coincident incident rays');rays[v].add(direction)
    g.require(epsilon<=Fraction(1,4),'incident-cone bound')
    diameter=(0,0)
    for a,b in combinations(g.VERTICES,2):
        squared=g.dot(g.sub(a,b),g.sub(a,b))
        if g.qcmp(squared,diameter)>0:diameter=squared
    g.require(diameter==(48,24),'reference diameter')
    # sqrt(3)<7/4 gives d(B)^2<45/2<(19/4)^2.
    g.require(7**2>3*4**2 and Fraction(45,2)<Fraction(19,4)**2,'diameter comparison')
    g.require((Fraction(19,4)+epsilon/8)**2<23,'bowed diameter bound')
    # sqrt(3)>17/10 and exact Green area A=3+3sqrt(3)-epsilon/15.
    g.require(17**2<3*10**2 and 3+3*Fraction(17,10)-epsilon/15>8,'area bound')
    upper11=(Fraction(22,7)*Fraction(23,8)*12**2).__floor__()
    g.require(2**11>upper11,'finite upper obstruction')
    branch7=(Fraction(22,7)*Fraction(23,8)*8**2).__floor__()
    g.require(len(poses)*2**5>branch7,'seven-corona obstruction for this branch')
    return {'prefix_sizes':list(sizes),'prefix_boundary_ports':[sum(len(v)==1 for v in x[1].values()) for x in info],
            'full_patch_shared_ports':sum(len(v)==2 for v in info[-1][1].values()),'nonincident_edge_pairs':checked,
            'least_edge_distance_squared_times16':list(least),'epsilon':str(epsilon),'profile_multiplicities':[4,2,8],
            'area_lower':8,'diameter_squared_upper':23,'curvature_ratio':2,'depth11_lower':2**11,'depth11_capacity':upper11,
            'depth7_branch_lower':len(poses)*2**5,'depth7_capacity':branch7,'Heesch_interval':[2,10]}

def rejected_controls(data):
    controls={}
    bad=deepcopy(data);bad['amplitudes'][0],bad['amplitudes'][5]=bad['amplitudes'][5],bad['amplitudes'][0]
    controls['same_count_wrong_interfaces']=bad
    bad=deepcopy(data);bad['poses'].pop();bad['prefix_sizes'][-1]-=1
    controls['missing_outer_tile']=bad
    bad=deepcopy(data);bad['poses'][8][2]+=2
    controls['moved_outer_tile']=bad
    bad=deepcopy(data);bad['poses'][1][1]^=1
    controls['wrong_reflection']=bad
    result=[]
    for name,bad in controls.items():
        try:verify(bad)
        except (ValueError,KeyError):result.append(name)
        else:raise ValueError('malformed control accepted: '+name)
    return sorted(result)

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--expected',action='store_true');args=parser.parse_args()
    raw=(HERE/'certificate.json').read_bytes();data=json.loads(raw)
    result=verify(data);result['rejected_controls']=rejected_controls(data)
    result['certificate_sha256']=sha256(raw).hexdigest()
    if args.expected:g.require(result==json.loads((HERE/'expected.json').read_text()),'expected result differs')
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
