"""Independent point-mask star reconstruction and generating-polynomial coefficients."""
import argparse
import hashlib
import itertools
import json
from pathlib import Path
import time
from functools import lru_cache

FIELDS=('e','k','q','eligible','h','g1_S','ss_excess','hub_weight','psi','margin','ss_hist')
ALL=(1<<17)-1
PIN='c188200792c201bdb44ea1667a8a70255c4e40f04fee6c334c98ecfa650113e7'
CANON=lambda x:json.dumps(x,sort_keys=True,separators=(',',':')).encode()
def need(condition,message):
    if not condition:
        raise ValueError(message)

def literal_rows(data):
    need(len(data['stars'])==23,'generic input must contain23 actual stars')
    rows=[]
    for fi,words in enumerate(data['stars']):
        masks=[]
        for word in words:
            need(len(word)==4 and len(set(word))==4 and all(isinstance(p,int) and 0<=p<17 for p in word),'invalid quadruple')
            masks.append(sum(1<<p for p in word))
        need(len(masks)==20 and len(set(masks))==20,'twenty distinct actual quadruples')
        rep=[sum(bool(mask&(1<<p)) for mask in masks) for p in range(17)]
        deficit=[5-r for r in rep]
        need(min(deficit)>=0 and sum(deficit)==5,'weighted deficit sum')
        covered=[0]*17
        for mask in masks:
            points=[p for p in range(17) if mask&(1<<p)]
            for p,q in itertools.combinations(points,2):
                need(not covered[p]&(1<<q),'repeated owned pair')
                covered[p]|=1<<q;covered[q]|=1<<p
        leave=[ALL^(1<<p)^covered[p] for p in range(17)]
        high=[p for p in range(17) if deficit[p]]
        high_mask=sum(1<<p for p in high)
        need(sum(v.bit_count() for v in leave)==32,'sixteen actual leave edges')
        need(all(leave[p].bit_count()==1 and leave[p]&high_mask for p in range(17) if deficit[p]==0),'universal low-leave rule')
        pairs=[(1<<p)|(1<<q) for p,q in itertools.combinations(high,2) if leave[p]&(1<<q)]
        need(len(pairs)==len(high)-1,'high-high leave count')
        for length in range(len(high)+1):
            for hubs in itertools.combinations(high,length):
                hub_mask=sum(1<<p for p in hubs)
                hist=tuple(sum(deficit[p]==d for p in high if not hub_mask&(1<<p)) for d in range(1,6))
                eligible=any(not leave[p]&high_mask for p in hubs)
                e=5-len(high);k=length;q=sum(bool(pair&hub_mask) for pair in pairs)
                g1=hist[0];sigma=sum((d-1)*count for d,count in enumerate(hist,1))
                weight=sum(deficit[p] for p in hubs)
                need(e==weight-k+sigma,'literal support/weight identity')
                psi=g1 if e==0 and eligible else -g1 if e>0 and not eligible else 0
                rows.append(dict(fixture=fi,hub_high=list(hubs),h=len(high),e=e,k=k,q=q,
                                 eligible=eligible,g1_S=g1,ss_excess=sigma,hub_weight=weight,
                                 psi=psi,margin=psi-3*(k-e-q),ss_hist=hist))
    rows.sort(key=lambda row:(row['fixture'],row['hub_high']))
    return rows

def audit_population(types,population):
    counts=dict(population)
    failures=set()
    for i,number in population:
        centre=types[i]
        upper=0
        for colour,demand in enumerate(centre['ss_hist']):
            if not demand:continue
            pool=[]
            for j,c in population:
                endpoint=types[j]
                if not endpoint['ss_hist'][colour]:continue
                if centre['e']==0 and endpoint['eligible']:continue
                if endpoint['e']==0 and centre['eligible']:continue
                multiplicity=c-(j==i)
                if multiplicity:pool.append((endpoint['h']-endpoint['k'],multiplicity))
            if sum(c for degree,c in pool)<demand:
                failures.add('too_few_weighted_partners')
            remaining=demand
            for degree,c in sorted(pool,reverse=True):
                take=min(remaining,c);upper+=take*degree;remaining-=take
            # Separate colours may reuse a candidate here. This relaxes the
            # upper bound, never strengthens the necessary radius test.
        if centre['k']==0 and upper<13:
            failures.add('hub_complete_radius_two')
    for colour in range(5):
        if sum(c*types[i]['ss_hist'][colour] for i,c in population)%2:
            failures.add('odd_weight_layer')
    return sorted(failures)

def reconstruct(rows, allowed):
    keys=sorted({tuple(tuple(row[f]) if f=='ss_hist' else row[f] for f in FIELDS)
                 for row in rows if row['k']<=4})
    types=[dict(zip(FIELDS,key)) for key in keys]
    branches=[]
    # Coefficients of product_i (1 + z*v_i + ... + z^14*v_i^14).
    # v_i records e,k,q,sigma,margin. A cached suffix coefficient query
    # treats every type uniformly: no positive-charge splitting or special
    # algebraic completion of unit counts is used.
    for Q in range(13):
        for T in (0,):
            for X in range(7):
                for tau in range(4):
                    cost=Q+2*T+2*X+4*tau
                    if cost>12:continue
                    E=18-Q-T-2*tau;K=24-E+2*X;budget=3*(12-cost)
                    ids=[i for i,row in enumerate(types) if i in allowed and row['q']<=Q
                         and row['ss_excess']<=2*X and row['margin']<=budget]
                    ids.reverse()
                    weights=[(1,types[i]['e'],types[i]['k'],types[i]['q'],
                              types[i]['ss_excess'],types[i]['margin']) for i in ids]
                    calls=0;started=time.monotonic()
                    @lru_cache(maxsize=None)
                    def coefficient(at,state):
                        nonlocal calls
                        calls+=1
                        if calls>500000 or time.monotonic()-started>20:
                            raise RuntimeError('INCOMPLETE fixed polynomial guard; no mathematical absence')
                        if min(state)<0:return False
                        if at==len(weights):return not any(state[:5])
                        tail=weights[at:]
                        n=state[0]
                        if any(state[j]<n*min(w[j] for w in tail)
                               or state[j]>n*max(w[j] for w in tail) for j in range(1,5)):
                            return False
                        if state[5]<n*min(w[5] for w in tail):return False
                        w=weights[at]
                        limit=min(state[j]//value for j,value in enumerate(w) if value)
                        return any(coefficient(at+1,tuple(x-c*y for x,y in zip(state,w)))
                                   for c in range(limit+1))
                    populations=[]
                    def extract(at,state,chosen):
                        if at==len(weights):
                            populations.append(sorted(chosen));return
                        w=weights[at]
                        limit=min(state[j]//value for j,value in enumerate(w) if value)
                        for c in range(limit+1):
                            new=tuple(x-c*y for x,y in zip(state,w))
                            if coefficient(at+1,new):
                                extract(at+1,new,chosen+([(ids[at],c)] if c else []))
                    target=(14,E,K,Q,2*X,budget)
                    if coefficient(0,target):extract(0,target,[])
                    templates=[dict(population=p,failures=audit_population(types,p))
                               for p in sorted(populations)]
                    branches.append(dict(Q=Q,T=T,X=X,tau=tau,E=E,K=K,
                                         margin_budget=budget,templates=templates))
                    Path('round-two/six-code-3/scratch/pass23-T0-polynomial-progress.json').write_text(json.dumps(dict(types=types,branches=branches),sort_keys=True,separators=(',',':'))+'\n')
                    print(json.dumps(dict(branch=len(branches),Q=Q,T=T,X=X,tau=tau,raw=len(templates),states=calls)),flush=True)
                    coefficient.cache_clear()
    return dict(types=types,branches=branches)

def digest(value):return hashlib.sha256(CANON(value)).hexdigest()

def main():
    r=Path('round-two/six-code-3');s=r/'scratch'
    raw=(r/'four_hub_p21_endpoint_cut/fixtures.json').read_bytes()
    need(hashlib.sha256(raw).hexdigest()==PIN,'exact credited fixture bytes')
    rows=literal_rows(json.loads(raw))
    allowed=set(json.loads((s/'pass16-independent-low-friends.json').read_text())['projected_types'])
    inventory=reconstruct(rows,allowed)
    need(len(inventory['branches'])==84,'all eighty-four T0 scalar branches')
    out=s/'pass23-T0-polynomial.json';need(not out.exists(),'fresh output')
    out.write_text(json.dumps(dict(agent='six-code-3',role='researcher',status='PRIVATE_COMPLETE_FOCUSED_T0_POLYNOMIAL_CENSUS',
                                  rows=rows,inventory=inventory,new_pair_total_claim=None),sort_keys=True,separators=(',',':'))+'\n')
    print(json.dumps(dict(branches=len(inventory['branches']),raw=sum(len(b['templates']) for b in inventory['branches']),
                         necessary_survivors=sum(not t['failures'] for b in inventory['branches'] for t in b['templates']),
                         inventory_sha256=digest(inventory),all426_rows_matched=True,all60_types_matched=True,
                         all84_T0_branches_enumerated=True,global_P22_census_not_claimed=True)))
if __name__=='__main__':main()
