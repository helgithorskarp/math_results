"""Rational maximal-rank H for every simple2-(v,3,lambda),v>=13,lambda>=2.

All inputs are checked literally. UNIFORM_LAMBDA_PROOF.md proves the scope.
A cap is proved atv>=24lambda; tighter prior bounds coverlambda2/3 atv>=13.
None from cap_bound means no uniform cap claimed here, not cap nonexistence.
Standard library only. Author: six-downset-2, researcher.
"""
from collections import Counter
from fractions import Fraction as F
from itertools import combinations
from certificates import mask,ordered


def parameters(v,lam):
    assert type(v) is int and type(lam) is int
    assert v>=13 and 2<=lam<=v-2
    assert lam*(v-1)%2==0 and lam*v*(v-1)%6==0
    m,b,r=v*(v-1)//2,lam*v*(v-1)//6,lam*(v-1)//2
    return m,b,r,v+r,1+v+m+b


def weights(v,lam):
    parameters(v,lam)
    r=F(lam*(v-1),2)
    s=v+r
    D=lam*(v*v-10*v+27)-6
    assert D>0
    c=F(3*v*v-3*(lam+3)*v+11*lam,3*(v-2)*(v-3))
    d=F(v*v-v-4,(v-4)*(v-3))
    t=F((v-1)*(lam*(v-3)-6),D)
    return {'a':F(-lam,3),'c':c,'d':d,'t':t,
            'w':s-(v-3)*c-(r-2*lam)*d,
            'h':s-(v-4)*d-(r-3*lam)*t}


def design_data(v,lam,blocks):
    m,b,r,_,_=parameters(v,lam)
    assert len(blocks)==b and len(set(blocks))==b
    pairs=[mask(p) for p in combinations(range(v),2)]
    completing={p:[] for p in pairs}
    replication=Counter()
    for block in blocks:
        assert type(block) is int and 0<block<1<<v and block.bit_count()==3
        points=[x for x in range(v) if block>>x&1]
        replication.update(points)
        for p in combinations(points,2):completing[mask(p)].append(block^mask(p))
    assert all(len(xs)==len(set(xs))==lam for xs in completing.values())
    assert all(replication[x]==r for x in range(v)) and len(pairs)==m
    codegrees=Counter()
    for xs in completing.values():codegrees.update(x|y for x,y in combinations(xs,2))
    outside={}
    for block in blocks:
        counts=Counter()
        points=[x for x in range(v) if block>>x&1]
        for p in combinations(points,2):
            for x in completing[mask(p)]:
                if not x&block:counts[x.bit_length()-1]+=1
        assert sum(counts.values())==3*(lam-1)
        outside[block]=counts
    return pairs,completing,codegrees,outside


def centered_certificate(v,lam,blocks):
    pairs,_,codegrees,outside=design_data(v,lam,blocks)
    _,_,_,s,N=parameters(v,lam)
    w=weights(v,lam);u=lam*(lam-1)//2
    D=ordered({0}|{1<<x for x in range(v)}|set(pairs)|set(blocks))
    assert len(D)==N
    U=set(blocks)
    Q=[[F(0)]*N for _ in D]
    for i,a in enumerate(D):
        for j in range(i,N):
            b=D[j]
            if a&b:value=F(s if i==j else 0)
            elif not a or not b:value=F(1)
            else:
                ka,kb=a.bit_count(),b.bit_count()
                if ka>kb:a0,b0,ka,kb=b,a,kb,ka
                else:a0,b0=a,b
                if (ka,kb)==(1,1):value=w['a']+w['t']*(codegrees[a0|b0]-u)
                elif (ka,kb)==(1,2):value=w['w']-w['d']*int(a0|b0 in U)
                elif (ka,kb)==(1,3):value=w['h']-w['t']*outside[b0].get(a0.bit_length()-1,0)
                elif (ka,kb)==(2,2):value=w['c']
                elif (ka,kb)==(2,3):value=w['d']
                else:
                    assert (ka,kb)==(3,3)
                    value=w['t']
            Q[i][j]=Q[j][i]=value
    return D,s,Q


def cap_bound(v,lam):
    parameters(v,lam)
    if lam==2:return F(28*v,5)  # Independently proved refinement8010.
    if lam==3:return F(25*v,2)  # Prior degree-three theorem8028.
    if v>=24*lam:return F(2*lam*lam*v)
    return None


def cap_gap(v,lam):
    bound=cap_bound(v,lam)
    if bound is None:return None
    delta=parameters(v,lam)[4]-bound
    assert delta>0
    return delta


def maximal_certificate(v,lam,blocks,centered=None,eta=None):
    if centered is None:centered=centered_certificate(v,lam,blocks)
    D,s,Qc=centered
    m,_,_,expected_s,N=parameters(v,lam)
    assert s==expected_s and len(D)==N
    k=(v-2)*(v-3)//2
    if eta is None:
        eta=F(1,8*v*v)
        delta=cap_gap(v,lam)
        if delta is not None:eta=min(eta,delta/(8*m*k))
    assert 0<eta<=F(1,8*v*v)
    Qm=[row[:] for row in Qc]
    for i,a in enumerate(D):
        for j in range(i,N):
            b=D[j]
            if a&b:change=0
            elif not a and not b:change=m*k
            elif not a or not b:
                size=(a|b).bit_count()
                change=-(v-1)*k if size==1 else (k if size==2 else 0)
            else:
                sizes=sorted((a.bit_count(),b.bit_count()))
                change=2*k if sizes==[1,1] else (-(v-3) if sizes==[1,2] else (1 if sizes==[2,2] else 0))
            Qm[i][j]=Qm[j][i]=Qc[i][j]+eta*change
    return D,s,Qm,eta


def fixtures():
    """Four literal validation designs, not a design census."""
    from uniform_twofold import nonbijective_fixture
    from uniform_threefold import fixtures as old_threefold
    blocks,permutation=nonbijective_fixture(13)
    yield 'nonbijective_twofold13',13,2,blocks,{'kind':'retained twofold fixture','permutation':permutation}
    for name,v,blocks,generation in old_threefold():
        if name=='nondecomposable13':
            yield 'nondecomposable_threefold13',v,3,blocks,generation
    seeds4=[(0,1,2),(0,1,3),(0,1,5),(0,2,6),(0,2,7),(0,3,7),(0,3,8),(0,3,9)]
    seeds5=[(0,1,2),(0,1,3),(0,1,4),(0,1,5),(0,2,6),(0,2,7),(0,2,8),(0,3,7),(0,3,8),(0,3,9)]
    for lam,seeds in ((4,seeds4),(5,seeds5)):
        blocks=sorted({mask((x+j)%13 for x in seed) for seed in seeds for j in range(13)})
        design_data(13,lam,blocks)
        yield 'cyclic_lambda'+str(lam)+'_13',13,lam,blocks,{'modulus':13,'seeds':[list(p) for p in seeds]}
