"""Checks using hypergeometric probabilities and direct finite definitions."""
from fractions import Fraction as F
from itertools import combinations,permutations
from math import comb
import model as M

def C(n,k):return comb(n,k) if 0<=k<=n else 0

def audit_coefficients(configurations):
    checked=0
    for v,s,r,pos in sorted(configurations,key=str):
        pos=tuple(range((v-s)//2,(v-s)//2+s)) if pos is None else pos
        N=v-s;den,table=M.coefficients(v,s,r,pos)
        for k,(first,last,pairs,mark,L,R) in enumerate(table):
            ff={};ll={};pp={}
            # Derive eligible fixed vertices directly from their assigned ranks.
            for A in range(1<<s):
                a=r-A.bit_count();fixed=[pos[i] for i in range(s) if A>>i&1]
                if not 0<=a<=N:continue
                if mark:
                    if k in fixed and all(p<=k for p in fixed):ff[A]=F(C(L,a),C(N,a))
                    if k in fixed and all(p>=k for p in fixed):ll[A]=F(C(R,a),C(N,a))
                elif a:
                    if all(p<k for p in fixed):ff[A]=F(a,N)*F(C(L,a-1),C(N-1,a-1))
                    if all(p>k for p in fixed):ll[A]=F(a,N)*F(C(R,a-1),C(N-1,a-1))
            for A in ff:
                for B in ll:
                    a=r-A.bit_count();b=r-B.bit_count()
                    if mark and A&B==mark and a+b<=N:
                        pp[A,B]=F(C(L,a)*C(R,b),C(N,a)*C(N-a,b))
                    elif not mark and not A&B and a+b-1<=N:
                        pp[A,B]=F(1,N)*F(C(L,a-1)*C(R,b-1),C(N-1,a-1)*C(N-a,b-1))
            assert {A:x for A,x in ff.items() if x}=={A:F(c,den) for A,c in first if c}
            assert {A:x for A,x in ll.items() if x}=={A:F(c,den) for A,c in last if c}
            assert {AB:x for AB,x in pp.items() if x}=={(A,B):F(c,den) for A,B,c in pairs if c}
        checked+=1
    return checked

def audit_pair_partitions(expected):
    # Independently select disjoint cliques of size>=3; all uncovered pairs
    # must be size-two blocks. No first-uncovered-pair recursion is used.
    ps=list(combinations(range(6),2));idx={p:i for i,p in enumerate(ps)}
    large=[]
    for n in [3,4,5]:
        for vs in combinations(range(6),n):
            large.append((sum(1<<idx[p] for p in combinations(vs,2)),sum(1<<i for i in vs)))
    got=set()
    def rec(i,used,blocks):
        if i==len(large):
            rest=[(1<<a)|(1<<b) for j,(a,b) in enumerate(ps) if not used>>j&1]
            got.add(tuple(sorted(blocks+rest)));return
        rec(i+1,used,blocks)
        bits,mask=large[i]
        if not bits&used:rec(i+1,used|bits,blocks+[mask])
    rec(0,0,[])
    assert got==expected
    return len(got)

def audit_small_controls():
    from collections import Counter
    v=6;r=3;edges=list(combinations(range(v),r));sets=list(map(set,edges));events=0
    for pos in [(),(2,),(1,4),(4,1,3)]:
        s=len(pos);free_slots=[i for i in range(v) if i not in pos]
        lasts=Counter();firsts=Counter();both=Counter()
        pairs=[(i,j) for i,E in enumerate(sets) for j,G in enumerate(sets) if len(E&G)==1]
        for free in permutations(range(s,v)):
            rank=dict(enumerate(pos));rank.update({x:k for x,k in zip(free,free_slots)})
            lo=[min(rank[x] for x in E) for E in edges];hi=[max(rank[x] for x in E) for E in edges]
            for i in range(len(edges)):lasts[i,hi[i]]+=1;firsts[i,lo[i]]+=1
            for i,j in pairs:
                if hi[i]==lo[j]:both[i,j,hi[i]]+=1
        den,cs=M.coefficients(v,s,r,pos)
        masks=[sum(1<<x for x in E if x<s) for E in edges]
        for k,(aa,bb,ab,*_) in enumerate(cs):
            aa=dict(aa);bb=dict(bb);ab={(A,B):c for A,B,c in ab}
            for i,A in enumerate(masks):
                assert lasts[i,k]==aa.get(A,0);assert firsts[i,k]==bb.get(A,0);events+=2
            for i,j in pairs:assert both[i,j,k]==ab.get((masks[i],masks[j]),0);events+=1
    # Direct colorability on all 1024 hypergraphs on five vertices with 3-edges.
    ee=[sum(1<<i for i in E) for E in combinations(range(5),3)];positive=0
    for h in range(1<<len(ee)):
        es=[e for j,e in enumerate(ee) if h>>j&1]
        colorable=any(all(c&e not in (0,e) for e in es) for c in range(32))
        x=[sum(1 for e in es if e&3==a) for a in range(4)]
        a,b=M.bound(5,x,r=3,positions=(1,3))
        if a<b:assert colorable;positive+=1
    # Verify the star collision inequality on every covering family of
    # distinct 4-subsets of a 6-element set (the relevant uniformity 5 links).
    blocks=[sum(1<<i for i in E) for E in combinations(range(6),4)];families=0
    for mask in range(1<<len(blocks)):
        bs=[b for i,b in enumerate(blocks) if mask>>i&1]
        union=0
        for b in bs:union|=b
        if union!=63:continue
        overlap=sum(bool(a&b) for a,b in combinations(bs,2))
        excess=4*len(bs)-6
        assert overlap>=(excess+2)//3
        families+=1
    return {'direct_permutation_event_checks':events,'hypergraphs_checked':1024,
            'certified_colorable_controls':positive,'covering_link_families_checked':families}
