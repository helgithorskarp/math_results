#!/usr/bin/env python3
"""Mathematical corruption controls for the definition-level checker."""
import argparse
import copy
import json
from pathlib import Path
import tempfile

from check import (C,H,N,ap_points,check_cut,check_family,check_inner_aps,
                   qr,reflect_cut,representatives,require,verify,verify_inner)


def run_controls(work):
    q=qr();key=[0,0,1];data=json.loads((work/'canonical-0.json').read_text());cuts=data['cuts'][:33]
    check_family(cuts,key,q);inner=json.loads((work/'inner.json').read_text())
    first_imp=next(i for i,c in enumerate(cuts) if c['type']=='implication')
    rejected=[]
    def reject(name,call):
        try:call()
        except (ValueError,KeyError,TypeError,IndexError):rejected.append(name)
        else:raise ValueError('corruption was accepted: '+name)
    def family_mutation(name,mutate):
        altered=copy.deepcopy(cuts);mutate(altered);reject(name,lambda:check_family(altered,key,q))
    family_mutation('constant_opposed_AP',lambda cs:cs[0]['record'].__setitem__(1,0))
    family_mutation('opposed_center_outside_bridge',lambda cs:cs[0]['record'].__setitem__(0,0))
    family_mutation('duplicated_protected_support',lambda cs:cs.__setitem__(1,copy.deepcopy(cs[0])))
    family_mutation('wrong_implication_phase',lambda cs:cs[first_imp]['record'].__setitem__('key',[1,1,1]))
    family_mutation('flipped_forced_color',lambda cs:cs[first_imp]['record']['steps'][0].__setitem__(1,cs[first_imp]['record']['steps'][0][1]^1))
    family_mutation('forced_point_out_of_bounds',lambda cs:cs[first_imp]['record']['steps'][0].__setitem__(0,N))
    family_mutation('Boolean_coordinate',lambda cs:cs[first_imp]['record']['steps'][0].__setitem__(0,True))
    family_mutation('floating_coordinate',lambda cs:cs[first_imp]['record']['steps'][0].__setitem__(0,1.0))
    family_mutation('constant_implication_AP',lambda cs:cs[first_imp]['record']['steps'][0].__setitem__(3,0))
    family_mutation('missing_required_implication',lambda cs:cs[first_imp]['record']['steps'].pop(0))
    family_mutation('empty_implication_trace',lambda cs:cs[first_imp]['record'].__setitem__('steps',[]))
    family_mutation('constant_final_AP',lambda cs:cs[first_imp]['record']['final_ap'].__setitem__(1,0))
    family_mutation('final_AP_out_of_bounds',lambda cs:cs[first_imp]['record']['final_ap'].__setitem__(0,N))
    family_mutation('unknown_cut_kind',lambda cs:cs[first_imp].__setitem__('type','unverified_solver_status'))
    reject('compatible_key_outside_claim',lambda:check_family(cuts,[0,0,0],q))
    reject('unequal_phase_key_outside_claim',lambda:check_family(cuts,[0,1,1],q))
    protected=check_cut(cuts[0],key,q)
    reject('duplicate_erasure',lambda:check_cut(cuts[first_imp],key,q,[min(protected)]*2))
    reject('bridge_erasure_is_not_protected',lambda:check_cut(cuts[first_imp],key,q,[C]))
    reject('pole_erasure_is_not_protected',lambda:check_cut(cuts[first_imp],key,q,[1]))
    used=set()
    for cut in cuts[:first_imp]:used.update(check_cut(cut,key,q,used))
    support=check_cut(cuts[first_imp],key,q,used)
    reject('erasing_a_used_proof_root',lambda:check_cut(cuts[first_imp],key,q,used|{min(support)}))
    reflected=[reflect_cut(c,key) for c in cuts];mate=[1,1,1]
    check_family(reflected,mate,q)
    require([reflect_cut(c,mate) for c in reflected]==cuts,'reflection involution')
    bad=copy.deepcopy(reflected);bad[0]['record'][1],bad[0]['record'][2]=bad[0]['record'][2],bad[0]['record'][1]
    reject('reflection_without_color_exchange',lambda:check_family(bad,mate,q))
    row=next(r for r in inner['records'] if r['key']==key);aps=row['aps']
    check_inner_aps(aps,0,q)
    reject('duplicated_inner_AP',lambda:check_inner_aps(aps+[aps[0]],0,q))
    reject('inner_AP_at_pole',lambda:check_inner_aps([[C,1]],0,q))
    reject('constant_inner_AP',lambda:check_inner_aps([[C+1,0]],0,q))
    reject('inner_AP_outside_region',lambda:check_inner_aps([[C-H-1,1]],0,q))
    nonmono=None
    for a in range(C-H,C+H-6):
        points=ap_points(a,1);residues=[(x-C)%617 for x in points]
        if all(residues) and len({q[r]^int(x>=C) for x,r in zip(points,residues)})>1:nonmono=[a,1];break
    require(nonmono is not None,'nonmonochromatic control instance')
    reject('nonmonochromatic_inner_AP',lambda:check_inner_aps([nonmono],0,q))
    with tempfile.TemporaryDirectory(prefix='checker-controls-',dir=work) as name:
        temp=Path(name);domain=temp/'domain';domain.mkdir()
        reject('missing_canonical_domain',lambda:verify(domain,work/'inner.json'))
        for s in representatives():(domain/f'canonical-{s}.json').symlink_to((work/f'canonical-{s}.json').resolve())
        path=domain/'canonical-0.json';path.unlink();bad_data=copy.deepcopy(data);bad_data['cuts']=bad_data['cuts'][:32]
        path.write_text(json.dumps(bad_data));reject('exceptional_phase_missing_33rd_cut',lambda:verify(domain,work/'inner.json'))
        path.write_text(json.dumps({'key':[0,0,1],'cuts':[]}));reject('missing_far_cut_family',lambda:verify(domain,work/'inner.json'))
        (domain/'canonical-617.json').write_text('{}');reject('extra_canonical_phase',lambda:verify(domain,work/'inner.json'))
        inner_path=temp/'inner.json'
        def bad_inner(name,mutate):
            bad=copy.deepcopy(inner);mutate(bad);inner_path.write_text(json.dumps(bad))
            reject(name,lambda:verify_inner(inner_path,q))
        bad_inner('missing_inner_phase',lambda d:d['records'].pop())
        bad_inner('duplicate_inner_phase',lambda d:d['records'].__setitem__(1,copy.deepcopy(d['records'][0])))
        bad_inner('wrong_inner_region',lambda d:d.__setitem__('region',[C-H+1,C+H]))
        def truncate(d,phases,count):
            for r in d['records']:
                if r['key'][0] in phases:r['aps']=r['aps'][:count]
        bad_inner('generic_phase_below_40',lambda d:truncate(d,{2,616},39))
        bad_inner('exceptional_phase_below_38',lambda d:truncate(d,{0,1},37))
    return {'agent':'six-vdw-3','role':'researcher','status':'ALL_CORRUPTION_CONTROLS_REJECTED',
            'rejected_count':len(rejected),'rejected':rejected,'positive_reflection_involution':True}


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--workdir',type=Path,required=True);parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args();r=run_controls(args.workdir.resolve());args.output.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
