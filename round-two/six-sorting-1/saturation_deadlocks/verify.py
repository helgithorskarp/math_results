#!/usr/bin/env python3
"""Standalone scalar proof-witness and complete oriented-event checker.

Imports no producer, column profiler, construction engine, solver, or sibling
module. It verifies the small witnesses sufficient for the deadlock proofs.
Use compare.py separately for the seven complete-family comparison profiles.
"""
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import resource
import time

ROOT=Path(__file__).resolve().parent
METRICS={'original_free_assignments':0,'scalar_gate_evaluations':0,
         'oriented_events':0,'full_boolean_control_inputs':0}

def need(condition,message):
    if not condition:raise ValueError(message)

def sha(obj):
    return hashlib.sha256(json.dumps(obj,separators=(',',':')).encode()).hexdigest()

def ports(values):
    return (sum(1<<i for i,x in enumerate(values) if x<0),
            sum(1<<i for i,x in enumerate(values) if x>1))

def single_domain(prefix,original_low,original_high):
    need(original_low&original_high==0,'clamping sets overlap')
    need(0<=original_low<8192 and 0<=original_high<8192,'clamping mask out of range')
    lows=[i for i in range(13) if original_low>>i&1]
    highs=[i for i in range(13) if original_high>>i&1]
    free=[i for i in range(13) if i not in lows and i not in highs]
    template=[0]*13
    for j,i in enumerate(lows):template[i]=j-len(lows)
    for j,i in enumerate(highs):template[i]=2+j
    touched,active=0,0;final_ports=None
    for assignment in range(1<<len(free)):
        values=list(template)
        for j,i in enumerate(free):values[i]=(assignment>>j)&1
        this_touched=0
        for t,(a,b) in enumerate(prefix):
            hit=values[a]<0 or values[a]>1 or values[b]<0 or values[b]>1
            if hit:this_touched|=1<<t
            if values[a]>values[b]:
                if not hit:active|=1<<t
                values[a],values[b]=values[b],values[a]
        if assignment==0:touched=this_touched;final_ports=ports(values)
        need(touched==this_touched,'marked trajectory depends on free inputs')
        need(final_ports==ports(values),'marked final ports depend on free inputs')
        METRICS['original_free_assignments']+=1
        METRICS['scalar_gate_evaluations']+=len(prefix)
    redundant=((1<<len(prefix))-1)&~(touched|active)
    return [original_low,original_high,*final_ports,touched.bit_count(),redundant.bit_count(),redundant]

def scalar_events(support):
    table=[]
    for a in range(13):
        for b in range(13):
            if a==b:continue
            successors={};any_hit=False
            for mask,cost in support:
                tags=[2 if mask>>i&1 else 0 for i in range(13)]
                hit=tags[a]>1 or tags[b]>1;any_hit|=hit
                if tags[a]>tags[b]:tags[a],tags[b]=tags[b],tags[a]
                after=sum(1<<i for i,x in enumerate(tags) if x>1)
                successors[after]=max(successors.get(after,0),cost+int(hit))
            table.append([a,b,sum(1<<c for c in successors.values()),int(any_hit)])
            METRICS['oriented_events']+=1
    return table

def validate(certificate,fixture,positive=True):
    need(certificate['schema']=='four-native-prefix-saturation-deadlocks-v1','wrong schema')
    need(certificate['budget']==44,'wrong size budget')
    need([x['kernel_id'] for x in certificate['cases']]==[11,17,19,26],'wrong case coverage')
    need(len(fixture['cases'])==4,'wrong fixture count')
    for claimed,case in zip(certificate['cases'],fixture['cases']):
        prefix=case['prefix'];n=len(prefix)
        need(claimed['kernel_id']==case['kernel_id'],'case labels differ')
        need(all(len(g)==2 and all(type(i)is int for i in g) and 0<=g[0]<g[1]<13 for g in prefix),
             'nonstandard literal fixture')
        need(claimed['prefix_size']==n and claimed['prefix_sha256']==sha(prefix),'prefix differs')
        need(claimed['mode']==case['mode'],'proof mechanism differs')
        support=[]
        for record in claimed['four_high_witnesses']:
            need(len(record)==7 and record[0]==0 and record[1].bit_count()==4,'not a four-high witness')
            rebuilt=single_domain(prefix,record[0],record[1])
            need(rebuilt==record,'scalar four-high record differs')
            support.append([record[3],record[4]+record[5]])
        expected=([[6912,18],[7680,18]] if case['kernel_id']!=26 else
                  [[6912,17],[7424,17],[7680,18]])
        need(support==expected and claimed['weighted_support']==support,'saturated support differs')
        need(sum(1<<c for _,c in support)==1<<19,'support does not saturate the size44 cap')
        table=scalar_events(support)
        need(table==claimed['oriented_event_cover'],'complete oriented event cover differs')
        allowed=[r[:2] for r in table if r[2]<=1<<19 and r[3]]
        if case['mode']=='coupled_activity':
            need(allowed==[[8,10],[10,8]],'allowed first marked event differs')
            before=claimed['blocking_two_high_before']
            after=claimed['blocking_two_high_after_forced_gate']
            need(before[:2]==[0,case['blocking_high_input_mask']],'blocking input family differs')
            need(before[1].bit_count()==2,'blocking family is not two-high')
            need(single_domain(prefix,*before[:2])==before,'blocking prefix record differs')
            need(single_domain(prefix+[[8,10]],*before[:2])==after,'blocking forced-event record differs')
            need(before[2:]==[0,6144,9,0,0],'pair budget is not saturated')
            need(after[2:]==[0,6144,9,1,1<<n],'forward merge is not a full-domain identity')
            # Reverse merging freezes the high at8. Sorted four-high outputs
            # must be9..12, and touching8 again would increase C beyond19.
            reverse={}
            for mask,c in support:
                tags=[2 if mask>>i&1 else 0 for i in range(13)]
                if tags[10]>tags[8]:tags[10],tags[8]=tags[8],tags[10]
                out=sum(1<<i for i,x in enumerate(tags) if x>1)
                reverse[out]=max(reverse.get(out,0),c+1)
            need(reverse=={6912:19},'reverse merge does not freeze the wrong high port')
        else:
            need(case['mode']=='no_marked_event' and allowed==[],'deadlock has a permitted marked event')
        need(any(mask!=7680 for mask,_ in support),'all witness configurations already terminal')
    if positive:
        control=fixture['known45_control'];need(len(control)==45,'wrong positive sorter size')
        for x in range(8192):
            values=[(x>>p)&1 for p in range(13)]
            wanted=sorted(values)
            for a,b in control:
                if values[a]>values[b]:values[a],values[b]=values[b],values[a]
            need(values==wanted,'known45 positive control fails')
            METRICS['full_boolean_control_inputs']+=1

def main():
    start=time.monotonic()
    certificate=json.loads((ROOT/'certificate.json').read_text())
    fixture=json.loads((ROOT/'fixture.json').read_text())
    validate(certificate,fixture)
    main_metrics=dict(METRICS)
    damaged=[]
    first=deepcopy(certificate);first['cases'][0]['four_high_witnesses'][0][4]-=1;damaged.append(first)
    second=deepcopy(certificate);second['cases'][1]['blocking_two_high_after_forced_gate'][5]=0;damaged.append(second)
    third=deepcopy(certificate);third['cases'][3]['oriented_event_cover'].pop();damaged.append(third)
    for altered in damaged:
        try:validate(altered,fixture,positive=False)
        except ValueError:pass
        else:raise ValueError('damaged certificate was accepted')
    print(json.dumps({'agent':'six-sorting-1','role':'researcher',
                     'status':'ALL_FOUR_SATURATION_DEADLOCK_CHECKS_PASSED',
                     'prefix_sizes':[len(x['prefix']) for x in fixture['cases']],
                     'corruptions_rejected':len(damaged),
                     'certificate_sha256':hashlib.sha256((ROOT/'certificate.json').read_bytes()).hexdigest(),
                     'seconds':time.monotonic()-start,
                     'maximum_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                     **main_metrics},sort_keys=True))

if __name__=='__main__':main()
