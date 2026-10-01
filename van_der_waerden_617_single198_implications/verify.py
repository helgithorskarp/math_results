"""Replay ten new phase bounds; distinguish imported global context."""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import base_verify
import check_core
import check_probe
import compact

HERE=Path(__file__).absolute().parent
need=base_verify.need
PHASES=[156,170,174,198,213,220,235,252,287,560]


def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()


def case(base,proof,kind):
    colors,_,b=base_verify.base_premise(base);raw=json.loads(base.read_text());N=3704;D=raw['denominator'];S=b['base_weight_numerator']
    L=[0]*N
    for a,d,w in raw['color0_APs']:
        for aa in [a,N-1-a-6*d]:
            for x in base_verify.actual_ap(aa,d):L[x]+=w
    data=json.loads(proof.read_text())
    if kind=='forcing_core':
        checked=check_core.check(data)
        need(data['N']==N and data['color']==0 and all(colors[x]==0 for x in data['seed']),'Entire forcing set lies in actual original class0')
        minimum=min(D-L[x] for x in data['seed'])
        need(S+minimum>197*D,'Strict forcing-set defect transfer to the198 integer floor')
        details={**checked,'minimum_seed_defect_numerator':minimum,'packing_plus_core_numerator':S+minimum,
                 'strict_gap_to197_numerator':S+minimum-197*D}
    elif kind=='scoped_units':
        trace=compact.decode(data)
        need(trace['caps']==[197,None] and trace['root']==-1,'The other original class is UNCAPPED; no root or candidate symmetry assumption')
        checked=check_probe.check(base,trace)
        need(checked['excluded'],'Every included phase requires a completed exact contradiction')
        details={k:checked[k] for k in ['initial_fixed_positions','steps_checked','terminal','forced_original_class_edits','consumed_base_defects','forced_poles']}
    else:raise ValueError('Unknown proof mechanism')
    need(b['original_class_sizes']==[1849,1849] and b['free_poles']==6,'These ten actual reference sizes')
    return {'phase':b['phase'],'key':b['key'],'proof_kind':kind,'base_certificate_sha256':sha(base),'proof_sha256':sha(proof),
            'base_denominator':D,'base_weight_numerator':S,'checked_base_actual_APs':b['checked_base_actual_APs'],
            'original_class_sizes':b['original_class_sizes'],'free_poles':b['free_poles'],'proved_individual_floor':198,
            'individual_upper_bound':1651,'total_lower_bound':396,'total_upper_bound':3302,'details':details}


def all_cases(directory=HERE):
    manifest=json.loads((directory/'manifest.json').read_text())
    need(manifest['phases']==PHASES and [r['phase'] for r in manifest['cases']]==PHASES,'Exactly ten new phases, each once')
    out=[]
    for row in manifest['cases']:
        base=directory/row['base'];proof=directory/row['proof']
        need(sha(base)==row['base_sha256'] and sha(proof)==row['proof_sha256'],'Actual frozen base and compact proof bytes')
        checked=case(base,proof,row['kind']);need(checked['phase']==row['phase'],'Actual phase matches manifest');out.append(checked)
    # Explicit mathematical imports. Byte identity and this bridge do not replay
    # the602 original weighted proofs or the prior uniform395 proof.
    for dep in manifest['dependencies']:
        need(sha(directory/dep['file'])==dep['sha256'],'Pinned unchanged prior summary')
    profile=json.loads((directory/'dependencies/base_profile.json').read_text())
    prior=json.loads((directory/'dependencies/uniform395.json').read_text())['uniform']
    floors=profile['per_phase_lower_bound_each_color']
    need(type(floors) is list and len(floors)==617 and all(type(k) is int for k in floors),'Imported complete617 profile')
    strong=[s for s,k in enumerate(floors) if k>=198]
    weak=[s for s,k in enumerate(floors) if k<198]
    need(len(strong)==602 and weak==[156,170,174,184,198,201,205,213,220,235,252,269,287,560,611],'Imported exact weak-phase set')
    need(prior['minimum_total_nonpole_edits']==395 and prior['necessary_max_original_class_edits']==198,'Imported uniform395/max198 conclusion')
    need(not(set(PHASES)&set(strong)),'The ten new floors add ten distinct phases')
    per_class=[max(197,k,198 if s in PHASES else 0) for s,k in enumerate(floors)]
    totals=[max(395,2*k) for k in per_class]
    remaining=[s for s,k in enumerate(per_class) if k<198]
    need(remaining==[184,201,205,269,611] and sum(k>=198 for k in per_class)==612,'Exact combined612+5 coverage')
    return {'agent':'six-vdw-3','role':'researcher','status':'VERIFIED_TEN_SINGLE_CLASS198_IMPLICATION_BOUNDS','new_cases':out,
            'combined_imported_context':{'prior_strong_phases':602,'new_individual198_phases':PHASES,'individual198_or_stronger_count':612,
            'remaining_individual197_phases':remaining,'remaining_total395_phases':remaining,'total_floor_histogram':{str(k):v for k,v in sorted(Counter(totals).items())},
            'per_phase_lower_bound_each_color':per_class,'per_phase_total_lower_bound':totals,
            'prior_proofs_replayed_here':False,'imported_mathematical_results':['base_profile','uniform395']},
            'candidate_symmetry_assumed':False,'other_class_uncapped_in_all_new_proofs':True,'poles_initially_free':True,
            'attainment_claimed':False,'new_W_bound':False,'unrestricted_nonexistence_claimed':False,'solver_trusted':False,
            'external_independent_review_claimed':False,'proof_assistant_formalization_claimed':False}


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--directory',type=Path,default=HERE);p.add_argument('--output',type=Path);a=p.parse_args()
    out=all_cases(a.directory);encoded=json.dumps(out,sort_keys=True,separators=(',',':'))+'\n'
    if a.output:a.output.write_text(encoded)
    else:print(encoded,end='')
