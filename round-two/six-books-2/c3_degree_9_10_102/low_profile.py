"""Literal checks for the ordinary7^3,8^3,9^1,10^15 E102 obstruction."""
from argparse import ArgumentParser
from itertools import combinations, product
from pathlib import Path
from collections import Counter
import hashlib,json,time,resource

def local(word):
    H=[]
    for u in range(9):
        row=set();i,t=divmod(u,3)
        for v in range(9):
            if u==v:continue
            j,s=divmod(v,3)
            bit=i if i==j else {(0,1):3,(0,2):6,(1,2):9}[min(i,j),max(i,j)]+((s-t)%3 if i<j else (t-s)%3)
            if word>>bit&1:row.add(v)
        H.append(row)
    return H

def derive():
    orbit_marks=(7,8,10,10,10,10,10)
    root_marks=[]
    for slots in combinations(range(7),3):
        degrees=sorted(orbit_marks[i] for i in slots)
        DA=3*sum(degrees);Dx=171-2*DA
        if 0<=Dx<=6:root_marks.append((slots,degrees,DA,Dx))
    if len(root_marks)!=10 or any(r[1:]!=([8,10,10],84,3) for r in root_marks):
        raise ValueError('Complete low-profile root budget')

    low_table=[]
    surviving=[]
    for ell,q in product([0,2],range(4)):
        neighbors=[9]+[8]*ell+[10]*(3-ell)+[7]*q+[10]*(4-q)
        D=204-294+38*8-8*8-2*sum(neighbors)
        if D!=-8+4*ell+6*q:raise ValueError('Exact low-vertex row deficit')
        retained=0<=D<=2
        low_table.append(dict(internal_low_neighbors=ell,B7_neighbors=q,incident_deficit=D,retained=retained))
        if retained:surviving.append((ell,q,D))
    if surviving!=[(2,0,0)]:raise ValueError('Complete low-vertex deficit table')

    DG=[8]*3+[10]*6
    counts=Counter();forced=[]
    for word in range(4096):
        H=local(word);degrees=list(map(len,H))
        if sum(degrees)!=24 or max(degrees)>3:continue
        counts['H12_max3_words']+=1
        caps={(u,v):(2 if v in H[u] else DG[u]+DG[v]-15)-len(H[u]&H[v]) for u,v in combinations(range(9),2)}
        total=sum(caps.values())
        if total!=(87 if degrees[0]==2 else 93):raise ValueError('Marked low-profile A capacity')
        if total<93:continue
        counts['capacity_equality_words']+=1
        if any(len(H[u]&set(range(3)))!=2 for u in range(3)):continue
        counts['low_triangle_words']+=1
        low_Gram=[]
        for u in range(3):
            low_Gram.append(4+sum(caps[min(u,v),max(u,v)] for v in range(9) if v!=u))
        if low_Gram!=[20]*3:continue
        counts['forced_shape_words']+=1;forced.append(word)
        mid=next(i for i in [1,2] if degrees[3*i]==2)
        top=3-mid
        L=set(range(3));M=set(range(3*mid,3*mid+3));T=set(range(3*top,3*top+3))
        if any(len(H[u]&M)!=1 or H[u]-L-M for u in L):raise ValueError('Low-to-mid matching')
        if any(len(H[u]&L)!=1 or len(H[u]&T)!=1 or H[u]&M for u in M):raise ValueError('Mid matchings')
        if any(len(H[u]&M)!=1 or len(H[u]&T)!=2 or H[u]&L for u in T):raise ValueError('Top triangle/matching')
        if any(caps[min(u,v),max(u,v)]!=2 for u in L for v in M):raise ValueError('Exact L-M Gram block')
        if any(caps[u,v]!=5 for u,v in combinations(sorted(M),2)):raise ValueError('Exact M-M blue Gram')
        if any(caps[u,v]!=1 for u,v in combinations(range(3),2)):raise ValueError('Exact L-L red Gram')
    shapes=set()
    for mid in [1,2]:
        top=3-mid
        for lm,mt in product(range(3),repeat=2):
            H=[set() for _ in range(9)]
            edges=[]
            for orbit in [0,top]:
                edges.extend((3*orbit+t,3*orbit+(t+1)%3) for t in range(3))
            edges.extend((t,3*mid+(t+lm)%3) for t in range(3))
            edges.extend((3*mid+t,3*top+(t+mt)%3) for t in range(3))
            for u,v in edges:H[u].add(v);H[v].add(u)
            words=[w for w in forced if local(w)==H]
            if len(words)!=1:raise ValueError('Distinct forced shape decoding')
            shapes.add(words[0])
    if shapes!=set(forced) or len(shapes)!=18:raise ValueError('Entire forced H shape domain')

    low_weights=[r for r in product(range(4),repeat=3) if sum(r)==4 and sum(x*(x-1)//2 for x in r)==1]
    if sorted(low_weights)!=[(1,1,2),(1,2,1),(2,1,1)]:raise ValueError('Complete low column weights')
    mid_cases=[]
    for m0,mU,mV,mW in product(range(3),range(4),range(1,4),range(1,4)):
        if m0+mU+mV+mW!=7 or 2*mU+mV+mW!=6:continue
        if not all(0<=t<=3 for t in [2-m0,3-mU,4-mV,4-mW]):continue
        pair_common=sum(m*(m-1)//2 for m in [m0,mU,mV,mW])
        if pair_common==5:raise ValueError('Unexpected tight-Gram scalar solution')
        mid_cases.append(dict(weights=[m0,mU,mV,mW],actual_pair_common=pair_common,required_pair_common=5))
    if [r['weights'] for r in mid_cases]!=[[1,0,3,3],[2,1,1,3],[2,1,2,2],[2,1,3,1]]:
        raise ValueError('Whole four scalar cases')

    # No phase-normalization premise: every labeled9-column seed, literal sets.
    orbit_checks=0
    for mask in range(512):
        cols=[{3*(u//3)+(u%3+s)%3 for u in range(9) if mask>>u&1} for s in range(3)]
        for orbit in range(3):
            points=list(range(3*orbit,3*orbit+3))
            m=len(cols[0]&set(points))
            for u,v in combinations(points,2):
                actual=sum(u in c and v in c for c in cols)
                if actual!=m*(m-1)//2:raise ValueError('Literal C3 same-orbit pair identity')
                orbit_checks+=1
    record=dict(status='COMPLETE_ORDINARY_LOW_PROFILE_BRIDGE_CHECKS',agent='six-books-2',role='researcher',
                root_mark_choices=35,surviving_root_marks=len(root_marks),root_degree_sum=84,root_deficit=3,
                deficit_weight=6,remaining_nonroot_deficit=3,low_vertex_table=low_table,H_counts=dict(counts),
                forced_H_words=sorted(forced),low_column_weights=[list(r) for r in low_weights],
                mid_scalar_cases=mid_cases,solutions=0,labeled_column_seeds=512,literal_same_orbit_pair_checks=orbit_checks,
                trust='Ordinary proof bridges checked literally; no X/K/host census or prior classification used; unformalized, independent peer review pending.')
    return record

def main():
    p=ArgumentParser();p.add_argument('--work',type=Path,required=True);args=p.parse_args()
    start=time.monotonic();record=derive()
    raw=json.dumps(record,sort_keys=True,separators=(',',':'),allow_nan=False)+'\n'
    args.work.mkdir(parents=True,exist_ok=True);(args.work/'low-profile.json').write_text(raw)
    if time.monotonic()-start>25:raise RuntimeError('INCOMPLETE low-profile guard; no exclusion')
    print(json.dumps(dict(record=record,bytes=len(raw.encode()),sha256=hashlib.sha256(raw.encode()).hexdigest(),seconds=time.monotonic()-start,peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss),indent=2))

if __name__=='__main__':main()
