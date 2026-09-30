"""Root-screen corruption checks and exact small logical controls."""
import copy
import itertools
import json
from pathlib import Path
import sys
import verify

HERE=Path(__file__).parent


def main():
    colors,K,_=verify.premise()
    doc=json.loads((HERE/'root1427.json').read_text())
    baseline=verify.check_screen(doc,colors,K)
    changes=[]
    def add(name,fn):
        d=copy.deepcopy(doc);fn(d);changes.append((name,d))
    add('missing_cap',lambda d:d.pop('opposite_class_cap'))
    add('boolean_cap',lambda d:d.update(opposite_class_cap=True))
    add('wrong_cap',lambda d:d.update(opposite_class_cap=198))
    add('wrong_phase',lambda d:d.update(phase=269))
    add('boolean_root',lambda d:d.update(root=True))
    add('wrong_root',lambda d:d.update(root=1662))
    add('wrong_zero_dependency',lambda d:d.update(zero_tree_sha256='0'*64))
    add('hidden_other_edit',lambda d:d.update(initial_edits=[1662]))
    add('hidden_restricted_screen',lambda d:d.update(permitted_vertices=[1]))
    add('zero_denominator',lambda d:d.update(denominator=0))
    add('boolean_denominator',lambda d:d.update(denominator=True))
    add('capacity_overflow',lambda d:d.update(denominator=1))
    add('no_nontrivial_screen',lambda d:d.update(denominator=2_000_000))
    add('unsupported_claim_of_exclusion',lambda d:d.update(denominator=999000))
    add('zero_AP_step',lambda d:d['AP_weights'][0].__setitem__(1,0))
    add('out_of_bounds_AP',lambda d:d['AP_weights'][0].__setitem__(0,3704))
    add('wrong_color_AP',lambda d:d['AP_weights'].__setitem__(0,[0,1,1]))
    add('zero_AP_weight',lambda d:d['AP_weights'][0].__setitem__(2,0))
    add('boolean_AP_weight',lambda d:d['AP_weights'][0].__setitem__(2,True))
    add('negative_AP_weight',lambda d:d['AP_weights'][0].__setitem__(2,-1))
    add('duplicate_AP',lambda d:d['AP_weights'].append(d['AP_weights'][0][:]))
    add('zero_triple_weight',lambda d:d['cover2_weights'][0].__setitem__(1,0))
    add('repeated_triple_AP',lambda d:d['cover2_weights'][0][0].__setitem__(1,d['cover2_weights'][0][0][0][:]))
    add('duplicate_triple',lambda d:d['cover2_weights'].append(copy.deepcopy(d['cover2_weights'][0])))
    add('empty_packing',lambda d:d.update(AP_weights=[],cover2_weights=[]))
    incidence={}
    for a,s,w in doc['AP_weights']:
        A={a+j*s for j in range(7)}
        if not all(colors[x]==1 for x in A):continue
        for x in A-K[1]:incidence.setdefault(x,[]).append([a,s])
    common=next(es[:3] for es in incidence.values() if len(es)>=3)
    add('triple_with_permitted_common_point',lambda d:d['cover2_weights'][0].__setitem__(0,common))
    rejected=[]
    for name,d in changes:
        try:verify.check_screen(d,colors,K)
        except (ValueError,KeyError,TypeError):rejected.append(name)
        else:raise ValueError('Accepted corrupted root screen: '+name)
    activated=0
    for flips in itertools.product((0,1),repeat=6):
        actual=[1]+[1-e for e in flips]
        verify.need((not all(c==actual[0] for c in actual))==any(flips),'Activated AP truth table')
        activated+=1
    capacity_cases=valid_cases=0
    for ls in itertools.product(range(5),repeat=3):
        for W in range(1,9):
            delta=8-W
            for bits in itertools.product((0,1),repeat=3):
                E={i for i,b in enumerate(bits) if b}
                if len(E)>2:continue
                capacity_cases+=1
                if sum(ls[i] for i in E)<W:continue
                valid_cases+=1
                verify.need(all(4-ls[i]<=delta for i in E),'Nonnegative-defect screen bridge')
    verify.need(verify.check_screen(doc,colors,K)==baseline,'Controls changed frozen inputs')
    print(json.dumps({'agent':'six-vdw-3','role':'researcher','all_rejected':True,
                      'rejected_controls':len(rejected),'names':rejected,'python_optimization':sys.flags.optimize,
                      'activated_truth_table_cases':activated,'small_defect_models':capacity_cases,
                      'small_defect_models_meeting_lower_bound':valid_cases}))


if __name__=='__main__':main()
