"""Six complete remaining first-row models, with proved orbit16 cuts only."""
import argparse
import importlib.util
import json
from math import gcd
from pathlib import Path

spec=importlib.util.spec_from_file_location('pinned_support',Path(__file__).resolve().parent/'support.py')
support=importlib.util.module_from_spec(spec);spec.loader.exec_module(support)


def forbidden():
    def bit(s):return((16>>(s%10))&1)^(s//10)
    return sorted({sum(bit((v*j+z)%20)<<j for j in range(10)) for v in range(20) if gcd(v,20)==1 for z in range(20)})


def build(rep):
    support.require(rep in support.REPS,'complete remaining six-row domain')
    base=support.load('model').build(31,10,7,[1,5,25],rep)
    masks=forbidden();support.require(len(masks)==160,'proved forbidden orbit size')
    cuts=[[ -(10*g+j+1) if(m>>j)&1 else 10*g+j+1 for j in range(10)] for g in range(10) for m in masks]
    clauses=sorted({tuple(c) for c in base['clauses']+cuts})
    return {'author':'six-vdw-1','role':'researcher','model_kind':'six_remaining_H3_with_proved_orbit16_cuts',
            'base_model':base,'cut_premise':support.PREMISE,'forbidden_masks':masks,
            'necessary_cut_clauses':cuts,'variables':100,'clauses':[list(c) for c in clauses],
            'scope':'Chosen H3 regular620; first literal row in complete remaining six-class cover; orbit16 bans follow ACTUAL9576. No other class cut/palette/row law/pole assignment.'}


def write(d,out):
    support.require(not out.exists() and not out.with_suffix('.cnf').exists(),'fresh model paths')
    out.write_text(json.dumps(d,sort_keys=True)+'\n')
    out.with_suffix('.cnf').write_text('p cnf 100 '+str(len(d['clauses']))+'\n'+''.join(' '.join(map(str,c))+' 0\n' for c in d['clauses']))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('work',type=Path);a=p.parse_args()
    support.require(not a.work.exists(),'fresh six-case model directory');a.work.mkdir()
    records=[]
    for rep in support.REPS:
        d=build(rep);out=a.work/('row'+str(rep)+'.json');write(d,out)
        records.append({'first_literal_row':rep,'variables':100,'clauses':len(d['clauses']),
                        'AP_clauses':d['base_model']['distinct_AP_clauses'],'first_units':d['base_model']['fixed_row_clauses'],
                        'necessary_cuts':len(d['necessary_cut_clauses']),'free_original_inputs_before_AP_cuts':90})
    print(json.dumps({'author':'six-vdw-1','role':'researcher','status':'GENERATED_COMPLETE_SIX_H3_REMAINING_MODELS',
                      'cut_premise':support.PREMISE,'cases':records,'scope':'Untrusted definitions only; no witness/refutation/W bound.'},sort_keys=True),flush=True)
