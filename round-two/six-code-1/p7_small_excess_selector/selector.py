"""Check the exact hypotheses and capacities of the ordinary selector.

These are abstract necessary rows, not an actual packing realization.
Imported local9045 and the written coverage/leave bridge remain premises.
"""
from row_types import need


def capacity(eligible, uv_words, outside_edges):
    covered = eligible - (15-3*uv_words)
    usable = covered - 2*outside_edges
    need(0 <= uv_words <= 5 and 0 <= outside_edges <= 28,
         'invalid coverage/edge domain')
    need(usable > 0, 'pigeonhole does not force a usable marked point')
    return dict(eligible=eligible, covered_lower_bound=covered,
                outside_edges=outside_edges, usable_lower_bound=usable)


def orientation(first, second, isolated, low, remaining):
    """Only the three hub entries are specified; SS rows are unit elsewhere."""
    need(sorted((isolated,low,remaining)) == [0,1,2], 'hub marks not distinct')
    need(first[isolated] in (1,2), 'first isolated deficit is not one or two')
    need(first[low] == first[remaining] == 0, 'first extra deficient hub')
    need(second[isolated] == second[low] == 0, 'second specified marks not low')
    need(second[remaining] == 1, 'second row not unit at its remaining hub')
    return True


def rows_of(case, survivor):
    rows=[list(r) for r in survivor['exceptional_rows']]
    for dh,n in zip(((0,0,0),(1,0,0),(0,1,0),(0,0,1)),survivor['base_counts']):
        # Unit rows with no hub, or one isolated hub.
        row=list(dh)+( [0,0,5-sum(dh)] )+list(dh)
        rows.extend([row]*n)
    need(len(rows)==15, 'incomplete row inventory')
    need(tuple(sum(r[j] for r in rows) for j in range(3))==tuple(case['cross_weights']),
         'cross weights do not match inventory')
    return rows


def check(case, survivor):
    rows=rows_of(case,survivor)
    need(survivor['X']==survivor['tau']==0, 'selector requires unit SS and tau zero')
    E=case['E'];a,b,c=case['pair_multiplicities']
    if E<=1:
        need(case['t']==0, 'small-excess selector needs uncovered H triple')
        support=[sum(d>0 for d in r[:3]) for r in rows]
        if E==0:
            need([support.count(j) for j in range(4)]==[0,13,0,2], 'E0 support pattern')
            need((a,b,c)==(1,1,5), 'E0 pair boundary')
        else:
            need([support.count(j) for j in range(4)]==[0,13,1,1], 'E1 support pattern')
            need((a,b,c) in ((1,1,5),(1,2,4)), 'E1 pair boundary')
        A=[r for r,k in zip(rows,support) if k==1 and r[0]>0 and r[4]==0]
        need(all(r[3] in (0,1) and r[0]==1+r[3] for r in A), 'A row scope')
        need(sum(r[3] for r in A)<=1, 'more than one mixed A row')
        degree=sum(r[5] for r in A);need(degree<=28, 'A independence capacity')
        eligible=[r for r,k in zip(rows,support) if k==1 and r[0]==0 and
                  r[3]==r[4]==0 and r[1]+r[2]==1]
        cap=capacity(len(eligible),c,28-degree)
        for r in eligible:
            U=1 if r[1] else 2;V=3-U
            for y in A:
                if y[3]==0:
                    orientation(r[:3],y[:3],U,V,0)
                else:
                    # Mixed second rows violate9045; the reverse direction is valid.
                    orientation(y[:3],r[:3],0,V,U)
        return dict(method='reviewed9045 selector, including reversed centers',
                    A_size=len(A),A_degree=degree,**cap)
    need(E==2 and case['t']==1, 'E2t0 is not claimed')
    need((a,b,c)==(2,2,3), 'last E2t1 pair inventory')
    T=[r for r in rows if sum(d>0 for d in r[:3])==3]
    need(len(T)==1 and T[0][:6]==[3,1,1,2,2,0], 'last heavy T scope')
    bad=[r for r in rows if r[4]==1]
    need(len(bad)==1 and bad[0][:6]==[1,0,0,0,1,4], 'last exceptional singleton')
    A=[r for r in rows if r[:5]==[1,0,0,0,0]]
    need(len(A)==7 and sum(r[5] for r in A)==28, 'isolated-cohort edge saturation')
    need(survivor['Q']==3, 'last high-leave budget')
    # Every neighbor of bad[0] lies in A. Isolation at that neighbor
    # makes every high-leave edge touching w at bad[0] impossible.
    return dict(method='high-leave reciprocity contradiction',A_size=7,
                A_degree=28,outside_edges=0,required_q=1,forced_q=0)
