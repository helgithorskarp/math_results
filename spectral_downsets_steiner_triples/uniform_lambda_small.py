"""Exact H for every feasible simple 2-(v,3,lambda), lambda>=2.

For v>=5, UNIFORM_LAMBDA_ALL_ORDERS.md proves centered rank N-v-1
and repaired rank N-v for every real 0<eta<=1/(8v^2). The only feasible
smaller input is v=4,lambda=2; its known unique slack has rank seven.
Cap bounds retain only their separately proved parameter ranges.
Standard library only. Author: six-downset-2, researcher.
"""
from collections import Counter
from fractions import Fraction as F
from itertools import combinations
from certificates import mask,ordered


def parameters(v,lam):
    assert type(v) is int and type(lam) is int
    assert v>=4 and 2<=lam<=v-2
    assert lam*(v-1)%2==0 and lam*v*(v-1)%6==0
    m,b,r=v*(v-1)//2,lam*v*(v-1)//6,lam*(v-1)//2
    return m,b,r,v+r,1+v+m+b


def weights(v,lam):
    parameters(v,lam);assert v>=5
    r=F(lam*(v-1),2);s=v+r
    c=F(3*v*v-3*(lam+3)*v+11*lam,3*(v-2)*(v-3))
    d=F(v*v-v-4,(v-4)*(v-3))
    if (v,lam)==(5,3):t=F(6)
    elif (v,lam)==(6,2):t=F(2)
    else:
        D=lam*(v*v-10*v+27)-6
        assert D>0
        t=F((v-1)*(lam*(v-3)-6),D)
    return {'a':F(-lam,3),'c':c,'d':d,'t':t,
            'w':s-(v-3)*c-(r-2*lam)*d,
            'h':s-(v-4)*d-(r-3*lam)*t}


def design_data(v,lam,blocks):
    m,b,r,_,_=parameters(v,lam)
    assert len(blocks)==b and len(set(blocks))==b
    pairs=[mask(p) for p in combinations(range(v),2)]
    completing={p:[] for p in pairs};replication=Counter()
    for block in blocks:
        assert type(block) is int and 0<block<1<<v and block.bit_count()==3
        points=[x for x in range(v) if block>>x&1];replication.update(points)
        for p in combinations(points,2):completing[mask(p)].append(block^mask(p))
    assert all(len(xs)==len(set(xs))==lam for xs in completing.values())
    assert all(replication[x]==r for x in range(v)) and len(pairs)==m
    codegrees=Counter()
    for xs in completing.values():codegrees.update(x|y for x,y in combinations(xs,2))
    outside={}
    for block in blocks:
        counts=Counter()
        for p in combinations([x for x in range(v) if block>>x&1],2):
            for x in completing[mask(p)]:
                if not x&block:counts[x.bit_length()-1]+=1
        assert sum(counts.values())==3*(lam-1)
        outside[block]=counts
    return pairs,completing,codegrees,outside


def centered_certificate(v,lam,blocks):
    pairs,_,codegrees,outside=design_data(v,lam,blocks)
    _,_,_,s,N=parameters(v,lam)
    D=ordered({0}|{1<<x for x in range(v)}|set(pairs)|set(blocks))
    assert len(D)==N
    if v==4:
        # Known proper-four-cube certificate, graph8020/review8066.
        assert lam==2 and set(D)==set(range(15))
        Q=[[F(1) if not a or not b else F(7) if a==b or a^b==15 else F(0)
            for b in D] for a in D]
        return D,s,Q
    w=weights(v,lam);u=lam*(lam-1)//2;U=set(blocks)
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
    if v==4:return F(14)  # Known proper-four-cube spectrum.
    if lam==2 and v>=13:return F(28*v,5)  # Review8010.
    if lam==2 and v>=9:return F(20*v,3)  # Small-order theorem7978/review8034.
    if lam==3 and v>=13:return F(25*v,2)  # Threefold theorem8028.
    if v>=24*lam:return F(2*lam*lam*v)  # All-multiplicity theorem8082.
    return None


def cap_gap(v,lam):
    bound=cap_bound(v,lam)
    if bound is None:return None
    delta=parameters(v,lam)[4]-bound;assert delta>0
    return delta


def maximal_certificate(v,lam,blocks,centered=None,eta=None):
    if centered is None:centered=centered_certificate(v,lam,blocks)
    D,s,Qc=centered;m,_,_,expected_s,N=parameters(v,lam)
    assert s==expected_s and len(D)==N
    if v==4:
        assert eta is None
        return D,s,[row[:] for row in Qc],F(0)
    k=(v-2)*(v-3)//2
    if eta is None:
        eta=F(1,8*v*v);delta=cap_gap(v,lam)
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
    """Eleven literal controls; first-witness constructions, never a census."""
    for v,lam in ((4,2),(5,3),(6,4)):
        yield 'complete'+str(v),v,lam,[mask(p) for p in combinations(range(v),3)],{'kind':'all triples'}
    blocks=sorted({mask((x+j)%5 for x in (0,1,3)) for j in range(5)}|
                  {mask((5,i,(i+1)%5)) for i in range(5)})
    yield 'rotational_twofold6',6,2,blocks,{'modulus':5,'seed':[0,1,3],'extra_point':5,'extra_pairs':'cyclic neighbors'}
    all7={mask(p) for p in combinations(range(7),3)}
    one={mask((x+j)%7 for x in (0,1,3)) for j in range(7)}
    two=one|{mask((x+j)%7 for x in (0,1,5)) for j in range(7)}
    for lam,blocks in ((2,two),(3,all7-two),(4,all7-one),(5,all7)):
        yield 'cyclic_lambda'+str(lam)+'_7',7,lam,sorted(blocks),{'modulus':7,'first_STS_seed':[0,1,3],'second_STS_seed':[0,1,5],'lambda':lam}
    # Retained literal input from the prior three-STS9 artifact7705.
    layers=[[7,56,73,84,98,140,146,161,266,273,292,448],
            [11,21,44,70,112,152,162,193,274,289,328,388],
            [13,19,38,88,97,138,176,196,276,296,322,385]]
    yield 'retained_threefold9',9,3,sorted(A for layer in layers for A in layer),{'kind':'prior three-STS9 fixture','layers':layers}
    seeds10=[(0,1,2),(0,1,3),(0,1,5),(0,2,5),(0,2,6),(0,3,6)]
    seeds12=[(0,4,8),(0,1,2),(0,1,3),(0,1,5),(0,2,6),(0,2,7),(0,3,6),(0,3,7)]
    for v,seeds in ((10,seeds10),(12,seeds12)):
        blocks=sorted({mask((x+j)%v for x in seed) for seed in seeds for j in range(v)})
        yield 'cyclic_lambda4_'+str(v),v,4,blocks,{'modulus':v,'seeds':[list(p) for p in seeds]}
