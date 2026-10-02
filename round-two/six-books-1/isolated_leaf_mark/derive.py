"""Exact row producer for the isolated-mark fixed-leaf obstruction.

No external corpus, solver, graph catalogue or shared checker implementation.
"""
from collections import Counter
from itertools import combinations,product,permutations,combinations_with_replacement
from pathlib import Path
import hashlib,json,time

start=time.monotonic()
MIN=(2,2,1,1,1,1)
own=(40,20)
cycle=((0,4),(4,3),(3,1),(1,2),(2,5),(5,0))
def mask(s):return sum(1<<i for i in s)
five=tuple(mask(s) for s in combinations(range(8),5))
four=tuple(mask(s) for s in combinations(range(6),4))
budgets={}
for k in product(range(3),repeat=6):
    if sum(k)!=3:continue
    good=[]
    for beta in range(6):
        target=tuple(2-k[i]-int(i==beta) for i in range(6))
        if min(target)<0:continue
        for r0 in four:
            for r1 in four:
                if tuple(int(bool(r0&(1<<i)))+int(bool(r1&(1<<i))) for i in range(6))==target:
                    good.append((beta,r0,r1))
    budgets[k]=good

def frame(item):
    word,beta,r0,r1,sy0,sy1=item
    c=tuple((word>>(3*i))&7 for i in range(8))
    r=[0]*16
    def edge(i,j):r[i]|=1<<j;r[j]|=1<<i
    for z in (1,2,*range(3,11)):edge(0,z)
    for z in (2,11,12):edge(1,z)
    for z in (*range(9,16),):edge(2,z)
    for i,j in cycle:edge(3+i,3+j)
    for s in range(2):
        for i in range(6):
            if own[s]&(1<<i):edge(9+s,3+i)
            if (r0,r1)[s]&(1<<i):edge(11+s,3+i)
    for i,z in enumerate(range(3,11)):
        for t in range(3):
            if c[i]&(1<<t):edge(z,13+t)
    for s in range(2):
        for t in range(3):
            if (sy0,sy1)[s]&(1<<t):edge(11+s,13+t)
    q=(0,6,0,*(3+int(i==beta) for i in range(6)),4,4,2,2,
       *(4-int(bool(sy0&(1<<t)))-int(bool(sy1&(1<<t))) for t in range(3)))
    if tuple(r[i].bit_count()+q[i] for i in range(16)) != (10,10,9,*([10]*13)):
        raise ValueError('fixed degree budget correspondence failed')
    return r,q

def accept(item):
    r,q=frame(item)
    for i in range(16):
        for j in range(i+1,16):
            if (r[i]&r[j]).bit_count()+max(0,q[i]+q[j]-6) > (3 if r[i]&(1<<j) else 6-int(i==2)-int(j==2)):
                return False
    return True

counts=Counter();kept=[]
for rows in product(five,repeat=3):
    counts['row_triples']+=1
    c=tuple(sum(int(bool(rows[t]&(1<<i)))<<t for t in range(3)) for i in range(8))
    if any(c[i].bit_count()<MIN[i] for i in range(6)) or any(c[i].bit_count()!=2 for i in (6,7)):
        continue
    counts['basic_X']+=1
    word=sum(z<<(3*i) for i,z in enumerate(c))
    k=tuple(c[i].bit_count()-MIN[i] for i in range(6))
    if any((c[i]&c[j]).bit_count()>min(2,k[i]+k[j]) for i,j in cycle):continue
    if any((c[6+s]&c[i]).bit_count()>min(2,1+k[i])
           for s in range(2) for i in range(6) if own[s]&(1<<i)):continue
    counts['early_X_pages']+=1
    for beta,r0,r1 in budgets[k]:
        counts['budget_choices']+=1
        if any((c[6+s]&c[i]).bit_count()+int(i==beta)>1
               for s in range(2) for i in range(6) if own[s]&(1<<i)):continue
        if any((c[i]&c[j]).bit_count()+int(bool(r0&(1<<i)) and bool(r0&(1<<j)))
               +int(bool(r1&(1<<i)) and bool(r1&(1<<j)))+int(i==beta)+int(j==beta)>2
               for i,j in cycle):continue
        counts['early_budget_pages']+=1
        for sy0,sy1 in product((3,5,6),repeat=2):
            if any(sum(int(bool(z&(1<<t))) for z in (c[6],c[7],sy0,sy1))>3 for t in range(3)):
                continue
            counts['special_cores']+=1
            item=(word,beta,r0,r1,sy0,sy1)
            if accept(item):kept.append(item)
    if time.monotonic()-start>45:raise RuntimeError('fixed45s guard; missing cases imply no theorem')
kept.sort()
x_counts=dict(counts)
edge_set = {tuple(sorted(e)) for e in ((0,4),(4,3),(3,1),(1,2),(2,5),(5,0))}
own = (40,20)
def perm_mask(mask,p):
    return sum(bool(mask & (1<<i)) << p[i] for i in range(len(p)))
group = []
for p in permutations(range(6)):
    if {tuple(sorted((p[i],p[j]))) for i,j in edge_set} != edge_set:
        continue
    moved = tuple(perm_mask(m,p) for m in own)
    for sp in permutations(range(2)):
        if all(moved[i]==own[sp[i]] for i in range(2)):
            group.append((p,sp))
ts = tuple(permutations(range(3)))
ys = ((0,1),(1,0))
def orbit(item):
    word,beta,r0,r1,s0,s1 = item
    old = tuple((word >> (3*i)) & 7 for i in range(8))
    for p,sp in group:
        for tp in ts:
            c = [0]*8
            for i in range(6):c[p[i]] = perm_mask(old[i],tp)
            for i in range(2):c[6+sp[i]] = perm_mask(old[6+i],tp)
            for yp in ys:
                r = [0,0];s=[0,0]
                for i,z in enumerate((r0,r1)):r[yp[i]]=perm_mask(z,p)
                for i,z in enumerate((s0,s1)):s[yp[i]]=perm_mask(z,tp)
                yield (sum(z << (3*i) for i,z in enumerate(c)),p[beta],*r,*s)
domain=set(kept)
representatives=[];covered=set()
for item in kept:
    if item in covered:continue
    images=set(orbit(item))
    if not images<=domain:raise ValueError("invalid orbit")
    covered.update(images);representatives.append((min(images),len(images)))
if covered!=domain:raise ValueError("incomplete orbit expansion")
representatives.sort()
F=(0,1,2,9,10,11,12,13,14,15)
own=(40,20);cycle=((0,4),(4,3),(3,1),(1,2),(2,5),(5,0))
def mask(s):return sum(1<<i for i in s)
two=tuple(sorted(mask(s) for s in combinations(range(6),2)))
four=tuple(sorted(mask(s) for s in combinations(range(6),4)))
def frame22(rep,y,syy,sxy):
    word,beta,syx0,syx1,sy0,sy1=rep
    c=tuple((word>>(3*i))&7 for i in range(8));r=[0]*22
    def edge(i,j):r[i]|=1<<j;r[j]|=1<<i
    for z in (1,2,*range(3,11)):edge(0,z)
    for z in (2,11,12,*range(16,22)):edge(1,z)
    for z in range(9,16):edge(2,z)
    for i,j in cycle:edge(3+i,3+j)
    for s in range(2):
        for i in range(6):
            if own[s]&(1<<i):edge(9+s,3+i)
            if (syx0,syx1)[s]&(1<<i):edge(11+s,3+i)
            if syy[s]&(1<<i):edge(11+s,16+i)
            if sxy[s]&(1<<i):edge(9+s,16+i)
    for i,z in enumerate(range(3,11)):
        for t in range(3):
            if c[i]&(1<<t):edge(z,13+t)
    for s in range(2):
        for t in range(3):
            if (sy0,sy1)[s]&(1<<t):edge(11+s,13+t)
    for i in range(6):
        for t in range(3):
            if y[i]&(1<<t):edge(16+i,13+t)
    return r

def pair_bad(ri,rj,i,j):
    if ri&(1<<j):return (ri&rj).bit_count()>3
    return sum(k!=i and k!=j and not ri&(1<<k) and not rj&(1<<k) for k in range(22))>6

results=[];obstructions=[];tot=Counter()
for rid,(rep,orbit_size) in enumerate(representatives):
    w,beta,rx0,rx1,st0,st1=rep
    xc=tuple((w>>(3*i))&7 for i in range(8))
    tx=tuple(sum(bool(z&(1<<t))<<i for i,z in enumerate(xc[:6])) for t in range(3))
    y_types=[]
    for y in combinations_with_replacement(range(1,8),6):
        if all(sum(bool(z&(1<<t)) for z in y)+int(bool(st0&(1<<t)))+int(bool(st1&(1<<t)))==4 for t in range(3)):
            y_types.append(y)
    counts=Counter();hist=Counter()
    for y in y_types:
        counts['TY_types']+=1
        ty=tuple(sum(bool(z&(1<<t))<<i for i,z in enumerate(y)) for t in range(3))
        p_sx=[[],[]];p_sy=[[],[]]
        for s in range(2):
            for row in four:
                if all(1+(own[s]&tx[t]).bit_count()+(row&ty[t]).bit_count()
                       <=(3 if xc[6+s]&(1<<t) else 6) for t in range(3)):
                    p_sx[s].append(row)
            for row in two:
                if all(1+((rx0,rx1)[s]&tx[t]).bit_count()+(row&ty[t]).bit_count()
                       <=(3 if (st0,st1)[s]&(1<<t) else 6) for t in range(3)):
                    p_sy[s].append(row)
        for r0 in p_sy[0]:
            for r1 in p_sy[1]:
                h=tuple(4-y[i].bit_count()-int(bool(r0&(1<<i)))-int(bool(r1&(1<<i))) for i in range(6))
                if min(h)<0:continue
                for z0 in p_sx[0]:
                    for z1 in p_sx[1]:
                        counts['candidate_frames']+=1
                        r=frame22(rep,y,(r0,r1),(z0,z1))
                        if any(r[f].bit_count() != (9 if f==2 else 10) for f in F):
                            raise ValueError('fixed global degrees not reproduced')
                        if any(pair_bad(r[i],r[j],i,j) for ix,i in enumerate(F) for j in F[ix+1:]):continue
                        counts['fixed_spines']+=1
                        rejected_row=None
                        for i in range(6):
                            failures=[];good=[]
                            candidates=sorted(mask(js) for js in combinations(range(6),3+int(i==beta)))
                            for row in candidates:
                                ri=r[3+i]|sum(1<<(16+j) for j in range(6) if row&(1<<j))
                                if ri.bit_count()!=10:raise ValueError('X global degree not reproduced')
                                for f in F:
                                    if pair_bad(ri,r[f],3+i,f):
                                        red=int(bool(ri&(1<<f)))
                                        pages=(ri&r[f]).bit_count() if red else sum(k!=3+i and k!=f and not ri&(1<<k) and not r[f]&(1<<k) for k in range(22))
                                        failures.append([row,f,red,pages]);break
                                else:good.append(row)
                            if not good:
                                rejected_row={'rep':rid,'Y_columns':list(y),'SY_own_rows':[r0,r1],
                                              'SX_cross_rows':[z0,z1],'empty_X':i,'failures':failures}
                                break
                        if rejected_row is None:raise ValueError('unexcluded fixed-spine frame; no theorem')
                        obstructions.append(rejected_row);counts['empty_X_row']+=1
                        hist[rejected_row['empty_X']]+=1
    results.append({'rep':rid,'counts':dict(counts),'first_empty_X':dict(hist)})
    tot.update(counts)
    if time.monotonic()-start>45:raise RuntimeError('fixed45s guard; incomplete enumeration proves nothing')

record={'schema':1,'agent':'six-books-1','role':'researcher',
        'scope':'fixed one-nine leaf, E<=108, all nine N(a) vertices global10; finite fixed-spine obstruction, no global max/rootlessness/catalogue',
        'coordinates':['u','v','a',*[f'X{i}' for i in range(6)],'SX0','SX1','SY0','SY1','T0','T1','T2',*[f'Y{i}' for i in range(6)]],
        'outside_pair_controls':{'orders':[6,8],'subset_pair_trials':[4096,65536],'agrees_with_pigeonhole':True},
        'x_counts':x_counts,'x_domain_count':len(domain),
        'x_domain_sha256':hashlib.sha256(json.dumps(kept,separators=(',',':')).encode()).hexdigest(),
        'ordinary_symmetries':[[list(p),list(sp)] for p,sp in group],
        'subgroup_size':len(group)*len(ts)*len(ys),
        'orbits':[[list(rep),n] for rep,n in representatives],
        'Y_counts':dict(tot),'per_rep':results,
        'obstructions':sorted(obstructions,key=lambda x:(x['rep'],x['Y_columns'],x['SY_own_rows'],x['SX_cross_rows']))}
print(json.dumps(record,sort_keys=True,separators=(',',':')))
