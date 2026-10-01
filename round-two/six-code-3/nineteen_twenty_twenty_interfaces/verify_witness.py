"""Standalone literal verification of the positive67-word example."""
from collections import Counter
import copy
from itertools import combinations
import json
from pathlib import Path

import verify_residual as v

HERE=Path(__file__).resolve().parent


def check(witness):
    v.check(witness['center_triple']==[17,15,16] and
            witness['center_degrees']==[19,20,20] and
            witness['pair_multiplicities']==[5,5,4],'witness declaration')
    core=v.decode(witness['core_blocks'],45)
    words=v.decode(witness['blocks'],67)
    v.check(v.sha(sorted(witness['core_blocks']))==witness['core_sha256'],'positive core binding')
    v.check(set(core)<=set(words),'positive core containment')
    candidates,adjacent=v.candidates_graph(core)
    indices=witness['residual_indices']
    v.check(type(indices) is list and len(indices)==len(set(indices))==22 and
            all(type(i) is int and 0<=i<len(candidates) for i in indices),'positive residual indices')
    residual=[frozenset(candidates[i]) for i in indices]
    v.check(set(words)==set(core)|set(residual),'positive residual decoder')
    degrees=Counter(sum(i in w for w in words) for i in range(18))
    return {'status':'EXACT_LITERAL_POSITIVE','words':67,'center_degrees':[19,20,20],
            'pair_multiplicities':[5,5,4],'uncovered_center_triple':True,
            'degree_census':dict(sorted(degrees.items())),'witness_sha256':v.sha(witness)}


def run():
    witness=json.loads((HERE/'witness67.json').read_text())
    record=check(witness)
    for kind in ('index','duplicate','degree','hash'):
        damaged=copy.deepcopy(witness)
        if kind=='index':damaged['residual_indices'][0]=True
        elif kind=='duplicate':damaged['blocks'][0]=damaged['blocks'][1]
        elif kind=='degree':damaged['center_degrees']=[19,19,19]
        else:damaged['core_sha256']='0'*64
        try:
            check(damaged)
        except (ValueError,TypeError):
            continue
        raise ValueError('damaged positive witness accepted')
    record['bad_witness_rejections']=4
    print(json.dumps(record),flush=True)
    return record


if __name__=='__main__':
    run()
