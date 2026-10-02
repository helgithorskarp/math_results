"""Independent labeled incidence, exception matrix and MITM star coverage.

No author executable or certificate import. Low points are physical0..3;
high points are physical4..21, with logical masks0..17 in stored stars.
"""
from collections import defaultdict
from itertools import combinations, product
from common import require, digest, ALL22

PAIR_TYPES = tuple(sum(1 << p for p in q) for q in combinations(range(4),2))


def profiles():
    result = []
    # First enumerate every bounded labeled pair-count vector from actual
    # degree and low-blue page constraints, not r/s/t substitutions.
    for counts in product(range(5),repeat=6):
        low_degree = [int(p in (0,1))+int(p in (0,1,2))+int(p in (0,1,3))+
                      sum(n for n,t in zip(counts,PAIR_TYPES) if t >> p & 1) for p in range(4)]
        if low_degree != [9]*4 or sum(counts) != 14:
            continue
        if any(n+int(t & 7 == t)+int(t & 11 == t)>4 for n,t in zip(counts,PAIR_TYPES)):
            continue
        types = (1,2,7,11)+tuple(t for t,n in zip(PAIR_TYPES,counts) for _ in range(n))
        require(len(types) == 18,'physical high population')
        low = tuple(sum(1 << x for x,t in enumerate(types) if t >> i & 1) for i in range(4))
        groups = {t:tuple(x for x,v in enumerate(types) if v == t) for t in sorted(set(types))}
        result.append({'pair_counts':counts,'rst':(counts[0],counts[1],counts[2]),
                       'types':types,'low_masks':low,'groups':groups})
    require([p['rst'] for p in result] == [(0,3,3),(1,2,3),(1,3,2),(2,1,3),(2,2,2),(2,3,1)],
            'complete labeled six-profile census')
    return result


def exceptions(profile):
    types,low,groups = profile['types'],profile['low_masks'],profile['groups']
    actual = tuple(tuple(x for x in range(18) if low[i] >> x & 1) for i in range(4))
    canonical = set(); raw_good = 0
    for chosen in product(*actual):
        if not all(bool(types[chosen[i]] >> j & 1) == bool(types[chosen[j]] >> i & 1)
                   for i in range(4) for j in range(i)):
            continue
        raw_good += 1; labels = {}; per_type = defaultdict(list); normalized = []
        for x in chosen:
            t = types[x]
            if x not in labels:
                labels[x] = groups[t][len(per_type[t])]; per_type[t].append(x)
            normalized.append(labels[x])
        canonical.add(tuple(normalized))
    require(len(set(product(*actual))) == 6561,'all actual exception assignments')
    return tuple(sorted(canonical)),raw_good


def half_subsets(vertices,types):
    result = [(0,(0,0,0,0,0))]
    for v in vertices:
        step = (1,)+tuple(int(types[v] >> i & 1) for i in range(4))
        result += [(mask | 1 << v,tuple(a+b for a,b in zip(vector,step))) for mask,vector in result]
    require(len(result) == 1 << len(vertices),'complete binary half population')
    return result


def stars(profile,exception,center):
    types,low = profile['types'],profile['low_masks']; own = types[center]
    available = tuple(x for x in range(18) if x != center)
    left = half_subsets(available[:8],types); right = half_subsets(available[8:],types)
    lookup = defaultdict(list)
    for mask,vector in right: lookup[vector].append(mask)
    demand = (10-own.bit_count(),)+tuple((3-int(exception[i] == center)) if own >> i & 1 else 5 for i in range(4))
    result = []
    for mask,vector in left:
        remainder = tuple(a-b for a,b in zip(demand,vector))
        if min(remainder) < 0: continue
        for tail in lookup.get(remainder,()):result.append(mask | tail)
    result.sort(); require(len(result) == len(set(result)),'duplicate MITM star')
    for mask in result:
        physical = (mask << 4)|own
        require(physical.bit_count() == 10 and not physical >> (center+4) & 1,'full prescribed high row')
        blue_high = ALL22 ^ physical ^ (1 << (center+4))
        for i in range(4):
            red_low = low[i] << 4; blue_low = ALL22 ^ red_low ^ (1 << i)
            if own >> i & 1:
                require((physical & red_low).bit_count() == 3-int(exception[i] == center),
                        'literal mixed red page equality')
            else:
                require((blue_high & blue_low).bit_count() == 6,'literal mixed blue page equality')
    return tuple(result)


def initial(profile,exception):
    return tuple(stars(profile,exception,x) for x in range(18))
