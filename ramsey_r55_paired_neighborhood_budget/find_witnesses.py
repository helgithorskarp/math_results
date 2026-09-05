#!/usr/bin/env python3
"""Optional bounded discovery of alternative exact edge-count witnesses.

No infeasibility verdict is published or used: any missing primal aborts.
Output may differ from the reference witnesses, whose validity is checked
directly by verify.py without these numerical dependencies.
"""
import json
import numpy as np
from scipy.optimize import Bounds,LinearConstraint,milp
import verify as v

old,union=v.inputs();caps,b,near=v.replay_core(old,union)
records=[]
for y in v.old_vectors(caps,b,near,union):
    if v.statistics(y)[2]<76:continue
    pairs,boxes,rows=v.edge_rows(y,near,union)
    result=milp(np.zeros(len(pairs)),integrality=np.ones(len(pairs)),bounds=Bounds(0,boxes),
                constraints=LinearConstraint([r[1] for r in rows],[r[2] for r in rows],[r[3] for r in rows]),
                options={'time_limit':20})
    v.require(result.success,'bounded discovery found no verified primal: '+result.message)
    e=[round(x) for x in result.x]
    v.check_edge_witness(y,e,near,union)
    records.append({'a':[y[5],y[9],y[17]],'edge_counts':e})
v.require(len(records)==7,'complete discovery output')
print(json.dumps(records,indent=2))
