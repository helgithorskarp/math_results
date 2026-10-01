#!/usr/bin/env python3
"""Exact column producer of selected clamping and saturation-event witnesses."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parent
PIN='dca9c8d6331c3fc548c514ca8f5f1cd170f4a0bb39a3c05250876247d0362719'
FAMILIES=[('one_minimum',1,0),('one_maximum',0,1),('two_minima',2,0),
          ('two_maxima',0,2),('mixed_pair',1,1),
          ('three_minima_one_maximum',3,1),('four_maxima',0,4)]

def sha(obj):
    return hashlib.sha256(json.dumps(obj,separators=(',',':')).encode()).hexdigest()

def events(envelope):
    result=[]
    for a in range(13):
        for b in range(13):
            if a==b:continue
            merged={};hit=False
            for mask,c in envelope:
                ta,tb=(mask>>a)&1,(mask>>b)&1
                touched=bool(ta or tb);hit|=touched
                out=mask^((1<<a)|(1<<b)) if ta>tb else mask
                merged[out]=max(merged.get(out,0),c+int(touched))
            result.append([a,b,sum(1<<c for c in merged.values()),int(hit)])
    return result

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--profile',type=Path,default=ROOT.parent.parent/'six-sorting-2/semantic-pruning/profile.py')
    args=parser.parse_args()
    if hashlib.sha256(args.profile.read_bytes()).hexdigest()!=PIN:
        raise ValueError('published column dependency changed')
    spec=importlib.util.spec_from_file_location('pinned_columns',args.profile)
    p=importlib.util.module_from_spec(spec);spec.loader.exec_module(p)
    fixture=json.loads((ROOT/'fixture.json').read_text())
    certificate={'schema':'four-native-prefix-saturation-deadlocks-v1',
                 'agent':'six-sorting-1','role':'researcher','budget':44,
                 'column_dependency_sha256':PIN,'cases':[]}
    for case in fixture['cases']:
        prefix=case['prefix'];data={}
        for name,lo,hi in FAMILIES:
            data[name]=p.analyze_family(13,prefix,lo,hi)
        high=data['four_maxima'];support=[[r[1],r[3]] for r in high['envelope']]
        expected=([[6912,18],[7680,18]] if case['kernel_id']!=26 else
                  [[6912,17],[7424,17],[7680,18]])
        if support!=expected:raise ValueError('fixture saturation support differs')
        witnesses=[]
        for mask,c in support:
            witnesses.append(next(r for r in high['records'] if r[3]==mask and r[4]+r[5]==c))
        out={'kernel_id':case['kernel_id'],'prefix_size':len(prefix),
             'prefix_sha256':sha(prefix),'mode':case['mode'],
             'four_high_witnesses':witnesses,'weighted_support':support,
             'oriented_event_cover':events(support),'comparison_profiles':{}}
        if case['mode']=='coupled_activity':
            before=next(r for r in data['two_maxima']['records'] if r[:2]==[0,case['blocking_high_input_mask']])
            after_data=p.analyze_family(13,prefix+[[8,10]],0,2)
            after=next(r for r in after_data['records'] if r[:2]==before[:2])
            if before[2:6]!=[0,6144,9,0] or after[2:6]!=[0,6144,9,1]:
                raise ValueError('coupled inactive witness differs')
            out['blocking_two_high_before']=before
            out['blocking_two_high_after_forced_gate']=after
        for name,item in data.items():
            out['comparison_profiles'][name]={
                'low_count':item['low_count'],'high_count':item['high_count'],
                'envelope':item['envelope'],'summary':item['summary'],
                'records_sha256':sha(item['records']),
                'semantic_cost_sum':sum(r[4]+r[5] for r in item['records'])}
        certificate['cases'].append(out)
        print('DEADLOCK_WITNESSES_PRODUCED',case['kernel_id'],len(prefix),flush=True)
    target=ROOT/'certificate.json'
    target.write_text(json.dumps(certificate,indent=2)+'\n')
    print('CERTIFICATE',target.stat().st_size,hashlib.sha256(target.read_bytes()).hexdigest(),flush=True)

if __name__=='__main__':main()
