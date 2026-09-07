"""Transparent independent cycle-index count for the row-profile cover."""
from collections import Counter
import json
import normalize


def census():
    kinds=Counter()
    for image in normalize.linear_maps():
        seen={0};cycles=[]
        for x in range(1,16):
            if x in seen:continue
            length=0;y=x
            while y not in seen:
                seen.add(y);length+=1;y=image[y]
            cycles.append(length)
        kinds[tuple(sorted(cycles))]+=1
    records=[];sums=[0,0]
    for cycles,multiplicity in sorted(kinds.items()):
        poly=[1]+[0]*20
        for length in cycles:
            new=[0]*21
            for w,value in enumerate(poly):
                for digit in range(4):
                    if w+digit*length<=20:new[w+digit*length]+=value
            poly=new
        records.append({'cycles':list(cycles),'group_elements':multiplicity,
                        'fixed_weight19':poly[19],'fixed_weight20':poly[20]})
        for j in range(2):sums[j]+=multiplicity*poly[19+j]
    order=sum(kinds.values())
    if any(s%order for s in sums):raise ValueError('Burnside integrality')
    all_orbits=[s//order for s in sums]
    # A nonspanning profile has full support on one 3-dimensional hyperplane:
    # seven multiplicities initially 3, with deficit 2 or 1. Deficit 2 means
    # either one entry lowered twice or two entries lowered once. GL(3,2)
    # is transitive on points and on unordered pairs of distinct points.
    # The C++ checker also enumerates these profiles instead of using this fact.
    nonspanning=[2,1]
    return {'group_order':order,'cycle_types':records,'fixed_sums':sums,
            'all_profile_orbits':all_orbits,'nonspanning_orbits':nonspanning,
            'spanning_orbits':[a-b for a,b in zip(all_orbits,nonspanning)]}


if __name__=='__main__':print(json.dumps(census(),indent=2))
