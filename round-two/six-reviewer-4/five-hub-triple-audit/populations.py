"""Uniform factor DAG over every row type; exact support charges and guards."""
import functools
import time
from collections import Counter
from rows import require

def scalar_cases():
    out = []
    # This bound is capacity at N5=0, not the conditional exceptional surcharge.
    for t in range(3, 8):
        for x in range(5):
            for tau in range(3):
                for q in range(10):
                    e = 17 - t - 2*tau - q
                    k = 19 - e + 2*x
                    slack = 15 - 2*t - 2*x - 4*tau - q
                    if e >= 0 and k >= 0 and slack >= 0:
                        out.append((t, x, tau, q, e, k, 3*slack))
    return sorted(out)

def inventories(types, case, n_rows=13):
    t, x, tau, q, e, k, margin = case
    charges = [(r[0], r[1], r[2], r[8], r[9], r[7]) for r in types]
    target = (e, k, q, 2*x, 0, margin)
    # Types exceeding nonnegative target budgets can only have multiplicity zero.
    chosen = [i for i, c in enumerate(charges) if all(a <= b for a,b in zip(c,target))]
    chosen.sort(key=lambda i: (charges[i][2], charges[i][3], charges[i][5], charges[i][0], charges[i][1]), reverse=True)
    cs = [charges[i] for i in chosen]
    minima, maxima = [], []
    for j in range(len(cs)):
        minima.append(tuple(min(c[d] for c in cs[j:]) for d in range(6)))
        maxima.append(tuple(max(c[d] for c in cs[j:]) for d in range(6)))
    start = time.monotonic()
    states = 0
    @functools.lru_cache(None)
    def count(j, n, rem):
        nonlocal states
        states += 1
        require(states <= 100000 and time.monotonic()-start <= 10, 'INCOMPLETE branch guard')
        if n == 0:
            return int(all(a == 0 for a in rem[:5]) and rem[5] >= 0)
        if j == len(cs):
            return 0
        if any(rem[d] < n*minima[j][d] for d in range(6)):
            return 0
        if any(rem[d] > n*maxima[j][d] for d in range(5)):
            return 0
        c = cs[j]
        limit = min([n] + [a//b for a,b in zip(rem,c) if b])
        return sum(count(j+1,n-v,tuple(a-v*b for a,b in zip(rem,c))) for v in range(limit+1))
    total = count(0,n_rows,target)
    result = []
    vector = [0]*len(types)
    def expand(j, n, rem):
        if n == 0:
            require(all(a == 0 for a in rem[:5]), 'terminal totals')
            result.append(tuple(vector))
            return
        c = cs[j]
        limit = min([n] + [a//b for a,b in zip(rem,c) if b])
        for v in range(limit+1):
            next_rem = tuple(a-v*b for a,b in zip(rem,c))
            if count(j+1,n-v,next_rem):
                vector[chosen[j]] = v
                expand(j+1,n-v,next_rem)
        vector[chosen[j]] = 0
    if total:
        expand(0,n_rows,target)
    require(len(result) == total == len(set(result)), 'DAG expansion/uniqueness')
    for v in result:
        require(sum(v)==n_rows and all(type(a) is int and a >= 0 for a in v), 'population')
        totals = tuple(sum(v[i]*charges[i][d] for i in range(len(types))) for d in range(6))
        require(totals[:5]==target[:5] and totals[5]<=target[5], 'full exact totals')
    return sorted(result), states

def certificate(types, vector):
    vertices = [r for r,n in zip(types,vector) for _ in range(n)]
    unit = [r for r in vertices if r[0]==0]
    a = [r for r in unit if not r[3]]
    v = [r for r in unit if r[3]]
    c = [r for r in vertices if r[0]>0 and not r[3]]
    b = [r for r in vertices if r[0]>0 and r[3]]
    degree = lambda r: r[4]-r[1]
    du = sum(map(degree,unit))
    da = sum(map(degree,a))
    dv = sum(map(degree,v))
    internal = sum(min(degree(r),len(a)-1) for r in a)
    c1,c2 = sum(r[5] for r in c),sum(r[8] for r in c)
    b2 = sum(r[8] for r in b)
    roots = sum(r[1]==0 for r in unit)
    closure_root = any(r[1]==0 for r in unit+c)
    exceptional_b = sum(r[3] and r[1]==1 and r[10]==2 for r in vertices)
    if du > internal+c1:
        verdict = 'unit'
    elif roots and b and c1+c2 < roots+len(b):
        verdict = 'crossing'
    elif du==internal+c1 and b and (c2==0 or b2==0) and closure_root:
        verdict = 'closure'
    elif roots and v+b and c1 < dv+max(roots,da-2*(internal//2)):
        verdict = 'root_endpoint'
    elif exceptional_b > 2:
        verdict = 'B2'
    else:
        verdict = 'joint_column'
    return {'verdict':verdict,'D_U':du,'D_A':da,'D_V':dv,'I':internal,
            'C1':c1,'C2':c2,'B2_support':b2,'roots':roots,'closure_root':closure_root,
            'eligible_nonunits':len(b),'exceptional_B':exceptional_b}

def census(types):
    case_records, all_vectors = [], []
    histogram = Counter()
    for case in scalar_cases():
        vectors, states = inventories(types,case)
        checks = [(v,certificate(types,v)) for v in vectors]
        for _, c in checks:
            histogram[c['verdict']]+=1
        case_records.append({'case':case,'count':len(vectors),'states':states})
        all_vectors.extend((case,v,c) for v,c in checks)
    return case_records,all_vectors,dict(sorted(histogram.items()))
