#!/usr/bin/env python3
"""Reject narrowed negative coverage, changed word, and inflated scope."""
import argparse
import copy
import json
import tempfile
from pathlib import Path
import cover_check


def controls(expected_path):
    expected=json.loads(expected_path.read_text())
    cover_check.manifest_guard(expected_path)
    changes=[]
    omitted=copy.deepcopy(expected);omitted['number_of_sparse_negative_inputs']=0;changes.append(omitted)
    narrowed=copy.deepcopy(expected);narrowed['cover']['number_of_sparse_negative_inputs']=0;changes.append(narrowed)
    word=copy.deepcopy(expected);word['model']['fixed_core_bits'][7][1]=0;changes.append(word)
    fixed=copy.deepcopy(expected);fixed['model']['other_regular_bits_free']=0;changes.append(fixed)
    global_count=copy.deepcopy(expected);global_count['cover']['admissible_global_colorings_counted']=True;changes.append(global_count)
    W=copy.deepcopy(expected);W['cover']['W_bound_improved']=True;changes.append(W)
    with tempfile.TemporaryDirectory() as directory:
        path=Path(directory)/'damaged.json'
        for damaged in changes:
            path.write_text(json.dumps(damaged)+'\n')
            try:cover_check.manifest_guard(path)
            except ValueError:pass
            else:raise ValueError('Damaged coverage/scope accepted')
    return {'complete_manifest_positive_control':True,'damaged_source_records_rejected':len(changes)}


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--expected',type=Path,required=True)
    args=parser.parse_args()
    print(json.dumps(controls(args.expected)))
