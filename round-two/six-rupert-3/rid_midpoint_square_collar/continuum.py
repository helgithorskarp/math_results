"""Fresh original fixed-source feasibility on the ENTIRE closed segment."""
from itertools import combinations
from primitives import F,Z,O,need,dot,cross,sub,encode,projection,turn,hull

def verify(cert,g):
    V,M=g['V'],g['M'];lo,hi=[F(*a) for a in cert['receiving_x_interval']]
    middle=(lo+hi)/2;ring=cert['receiving_ring']
    need(len(ring)==len(set(ring))==18,'actual receiving ring is incomplete or repeated')
    rings={x:[projection(V[i],(x,Z,O)) for i in ring] for x in (lo,middle,hi)}
    turns=[];witness=[];supports=[];endpoint_hulls=[];distinct_pairs=[]
    for ia,ib in combinations(ring,2):
        E=sub(V[ib],V[ia]);reason='fixed distinct second planar coordinate'
        if E[1]==Z and E[2]!=Z:
            critical=E[0]/E[2]
            need(not lo<=critical<=hi,'two literal receiving ring points coincide in the closed interval')
            reason={'only_possible_coincidence_x':critical.encode(),'outside_closed_interval':True}
        elif E[1]==E[2]==Z:
            need(E[0]!=Z,'receiving ring has repeated originals')
            reason='fixed distinct first planar coordinate'
        distinct_pairs.append({'original_pair':[ia,ib],'reason':reason})
    for indices in combinations(range(18),3):
        a,b,k=indices
        values=[turn(rings[x][a],rings[x][b],rings[x][k]) for x in (lo,middle,hi)]
        need(values[1]==(values[0]+values[2])/2 and all(t>=Z for t in values),
             'full cyclic triple is not a nonnegative affine receiving turn')
        turns.append({'indices':list(indices),'all3_full_affine_turn_controls':encode(values)})
        if all(v>Z for v in values):witness.append(list(indices))
    need(witness,'receiving ring degenerates on the entire closed interval')
    edge_nonzero=[]
    for si,ia in enumerate(ring):
        ib=ring[(si+1)%18];E=sub(V[ib],V[ia]);reason='fixed nonzero first component'
        if E[1]==Z and E[2]!=Z:
            critical=E[0]/E[2]
            need(not lo<=critical<=hi,'receiving edge collapses in the closed interval')
            reason={'only_possible_zero_x':critical.encode(),'outside_entire_closed_interval':True}
        elif E[1]==E[2]==Z:
            need(E[0]!=Z,'receiving ring has an identical original edge')
            reason='fixed nonzero second component'
        edge_nonzero.append({'edge':[ia,ib],'nonzero_physical_normal_reason':reason})
        row=[]
        for x in (lo,middle,hi):
            r=(x,Z,O);m=cross(E,r);h=dot(m,V[ia])
            receiving=[h-dot(m,v) for v in V];moving=[h-dot(m,v) for v in M]
            need(h>Z and all(t>=Z for t in receiving+moving),
                 'actual original receiving/moving continuum support fails')
            row.append({'x':x.encode(),'normal':encode(m),'height':h.encode(),
                        'full60_receiving_gaps':encode(receiving),'full60_moving_gaps':encode(moving)})
        for key in ['full60_receiving_gaps','full60_moving_gaps']:
            for j in range(60):
                a,b,k=[F(*row[i][key][j]) for i in range(3)]
                need(b==(a+k)/2,'physical original receiving/moving gap is not affine')
        supports.append({'edge':[ia,ib],'support':si,'all3_full_affine_support_records':row})
    for x in (lo,hi):
        r=(x,Z,O);H=hull([projection(v,r) for v in V]);J=hull([projection(v,r) for v in M])
        need(H==hull(rings[x])
             and all(turn(a,b,w)>=Z for a,b in zip(H,H[1:]+H[:1]) for w in J),
             'full independent endpoint containment or ring completeness fails')
        endpoint_hulls.append({'x':x.encode(),'full_receiving_hull':list(map(encode,H)),
            'full_moving_hull':list(map(encode,J)),'proper_containment':H!=J})
    return {'entire_closed_receiving_x_interval':encode((lo,hi)),
        'actual_original_receiving_ring':ring,'all816_full_affine_cyclic_triples':turns,
        'all_strict_nondegenerate_triples':witness,'all153_distinct_planar_pair_controls':distinct_pairs,
        'all18_nonzero_normal_reasons':edge_nonzero,
        'all18_full_affine_original_supports':supports,
        'all_full_closed_endpoint_receiving_and_moving_support_controls':4320,
        'additional_exact_midpoint_affinity_support_fixtures':2160,
        'all_full_closed_endpoint_cyclic_turn_controls':1632,
        'additional_exact_midpoint_affinity_turn_fixtures':816,
        'independent_full_original_endpoint_hulls':endpoint_hulls,
        'sufficiency_dependency':'NONE: actual original midpoint feasibility throughout the closed interval is rebuilt through affine supports and full weak convex ring order. Ordinary planar polygon bridge required; public9896 is prior context only.'}
