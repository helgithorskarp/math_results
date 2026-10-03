"""Extend sufficient original3+3 witnesses; every unclosed case stays open."""
from itertools import combinations
import hashlib
import importlib.util
import json
from pathlib import Path
import resource
import sys
import time

from controls import operations_allow
from inputs import digest, need, current_cases

ROOT=Path(__file__).resolve().parent
WORK=ROOT/'work'
PUBLIC=ROOT/'prior'


def load_module(name,path):
    s=importlib.util.spec_from_file_location(name,path)
    m=importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m


def main():
    operations_allow()
    first,last=map(int,sys.argv[1:3])
    start=time.monotonic();deadline=start+45
    old, fresh_front, fresh_partition = current_cases(first,last)
    front=json.loads((WORK/f'fronts03-{first:05}-{last:05}.json').read_text())
    normal=json.loads((WORK/f'check03-{first:05}-{last:05}.json').read_text())
    optimized=json.loads((WORK/f'check03-{first:05}-{last:05}-O.json').read_text())
    need(normal['finite']==optimized['finite'] and normal['finite']['producer_front_sha256']==front['finite_sha256'],
         'Whole actual front interface has not passed scalar normal/O')
    need(digest(old['cases'])==old['cases_sha256'],'Old original-pool cases changed')
    indices=[r['front_index'] for r in old['cases'] if not r['constant16_exceeds44']]
    need(0<len(indices)<=32,'Require 1..32 genuine sufficient misses')
    pins={r['path']:r['sha256'] for r in json.loads((PUBLIC/'source-manifest.json').read_text())['files']}
    for name in ('profile.py','pruning.py','fixture.json'):
        need(hashlib.sha256((PUBLIC/name).read_bytes()).hexdigest()==pins[name],'Credited packed source changed')
    profile=load_module('extended_original_packed_profile',PUBLIC/'profile.py')
    pruning=load_module('extended_original_packed_pruning',PUBLIC/'pruning.py')
    pool=json.loads((PUBLIC/'fixture.json').read_text())['selected_original_pool']
    masks=sorted(sum(1<<p for p in row) for row in combinations(range(13),3))
    cases=[]
    for index in indices:
        operations_allow()
        row=front['survivors'][index]
        classes={};seen=set();tested=0

        def proposal(low,high):
            nonlocal tested
            need(time.monotonic()<deadline,'Incomplete45s extended original selector; no exclusion')
            if (low,high) in seen:return
            seen.add((low,high));tested+=1
            r=pruning.pruning(row['prefix'],low,high,profile)
            original=r['outer_record'];key=tuple(original[2:4]);label=original[4]+original[5]+16
            w={'original_LOW_mask':low,'original_HIGH_mask':high,'outer_record':original,
               'retained_Q_sha256':digest(r['retained_prefix']),'B7':16,'label':label}
            if key not in classes or label>classes[key]['label']:classes[key]=w

        for low,high in pool:proposal(low,high)
        initial_mass=sum(1<<w['label'] for w in classes.values())
        need(initial_mass==old['cases'][index]['whole99_class_mass'],'Original pool mass did not reproduce')
        finished=False
        for low in masks:
            for high in masks:
                if low&high:continue
                proposal(low,high)
                if sum(1<<w['label'] for w in classes.values())>1<<44:
                    finished=True;break
            if finished:break
        witnesses=[];mass=0
        for w in sorted(classes.values(),key=lambda w:(-w['label'],w['outer_record'][2:4])):
            witnesses.append(w);mass+=1<<w['label']
            if mass>1<<44:break
        cases.append({'front_index':index,'function_id':row['function_id'],
                      'prefix_sha256':row['prefix_sha256'],'nine_core_sha256':row['nine_core_sha256'],
                      'original99_class_mass':initial_mass,'tested_original_pairs':tested,
                      'constant16_exceeds44':mass>1<<44,'selected_mass':mass,'selected_witnesses':witnesses})
    finite={'retained_interval':[first,last],'actual_genuine_miss_front_indices':indices,
            'actual_complete_front_sha256':front['finite_sha256'],'old_constant_cases_sha256':old['cases_sha256'],
            'extended_cases_sha256':digest(cases),'positive_count':sum(r['constant16_exceeds44'] for r in cases),
            'remaining_open_indices':[r['front_index'] for r in cases if not r['constant16_exceeds44']],
            'native_threads':1,'imported_negative_corpus_count':0}
    out={'agent':'six-sorting-1','role':'researcher','status':'EXTENDED_ORIGINAL_POOL_PROPOSALS_REQUIRE_SCALAR_REPLAY',
         'finite':finite,'finite_sha256':digest(finite),'cases':cases,'seconds':time.monotonic()-start,
         'maximum_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
    (WORK/f'extended-{first:05}-{last:05}.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k!='cases'},indent=2))


if __name__=='__main__':main()
