#!/usr/bin/env python3
"""Exact complete transportation cover for nonadjacent two-double sectors.

Actual author six-sendov-2, researcher. Classical staircase transportation
parametrization is used openly, not claimed as a new general triangulation.
Its strict angular certificate is the stated new scoped result.
The pinned public trace/filter backend is adapted, not independently audited.
"""
import argparse,hashlib,importlib.util,json,time
from fractions import Fraction as F
from itertools import combinations
from math import comb,lcm
from pathlib import Path

s=Path(__file__).resolve().parent
source=s.parent/'sendov_degree9_one_triple_six_level_displacement'/'verify.py'
PIN='84db02a4d866aa94d400481e19ea84679c4e8d09e9de6085594e96a9aee6d2dd'
if hashlib.sha256(source.read_bytes()).hexdigest()!=PIN:raise ValueError('public backend pin mismatch')
spec=importlib.util.spec_from_file_location('credited_one_triple_backend',source)
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
ADJACENT=((1,5),(1,6),(2,5),(2,6))
SECTIONS=tuple(pair for pair in combinations(range(1,7),2) if pair not in ADJACENT)
def unit(j):return tuple(F(int(i==j)) for i in range(5))
def data(pair):
    weights=[1+int(i in pair) for i in range(1,7)]
    prefix=[sum(weights[:j]) for j in range(1,6)]
    low=[i for i,M in enumerate(prefix) if M<4]
    neutral=[i for i,M in enumerate(prefix) if M==4]
    high=[i for i,M in enumerate(prefix) if M>4][::-1]
    return weights,prefix,low,neutral,high
def vertex(prefix,i,j):
    if i is None:return unit(j)
    gamma=F(prefix[i]*(prefix[j]-4),4*(prefix[j]-prefix[i]))
    a=[F(0)]*5;a[i]=gamma;a[j]=1-gamma
    return tuple(a)
def path_cells(pair):
    weights,prefix,low,neutral,high=data(pair)
    rows=[*low,None];out=[]
    for downs in combinations(range(len(low)+len(high)-1),len(low)):
        i=j=0;edges=[(rows[i],high[j])]
        for step in range(len(low)+len(high)-1):
            if step in downs:i+=1
            else:j+=1
            edges.append((rows[i],high[j]))
        keys=[(None,j) for j in neutral]+edges
        keys.sort(key=lambda p:(0,p[1]) if p[0] is None else (1,p[0],p[1]))
        out.append((keys,[vertex(prefix,i,j) for i,j in keys]))
    m.require(len(out)==comb(len(low)+len(high)-1,len(low)),'complete monotone path count')
    return weights,prefix,low,neutral,high,out
def geometry(pair,cell):
    weights,prefix,low,neutral,high,cells=path_cells(pair)
    keys,vertices=cells[cell]
    profiles=[m.levels_from_gaps(a,prefix) for a in vertices]
    m.require(len(vertices)==5 and len(set(vertices))==5,'full path five distinct vertices')
    for a,x in zip(vertices,profiles):
        m.require(sum(a)==1 and all(t>=0 for t in a),'full nonnegative vertex normalization')
        m.require(sum(a[j]/prefix[j] for j in range(5))<=F(1,4),'full vertex clipping')
        m.require(sum(w*t for w,t in zip(weights,x))==0 and min(x)>=-1 and max(x)==1 and tuple(sorted(x))==x,'full weighted level vertex')
    matrix=[[vertices[j][i] for j in range(5)] for i in range(5)]
    cols=[m.solve(matrix,unit(j)) for j in range(5)]
    inverse=[[cols[j][i] for j in range(5)] for i in range(5)]
    m.require(m.mm(matrix,inverse)==[[F(int(i==j)) for j in range(5)] for i in range(5)],'whole path-cell inverse')
    # Check every row/column transport identity as a linear identity by
    # applying it to all five unit coordinates. The dummy row is unused
    # supply: sum_j d_j*a_j - sum_i c_i*a_i.
    for coordinate in range(5):
        a=unit(coordinate);b=[inverse[i][coordinate] for i in range(5)]
        flows={}
        for weight,(i,j) in zip(b,keys):
            if j in neutral:continue
            d=1-F(4,prefix[j])
            flows[i,j]=weight*d if i is None else weight/(1/(F(4,prefix[i])-1)+1/d)
        for i in low:
            m.require(sum(v for (h,j),v in flows.items() if h==i)==(F(4,prefix[i])-1)*a[i],'full transport demand identity')
        for j in high:
            m.require(sum(v for (i,h),v in flows.items() if h==j)==(1-F(4,prefix[j]))*a[j],'full transport supply identity')
        m.require(sum(v for (i,j),v in flows.items() if i is None)==sum((1-F(4,prefix[j]))*a[j] for j in high)-sum((F(4,prefix[i])-1)*a[i] for i in low),'full dummy surplus identity')
    scale=lcm(*(t.denominator for x in profiles for t in x))
    return weights,prefix,vertices,profiles,scale,inverse
def all_geometry():
    record=[]
    for pair in SECTIONS:
        weights,prefix,low,neutral,high,cells=path_cells(pair)
        complete={unit(j) for j in neutral+high}
        complete.update(vertex(prefix,i,j) for i in low for j in high)
        used=set(a for _,vs in cells for a in vs)
        m.require(used==complete,'all and only entire clipped-section vertices')
        cell_records=[]
        for index,(keys,vertices) in enumerate(cells):
            w,M,vs,profiles,scale,inverse=geometry(pair,index)
            m.require(all(sum(v[j] for v in vs)>0 for j in range(5)),'positive cell interior gives all five gaps')
            cell_records.append({'cell':index,'keys':keys,'scale':scale,
                 'vertices':[[str(t) for t in a] for a in vs],
                 'level_vertices':[[str(t) for t in a] for a in profiles],
                 'inverse_sha256':m.digest([[str(t) for t in r] for r in inverse])})
        record.append({'doubled_ranks':pair,'weights':weights,'cumulative':prefix,
            'low':[i+1 for i in low],'neutral':[i+1 for i in neutral],
            'high':[i+1 for i in high],
            'full_vertices':[[str(t) for t in a] for a in sorted(complete)],
            'cells':cell_records})
    return record
