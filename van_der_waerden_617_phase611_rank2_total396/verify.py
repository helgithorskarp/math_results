"""Frozen proof replay: no proposer, numerical library or solver is imported."""
import argparse
import hashlib
import json
from pathlib import Path
from collections import Counter
import base_verify
import check_transfer
import compact

HERE=Path(__file__).absolute().parent
need=base_verify.need


def canonical(data):return (json.dumps(data,sort_keys=True,separators=(',',':'))+'\n').encode()


def verify(work):
    work=work.absolute()
    need(work.resolve()!=HERE.resolve() and HERE.resolve() not in work.resolve().parents,'Generated state belongs outside the source directory')
    work.mkdir(parents=True,exist_ok=True)
    manifest=json.loads((HERE/'manifest.json').read_text())
    for item in manifest['inputs']:
        path=HERE/item['file'];need(hashlib.sha256(path.read_bytes()).hexdigest()==item['sha256'],'Exact published input '+item['file'])
    shared=compact.decode(json.loads((HERE/'certificates/shared.json').read_text()))
    exclusion=compact.decode(json.loads((HERE/'certificates/exclusion.json').read_text()))
    raw=canonical(shared);need(hashlib.sha256(raw).hexdigest()==manifest['decoded_shared_sha256'],'Canonical decoded shared proof')
    shared_path=work/'shared-expanded.json';shared_path.write_bytes(raw)
    raw=canonical(exclusion);need(hashlib.sha256(raw).hexdigest()==manifest['decoded_exclusion_sha256'],'Canonical decoded exclusion proof')
    (work/'exclusion-expanded.json').write_bytes(raw)
    base=HERE/'base/phase611.json';packing=HERE/'certificates/packing.json'
    ctx=check_transfer.Context(base,shared_path,packing);out=ctx.check(exclusion)
    need(ctx.phase==611 and ctx.caps==[197,198] and exclusion['root']==-1 and shared['root']==-1,'Precisely the root-free phase611197/198 box')
    need(shared['caps']==[197,None],'Shared premise uses ONLY the original0 cap')
    need(out['excluded'],'An actual checked contradiction, never a solver status')
    need((ctx.S+ctx.D-1)//ctx.D==197,'Checked original packing floor in BOTH reflected classes')
    sizes=[sum(c==k for c in ctx.colors) for k in (0,1)];need(sizes==[1849,1849],'Actual reference class sizes')
    need(all(ctx.colors[3703-x]==(-1 if c<0 else 1-c) for x,c in enumerate(ctx.colors)),'Full actual reference antisymmetry')
    prior=json.loads((HERE/'dependencies/prior_context.json').read_text())['combined_imported_context']
    individual=list(prior['per_phase_lower_bound_each_color']);total=list(prior['per_phase_total_lower_bound'])
    need(len(individual)==len(total)==617 and total[611]==395 and individual[611]==197,'Exact imported prior profile and changed phase')
    need(sum(v>=198 for v in individual)==612,'Imported612 individually strong phases')
    total[611]=396
    weak=[s for s,v in enumerate(total) if v==395]
    need(weak==[184,201,205,269] and sum(v>=396 for v in total)==613,'Exact new combined count')
    result={'agent':'six-vdw-3','role':'researcher','status':'VERIFIED_PHASE611_TOTAL396_BY_RANK2_DEFECT_TRANSFER',
            'phase':611,'key':[611,7,1],'candidate_interval_zero_based':[0,3703],
            'arbitrary_AP_free_candidates':True,'candidate_symmetry_assumed':False,'initial_poles_free':True,'free_poles':6,
            'original_class_sizes':sizes,'individual_lower_bound_each_color':197,'individual_upper_bound_each_color':1652,
            'total_lower_bound':396,'total_upper_bound':3302,'individual198_claimed':False,'attainment_claimed':False,
            'excluded_caps':[197,198],'reflected_excluded_caps':[198,197],
            'base_sha256':ctx.base_sha,'base_denominator':ctx.D,'base_weight_numerator':ctx.S,
            'shared':{'caps':shared['caps'],'fixed_positions':len(ctx.known),'top_rows':len(shared['steps']),
                      'counts':ctx.shared_check['steps_checked'],'decoded_sha256':ctx.shared_sha},
            'packing':ctx.packing_check,
            'exclusion':{k:v for k,v in out.items() if k!='known_candidate_values'},
            'combined_imported_context':{'prior_proofs_replayed_here':False,'individual198_or_stronger_count':612,
                                        'total396_or_stronger_count':613,'remaining_individual197_phases':[184,201,205,269,611],
                                        'remaining_total395_phases':weak,'uniform_total_floor':395,
                                        'total_floor_histogram':{str(k):v for k,v in sorted(Counter(total).items())}},
            'native_solver_trusted':False,'external_independent_review_claimed':False,'proof_assistant_formalization_claimed':False,
            'new_W_bound':False,'length3704_witness':False}
    (work/'result.json').write_bytes(canonical(result));return result


def main():
    p=argparse.ArgumentParser();p.add_argument('--work',type=Path,required=True);a=p.parse_args()
    out=verify(a.work);print(json.dumps(out),flush=True)


if __name__=='__main__':main()
