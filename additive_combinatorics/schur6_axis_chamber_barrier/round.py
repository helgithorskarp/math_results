"""Exact integer rounding of interval-length sums for an axis chamber."""
import argparse
from fractions import Fraction
import itertools
import json
import math
from pathlib import Path

from model import model,bound


def run(source,multiplier,output,target=108,max_tests=500):
    word=json.loads(Path(source).read_text())['word'];m=model(word,multiplier)
    rows=m['rows'][:];reasons=m['reasons'][:];d=m['dimension'];cuts=[];tests=0
    objectives={tuple(int(lo<=j<hi) for j in range(d)) for lo in range(d) for hi in range(lo+1,d+1)}
    objectives.update(tuple(int(j in (x,y)) for j in range(d)) for x,y in itertools.combinations(range(d),2))
    attempted=set()
    while True:
        upper,proof,point=bound(m,rows,reasons,m['objective'],1)
        if upper<=target or tests>=max_tests:break
        candidates=[]
        for obj in objectives:
            if obj in attempted:continue
            val=sum(c*x for c,x in zip(obj,point))
            if abs(val-round(val))>1e-6:candidates.append((sum(obj),math.floor(val),obj,val))
        candidates.sort();changed=False
        for _,_,obj,val in candidates:
            if tests>=max_tests:break
            attempted.add(obj);tests+=1;cap,certificate,_=bound(m,rows,reasons,list(obj),0)
            if math.floor(cap)<val-1e-7:
                certificate.update(coefficients=list(obj),upper=str(cap));cuts.append(certificate)
                rows.append([*obj,math.floor(cap)]);reasons.append(['integer_rounding',len(cuts)-1]);changed=True
                attempted.clear()
                print(json.dumps(dict(multiplier=multiplier,cut=len(cuts),objective=list(obj),upper=str(cap),floor=math.floor(cap),tests=tests)),flush=True)
                break
        if not changed:break
    record=dict(multiplier=multiplier,dimension=d,run_colours=m['run_colours'],upper_bound_axis_factor=str(upper),
        rounding_cuts=cuts,tests=tests,**proof)
    Path(output).write_text(json.dumps(record,indent=2)+'\n')
    print(json.dumps(dict(multiplier=multiplier,upper=str(upper),cuts=len(cuts),tests=tests)),flush=True)
    return record


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--source',required=True);p.add_argument('--output',required=True)
    p.add_argument('--multiplier',type=int,required=True);p.add_argument('--target',type=int,default=108)
    args=p.parse_args();run(args.source,args.multiplier,args.output,args.target)
