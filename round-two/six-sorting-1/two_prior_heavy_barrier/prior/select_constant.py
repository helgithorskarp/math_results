"""Private constantS7>=16 selected original3+3 screen, one branch per stage.
All99 proposals are exact whole original cubes. Inconclusive <=2^44 is open.
No inner anchor calculation, timeout/partial result is never an exclusion.
"""
import argparse
from collections import Counter
import hashlib
import importlib.util
import json
from pathlib import Path
import resource
import time

ROOT=Path(__file__).resolve().parent
PUBLIC=ROOT


def need(test,message):
    if not test:raise ValueError(message)


def load(name,path):
    spec=importlib.util.spec_from_file_location(name,path)
    m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m


def digest(obj):
    return hashlib.sha256(json.dumps(obj,separators=(',',':')).encode()).hexdigest()


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--branch',type=int,required=True)
    args=parser.parse_args();start=time.monotonic();deadline=start+45
    producer=load('one_prior_packed_carrier',PUBLIC/'pruning.py')
    semantic=load('one_prior_packed_profile',PUBLIC/'profile.py')
    intake=json.loads((ROOT/'work/partner4-one-prior-singleton-fronts.json').read_text())
    prior=json.loads((ROOT/'work/low26-HIGH-binary-selected-screen.json').read_text())
    pool=sorted({tuple(p) for p in prior['selected_original_pool']});need(len(pool)==99,'Original proposal pool differs')
    fronts=[(i,r) for i,r in enumerate(intake['survivors']) if r['branch_id']==args.branch]
    cases=[];counts=Counter();minimum=None
    for index,front in fronts:
        need(time.monotonic()<deadline,'Operational45s stage guard; incomplete constant screen is not an exclusion')
        word=front['prefix'];classes={}
        for lo,hi in pool:
            p=producer.pruning(word,lo,hi,semantic);record=p['outer_record'];label=sum(record[4:6])+16
            z=tuple(record[2:4]);candidate={'original_LOW_mask':lo,'original_HIGH_mask':hi,
                 'outer_record':record,'retained_Q_sha256':digest(p['retained_prefix']), 'B7':16,'label':label}
            if z not in classes or label>classes[z]['label']:classes[z]=candidate
        mass=sum(1<<c['label'] for c in classes.values());closed=mass>1<<44
        selected=[];selected_mass=0
        for c in sorted(classes.values(),key=lambda r:(-r['label'],r['outer_record'][2:4])):
            selected.append(c);selected_mass+=1<<c['label']
            if selected_mass>1<<44:break
        counts['complete_fronts']+=1;counts['constant16_excluded' if closed else 'constant16_inconclusive']+=1
        counts['selected_occurrences']+=len(selected)
        minimum=selected_mass if minimum is None else min(minimum,selected_mass)
        cases.append({'front_index':index,'branch_id':args.branch,'function_id':front['function_id'],
             'singleton':front['singleton'],'tail_id':front['tail_id'],'prefix_sha256':front['prefix_sha256'],
             'remaining_gate_budget':front['remaining_gate_budget'],'nine_core_sha256':front['nine_core_sha256'],
             'whole99_class_mass':mass,'class_count':len(classes),'constant16_exceeds44':closed,
             'selected_mass':selected_mass,'selected_witnesses':selected})
    out={'agent':'six-sorting-1','role':'researcher','status':'COMPLETE_PRIVATE_CONSTANT16_NESTED_SCREEN_NEEDS_INDEPENDENT_REPLAY',
         'branch_id':args.branch,'proposal_pool_size':99,'intake_records_sha256':intake['finite_records_sha256'],
         'census':dict(counts),'minimum_selected_mass':minimum,'finite_cases_sha256':digest(cases),'cases':cases,
         'inconclusive_front_indices':[r['front_index'] for r in cases if not r['constant16_exceeds44']],
         'same_author_producer_only':True,'external_person_review_claimed':False,
         'scope':'Partner4 exactlyONE pre-singleton HIGH equal merge; selected original3+3 nested constant16 only; <=2^44 remains open.',
         'seconds':time.monotonic()-start,'maximum_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
    (ROOT/f'work/partner4-one-prior-constant-branch{args.branch}.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k!='cases'},sort_keys=True))


if __name__=='__main__':main()
