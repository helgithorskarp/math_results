"""Exact necessary small-excess P7 inventory layer; not ambient enumeration.

Unit leave graphs are imported from the reviewed literal catalog. The
nonunit rows use every high leave with h-1 edges, not a heavy census.
The source-domain guard is a fixed 2 million recursive visits per case.
An interrupted/guarded case never produces COMPLETE status. Threads one.
"""
from collections import Counter
import hashlib
import itertools
import json
from pathlib import Path
import sys
import time

ROOT = Path(__file__).resolve().parent
from row_types import statistics, unit_graphs, need


def types():
    units = unit_graphs(json.loads((ROOT/'unit_fixtures.json').read_text()))
    ts = set()
    for delta in ((1,1,1,1,1),(2,1,1,1),(3,1,1),(2,2,1)):
        h=len(delta)
        for leave in itertools.combinations(list(itertools.combinations(range(h),2)),h-1):
            if h == 5 and min(tuple(sorted(tuple(sorted((p[a],p[b]))) for a,b in leave))
                              for p in itertools.permutations(range(h))) not in units:
                continue
            for hubs in itertools.permutations(range(h+3),3):
                row=statistics(delta,leave,hubs)
                if row[3]+row[4] <= 6:
                    ts.add(row)
    return sorted(ts)


def run_case(alltypes, a,b,c,t,targetE):
    D=(14-c,6-b,6-a); budget=6-t
    bases={r[:3]:r for r in alltypes if r[3]+r[4]==0}
    extras=[r for r in alltypes if r[3]+r[4]>0 and r[3] <= targetE]
    counts=Counter(); survivors=[]; states=0; chosen=[]
    def visit(start,cost,E,d):
        nonlocal states
        states += 1
        need(states <= 2_000_000, 'fixed inventory state guard hit; incomplete')
        if E == targetE:
            remaining=tuple(D[j]-d[j] for j in range(3))
            z=15-len(chosen)-sum(remaining)
            if min(remaining)>=0 and z>=0:
                rows=chosen.copy()
                bcounts=(z,)+remaining
                for dh,n in zip(((0,0,0),(1,0,0),(0,1,0),(0,0,1)),bcounts):
                    rows.extend([bases[dh]]*n)
                need(len(rows)==15,'row count')
                EH=sum(sum(max(0,v-1) for v in r[:3]) for r in rows)
                Q=sum(r[4] for r in rows)
                if E >= EH and (E-EH)%2==0 and budget-E-Q>=0 and (budget-E-Q)%2==0:
                    X=(E-EH)//2; tau=(budget-E-Q)//2
                    counts['budget_valid']+=1
                    lows=tuple(sum(r[i]==r[j]==0 for r in rows) for i,j in ((0,1),(0,2),(1,2)))
                    if any(n>cap for n,cap in zip(lows,(3*a-t,3*b-t,3*c-t))):
                        counts['low_pair_fail']+=1
                    else:
                        degrees=tuple(sum(r[5] for r in rows if r[6+j]) for j in range(3))
                        if any(s>28-X for s in degrees):
                            counts['independent_cohort_fail']+=1
                        else:
                            counts['survivor']+=1
                            survivors.append(dict(exceptional_rows=chosen.copy(),base_counts=bcounts,
                                                  E=E,Q=Q,X=X,tau=tau,low_counts=lows,
                                                  good_degrees=degrees))
        for i in range(start,len(extras)):
            r=extras[i];newcost=cost+r[3]+r[4];ne=E+r[3]
            if newcost>budget or ne>targetE or len(chosen)==15:
                continue
            nd=tuple(d[j]+r[j] for j in range(3))
            if any(nd[j]>D[j] for j in range(3)):
                continue
            chosen.append(r);visit(i,newcost,ne,nd);chosen.pop()
    visit(0,0,0,(0,0,0))
    return dict(pair_multiplicities=(a,b,c),t=t,E=targetE,cross_weights=D,
                states=states,counts=dict(counts),survivors=survivors)
