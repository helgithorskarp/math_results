#!/usr/bin/env python3
"""Small abstract fixtures for the quantifier/compiler semantics."""


def controls():
    cases=[]

    def add(name,n,edges,cross,patterns,budget,expected):
        cases.append(dict(name=name,n=n,edges=sorted(edges),cross=sorted(cross),
                          patterns=patterns,budget=budget,expected=expected))

    add('empty',0,[],[],[[]],0,False)
    add('isolated',1,[],[],[[]],1,False)
    for budget in [0,1]:
        add(f'four_forbidden_b{budget}',1,[],[(a,0) for a in range(4)],
            [[0,1,2,3]],budget,budget==1)
    add('three_forbidden',1,[],[(a,0) for a in range(3)],[[0,1,2]],1,False)
    cross=[(a,v) for a in range(3) for v in range(2)]
    for budget in [1,2]:
        add(f'forced_equal_edge_b{budget}',2,[(0,1)],cross,[[0,1,2]],budget,budget==2)
    cross=[(a,0) for a in range(4)]+[(a,1) for a in range(4,8)]
    p0=[0,1,2,3,0,0,0,0]
    p1=[0,0,0,0,0,1,2,3]
    for count in [2,3,20]:
        for budget in [1,2]:
            add(f'common_selection_p{count}_b{budget}',2,[],cross,
                [p0 if j%2==0 else p1 for j in range(count)],budget,budget==2)
    add('permuted_four_colours',1,[],[(a,0) for a in range(4)],[[3,1,0,2]],1,True)
    return cases
