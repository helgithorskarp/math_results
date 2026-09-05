#!/usr/bin/env python3
"""Reject malformed new lemma applications and local limitation fixtures."""
from pathlib import Path
import argparse
import copy
import json
import check_lemma


def run(source, work):
    work.mkdir(parents=True,exist_ok=True)
    original={name:json.loads((source/name).read_text()) for name in ('classification.json','fixtures.json')}
    mutations={}
    x=copy.deepcopy(original);x['classification.json']['rows'].pop();mutations['missing_core']=x
    x=copy.deepcopy(original);x['classification.json']['rows'][0]['blue_triangles'].pop();mutations['missing_witness']=x
    x=copy.deepcopy(original);x['classification.json']['rows'][0]['blue_triangles'][0]=[0,1,2];mutations['red_triangle_as_blue']=x
    x=copy.deepcopy(original);x['classification.json']['rows'][0]['blue_triangles'][0]=[0,3,6];mutations['wrong_omitted_triangle']=x
    x=copy.deepcopy(original);x['classification.json']['selected_labeled']+=1;mutations['wrong_multiplicity']=x
    x=copy.deepcopy(original);x['fixtures.json']['local_zero_empty']['signatures'][0]=0;mutations['changed_uniform_signature']=x
    x=copy.deepcopy(original);x['fixtures.json']['repeated_singleton']['signatures']=[1,2];mutations['lost_repeat_control']=x
    rejected=[]
    for name,data in mutations.items():
        target=work/name;target.mkdir(exist_ok=True)
        for file,obj in data.items():(target/file).write_text(json.dumps(obj))
        try:
            check_lemma.check(target)
        except ValueError:
            rejected.append(name)
        else:
            raise ValueError('malformed input accepted '+name)
    return dict(verified=True,rejected=rejected)


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);p.add_argument('--work',type=Path,required=True)
    a=p.parse_args();r=run(a.source,a.work);(a.work/'controls.json').write_text(json.dumps(r,sort_keys=True,indent=2)+'\n');print(json.dumps(r,sort_keys=True))
