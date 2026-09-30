#!/usr/bin/env python3
"""Exact hypotheses for the adaptive deltoidal area/roll receiver theorem.

Python3.11+, standard library, Q(sqrt(5))/Fraction only. The geometric
continuum arguments and exact scope are in adaptive_area_proof.md.
"""
import argparse,hashlib,json,re
from fractions import Fraction as F
from pathlib import Path
from verify import Q5,ZERO,vec,vertices,dot,cross,sub,add,mul
from orientation_certificate import build_cells,CERTIFICATES,determinant,area_twice
from global_area_certificate import check as check_parent,root_gap_greater

if not __debug__:
    raise RuntimeError('verification requires assertions; do not use python -O')

PARENT_SHA256='22196b0e3e6449841ac3686cc518aa51d354d41e743ff7599c77f1b6ff39dd32'
AREA_COERCIVITY=F(6)
ROLL_GATE=F(1,28)
ROLL_PROBES=[(57,59,57,1),(41,57,57,-1)]
PATCH_MIX=F(1,20)
PATCH_DRIFT=F(239,100000)
CELL_BALLS={4:F(2,25),7:F(17,100),9:F(2,25)}

def parse(s):
    match=re.fullmatch(r'\(([^)]+)\) \+ \(([^)]+)\)\*sqrt\(5\)',s)
    assert match is not None
    return Q5(F(match.group(1)),F(match.group(2)))

def serial(v):return list(map(str,v))

def finite(parent,coercivity=AREA_COERCIVITY,roll_probes=ROLL_PROBES,
           roll_gate=ROLL_GATE,patch_mix=PATCH_MIX,ball_override=None,
           reverse_contact=False,omit_patch_corner=False):
    V=vertices();cells,triangles=build_cells()
    nodes=[vec(map(parse,x['ray'])) for x in parent['corner_areas']]
    M=nodes[9];qmin=parse(parent['global_minimum_area_squared'])
    assert M in cells[4] and M in cells[7] and M in cells[9]
    assert set(nodes)=={u for p in cells for u in p}

    # Normalization is1-Lipschitz on unit-z chart segments. A vertex gap
    # sqrt(qj)-sqrt(qmin)>2||uj-M||/coercivity gives the global rate.
    assert coercivity>0
    corner_bounds=[]
    for j,u in enumerate(nodes):
        if j==9:continue
        q=parse(parent['corner_areas'][j]['physical_area_squared'])
        dsq=dot(sub(u,M),sub(u,M));assert dsq.sign()>0
        d2=4*dsq/(coercivity*coercivity)
        left=q-qmin-d2
        assert left.sign()>0 and left*left>4*qmin*d2
        corner_bounds.append({'corner':j,'chart_distance_squared':str(dsq),
                              'root_gap_branch_left':str(left),
                              'root_gap_squared_margin':str(left*left-4*qmin*d2)})
    assert len(corner_bounds)==13

    # Both signs of arbitrary C2-reduced roll are handled by actual edges.
    assert {p[3] for p in roll_probes}=={-1,1} and len(roll_probes)==2
    top=parse(parent['minimal_shadow_max_radius_squared'])
    root_gap_greater(top,Q5(5),roll_gate)
    assert 0<roll_gate<F(1,25)
    roll_records=[]
    for a,b,j,sign in roll_probes:
        assert a!=b and j in [a,b]
        normal=cross(sub(V[b],V[a]),M)
        norm2=dot(normal,normal);assert norm2.sign()>0
        h=dot(normal,V[j]);assert h.sign()>0
        assert all(dot(normal,sub(V[j],v)).sign()>=0 for v in V)
        derivative=dot(M,cross(V[j],normal))
        assert derivative.sign()==sign
        h2=h*h/norm2
        tau2=derivative*derivative/(dot(M,M)*norm2)
        assert h2<Q5(F(81,16)) and tau2>Q5(F(9,16))
        roll_records.append({'edge':[a,b],'vertex':j,'roll_sign':sign,
                             'unit_support_squared':str(h2),
                             'unit_roll_derivative_squared':str(tau2)})
    linear_roll_margin=F(99,100)*F(3,4)-F(9,4)*F(1,10)
    assert linear_roll_margin==F(207,400) and linear_roll_margin>F(1,2)
    assert F(101,100)**2*(1-F(1,400))>1
    assert 2*roll_gate<F(1,10) and roll_gate/F(5,2)<F(1,10)
    assert F(303,50)*roll_gate/F(5,2)<F(1,10)
    separation=parse(parent['receiver_halfturn_Frobenius_separation_squared'])
    assert separation>Q5(8*(roll_gate/F(5,2))**2)

    # Four actual weak endpoint supports persist on each WHOLE closed cell.
    support_count=0;cell_records=[]
    for cell in [4,7,9]:
        _,_,sign,original=next(x for x in CERTIFICATES if x[:2]==(cell,0))
        contacts=[tuple(x) for x in original]
        if reverse_contact and cell==7:
            a,b,j=contacts[0];contacts[0]=(b,a,j)
        edges=[sub(V[b],V[a]) for a,b,j in contacts]
        assert all(dot(e,e)<Q5(F(25,16)) for e in edges)
        for u in cells[cell]:
            for (_,_,j),edge in zip(contacts,edges):
                normal=cross(edge,u)
                assert all(dot(normal,sub(V[j],v)).sign()>=0 for v in V)
                support_count+=len(V)
        T=[cross(V[j],cross(e,M)) for (_,_,j),e in zip(contacts,edges)]
        weights=[sign*((-1)**j)*determinant(*(T[k] for k in range(4) if k!=j))
                 for j in range(4)]
        assert all(w.sign()>0 for w in weights)
        assert tuple(sum((weights[j]*T[j][k] for j in range(4)),ZERO)
                     for k in range(3))==vec((0,0,0))
        ball=CELL_BALLS[cell] if ball_override is None else ball_override
        assert ball>0
        distances=[]
        for omitted in range(4):
            a,b,c=[T[j] for j in range(4) if j!=omitted]
            normal=cross(sub(b,a),sub(c,a))
            norm2=dot(normal,normal);assert norm2.sign()>0
            squared=dot(normal,a)**2/norm2
            assert squared>Q5(ball*ball)
            distances.append(squared)
        C=vec(map(parse,parent['cell_certificates'][cell]['area_vector']))
        assert dot(C,M).sign()>0 and dot(C,M)**2/dot(M,M)==qmin
        tangent2=dot(C,C)-qmin
        slope={4:F(2),7:F(4,5),9:F(9,5)}[cell]
        assert tangent2.sign()>0 and tangent2<Q5(slope*slope)
        cell_records.append({'cell':cell,'corner_indices':[nodes.index(u) for u in cells[cell]],
                             'contacts':[list(x) for x in contacts],
                             'cofactor_sign':sign,'center_positive_cofactors':list(map(str,weights)),
                             'center_facet_distance_squared':list(map(str,distances)),
                             'center_ball_lower':str(ball),'edge_norm_upper':'5/4',
                             'tangent_area_slope_squared':str(tangent2),
                             'tangent_area_slope_upper':str(slope)})
    assert support_count==2480

    # Explicit full receiver triangle. These are affine chart rays, not
    # an assumption that physical area maxima occur at polygon corners.
    assert set(cells[7])=={nodes[8],M,nodes[7]} and 0<patch_mix<1
    patch=[M]+[add(M,mul(Q5(patch_mix),sub(nodes[j],M))) for j in [7,8]]
    if omit_patch_corner:patch.pop()
    assert len(patch)==3 and area_twice(patch).sign()!=0
    H=PATCH_DRIFT
    assert all(dot(sub(u,M),sub(u,M))<Q5(H*H) for u in patch)
    assert all(dot(u,u)<Q5(F(121,100)) for u in patch)
    cosine=F(1)-F(1,2*500**2)
    p=dot(M,patch[1]);assert p.sign()>0
    assert cosine*cosine*dot(M,M)*dot(patch[1],patch[1])>p*p
    source=coercivity*F(4,5)*H
    eta=F(5,2)*(source+H)
    theta=F(101,100)*(source+H+2*eta)
    assert eta<roll_gate
    assert source<F(1,10) and H<F(1,10) and 2*eta<F(1,10)
    assert theta<F(1,10)
    margin=CELL_BALLS[7]-F(25,8)*H-F(55,32)*theta
    assert margin>F(1,60)
    parent_normal_digest=hashlib.sha256(json.dumps(parent,sort_keys=True,separators=(',',':')).encode()).hexdigest()
    return {'agent':'six-rupert-1','role':'researcher',
            'status':'exact finite hypotheses for adaptive area criterion and whole receiver triangle',
            'global_Rupert_property':'unresolved','arithmetic':'Q(sqrt(5))/Fraction; standard Python3.11+',
            'parent_expected_sha256':PARENT_SHA256,'parent_normal_output_sha256':parent_normal_digest,
            'global_source_normal_coercivity':str(coercivity),'corner_coercivity_comparisons':13,
            'corner_coercivity_bounds':corner_bounds,
            'complete_reduced_roll_interval':'[-pi/2,pi/2] modulo C2',
            'radial_roll_gate_error':str(roll_gate),'roll_probes':roll_records,
            'roll_probe_all_vertex_support_comparisons':2*len(V),
            'local_roll_chord_upper_per_transport_error':2,
            'linear_roll_positive_margin':str(linear_roll_margin),
            'proper_factor_angle_per_chord_upper':'101/100',
            'adaptive_full_angle_upper':'Theta=(303/50)*(6*(A(n)-Amin)+||n-m||)',
            'adaptive_criterion':'eta=(5/2)*(6*(A(n)-Amin)+||n-m||)<=1/28; r_cell(u)>(25/16)*||u||*Theta',
            'whole_cell_weak_support_comparisons':support_count,'persistent_cell_tetrahedra':cell_records,
            'receiver_triangle_cell':7,'receiver_triangle_affine_mix':str(patch_mix),
            'receiver_triangle_rays':[serial(u) for u in patch],
            'receiver_triangle_chart_drift_upper':str(H),'receiver_triangle_chart_norm_upper':'11/10',
            'receiver_triangle_outer_normal_chord_lower':'1/500',
            'receiver_triangle_source_chord_upper':str(source),
            'receiver_triangle_transport_error_upper':str(eta),
            'receiver_triangle_gauged_full_angle_upper':str(theta),
            'receiver_triangle_torque_remainder_margin':str(margin),
            'closed_classification':'lambda=1,t=0,Q in G union J_n G; two disjoint left cosets',
            'relative_rotations_per_receiver':120,'initial_source_orientation_restriction':'none',
            'strict_passages_on_certified_receiver_domain':'excluded at every source rotation, roll, translation and scale>=1',
            'solver_or_floating_point_proof_decisions':0}

def negative_tests(parent):
    controls=[('unsupported coercivity5',{'coercivity':F(5)}),
              ('missing roll sign',{'roll_probes':ROLL_PROBES[:1]}),
              ('unsupported radial gate1/20',{'roll_gate':F(1,20)}),
              ('reversed actual weak support',{'reverse_contact':True}),
              ('unsupported torque ball1/5',{'ball_override':F(1,5)}),
              ('unsupported triangle mix1/10',{'patch_mix':F(1,10)}),
              ('missing receiver corner',{'omit_patch_corner':True})]
    rejected=[]
    for name,kwargs in controls:
        try:finite(parent,**kwargs)
        except AssertionError:rejected.append(name)
        else:raise AssertionError('malformed certificate accepted: '+name)
    return rejected

def check(self_test=False):
    path=Path(__file__).with_name('expected_global_area.json')
    assert hashlib.sha256(path.read_bytes()).hexdigest()==PARENT_SHA256
    expected=json.loads(path.read_text());assert len(expected.pop('malformed_controls_rejected'))==5
    parent=check_parent();assert parent==expected
    result=finite(parent)
    if self_test:result['malformed_controls_rejected']=negative_tests(parent)
    return result

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--self-test',action='store_true')
    args=parser.parse_args()
    print(json.dumps(check(args.self_test),indent=2))
