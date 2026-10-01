"""Meaningful certificate corruption controls and defining local model audits."""
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
    a.work.mkdir(parents=True,exist_ok=True);start=time.monotonic();rejections=[];ctx=verify.context()
    docs={r:json.loads((verify.HERE/f'certificates/root-{r}.json').read_text()) for r in verify.NEW_ROOTS};good=docs[605]
    def reject(name,fn):
        try:fn()
        except (ValueError,TypeError,KeyError,FileNotFoundError) as e:
            rejections.append({'name':name,'reason':str(e)[:120]});return
        raise ValueError('Invalid proof accepted: '+name)
    def mutate(name,fn):
        bad=copy.deepcopy(good);fn(bad);reject(name,lambda:verify.check_new_root(bad,ctx))
    mutate('extra_other_class_cap',lambda d:d.update(other_class_cap=197))
    mutate('hidden_partial_domain',lambda d:d.update(permitted_domain=[]))
    mutate('wrong_cap198',lambda d:d.update(capped_class_cap=198))
    mutate('float_cap',lambda d:d.update(capped_class_cap=197.0))
    mutate('wrong_capped_class',lambda d:d.update(capped_original_class=0))
    mutate('boolean_capped_class',lambda d:d.update(capped_original_class=True))
    mutate('wrong_phase',lambda d:d.update(phase=205))
    mutate('float_phase',lambda d:d.update(phase=611.0))
    mutate('nonanchor_root',lambda d:d.update(root=604))
    mutate('float_root',lambda d:d.update(root=605.0))
    mutate('wrong_base_hash',lambda d:d.update(base_sha256='0'*64))
    mutate('zero_denominator',lambda d:d.update(denominator=0))
    mutate('float_denominator',lambda d:d.update(denominator=1000000.0))
    mutate('insufficient_capacity',lambda d:d.update(denominator=1))
    mutate('insufficient_demand',lambda d:d.update(denominator=1000000000))
    mutate('empty_weights',lambda d:d.update(AP_weights=[]))
    mutate('zero_weight',lambda d:d['AP_weights'][0].__setitem__(2,0))
    mutate('negative_weight',lambda d:d['AP_weights'][0].__setitem__(2,-1))
    mutate('boolean_weight',lambda d:d['AP_weights'][0].__setitem__(2,True))
    mutate('float_weight',lambda d:d['AP_weights'][0].__setitem__(2,1.0))
    mutate('point_overload',lambda d:d['AP_weights'][0].__setitem__(2,d['denominator']+1))
    mutate('constant_AP',lambda d:d['AP_weights'][0].__setitem__(1,0))
    mutate('outside_interval',lambda d:d['AP_weights'][0].__setitem__(0,verify.N))
    mutate('float_coordinate',lambda d:d['AP_weights'][0].__setitem__(0,0.0))
    mutate('duplicate_AP',lambda d:d['AP_weights'].append(copy.deepcopy(d['AP_weights'][0])))
    mutate('wrong_reference_colour',lambda d:d['AP_weights'][0].__setitem__(slice(0,2),[45,560]))
    pole=next(x for x,c in enumerate(ctx['colors']) if c<0 and x+6<verify.N)
    mutate('unknown_pole',lambda d:d['AP_weights'][0].__setitem__(slice(0,2),[pole,1]))
    def equality(d):
        W=sum(w for aa,dd,w in d['AP_weights'])
        for row in d['AP_weights']:row[2]*=197
        d['denominator']=W
    mutate('zero_gap_is_not_exclusion',equality)
    for root in verify.NEW_ROOTS:
        bad=copy.deepcopy(docs);del bad[root]
        reject(f'omitted_new_root_{root}',lambda bad=bad:verify.check_complete(verify.HERE,bad))
    temp=a.work/'damaged';shutil.copytree(verify.HERE,temp,ignore=shutil.ignore_patterns('__pycache__','*.pyc','.venv','work'),dirs_exist_ok=True)
    path=temp/'manifest.json';original=path.read_text();manifest=json.loads(original)
    for name,fn in (
        ('manifest_other_cap',lambda d:d.update(other_class_cap=197)),
        ('manifest_missing_new_root',lambda d:d['new_roots'].pop()),
        ('manifest_missing_old_root',lambda d:d['old_roots'].pop()),
        ('manifest_wrong_anchor',lambda d:d.update(anchor=[45,561])),
        ('manifest_boolean_class',lambda d:d.update(capped_original_class=True))):
        bad=copy.deepcopy(manifest);fn(bad);path.write_text(json.dumps(bad));reject(name,lambda:verify.check_complete(temp))
    path.write_text(original)
    path=temp/'prior/covers/phase-611.json';original=path.read_text();cover=json.loads(original)
    for root in verify.OLD_ROOTS:
        bad=copy.deepcopy(cover);bad['chains']=[x for x in bad['chains'] if x['root']!=root]
        path.write_text(json.dumps(bad));reject(f'omitted_old_root_{root}',lambda:verify.check_complete(temp))
    bad=copy.deepcopy(cover);next(x for x in bad['chains'] if x['root']==1725)['certificates'].pop(0)
    path.write_text(json.dumps(bad));reject('old_chain_missing_domain_stage',lambda:verify.check_complete(temp));path.write_text(original)
    path=temp/'prior/certificates/phase-611-root1725-03-after1854.json';original=path.read_text();bad=json.loads(original)
    bad['domain_sha256']='0'*64;path.write_text(json.dumps(bad));reject('unproved_old_domain_restriction',lambda:verify.check_complete(temp));path.write_text(original)
    path=temp/'imported_profile.json';original=path.read_bytes();bad=json.loads(original)
    bad['combined_profile']['remaining_individual197_phases']=[];path.write_text(json.dumps(bad))
    reject('unproved_imported_profile',lambda:verify.check_complete(temp));path.write_bytes(original)

    activation=anchor_models=nonempty=0
    for bits in itertools.product((0,1),repeat=6):
        final=[1]+[1-b for b in bits]
        if (len(set(final))!=1)!=(sum(bits)>=1):raise ValueError('Actual activation truth table')
        activation+=1
    roots=verify.OLD_ROOTS|verify.NEW_ROOTS;anchor=sorted(ctx['anchor'])
    for bits in itertools.product((0,1),repeat=7):
        E={x for x,b in zip(anchor,bits) if b};anchor_models+=1
        if E:
            if not E&roots:raise ValueError('Incomplete anchor cover')
            nonempty+=1
    U=set(range(4));petals=[{x for x in U if mask>>x&1} for mask in range(1,16)];subsets=[{x for x in U if mask>>x&1} for mask in range(16)]
    families=hitting=defects=screens=0
    for ps in itertools.combinations(petals,3):
        if set.intersection(*ps):continue
        families+=1;union=set.union(*ps);loads={x:sum(x in p for p in ps)+int(x in union) for x in U};D=max(loads.values());W=5
        for E in subsets:
            if not all(E&p for p in ps):continue
            if len(E&union)<2 or sum(loads[x] for x in E)<W:raise ValueError('Historical triple demand')
            hitting+=1
            for cap in range(len(E),5):
                B=cap*D-W;delta={x:D-loads[x] for x in U}
                if sum(delta[x] for x in E)>B:raise ValueError('Nonnegative defect budget')
                defects+=1
                for T in subsets:
                    if not T<=E:continue
                    cost=sum(delta[x] for x in T)
                    for x in E-T:
                        if delta[x]>B-cost:raise ValueError('Strict remaining-edit screen')
                        screens+=1
    result={'agent':'six-vdw-3','role':'researcher','corruptions_rejected':len(rejections),'rejections':rejections,
            'activation_assignments':activation,'anchor_assignments':anchor_models,'nonempty_anchor_subsets':nonempty,
            'empty_intersection_triple_families':families,'weighted_hitting_models':hitting,'defect_models':defects,
            'strict_remaining_edit_screen_models':screens,'seconds':time.monotonic()-start,'new_W_bound':False,'external_review_asserted':False}
    (a.work/'controls.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='rejections'}),flush=True)

if __name__=='__main__':main()
