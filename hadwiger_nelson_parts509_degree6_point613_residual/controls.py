#!/usr/bin/env python3
"""Definition-level finite controls for each monotone repair argument."""
from itertools import combinations
import json


def compute():
    R=set(range(8));P={5,6,7};A={0,5};B={1,2}
    counts={'hit_B':0,'hit_A_with_quota':0,'two_repairs':0,'already_present':0}
    for size in range(9):
        for values in combinations(R,size):
            X=set(values)
            for quota in [2,3]:
                for bound in range(3,10):
                    if len(X)>bound-2 or len(X&P)<quota-1:continue
                    repairs=[]
                    if X&B:
                        Y=X|{5}
                        if len(Y&P)<quota:Y.add(min(P-Y))
                        repairs.append(('hit_B',Y))
                    if X&A and len(X&P)>=quota:repairs.append(('hit_A_with_quota',X|{1}))
                    if len(X)<=bound-3:
                        Y=X|{5,1}
                        if len(Y&P)<quota:Y.add(min(P-Y))
                        repairs.append(('two_repairs',Y))
                    for case,Y in repairs:
                        assert X<=Y<=R and Y&A and Y&B and len(Y&P)>=quota and len(Y)<=bound-1
                        counts[case]+=1;counts['already_present']+=int(5 in X)
    # Negative control: these two missing rows need not have a common repair.
    X={3,4,6,7};assert not (A&B) and not any((X|{v})&A and (X|{v})&B for v in R)
    return dict(status='STAGED REPAIR CONTROLS VERIFIED',**counts,two_disjoint_missing_rows_need_two_additions=True)


if __name__=='__main__':print(json.dumps(compute(),indent=2,sort_keys=True))
