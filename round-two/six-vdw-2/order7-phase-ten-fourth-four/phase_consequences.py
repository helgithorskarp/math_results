"""Exact necessary phase catalogue, ordinary run bridge and ten length-six heads."""
from collections import Counter
from functools import lru_cache
import itertools,json,math
def require(ok,message):
    if not ok:raise ValueError(message)
@lru_cache(None)
def coefficient(total,parts):
    values={0:1}
    for _ in range(parts):
        following=Counter()
        for s,count in values.items():
            for a in range(1,8):
                if s+a<=total:following[s+a]+=count
        values=following
    return values.get(total,0)
def independent_coefficient(total,parts):
    if parts==0:return int(total==0)
    if total<parts:return 0
    return sum((-1)**j*math.comb(parts,j)*math.comb(total-7*j-1,parts-1)
        for j in range(parts+1) if total-7*j>=parts)
def compositions(total,parts):
    if parts==0:
        if total==0:yield ()
        return
    for a in (1,3,4,5,6,7):
        if a<=total:
            for rest in compositions(total-a,parts-1):yield (a,*rest)
def small_prediction(n,k):
    value=n*coefficient(n-k,k)
    require(value%k==0,'singleton multiplicity nonintegral');value//=k
    for t in range(3,min(7,k)+1):
        r=k-t+1
        value+=n*coefficient(n-k-1,r-1) if t==3 else n*coefficient(n-k,r)
    return value
def verify():
    table=[];total=adjacent=0;shapes=set();composition_inputs=0
    for r in range(1,11):
        background_weight=0
        for lengths in compositions(10,r):
            composition_inputs+=1;q3=lengths.count(3)
            b=coefficient(34-q3,r-q3)
            require(b==independent_coefficient(34-q3,r-q3),'DP/IE constrained backgrounds differ')
            background_weight+=b
            if b:
                nontrivial=tuple(t for t in lengths if t>1)
                require(r>=5 and len(nontrivial)<=1 and all(t<=6 for t in nontrivial),
                        'TEN/34 whole-run consequence differs')
                shapes.add((r,tuple(sorted(nontrivial))))
        numerator=44*background_weight
        require(numerator%r==0,'cyclic run-start multiplicity nonintegral')
        count=numerator//r;total+=count
        if r!=10:adjacent+=count
        table.append(dict(runs=r,labeled_selected_value_patterns=count))
    independent=44*(coefficient(33,7)+coefficient(34,7)+coefficient(34,6)+coefficient(34,5))
    require(adjacent==independent,'independent one-long-run expression differs')
    require(total-adjacent==50389724,'singleton phase count differs')
    require(shapes=={(5,(6,)),(6,(5,)),(7,(4,)),(8,(3,)),(10,())},'complete run catalogue differs')

    # Literal small words check the one-long-run counting identity, not the 44-point theorem.
    observed=Counter();inputs=0
    for n in range(6,17):
        for mask in range(1,(1<<n)-1):
            k=mask.bit_count()
            if k>10:continue
            inputs+=1;bits=[(mask>>i)&1 for i in range(n)]
            starts=[i for i in range(n) if bits[i] and not bits[(i-1)%n]]
            runs=[];backgrounds=[]
            for i in starts:
                t=1
                while bits[(i+t)%n]:t+=1
                z=1
                while not bits[(i+t+z)%n]:z+=1
                runs.append(t);backgrounds.append(z)
            if any(t==2 or t>7 for t in runs) or max(backgrounds)>7:continue
            if sum(t>1 for t in runs)>1:continue
            if any(t==3 and z!=1 for t,z in zip(runs,backgrounds)):continue
            observed[n,k]+=1
    checked=0
    for n in range(6,17):
        for k in range(1,min(10,n-1)+1):
            require(observed[n,k]==small_prediction(n,k),'literal small cyclic count differs')
            checked+=1

    # Unique length-six selected run: five backgrounds sum34 and each<=7.
    vectors=[]
    for j in range(5):
        gaps=[7]*5;gaps[j]=6;selected=list(range(6));cursor=5
        for gap in gaps[:-1]:cursor+=gap+1;selected.append(cursor)
        require(len(selected)==10 and selected[-1]+gaps[-1]==43,'length-six cyclic head differs')
        for background in (0,1):
            phases=[int((i in selected)!=bool(background)) for i in range(44)]
            vectors.append(dict(deficient_gap=j,background=background,selected=selected,gaps=gaps,phases=phases,
                all_phase_variables_fixed=True,lower_color_variables=44,only_global_y0_zero=True,
                field_models_generated=False,native_proposals=0))
    # Independent five-composition enumeration uses bounded integer values.
    expected=set()
    for gaps in itertools.product(range(1,8),repeat=5):
        if sum(gaps)==34:expected.add(gaps)
    require(expected=={tuple(v['gaps']) for v in vectors} and len(expected)==5,'complete length-six five-vector cover differs')
    return dict(agent='six-vdw-2',role='researcher',status='EXACT_PHASE_SUPERSET_AND_LENGTH6_TEN_HEAD_PLAN_ONLY',
        phase_length=44,selected_count=10,background_count=34,run_shapes=[(r,list(s)) for r,s in sorted(shapes)],
        selected_run_compositions_checked=composition_inputs,phase_count_table=table,
        labeled_selected_value_patterns=total,with_selected_adjacency_patterns=adjacent,
        without_selected_adjacency_patterns=total-adjacent,prior_TWO_only_patterns=68603678,
        counts_are_necessary_phase_patterns_not_valid_field_colorings=True,
        literal_small_cyclic_word_controls=inputs,small_count_identities=checked,
        small_controls_do_not_prove_the_44_point_bridge=True,length6_case_plan=vectors,
        length6_exclusion=False,full_phase10_exclusion=False,selected_no_adjacency=False,
        global_W_bound=False,interval3704_witness=False)
if __name__=='__main__':print(json.dumps(verify(),sort_keys=True,indent=2))
