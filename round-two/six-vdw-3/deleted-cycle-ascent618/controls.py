#!/usr/bin/env python3
"""Positive small literal tests, exact cycle decoding, and model damage probes."""
import argparse
import itertools
import json
from pathlib import Path
from generate import generate
from check import audit, small, parameters, parse, need

def shapes(q):
    left=set(range(2,q));result=[]
    while left:
        x=min(left);orbit={x,(1-x)%q,pow(x,-1,q),pow(1-x,-1,q),x*pow(x-1,-1,q)%q,(x-1)*pow(x,-1,q)%q}
        result.append(x);left-=orbit
    return result

def controls(q,work):
    work.mkdir(parents=True,exist_ok=True);cases=[];damages=0;pair_inputs=pair_valid=0
    for lam in shapes(q):
        path=work/('lambda-'+str(lam)+'.cnf');model=generate(q,lam,path);checked=audit(path,q,lam);checked.pop('seconds')
        for key in model:need(model[key]==checked[key],'Small model/audit mismatch')
        enumeration=small(path,q,lam);cases.append({'model':model,'audit':checked,'enumeration':enumeration})
        if q==7:
            _,outside,pairs,index=parameters(q,lam);rows=parse(path,len(pairs))
            for values in itertools.product((0,1),repeat=len(pairs)):
                cnf=all(any(values[abs(x)-1]==int(x>0) for x in row) for row in rows)
                u={outside[0]:0}
                for x in outside[1:]:u[x]=values[index[(outside[0],x)]-1]
                consistent=all(values[index[(x,y)]-1]==u[x]^u[y] for x,y in pairs)
                need(cnf==consistent,'Complete small cycle-basis decoding mismatch')
                pair_inputs+=1;pair_valid+=int(cnf)
        original=path.read_text();lines=original.splitlines();header=lines[0].split();badpath=work/'damaged.cnf'
        versions=[]
        # Remove a root parity clause, add an unauthorized seed unit, and widen
        # the declared domain. Each has a distinct semantic failure.
        removed=next(i for i,line in enumerate(lines[1:],1) if len(line.split())==4)
        damaged=lines[:removed]+lines[removed+1:];damaged[0]='p cnf '+header[2]+' '+str(int(header[3])-1);versions.append('\n'.join(damaged)+'\n')
        versions.append('p cnf '+header[2]+' '+str(int(header[3])+1)+'\n'+'\n'.join(lines[1:])+'\n1 0\n')
        versions.append('p cnf '+str(int(header[2])+1)+' '+header[3]+'\n'+'\n'.join(lines[1:])+'\n')
        for damaged in versions:
            badpath.write_text(damaged)
            try:audit(badpath,q,lam)
            except ValueError:damages+=1
            else:raise ValueError('Damaged mathematical model accepted')
    return {'q':q,'cases':cases,'normalized_orientation_inputs':sum(x['enumeration']['normalized_inputs'] for x in cases),
            'positive_partial_colorings':sum(x['enumeration']['valid_count'] for x in cases),'damaged_models_rejected':damages,
            'complete_small_pair_inputs':pair_inputs,'consistent_small_pair_inputs':pair_valid}

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--q',type=int,choices=(7,11,13),required=True);p.add_argument('--work',type=Path,required=True)
    a=p.parse_args();print(json.dumps(controls(a.q,a.work)))
