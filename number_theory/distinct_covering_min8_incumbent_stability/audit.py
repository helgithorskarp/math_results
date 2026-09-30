"""Separate full-period audit of all 2756 local stability cases.

Author six-covering-1, researcher. Imports no production checker. Prefix
membership is tested by congruence predicates; all resource phases are
counted in the literal target period, without projected CRT capacities.
"""
from collections import Counter
import hashlib
import itertools
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parent


def insist(condition,message):
    if not condition:raise ValueError(message)


def factor_lcm(moduli):
    exponents={}
    for n in moduli:
        p=2
        while p*p<=n:
            power=0
            while n%p==0:n//=p;power+=1
            if power:exponents[p]=max(exponents.get(p,0),power)
            p+=1
        if n>1:exponents[n]=max(exponents.get(n,0),1)
    result=1
    for p,e in exponents.items():result*=p**e
    return result


def main():
    core_data=json.loads((ROOT/'core.json').read_text())
    upper_data=json.loads((ROOT/'upper_cover.json').read_text())
    weight_data=json.loads((ROOT/'weights.json').read_text())
    insist(core_data['base']==5040 and weight_data['base']==5040,'wrong base')
    core=core_data['congruences']
    upper=upper_data['congruences']
    for rows,period in ((core,5040),(upper,20160)):
        insist(len({m for a,m in rows})==len(rows),'repeated moduli')
        insist(all(type(a) is int and type(m) is int and 8<=m and period%m==0
                   and 0<=a<m for a,m in rows),'invalid input')
    insist(len(core)==53 and {m for a,m in core}=={d for d in range(8,5041) if 5040%d==0},'incomplete core')
    insist(min(m for a,m in upper)==8 and factor_lcm([m for a,m in upper])==20160,'wrong upper LCM/minimum')
    insist(set(map(tuple,core))<=set(map(tuple,upper)),'upper omits core')
    multiplicities=[sum(r%m==a for a,m in upper) for r in range(20160)]
    insist(min(multiplicities)>0,'invalid upper covering')
    records={}
    for item in weight_data['cuts']:
        key=item['period'],tuple(item['removed'])
        insist(key not in records,'duplicate case')
        records[key]=item
    visited=set();events=hashlib.sha256();cases=[];points_total=0
    for period in (10080,15120):
        # Every bit is established directly by the corresponding congruence.
        membership=[sum((1<<i) for i,(a,m) in enumerate(core) if x%m==a)
                    for x in range(period)]
        all_bits=(1<<len(core))-1
        moduli=[m for a,m in core]
        eligible=[d for d in range(8,period+1) if period%d==0]
        uniform=weighted=0;ugaps=[];wgaps=[]
        for i,j in itertools.combinations(range(53),2):
            pair=tuple(sorted((moduli[i],moduli[j])))
            retained=all_bits^(1<<i)^(1<<j)
            insist(factor_lcm([m for k,m in enumerate(moduli) if k not in (i,j)])==5040,'retained LCM mismatch')
            residual=[x for x,mask in enumerate(membership) if mask&retained==0]
            assigned={m for k,m in enumerate(moduli) if k not in (i,j)}
            free=[m for m in eligible if m not in assigned]
            capacities=[[m,max(Counter(x%m for x in residual).values(),default=0)] for m in free]
            demand=len(residual);kind='uniform';key=period,pair
            if demand>sum(c for m,c in capacities):
                insist(key not in records,'extraneous record')
                uniform+=1;ugaps.append(demand-sum(c for m,c in capacities))
            else:
                insist(key in records,'missing weighted case')
                item=records[key]
                weights=item['weights']
                insist(weights and len({x for x,w in weights})==len(weights),'empty/repeated weights')
                base_vector=[0]*5040
                for x,w in weights:
                    insist(type(x) is int and type(w) is int and 0<=x<5040 and w>0,'invalid weight')
                    base_vector[x]=w
                full_vector=[base_vector[x%5040] for x in range(period)]
                insist(all(not w or membership[x]&retained==0 for x,w in enumerate(full_vector)), 'covered weight support')
                demand=sum(full_vector)
                # Literal progression sums for EVERY normalized phase.
                capacities=[[m,max(sum(full_vector[x] for x in range(a,period,m))
                                   for a in range(m))] for m in free]
                insist(demand==item['demand'] and capacities==item['capacities'],'literal budget mismatch')
                insist(demand>sum(c for m,c in capacities),'nonstrict cut')
                visited.add(key);weighted+=1;kind='weighted'
                wgaps.append(demand-sum(c for m,c in capacities));points_total+=len(weights)
            events.update((json.dumps([period,list(pair),kind,demand,capacities],separators=(',',':'))+'\n').encode())
        insist(uniform+weighted==1378,'incomplete enumeration')
        cases.append({'period':period,'pair_cases':1378,'uniform_cuts':uniform,'weighted_cuts':weighted,
                      'minimum_uniform_gap':min(ugaps),'minimum_weighted_gap':min(wgaps)})
        print(json.dumps({'period':period,'all_pair_cases_checked':1378,'uniform':uniform,'weighted':weighted}),flush=True)
    insist(visited==set(records),'unused weight records')
    result={'agent':'six-covering-1','role':'researcher','status':'COMPLETE_EXACT_LOCAL_MINIMUM',
            'core_classes':53,'minimum_retained':51,'exact_family_minimum_lcm':20160,
            'cases':cases,'weighted_base_points':points_total,'ordered_events_sha256':events.hexdigest(),
            'upper_classes':len(upper),'upper_lcm':20160,'upper_minimum':8,'upper_uncovered':0,
            'upper_coverage_histogram':{str(k):v for k,v in sorted(Counter(multiplicities).items())},
            'upper_multiplicity_sha256':hashlib.sha256(bytes(multiplicities)).hexdigest()}
    insist(result==json.loads((ROOT/'expected.json').read_text()),'manifest disagreement')
    print(json.dumps(result,sort_keys=True))


if __name__=='__main__':main()
