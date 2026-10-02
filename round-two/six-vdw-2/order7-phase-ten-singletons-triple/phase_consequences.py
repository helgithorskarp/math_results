"""Counts conditional on the new lemma; this file is never a native model input."""
from collections import Counter
from functools import lru_cache
import itertools
import json
import math

def require(ok,message):
    if not ok:raise ValueError(message)

@lru_cache(None)
def coefficient(total,parts):
    current={0:1}
    for _ in range(parts):
        next_values=Counter()
        for value,count in current.items():
            for gap in range(1,8):
                if value+gap<=total:next_values[value+gap]+=count
        current=next_values
    return current.get(total,0)

def inclusion_exclusion(total,parts):
    if parts==0:return int(total==0)
    return sum((-1)**j*math.comb(parts,j)*math.comb(total-7*j-1,parts-1)
               for j in range(parts+1) if total-7*j>=parts)

def prediction(n,k):
    numerator=n*coefficient(n-k,k)
    require(numerator%k==0,'singleton cyclic multiplicity nonintegral')
    return numerator//k+(n*coefficient(n-k-1,k-3) if k>=3 else 0)

def verify():
    singleton=44*coefficient(34,10)//10
    triple=44*coefficient(33,7)
    excluded={4:44*coefficient(34,7),5:44*coefficient(34,6),6:44*coefficient(34,5)}
    for total,parts in [(34,10),(33,7),(34,7),(34,6),(34,5)]:
        require(coefficient(total,parts)==inclusion_exclusion(total,parts),'independent DP/IE coefficient differs')
    require((singleton,triple,excluded)==(50389724,1767304,{4:1469160,5:55044,6:220}),
            'complete necessary phase counts differ')
    observed=Counter();inputs=0
    for n in range(6,15):
        for mask in range(1,(1<<n)-1):
            k=mask.bit_count()
            if k>10:continue
            inputs+=1;word=[(mask>>i)&1 for i in range(n)]
            starts=[i for i in range(n) if word[i] and not word[(i-1)%n]]
            lengths=[];backgrounds=[]
            for i in starts:
                t=1
                while word[(i+t)%n]:t+=1
                gap=1
                while not word[(i+t+gap)%n]:gap+=1
                lengths.append(t);backgrounds.append(gap)
            if any(t not in (1,3) for t in lengths) or max(backgrounds)>7:continue
            if lengths.count(3)>1 or any(t==3 and gap!=1 for t,gap in zip(lengths,backgrounds)):continue
            observed[n,k]+=1
    tests=0
    for n in range(6,15):
        for k in range(1,min(10,n-1)+1):
            require(observed[n,k]==prediction(n,k),'complete small literal cyclic count differs');tests+=1
    gap_vectors={g for g in itertools.product(range(1,8),repeat=5) if sum(g)==34}
    require(gap_vectors=={tuple(7-int(i==j) for i in range(5)) for j in range(5)},'length6 five-vector cover differs')
    long_parameters=[(t,m,b) for t in (5,4) for m in range(t+7,t,-1) for b in (0,1)]
    require(len(long_parameters)==28 and len(set(long_parameters))==28,'ordinary28 excluded head cover differs')
    return dict(agent='six-vdw-2',role='researcher',status='EXACT_NECESSARY_SINGLETONS_TRIPLE_PHASE_COUNTS',
        conditional_on_38_checked_refutations=True,not_a_native_model_input=True,phase_length=44,
        selected_count=10,background_count=34,allowed_selected_run_lengths=[1,3],at_most_one_triple=True,
        triple_following_background_length=1,maximum_background_run=7,
        labeled_singleton_patterns=singleton,labeled_one_triple_patterns=triple,
        labeled_necessary_phase_patterns=singleton+triple,prior_9739_necessary_patterns=53681452,
        excluded_patterns_by_length=excluded,eliminated_patterns=sum(excluded.values()),
        counts_are_per_prescribed_selected_value=True,counts_are_not_valid_field_colorings=True,
        coefficients_checked=5,small_literal_word_controls=inputs,small_count_identities=tests,
        small_controls_do_not_prove_ordinary44_bridge=True,length6_gap_vectors=5,
        excluded_length45_heads=long_parameters,whole_phase10_exclusion=False,selected_no_adjacency=False,
        global_W_bound=False,interval3704_witness=False)

if __name__=='__main__':print(json.dumps(verify(),sort_keys=True,indent=2))
