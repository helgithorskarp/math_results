"""Ordinary summed-Gram obstruction for the two P2 A=(8,8,10) cases."""
from argparse import ArgumentParser
from collections import Counter
from itertools import combinations
from pathlib import Path
import json,resource,time

START=time.monotonic()
p=ArgumentParser();p.add_argument('--work',type=Path,required=True);OUT=p.parse_args().work
OUT.mkdir(parents=True,exist_ok=True)

def local(word):
    H=[set() for _ in range(9)]
    for a,b in combinations(range(9),2):
        i,t=divmod(a,3);j,s=divmod(b,3)
        bit=i if i==j else {(0,1):3,(0,2):6,(1,2):9}[i,j]+(s-t)%3
        if word>>bit&1:H[a].add(b);H[b].add(a)
    return H

def minimum_weighted_load(ranks,total):
    dp={0:0}
    for rank in ranks:
        next_dp={}
        for load,cost in dp.items():
            for n in range(min(6,rank,total-load)+1):
                m=load+n;value=cost+rank*n
                next_dp[m]=min(next_dp.get(m,10**9),value)
        dp=next_dp
    return dp[total]

columns=(3,)*3+(4,)*9
dp_lower=minimum_weighted_load(columns,24)
if dp_lower!=87 or 4*24-3*3!=dp_lower:
    raise ValueError('Exact full-column load lower certificate differs')
counts=Counter();row_records=[]
DG=[8]*6+[10]*3;L=set(range(6));U=set(range(6,9))
for word in range(4096):
    H=local(word);hd=list(map(len,H));h=sum(hd)//2
    counts['all_binary_H']+=1
    if h!=12:continue
    counts['H12']+=1
    if max(hd)>3:continue
    counts['H12_max_degree3']+=1
    gamma=[DG[a]-1-hd[a] for a in range(9)]
    caps={}
    for a,b in combinations(range(9),2):
        if b in H[a]:
            caps[a,b]=3-1-len(H[a]&H[b])
        else:
            blue_A=sum(v not in H[a] and v not in H[b]
                       for v in range(9) if v not in [a,b])
            caps[a,b]=6-blue_A-(12-gamma[a]-gamma[b])
    capacity=sum(caps.values())
    if capacity<63:continue
    counts['capacity_at_least63']+=1
    if hd!=[3]*6+[2]*3 or gamma!=[4]*6+[7]*3 or capacity!=63:
        raise ValueError('Equality does not force stated H/Gamma margins')
    if any(H[a]&U for a in U):
        counts['high_triangle_forbidden']+=1
        for a,b in combinations(sorted(U),2):
            if b not in H[a] or caps[a,b]!=1 or max(0,gamma[a]+gamma[b]-12)!=2:
                raise ValueError('Literal high-triangle ordinary red-page boundary')
        continue
    counts['high_independent']+=1
    low_to_high=sum(len(H[a]&U) for a in L)
    if low_to_high!=6:raise ValueError('Complete H high incidence total')
    full_rows=[]
    for a in sorted(L):
        row=gamma[a]+sum(c for pair,c in caps.items() if a in pair)
        expected=15-len(H[a]&U)
        if row!=expected:raise ValueError('Literal full upper Gram row, diagonal retained')
        full_rows.append(row)
    if sum(full_rows)!=84 or not sum(full_rows)<dp_lower:
        raise ValueError('Summed ordinary Gram obstruction')
    row_records.append(dict(H_word=word,low_to_high=low_to_high,
        literal_full_upper_rows=full_rows,sum_upper=84,weighted_column_lower=87))
    if time.monotonic()-START>25:
        raise RuntimeError('INCOMPLETE ordinary-cut corroboration; no verdict')
if not row_records or counts['capacity_at_least63'] != \
       counts['high_triangle_forbidden']+counts['high_independent']:
    raise ValueError('Incomplete ordinary-cut coverage partition')
result=dict(status='COMPLETE_ORDINARY_P2_8810_SUMMED_GRAM_CUT',agent='six-books-2',role='researcher',
    scope='The two complete P2 root cases with A-orbit degrees8,8,10 and alpha multiset3,4,4,4.',
    cases=['P2_8810_A3','P2_8810_A4'],counts=dict(counts),
    literal_records=row_records,weighted_load_total=24,weighted_load_lower=dp_lower,
    maximum_full_Gram_upper=84,gap=3,
    ordinary_argument='Capacity equality forces local degrees3,3,2. A high triangle violates ordinary red-pair load. Otherwise six low-to-high incidences give upper84;12 B-column ranks3^3,4^9 and total low rowload24 give weighted lower87.',
    seconds=time.monotonic()-START,peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
    trust='Written ordinary proof, unformalized; exact H/full-spine and broad-load DP corroboration by the same author.')
(OUT/'ordinary-cut.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='literal_records'},indent=2))
