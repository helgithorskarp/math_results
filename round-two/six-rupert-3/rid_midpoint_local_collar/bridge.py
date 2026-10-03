"""Literal nonlinear contact and actual small-rotation exclusion fixtures."""
from pathlib import Path
from itertools import product


from primitives import F,Q,Z,O,phi,vertices,rotate,dot,cross,sub,encode,need,hull,projection,turn

def verify(record,certificate):
    V=vertices()
    need(set(V)=={tuple(-a for a in v) for v in V},'actual original RID centrality fails')
    c=tuple(F(*a) for a in certificate['source_cayley']);M=[rotate(c,v) for v in V]
    need(record['closed_physical_left_Cayley_radius']==certificate['left_Cayley_radius'],'actual physical collar binding differs')
    x0,x1=[F(*v) for v in record['whole_closed_receiving_x_interval']]
    theta=F(Q(certificate['theta_upper']));corners=[(x,x*t,O) for x,t in product((x0,x1),(Z,theta))]
    labels=sorted({tuple(a) for row in record['all6_exact_uniform_torque_duals']
                   for a in row['three_actual_spatial_contacts']})
    ring=certificate['ring']
    basis=[tuple(O if i==j else Z for i in range(3)) for j in range(3)]
    samples=[(Z,Z,Z),*basis,*[tuple(-a for a in v) for v in basis],
             *[tuple(basis[i][j]+basis[k][j] for j in range(3)) for i,k in ((0,1),(0,2),(1,2))]]
    need(len(samples)==10,'complete trivariate quadratic unisolvent grid differs')
    identities=[]
    for r in corners:
        for si,source in labels:
            m=cross(sub(V[ring[(si+1)%18]],V[ring[si]]),r)
            h=dot(m,V[ring[si]]);N=tuple(a/h for a in m);v=M[source]
            need(h>Z and dot(N,v)==O,'actual moved source does not give the original contact')
            for d in samples:
                d2=dot(d,d);literal=(O+d2)*(dot(N,rotate(d,v))-O)
                analytic=2*dot(cross(v,N),d)+2*dot(N,d)*dot(v,d)-2*d2
                need(literal==analytic,'literal nonlinear Rodrigues contact identity differs')
                identities.append({'r':encode(r),'support':si,'source':source,'delta':encode(d),'cleared_contact_value':literal.encode()})
    r=((x0+x1)/2,Z,O);rho=F(Q(certificate['left_Cayley_radius']));controls=[]
    for axis,sign in product(range(3),(-1,1)):
        d=tuple(F(sign)*rho if i==axis else Z for i in range(3));positive=[]
        for si,source in labels:
            m=cross(sub(V[ring[(si+1)%18]],V[ring[si]]),r);h=dot(m,V[ring[si]])
            gap=dot(m,rotate(d,M[source]))-h
            if gap>Z:positive.append({'support':si,'source':source,'strict_actual_gap':gap.encode()})
        need(positive,'actual nonzero rotation control survives all genuine contacts')
        controls.append({'delta':encode(d),'actual_strict_support_violations':positive})
    H=hull([projection(v,r) for v in V]);J=hull([projection(v,r) for v in M])
    need(H!=J and all(turn(a,b,p)>=Z for a,b in zip(H,H[1:]+H[:1]) for p in J),
         'actual delta0 full-hull boundary fit is not retained')
    out={'agent':'six-rupert-3','role':'researcher','actual_original_centrality':True,
         'all_complete_trivariate_quadratic_contact_identities':identities,
         'literal_contact_identity_control_count':len(identities),
         'all6_actual_nonzero_rotation_exclusion_fixtures':controls,
         'actual_delta0_original_receiving_hull':[encode(p) for p in H],
         'actual_delta0_original_moving_hull':[encode(p) for p in J],
         'actual_delta0_proper_closed_fit_retained':True,
         'scope':'Independent definition-level bridge/control checks; uniform dual proof is separate.',
         'global_RID':'OPEN','threads':1}
    return out
