"""Independent physical-page projection; no target code or frozen record read."""
from itertools import combinations, product
from collections import Counter
import json, hashlib

def require(ok, message):
    if not ok:
        raise ValueError(message)

def edge(rows, i, j):
    rows[i] |= 1 << j
    rows[j] |= 1 << i

def mask(points):
    return sum(1 << x for x in points)

def pages(rows, i, j, n, red):
    if red:
        return (rows[i] & rows[j]).bit_count()
    universe = (1 << n) - 1
    return ((universe ^ rows[i] ^ (1 << i)) &
            (universe ^ rows[j] ^ (1 << j))).bit_count()

def fixed():
    # u,v,a,X0..5,SX0,SX1,T0..2. Eight unlisted Y points.
    r = [0] * 14
    for j in range(1, 11):
        edge(r, 0, j)
    edge(r, 1, 2)
    for j in [9, 10, 11, 12, 13]:
        edge(r, 2, j)
    cycle = [0, 4, 3, 1, 2, 5]
    for x, y in zip(cycle, cycle[1:] + cycle[:1]):
        edge(r, 3+x, 3+y)
    for s, own in [(9, [3, 5]), (10, [2, 4])]:
        for x in own:
            edge(r, s, 3+x)
        for t in [12, 13]:
            edge(r, s, t)
    return r

def necessary(r, degrees):
    outside = [d-v.bit_count() for d, v in zip(degrees, r)]
    if any(x < 0 or x > 8 for x in outside):
        return False
    for i, j in combinations(range(14), 2):
        red = bool(r[i] & (1 << j))
        count = pages(r, i, j, 14, red)
        minimum = max(0, outside[i]+outside[j]-8) if red else max(0, 8-outside[i]-outside[j])
        if count + minimum > (3 if red else 6):
            return False
    return True

def domain():
    answer = []
    tested = 0
    minrank = [2, 2, 1, 1, 1, 1]
    by_size = {s:list(combinations(range(6),s)) for s in range(7)}
    for ranks in product(range(7),repeat=3):
        lows = [5-ranks[0],3-ranks[1],3-ranks[2]]
        for rows in product(*(by_size[k] for k in ranks)):
            tested += 1
            columns = [sum(1 << t for t in range(3) if x in rows[t]) for x in range(6)]
            if any(c.bit_count() < k for c, k in zip(columns, minrank)):
                continue
            r = fixed()
            for t, xs in enumerate(rows):
                for x in xs:
                    edge(r, 11+t, 3+x)
            deg = [10, 10, 9] + [10]*8 + [10-x for x in lows]
            if necessary(r, deg):
                answer.append({'lows':list(lows), 'T_rows':[list(x) for x in rows],
                               'columns':columns, 'degrees':deg, 'red_rows':r})
    return tested, answer

def full_endpoints(d, A, B, Z1, Z2):
    # Add SY0,SY1,Y0..5. All four endpoint rows become complete.
    r = d['red_rows'][:] + [0]*8
    for sy, ts in [(14,[11,13]),(15,[11,12])]:
        for p in [1,2]+ts:
            edge(r, sy, p)
    for s, ys in [(9,A),(10,B),(12,Z1),(13,Z2)]:
        for y in ys:
            edge(r,s,16+y)
    require(all(r[i].bit_count()==d['degrees'][i] for i in [9,10,12,13]), 'endpoint rank')
    return r

def finish(d):
    fours = list(combinations(range(6),4))
    threes = list(combinations(range(6),3))
    frames = 0
    survivors = 0
    pairtests = 0
    own = [{3,5},{2,4}]
    overlap = [[len(set(row)&s) for s in own] for row in d['T_rows'][1:]]
    # No SY cross row, ordinary X--Y edge, or ordinary Y edge is enumerated.
    for A,B in product(fours, repeat=2):
        if len(set(A)&set(B)) != 2:
            continue
        frames += 1
        choices = []
        for pair in overlap:
            choices.append([Z for Z in threes if len(set(Z)&set(A)) <= 2-pair[0]
                            and len(set(Z)&set(B)) <= 2-pair[1]])
        for Z1,Z2 in product(*choices):
            r = full_endpoints(d,A,B,Z1,Z2)
            pairtests += 1
            require(pages(r,9,10,22,False)==6, 'SX blue frame')
            require(all(pages(r,s,t,22,True)<=3 for s,t in product([9,10],[12,13])), 'SX--T red')
            if pages(r,12,13,22,False)<=6:
                survivors += 1
    return {'frames':frames,'pairtests':pairtests,'survivors':survivors,'overlap':overlap}

def canonical(value):
    return json.dumps(value,sort_keys=True,separators=(',',':'))

def result(D, tested, finishes):
    ordered=sorted(D,key=lambda d:tuple(d['columns']))
    groups=Counter()
    remaining=[]
    for d,f in zip(D,finishes):
        p=f['overlap']
        kind='both-own-pairs' if any(min(x)>0 for x in p) else 'two-in-one-own-pair' if any(max(x)>1 for x in p) else 'remaining'
        groups[kind]+=1
        if kind=='remaining':
            require(all(len(row)==3 and {0,1}<=set(row) for row in d['T_rows'][1:]),'remaining ordinary finish')
            remaining.append(tuple(len(row) for row in d['T_rows']))
    require(all(f['survivors']==0 for f in finishes),'complete endpoint exclusion')
    return {'scope':'fixed full one-nine leaf; at most108 red edges; arbitrary outside degrees; X-repeated core',
        'tested_row_triples':tested,'projection_rows':len(D),
        'sorted_domain_sha256':hashlib.sha256(canonical(ordered).encode()).hexdigest(),
        'finish_groups':dict(sorted(groups.items())),
        'remaining_rank_counts':[[list(k),v] for k,v in sorted(Counter(remaining).items())],
        'SX_frames':sum(f['frames'] for f in finishes),
        'compatible_T_row_pairs':sum(f['pairtests'] for f in finishes),
        'endpoint_survivors':sum(f['survivors'] for f in finishes)}

def generate():
    tested,D=domain()
    finishes=[finish(d) for d in D]
    return result(D,tested,finishes),D,finishes

if __name__=='__main__':
    print(canonical(generate()[0]))
