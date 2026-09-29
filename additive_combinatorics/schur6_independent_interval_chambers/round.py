"""Find exact one-coordinate Chvatal rounding steps for a chamber bound."""
import argparse
import json
import math
from fractions import Fraction
from pathlib import Path
from model import chamber

def run(source,multiplier,output,target_bound=70,max_tests=20):
    import numpy as np
    from scipy.optimize import linprog
    m=chamber(source,multiplier);rows=m['rows'][:];reasons=m['reasons'][:];eq=np.array(m['equalities'],float)
    cuts=[];attempted=set();tests=0
    def bound(objective,constant=0):
        arr=np.array(rows,float)
        r=linprog(-np.array(objective),A_ub=arr[:,:-1],b_ub=arr[:,-1],A_eq=eq[:,:-1],b_eq=eq[:,-1],bounds=(None,None),method='highs',options={'time_limit':45})
        assert r.success,r.message
        weights=[Fraction(float(-v)).limit_denominator(1000000) for v in r.ineqlin.marginals]
        equal=[Fraction(float(-v)).limit_denominator(1000000) for v in r.eqlin.marginals]
        assert all(w>=0 for w in weights)
        active=[(w,row) for w,row in zip(weights,rows) if w]+[(w,row) for w,row in zip(equal,m['equalities']) if w]
        assert [sum(w*row[k] for w,row in active) for k in range(m['dimension'])]==list(objective)
        upper=constant+sum(w*row[-1] for w,row in zip(weights,rows))+sum(w*row[-1] for w,row in zip(equal,m['equalities']))
        proof=dict(terms=[dict(reason=reasons[i],weight=str(w)) for i,w in enumerate(weights) if w],equality_weights=list(map(str,equal)))
        return upper,proof,r.x
    while True:
        upper,proof,point=bound(m['objective'],1)
        if upper<=target_bound or tests>=max_tests:break
        candidates=[j for j,x in enumerate(point) if abs(x-round(x))>1e-6 and j not in attempted]
        candidates.sort(key=lambda j:(math.floor(point[j]),j))
        changed=False
        for j in candidates:
            if tests>=max_tests:break
            attempted.add(j);tests+=1
            obj=[int(k==j) for k in range(m['dimension'])];cap,certificate,_=bound(obj)
            if math.floor(cap)<point[j]-1e-7:
                certificate.update(coordinate=j,upper=str(cap));cuts.append(certificate)
                rows.append(obj+[math.floor(cap)]);reasons.append(['integer_rounding',len(cuts)-1]);changed=True
                print(json.dumps(dict(multiplier=multiplier,coordinate=j,rational_upper=str(cap),integer_upper=math.floor(cap))),flush=True)
                break
        if not changed:break
    record=dict(multiplier=multiplier,rounding_cuts=cuts,upper_bound_axis_factor=str(upper),tests=tests,**proof)
    Path(output).write_text(json.dumps(record,indent=2)+'\n')
    print(json.dumps(dict(multiplier=multiplier,upper=str(upper),rounding_cuts=len(cuts),tests=tests)),flush=True)
    return record

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--source',required=True);p.add_argument('--multiplier',type=int,required=True);p.add_argument('--output',required=True)
    args=p.parse_args();run(args.source,args.multiplier,args.output)
