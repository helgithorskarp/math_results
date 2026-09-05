#!/usr/bin/env python3
"""Optional bounded discovery; exact primals only, never trust an UNSAT status."""
import importlib.util
import json
from pathlib import Path
from hashlib import sha256
import numpy as np
from scipy.optimize import Bounds, LinearConstraint, milp

HERE=Path(__file__).resolve().parent
PATH=HERE.parent/'ramsey_r55_paired_neighborhood_budget/verify.py'
if sha256(PATH.read_bytes()).hexdigest()!='518a05072a726287628c57e8c9d9bc16aac4380dd800b4d807d00208b6b6e624':
    raise ValueError('parent hash')
spec=importlib.util.spec_from_file_location('adjusted_parent',PATH)
p=importlib.util.module_from_spec(spec);spec.loader.exec_module(p)
old,union=p.inputs();near=p.adjacency(443,5)
records=json.loads((PATH.parent/'EDGE_WITNESSES.json').read_text())
for r in records:
    a,b,_=r['a'];y=p.normal_form(a,b)
    pairs,boxes,rows=p.edge_rows(y,near,union)
    ww=pairs.index((28,28))
    if r['edge_counts'][ww]<11:
        lower=np.zeros(len(boxes));lower[ww]=11
        result=milp(np.zeros(len(boxes)),integrality=np.ones(len(boxes)),bounds=Bounds(lower,boxes),
                    constraints=LinearConstraint([r[1] for r in rows],[r[2] for r in rows],[r[3] for r in rows]),
                    options={'time_limit':20})
        p.require(result.success,'bounded discovery has no certified primal')
        r['edge_counts']=[round(v) for v in result.x]
    p.check_edge_witness(y,r['edge_counts'],near,union)
    p.require(11<=r['edge_counts'][ww]<=12,'new critical-cell bound')
print(json.dumps(records,indent=2))
