"""Discover an integral axis word; exact inequalities and sums are mandatory."""
import argparse
import json
from pathlib import Path

from audit import check_word
from model import model


def run(source,multiplier,output):
    import numpy as np
    from scipy.optimize import milp,Bounds,LinearConstraint
    m=model(json.loads(Path(source).read_text())['word'],multiplier)
    rows=np.array(m['rows'],float)
    r=milp(-np.array(m['objective']),integrality=np.ones(m['dimension']),
        bounds=Bounds(np.ones(m['dimension']),np.full(m['dimension'],np.inf)),
        constraints=LinearConstraint(rows[:,:-1],np.full(len(rows),-np.inf),rows[:,-1]),
        options={'time_limit':30,'mip_rel_gap':0})
    assert r.x is not None,r.message
    lengths=[int(round(x)) for x in r.x];assert all(x>=1 for x in lengths)
    assert all(sum(c*x for c,x in zip(row[:-1],lengths))<=row[-1] for row in m['rows'])
    half=[c for c,x in zip(m['run_colours'],lengths) for _ in range(x)]
    axis=half+half[::-1];check=check_word(axis)
    record=dict(multiplier=multiplier,axis_factor=len(axis)+1,axis_word=axis,
        run_lengths=lengths,status='FULL_AXIS_WORD_VERIFIED',class_sizes=check['class_sizes'])
    Path(output).write_text(json.dumps(record,indent=2)+'\n')
    print(json.dumps({k:v for k,v in record.items() if k not in ('axis_word','run_lengths')}))


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--source',required=True)
    p.add_argument('--multiplier',type=int,default=15);p.add_argument('--output',required=True)
    args=p.parse_args();run(args.source,args.multiplier,args.output)
