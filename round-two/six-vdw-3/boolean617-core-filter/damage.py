#!/usr/bin/env python3
"""Reject damaged witnesses, finite domains, affine maps and completion records."""
import argparse
import copy
import importlib.util
import json
from pathlib import Path


def load(name):
    spec=importlib.util.spec_from_file_location('independent_'+name,Path(__file__).with_name(name+'.py'))
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    return module


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--work',type=Path,required=True);parser.add_argument('--mode',choices=('normal','optimized'),required=True);parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args();mode=args.work/args.mode
    core=load('check');roots=load('check_roots');cover_check=load('check_cover');merger=load('merge')
    source=json.loads((mode/'core/t002.json').read_text());unit=json.loads((mode/'roots/roots000-016.json').read_text());cover=json.loads((args.work/'cover.json').read_text())
    transport=json.loads((mode/'cover-check.json').read_text());seed=json.loads((mode/'seed.json').read_text())
    rejected=[]
    def reject(label,callback):
        try:callback()
        except (ValueError,KeyError,TypeError,IndexError):rejected.append(label)
        else:raise ValueError('Damaged record accepted: '+label)
    damages=[]
    x=copy.deepcopy(source);x['histogram'][1]+=1;damages.append(('core-histogram',x))
    x=copy.deepcopy(source);x['transcript_sha256']='0'*64;damages.append(('core-transcript',x))
    x=copy.deepcopy(source);x['blocked_words'].pop();damages.append(('core-missing-truth-rule',x))
    x=copy.deepcopy(source);x['survivor_words'].append(0);damages.append(('core-false-survivor',x))
    x=copy.deepcopy(source);x['witnesses']['0'][1]=0;damages.append(('core-constant-step-witness',x))
    x=copy.deepcopy(source);x['original_roots_all_free']=False;damages.append(('core-original-root-domain',x))
    x=copy.deepcopy(source);x['domain']['pairs']-=1;damages.append(('core-incomplete-AP-domain',x))
    for label,data in damages:reject(label,lambda data=data:core.check(data))
    damages=[]
    x=copy.deepcopy(unit);x['cases'].pop();damages.append(('interval-missing-projection-case',x))
    x=copy.deepcopy(unit);x['third_root_range'][1]-=1;damages.append(('interval-wrong-contiguous-range',x))
    x=copy.deepcopy(unit);x['cases'][0]['certificate']['unit_demands'].pop();damages.append(('interval-missing-vertical-unit',x))
    x=copy.deepcopy(unit);x['cases'][0]['certificate']['forced_color']^=1;damages.append(('interval-wrong-forced-color',x))
    x=copy.deepcopy(unit);x['cases'][0]['certificate']['unit_demands'][0][2]=0;damages.append(('interval-constant-step',x))
    x=copy.deepcopy(unit);x['cases'][0]['certificate']['unit_demands'][0][1]=0;damages.append(('interval-outside-endpoint',x))
    x=copy.deepcopy(unit);x['cases'][0]['certificate']['column']=1;damages.append(('interval-projected-free-root-target',x))
    x=copy.deepcopy(unit);x['cases'][0]['status']='UNIT_MECHANISM_INCOMPLETE_NO_EXCLUSION';damages.append(('interval-incomplete-status',x))
    for label,data in damages:reject(label,lambda data=data:roots.verify(data))
    damages=[]
    x=copy.deepcopy(cover);x['maps'].pop();damages.append(('cover-missing-original-geometry',x))
    x=copy.deepcopy(cover);x['maps'][0]['representative']=3;damages.append(('cover-wrong-BFS-component',x))
    x=copy.deepcopy(cover);x['maps'][0]['inverse_map_scale']=0;damages.append(('cover-zero-affine-scale',x))
    for label,data in damages:reject(label,lambda data=data:cover_check.verify(data,mode/'core'))
    bad=copy.deepcopy(cover);bad['geometries'].pop()
    reject('merge-missing-canonical-geometry',lambda:merger.merge(bad,mode/'core',mode/'roots',seed,transport))
    bad=copy.deepcopy(transport);bad['raw_states_with_literal_positive_witness']-=1
    reject('merge-incomplete-raw-truth-domain',lambda:merger.merge(cover,mode/'core',mode/'roots',seed,bad))
    bad=copy.deepcopy(transport);bad['status']='UNKNOWN'
    reject('merge-UNKNOWN-status',lambda:merger.merge(cover,mode/'core',mode/'roots',seed,bad))
    bad=copy.deepcopy(seed);bad['ordinary_nonconstant_seven_term_APs_checked']-=1
    reject('merge-incomplete-known-seed-domain',lambda:merger.merge(cover,mode/'core',mode/'roots',bad,transport))
    if len(rejected)!=22:raise ValueError('Incomplete damage inventory')
    result={'schema':'boolean617-damage-check-v1','status':'ALL_DAMAGES_REJECTED','rejected_count':len(rejected),'rejected':rejected}
    args.output.write_text(json.dumps(result,sort_keys=True,indent=2)+'\n')
    print(json.dumps(result))


if __name__=='__main__':main()
