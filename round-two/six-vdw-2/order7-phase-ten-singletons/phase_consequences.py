"""Necessary phase counts conditional on the parent and14 checked refutations."""
from collections import Counter
from functools import lru_cache
import json
import math

def require(ok,message):
    if not ok:raise ValueError(message)

@lru_cache(None)
def coefficient(total,parts):
    values={0:1}
    for _ in range(parts):
        next_values=Counter()
        for value,count in values.items():
            for gap in range(1,8):
                if value+gap<=total:next_values[value+gap]+=count
        values=next_values
    return values.get(total,0)

def inclusion_exclusion(total,parts):
    if parts==0:return int(total==0)
    return sum((-1)**j*math.comb(parts,j)*math.comb(total-7*j-1,parts-1)
               for j in range(parts+1) if total-7*j>=parts)

def prediction(n,k):
    numerator=n*coefficient(n-k,k)
    require(numerator%k==0,'marked singleton multiplicity not integral')
    return numerator//k

def verify():
    for total,parts in ((34,10),(33,7)):
        require(coefficient(total,parts)==inclusion_exclusion(total,parts),'whole DP/IE coefficient differs')
    singletons=prediction(44,10);eliminated=44*coefficient(33,7)
    require((singletons,eliminated)==(50389724,1767304),'ordinary44 necessary catalogue differs')
    observed=Counter();words=tests=0
    for n in range(6,15):
        for mask in range(1,(1<<n)-1):
            k=mask.bit_count()
            if k>10:continue
            words+=1;word=[(mask>>i)&1 for i in range(n)]
            if any(word[i] and word[(i+1)%n] for i in range(n)):continue
            if any(all(not word[(i+j)%n] for j in range(8)) for i in range(n)):continue
            observed[n,k]+=1
        for k in range(1,min(10,n-1)+1):
            require(observed[n,k]==prediction(n,k),'whole small cyclic singleton count differs');tests+=1
    return dict(agent='six-vdw-2',role='researcher',status='EXACT_NECESSARY_SINGLETON_PHASE_COUNTS',
        conditional_on_actual_9799_and14_checked_refutations=True,not_a_native_model_input=True,
        phase_length=44,selected_count=10,background_count=34,allowed_selected_run_lengths=[1],
        selected_no_adjacency=True,maximum_background_run=7,labeled_necessary_phase_patterns=singletons,
        prior_9799_necessary_patterns=singletons+eliminated,eliminated_one_triple_patterns=eliminated,
        counts_are_per_prescribed_selected_value=True,counts_are_not_valid_field_colorings=True,
        coefficients_checked=2,small_literal_word_controls=words,small_count_identities=tests,
        small_controls_do_not_prove_ordinary44_bridge=True,whole_phase10_exclusion=False,
        whole_H7_exclusion=False,global_W_bound=False,interval3704_witness=False)

if __name__=='__main__':print(json.dumps(verify(),sort_keys=True,indent=2))
