#!/usr/bin/env python3
"""Generate and independently audit all19 new signed words; literal unit controls."""
import argparse
import itertools
import json
import time
from pathlib import Path
import check
import cover_check
import generate

def need(condition,message):
    if not condition:raise ValueError(message)

def audit(cover_path,work,helper_path):
    started=time.monotonic();work.mkdir(parents=True,exist_ok=True)
    coverage=cover_check.verify(cover_path)
    proposed=json.loads(cover_path.read_text());common=check.helper(helper_path)
    records=[];unit_inputs=unit_positives=0
    for entry in proposed['cases']:
        case=entry['number'];path=work/('case-'+str(case)+'.cnf')
        model=generate.generate(103,case,path)
        actual=check.audit(path,103,case,common);actual.pop('seconds',None)
        need(all(actual[k]==v for k,v in model.items()),'Generator/actual-cyclic audit mismatch')
        need(model['fixed_core_bits']==entry['reflected_to_E1_fixed_core_bits'] and
             model['positive_core_units']==entry['opposite_weight'],'Word/count differs from full cover')
        _,core,_,regular,_,index=check.parameters(103,case)
        units=[row for row in common.parse(path,4950) if len(row)==1]
        need(len(units)==11,'Signed unit domain changed')
        wanted=dict(entry['reflected_to_E1_fixed_core_bits'])
        for tail in itertools.product((0,1),repeat=11):
            word=dict(zip(core,(0,)+tail))
            root_pairs={index[(regular[0],x)]:word[x] for x in core if x!=regular[0]}
            encoded=all(root_pairs[abs(row[0])]==int(row[0]>0) for row in units)
            literal=all(word[x]==wanted[x] for x in core)
            need(encoded==literal,'Full signed-word unit interface differs from literal local values')
            unit_inputs+=1;unit_positives+=literal
        records.append({'number':case,'model':model,'audit':actual})
    need(len(records)==19 and unit_inputs==38912 and unit_positives==19,'Incomplete signed-word controls')
    result={'coverage':coverage,'cases':records,'literal_unit_inputs_checked':unit_inputs,
            'positive_literal_unit_words':unit_positives,
            'common_actual_cyclic_pairs_checked':381306,'all_models_free_bits':88,
            'seconds':time.monotonic()-started}
    (work/'family-audit.json').write_text(json.dumps(result,indent=2)+'\n')
    return result

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--cover',type=Path,required=True)
    p.add_argument('--work',type=Path,required=True);p.add_argument('--helper',type=Path,required=True)
    a=p.parse_args();r=audit(a.cover,a.work,a.helper)
    print(json.dumps({k:v for k,v in r.items() if k!='cases'}))
