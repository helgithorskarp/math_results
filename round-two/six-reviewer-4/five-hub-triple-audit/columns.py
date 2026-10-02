"""Enumerate labelled necessary allocations, not physical packings."""
from itertools import combinations
from rows import require

def compositions(mass, length, minimum=0, maximum=8):
    if length == 0:
        if mass == 0:
            yield ()
        return
    low = max(minimum, mass-maximum*(length-1))
    high = min(maximum,mass-minimum*(length-1))
    for first in range(low,high+1):
        for tail in compositions(mass-first,length-1,minimum,maximum):
            yield (first,)+tail

def accept(nsupport, heavy, k, require_heavy_support=True):
    require(len(nsupport)==len(heavy)==5, 'five named columns')
    require(all(type(x) is int for x in nsupport+heavy), 'integer columns')
    d = tuple(n+h for n,h in zip(nsupport,heavy))
    if not (sum(nsupport)==k and sum(heavy)==19-k): return False
    if not all(1<=n<=8 and 0<=h<=n for n,h in zip(nsupport,heavy)): return False
    if not all(x<=8 for x in d): return False
    if not all(d[a]+d[b]<=11 for a,b in combinations(range(5),2)): return False
    if not all(nsupport[a]>=4 and heavy[a]>=1 for a in (0,1)): return False
    if require_heavy_support and any(h>0 and n<3 for n,h in zip(nsupport,heavy)): return False
    return True

def allocations(k, require_heavy_support=True):
    out = []
    for n in compositions(k,5,1):
        for h in compositions(19-k,5):
            if accept(n,h,k,require_heavy_support):
                out.append((n,h,tuple(a+b for a,b in zip(n,h))))
    return out

def same_owner_necessary(d, n, multiplicity, ta):
    return (1<=d<=8 and 1<=n<=d and n>=4 and d>=n+multiplicity
            and (multiplicity==1 or n>=5)
            and 0<=ta<=6 and multiplicity*(8-n)<=19-3*d+2*ta)

def occupancy_profiles():
    profiles = []
    for d in range(1,9):
        for n in range(1,d+1):
            for b in range(1,n+1):
                for ta in range(7):
                    if same_owner_necessary(d,n,b,ta):
                        profiles.append((d,n,b,ta))
    require(not any(b>=3 for d,n,b,ta in profiles), 'three same-owner B impossible')
    require(all(2*ta>=d+1 for d,n,b,ta in profiles if b==2), 'double B local refinement')
    require(not any(b>=2 and ta<=3 for d,n,b,ta in profiles), 'low-Ta distinct owners')
    return profiles
