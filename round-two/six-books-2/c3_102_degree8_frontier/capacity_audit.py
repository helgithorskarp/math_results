"""Literal H spines and load-composition reconstruction of the P1 root table."""
from argparse import ArgumentParser
from collections import Counter
from itertools import combinations, combinations_with_replacement, permutations
from pathlib import Path
import json,resource,time

START=time.monotonic()
parser=ArgumentParser();parser.add_argument('--work',type=Path,required=True)
OUT=parser.parse_args().work
primary=json.loads((OUT/'root-capacity.json').read_text())
PAIRS=list(combinations(range(9),2))
FREE_COUNTS={8:1,9:3,10:3}
NAMED={
    ((8,10,10),(9,9,9,10),(4,4,4,5)):'P1_81010',
    ((9,9,9),(8,10,10,10),(3,4,4,5)):'P1_999',
    ((9,9,10),(8,9,10,10),(3,4,5,5)):'P1_9910',
    ((8,9,10),(9,9,10,10),(4,4,3,5)):'P1_8910_G7',
    ((8,9,10),(9,9,10,10),(3,4,4,5)):'P1_8910_GM',
    ((8,9,10),(9,9,10,10),(4,4,4,4)):'P1_8910_G6',
    ((8,9,10),(9,9,10,10),(3,3,5,5)):'P1_8910_J66',
}

def encoded(value):
    return json.dumps(value,sort_keys=True,separators=(',',':'),allow_nan=False)

def local(word):
    rows=[]
    for u in range(9):
        i,t=divmod(u,3);row=set()
        for v in range(9):
            if u==v:
                continue
            j,s=divmod(v,3)
            bit=i if i==j else {(0,1):3,(0,2):6,(1,2):9}[min(i,j),max(i,j)]+((s-t)%3 if i<j else (t-s)%3)
            if word>>bit&1:
                row.add(v)
        rows.append(row)
    return rows

def load_vectors(caps,total,prefix=()):
    if not caps:
        if total==0:
            yield prefix
        return
    for load in range(min(caps[0],total)+1):
        yield from load_vectors(caps[1:],total-load,prefix+(load,))

placements=[]
for n8 in range(2):
    for n9 in range(4):
        n10=3-n8-n9
        if not 0<=n10<=3:
            continue
        placements.append((8,)*n8+(9,)*n9+(10,)*n10)
placements.sort();records=[];residual=[]
global_degrees=[8]*3+[9]*10+[10]*9
E=sum(global_degrees)//2
if E!=102 or [d for d in [8,9,10] if Counter(global_degrees)[d]%3!=0]!=[9]:
    raise ValueError('P1 edge count/fixed-root congruence')
for A in placements:
    used=Counter(A)
    B=tuple(d for d in [8,9,10] for _ in range(FREE_COUNTS[d]-used[d]))
    DA=sum(A)*3
    # Literal root red deficit 27-2h and blue deficit -60+2k:
    # their sum is -33+2(k-h), hence -33+2(E-DA).
    root_deficit=-33+2*(E-DA)
    record=dict(A=A,B=B,DA=DA,root_deficit=root_deficit,cuts=[])
    if root_deficit<0:
        record['verdict']='negative_fixed_root_deficit';records.append(record);continue
    Bperms=[p for p in permutations(range(4)) if all(B[i]==B[p[i]] for i in range(4))]
    for h in [0,3,6,9,12]:
        k=E-DA+h
        if 2*k<12*5:
            record['cuts'].append(dict(h=h,k=k,verdict='K_minimum_degree_five'));continue
        t_vectors=sorted({p for t in combinations_with_replacement(range(4),3) if 3*sum(t)==2*h for p in permutations(t)})
        capacities=[]
        for t in t_vectors:
            cap=8*DA-15*36+17*h-3*sum(x*d+x*(x-1)//2 for x,d in zip(t,A))
            capacities.append((t,cap))
        upper=max(cap for _,cap in capacities)
        total_alpha=(DA-9-2*h)//3
        ordered_alpha=list(load_vectors(tuple(d-5 for d in B),total_alpha))
        ordered_beta=sorted(tuple(d-a for d,a in zip(B,alpha)) for alpha in ordered_alpha)
        representatives=sorted({min(tuple(alpha[p[i]] for i in range(4)) for p in Bperms) for alpha in ordered_alpha})
        canonical=[]
        for alpha in representatives:
            overlap=sum(3*a*(a-1)//2 for a in alpha)
            survives=overlap<=upper
            canonical.append(dict(alpha=alpha,beta=[d-a for d,a in zip(B,alpha)],overlap=overlap,survives=survives))
            if survives:
                key=(A,B,alpha)
                if key not in NAMED or h!=12:
                    raise ValueError('Independent complete residual marks differ')
                residual.append(dict(case=NAMED[key],A=A,B=B,h=h,k=k,alpha=alpha,overlap=overlap,capacity_upper=upper))
        record['cuts'].append(dict(h=h,k=k,capacity_upper=upper,degree_vectors=capacities,ordered_beta_vectors=ordered_beta,
                                  canonical_columns=canonical,minimum_column_overlap=min((v['overlap'] for v in canonical),default=None),
                                  verdict='residual_marked_case' if any(v['survives'] for v in canonical) else 'column_overlap_exceeds_capacity'))
    record['verdict']='some_marked_cases_survive' if any(r['A']==A for r in residual) else 'capacity_exclusion'
    records.append(record)
math=dict(free_degree_orbits=[8,9,9,9,10,10,10],placements=records,residual=residual)
if encoded(math)!=encoded({k:primary[k] for k in math}):
    raise ValueError('ENTIRE typed root/capacity/column table differs')

literal_rows=0;literal_pairs=0;actual_maxima={};words_checked=0
for word in range(4096):
    H=local(word);hd=list(map(len,H));h=sum(hd)//2
    for A in [(8,9,9),(8,9,10),(8,10,10),(9,9,9),(9,9,10)]:
        DG=[d for d in A for _ in range(3)]
        margins=[DG[u]-1-hd[u] for u in range(9)]
        caps=[]
        for u,v in PAIRS:
            if v in H[u]:
                cap=3-1-len(H[u]&H[v])
            else:
                blue_A=sum(w not in H[u] and w not in H[v] for w in range(9) if w not in [u,v])
                cap=6-blue_A-(12-margins[u]-margins[v])
            caps.append(cap)
        literal_pairs+=36
        for u in range(9):
            actual=margins[u]+sum(cap for (v,w),cap in zip(PAIRS,caps) if u in [v,w])
            formula=sum(DG)+8*DG[u]-121+hd[u]*(17-DG[u])-sum(DG[v]+hd[v] for v in H[u])
            if actual!=formula:
                raise ValueError('Literal complete AA Gram-row identity differs')
            literal_rows+=1
        total=17*h-540+8*sum(DG)-sum(x*d for x,d in zip(hd,DG))-sum(x*(x-1)//2 for x in hd)
        if total!=sum(caps):
            raise ValueError('Literal whole AA capacity identity differs')
        if max(hd)<=3:
            actual_maxima[A,h]=max(actual_maxima.get((A,h),-10**9),sum(caps))
    words_checked+=1
    if time.monotonic()-START>25:
        raise RuntimeError('INCOMPLETE literal capacity audit; no exclusion')
for record in records:
    A=tuple(record['A'])
    for cut in record['cuts']:
        if 'capacity_upper' in cut and actual_maxima[A,cut['h']]>cut['capacity_upper']:
            raise ValueError('Actual H-spine upper exceeds degree-domain bound')
result=dict(status='COMPLETE_DISTINCT_P1_ROOT_CAPACITY_AUDIT',agent='six-books-2',role='researcher',
            whole_typed_root_table_equal=True,fixed_root_congruence_checked=True,ordered_alpha_compositions_and_full_B_transports_checked=True,
            literal_H_words=words_checked,literal_pair_capacity_checks=literal_pairs,literal_Gram_row_checks=literal_rows,
            literal_ordinary_capacity_identity_checked=True,actual_H_maxima_bounded=True,
            seconds=time.monotonic()-START,peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
            trust='Literal H spines/load composition/full transport algorithm, same author; ordinary/completeness bridges unformalized, no independent review.')
(OUT/'capacity-audit.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
