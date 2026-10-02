"""Private inner-anchor refinement of constant16 inconclusive fronts only.
One branch per stage; exact original3+3 cubes and oriented carrier functions.
Subset mass>2^44 is a proposal until independently replayed. Others stay open.
"""
import argparse
from collections import Counter
from functools import lru_cache
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
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);return module


def digest(obj):
    return hashlib.sha256(json.dumps(obj,separators=(',',':')).encode()).hexdigest()


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--branch',type=int,required=True)
    args=parser.parse_args();start=time.monotonic();deadline=start+45
    producer=load('one_prior_full_packed_carrier',PUBLIC/'pruning.py')
    anchors=load('one_prior_full_packed_anchor',PUBLIC/'anchors.py')
    intake=json.loads((ROOT/'work/partner4-one-prior-singleton-fronts.json').read_text())
    baseline=json.loads((ROOT/f'work/partner4-one-prior-constant-branch{args.branch}.json').read_text())
    prior=json.loads((ROOT/'work/low26-HIGH-binary-selected-screen.json').read_text())
    pool=sorted({tuple(p) for p in prior['selected_original_pool']});need(len(pool)==99,'Original proposal pool differs')
    indices=baseline['inconclusive_front_indices']
    @lru_cache(None)
    def inner(word):
        data=anchors.semantic.analyze(7,[list(g) for g in word]);bounds=anchors.both(7,data)
        return max(16,*(r['lower_bound'] for r in bounds.values()))
    cases=[];counts=Counter();status='COMPLETE_PRIVATE_FULL_NESTED_REFINEMENT_NEEDS_INDEPENDENT_REPLAY'
    for index in indices:
        if time.monotonic()>deadline:
            status='INCOMPLETE_OPERATIONAL45_SECOND_GUARD_NOT_AN_EXCLUSION';break
        front=intake['survivors'][index];word=front['prefix'];candidates=[]
        for lo,hi in pool:
            p=producer.pruning(word,lo,hi,anchors.semantic)
            candidates.append((sum(p['outer_record'][4:6]),lo,hi,p))
        classes={};tested=0;stopped=False
        for credit,lo,hi,p in sorted(candidates,key=lambda r:(-r[0],r[1],r[2])):
            if time.monotonic()>deadline:
                stopped=True;status='INCOMPLETE_OPERATIONAL45_SECOND_GUARD_NOT_AN_EXCLUSION';break
            q=tuple(tuple(g) for g in p['retained_prefix']);B=inner(q);record=p['outer_record'];z=tuple(record[2:4]);label=credit+B
            if z not in classes or label>classes[z]['label']:
                classes[z]={'original_LOW_mask':lo,'original_HIGH_mask':hi,'outer_record':record,
                            'retained_Q_sha256':digest(q),'B7':B,'label':label}
            tested+=1
            if sum(1<<r['label'] for r in classes.values())>1<<44:break
        if stopped:break
        mass=sum(1<<r['label'] for r in classes.values());selected=[];selected_mass=0
        for r in sorted(classes.values(),key=lambda r:(-r['label'],r['outer_record'][2:4])):
            selected.append(r);selected_mass+=1<<r['label']
            if selected_mass>1<<44:break
        counts['complete_refined_fronts']+=1;counts['nested_excluded' if mass>1<<44 else 'nested_inconclusive']+=1
        counts['selected_occurrences']+=len(selected)
        cases.append({'front_index':index,'branch_id':args.branch,'function_id':front['function_id'],
                      'singleton':front['singleton'],'tail_id':front['tail_id'],'prefix_sha256':front['prefix_sha256'],
                      'nine_core_sha256':front['nine_core_sha256'],'remaining_gate_budget':front['remaining_gate_budget'],
                      'producer_exceeds44':mass>1<<44,'selected_mass':selected_mass,
                      'proposals_tested':tested,'selected_witnesses':selected})
    out={'agent':'six-sorting-1','role':'researcher','status':status,'branch_id':args.branch,
         'total_constant16_inconclusive_fronts':len(indices),'census':dict(counts),
         'cases':cases,'finite_cases_sha256':digest(cases),'distinct_inner_words':inner.cache_info().currsize,
         'selected_B7_counts':dict(Counter(w['B7'] for c in cases for w in c['selected_witnesses'])),
         'inconclusive_front_indices':[r['front_index'] for r in cases if not r['producer_exceeds44']],
         'uncomputed_front_indices':indices[len(cases):],
         'minimum_selected_mass':min((r['selected_mass'] for r in cases),default=0),
         'same_author_producer_only':True,'external_person_review_claimed':False,
         'scope':'ExactlyONE priorHIGH equal merge afterL4; current99 proposal-pool inner-anchor refinement only; passing/partial bound is not existence or global exclusion.',
         'seconds':time.monotonic()-start,'maximum_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
    (ROOT/f'work/partner4-one-prior-full-branch{args.branch}.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k!='cases'},sort_keys=True))


if __name__=='__main__':main()
