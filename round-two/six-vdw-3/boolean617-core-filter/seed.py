#!/usr/bin/env python3
"""Reproduce the known Rabung617 length3703 bound, never a record improvement."""
import argparse
import hashlib
import json
from pathlib import Path


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    p,n=617,3703
    generated=[]
    for position in range(1,n+1):
        z=(position-1)%p
        generated.append(1 if position==1 else 0 if z==0 or pow(z,308,p)==1 else 1)
    # Separate character oracle and literal integer-AP checker.
    squares={a*a%p for a in range(1,p)}
    colors=[int(position==1 or ((position-1)%p!=0 and (position-1)%p not in squares)) for position in range(1,n+1)]
    if generated!=colors or len(squares)!=308:
        raise ValueError('Independent seed reconstruction disagrees')
    progressions=0
    for d in range(1,(n-1)//6+1):
        for a in range(1,n-6*d+1):
            first=colors[a-1]
            monochromatic=True
            for j in range(1,7):
                if colors[a+j*d-1]!=first:
                    monochromatic=False
                    break
            if monochromatic:
                raise ValueError(f'Known seed recipe failed at ordinary AP {a},{d}')
            progressions+=1
    if progressions!=1140833:
        raise ValueError('Incomplete ordinary AP coverage')
    bits=''.join(map(str,colors)).encode()
    result={'schema':'known-rabung617-seed-v1','status':'KNOWN_3703_SEED_INDEPENDENTLY_RECONSTRUCTED_AND_CHECKED',
            'agent':'six-vdw-3','role':'researcher','interval':n,'prime':p,
            'formula':'c(1)=1; c(n)=0 if (n-1)%617 is zero or a nonzero square; otherwise c(n)=1.',
            'ordinary_nonconstant_seven_term_APs_checked':progressions,
            'coloring_ascii_bits_sha256':hashlib.sha256(bits).hexdigest(),
            'known_bound_context':'Monroe Table1 >3703 / Table2 prime617 / Rabung construction; no numerical improvement.'}
    args.output.write_text(json.dumps(result,sort_keys=True,indent=2)+'\n')
    print(json.dumps(result))


if __name__=='__main__':
    main()
