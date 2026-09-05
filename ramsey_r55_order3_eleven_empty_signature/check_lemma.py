#!/usr/bin/env python3
"""Definition-level core/witness/fixture checking; imports no producer."""
from itertools import combinations
from pathlib import Path
import argparse
import hashlib
import json


def need(ok, why):
    if not ok:
        raise ValueError(why)


def matrix(bits):
    need(len(bits)==18 and set(bits)<=set('01'),'core bits')
    red = {tuple(e) for i in range(4) for e in combinations(range(3*i,3*i+3),2)}
    for pair_no,(i,j) in enumerate(combinations(range(4),2)):
        for offset in range(3):
            if bits[3*pair_no+offset]=='1':
                for phase in range(3):
                    red.add((3*i+phase,3*j+(phase+offset)%3))
    return red


def monochromatic(red, vertices, k, color):
    return [list(s) for s in combinations(vertices,k)
            if all(((a,b) in red)==color for a,b in combinations(s,2))]


def check(source):
    root=Path(__file__).resolve().parent
    previous=root.parent/'ramsey_r55_order3_eleven_residual_sweep'
    old_raw=(previous/'result.json').read_bytes()
    need(hashlib.sha256(old_raw).hexdigest()=='aa6fe619507d058d69aadf36f5ef92ec7bc073f5cfab2d1e99b3191d8b2e658c','run input')
    old=json.loads(old_raw)
    case_raw=(previous/'cases.json').read_bytes()
    need(hashlib.sha256(case_raw).hexdigest()=='b14870da74f34b18f326b649be79452d05ff6517dcf21a86af47b7caad3c3a65','case input')
    cases={r['index']:r for r in json.loads(case_raw)}
    report=json.loads((source/'classification.json').read_text())
    need([r['index'] for r in report['rows']]==old['open'],'full residual coverage')
    selected=[]
    for row in report['rows']:
        case=cases[row['index']]
        need(all(row[k]==case[k] for k in ['bits','labeled']),'core identity')
        need(len(row['blue_triangles'])==4,'four witness slots')
        red=matrix(row['bits'])
        need(not monochromatic(red,range(12),5,True) and not monochromatic(red,range(12),5,False),'core Ramsey property')
        found=[]
        for omit in range(4):
            vertices=[v for v in range(12) if v//3!=omit]
            blue=monochromatic(red,vertices,3,False)
            witness=row['blue_triangles'][omit]
            need(witness in blue if blue else witness is None,'blue triangle witness/completeness')
            found.append(bool(blue))
        need(row['forces_empty']==all(found),'hypothesis classification')
        if all(found):selected.append(row['index'])
    need(report['selected']==selected and report['other']==[i for i in old['open'] if i not in selected],'split lists')
    need(report['selected_labeled']==sum(cases[i]['labeled'] for i in selected),'multiplicity')
    fixtures=json.loads((source/'fixtures.json').read_text())
    summaries={}
    for name, f in fixtures.items():
        n=f['vertices'];edges=[tuple(e) for e in f['red_edges']]
        need(edges==sorted(set(edges)) and all(0<=a<b<n for a,b in edges),'edge list')
        red=set(edges);sig=f['signatures']
        need(n==12+len(sig),'fixture dimensions')
        need(red & set(combinations(range(12),2))==matrix(f['core_bits']),'fixture core')
        for j,s in enumerate(sig,12):
            need(all(((i,j) in red)==bool(s>>(i//3)&1) for i in range(12)),'uniform signature')
        need(not monochromatic(red,range(n),5,True) and not monochromatic(red,range(n),5,False),'fixture K5')
        summaries[name]=dict(vertices=n,red_edges=len(edges),empty_signatures=sig.count(0),ramsey=True)
    need(fixtures['local_zero_empty']['vertices']==22 and summaries['local_zero_empty']['empty_signatures']==0,'local limitation')
    need(fixtures['local_zero_empty']['core_bits']==cases[87]['bits'],'local core')
    need(fixtures['repeated_singleton']['signatures']==[1,1] and fixtures['repeated_singleton']['core_bits']==cases[194]['bits'],'hypothesis limitation')
    # The first four coordinates are a prefix of the normalized full row.
    rows=sorted(tuple((mask>>i)&1 for i in range(11)) for mask in range(2048))
    prefixes=[row[:4] for row in rows]
    need(prefixes==sorted(prefixes) and prefixes[:128]==[(0,0,0,0)]*128 and prefixes[128]!=(0,0,0,0),'full-row prefix bridge')
    return dict(verified=True,checked_classes=45,selected=selected,selected_labeled=report['selected_labeled'],
                complete_literal_triple_trials=45*4*84,full_rows_checked=2048,fixtures=summaries)


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);p.add_argument('--report',type=Path,required=True)
    a=p.parse_args();r=check(a.source);a.report.parent.mkdir(parents=True,exist_ok=True)
    a.report.write_text(json.dumps(r,sort_keys=True,indent=2)+'\n');print(json.dumps(r,sort_keys=True))
