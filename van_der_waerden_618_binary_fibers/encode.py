"""Exact binary fibers and the complete2187-entry ternary local classification."""
from collections import Counter
from itertools import product


def canonical(literals):
    values=tuple(sorted(literals))
    assert len(set(map(abs,values)))==7
    return min(values,tuple(sorted(-v for v in values)))


def local_table():
    rows=[];profiles=Counter();sizes=Counter()
    for tau in product(range(3),repeat=7):
        counts=Counter()
        for b in range(6):
            for s in range(6):
                mask=sum(int((b+j*s-tau[j])%6>=3)<<j for j in range(7))
                counts[min(mask,mask^127)]+=1
        assert all(n%2==0 for n in counts.values())
        weights=[counts[i]//2 for i in range(64)]
        assert sum(weights)==18 and max(weights)<=3
        count=sum(w>0 for w in weights)
        period_three=all(tau[j+3]==tau[j] for j in range(4))
        assert (count==8)==period_three and (count==8 or count>=12)
        profile=tuple(sorted(Counter(w for w in weights if w).items()))
        profiles[profile]+=1;sizes[count]+=1;rows.append(weights)
    raw='2187 64\n'+''.join(str(i)+' '+' '.join(map(str,row))+'\n' for i,row in enumerate(rows))
    metadata={'ternary_vectors':2187,'class_count_histogram':dict(sorted(sizes.items())),
              'profiles':[{'weights':[list(x) for x in p],'vectors':n} for p,n in sorted(profiles.items())],
              'entries_compared':2187*64,'weight_sum_per_support':18,
              'eight_classes_iff_period_three':True,'max_multiplicity':3}
    return raw.encode(),metadata


def encoding(tau):
    assert len(tau)==103 and set(tau)<={0,1,2}
    weights={};supports=set();profiles=Counter();nonperiodic=0
    for a in range(103):
        for r in range(1,103):
            points=tuple((a+j*r)%103 for j in range(7))
            if points>points[::-1]:continue
            support=tuple(sorted(points));assert support not in supports;supports.add(support)
            local=Counter()
            for offset in range(3):
                b=(tau[a]+offset)%6
                for s in range(6):
                    bits=[int((b+j*s-tau[x])%6>=3) for j,x in enumerate(points)]
                    assert bits[0]==0
                    edge=canonical((x+1)*(1 if bit==0 else -1) for x,bit in zip(points,bits))
                    local[edge]+=1
            assert sum(local.values())==18 and max(local.values())<=3
            period_three=all(tau[points[j+3]]==tau[points[j]] for j in range(4))
            assert (len(local)==8)==period_three and (len(local)==8 or len(local)>=12)
            nonperiodic+=int(not period_three)
            profile=tuple(sorted(Counter(local.values()).items()));profiles[profile]+=1
            for edge,weight in local.items():
                assert edge not in weights
                weights[edge]=weight
    assert len(supports)==5253 and sum(weights.values())==94554
    n=[tau.count(i) for i in range(3)]
    histogram_lower=42024+2*(103**2-sum(v*v for v in n))
    lower=max(histogram_lower,43044 if len(set(tau))>1 else 42024)
    assert lower<=len(weights)<=94554
    if len(set(tau))>1:assert nonperiodic>=255
    else:assert len(weights)==42024
    clauses={(-1,)} # Global complement fixes the orientation u(0), not necessarily c(0).
    edges=sorted(weights)
    for e in edges:clauses.add(e);clauses.add(tuple(sorted(-v for v in e)))
    cnf=f'p cnf 103 {len(clauses)}\n'+''.join(' '.join(map(str,c))+' 0\n' for c in sorted(clauses))
    weighted=f'103 {len(edges)}\n'+''.join(' '.join(map(str,e))+' 0 '+str(weights[e])+'\n' for e in edges)
    metadata={'variables':103,'clauses':len(clauses),'nae_edges':len(edges),
              'weights_histogram':dict(sorted(Counter(weights.values()).items())),
              'profile_histogram':[{'weights':[list(x) for x in k],'supports':v} for k,v in sorted(profiles.items())],
              'weight_sum':94554,'cyclic_pairs_per_weight':4,'field_AP_supports':5253,
              'non_period3_supports':nonperiodic,'tau_color_class_sizes':n,
              'proved_model_size_lower_bound':lower,'normalized_binary_assignments':str(2**102)}
    return cnf.encode(),weighted.encode(),metadata


def candidate(tau,u):
    assert len(tau)==len(u)==103 and set(tau)<={0,1,2} and set(u)<={0,1}
    return [u[t%103]^int((t%6-tau[t%103])%6>=3) for t in range(618)]


def static_cost(weighted,u):
    result=count=0
    for line in weighted.decode().splitlines()[1:]:
        values=list(map(int,line.split()));assert values[-2]==0
        if len({u[abs(v)-1]^int(v<0) for v in values[:-2]})==1:
            count+=1;result+=values[-1]
    return count,result
