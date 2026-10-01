#!/usr/bin/env python3
"""Optional exact source bridge; explicitly imports the PINNED author code.

This program is separate from the independent mathematical audit. The
author constructor is an input here, and is not a premise of audit.py.
"""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
from fractions import Fraction as F
import audit as independent


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--author',type=Path,required=True)
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    code=args.author/'verify.py'
    independent.require(hashlib.sha256(code.read_bytes()).hexdigest()==
        '2f399c4db370b97a4b394fbd2420140dfca4cc5d9879188b76fb464d6ac1d635',
        'wrong author source')
    spec=importlib.util.spec_from_file_location('pinned_author_complement',code)
    author=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(author)
    records=[]
    entries=0
    for n in [4,5,6,7]:
        d=independent.data(n)
        af,ap,_,s,N=author.data(n)
        decoded=[frozenset(i+1 for i in range(n) if a & (1<<i)) for a in af]
        order=[0]+[d['index'][a] for a in decoded]
        for label,z in [('zero',[F(0)]*len(ap)),('one',[F(1)]*len(ap)),
                        ('two',[F(2)]*len(ap)),
                        ('one_flip',[F(s)]+[F(0)]*(len(ap)-1)),
                        ('asymmetric',[F(i%4,5) for i in range(len(ap))])]:
            weights={frozenset(i+1 for i in range(n) if a&(1<<i)):x
                     for pair,x in zip(ap,z) for a in pair}
            mine=independent.literal_architecture(d,[weights[a] for a,b in d['pairs']])
            C,K,L=author.matrix(n,z)
            independent.require(all(L[i][j]==mine[order[i]][order[j]]
                                    for i in range(N) for j in range(N)),
                                'full source entry mismatch')
            independent.require(all(K[i][j]==L[i+1][j+1] and C[i][j]==K[i][j]-1
                                    for i in range(N-1) for j in range(N-1)),
                                'author core/lift mismatch')
            entries += N*N+2*(N-1)**2
            records.append({'n':n,'label':label,'entries':N*N+2*(N-1)**2})
    result={'method':'optional pinned author import; independent tuple-set constructor; all full/core entries',
            'author_verify_sha256':hashlib.sha256(code.read_bytes()).hexdigest(),
            'cases':len(records),'entries':entries,'records':records}
    raw=json.dumps(result,sort_keys=True,indent=2)+'\n'
    args.output.write_text(raw)
    print(json.dumps({'cases':len(records),'entries':entries,'sha256':hashlib.sha256(raw.encode()).hexdigest()}))


if __name__=='__main__':
    main()
