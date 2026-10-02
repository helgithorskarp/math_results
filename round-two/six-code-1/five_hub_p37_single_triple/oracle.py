"""Exact T2 exclusion kernels; actual six-code-1, researcher."""
from collections import Counter
import hashlib
import importlib.util
import itertools as it
import json
import math
from pathlib import Path
import time
HERE=Path(__file__).resolve().parent
PARENT=HERE.parent/"five_hub_pair_total36"
PAIRS=tuple(it.combinations(range(5),2))
PATTERNS=(("T1",((0,1,2),)),("T2_shared_one",((0,1,2),(0,3,4))),("T2_shared_pair",((0,1,2),(0,1,3))))
BTYPE=(1,1,0,True,4,3,0,0,0,0,2)

def independently_derive():
    pairs = list(it.combinations(range(5), 2))
    patterns = [("T1", [(0, 1, 2)]),
                ("T2_shared_one", [(0, 1, 2), (0, 3, 4)]),
                ("T2_shared_pair", [(0, 1, 2), (0, 1, 3)])]
    records = []
    for name, triples in patterns:
        pair_owners = [sum(all(a in triple for a in p) for triple in triples) for p in pairs]
        hub_owners = [sum(a in triple for triple in triples) for a in range(5)]
        variants = [("all_le4", -1, 3)]
        if name == "T2_shared_pair":
            variants.append(("common_pair5", 0, 4))
        for mode, fixed, n in variants:
            locations = [i for i in range(10) if i != fixed]
            candidates = []
            for repeated in it.combinations_with_replacement(locations, n):
                values = [4 + int(i == fixed) - repeated.count(i) for i in range(10)]
                candidates.append(values)
            # Producer's recursive weak compositions increase u lexicographically.
            candidates.sort(key=lambda row: tuple(4-row[i] for i in locations))
            for lam in candidates:
                D = [sum(lam[i] for i in range(10) if a in pairs[i]) - 11 for a in range(5)]
                L = [13 - 3 * lam[i] + pair_owners[i] for i in range(10)]
                reason = "PAIR_FEASIBLE"
                if not all(lam[i] >= pair_owners[i] and lam[i] >= 0 and L[i] >= 0 for i in range(10)):
                    reason = "ACTUAL_HH_HHH_QUOTA"
                elif not all(3 * D[a] - 3 - hub_owners[a] >= 0 for a in range(5)):
                    reason = "Z_EDGES_NONNEGATIVE"
                elif not all(sum(D[a] for a in p) <= 11 for p in pairs):
                    reason = "PAIR_COLUMN11"
                elif not all(L[i] <= sum(D[a] for a in pairs[i]) for i in range(10)):
                    reason = "HH_HIGH_ENDPOINT_WEIGHT"
                columns = []
                if reason == "PAIR_FEASIBLE":
                    for heavy in it.product(*(range(d//2 + 1) for d in D)):
                        N = [d - h for d, h in zip(D, heavy)]
                        if any(L[i] > sum(N[a] for a in pairs[i]) for i in range(10)):
                            continue
                        possible = True
                        for excluded in pairs:
                            remaining = set(range(5)) - set(excluded)
                            available = sum(N[a]+N[b] for a,b in it.combinations(sorted(remaining),2))
                            required = sum(L[pairs.index(p)] for p in it.combinations(sorted(remaining),2))
                            if available < required:
                                possible = False
                                break
                        if possible:
                            columns.append(dict(N=N, n=heavy, K=sum(N)))
                    columns.sort(key=lambda c: c["N"])
                records.append(dict(pattern=name,triples=triples,mode=mode,lam=lam,t=pair_owners,
                    Ta=hub_owners,D=D,L=L,reason=reason,columns=columns))
    return records

def hall_check(types,vector,r,c,covered_pair=True):
    groups=Counter()
    for t,n in zip(types,vector):
        groups[(t[1],t[2])]+=n*(t[10]-t[1])
    groups=sorted((key,n) for key,n in groups.items() if n)
    capacities={a:r['D'][a]-c['N'][a] for a in range(5)}
    available=[]
    for (k,q),number in groups:
        neighbors=set()
        for a in range(5):
            blocked=covered_pair and k==1 and any(v==5 and a in p for p,v in zip(PAIRS,r['lam']))
            possible_LOW_hubs=5-k-int(blocked)
            # Direct feasibility: at most q HIGH friends and this many LOW
            # hub friends leave at least this many of seven friends in LOW S.
            sat_friends=7-q-possible_LOW_hubs
            if sat_friends<0:sat_friends=0
            if c['N'][a]-1>=sat_friends:neighbors.add(a)
        available.append(neighbors)
    # Checking full groups suffices: removing only some of an identical
    # group leaves its neighborhood unchanged and lowers the demand.
    for chosen in it.product((0,1),repeat=len(groups)):
        required=sum(n for flag,(_,n) in zip(chosen,groups) if flag)
        union=set().union(*(neighbors for flag,neighbors in zip(chosen,available) if flag))
        if required>sum(capacities[a] for a in union):return False
    return True

def scalar_cases():
    out=[]
    for X,tau,Q in it.product(range(8),range(4),range(16)):
        if 4+2*X+4*tau+Q<=15:
            out.append(dict(T=2,X=X,tau=tau,N5=0,Q=Q,E=15-2*tau-Q,K=4+2*tau+Q+2*X,margin_budget=3*(11-2*X-4*tau-Q)))
    return out

def prior_certificate(types,v,o):
    cut=o.direct_capacity(types,v)
    if cut['reason']!='OPEN':return dict(reason='FROZEN_ENDPOINT_RADIUS_OR_CLOSURE',cut=cut)
    vertices=[]
    for t,n in zip(types,v):
        vertices.extend(dict(unit=t[0]==0,eligible=t[3],degree=t[4]-t[1],one=t[5],root=t[1]==0,B=t==BTYPE,k=t[1]) for _ in range(n))
    units=[x for x in vertices if x['unit']]
    A=[x for x in units if not x['eligible']];V=[x for x in units if x['eligible']]
    C=[x for x in vertices if not x['unit'] and not x['eligible']]
    eligible=[x for x in vertices if x['eligible']]
    R=sum(x['root'] for x in units);DA=sum(x['degree'] for x in A);DV=sum(x['degree'] for x in V)
    bound=sum(min(x['degree'],len(A)-1) for x in A);bound-=bound%2
    C1=sum(x['one'] for x in C);required=DV+max(R,DA-bound)
    if R and eligible and C1<required:return dict(reason='9538_ROOT_ENDPOINT_C1',R=R,D_A=DA,D_V=DV,I_even=bound,C1=C1,required=required)
    b=sum(x['B'] for x in vertices)
    if b>2:return dict(reason='9697_ACTUAL_B2_CAP',B_count=b)
    return dict(reason='OPEN',K=sum(x['k'] for x in vertices),B_count=b)
