#!/usr/bin/env python3
"""Complete uncolored triple quotient, audited by literal affine actions."""
import argparse
import hashlib
import itertools
import json
import math
import time
from pathlib import Path

def need(condition,message):
    if not condition:raise ValueError(message)

def representatives(q):
    need(q>=7 and all(q%d for d in range(2,math.isqrt(q)+1)),'Prime q>=7 required')
    left=set(range(2,q));result=[]
    while left:
        x=min(left);orbit={x,(1-x)%q,pow(x,-1,q),pow(1-x,-1,q),x*pow(x-1,-1,q)%q,(x-1)*pow(x,-1,q)%q}
        need(orbit<=left,'Overlapping normalized parameter classes')
        result.append({'representative':x,'parameters':sorted(orbit)});left-=orbit
    return result

def audit(q):
    begin=time.monotonic();records=[];owners={}
    for shape in representatives(q):
        lam=shape['representative'];literal=set();stabilizer=0
        for scale in range(1,q):
            for shift in range(q):
                triple=tuple(sorted((scale*x+shift)%q for x in (0,1,lam)))
                literal.add(triple);stabilizer+=int(triple==(0,1,lam))
        need(len(literal)*stabilizer==q*(q-1),'Orbit/stabilizer discrepancy')
        for triple in literal:
            need(triple not in owners,'Two affine classes overlap');owners[triple]=lam
        records.append({**shape,'raw_hole_sets':len(literal),'stabilizer':stabilizer})
    need(len(owners)==math.comb(q,3),'Raw hole family incomplete')
    encoded=bytearray()
    for triple in itertools.combinations(range(q),3):
        root_values=[]
        for first,second,third in itertools.permutations(triple):
            root_values.append((third-first)*pow(second-first,-1,q)%q)
        need(owners[triple]==min(root_values),'Literal ordered-root owner mismatch')
        encoded.extend(owners[triple].to_bytes(2,'little'))
    return {'q':q,'raw_hole_sets':math.comb(q,3),'classes':records,'representatives':[x['representative'] for x in records],
            'owner_array_u16le_sha256':hashlib.sha256(encoded).hexdigest(),'orientation_stabilizer_invariance_imposed':False,
            'seconds':time.monotonic()-begin}

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--q',type=int,default=103);p.add_argument('--output',type=Path)
    a=p.parse_args();d=audit(a.q)
    if a.output:a.output.write_text(json.dumps(d,indent=2)+'\n')
    print(json.dumps(d))
