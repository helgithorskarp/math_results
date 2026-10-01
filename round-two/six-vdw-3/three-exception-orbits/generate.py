#!/usr/bin/env python3
"""Full orientation CNF for a fixed sparse ternary skeleton; no weight caps."""
import argparse
import functools
import hashlib
import json
from pathlib import Path
from normalize import skeleton

@functools.lru_cache(maxsize=None)
def patterns(phases):
    result=set()
    for slope in range(6):
        for start in range(6):
            row=tuple(int((start+j*slope-phase)%6>=3) for j,phase in enumerate(phases))
            if row[0]:row=tuple(1-value for value in row)
            result.add(row)
    return tuple(sorted(result))

def generate(q,kind,lam,path):
    tau=skeleton(q,kind,lam);clauses=set()
    for step in range(1,(q+1)//2):
        for start in range(q):
            points=tuple((start+j*step)%q for j in range(7))
            for row in patterns(tuple(tau[x] for x in points)):
                clause=tuple(sorted((x+1)*(1 if value==0 else -1) for x,value in zip(points,row)))
                clauses.add(clause);clauses.add(tuple(sorted(-literal for literal in clause)))
    clauses.add((-1,))
    raw=('p cnf '+str(q)+' '+str(len(clauses))+'\n'+''.join(' '.join(map(str,clause))+' 0\n' for clause in sorted(clauses))).encode()
    path.write_bytes(raw)
    return {'q':q,'kind':kind,'lambda':lam,'variables':q,'clauses':len(clauses),
            'orientation_anchor':'u(0)=0 by global color exchange only',
            'counter_variables':0,'weight_cap':None,'cnf_sha256':hashlib.sha256(raw).hexdigest()}

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--q',type=int,default=103);parser.add_argument('--kind',choices=('same','mixed'),required=True)
    parser.add_argument('--lambda',dest='lam',type=int,required=True);parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args();print(json.dumps(generate(args.q,args.kind,args.lam,args.output)))

if __name__=='__main__':main()
