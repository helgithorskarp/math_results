#!/usr/bin/env python3
"""Finite controls of the one-pool-point repair lemma, including its boundary."""
import json
from itertools import combinations


def main():
    R=set(range(7));P=set(range(2,7))
    subsets=[{v for v in R if mask>>v&1} for mask in range(128)]
    eligible=[X for X in subsets if len(X&P)>=3]
    checks=already_present=0
    for p in sorted(P):
        # This maximal family contains every possible clause with common p.
        family=[D for D in subsets if p in D]
        assert len(family)==64
        for X in eligible:
            Y=X|{p}
            if len(Y&P)<4:Y=Y|{min(P-Y)}
            assert X<=Y and len(Y-X)<=1 and len(Y&P)>=4
            assert all(Y&D for D in family)
            checks+=1;already_present+=p in X
    for X in eligible:
        Y=X if len(X&P)>=4 else X|{min(P-X)}
        assert X<=Y and len(Y-X)<=1 and len(Y&P)>=4
        checks+=1
    # A common original vertex alone cannot always repair the pool quota.
    X={2,3,4};family=[{0},{2},{3},{4}]
    m=min(len(Y) for Y in subsets if len(Y&P)>=4 and all(Y&D for D in family))
    assert m==5 and len(X)==m-2 and all(X&D for D in family[1:])
    assert not X&family[0] and len((X|{0})&P)==3
    print(json.dumps(dict(pool_and_empty_family_repairs=checks,
                          common_point_already_selected=already_present,
                          common_original_vertex_counterexample=True,
                          status='POOL-REPAIR LEMMA CONTROLS VERIFIED'),indent=2,sort_keys=True))


if __name__=='__main__':main()
