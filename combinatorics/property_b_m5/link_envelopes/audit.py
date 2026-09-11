"""Definition-level checks for the new link and forest inequalities."""
from itertools import combinations, product
from fractions import Fraction as F
from math import comb
from random import Random
from star_envelope import envelope, count_critical, overlap_types
from forest import tail, star_bound, pair_tail, M

def bits(vs): return sum(1<<i for i in vs)

def audit_links():
    # Directly enumerate labeled free sets; neither signature generation nor its
    # color-counting dynamic program is used for the reference maximum.
    checks=0
    for N,sizes in [(4,(2,2,2)),(5,(2,2,2)),(6,(3,3,3)),(5,(1,2,3))]:
        choices=[[bits(c) for c in combinations(range(N),a)] for a in sizes]
        families=[fs for fs in product(*choices) if fs[0]|fs[1]|fs[2]==(1<<N)-1]
        for flags in [(3,3,3),(1,2,3),(0,1,2),(3,0,3)]:
            rows=tuple(sorted(zip(sizes,flags)))
            for L in range(1,N):
                cuts=[bits(c) for c in combinations(range(N),L)]
                best=0
                for fs in families:
                    count=0
                    for cut in cuts:
                        left=any(f&1 and E&cut==E for E,f in zip(fs,flags))
                        right=any(f&2 and E&cut==0 for E,f in zip(fs,flags))
                        count+=left and right
                    best=max(best,count)
                actual=envelope(rows,N,L,3)
                assert actual is not None and actual[:2]==(best,comb(N,L))
                checks+=1
    return checks

def audit_forests():
    rng=Random(20260911);checks=0
    for N,r,L in [(6,2,3),(8,3,4),(10,3,5),(12,4,6)]:
        es=[bits(c) for c in combinations(range(N),r)]
        cuts=[bits(c) for c in combinations(range(N),L)]
        # All small graph families, plus fixed-seed exact hypergraph controls.
        if (N,r)==(6,2):
            families=(z for d in range(1,5) for z in combinations(es,d))
        else:
            families=(rng.sample(es,rng.randrange(1,min(35,len(es))+1)) for _ in range(100))
        for fs in families:
            actual=F(sum(any(E&cut in (0,E) for E in fs) for cut in cuts),len(cuts))
            assert actual<=tail(N,L,r,len(fs))
            checks+=1
        # Check every possible pair intersection against direct subset counts.
        for i in range(r):
            E=(1<<r)-1
            G=((1<<i)-1)|sum(1<<j for j in range(r,2*r-i))
            actual=F(sum(E&cut in (0,E) and G&cut in (0,G) for cut in cuts),len(cuts))
            assert actual==pair_tail(N,L,r,i)
    return checks

def audit_pivots():
    # All covering families of 2-subsets on six vertices, with 3..6 link edges.
    N=6;r=3;L=3;es=[bits(c) for c in combinations(range(N),2)]
    cuts=[bits(c) for c in combinations(range(N),L)];checks=0
    for d in range(3,7):
        for fs in combinations(es,d):
            union=0
            for E in fs:union|=E
            if union!=(1<<N)-1:continue
            actual=F(sum(any(E&cut==E for E in fs) and any(E&cut==0 for E in fs) for cut in cuts),len(cuts))
            # Isolate the pivot term from the displayed star formula (tail=0).
            assert actual<=star_bound(N+1,d,d,r)
            checks+=1
    # Larger cuts exercise the nonzero shared-endpoint forest correction.
    N=8;L=4;es=[bits(c) for c in combinations(range(N),2)]
    cuts=[bits(c) for c in combinations(range(N),L)];rng=Random(314159);accepted=0
    while accepted<300:
        d=rng.randrange(5,10);fs=rng.sample(es,d);union=0
        for E in fs:union|=E
        if union!=(1<<N)-1:continue
        actual=F(sum(any(E&cut==E for E in fs) and any(E&cut==0 for E in fs) for cut in cuts),len(cuts))
        assert actual<=star_bound(N+1,d,d,r)
        checks+=1;accepted+=1
    return checks

if __name__=='__main__':
    print({'link_envelope_maxima':audit_links(),'tail_union_families':audit_forests(),'covering_pivot_families':audit_pivots()})
