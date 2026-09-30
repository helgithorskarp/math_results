"""Corrupt stage, inherited-domain and complete-cover rejections."""
import copy
import itertools
import json
from pathlib import Path
import sys
import verify

HERE=Path(__file__).parent


def main():
    docs={root:[json.loads((HERE/'certificates'/f).read_text()) for f in files]
          for root,files in verify.ROOT_FILES.items()}
    baseline=verify.check_complete(documents=docs)
    colors,K,V,_=verify.premise(root=1662)
    original=docs[1662][0];mutations=[]
    def add(name,fn):
        d=copy.deepcopy(original);fn(d);mutations.append((name,d))
    add('missing_domain',lambda d:d.pop('domain_sha256'))
    add('wrong_domain',lambda d:d.update(domain_sha256='0'*64))
    add('hidden_forced_point',lambda d:d.update(forced=[2382]))
    add('hidden_forbidden_point',lambda d:d.update(forbidden=[2382]))
    add('hidden_larger_cap',lambda d:d.update(cap=198))
    add('wrong_phase',lambda d:d.update(phase=269))
    add('boolean_phase',lambda d:d.update(phase=True))
    add('wrong_root',lambda d:d.update(root=1427))
    add('boolean_root',lambda d:d.update(root=True))
    add('zero_denominator',lambda d:d.update(denominator=0))
    add('boolean_denominator',lambda d:d.update(denominator=True))
    add('capacity_overflow',lambda d:d.update(denominator=1))
    add('zero_AP_step',lambda d:d['AP_weights'][0].__setitem__(1,0))
    add('out_of_bounds_AP',lambda d:d['AP_weights'][0].__setitem__(0,3704))
    add('wrong_color_AP',lambda d:d['AP_weights'].__setitem__(0,[0,1,1]))
    add('zero_AP_weight',lambda d:d['AP_weights'][0].__setitem__(2,0))
    add('boolean_AP_weight',lambda d:d['AP_weights'][0].__setitem__(2,True))
    add('negative_AP_weight',lambda d:d['AP_weights'][0].__setitem__(2,-1))
    add('duplicate_AP',lambda d:d['AP_weights'].append(d['AP_weights'][0][:]))
    add('zero_bundle_weight',lambda d:d['bundle_weights'][0].__setitem__(1,0))
    add('boolean_bundle_weight',lambda d:d['bundle_weights'][0].__setitem__(1,True))
    add('repeated_bundle_AP',lambda d:d['bundle_weights'][0][0].__setitem__(1,d['bundle_weights'][0][0][0][:]))
    add('duplicate_bundle',lambda d:d['bundle_weights'].append(copy.deepcopy(d['bundle_weights'][0])))
    add('surcharge_on_fixed_zero',lambda d:d['surcharges'].append([next(iter(K[1])),1]))
    add('negative_surcharge',lambda d:d['surcharges'].append([next(iter(V)),-1]))
    add('boolean_surcharge',lambda d:d['surcharges'].append([next(iter(V)),True]))
    incidence={}
    for a,s,w in original['AP_weights']:
        A={a+j*s for j in range(7)}
        if not all(colors[x]==1 for x in A):continue
        for x in A&V:incidence.setdefault(x,[]).append([a,s])
    common=next(es[:3] for es in incidence.values() if len(es)>=3)
    add('triple_with_permitted_common_point',lambda d:d['bundle_weights'][0].__setitem__(0,common))
    rejected=[]
    for name,d in mutations:
        try:verify.check_stage(d,colors,V,root=1662)
        except (ValueError,KeyError,TypeError):rejected.append(name)
        else:raise ValueError('Accepted corrupted stage: '+name)
    changed_sets=[]
    def cover(name,fn):
        d=copy.deepcopy(docs);fn(d);changed_sets.append((name,d))
    for root in docs:
        cover('missing_root'+str(root),lambda d,root=root:d.pop(root))
    cover('extra_root',lambda d:d.update({722:copy.deepcopy(d[1427])}))
    cover('wrong_root_identity',lambda d:d[1662][0].update(root=1897))
    cover('missing_root1427_refinement',lambda d:d[1427].pop(0))
    cover('missing_root1427_contradiction',lambda d:d[1427].pop())
    cover('root1427_reversed_stages',lambda d:d[1427].reverse())
    cover('root2132_missing_first_screen',lambda d:d[2132].pop(0))
    cover('root2132_missing_zero_fix',lambda d:d[2132].pop(1))
    cover('root2132_missing_final_contradiction',lambda d:d[2132].pop())
    cover('root2132_reversed_stages',lambda d:d[2132].reverse())
    cover('root2132_million_scale_rounding_failure',lambda d:d[2132].__setitem__(1,
          dict(d[2132][1],denominator=1000000)))
    cover('extra_stage_after_exclusion',lambda d:d[1662].append(copy.deepcopy(d[1662][0])))
    cover('empty_root_chain',lambda d:d.update({1662:[]}))
    cover('no_strict_last_root',lambda d:d[2367][0].update(denominator=2_000_000))
    for name,d in changed_sets:
        try:verify.check_complete(documents=d)
        except (ValueError,KeyError,TypeError):rejected.append(name)
        else:raise ValueError('Accepted incomplete or mismatched full proof: '+name)
    # A claimed full domain cannot silently omit a point: even dropping a
    # truly forbidden point requires an earlier valid load-defect argument.
    for name,small in [('omit_arbitrary_domain_point',V-{next(iter(V))}),('reuse_another_root_screen',
                      set(baseline['root_results'][0]['stages'][0]['next_domain']))]:
        try:verify.check_stage(original,colors,small,root=1662)
        except (ValueError,KeyError,TypeError):rejected.append(name)
        else:raise ValueError('Accepted unproved inherited restriction')
    for cap in (198,True):
        try:verify.check_stage(original,colors,V,root=1662,cap=cap)
        except ValueError:rejected.append('illegal_runtime_cap'+str(cap))
        else:raise ValueError('Accepted wrong runtime cap')
    activated=anchor=defects=valid=0
    for flips in itertools.product((0,1),repeat=6):
        actual=[1]+[1-e for e in flips]
        verify.need((not all(c==actual[0] for c in actual))==any(flips),'Activated six-term truth table');activated+=1
    for flips in itertools.product((0,1),repeat=5):
        actual=[0,0]+list(flips)
        verify.need((not all(c==0 for c in actual))==any(flips),'Complete five-root anchor truth table');anchor+=1
    # Enumerate the general defect bridge on small integer-capacity models,
    # including exact positive overflow surcharges and point screens.
    for loads in itertools.product(range(7),repeat=3):
        gamma=sum(max(0,l-4) for l in loads)
        effective=[min(l,4) for l in loads]
        for W in range(1,13):
            adjusted=W-gamma
            for bits in itertools.product((0,1),repeat=3):
                E={i for i,b in enumerate(bits) if b}
                if len(E)>2:continue
                defects+=1
                if sum(loads[i] for i in E)<W:continue
                valid+=1
                verify.need(sum(effective[i] for i in E)>=adjusted,'Overflow-adjusted load lower bound')
                verify.need(all(4-effective[i]<=8-adjusted for i in E),'Nonnegative-defect individual screen')
    verify.need(verify.check_complete(documents=docs)==baseline,'Controls changed frozen data')
    print(json.dumps({'agent':'six-vdw-3','role':'researcher','all_rejected':True,'rejected_controls':len(rejected),
                      'names':rejected,'python_optimization':sys.flags.optimize,'activated_truth_cases':activated,
                      'anchor_truth_cases':anchor,'small_defect_models':defects,'models_meeting_load_lower_bound':valid}))


if __name__=='__main__':main()
