"""Seek integer interval lengths; accept only a directly verified full word."""
import argparse
import json
import time
from pathlib import Path
from model import chamber
from word import verify_word

def decode_lengths(model,lengths):
    assert all(type(v)is int and v>=1 for v in lengths)
    assert all(sum(c*x for c,x in zip(row[:-1],lengths))<=row[-1] for row in model['rows'])
    assert all(sum(c*x for c,x in zip(row[:-1],lengths))==row[-1] for row in model['equalities'])
    parts=[];pos=0
    for colours in model['run_colours']:
        values=[]
        for c in colours:values.extend([c]*lengths[pos]);pos+=1
        parts.append(values)
    E,A,B=parts;a=2*len(E)+1;assert len(A)==len(B)==a
    row=[None]*(5*a)
    for u,c in enumerate(E,1):row[5*u]=row[5*(a-u)]=c
    for b,Q in ((1,A),(2,B)):
        for q,state in enumerate(Q):
            c=state if state else b-1;row[5*q+b]=row[5*a-5*q-b]=c
    record=dict(axis_factor=a,word=row[1:],run_lengths=lengths)
    record['check']=verify_word(record)
    record['residual_sizes']=[A.count(0),B.count(0)]
    return record

def run(source,multiplier,output,seconds=45):
    import numpy as np
    from scipy.optimize import milp,Bounds,LinearConstraint
    model=chamber(source,multiplier);rows=np.array(model['rows'],dtype=float);eq=np.array(model['equalities'],dtype=float)
    A=np.vstack((rows[:,:-1],eq[:,:-1]));upper=np.concatenate((rows[:,-1],eq[:,-1]));lower=np.concatenate((np.full(len(rows),-np.inf),eq[:,-1]))
    tick=time.monotonic();result=milp(-np.array(model['objective']),integrality=np.ones(model['dimension']),
       bounds=Bounds(np.ones(model['dimension']),np.full(model['dimension'],np.inf)),
       constraints=LinearConstraint(A,lower,upper),options={'time_limit':seconds,'mip_rel_gap':0})
    report=dict(source=source,multiplier=multiplier,mip_status=int(result.status),mip_message=result.message,
                seconds=time.monotonic()-tick,time_limit=seconds,status='NO_WITNESS')
    if result.x is not None:
        lengths=[int(round(x)) for x in result.x]
        report.update(decode_lengths(model,lengths));report['status']='FULL_WORD_VERIFIED'
    Path(output).write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k not in ('word','run_lengths')}),flush=True)
    return report

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--source',required=True);p.add_argument('--multiplier',type=int,required=True)
    p.add_argument('--output',required=True);p.add_argument('--seconds',type=int,default=45)
    args=p.parse_args();run(args.source,args.multiplier,args.output,args.seconds)
