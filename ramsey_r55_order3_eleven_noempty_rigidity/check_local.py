#!/usr/bin/env python3
"""Check small literal Ramsey obstructions without SAT, DRAT or producer imports."""
from itertools import combinations
from pathlib import Path
import argparse
import copy
import hashlib
import json


def need(ok,why):
    if not ok:raise ValueError(why)


def check(data):
    need(data['core']==194 and data['bits']=='100110110110110100' and data['vertices']==22,'core identity')
    expected=sorted(sorted([1,1,2,2,4,4,8,8,p,q]) for p,q in combinations([3,5,6,9,10,12],2))
    need(len(data['cases'])==15,'fifteen-case coverage')
    core={};offset=0
    for i in range(4):
        for edge in combinations(range(3*i,3*i+3),2):core[edge]=True
    for i,j in combinations(range(4),2):
        for shift in range(3):
            for s in range(3):core[3*i+s,3*j+(s+shift)%3]=data['bits'][offset+shift]=='1'
        offset+=3
    for n,(row,profile) in enumerate(zip(data['cases'],expected)):
        need(row['index']==n and sorted(row['fixed_masks'])==profile,'complete signature profile')
        color=dict(core)
        for f,m in enumerate(row['fixed_masks'],12):
            for v in range(12):color[v,f]=bool(m&(1<<(v//3)))
        # Every newly forced blue edge is justified by a literal red triangle.
        need(len(row['forced_blue'])==3,'three forced fixed edges')
        for witness in row['forced_blue']:
            e=witness['edge'];t=witness['red_triangle']
            need(len(set(e))==2 and all(12<=v<22 for v in e),'fixed endpoints')
            need(len(set(t))==3 and all(0<=v<12 for v in t),'core triangle')
            need(tuple(sorted(e)) not in color,'new forced edge')
            need(all(color[tuple(sorted(edge))] for edge in combinations(t,2)),'red witness triangle')
            need(all(color[v,f] for v in t for f in e),'red attachments to witness')
            color[tuple(sorted(e))]=False
        five=row['blue_k5'];need(len(set(five))==5 and all(0<=v<22 for v in five),'five distinct vertices')
        need(all(color.get(tuple(sorted(e))) is False for e in combinations(five,2)),'fully forced blue K5')
    return dict(verified=True,complete_profiles=15,forced_blue_edges=45,literal_blue_k5=15,
                solver_required=False,full_formula_required=False)


def main():
    p=argparse.ArgumentParser();p.add_argument('--certificate',type=Path,required=True);p.add_argument('--report',type=Path,required=True);a=p.parse_args()
    data=json.loads(a.certificate.read_text());answer=check(data);rejected=[]
    for name in ('missing_case','wrong_profile','wrong_core','false_triangle','repeated_vertex'):
        bad=copy.deepcopy(data)
        if name=='missing_case':bad['cases'].pop()
        if name=='wrong_profile':bad['cases'][0]['fixed_masks'][0]=0
        if name=='wrong_core':bad['bits']='0'+bad['bits'][1:]
        if name=='false_triangle':bad['cases'][0]['forced_blue'][0]['red_triangle']=[0,0,0]
        if name=='repeated_vertex':bad['cases'][0]['blue_k5']=[0,0,0,0,0]
        try:check(bad)
        except ValueError:rejected.append(name)
        else:raise ValueError('accepted malformed '+name)
    answer['rejected']=rejected
    answer['certificate_sha256']=hashlib.sha256(a.certificate.read_bytes()).hexdigest()
    answer['checker_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    a.report.write_text(json.dumps(answer,indent=2,sort_keys=True)+'\n');print(json.dumps(answer,sort_keys=True))


if __name__=='__main__':main()
