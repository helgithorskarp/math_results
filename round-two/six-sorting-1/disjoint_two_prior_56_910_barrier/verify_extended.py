"""Scalar entire original128-input/carrier replay of additional clamp witnesses."""
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


def main():
    operations_allow()
    first,last=map(int,sys.argv[1:3]);start=time.monotonic();deadline=start+45
    front=json.loads((WORK/f'fronts03-{first:05}-{last:05}.json').read_text())
    old, fresh_front, fresh_partition = current_cases(first,last)
    proposal=json.loads((WORK/f'extended-{first:05}-{last:05}.json').read_text())
    normal=json.loads((WORK/f'check03-{first:05}-{last:05}.json').read_text())
    optimized=json.loads((WORK/f'check03-{first:05}-{last:05}-O.json').read_text())
    need(normal['finite']==optimized['finite'] and normal['finite']['producer_front_sha256']==front['finite_sha256'],
         'Actual full front cover not scalar-checked normally/O')
    indices=[r['front_index'] for r in old['cases'] if not r['constant16_exceeds44']]
    need(proposal['finite']['actual_genuine_miss_front_indices']==indices and
         [r['front_index'] for r in proposal['cases']]==indices and
         proposal['finite']['actual_complete_front_sha256']==front['finite_sha256'] and
         proposal['finite']['old_constant_cases_sha256']==digest(old['cases'])==old['cases_sha256'] and
         digest(proposal['cases'])==proposal['finite']['extended_cases_sha256'], 'Complete genuine-miss binding differs')
    pin=next(r['sha256'] for r in json.loads((PUBLIC/'source-manifest.json').read_text())['files'] if r['path']=='numeric.py')
    need(hashlib.sha256((PUBLIC/'numeric.py').read_bytes()).hexdigest()==pin,'Credited independent scalar source changed')
    s=importlib.util.spec_from_file_location('extended_independent_scalar_outer',PUBLIC/'numeric.py')
    numeric=importlib.util.module_from_spec(s);s.loader.exec_module(numeric)
    records=[];masses=[];open_indices=[];occurrences=0
    for case in proposal['cases']:
        operations_allow();need(time.monotonic()<deadline,'Incomplete45s scalar extended replay')
        index=case['front_index'];row=front['survivors'][index]
        need(case['function_id']==row['function_id'] and case['prefix_sha256']==row['prefix_sha256'] and
             case['nine_core_sha256']==row['nine_core_sha256'],'Actual literal front differs')
        if not case['constant16_exceeds44']:
            open_indices.append(index);continue
        tags=set();mass=0
        for w in case['selected_witnesses']:
            low,high=w['original_LOW_mask'],w['original_HIGH_mask']
            need(low.bit_count()==high.bit_count()==3 and not low&high and (low|high)<8192,
                 'Not an immutable disjoint original3+3 clamp')
            actual=numeric.family(13,row['prefix'],low,high,'outer')
            need(actual==w['outer_record'],'Whole original scalar record differs')
            pruned=numeric.pruning(13,row['prefix'],actual)
            need(digest(pruned['retained_prefix'])==w['retained_Q_sha256'],'Entire oriented carrier prefix differs')
            need(w['B7']==16 and w['label']==actual[4]+actual[5]+16,'Unjustified constant7 bound')
            current=tuple(actual[2:4]);need(current not in tags,'Duplicate current dyadic class')
            tags.add(current);mass+=1<<w['label'];occurrences+=1
            records.append([index,actual,digest(pruned),w['label']])
        need(mass==case['selected_mass'] and mass>1<<44,'Strict extended original inequality fails')
        masses.append([index,mass])
    finite={'retained_interval':[first,last],'entire_case_front_indices':indices,
            'extended_cases_sha256':proposal['finite']['extended_cases_sha256'],
            'actual_complete_front_sha256':front['finite_sha256'],
            'independently_positive_cases':len(masses),'remaining_open_indices':open_indices,
            'selected_original_occurrences':occurrences,'replay_sha256':digest(records),
            'root_masses_sha256':digest(masses),'minimum_selected_mass':min((r[1] for r in masses),default=None),
            'metrics':numeric.METRICS,'credited_scalar_source_sha256':pin}
    result={'agent':'six-sorting-1','role':'researcher','status':'COMPLETE_EXTENDED_ORIGINAL_SCALAR_CUBE_AND_CARRIER_REPLAY',
            'finite':finite,'finite_sha256':digest(finite),'seconds':time.monotonic()-start,
            'maximum_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
            'external_person_review_claimed':False}
    suffix='-O' if not __debug__ else ''
    (WORK/f'extended-check-{first:05}-{last:05}{suffix}.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()
