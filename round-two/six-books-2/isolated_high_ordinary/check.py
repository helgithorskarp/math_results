"""Exact compact checks for the ordinary isolated-high neighborhood lemma.

No external input or nonstandard package. Logical proof is in PROOF.md.
The full virtual degree cube, whole terminal rank cube, literal local
capacity identities, and all feasible monotone decrements are checked.
"""
from itertools import combinations,combinations_with_replacement,product
import json,time


def require(condition,message):
    if not condition:raise ValueError(message)


def c2(n):return n*(n-1)//2


def balanced(m):
    q,r=divmod(m,12)
    return 12*c2(q)+r*q


def reject(operation, message):
    try:
        operation()
    except ValueError:
        return
    raise ValueError(message)


def terminal_cover(records, expected, capacity):
    require({tuple(r['beta']) for r in records}==set(expected),
            'Whole terminal column shape cover differs')
    require(all(39-(capacity-r['T'])>r['max_weighted_nine'] for r in records),
            'Actual terminal weighted row contradiction missing')


def degree_coupling(old, new, old_row, new_row, t, coefficient=8):
    require(old-new==coefficient-t and old_row-new_row==1,
            'Actual one-degree coupling differs')


def capacities(degrees,edges,drop_diagonal=False):
    adj=[set() for _ in range(9)]
    for a,b in edges:adj[a].add(b);adj[b].add(a)
    require(not adj[8],'The specified high vertex is not isolated in H')
    t=list(map(len,adj));gamma=[d-1-q for d,q in zip(degrees,t)]
    caps={(a,b):((2 if b in adj[a] else degrees[a]+degrees[b]-15)-len(adj[a]&adj[b]))
          for a,b in combinations(range(9),2)}
    total=sum(caps.values());row=(0 if drop_diagonal else gamma[8])+sum(v for (a,b),v in caps.items() if a==8 or b==8)
    formula=17*len(edges)-540+8*sum(degrees)-sum(d*q+c2(q) for d,q in zip(degrees,t))
    require(total==formula,'Literal whole capacity identity differs')
    require(row==sum(degrees)-41,'Literal isolated-high weighted row/diagonal differs')
    return total,row,t


def run():
    start=time.monotonic();weights=sorted([v+i for v in [8]*5+[10]*3 for i in range(3)])
    minima={};multiplicity={};virtual_degree_vectors=0
    for t in product(range(4),repeat=8):
        virtual_degree_vectors+=1
        if sum(t)%2:continue
        h=sum(t)//2;cost=sum(d*q+c2(q) for d,q in zip([8]*5+[10]*3,t))
        if h not in minima or cost<minima[h]:minima[h]=cost;multiplicity[h]=1
        elif cost==minima[h]:multiplicity[h]+=1
    table=[]
    for h in range(13):
        require(minima[h]==sum(weights[:2*h]),'Whole virtual degree cube/prefix cost differs')
        C=100+17*h-minima[h];M=71-2*h;T=balanced(M)
        if h<=10:require(C<T,'Strict ordinary scalar gap missing')
        table.append(dict(h=h,min_cost=minima[h],C_max=C,M=M,T_min=T,minimizing_vectors=multiplicity[h]))
    require(table[11]['C_max']==77 and table[11]['T_min']==76,'h11 boundary differs')
    require(table[12]['C_max']==70 and table[12]['T_min']==69,'h12 boundary differs')

    # A different finite algorithm: the entire sorted twelve-column rank cube.
    terminal={47:[],49:[]};rank_cube=0
    for beta in combinations_with_replacement(range(10),12):
        rank_cube+=1;load=sum(beta)
        if load not in terminal:continue
        cost=sum(map(c2,beta));limit=70 if load==47 else 77
        if cost<=limit:terminal[load].append(dict(beta=list(beta),T=cost,max_weighted_nine=sum(beta[-9:])))
    expected={47:[(3,)*2+(4,)*9+(5,),(3,)+(4,)*11],
              49:[(3,)+(4,)*9+(5,)*2,(4,)*11+(5,)]}
    for load,records in terminal.items():
        h=11 if load==49 else 12;C=table[h]['C_max']
        terminal_cover(records, expected[load], C)
    damaged=terminal[49][1:]
    reject(lambda:terminal_cover(damaged,expected[49],table[11]['C_max']),
           'Actual terminal rank-profile omission undetected')

    # Literal affine/Boolean-degree-two coefficient basis on all eight-point
    # edge supports of size at most two, plus actual degree-three stars.
    pairs=list(combinations(range(8),2));supports=[()]+[(p,) for p in pairs]+list(combinations(pairs,2))
    bases=[[0]*8]+[[int(a==b) for b in range(8)] for a in range(8)]
    literal_count=0
    for edges in supports:
        for basis in bases:capacities(basis+[10],edges);literal_count+=1
    coupling=0
    for center in range(8):
        edges=tuple((min(center,b),max(center,b)) for b in range(8) if b!=center)[:3]
        degrees=[8]*5+[10]*4;old,row,t=capacities(degrees,edges);lowered=degrees.copy();lowered[center]-=1
        new,new_row,_=capacities(lowered,edges)
        degree_coupling(old,new,row,new_row,t[center])
        reject(lambda:degree_coupling(old,new,row,new_row,t[center],coefficient=7),
               'Actual changed capacity-loss coefficient not rejected')
        coupling+=1
    reject(lambda:capacities([8]*5+[10]*4,(),drop_diagonal=True),
           'Actual isolated-row diagonal mutation undetected')

    require(all(balanced(m)-balanced(m-1)==(m-1)//12 for m in range(1,72)), 'Balanced-load marginal identity differs')
    decrements=0
    for h,r in enumerate(table):
        for delta in range(r['M']-9+1):
            C=r['C_max']-5*delta;T=balanced(r['M']-delta);decrements+=1
            if h<=10 or (h==11 and delta>=2) or (h==12 and delta>=1):
                require(C<T,'Actual monotone scalar gap missing')
            if h==11 and delta==1:
                require(C==T==72 and 39-delta>9*4,'Actual h11 one-decrement row contradiction missing')
    require(time.monotonic()-start<25,'INCOMPLETE compact exact check; no verdict')
    return dict(status='COMPLETE_EXACT_CHECKS',agent='six-books-2',role='researcher',
                claim='Ordinary22 red3/blue6: degree9 root, at least five neighbors degree<=8, all neighbors degree<=10 => every degree10 neighbor has an H neighbor.',
                no_global_profile_or_outside_degree_or_automorphism_hypothesis=True,
                virtual_row_cube=virtual_degree_vectors,isolated_H_edge_cases=13,
                literal_identity_supports=len(supports),literal_identity_cases=literal_count,
                sorted_terminal_rank_cube=rank_cube,terminal_shapes=terminal,
                table=table,exact_degree_coupling_cases=coupling,balanced_marginal_cases=71,
                monotone_decrement_cases=decrements,
                controls=dict(actual_rank_profile_omission_rejected=True,actual_diagonal_damage_rejected=True,
                              actual_capacity_loss_coefficient_damage_rejected=True),
                proof_assistant_formalized=False,independent_person_review=False,threads=1,program_guard_seconds=25)


if __name__=='__main__':print(json.dumps(run(),indent=2,sort_keys=True))
