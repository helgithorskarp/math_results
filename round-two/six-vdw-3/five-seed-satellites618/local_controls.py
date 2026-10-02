#!/usr/bin/env python3
"""Coverage/polynomial damage guards with the separate literal checker."""
import argparse
import copy
import json
import tempfile
from pathlib import Path
from check_local import check, need

def controls(path):
    original=json.loads(path.read_text());positive=check(path);need(positive['local_accepted']>0,'Local controls vacuous')
    damaged=[]
    one=copy.deepcopy(original);one['profiles'].pop();damaged.append(one)
    one=copy.deepcopy(original);one['profiles'][0]['other_color_polynomial'][0]=1;damaged.append(one)
    one=copy.deepcopy(original);one['zero_other_color_hole_triples'].pop();damaged.append(one)
    one=copy.deepcopy(original);one['profile_classes'].pop();damaged.append(one)
    one=copy.deepcopy(original);one['zero_other_color_reflection_classes'].pop();damaged.append(one)
    one=copy.deepcopy(original);one['seed'].pop();damaged.append(one)
    one=copy.deepcopy(original);one['q']=101;damaged.append(one)
    one=copy.deepcopy(original);one['profiles'][0]['path_polynomial'][2]+=1;damaged.append(one)
    with tempfile.TemporaryDirectory() as directory:
        p=Path(directory)/'damaged.json'
        for proposed in damaged:
            p.write_text(json.dumps(proposed))
            try:check(p)
            except (ValueError,KeyError,IndexError):pass
            else:raise ValueError('Damaged local cover/polynomial accepted')
    return {'positive_local_accepted':positive['local_accepted'],'damaged_local_artifacts_rejected':len(damaged)}

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('path',type=Path)
    a=p.parse_args();print(json.dumps(controls(a.path)))
