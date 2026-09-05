#!/usr/bin/env python3
"""Optional bounded discovery of primals; never treat MILP failure as proof."""
import json
import numpy as np
from scipy.optimize import Bounds, LinearConstraint, milp
import verify as v


def main():
    p,union=v.parent();y=p.normal_form(4,2);near=p.adjacency(443,5)
    pairs,caps,old=p.edge_rows(y,near,union);out=[]
    for k in (11,12):
        rows=old+v.extra_rows(y,pairs,k)
        ans=milp(np.zeros(len(pairs)),integrality=np.ones(len(pairs)),
                 bounds=Bounds(np.zeros(len(pairs)),caps),
                 constraints=LinearConstraint([r[1] for r in rows],[r[2] for r in rows],[r[3] for r in rows]),
                 options={'time_limit':20})
        v.require(ans.success,'no certified primal found within bounded discovery')
        e=[round(x) for x in ans.x];p.check_edge_witness(y,e,near,union);v.check_extra(y,pairs,e,k)
        out.append({'W_edges':k,'a':[4,2,8],'edge_counts':e})
    print(json.dumps(out,indent=2))


if __name__=='__main__':main()
