"""Exact finite bounds for a uniform all-source receiving cap.

The elementary support-transport and Neumann arguments are in PROOF.md.
This module checks their finite constants directly against actual originals.
"""
from fractions import Fraction as F

def inverse(c,A):
    Q=c.Q;n=len(A)
    B=[list(row)+[Q(int(i==j)) for j in range(n)] for i,row in enumerate(A)]
    for j in range(n):
        pivot=next((i for i in range(j,n) if B[i][j]!=0),None)
        c.require(pivot is not None,'selected local contact basis is independent')
        B[j],B[pivot]=B[pivot],B[j];d=B[j][j];B[j]=[x/d for x in B[j]]
        for i in range(n):
            if i==j:continue
            d=B[i][j]
            if d!=0:B[i]=[x-d*y for x,y in zip(B[i],B[j])]
    result=tuple(tuple(row[n:]) for row in B)
    c.require(c.matmul(A,result)==tuple(tuple(Q(int(i==j)) for j in range(n)) for i in range(n)),
              'entire exact local inverse product')
    return result

def finite_bounds(c,data,u,cycle,N,radius2,minimum_cut_coefficient,requested_radius=None):
    Q=c.Q;a=c.a;V=c.V
    edges=[a.sub(V[j],V[i]) for i,j in zip(cycle,cycle[1:]+cycle[:1])]
    u2=a.dot(u,u);support_floor=Q(F(1,10000))
    c.require(radius2<Q(F(81,16)),'R<9/4')
    c.require(u[2]<0 and u[2]*u[2]>u2/4,'unit center has z<-1/2')
    for E,i in zip(edges,cycle):
        h=a.dot(a.cross(E,u),V[i])
        c.require(a.dot(E,E)==1,'actual receiving hull edge has original unit length')
        c.require(h>0 and h*h>u2/100,'each physical raw support height exceeds1/10')
    s=Q(0,1);phi=(1+s)/2
    axes=((Q(1),Q(),Q()),(Q(),Q(1),Q()))+tuple(a.scale(1/(2*phi),(Q(1),e*phi,d*phi*phi))
                                                 for e,d in ((-1,-1),(-1,1),(1,-1),(1,1)))
    c.require(all(a.dot(u,m)*a.dot(u,m)<Q(F(119*119,128*128))*u2 for m in axes),
              'unit center projective chord exceeds3/8 from all six minimum axes')
    minimum_weight=None;minimum_mass_slack=None;inverse_norm=None;inverse_cache={};slack_comparisons=0
    for item in data['poses']:
        g=c.matrix(item['proper_matrix_rows']);images=[c.act(g,v) for v in V]
        for i in cycle:
            c.require(V[i] in images,'every original receiver corner has a literal spatial preimage')
        for E,i,j in zip(edges,cycle,cycle[1:]+cycle[:1]):
            for p in images:
                if p in (V[i],V[j]):continue
                hgap=a.dot(a.cross(E,u),a.sub(V[i],p))
                c.require(hgap>0 and hgap*hgap>support_floor*support_floor*u2,
                          'positive normalized whole-source offendpoint support margin')
                slack_comparisons+=1
        for dual in item['coordinate_duals']:
            weights=[c.field(x) for x in dual['weights']]
            c.require(min(weights)>0,'strictly positive point basis weights for continuous repair')
            m=sum(weights,Q());mass_limit=Q((6,7,8)[dual['axis']]);slack=mass_limit-m
            c.require(m<8 and slack>0,'strict point mass slack below uniform6,7,8')
            minimum_weight=min(minimum_weight,min(weights)) if minimum_weight is not None else min(weights)
            minimum_mass_slack=min(minimum_mass_slack,slack) if minimum_mass_slack is not None else slack
            columns=[]
            for i,k in dual['actual_contact_rows']:
                p,n=images[k],N[i]
                c.require(p in (V[cycle[i]],V[cycle[(i+1)%len(cycle)]]),'point dual uses literal actual endpoints')
                columns.append(tuple(a.cross(p,n))+tuple(n[:2]))
            B=tuple(zip(*columns))
            if B not in inverse_cache:inverse_cache[B]=inverse(c,B)
            value=max(sum((c.absolute(x) for x in row),Q()) for row in inverse_cache[B])
            inverse_norm=max(inverse_norm,value) if inverse_norm is not None else value
    J=next(k for k in (1,2,4,8,16,32,64,128,256,512,1024,2048,4096,8192,16384,32768,65536,131072,262144,524288,1048576)
           if inverse_norm<=k)
    c.require(minimum_weight>Q(F(1,160)),'simple strict point-weight floor1/160')
    c.require(minimum_mass_slack>Q(F(1,10)),'simple strict point mass slack1/10')
    c.require(minimum_cut_coefficient>Q(F(1,1000000)),'simple strict global quadratic coefficient floor1/1000000')
    Mn=tuple(tuple(c.IDENTITY[i][j]-2*u[i]*u[j]/u2 for j in range(3)) for i in range(3))
    Mx=((Q(-1),Q(),Q()),(Q(),Q(1),Q()),(Q(),Q(),Q(1)))
    poses=[]
    for item in data['poses']:
        g=c.matrix(item['proper_matrix_rows']);poses.extend((g,c.matmul(c.matmul(Mn,g),Mx)))
    separation2=min(sum(((g[i][j]-h[i][j])*(g[i][j]-h[i][j]) for i in range(3) for j in range(3)),Q())
                    for k,g in enumerate(poses) for h in poses[k+1:])
    c.require(separation2>Q(F(1,100)),'point equality poses have Frobenius separation>1/10')
    def admissible(delta):
        return (0<delta<=Q(F(1,1000)) and 11250*delta<1 and 9*delta<support_floor
             and 6000*J*delta<Q(F(1,2))
             and 96000*J*delta<minimum_weight/2
             and 480000*J*delta<minimum_mass_slack
             and 12*delta<minimum_cut_coefficient)
    if requested_radius is None:
        delta=next(Q(F(1,10**k)) for k in range(3,19) if admissible(Q(F(1,10**k))))
    else:
        delta=requested_radius;c.require(admissible(delta),'explicit whole receiving-cap absorption constants')
    # All these rational inequalities are the actual scalar closure gates.
    c.require(Q(F(13,10))*Q(F(13,10))*149/256<1,'near-receiver Euclidean local absorption')
    c.require(Q(F(8,75))+2*delta<Q(F(11,100)),'moving companion remains in finite relative chart')
    c.require(Q(F(121,10000))<Q(F(4,257)),'operator11/100 implies relative Cayley norm<1/16')
    c.require(Q(F(3,8))-delta>Q(F(1,3)),'whole cap separated from all six minimum axes')
    c.require(6*delta<Q(F(1,10)),'moving equality poses remain distinct')
    return {'explicit_projective_unit_normal_chord_radius':c.enc(delta),
            'whole_source_offendpoint_normalized_margin_floor':c.enc(support_floor),
            'whole_source_offendpoint_margin_comparisons':slack_comparisons,
            'local_selected_inverse_infinity_maximum':c.enc(inverse_norm),
            'integer_uniform_inverse_infinity_bound':J,'different_exact_local_basis_inverses':len(inverse_cache),
            'minimum_strict_point_basis_weight':c.enc(minimum_weight),
            'simple_strict_point_basis_weight_floor':c.enc(Q(F(1,160))),
            'minimum_strict_point_coordinate_mass_slack':c.enc(minimum_mass_slack),
            'simple_strict_point_coordinate_mass_slack_floor':c.enc(Q(F(1,10))),
            'simple_strict_global_quadratic_coefficient_floor':c.enc(Q(F(1,1000000))),
            'normalized_support_Lipschitz_constant':500,'five_component_contact_entry_Lipschitz_constant':1200,
            'five_by_five_matrix_infinity_perturbation_constant':6000,
            'uniform_repaired_coordinate_mass_bounds':[6,7,8],
            'uniform_near_contact_quadratic_constant':c.enc(Q(F(13,10))),
            'closed_near_relative_Cayley_Euclidean_gate':c.enc(Q(F(1,16))),
            'near_local_squared_absorption':c.enc(Q(F(25181,25600))),
            'global_support_cut_transport_Lipschitz_constant':3,
            'strict_global_support_cut_transport_margin':c.enc(minimum_cut_coefficient/4-3*delta),
            'source_hole_reference_radius':c.enc(Q(F(4,75))),
            'moving_companion_operator_upper':c.enc(Q(F(11,100))),
            'point_minimum_equality_pose_Frobenius_distance_squared':c.enc(separation2),
            'whole_cap_minimum_axis_chord_lower':c.enc(Q(F(3,8))-delta)}
