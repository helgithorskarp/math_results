#!/usr/bin/env python3
"""Reject incomplete coverage, altered signed words and outside invariance."""
import argparse
import copy
import json
import tempfile
from pathlib import Path
import cover_check

def controls(path):
    source=json.loads(path.read_text());cover_check.verify(path)
    damaged=[]
    missing=copy.deepcopy(source);missing['cases'].pop();damaged.append(missing)
    orbit=copy.deepcopy(source);orbit['cases'][0]['represented_raw_inputs'].pop();damaged.append(orbit)
    word=copy.deepcopy(source);word['cases'][0]['reflected_to_E1_fixed_core_bits'][5][1]=0;damaged.append(word)
    symmetry=copy.deepcopy(source);symmetry['cases'][10]['reflection_invariance_imposed']=True;damaged.append(symmetry)
    bound=copy.deepcopy(source);bound['cases'][0]['other_regular_bits_free']=87;damaged.append(bound)
    premise=copy.deepcopy(source);premise['mathematical_dependencies'].pop();damaged.append(premise)
    with tempfile.TemporaryDirectory() as directory:
        target=Path(directory)/'damaged.json'
        for item in damaged:
            target.write_text(json.dumps(item)+'\n')
            try:cover_check.verify(target)
            except ValueError:pass
            else:raise ValueError('Damaged coverage accepted')
    return {'positive_complete_cover':True,'damaged_source_records_rejected':len(damaged)}

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--cover',type=Path,required=True)
    print(json.dumps(controls(p.parse_args().cover)))
