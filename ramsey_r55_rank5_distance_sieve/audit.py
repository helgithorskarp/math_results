"""Exact independent checks of strata, dependent distances and physical graphs."""
from collections import Counter
from copy import deepcopy
from fractions import Fraction
from itertools import combinations
from math import comb
import json
import random

import counts
from independent_marked import marked
from base_span import span_counts
from distance import (grouped_transfer, grouped_positive_transfer,
                      transfer, positive_transfer)
from base_model import PAIRS, INTERNAL
from model import classify, physical, selected_pairs, pair_distances
from extract import extract, clique
from verify import decode, verify


def need(ok,message):
    if not ok:raise ArithmeticError(message)


def rank(rows,width):
    a=[[(row >> j)&1 for j in range(width)] for row in rows]
    p=0
    for col in range(width):
        k=next((i for i in range(p,len(a)) if a[i][col]),None)
        if k is None:continue
        a[p],a[k]=a[k],a[p]
        for i in range(p+1,len(a)):
            if a[i][col]:a[i]=[x^y for x,y in zip(a[i],a[p])]
        p+=1
    return p


def arithmetic():
    a0=marked(range(1,32),5,20)
    a1=marked(range(1,32),5,19)
    la=marked(range(16,32),5,20)
    rows=[(20,False,a0),(19,False,a1),(20,True,la)]
    for length,affine,values in rows:
        need(values==counts.span_polynomial(length,5,affine),'marked word disagreement')
    b=span_counts(range(1,32),5,23,5)
    lb=span_counts(range(16,32),5,23,5)[23]
    for m in (21,22,23):
        need(b[m]==counts.prior.nonzero_span(m,5,5),'column word disagreement')
    need(lb==counts.prior.affine_span(23,5,5),'column affine disagreement')
    actual=counts.compute();observed=[]
    gl=31*30*28*24*16
    for j in range(11):
        raw=0
        for za in (0,1):
            aa=a0 if za==0 else a1
            for zb in (0,1,2):
                if za and zb:continue
                raw+=comb(20,za)*comb(23,zb)*(aa[j] if j<len(aa) else 0)*b[23-zb]
        low=31*16*la[j]*lb
        need(raw%gl==low%gl==0,'independent stratum quotient')
        row={'repeated_row_classes':j,'raw':raw//gl,
             'blue_rank_four':low//gl,'cross_matrices':(raw-low)//gl}
        need(row==actual['strata'][j],'complete stratum disagreement')
        observed.append(row)
    transfers=[]
    for p in range(11):
        q,states=grouped_positive_transfer(pairs=p)
        expected=actual['transfers'][p]
        need([q.numerator,q.denominator]==expected['keep_fraction'],'positive transfer disagreement')
        if p<=6:need(q==transfer(pairs=p),'ungrouped signed graph sum disagreement')
        if p<=4:need(q==positive_transfer(pairs=p),'ungrouped actual-block disagreement')
        need(expected['signed_states']<=2**p,'signed histogram state bound')
        bound=sum(comb(p+t,2*t) for t in range(p+1))
        need(states<=bound,'positive histogram state bound')
        transfers.append({'pairs':p,'keep_fraction':[q.numerator,q.denominator],
                          'positive_states':states,'positive_state_bound':bound})
    kept=sum(Fraction(row['cross_matrices'])*Fraction(*transfers[row['repeated_row_classes']]['keep_fraction'])*2**443
             for row in observed)
    need(kept.denominator==1,'physical count must be integral')
    need(kept.numerator==actual['remaining_units']*2**actual['unit_exponent'],'full-graph count disagreement')
    baseline=sum(row['cross_matrices'] for row in observed)*2**443
    f=(baseline-kept)/baseline
    need([f.numerator,f.denominator]==actual['removed_fraction'],'global fraction disagreement')
    need(f>Fraction(66,100),'substantial global reduction gate')
    q1=Fraction(*transfers[1]['keep_fraction']);q2=Fraction(*transfers[2]['keep_fraction'])
    gap=q2-q1*q1
    need(gap>0,'pair events are not independent')
    return {'counts':actual,'independent_marked_coefficients':sum(len(v) for _,_,v in rows),
            'independent_column_counts':4,'all_stratum_fields_checked':33,
            'positive_transfers':transfers,'independence_error_for_two_pairs':[gap.numerator,gap.denominator]}


def literal_distance_counts():
    results=[]
    for n in range(2,7):
        pairs=list(combinations(range(n),2));hist=Counter()
        for bits in range(1 << len(pairs)):
            adjacency=[[False]*n for _ in range(n)]
            for k,(a,b) in enumerate(pairs):
                adjacency[a][b]=adjacency[b][a]=bool(bits >> k & 1)
            minimum=n
            for p in range(1,n//2+1):
                a,b=2*p-2,2*p-1
                d=sum(adjacency[a][v]!=adjacency[b][v] for v in range(n) if v not in (a,b))
                minimum=min(minimum,d);hist[p,minimum]+=1
        tests=0
        for p in range(1,n//2+1):
            for h in range(n-1):
                count=sum(value for (q,d),value in hist.items() if q==p and d>=h)
                expected=Fraction(count,2**len(pairs))
                need(grouped_transfer(n,h,p)[0]==expected,'literal distance/graph sum')
                need(grouped_positive_transfer(n,h,p)[0]==expected,'literal distance/block sum')
                tests+=1
        results.append({'order':n,'all_graphs':1 << len(pairs),'probabilities_checked':tests})
    return results


def full_small_graphs():
    """Test the complete cross-stratum times internal-probability bridge."""
    records=[]
    pairs=list(combinations(range(6),2))
    for m,n in [(3,3),(4,2)]:
        hist=Counter()
        for bits in range(1 << len(pairs)):
            adj=[[False]*6 for _ in range(6)]
            for k,(a,b) in enumerate(pairs):adj[a][b]=adj[b][a]=bool(bits >> k & 1)
            rows=[sum(adj[i][m+j] << j for j in range(n)) for i in range(m)]
            cols=[sum(adj[i][m+j] << i for i in range(m)) for j in range(n)]
            r=rank(rows,n);br=rank([row^((1<<n)-1) for row in rows],n)
            if r==0 or br<r:continue
            ca,cb=Counter(rows),Counter(cols)
            if ca[0]>1 or cb[0]>2 or ca[0]*cb[0] or max(ca.values())>3 or max(cb.values())>5:continue
            chosen=selected_pairs(rows);j=len(chosen)
            hist[r,j,0]+=1
            ds=[sum(adj[a][v]!=adj[b][v] for v in range(6) if v not in (a,b)) for a,b in chosen]
            for h in range(1,m-1):
                if all(d>=h for d in ds):hist[r,j,h]+=1
        comparisons=0
        free=comb(m,2)+comb(n,2)
        for r in range(1,min(m,n)+1):
            for row in counts.strata(m,n,r):
                j=row['repeated_row_classes']
                for h in range(m-1):
                    expected=row['cross_matrices']*2**free*grouped_transfer(m,h,j)[0]
                    need(expected==hist[r,j,h],'full physical graph bridge')
                    comparisons+=1
        records.append({'cut':[m,n],'all_full_graphs':32768,'entry_comparisons':comparisons})
    return records


def physical_checks():
    rng=random.Random(9076622)
    pool=[1,2,4,8,16]+[x for x in range(1,32) if x not in (1,2,4,8,16)]
    index={pair:k for k,pair in enumerate(INTERNAL)}
    def edge(bits,a,b,value):
        bit=1 << index[tuple(sorted((a,b)))]
        return (bits|bit) if value else (bits & ~bit)
    def make(j,tripled=False):
        labels=[x for x in pool[:j] for _ in range(2)]+pool[j:20-j]
        if tripled:
            labels.pop();labels.append(pool[0])
        rng.shuffle(labels)
        return {'rows':labels,'columns':list(range(1,24)),
                'internal_hex':format(rng.getrandbits(443),'0111x')}
    def force_pass(data):
        changed=deepcopy(data);selected=selected_pairs(data['rows']);bits=int(data['internal_hex'],16)
        used={v for pair in selected for v in pair};unused=[v for v in range(20) if v not in used]
        for a,b in selected:
            for w in unused:bits=edge(bits,a,w,0);bits=edge(bits,b,w,1)
        for (a,b),(c,d) in combinations(selected,2):
            for u,v,value in [(a,c,0),(a,d,1),(b,c,1),(b,d,0)]:bits=edge(bits,u,v,value)
        changed['internal_hex']=format(bits,'0111x');return changed
    fixture=None;certificates=basis_changes=negative=0;checked_j=[]
    def rejects(fn):
        nonlocal negative
        try:fn()
        except (ValueError,ArithmeticError,TypeError):negative+=1;return
        raise ArithmeticError('corrupt/out-of-scope input accepted')
    for j in range(11):
        trials=1 if j==0 else 2
        for trial in range(trials):
            data=make(j,tripled=bool(trial and j<10))
            need(len(selected_pairs(data['rows']))==j,'wrong repeated-class fixture')
            passed=force_pass(data)
            need(classify(passed).get('keep'),'physical all-pair retained control')
            rejects(lambda:extract(passed))
            if not j:continue
            broken=deepcopy(passed);a,b=selected_pairs(broken['rows'])[0]
            bits=int(broken['internal_hex'],16)
            for v in range(20):
                if v in (a,b):continue
                value=rng.getrandbits(1)
                bits=edge(bits,a,v,value);bits=edge(bits,b,v,value)
            broken['internal_hex']=format(bits,'0111x')
            status=classify(broken)
            need(status.get('baseline') and not status.get('keep'),'physical rejection')
            graph,cert=extract(broken);verify(graph,cert);certificates+=1
            adj=decode(graph)
            for record in pair_distances(graph,status['selected_pairs']):
                x,y=record['pair']
                expected=[v for v in range(43) if v not in (x,y) and adj[x][v]!=adj[y][v]]
                need(record['distinguishers']==expected,'physical distinguisher list')
                need(all(v<20 for v in expected),'equal cross rows must cancel')
            p,q=rng.sample(range(5),2);changed=deepcopy(broken)
            changed['rows']=[x ^ (((x >> q)&1) << p) for x in broken['rows']]
            changed['columns']=[y ^ (((y >> p)&1) << q) for y in broken['columns']]
            need(physical(changed)==graph and classify(changed)==status,'basis invariance')
            basis_changes+=1
            bad=deepcopy(cert);bad['vertices'][1]=bad['vertices'][0];rejects(lambda:verify(graph,bad))
            bad=deepcopy(cert);bad['color']='blue' if cert['color']=='red' else 'red';rejects(lambda:verify(graph,bad))
            checked_j.append(j)
            if j==5 and trial==1:fixture={'parameters':broken,'graph':graph,'certificate':cert}
    need(fixture is not None,'missing physical fixture')
    # Physical boundary at distances seven and eight, with exactly one pair.
    boundary=[]
    data=make(1);a,b=selected_pairs(data['rows'])[0];other=[v for v in range(20) if v not in (a,b)]
    for h in (7,8):
        bits=int(data['internal_hex'],16)
        for k,v in enumerate(other):bits=edge(bits,a,v,0);bits=edge(bits,b,v,k<h)
        x=deepcopy(data);x['internal_hex']=format(bits,'0111x')
        need(classify(x)['keep']==(h==8),'distance endpoint classification')
        boundary.append(h)
    data=fixture['parameters'];zero=deepcopy(data);zero['internal_hex']='0'*111
    initial=int(physical(zero)['red_hex'],16)
    for k,pair in enumerate(INTERNAL):
        x=deepcopy(zero);x['internal_hex']=format(1 << k,'0111x')
        need(int(physical(x)['red_hex'],16)^initial==1 << PAIRS.index(pair),'internal coordinate map')
    for key,value in [('rows',[1]*20),('internal_hex','0'),('internal_hex','f'*111),
                      ('columns',[1]*23)]:
        bad=deepcopy(data);bad[key]=value;rejects(lambda bad=bad:classify(bad))
    bad=deepcopy(data);bad['keep']=True;rejects(lambda:classify(bad))
    for value in (-1,32,True,1.0):
        bad=deepcopy(data);bad['rows'][0]=value;rejects(lambda bad=bad:classify(bad))
    old_reject={'rows':[1]*4+list(range(2,18)),'columns':list(range(1,24)),'internal_hex':'0'*111}
    need(not classify(old_reject)['baseline'],'old rejection must not be counted twice')
    rejects(lambda:extract(old_reject))
    bad=deepcopy(fixture['graph']);bad['n']=42;rejects(lambda:verify(bad,fixture['certificate']))
    return {'physical_certificates':certificates,'basis_changes':basis_changes,
            'repeated_counts_exercised':sorted(set(checked_j)),'zero_pair_control':True,
            'distance_boundaries':boundary,'all_internal_coordinates':443,
            'negative_controls':negative,'fixture':fixture}


def literal_clique_checks():
    tests=0;pairs=list(combinations(range(5),2))
    for bits in range(1024):
        for color in (0,1):
            a=[[False]*5 for _ in range(5)];rows=[0]*5
            for k,(u,v) in enumerate(pairs):
                if ((bits >> k)&1)==color:
                    a[u][v]=a[v][u]=True;rows[u] |= 1 << v;rows[v] |= 1 << u
            for size in range(1,6):
                expected=next((list(vs) for vs in combinations(range(5),size)
                               if all(a[u][v] for u,v in combinations(vs,2))),None)
                need(clique(rows,31,size)==expected,'literal clique checker');tests+=1
    return tests


def run():
    return {'status':'VERIFIED_RANK5_DISTANCE_SIEVE','arithmetic':arithmetic(),
            'literal_distance_counts':literal_distance_counts(),
            'full_small_graphs':full_small_graphs(),'physical':physical_checks(),
            'literal_clique_comparisons':literal_clique_checks()}


if __name__=='__main__':print(json.dumps(run(),indent=2,sort_keys=True))
