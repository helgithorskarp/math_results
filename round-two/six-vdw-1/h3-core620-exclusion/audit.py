"""Independent whole physical AP definition and every original row-cut truth."""
import argparse
import importlib.util
import json
from math import gcd
from pathlib import Path

spec=importlib.util.spec_from_file_location('pinned_support',Path(__file__).resolve().parent/'support.py')
support=importlib.util.module_from_spec(spec);spec.loader.exec_module(support)


def audit(d,rep):
    require=support.require
    require(type(d) is dict and set(d)=={'author','role','model_kind','base_model','cut_premise','forbidden_masks','necessary_cut_clauses','variables','clauses','scope'},'whole new cut model schema')
    require((d['author'],d['role'],d['model_kind'])==('six-vdw-1','researcher','six_remaining_H3_with_proved_orbit16_cuts'),'actual new domain')
    require(type(d['forbidden_masks']) is list and all(type(m) is int for m in d['forbidden_masks']),'exact forbidden mask types')
    for key in ['necessary_cut_clauses','clauses']:
        require(type(d[key]) is list and all(type(c) is list and c and all(type(v) is int and 0<abs(v)<=100 for v in c) for c in d[key]),'exact new literal types/domains '+key)
    require(len(d['necessary_cut_clauses'])==1600 and all(len(c)==10 for c in d['necessary_cut_clauses']),'necessary rowcut dimensions')
    require(rep in support.REPS and d['cut_premise']==support.PREMISE,'actual proved rowcut premise and requested case')
    base=d['base_model']
    require((base['field_prime'],base['row_half'],base['AP_length'],base['subgroup'],base['fixed_first_coset_row'],base['palette'],base['variables'])==(31,10,7,[1,5,25],rep,False,100),'NEW absolute first-row guard; no old16 target')
    physical=support.load('check_model').audit(base,target=False)
    units=[v for v in range(20) if gcd(v,20)==1]
    word=[((16//2**(s%10))%2+s//10)%2 for s in range(20)]
    masks=sorted({sum(word[(z+v*s)%20]*2**s for s in range(10)) for z in range(20) for v in units})
    require(len(masks)==160 and d['forbidden_masks']==masks,'entire independently computed proved phase orbit')
    expected=[];truths=0
    for g in range(10):
        for m in masks:
            clause=[]
            for j in range(10):clause.append((10*g+j+1)*(-1 if(m//2**j)%2 else 1))
            for original in range(1024):
                encoded=any(((original//2**j)%2)==int(v>0) for j,v in enumerate(clause))
                require(encoded==(original!=m),'ALL original raw phase-mask exclusion truths');truths+=1
            expected.append(clause)
    require(d['necessary_cut_clauses']==expected and len(expected)==1600,'whole actual rowcut inventory/order')
    clauses=[list(c) for c in sorted({tuple(c) for c in base['clauses']+expected})]
    require(d['variables']==100 and type(d['variables']) is int and d['clauses']==clauses,'ENTIRE new original AP/unit/necessary-cut clause set')
    require(d['scope']=='Chosen H3 regular620; first literal row in complete remaining six-class cover; orbit16 bans follow ACTUAL9576. No other class cut/palette/row law/pole assignment.','honest chosen construction/cut scope')
    return {'author':'six-vdw-1','role':'researcher','status':'COMPLETE_INDEPENDENT_H3_REMAINING_MODEL_AUDIT',
            'first_literal_row':rep,'variables':100,'clauses':len(clauses),'necessary_cut_clauses':1600,
            'original_row_cut_truths':truths,'full_physical_definition':physical,'cut_premise':support.PREMISE,
            'scope':'Whole original physical/CNF definition, conditional on ACTUAL9576 rowban; no new core/exclusion/W bound.'}


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('model',type=Path);p.add_argument('rep',type=int);a=p.parse_args()
    d=json.loads(a.model.read_text());r=audit(d,a.rep)
    raw=('p cnf 100 '+str(len(d['clauses']))+'\n'+''.join(' '.join(map(str,c))+' 0\n' for c in d['clauses'])).encode()
    support.require(a.model.with_suffix('.cnf').read_bytes()==raw,'whole new DIMACS bytes')
    print(json.dumps(r,sort_keys=True),flush=True)
