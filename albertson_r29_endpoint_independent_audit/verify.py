#!/usr/bin/env python3
"""Independent exact audit; standard library; no import of the target checker.

The code checks integer/rational consequences of the written proof. Imported
structural theorems and the graph-to-Hall reductions remain ordinary proofs.
"""
from fractions import Fraction as Q
from math import comb
import json


def ceil(x):
    return -((-x.numerator) // x.denominator)


def hill(r):
    return (r // 2) * ((r-1)//2) * ((r-2)//2) * ((r-3)//2) // 4


def sampling(n, m, q):
    # Sum over q-subsets BEFORE cancelling binomial coefficients.
    return (5*m*comb(n-2, q-2)-Q(203*(q-2), 9)*comb(n, q))/comb(n-4, q-4)


def join_floor(r, n):
    # Enumerate both integer coordinates, not the paper's concavity formula.
    vals = []
    for k in range(4, r):
        for a in range(2*k-1, n-r+k+1):
            b = n-a
            vals.append(ceil(Q(a*k+b*(r-k-1), 2)+a*b))
    assert vals
    return min(vals)


def order_audit(r, equality_refinement=False):
    # BK cubic bound + minimum degree r; no imported order-range theorem.
    cutoff = ceil(Q(8*41209*hill(r), 1500*r**3))
    assert Q(r,2) >= Q(203,30)
    rows, survivors = [], []
    for n in range(r+5, cutoff):
        m = ceil(Q(r*n, 2))
        if n <= 2*r-1:
            correction = 1 if equality_refinement and n <= 2*r-2 else 2
            m = max(m, ceil(Q((r-1)*n+(n-r)*(2*r-n)-correction, 2)))
        if n <= 2*r-2:
            m = max(m, join_floor(r,n))
        best, q = max((sampling(n,m,q), q) for q in range(4,n+1))
        if ceil(best) >= hill(r):
            rows.append([n,m,q,str(best), 'excluded'])
        else:
            top=m
            while max(ceil(sampling(n,top+1,q)) for q in range(4,n+1)) < hill(r):
                top+=1
            survivors.append([n,m,top])
            rows.append([n,m,q,str(best),'residual through '+str(top)])
    return {'r':r,'target':hill(r),'small_orders_through':r+4,
            'large_orders_from':cutoff,'large_order_bound_at_cutoff':str(Q(1500*r**3*cutoff,8*41209)),
            'gallai_equality_refinement':equality_refinement,'rows':rows,'residual':survivors}


def odd_at_least(x):
    x=max(1,x)
    return x if x%2 else x+1


def barriers(n,delta,u):
    # Remove u even/odd seed vertices. Tutte gives o >= s-u+2.
    return [s for s in range(u,n+1)
            if (s-u+2)*odd_at_least(delta-s+1) <= n-s]


def finite_checks():
    out={}
    raw57={a:barriers(57,27-a,3) for a in (1,3,5,7,9)}
    expected={1:[3,26,27,28,29],3:[3,24,25,26,27,28,29],
              5:[3,*range(22,30)],7:[3,4,*range(20,30)],
              9:[3,4,*range(18,30)]}
    assert raw57==expected
    reductions=[]
    for a,ss in raw57.items():
        remaining=[]
        for s in ss:
            if s==29:
                remaining.append(s);continue
            if s<=4:
                colors=57-(s-1)*(27-a-s)
                assert colors<29
            else:
                emax=Q((59-2*s)*(58-2*s)+27*(2*s-57)+a,2)
                assert emax<0
        assert remaining==[29]
        reductions.append([a,remaining])
    out['order57_barriers']={str(a):v for a,v in raw57.items()}
    out['order57_remaining_barriers']=reductions
    out['order57_hall_bad_vertices']=[r*(27-r) for r in range(2,12)]
    assert min(out['order57_hall_bad_vertices'])==50>36
    assert 26>19 and 26>9
    assert 2*27-19>28  # common neighbor of an S-edge
    # Triangle-free exceptional branch: this is a numeric check of the proof.
    assert 5*23>2*56 and 5*25>2*55 and 21+22>28
    for a in (5,7,9):
        for rem in range(min(3,a-5)+1):
            assert 27-a+rem>4+2*rem
    ss=barriers(58,26,6)
    assert ss==[6,26,27,28,29,30,31]
    out['order58_barriers']=ss
    caps=[]
    for s in (26,27,28):
        cap=comb(63-2*s,2)+28*(s-29)+1
        assert cap<0;caps.append([s,cap])
    out['order58_intermediate_edge_caps']=caps
    assert 58-2*20<29
    assert (4*17-15)**2 < 48*58+73 <= (4*18-15)**2
    out['rabern_order58_ceiling']=18
    fmin=min(max(x*(y-5),y*(x-4)) for x in range(1,28)
             for y in range(1,29) if x+y>=24)
    assert fmin==18
    out['two_triangle_edge_family_minimum']=fmin
    # Complete Hall failure parameter ranges, not selected failures.
    out['s29_hall_upper_cross_degree']=[r+3 for r in range(1,8)]
    assert max(out['s29_hall_upper_cross_degree'])<26-11
    out['s30_standard_hall_incident_edges']=[r*(25-r)-comb(r,2) for r in range(2,7)]
    assert min(out['s30_standard_hall_incident_edges'])==45>32
    # New independent shortcut: ell has d_X=0, hence d_S(ell)>=26.
    other_s_degree_max=32-26+1
    other_cross_min=26-other_s_degree_max
    common_min=2*other_cross_min-28
    left_min=26-2-5  # X after deleting five vertices of S
    right_min=other_cross_min-3  # S after deleting three vertices of X
    assert (other_s_degree_max,other_cross_min,common_min,left_min,right_min)==(7,19,10,19,16)
    assert common_min>2 and left_min+right_min>=25
    out['s30_zero_shortcut']={'other_s_degree_max':7,'other_cross_min':19,
         'common_anchors_min':10,'remaining_sides':[25,25],
         'bipartite_min_degrees':[19,16]}
    assert 2*48-9>57 and 48+26-3>57 and 3*26-3>57
    assert 57-(2*26-1)==6 and 26-(6+2)==18
    assert 2*18-27==9
    out['s31_incident_edge_contradictions']=[87,71,75]
    partitions={
      's29':[(3,2),(2,1),(2,25)],
      's30_standard':[(3,2),(2,26)],
      's30_zero':[(3,2),(2,1),(2,25)],
      's31_split':[(3,2),(2,1),(2,25)],
      's31_two_zeros':[(2,1),(3,2),(2,25)]}
    for p in partitions.values():
        assert sum(size*count for size,count in p)==58
        assert sum(count for _,count in p)==28
    out['terminal_partition_accounting']=partitions
    # Scope guard: the theorem's stronger minimum degree changes its rows.
    assert ceil(Q(29*57,2))==827 and ceil(Q(29*58,2))==841
    assert 840 < ceil(Q(29*58,2))
    return out


def main():
    r29=order_audit(29);r30=order_audit(30, equality_refinement=True)
    assert r30['residual']==[[59,885,891],[60,900,903],[61,915,915]]
    assert r29['residual']==[[57,827,831],[58,841,842]]
    assert join_floor(29,57)==840
    assert join_floor(30,59)==899
    assert ceil(sampling(59,899,24))>hill(30)
    assert ceil(sampling(57,840,24))>hill(29)
    result={'status':'PASS: exact arithmetic and complete listed proof cases; see ordinary-proof boundary',
        'r29':r29,'finite':finite_checks(),'r30_reusable_reduction':r30,
        'r30_status':'Reduction only; no closure or Albertson r=30 claim'}
    print(json.dumps(result,indent=2,sort_keys=True))


if __name__=='__main__':
    main()
