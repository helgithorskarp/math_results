"""Different literal audits; imports no producer functions or expected counts."""
from collections import Counter
from itertools import combinations, product


def profile_audit(record, all_marks, retained):
    # Every ordered mark in the four-value domain is visited, rather than
    # generating only eight multiset histograms as in the producer.
    observed = []
    kept = []
    counts = Counter()
    for marks in product(range(7,11),repeat=7):
        if 9+3*sum(marks) != 198:
            continue
        observed.append(marks)
        variance = 3*sum((degree-9)**2 for degree in marks)
        doubled_weight = 66-3*variance
        a,b = marks.count(8),marks.count(7)
        counts[(a,b)] += 1
        row = next(r for r in record['histograms'] if r['a']==a and r['b']==b)
        if 2*row['deficit_weight']!=doubled_weight or row['variance']!=variance:
            raise ValueError('Direct variance/profile formula mismatch')
        if doubled_weight >= 0:
            kept.append(marks)
    if observed != all_marks or kept != retained:
        raise ValueError('Entire ordered degree domains differ')
    if len(record['histograms']) != len(counts):
        raise ValueError('Extra/missing degree histogram')
    for r in record['histograms']:
        a,b=r['a'],r['b']
        actual = Counter(next(m for m in observed if m.count(8)==a and m.count(7)==b))
        if {int(k):v for k,v in r['free_degree_counts'].items()} != {d:actual[d] for d in range(7,11)}:
            raise ValueError('Whole histogram degree marks differ')
        if r['ordered_placements'] != counts[a,b] or r['retained']!=(r['deficit_weight']>=0):
            raise ValueError('Histogram count/selection differs')
    for r in record['new_profile_root_placements']:
        matching = [m for m in kept if m.count(8)==r['a'] and m.count(7)==r['b']]
        patterns=Counter(); rejection=Counter()
        for marks in matching:
            D_A=3*sum(marks[:3])
            if D_A>81:
                rejection['root_cut']+=1
            elif 165-2*D_A>6:
                rejection['root_budget']+=1
            else:
                patterns[tuple(sorted(marks[:3]))+tuple(sorted(marks[3:]))]+=1
        expected=[dict(A=list(k[:3]),B=list(k[3:]),ordered_placements=v) for k,v in sorted(patterns.items())]
        if r['survivors']!=expected or r['rejected']!=dict(rejection) or r['ordered_placements']!=len(matching):
            raise ValueError('Entire new-profile root placement records differ')
    return dict(ordered_marks_domain=4**7,sum_matches=len(observed),
                retained=len(kept),whole_ordered_domains_equal=True,
                whole_new_root_placement_fields_equal=True)


def H_rows(word):
    out=[]
    for u in range(9):
        i,t=divmod(u,3); neighbors=set()
        for v in range(9):
            if u==v:
                continue
            j,s=divmod(v,3)
            if i==j:
                bit=i
            else:
                base={(0,1):3,(0,2):6,(1,2):9}[min(i,j),max(i,j)]
                bit=base+((s-t)%3 if i<j else (t-s)%3)
            if word>>bit&1:
                neighbors.add(v)
        out.append(neighbors)
    return out


def literal_H_audit(record):
    pairs=list(combinations(range(9),2)); by_degrees=Counter(); parity_records=[]
    for word in range(4096):
        H=H_rows(word); degrees=list(map(len,H))
        if sum(degrees)!=24 or max(degrees)>3:
            continue
        hd=tuple(degrees[::3]); by_degrees[hd]+=1
        for DG,ranks in [([7]*3+[10]*6,[4]*4),([8]*3+[9]*3+[10]*3,[3,3,5,5])]:
            margins=[d-1-h for d,h in zip(DG,degrees)]
            caps=[]
            for u,v in pairs:
                if v in H[u]:
                    caps.append(3-1-len(H[u]&H[v]))
                else:
                    blue_A=sum(w not in H[u] and w not in H[v] for w in range(9) if w not in [u,v])
                    caps.append(6-blue_A-(12-margins[u]-margins[v]))
            case=next(r for r in record['marked_capacity_cases'] if r['A']==DG[::3] and r['H_orbit_degrees']==list(hd))
            actual=sum(caps)
            overlap=0
            for rank in ranks:
                overlap+=3*len(list(combinations(range(rank),2)))
            if actual!=case['capacity'] or overlap!=case['actual_overlap'] or case['slack']!=actual-overlap:
                raise ValueError('Literal capacities differ from scalar identity')
            if case['root_deficit']!=3 or case['total_deficit']!=6:
                raise ValueError('Root or whole deficit bound differs')
            if actual<overlap:
                reason='capacity_below_actual_overlap'
            elif DG[0]==7:
                if actual-overlap+3<=6:
                    raise ValueError('Exceptional total deficit bound fails')
                reason='A_pair_slack_plus_root_exceeds_total_budget'
            else:
                if actual!=overlap or hd!=(3,3,2):
                    raise ValueError('Three-pair equality fails')
                reason='all_A_pairs_tight_then_odd_column_parity'
            if case['reason']!=reason:
                raise ValueError('Actual obstruction label differs')
            if DG[0]==8 and hd==(3,3,2):
                sums=[]
                for u in range(3):
                    ell=len(H[u]&set(range(3)))
                    value=margins[u]+sum(c for (a,b),c in zip(pairs,caps) if u in [a,b])
                    if ell not in [0,2] or value!=15+ell or value%2==margins[u]%2:
                        raise ValueError('Literal tight-Gram low-row parity failure')
                    sums.append(value)
                parity_records.append(dict(word=word,low_Gram_row_sums=sums))
    expected_parity=[]
    for ell in [0,2]:
        for high in range(4-ell):
            neighbor_marks=[8]*ell+[10]*high+[9]*(3-ell-high)
            neighbor_locals=[3 if d in [8,9] else 2 for d in neighbor_marks]
            pair_capacity=17+sum(9-d for d in neighbor_marks)-sum(d-1 for d in neighbor_locals)
            expected_parity.append(dict(low_internal_neighbors=ell,high_neighbors=high,
                                        pair_capacity_sum=pair_capacity,tight_Gram_row_sum=4+pair_capacity,
                                        odd_column_required_parity=0))
    if record['low_row_parity_cases']!=expected_parity:
        raise ValueError('Entire marked low-row parity fields differ')
    if record['exceptional_all_nine']!=dict(A=[9,9,9],B=[7,9,10,10],B_column_ranks=[2,4,5,5],capacity=75,actual_overlap=81):
        raise ValueError('Exceptional all-nine fields differ')
    return dict(all_H_words=4096,edge12_max3_words=sum(by_degrees.values()),
                local_degree_groups=[dict(degrees=list(k),words=v) for k,v in sorted(by_degrees.items())],
                parity_words=len(parity_records),whole_parity_records=parity_records,
                literal_capacity_fields_equal=True)
