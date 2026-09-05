#!/usr/bin/env python3
"""Finite controls for counters and loss of one killing-set clause."""
from itertools import combinations,product
import json,random
from cardinality import Builder
from build_master import propagate


def main():
    counters=0
    for n in range(8):
        for k in range(n+2):
            for required in (False,True):
                b=Builder(n);t=b.threshold(list(range(1,n+1)),k);b.clause(t if required else b.neg(t))
                for values in product((False,True),repeat=n):
                    assert propagate(b.rows,dict(enumerate(values,1)))==((sum(values)>=k)==required)
                    counters+=1
    R=set(range(6));P={3,4,5};D={0,1};rng=random.Random(610)
    subsets=[set(v for v in R if mask>>v&1) for mask in range(64)]
    families=[[D]]+[[D]+rng.sample(subsets[1:],rng.randrange(1,12)) for _ in range(63)]
    checked=tight=0
    for family in families:
        m=min(len(X) for X in subsets if len(X&P)>=2 and all(X&C for C in family))
        for X in subsets:
            if len(X&P)<1 or not all(X&C for C in family[1:]):continue
            assert len(X)>=m-2
            if len(X)==m-2:
                assert len(X&P)==1 and not X&D
                tight+=1
            checked+=1
    assert tight>0
    print(json.dumps(dict(counter_assignments=counters,abstract_families=len(families),
                          relaxed_assignments=checked,tight_boundary_cases=tight,
                          status='EXACT COUNTER AND ONE-CLAUSE-LOSS CONTROLS VERIFIED'),indent=2))


if __name__=='__main__':main()
