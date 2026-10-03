"""Literal-set producer; star compiler extends the credited 9313 source."""
import argparse
from collections import Counter
import hashlib
import itertools
import json
import time
from pathlib import Path

PIN = 'c188200792c201bdb44ea1667a8a70255c4e40f04fee6c334c98ecfa650113e7'
POINTS = frozenset(range(17))
def require(test, message):
    if not test:
        raise ValueError(message)
def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':')).encode()
def digest(value):
    return hashlib.sha256(canonical(value)).hexdigest()

def compile_star(blocks, fi):
    Q = frozenset(frozenset(q) for q in blocks)
    require(len(Q) == len(blocks) == 20, 'twenty distinct quadruples required')
    require(all(len(q) == 4 and q <= POINTS for q in Q), 'invalid quadruple')
    rho = Counter(p for q in Q for p in q)
    owners = Counter(t for q in Q for t in itertools.combinations(sorted(q), 2))
    require(all(count == 1 for count in owners.values()), 'repeated point pair')
    delta = {p: 5-rho[p] for p in POINTS}
    require(min(delta.values()) >= 0 and sum(delta.values()) == 5, 'invalid deficits')
    high = frozenset(p for p in POINTS if delta[p])
    leave = frozenset(t for t in itertools.combinations(range(17), 2) if t not in owners)
    require(len(leave) == 16, 'sixteen leave edges required')
    low = POINTS-high
    require(all(sum(p in t for t in leave) == 1 for p in low), 'low leave degree')
    require(all(not set(t) <= low for t in leave), 'universal low-low prohibition')
    HH = frozenset(t for t in leave if set(t) <= high)
    require(len(HH) == len(high)-1, 'high leave count')
    isolated = frozenset(p for p in high if all(p not in t for t in HH))
    return dict(fixture=fi, delta=delta, high=high, HH=HH, isolated=isolated)

def rows_from_data(data):
    require(len(data['stars']) == len(data['groups']) == 23, 'complete23-star input required')
    rows = []
    for fi, blocks in enumerate(data['stars']):
        s = compile_star(blocks, fi)
        high = tuple(sorted(s['high']))
        for bits in range(1 << len(high)):
            B = frozenset(p for j,p in enumerate(high) if bits >> j & 1)
            h, k = len(high), len(B)
            e = 5-h
            q = sum(bool(set(t) & B) for t in s['HH'])
            eligible = bool(s['isolated'] & B)
            g1 = sum(s['delta'][p] == 1 for p in s['high']-B)
            sigma = sum(s['delta'][p]-1 for p in s['high']-B)
            w = sum(s['delta'][p] for p in B)
            require(e == w-k+sigma, 'weighted/support identity')
            psi = g1 if e == 0 and eligible else -g1 if e and not eligible else 0
            rows.append(dict(fixture=fi, hub_high=sorted(B), h=h, e=e, k=k, q=q,
                eligible=eligible, g1_S=g1, ss_excess=sigma, hub_weight=w,
                psi=psi, margin=psi-3*(k-e-q),
                ss_hist=[sum(s['delta'][p] == d for p in s['high']-B) for d in range(1,6)]))
    return sorted(rows, key=lambda r:(r['fixture'],r['hub_high']))

FIELDS=('e','k','q','eligible','h','g1_S','ss_excess','hub_weight','psi','margin','ss_hist')
def type_key(row):
    return tuple(tuple(row[f]) if f=='ss_hist' else row[f] for f in FIELDS)
def necessary_failures(vertices):
    fail=[]
    for i,row in enumerate(vertices):
        radius=0
        for colour,required in enumerate(row['ss_hist']):
            if not required:continue
            possible=[other['h']-other['k'] for j,other in enumerate(vertices) if j!=i
                      and other['ss_hist'][colour] and not((row['e']==0 and other['eligible'])
                           or(other['e']==0 and row['eligible']))]
            if len(possible)<required:fail.append('too_few_weighted_partners')
            radius+=sum(sorted(possible,reverse=True)[:required])
        if row['k']==0 and radius<13:fail.append('hub_complete_radius_two')
    if any(sum(row['ss_hist'][colour] for row in vertices)%2 for colour in range(5)):
        fail.append('odd_weight_layer')
    return sorted(set(fail))

def inventories(rows):
    keys=sorted({type_key(row) for row in rows if row['k']<=4})
    types=[dict(zip(FIELDS,key)) for key in keys]
    index={key:i for i,key in enumerate(keys)}
    branches=[]
    for Q in range(5):
        for T,X,tau in itertools.product(range(3),range(3),range(2)):
            cost=Q+2*T+2*X+4*tau
            if cost>4:continue
            E=12-Q-T-2*tau;K=20-E+2*X;budget=3*(4-cost)
            available=[row for row in types if row['q']<=Q and row['ss_excess']<=2*X and row['margin']<=budget]
            positive=[row for row in available if row['q']]
            chosen=[];nodes=0;started=time.monotonic()
            def guard():
                nonlocal nodes
                nodes+=1
                if nodes>100000 or time.monotonic()-started>10:
                    raise RuntimeError('INCOMPLETE fixed census guard; no mathematical absence')
            def select_positive(i,counts,leftq,e,k,sigma,margin):
                guard()
                if min(leftq,E-e,K-k,2*X-sigma,budget-margin)<0:return
                if i==len(positive):
                    if leftq==0:chosen.append(counts)
                    return
                row=positive[i];limit=leftq//row['q']
                for field,remaining in (('e',E-e),('k',K-k),('ss_excess',2*X-sigma),('margin',budget-margin)):
                    if row[field]:limit=min(limit,remaining//row[field])
                for c in range(limit+1):
                    select_positive(i+1,counts+[c],leftq-c*row['q'],e+c*row['e'],k+c*row['k'],sigma+c*row['ss_excess'],margin+c*row['margin'])
            select_positive(0,[],Q,0,0,0,0)
            raw=[]
            for pos in chosen:
                n=14-sum(pos);e=E-sum(c*r['e'] for c,r in zip(pos,positive))
                k=K-sum(c*r['k'] for c,r in zip(pos,positive))
                sigma=2*X-sum(c*r['ss_excess'] for c,r in zip(pos,positive))
                margin=budget-sum(c*r['margin'] for c,r in zip(pos,positive))
                if min(n,e,k,sigma,margin)<0:continue
                zero=[r for r in available if r['q']==0 and r['ss_excess']<=sigma and r['margin']<=margin]
                unit0=[i for i,r in enumerate(zero) if r['e']==0 and not r['eligible']]
                unit1=[i for i,r in enumerate(zero) if r['e']==0 and r['eligible']]
                require(len(unit0)==1 and zero[unit0[0]]['k']==0,'zero unit basis differs')
                require(len(unit1)<=1 and (not unit1 or zero[unit1[0]]['k']==1),'positive unit basis differs')
                mixed=[i for i,r in enumerate(zero) if r['e']>0]
                limits=[]
                for i in mixed:
                    row=zero[i];maximum=min(n,e//row['e'])
                    for field,cap in (('k',k),('ss_excess',sigma),('margin',margin)):
                        if row[field]:maximum=min(maximum,cap//row[field])
                    limits.append(range(maximum+1))
                for population in itertools.product(*limits):
                    guard()
                    if sum(c*zero[i]['e'] for i,c in zip(mixed,population))!=e:continue
                    if sum(c*zero[i]['ss_excess'] for i,c in zip(mixed,population))!=sigma:continue
                    u1=k-sum(c*zero[i]['k'] for i,c in zip(mixed,population));u0=n-sum(population)-u1
                    if min(u0,u1)<0 or (u1 and not unit1):continue
                    if sum(c*zero[i]['margin'] for i,c in zip(mixed,population))+u1>margin:continue
                    counts=[0]*len(zero)
                    for i,c in zip(mixed,population):counts[i]=c
                    counts[unit0[0]]=u0
                    if unit1:counts[unit1[0]]=u1
                    pairs=sorted((index[type_key(r)],c) for r,c in list(zip(positive,pos))+list(zip(zero,counts)) if c)
                    vertices=[types[i] for i,c in pairs for _ in range(c)]
                    raw.append(dict(population=pairs,failures=necessary_failures(vertices)))
            raw.sort(key=lambda r:r['population'])
            require(len({tuple(tuple(p) for p in r['population']) for r in raw})==len(raw),'duplicate population')
            branches.append(dict(Q=Q,T=T,X=X,tau=tau,E=E,K=K,margin_budget=budget,templates=raw))
    return dict(types=types,branches=branches)

def build(fixtures):
    raw=fixtures.read_bytes();require(hashlib.sha256(raw).hexdigest()==PIN,'credited fixture bytes')
    rows=rows_from_data(json.loads(raw))
    baseline=[{k:v for k,v in row.items() if k!='ss_hist'} for row in rows]
    require(digest(baseline)=='19205841cee4584466bac048f114d0d5f0db096b6861e45f34c94b9180087b16','all426 published row records differ')
    require(all(row['margin']>=0 for row in rows if row['k']<=4),'within-scope coefficient')
    return dict(rows=rows,inventory=inventories(rows))

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--fixtures',type=Path,default=Path(__file__).with_name('fixtures.json'))
    parser.add_argument('--out',type=Path,required=True)
    args=parser.parse_args();require(not args.out.exists(),'fresh output required')
    result=build(args.fixtures);args.out.write_text(json.dumps(result,sort_keys=True,separators=(',',':'))+'\n')
    print(json.dumps(dict(row_count=len(result['rows']),inventory_sha256=digest(result['inventory']))))
if __name__=='__main__':main()
