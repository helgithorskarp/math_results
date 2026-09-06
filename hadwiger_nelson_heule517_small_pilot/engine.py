#!/usr/bin/env python3
"""Fixed-large selector and joint small-block cases."""
import importlib.util
from itertools import combinations
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent


def module(name, path):
    spec=importlib.util.spec_from_file_location(name,path)
    obj=importlib.util.module_from_spec(spec);spec.loader.exec_module(obj);return obj


J=module('joint_interface',HERE.parent/'hadwiger_nelson_heule517_joint_interface/engine.py')
P=module('prior_full_pilot',HERE.parent/'hadwiger_nelson_heule517_family_pilot/engine.py')


def inputs():
    data,sep=J.geometry();S=sep['small'];ss=set(S)
    data.update(sep);data['small_edges']=[e for e in data['edges'] if set(e)<=ss]
    data['profiles']=json.loads((J.HERE/'certificate.json').read_text())['rows']
    data['prior_rows']=json.loads((P.HERE/'certificate.json').read_text())['rows']
    return data


def master(rows, small):
    pos={v:i for i,v in enumerate(small)}
    n,cs=P.atleast(len(small),9)
    cs += [[-pos[v]-1 for v in row['D']] for row in rows]
    return n,cs


def activated_case(data, k):
    S=data['small'];n,cs=J.small_case(S,data['small_edges'],data['cross_edges'],data['boundary'],data['profiles'][k]['pattern'])
    for i in range(len(S)):cs[i]=[-n-i-1]+cs[i]
    return n+len(S),cs


def full_colour(row,data):
    if row['kind']=='seed':return P.decode(data['prior_rows'][row['row']],data)
    out=['.']*517
    for v,c in zip(data['large'],data['profiles'][row['case']]['colouring']):out[v]=c
    for v,c in zip(data['small'],row['colouring']):out[v]=c
    return ''.join(out)


def checked(row,data):
    c=full_colour(row,data);D=P.check_colouring(c,data['edges'])
    assert list(D)==row['D'] and set(D)<=set(data['small'])


def initial(data):
    rows=[];S=set(data['small'])
    for i,r in enumerate(data['prior_rows']):
        if set(r['D'])<=S:
            row={'kind':'seed','row':i,'D':r['D']};checked(row,data);rows.append(row)
    assert len(rows)==148
    return rows


def extend(colour,k,data):
    row={'kind':'case','case':k,'colouring':colour}
    c=full_colour(row,data);c=P.extend(c,data['adj'],data['small'])
    row['colouring']=''.join(c[v] for v in data['small'])
    row['D']=[v for v,c in enumerate(c) if c=='.'];checked(row,data);return row


def minimal(rows):
    out=[]
    for r in sorted(rows,key=lambda r:(len(r['D']),r['D'])):
        if not any(set(t['D'])<=set(r['D']) for t in out):out.append(r)
    return out
