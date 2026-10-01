"""Corruption controls and complete tiny models for the proof's logical rules."""
import argparse
import copy
import itertools
import json
from pathlib import Path
import shutil
import time
import verify


def main():
    p=argparse.ArgumentParser();p.add_argument('--work',type=Path,required=True);a=p.parse_args()
    a.work.mkdir(parents=True,exist_ok=True);started=time.monotonic();rejected=[]
    directory=verify.HERE;docs={s:{r:json.loads((directory/f'certificates/phase-{s}-root-{r}.json').read_text())
                              for r in verify.NEW_ROOTS[s]} for s in verify.ANCHORS}
    ctx=verify.premise(205);good=docs[205][19]

    def reject(name,fn):
        try:fn()
        except (ValueError,KeyError,TypeError,FileNotFoundError) as e:
            rejected.append({'name':name,'reason':str(e)[:120]});return
        raise ValueError('Corrupted or incomplete proof accepted: '+name)
    def mutate(name,fn):
        bad=copy.deepcopy(good);fn(bad)
        reject(name,lambda:verify.check_root(bad,ctx))
    mutate('extra_other_class_cap',lambda d:d.update(other_class_cap=197))
    mutate('wrong_single_class',lambda d:d.update(capped_original_class=0))
    mutate('wrong_cap198',lambda d:d.update(capped_class_cap=198))
    mutate('float_cap',lambda d:d.update(capped_class_cap=197.0))
    mutate('boolean_class',lambda d:d.update(capped_original_class=True))
    mutate('wrong_phase',lambda d:d.update(phase=184))
    mutate('nonanchor_root',lambda d:d.update(root=20))
    mutate('float_root',lambda d:d.update(root=19.0))
    mutate('base_hash',lambda d:d.update(base_sha256='0'*64))
    mutate('rigidity_hash',lambda d:d.update(rigidity_sha256='0'*64))
    mutate('zero_denominator',lambda d:d.update(denominator=0))
    mutate('float_denominator',lambda d:d.update(denominator=1000000.0))
    mutate('insufficient_capacity',lambda d:d.update(denominator=1))
    mutate('insufficient_demand',lambda d:d.update(denominator=1000000000))
    mutate('zero_AP_weight',lambda d:d['AP_weights'][0].__setitem__(2,0))
    mutate('negative_AP_weight',lambda d:d['AP_weights'][0].__setitem__(2,-1))
    mutate('boolean_AP_weight',lambda d:d['AP_weights'][0].__setitem__(2,True))
    mutate('point_overload',lambda d:d['AP_weights'][0].__setitem__(2,d['denominator']+1))
    mutate('constant_progression',lambda d:d['AP_weights'][0].__setitem__(1,0))
    mutate('outside_interval',lambda d:d['AP_weights'][0].__setitem__(0,verify.N))
    mutate('float_coordinate',lambda d:d['AP_weights'][0].__setitem__(0,0.0))
    mutate('duplicate_AP',lambda d:d['AP_weights'].append(copy.deepcopy(d['AP_weights'][0])))
    mutate('wrong_original_color',lambda d:d['AP_weights'][0].__setitem__(slice(0,2),[19,438]))
    pole=next(x for x,c in enumerate(ctx['colors']) if c<0 and x+6<verify.N)
    mutate('unknown_pole',lambda d:d['AP_weights'][0].__setitem__(slice(0,2),[pole,1]))
    mutate('remove_essential_triples',lambda d:d.update(triple_weights=[]))
    mutate('empty_all_rows',lambda d:d.update(AP_weights=[],triple_weights=[]))
    mutate('repeated_AP_in_triple',lambda d:d['triple_weights'][0][0].__setitem__(1,copy.deepcopy(d['triple_weights'][0][0][0])))
    mutate('zero_triple_weight',lambda d:d['triple_weights'][0].__setitem__(1,0))
    mutate('duplicate_triple',lambda d:d['triple_weights'].append(copy.deepcopy(d['triple_weights'][0])))
    incidence={}
    for aa,dd,w in good['AP_weights']:
        for x in verify.actual_ap(aa,dd)&ctx['V']:incidence.setdefault(x,[]).append([aa,dd])
    shared=next(aps[:3] for aps in incidence.values() if len(aps)>=3)
    mutate('triple_with_one_point_transversal',lambda d:d['triple_weights'][0].__setitem__(0,shared))
    def equality(d):
        W=sum(w for aa,dd,w in d['AP_weights'])+2*sum(w for aps,w in d['triple_weights'])
        for row in d['AP_weights']:row[2]*=197
        for row in d['triple_weights']:row[1]*=197
        d['denominator']=W
    mutate('zero_gap_is_not_exclusion',equality)
    for s,roots in verify.NEW_ROOTS.items():
        for r in roots:
            bad=copy.deepcopy(docs);del bad[s][r]
            reject(f'omitted_new_root_{s}_{r}',lambda bad=bad:verify.check_complete(directory,bad))
    for s in verify.ANCHORS:
        bad=copy.deepcopy(docs);del bad[s]
        reject(f'omitted_phase_{s}',lambda bad=bad:verify.check_complete(directory,bad))
    temp=a.work/'damaged';shutil.copytree(directory,temp,ignore=shutil.ignore_patterns('__pycache__','*.pyc','.venv','work'),dirs_exist_ok=True)
    original=json.loads((temp/'manifest.json').read_text())
    for name,fn in (
        ('manifest_missing_phase',lambda d:d['phases'].pop()),
        ('manifest_duplicate_phase',lambda d:d['phases'].__setitem__(1,copy.deepcopy(d['phases'][0]))),
        ('manifest_missing_anchor_position',lambda d:d['phases'][0]['new_roots'].pop())):
        bad=copy.deepcopy(original);fn(bad);(temp/'manifest.json').write_text(json.dumps(bad))
        reject(name,lambda:verify.check_complete(temp))
    (temp/'manifest.json').write_text(json.dumps(original))
    damaged=temp/'prior_uniform/covers/phase-184.json';saved=damaged.read_text();cover=json.loads(saved)
    cover['chains'][0]['certificates']=[];damaged.write_text(json.dumps(cover))
    reject('omitted_old_root_chain',lambda:verify.check_complete(temp));damaged.write_text(saved)
    damaged=temp/'prior201/certificates/root2132-02-forbid462-1790.json';saved=damaged.read_text();bad=json.loads(saved)
    bad['domain_sha256']='0'*64;damaged.write_text(json.dumps(bad))
    reject('unproved_old_domain_restriction',lambda:verify.check_complete(temp));damaged.write_text(saved)

    # Direct assignment enumeration is independent of the set-intersection
    # row check and verifies the activation/covering/strict-screen bridges.
    activation=0
    for edits in itertools.product((0,1),repeat=6):
        colors=[1]+[1-b for b in edits]
        if (len(set(colors))!=1)!=(sum(edits)>=1):raise ValueError('Activation truth table')
        activation+=1
    anchor_models=covered_nonempty=0
    for s in verify.ANCHORS:
        checked=verify.premise(s);anchor=sorted(checked['anchor']);roots=set(checked['old_roots'])|verify.NEW_ROOTS[s]
        for bits in itertools.product((0,1),repeat=7):
            E={x for x,b in zip(anchor,bits) if b};anchor_models+=1
            if E:
                if not E&roots:raise ValueError('Incomplete anchor case coverage')
                covered_nonempty+=1
            elif len(set(bits))!=1:raise ValueError('Unchanged original0 AP')
    universe=set(range(4));petals=[{x for x in universe if mask>>x&1} for mask in range(1,16)]
    subsets=[{x for x in universe if mask>>x&1} for mask in range(16)]
    triple_families=hitting_models=defect_models=screen_models=0
    for ps in itertools.combinations(petals,3):
        if set.intersection(*ps):continue
        triple_families+=1;U=set.union(*ps)
        loads={x:sum(x in p for p in ps)+int(x in U) for x in universe};D=max(loads.values());W=5
        for E in subsets:
            if not all(E&p for p in ps):continue
            if len(E&U)<2 or sum(loads[x] for x in E)<W:raise ValueError('Invalid triple demand')
            hitting_models+=1
            for cap in range(len(E),5):
                B=cap*D-W;delta={x:D-loads[x] for x in universe}
                if sum(delta[x] for x in E)>B:raise ValueError('Weighted defect inequality')
                defect_models+=1
                for T in subsets:
                    if not T<=E:continue
                    cost=sum(delta[x] for x in T)
                    for x in E-T:
                        if delta[x]>B-cost:raise ValueError('A valid remaining edit was forbidden by a strict screen')
                        screen_models+=1
    result={'agent':'six-vdw-3','role':'researcher','corruptions_rejected':len(rejected),
            'rejections':rejected,'activation_assignments_checked':activation,
            'anchor_edit_assignments_checked':anchor_models,'nonempty_anchor_subsets_covered':covered_nonempty,
            'empty_intersection_triple_families_checked':triple_families,'weighted_hitting_models':hitting_models,
            'defect_models_checked':defect_models,'strict_remaining_edit_screen_models':screen_models,
            'seconds':time.monotonic()-started,'new_W_bound':False,'external_review_asserted':False}
    (a.work/'controls.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='rejections'}),flush=True)


if __name__=='__main__':main()
