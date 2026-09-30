"""Corruption checks and exhaustive small removed-edit logical models."""
import copy
import itertools
import json
from pathlib import Path
import sys
import verify

HERE=Path(__file__).parent


def main():
    colors,V,K,_=verify.premise()
    tree=json.loads((HERE/'tree.json').read_text())
    baseline=verify.check_tree(tree,colors,V,K)
    changes=[]
    def tree_change(name,fn):
        d=copy.deepcopy(tree);fn(d);changes.append((name,d))
    def leaf_change(name,fn):
        tree_change(name,lambda d:fn(d['tree']['unchanged']['leaf']))
    tree_change('missing_edited_child',lambda d:d['tree'].pop('edited'))
    tree_change('missing_unchanged_child',lambda d:d['tree'].pop('unchanged'))
    tree_change('hidden_initial_edit',lambda d:d.update(initial_forced=[2065]))
    tree_change('zero_load_split',lambda d:d['tree'].update(split=next(iter(K[0]))))
    tree_change('boolean_split',lambda d:d['tree'].update(split=True))
    tree_change('wrong_tree_phase',lambda d:d.update(phase=269))
    tree_change('wrong_tree_cap',lambda d:d.update(class_cap=197))
    tree_change('wrong_tree_dependency',lambda d:d.update(base_certificate_sha256='0'*64))
    leaf_change('wrong_leaf_phase',lambda d:d.update(phase=269))
    leaf_change('wrong_leaf_cap',lambda d:d.update(class_cap=197))
    leaf_change('boolean_leaf_cap',lambda d:d.update(class_cap=True))
    leaf_change('wrong_leaf_dependency',lambda d:d.update(base_certificate_sha256='0'*64))
    leaf_change('missing_APs',lambda d:d.pop('color0_APs'))
    leaf_change('hidden_leaf_states',lambda d:d.update(forced=[2065]))
    leaf_change('zero_denominator',lambda d:d.update(denominator=0))
    leaf_change('boolean_denominator',lambda d:d.update(denominator=True))
    leaf_change('capacity_exceeded',lambda d:d.update(denominator=1))
    leaf_change('no_strict_gap',lambda d:d.update(denominator=2_000_000))
    leaf_change('zero_AP_step',lambda d:d['color0_APs'][0].__setitem__(1,0))
    leaf_change('out_of_bounds_AP',lambda d:d['color0_APs'][0].__setitem__(0,3704))
    leaf_change('wrong_color_AP',lambda d:d['color0_APs'].__setitem__(0,[0,1,1]))
    leaf_change('zero_AP_weight',lambda d:d['color0_APs'][0].__setitem__(2,0))
    leaf_change('boolean_AP_weight',lambda d:d['color0_APs'][0].__setitem__(2,True))
    leaf_change('negative_AP_weight',lambda d:d['color0_APs'][0].__setitem__(2,-1))
    leaf_change('duplicate_AP',lambda d:d['color0_APs'].append(d['color0_APs'][0][:]))
    leaf_change('zero_triple_weight',lambda d:d['color0_cover2'][0].__setitem__(1,0))
    leaf_change('repeated_triple_AP',lambda d:d['color0_cover2'][0][0].__setitem__(1,d['color0_cover2'][0][0][0][:]))
    leaf_change('duplicate_triple',lambda d:d['color0_cover2'].append(copy.deepcopy(d['color0_cover2'][0])))
    leaf_change('surcharge_outside_free_screen',lambda d:d['color0_surcharges'].append([2065,1]))
    leaf_change('negative_surcharge',lambda d:d['color0_surcharges'].append([next(iter(V[0]-{2065})),-1]))
    leaf_change('empty_packing',lambda d:d.update(color0_APs=[],color0_cover2=[],color0_surcharges=[]))
    incidence={}
    for a,d,w in tree['tree']['unchanged']['leaf']['color0_APs']:
        for x in {a+j*d for j in range(7)}&V[0]:incidence.setdefault(x,[]).append([a,d])
    common=next(es[:3] for es in incidence.values() if len(es)>=3)
    leaf_change('triple_with_screened_common_point',lambda d:d['color0_cover2'][0].__setitem__(0,common))
    rejected=[]
    for name,data in changes:
        try:verify.check_tree(data,colors,V,K)
        except (ValueError,KeyError,TypeError):rejected.append(name)
        else:raise ValueError('Accepted corrupted complete zero tree: '+name)
    # Six possible nonzero membership types in three petals whose common
    # intersection is empty. A removed z may have any of the eight types.
    memberships=[(1,0,0),(0,1,0),(0,0,1),(1,1,0),(1,0,1),(0,1,1)]
    cases=valid=0
    for z in itertools.product((0,1),repeat=3):
        ell=2 if all(z) else int(any(z))
        for states in itertools.product((0,1,2),repeat=6):
            cases+=1
            T={i for i,s in enumerate(states) if s==1}
            J={i for i,s in enumerate(states) if s==2}
            if not all(z[k] or any(memberships[i][k] for i in T|J) for k in range(3)):continue
            valid+=1
            b=max(0,2-len(T))
            verify.need(len(J)>=b-min(b,ell),'Removed-edit triple residual lower bound')
    verify.need(verify.check_tree(tree,colors,V,K)==baseline,'Controls changed frozen inputs')
    print(json.dumps({'agent':'six-vdw-3','role':'researcher','all_rejected':True,
                      'rejected_controls':len(rejected),'names':rejected,'python_optimization':sys.flags.optimize,
                      'removed_triple_model_cases':cases,'AP_hit_model_cases':valid}))


if __name__=='__main__':main()
