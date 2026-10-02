"""Complete five-word cyclic orbits for the fourteen involution-power types.

Literal orbit enumeration is cross-checked against fixed-subset coefficient
arithmetic. Only internal incompatibility removes an orbit. No code search.
"""
from collections import Counter
from itertools import combinations
from math import gcd
import bridge
from core import image,mask,require,digest

def fixed_subsets(parts,power):
    polynomial=[1,0,0,0,0,0]
    for length in parts:
        multiplicity=gcd(length,power);size=length//multiplicity
        for _ in range(multiplicity):
            for degree in range(5,size-1,-1):polynomial[degree]+=polynomial[degree-size]
    return polynomial[5]

def audit():
    universe={mask(q) for q in combinations(range(18),5)}
    require(len(universe)==8568,'whole five-subset universe')
    records=[]
    for case in bridge.check()['two_fixed_power_types']:
        parts=case['cycles'];order=case['order'];g=bridge.literal_power(parts,1)
        remaining=set(universe);orbits=[];eligible=[]
        while remaining:
            root=min(remaining);word=root;orbit=[]
            while not orbit or word!=root:
                require(word in remaining and word not in orbit,'orbit left complete universe')
                orbit.append(word);word=image(word,g)
                require(len(orbit)<=order,'cyclic closure guard')
            remaining-=set(orbit);orbit=tuple(sorted(orbit));orbits.append(orbit)
            if all((a&b).bit_count()<=2 for a,b in combinations(orbit,2)):eligible.append(orbit)
        counts=Counter(map(len,orbits));allowed=Counter(map(len,eligible))
        require(sum(d*n for d,n in counts.items())==8568,'all word-orbit coverage')
        exact={}
        for d in range(1,order+1):
            if order%d:continue
            total=fixed_subsets(parts,d)
            require(total==sum(e*n for e,n in counts.items() if d%e==0),'literal/coefficient fixed-subset discrepancy')
            numerator=total-sum(e*n for e,n in exact.items() if d%e==0)
            require(numerator>=0 and numerator%d==0,'exact orbit count integrality')
            exact[d]=numerator//d
        require({d:n for d,n in exact.items() if n}==dict(counts),'whole orbit histogram coefficient discrepancy')
        divisor=gcd(*allowed) if allowed else 1
        words=tuple(sorted(w for orbit in eligible for w in orbit))
        capacity=len(words)
        bound=min(69//divisor*divisor,capacity)
        exact_union=None
        if capacity<=70 and all((a&b).bit_count()<=2 for a,b in combinations(words,2)):
            require({image(w,g) for w in words}==set(words),'small positive union closure')
            exact_union={'maximum':capacity,'word_masks':words,'generator':g}
            require(capacity<=bound,'small union exceeds derived bound')
        records.append({'cycles':parts,'order':order,'all_orbit_histogram':sorted(counts.items()),
                        'internally_compatible_histogram':sorted(allowed.items()),
                        'all_orbits_sha256':digest(orbits),'eligible_orbits_sha256':digest(eligible),
                        'eligible_words':capacity,'word_count_divisor':divisor,
                        'upper_bound':bound,'exact_small_union':exact_union})
    return {'status':'PASS_FULL_CYCLIC_WORD_ORBIT_CENSUS','cycle_types':14,
            'five_words_per_type':8568,'records':records,'records_sha256':digest(records)}

if __name__=='__main__':
    import json
    print(json.dumps(audit(),sort_keys=True))
